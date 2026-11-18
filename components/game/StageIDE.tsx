"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { CaseResult, Concept, Problem, RunOutcome } from "@/lib/types";
import { show } from "@/lib/format";
import { formatPyArgs, parsePyArgs } from "@/lib/py-args";
import { getRunner } from "@/lib/runner";
import { load, markAttempted, markSolved, save, useStored } from "@/lib/storage";
import CodeEditor, { type Keymap } from "../CodeEditor";
import { RunnerBadge } from "../CodePane";
import LearnMode from "../LearnMode";
import Markdown from "../Markdown";
import { TaskRules } from "../ProblemDescription";
import SolutionBreakdown from "../SolutionBreakdown";
import { useTheme } from "../ThemeToggle";
import "./stage-ide.css";

/**
 * The Learn Python stage IDE: three flush columns.
 * - Problem: the statement, examples and tags, with Problem, Hints, Learn mode and Solution as tab buttons (plus the music visual).
 * - Editor: Vim / Emacs keybindings, a theme switch and Reset.
 * - Console: "Run Code" runs your function on arguments you type; "Run Test Cases" checks the examples; "Submit" runs every test.
 */

type View = "problem" | "lesson" | "hints" | "learn" | "solution";
/** One console row: plain text, or a labelled value ("in", "out", "print"…). */
type Row = { text: string; label?: string; tone?: "head" | "good" | "bad" | "dim" };

const DIFFICULTY_PILL: Record<string, string> = { Easy: "bg-[#3dbb5a]", Medium: "bg-[#d99a1e]", Hard: "bg-[#d9534f]" };

export default function StageIDE({
  problem,
  concepts,
  tags,
  lesson,
  back,
  barRight,
  visual,
  onSubmitted,
  onHintShown,
  onSolutionRevealed,
}: {
  problem: Problem;
  concepts: Concept[];
  /** The concept (or Blind 75 pattern) and the world. */
  tags: string[];
  /** The lesson for this stage's concept group (Learn Python worlds 1-7), shown in the Lesson tab. */
  lesson?: { title: string; intro: string };
  back: { href: string; label: string };
  /** Controls for the top bar's right side (visual and sound switches). */
  barRight?: React.ReactNode;
  /** Fills the space under the problem (the music visual). */
  visual?: React.ReactNode;
  onSubmitted?: (o: RunOutcome) => void;
  onHintShown?: () => void;
  onSolutionRevealed?: () => void;
}) {
  const key = `code:${problem.slug}`;
  const [code, setCode] = useState<string>(() => load<string | null>(key, null) ?? problem.starter);
  const saveTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  useEffect(() => () => clearTimeout(saveTimer.current), []);
  const onCodeChange = (v: string) => {
    setCode(v);
    clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(() => save(key, v), 400);
  };

  const [view, setView] = useState<View>("problem");
  const [hintsShown, setHintsShown] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const keymap = useStored<Keymap>("python:ide-keymap", "default");
  const theme = useTheme();

  // ---- console
  const [rows, setRows] = useState<Row[]>([]);
  const [running, setRunning] = useState(false);
  const autoClear = useStored<boolean>("python:ide-autoclear", true);
  const [input, setInput] = useState(() => (problem.examples[0] ? formatPyArgs(problem.examples[0].args) : ""));
  const logRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight });
  }, [rows]);
  useEffect(() => getRunner().warm(), []);

  const add = (...r: Row[]) => setRows((prev) => [...prev, ...r]);
  const gap: Row = { text: "" };
  const showValue = (v: unknown) => show(problem.spec, v);

  /** One case: its title, in / out / print, and (when judged) a verdict. */
  const logCase = (title: string, args: unknown[], c: CaseResult, expected: unknown, judge: boolean) => {
    const r: Row[] = [{ text: title, tone: "head" }, { label: "in", text: formatPyArgs(args) }];
    if (c.status === "timeout") r.push({ text: "✗ took too long (over 6 s): an infinite loop, or too slow?", tone: "bad" });
    else if (c.error) r.push({ label: "error", text: c.error, tone: "bad" });
    else {
      r.push({ label: "out", text: showValue(c.result) });
      if (judge) r.push(c.status === "pass" ? { text: "✓ correct", tone: "good" } : { text: `✗ expected ${showValue(expected)}`, tone: "bad" });
    }
    if (c.stdout) r.push({ label: "print", text: c.stdout.replace(/\n$/, ""), tone: "dim" });
    r.push(gap);
    add(...r);
  };

  const begin = (title: string) => {
    if (autoClear) setRows([{ text: title, tone: "dim" }, gap]);
    else add(gap, { text: title, tone: "dim" }, gap);
  };

  async function run(kind: "custom" | "run" | "submit") {
    if (running) return;
    let target = problem;
    let customArgs: unknown[] = [];
    if (kind === "custom") {
      try {
        customArgs = parsePyArgs(input);
      } catch (e) {
        begin("▸ Trying your input");
        add({ text: `✗ ${(e as Error).message}`, tone: "bad" });
        return;
      }
      target = { ...problem, examples: [{ args: customArgs, expected: null }] };
    }
    begin(kind === "custom" ? "▸ Trying your input" : kind === "run" ? `▸ Running ${problem.examples.length} example${problem.examples.length === 1 ? "" : "s"}` : `▸ Submitting · ${problem.tests.length} tests`);
    setRunning(true);
    save(key, code);
    try {
      const o = await getRunner().run(target, code, kind === "submit" ? "submit" : "run");
      if (o.stdout) add({ label: "print", text: o.stdout.replace(/\n$/, ""), tone: "dim" }, gap);
      if (o.compileError) {
        add({ text: o.compileError.startsWith("Task rule:") ? "✗ Task rule not met" : "✗ Your code didn't load", tone: "bad" }, { text: o.compileError, tone: "dim" });
      } else if (kind === "custom") {
        logCase("Your input", customArgs, o.cases[0], null, false);
      } else if (kind === "run") {
        o.cases.forEach((c, i) => logCase(`Example ${i + 1}`, o.tests[i].args, c, o.tests[i].expected, true));
        const ok = o.passed === o.total;
        add({ text: ok ? `✓ All ${o.total} examples pass. Submit when ready.` : `${o.passed} of ${o.total} examples pass`, tone: ok ? "good" : "bad" });
      } else {
        // Submit: only what failed (hidden tests included), then the score.
        const failed = o.cases.map((c, i) => [c, i] as const).filter(([c]) => c.status !== "pass");
        failed.slice(0, 3).forEach(([c, i]) => logCase(i < problem.examples.length ? `Example ${i + 1}` : `Hidden test ${i - problem.examples.length + 1}`, o.tests[i].args, c, o.tests[i].expected, true));
        if (failed.length > 3) add({ text: `… and ${failed.length - 3} more`, tone: "dim" }, gap);
        add(o.passed === o.total ? { text: `✓ All ${o.total} tests passed`, tone: "good" } : { text: `${o.passed} of ${o.total} tests passed`, tone: "bad" });
      }
      if (kind !== "custom") markAttempted(problem.slug);
      if (kind === "submit") {
        if (!o.compileError && o.passed === o.total) markSolved(problem.slug);
        onSubmitted?.(o);
      }
    } catch (e) {
      add({ text: `✗ Python failed to load: ${String(e)}. Check your connection and try again.`, tone: "bad" });
    } finally {
      setRunning(false);
    }
  }

  const toggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    save("theme", next);
  };

  // ---- pieces
  const barBtn = "inline-flex items-center gap-1.5 rounded px-3 py-1.5 text-sm font-medium text-(--ide-btn-fg) bg-(--ide-btn) hover:brightness-110 disabled:opacity-60";

  // Tabs: the selected one is filled; the others are outlined.
  const tabBtn = (id: View, label: string) => (
    <button
      type="button"
      role="tab"
      aria-selected={view === id}
      onClick={() => setView(id)}
      className={`rounded border px-3 py-1 text-sm font-medium transition-colors ${
        view === id
          ? "border-(--ide-tab-on) bg-(--ide-tab-on) text-white shadow-sm"
          : "border-(--ide-line) bg-(--ide-tab) text-(--ide-tab-fg) hover:border-(--ide-tab-on) hover:text-(--ide-tab-on)"
      }`}
    >
      {label}
    </button>
  );

  const toneClass: Record<NonNullable<Row["tone"]>, string> = {
    head: "font-semibold text-(--ide-text)",
    good: "font-medium text-[#2fae4e]",
    bad: "text-[#e5534b]",
    dim: "text-(--ide-muted)",
  };

  return (
    <div
      className="stage-ide flex min-w-0 flex-1 flex-col text-(--ide-text) lg:h-[calc(100vh-var(--header-h))] lg:flex-none lg:overflow-hidden"
    >
      <div className="flex min-h-12 items-center justify-between gap-2 border-b border-(--ide-line) bg-panel px-4 text-sm">
        <Link href={back.href} className="text-muted hover:text-fg">
          ← {back.label}
        </Link>
        {barRight}
      </div>

      <div className="grid min-h-0 min-w-0 flex-1 grid-cols-1 lg:grid-cols-[minmax(0,0.95fr)_minmax(0,1.2fr)_minmax(0,0.95fr)] lg:grid-rows-[minmax(0,1fr)]">
        {/* ---- problem */}
        <section className="flex min-h-0 min-w-0 flex-col overflow-auto border-(--ide-line) bg-(--ide-problem) lg:border-r">
          <div className="flex min-h-full flex-col gap-5 p-5">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-(--ide-line) pb-4">
              <span className={`rounded px-2 py-0.5 text-sm text-white lowercase ${DIFFICULTY_PILL[problem.difficulty] ?? "bg-subtle"}`}>{problem.difficulty}</span>
              <div className="flex flex-wrap gap-2" role="tablist" aria-label="Problem panel">
                {tabBtn("problem", "Problem")}
                {lesson && tabBtn("lesson", "Lesson")}
                {tabBtn("hints", `Hints${problem.hints.length ? ` (${problem.hints.length})` : ""}`)}
                {problem.grammar.length > 0 && tabBtn("learn", "Learn mode")}
                {tabBtn("solution", "Solution")}
              </div>
            </div>

            {view === "problem" && (
              <>
                <div className="flex flex-col gap-3">
                  <h1 className="text-xl font-bold text-(--ide-text)">{problem.title}</h1>
                  <Markdown>{problem.desc}</Markdown>
                  <TaskRules problem={problem} />
                </div>
                <div className="flex flex-col gap-3">
                  <h2 className="text-lg font-bold text-(--ide-text)">Examples</h2>
                  {problem.examples.map((ex, i) => (
                    <pre key={i} className="overflow-x-auto rounded bg-(--ide-example) px-3 py-2.5 font-mono text-[13px] leading-6 whitespace-pre-wrap text-(--ide-text)">
                      {`Input: ${formatPyArgs(ex.args)}\n${problem.spec.out === "stdout" ? "Prints:" : "Output:"} ${showValue(ex.expected)}`}
                    </pre>
                  ))}
                </div>
                {tags.length > 0 && (
                  <div className="flex flex-col gap-3">
                    <h2 className="text-lg font-bold text-(--ide-text)">Tags</h2>
                    <div className="flex flex-wrap gap-2">
                      {tags.map((t) => (
                        <span key={t} className="rounded bg-(--ide-chip) px-2.5 py-1 text-sm text-(--ide-chip-fg)">
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {visual && <div className="min-h-[280px] flex-1">{visual}</div>}
              </>
            )}

            {view === "hints" && (
              <div className="flex flex-col gap-3">
                {problem.hints.length === 0 && <p className="text-sm text-(--ide-muted)">This task has no hints. Try Learn mode for the building blocks.</p>}
                {problem.hints.slice(0, hintsShown).map((h, i) => (
                  <div key={i} className="rounded border border-(--ide-line) bg-(--ide-example) p-3">
                    <div className="mb-1 text-xs text-(--ide-muted)">Hint {i + 1}</div>
                    <Markdown>{h}</Markdown>
                  </div>
                ))}
                {hintsShown < problem.hints.length && (
                  <button
                    type="button"
                    onClick={() => {
                      setHintsShown(hintsShown + 1);
                      onHintShown?.();
                    }}
                    className={`self-start ${barBtn}`}
                  >
                    Show hint {hintsShown + 1}
                  </button>
                )}
              </div>
            )}

            {view === "lesson" && lesson && (
              <div className="flex flex-col gap-3">
                <p className="text-xs tracking-wide text-(--ide-muted) uppercase">Lesson</p>
                <h2 className="text-lg font-bold text-(--ide-text)">{lesson.title}</h2>
                <Markdown>{lesson.intro}</Markdown>
              </div>
            )}

            {view === "learn" && <LearnMode sections={problem.grammar} />}

            {view === "solution" &&
              (revealed ? (
                <div className="flex flex-col gap-4">
                  <Markdown>{problem.explanation}</Markdown>
                  <SolutionBreakdown code={problem.solution} lineTags={problem.lineTags} concepts={Object.fromEntries(concepts.map((c) => [c.id, c]))} />
                  <button type="button" onClick={() => onCodeChange(problem.solution)} className="self-start text-xs text-(--ide-link) hover:underline">
                    Load solution into editor
                  </button>
                </div>
              ) : (
                <div className="flex flex-col items-start gap-3">
                  <p className="text-sm text-(--ide-muted)">Revealing the solution caps this stage at 1 leaf. Give it a real try first.</p>
                  <button
                    type="button"
                    onClick={() => {
                      setRevealed(true);
                      onSolutionRevealed?.();
                    }}
                    className={barBtn}
                  >
                    Reveal solution
                  </button>
                </div>
              ))}
          </div>
        </section>

        {/* ---- editor */}
        <section className="flex min-h-[420px] min-w-0 flex-col border-(--ide-line) bg-(--ide-editor) lg:min-h-0 lg:border-r">
          <div className="flex flex-wrap items-center justify-end gap-3 px-3 py-2">
            {(["vim", "emacs"] as const).map((k) => (
              <button
                key={k}
                type="button"
                aria-pressed={keymap === k}
                onClick={() => save("python:ide-keymap", keymap === k ? "default" : k)}
                title={keymap === k ? "Back to normal editing" : `Use ${k === "vim" ? "Vim" : "Emacs"} keybindings`}
                className={`px-1 text-sm ${keymap === k ? "font-semibold text-(--ide-link) underline underline-offset-4" : "text-(--ide-link) opacity-70 hover:opacity-100"}`}
              >
                {k === "vim" ? "Vim" : "Emacs"}
              </button>
            ))}
            <button type="button" onClick={toggleTheme} className={barBtn}>
              {theme === "dark" ? "☀ Light" : "☾ Dark"}
            </button>
            <button type="button" onClick={() => window.confirm("Reset to the starter code? Your current code will be lost.") && onCodeChange(problem.starter)} className={barBtn}>
              ↺ Reset
            </button>
          </div>
          <div className="min-h-0 flex-1">
            <CodeEditor value={code} onChange={onCodeChange} onRun={() => run("run")} onSubmit={() => run("submit")} keymap={keymap} />
          </div>
        </section>

        {/* ---- console */}
        <section className="flex min-h-[420px] min-w-0 flex-col bg-(--ide-console) lg:min-h-0">
          <div className="flex flex-wrap items-center gap-2 px-3 py-2">
            <button type="button" disabled={running} onClick={() => run("custom")} className={`${barBtn} bg-(--ide-run) text-white`} title="Run your function on the input below (Enter)">
              <PlayIcon />
              Run Code
            </button>
            <button type="button" disabled={running} onClick={() => run("run")} className={barBtn} title="Run the examples (⌘/Ctrl + Enter)">
              <TestsIcon />
              Run Test Cases
            </button>
            <button type="button" disabled={running} onClick={() => run("submit")} className={barBtn} title="Run every test, including hidden ones (⌘/Ctrl + Shift + Enter)">
              Submit
            </button>
          </div>
          <div className="px-3">
            <label htmlFor="ide-input" className="sr-only">
              Arguments for Run Code
            </label>
            <input
              id="ide-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && run("custom")}
              spellCheck={false}
              placeholder="Arguments, e.g. [1, 2], 3"
              className="w-full rounded border border-(--ide-line) bg-(--ide-input) px-3 py-2 font-mono text-sm text-(--ide-input-fg) outline-none [font-variant-ligatures:none] focus:border-(--ide-link)"
            />
          </div>
          <div className="flex items-center justify-between gap-3 px-3 pt-2 text-sm">
            <RunnerBadge />
            <div className="flex gap-4">
              <button
                type="button"
                aria-pressed={autoClear}
                onClick={() => save("python:ide-autoclear", !autoClear)}
                title="Clear the log before each run"
                className={`text-(--ide-link) ${autoClear ? "underline underline-offset-4" : "opacity-60"}`}
              >
                Auto-clear
              </button>
              <button type="button" onClick={() => setRows([])} className="text-(--ide-link)">
                Clear log
              </button>
            </div>
          </div>
          <div ref={logRef} className="min-h-0 flex-1 overflow-auto px-3 py-3 font-mono text-[13px] leading-6 [font-variant-ligatures:none]" aria-live="polite">
            {rows.length === 0 && !running && (
              <p className="opacity-60">Run Code runs your function on the arguments above. Run Test Cases checks the examples; Submit runs every test.</p>
            )}
            {rows.map((r, i) =>
              r.label ? (
                <div key={i} className={`grid grid-cols-[3.5rem_minmax(0,1fr)] ${r.tone ? toneClass[r.tone] : ""}`}>
                  <span className="text-(--ide-muted)">{r.label}</span>
                  <span className="break-words whitespace-pre-wrap">{r.text}</span>
                </div>
              ) : (
                <div key={i} className={`min-h-6 break-words whitespace-pre-wrap ${r.tone ? toneClass[r.tone] : ""}`}>
                  {r.text}
                </div>
              ),
            )}
            {running && <div className="opacity-60">Running…</div>}
          </div>
        </section>
      </div>
    </div>
  );
}

function PlayIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true">
      <path d="M2.5 1.5v9l8-4.5z" fill="currentColor" />
    </svg>
  );
}

/** A small checklist: what Run Test Cases runs. */
function TestsIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
      <rect x="1.75" y="2.25" width="4.5" height="4.5" rx="0.75" />
      <rect x="1.75" y="9.25" width="4.5" height="4.5" rx="0.75" />
      <path d="M8.5 4.5h5.5M8.5 11.5h5.5" />
    </svg>
  );
}
