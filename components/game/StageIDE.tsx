"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { CaseResult, Concept, Problem, RunOutcome } from "@/lib/types";
import { clipText, show } from "@/lib/format";
import { formatPyArgs, parsePyArgs } from "@/lib/py-args";
import { edgeCases, runCaseIndexes } from "@/lib/edge-cases";
import { getRunner } from "@/lib/runner";
import { load, markAttempted, markSolved, save, useStored } from "@/lib/storage";
import CodeEditor, { type Keymap } from "../CodeEditor";
import { RunnerBadge } from "../CodePane";
import LearnMode from "../LearnMode";
import Markdown from "../Markdown";
import { PaneHandle, usePaneSplit } from "../PaneSplit";
import { TaskRules } from "../ProblemDescription";
import SolutionBreakdown from "../SolutionBreakdown";
import { useTheme } from "../ThemeToggle";
import "./stage-ide.css";

/**
 * The Learn Python stage IDE: three flush columns.
 * - Problem: the statement and examples, with Problem, Hints, Learn mode and Solution as tab buttons (plus the music visual).
 * - Editor: a "?" that shows the concept's lesson on hover, Vim / Emacs keybindings, a theme switch and Reset.
 * - Console: "Run Code" runs your function on arguments you type; "Run Test Cases" checks the examples; "Submit" runs every test.
 *   Run Test Cases also runs every labelled edge case; the edge cases are listed at the bottom (click one for its input and
 *   expected output) and turn green or red after each run.
 */

type View = "problem" | "hints" | "learn" | "solution";
/** One console row: plain text, or a labelled value ("in", "out", "print"…). */
type Row = { text: string; label?: string; tone?: "head" | "good" | "bad" | "dim" };

const DIFFICULTY_PILL: Record<string, string> = { Easy: "bg-[#3dbb5a]", Medium: "bg-[#d99a1e]", Hard: "bg-[#d9534f]" };

export default function StageIDE({
  problem,
  concepts,
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
  /** The lesson for this stage's concept group (Learn Python worlds 1-7), shown by hovering the "?" in the editor bar. */
  lesson?: { title: string; intro: string };
  back: { href: string; label: string };
  /** Controls for the top bar's right side (visual and sound switches). */
  barRight?: React.ReactNode;
  /** Fills the space under the problem (the music visual). */
  visual?: React.ReactNode;
  onSubmitted?: (o: RunOutcome) => void;
  /** Called with the number of the hint just opened (1 for the first). */
  onHintShown?: (n: number) => void;
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
  /** Whether the Examples list under the statement is expanded (click the heading to toggle; remembered across stages). */
  const examplesOpen = useStored<boolean>("python:ide-examples-open", true);
  const theme = useTheme();
  // Column widths (problem, editor, console); drag the lines between them to resize.
  const split = usePaneSplit("python:ide-columns", [0.95, 1.2, 0.95]);

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
  // Edge cases: labelled tests (an example can carry a label too). Run Test Cases checks the examples and every edge case;
  // Submit adds the hidden tests. `results` keeps each test's latest result from either, by its index in problem.tests.
  const edges = edgeCases(problem);
  const runIdx = runCaseIndexes(problem);
  const exampleCount = problem.examples.length;
  const edgeRunCount = runIdx.length - exampleCount;
  const hiddenCount = problem.tests.length - runIdx.length;
  const [results, setResults] = useState<Record<number, CaseResult>>({});
  const [openEdge, setOpenEdge] = useState<number | null>(null);
  // The Test cases list shows the first few; "View more" reveals the rest of the visible (non-hidden) ones.
  const CASES_SHOWN = 3;
  const [allCasesShown, setAllCasesShown] = useState(false);
  const shownEdges = allCasesShown ? edges : edges.slice(0, CASES_SHOWN);
  const moreCases = edges.length - CASES_SHOWN;
  // Each labelled test is shown as "Case 1", "Case 2"… in list order; its note describes it in the detail view.
  const caseNo = Object.fromEntries(edges.map((e, n) => [e.i, n + 1])) as Record<number, number>;
  const caseLabel = (i: number) => `Case ${caseNo[i]}`;
  const caseTitle = (i: number) => {
    const note = problem.tests[i]?.note;
    if (i < exampleCount) return note ? `Example ${i + 1} · ${caseLabel(i)}` : `Example ${i + 1}`;
    return note ? caseLabel(i) : `Hidden test ${i - exampleCount + 1}`;
  };
  const record = (o: RunOutcome, idx: number[]) => setResults((prev) => ({ ...prev, ...Object.fromEntries(o.cases.map((c, j) => [idx[j], c])) }));
  const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? "" : "s"}`;
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
      target = { ...problem, examples: [{ args: customArgs, expected: null }], tests: [] };
    }
    begin(
      kind === "custom"
        ? "▸ Trying your input"
        : kind === "run"
          ? `▸ Running ${plural(exampleCount, "example")}${edgeRunCount ? ` and ${plural(edgeRunCount, "edge case")}` : ""}`
          : `▸ Submitting · ${plural(problem.tests.length, "test")}${hiddenCount ? ` (${hiddenCount} hidden)` : ""}`,
    );
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
        o.cases.forEach((c, j) => logCase(caseTitle(runIdx[j]), o.tests[j].args, c, o.tests[j].expected, true));
        const ok = o.passed === o.total;
        const next = o.ruleNote ? "" : hiddenCount ? ` Submit also runs ${plural(hiddenCount, "hidden test")}.` : " Submit when ready.";
        add({ text: ok ? `✓ All ${o.total} pass.${next}` : `${o.passed} of ${o.total} pass`, tone: ok ? "good" : "bad" });
        record(o, runIdx);
      } else {
        // Submit: only what failed (hidden tests included), then the score.
        const failed = o.cases.map((c, i) => [c, i] as const).filter(([c]) => c.status !== "pass");
        failed.slice(0, 3).forEach(([c, i]) => logCase(caseTitle(i), o.tests[i].args, c, o.tests[i].expected, true));
        if (failed.length > 3) add({ text: `… and ${failed.length - 3} more`, tone: "dim" }, gap);
        if (edges.length > 0) {
          add({ text: "Test cases", tone: "head" });
          edges.forEach((e) => add(o.cases[e.i]?.status === "pass" ? { text: `✓ ${caseLabel(e.i)}`, tone: "good" } : { text: `✗ ${caseLabel(e.i)}`, tone: "bad" }));
          add(gap);
        }
        record(o, o.cases.map((_, i) => i));
        add(o.passed === o.total ? { text: `✓ All ${o.total} tests passed`, tone: "good" } : { text: `${o.passed} of ${o.total} tests passed`, tone: "bad" });
      }
      if (o.ruleNote) add(gap, { text: `! Submit will fail until this is fixed: ${o.ruleNote}`, tone: "bad" });
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

  // Tabs: the selected one is filled; the others are outlined. They tighten as the problem column narrows (container
  // queries on the column) so the pill and all four tabs stay on one line; they only wrap when the column is very narrow.
  const tabBtn = (id: View, label: React.ReactNode) => (
    <button
      type="button"
      role="tab"
      aria-selected={view === id}
      onClick={() => setView(id)}
      className={`rounded border px-2.5 py-1 text-[13px] font-medium whitespace-nowrap transition-colors @max-[25rem]:px-2 @max-[25rem]:text-xs @max-[19rem]:px-1 ${
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

      <div style={split.style} className="grid min-h-0 min-w-0 flex-1 grid-cols-1 lg:grid-cols-(--pane-cols) lg:grid-rows-[minmax(0,1fr)]">
        {/* ---- problem */}
        <section data-pane className="flex min-h-0 min-w-0 flex-col overflow-auto border-(--ide-line) bg-(--ide-problem) lg:border-r">
          <div className="@container flex min-h-full flex-col gap-5 p-5">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-(--ide-line) pb-4 @max-[25rem]:gap-1.5">
              <span className={`shrink-0 rounded px-2 py-0.5 text-sm text-white lowercase @max-[25rem]:px-1.5 @max-[25rem]:text-xs @max-[19rem]:px-1 ${DIFFICULTY_PILL[problem.difficulty] ?? "bg-subtle"}`}>
                {problem.difficulty}
              </span>
              <div className="flex flex-wrap gap-1.5 @max-[25rem]:gap-1" role="tablist" aria-label="Problem panel">
                {tabBtn("problem", "Problem")}
                {tabBtn("hints", `Hints${problem.hints.length ? ` (${problem.hints.length})` : ""}`)}
                {problem.grammar.length > 0 &&
                  tabBtn(
                    "learn",
                    <>
                      Learn<span className="@max-[21rem]:hidden"> mode</span>
                    </>,
                  )}
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
                <div className="flex flex-col">
                  <h2 className="text-lg font-bold text-(--ide-text)">
                    <button
                      type="button"
                      aria-expanded={examplesOpen}
                      aria-controls="stage-examples"
                      onClick={() => save("python:ide-examples-open", !examplesOpen)}
                      className="transition-colors duration-200 ease-out hover:text-(--ide-link) motion-reduce:transition-none"
                      title={examplesOpen ? "Hide the examples" : "Show the examples"}
                    >
                      Examples
                    </button>
                  </h2>
                  {/* Collapses by animating the row from its content height to 0 (and back). */}
                  <div
                    id="stage-examples"
                    inert={!examplesOpen}
                    className={`grid transition-[grid-template-rows,opacity] duration-300 ease-out motion-reduce:transition-none ${examplesOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"}`}
                  >
                    <div className="flex min-h-0 flex-col gap-3 overflow-hidden pt-3">
                      {problem.examples.map((ex, i) => (
                        <pre key={i} className="overflow-x-auto rounded bg-(--ide-example) px-3 py-2.5 font-mono text-[13px] leading-6 whitespace-pre-wrap text-(--ide-text)">
                          {`Input: ${formatPyArgs(ex.args)}\n${problem.spec.out === "stdout" ? "Prints:" : "Output:"} ${showValue(ex.expected)}`}
                        </pre>
                      ))}
                    </div>
                  </div>
                </div>
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
                      onHintShown?.(hintsShown + 1);
                    }}
                    className={`self-start ${barBtn}`}
                  >
                    Show hint {hintsShown + 1}
                  </button>
                )}
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

        <PaneHandle label="Resize the problem and editor panes" className="text-(--ide-link)" {...split.handle(0)} />

        {/* ---- editor */}
        <section data-pane className="flex min-h-[420px] min-w-0 flex-col border-(--ide-line) bg-(--ide-editor) lg:min-h-0 lg:border-r">
          <div className="flex flex-wrap items-center justify-end gap-3 px-3 py-2">
            {lesson && <LessonPeek lesson={lesson} />}
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

        <PaneHandle label="Resize the editor and console panes" className="text-(--ide-link)" {...split.handle(1)} />

        {/* ---- console */}
        <section data-pane className="flex min-h-[420px] min-w-0 flex-col bg-(--ide-console) lg:min-h-0">
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
              <p className="opacity-60">Use &quot;Run Code&quot;, &quot;Run Test Cases&quot; and &quot;Submit&quot; to gather information and pass this level.</p>
            )}
            {rows.map((r, i) =>
              r.label ? (
                <div key={i} className={`grid grid-cols-[3.5rem_minmax(0,1fr)] ${r.tone ? toneClass[r.tone] : ""}`}>
                  <span className="text-(--ide-muted)">{r.label}</span>
                  <span className="break-words whitespace-pre-wrap">{clipText(r.text)}</span>
                </div>
              ) : (
                <div key={i} className={`min-h-6 break-words whitespace-pre-wrap ${r.tone ? toneClass[r.tone] : ""}`}>
                  {clipText(r.text)}
                </div>
              ),
            )}
            {running && <div className="opacity-60">Running…</div>}
          </div>
          {edges.length > 0 && (
            <div className="max-h-[50%] overflow-auto border-t border-(--ide-line) px-3 py-3">
              <p className="mb-2 text-xs font-semibold tracking-wide text-(--ide-muted) uppercase">Test cases</p>
              <ul className="flex flex-wrap gap-1.5 text-[13px]">
                {shownEdges.map((e) => {
                  const r = results[e.i];
                  const ok = r && r.status === "pass";
                  return (
                    <li key={e.i}>
                      <button
                        type="button"
                        aria-expanded={openEdge === e.i}
                        onClick={() => setOpenEdge(openEdge === e.i ? null : e.i)}
                        className={`rounded px-2 py-0.5 ${!r ? "bg-(--ide-chip) text-(--ide-chip-fg)" : ok ? "bg-[#2fae4e]/15 text-[#2fae4e]" : "bg-[#e5534b]/15 text-[#e5534b]"} ${
                          openEdge === e.i ? "ring-1 ring-(--ide-link)" : ""
                        }`}
                      >
                        {!r ? "" : ok ? "✓ " : "✗ "}
                        {caseLabel(e.i)}
                      </button>
                    </li>
                  );
                })}
                {moreCases > 0 && (
                  <li className="self-center">
                    <button
                      type="button"
                      onClick={() => {
                        if (allCasesShown && openEdge !== null && !edges.slice(0, CASES_SHOWN).some((e) => e.i === openEdge)) setOpenEdge(null);
                        setAllCasesShown(!allCasesShown);
                      }}
                      className="px-1 text-xs text-(--ide-link) transition-colors duration-200 hover:underline"
                    >
                      {allCasesShown ? "View less" : `View ${moreCases} more`}
                    </button>
                  </li>
                )}
                {hiddenCount > 0 && (allCasesShown || moreCases <= 0) && (
                  <li className="self-center pl-1 text-xs text-(--ide-muted)" title="Submit runs these too; their inputs stay hidden.">
                    + {plural(hiddenCount, "hidden test case")}
                  </li>
                )}
              </ul>
              {openEdge !== null && problem.tests[openEdge] && (
                <EdgeDetail
                  label={caseLabel(openEdge)}
                  test={problem.tests[openEdge]}
                  result={results[openEdge]}
                  stdout={problem.spec.out === "stdout"}
                  showValue={showValue}
                  onUse={() => setInput(formatPyArgs(problem.tests[openEdge].args))}
                />
              )}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

/** One edge case opened from the console: its input, the expected output, and your latest result. */
function EdgeDetail({
  label,
  test,
  result,
  stdout,
  showValue,
  onUse,
}: {
  label: string;
  test: { args: unknown[]; expected: unknown; note?: string };
  result?: CaseResult;
  stdout: boolean;
  showValue: (v: unknown) => string;
  onUse: () => void;
}) {
  const row = (label: string, text: string, tone = "") => (
    <div className={`grid grid-cols-[5.5rem_minmax(0,1fr)] ${tone}`}>
      <span className="text-(--ide-muted)">{label}</span>
      <span className="break-words whitespace-pre-wrap">{text}</span>
    </div>
  );
  return (
    <div className="mt-3 rounded bg-(--ide-example) p-3 font-mono text-[13px] leading-6 [font-variant-ligatures:none]">
      <p className="mb-1 font-sans text-(--ide-text)">
        <span className="font-semibold">{label}</span>
        {test.note && <span className="text-(--ide-muted)"> · {test.note}</span>}
      </p>
      {row("input", formatPyArgs(test.args))}
      {row(stdout ? "prints" : "expected", showValue(test.expected))}
      {result &&
        (result.status === "timeout"
          ? row("yours", "took too long (over 6 s)", "text-[#e5534b]")
          : result.error
            ? row("yours", result.error, "text-[#e5534b]")
            : row("yours", showValue(result.result), result.status === "pass" ? "text-[#2fae4e]" : "text-[#e5534b]"))}
      <button type="button" onClick={onUse} className="mt-2 font-sans text-xs text-(--ide-link) hover:underline">
        Use this input to run your code
      </button>
    </div>
  );
}

/** A "?" that shows the concept's lesson while hovered or focused (cursor: help). Clicking pins it open; Escape closes it. */
function LessonPeek({ lesson }: { lesson: { title: string; intro: string } }) {
  const [pinned, setPinned] = useState(false);
  return (
    <div className="lesson-peek relative" data-open={pinned || undefined} onKeyDown={(e) => e.key === "Escape" && setPinned(false)}>
      <button
        type="button"
        aria-label={`Lesson: ${lesson.title}`}
        aria-expanded={pinned}
        onClick={() => setPinned(!pinned)}
        className="grid h-6 w-6 cursor-help place-items-center rounded-full border border-(--ide-line) text-sm font-semibold text-(--ide-link) hover:border-(--ide-link)"
      >
        ?
      </button>
      <div className="lesson-peek-card" role="tooltip">
        <div className="flex flex-col gap-3 rounded border border-(--ide-line) bg-(--ide-problem) p-4 text-(--ide-text) shadow-xl">
          <p className="text-xs tracking-wide text-(--ide-muted) uppercase">Lesson</p>
          <h2 className="text-lg font-bold">{lesson.title}</h2>
          <Markdown>{lesson.intro}</Markdown>
        </div>
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
