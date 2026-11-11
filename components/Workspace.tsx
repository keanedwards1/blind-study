"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { Concept, PatternGuide, Problem, ProblemSummary, RunOutcome } from "@/lib/types";
import { load, markAttempted, markSolved, save, useSolved } from "@/lib/storage";
import CodePane from "./CodePane";
import LearnTab from "./LearnTab";
import SolutionBreakdown from "./SolutionBreakdown";
import Markdown from "./Markdown";
import ProblemDescription from "./ProblemDescription";

type Tab = "desc" | "learn" | "hints" | "solution";

export default function Workspace({
  problem,
  prev,
  next,
  pattern,
  concepts,
}: {
  problem: Problem;
  prev?: ProblemSummary;
  next?: ProblemSummary;
  pattern: PatternGuide;
  concepts: Concept[];
}) {
  const key = `code:${problem.slug}`;
  const [code, setCode] = useState<string>(() => load<string | null>(key, null) ?? problem.starter);
  const [tab, setTab] = useState<Tab>("desc");
  const [hintsShown, setHintsShown] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const solved = useSolved();
  const saveTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  useEffect(() => () => clearTimeout(saveTimer.current), []);

  function onCodeChange(v: string) {
    setCode(v);
    clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(() => save(key, v), 400);
  }

  function onRan() {
    markAttempted(problem.slug);
    save(key, code);
  }

  function onSubmitted(o: RunOutcome) {
    if (!o.compileError && o.passed === o.total) markSolved(problem.slug);
  }

  const tabBtn = (id: Tab, label: string) => (
    <button
      onClick={() => setTab(id)}
      className={`px-3 py-2 text-sm ${tab === id ? "border-b-2 border-accent text-fg" : "text-subtle hover:text-fg-2"}`}
    >
      {label}
    </button>
  );

  return (
    <div className="flex flex-1 flex-col lg:h-[calc(100vh-3rem)] lg:overflow-hidden">
      <div className="flex items-center justify-between gap-2 border-b border-line px-4 py-2 text-sm">
        <Link href="/" className="text-muted hover:text-fg">
          ← Problems
        </Link>
        <div className="flex items-center gap-3">
          {solved[problem.slug] && <span className="rounded bg-emerald-500/15 px-2 py-0.5 text-xs text-ok">Solved</span>}
          {prev && (
            <Link href={`/problems/${prev.slug}`} className="text-muted hover:text-fg" title={prev.title}>
              ‹ Prev
            </Link>
          )}
          {next && (
            <Link href={`/problems/${next.slug}`} className="text-muted hover:text-fg" title={next.title}>
              Next ›
            </Link>
          )}
        </div>
      </div>

      <div className="grid min-h-0 flex-1 grid-cols-1 lg:grid-cols-2">
        <section className="flex min-h-0 flex-col border-line lg:border-r">
          <div className="flex border-b border-line px-2">
            {tabBtn("desc", "Description")}
            {tabBtn("learn", "Learn")}
            {tabBtn("hints", `Hints (${problem.hints.length})`)}
            {tabBtn("solution", "Solution")}
          </div>
          <div className="flex-1 overflow-auto p-5">
            {tab === "desc" && <ProblemDescription problem={problem} />}

            {tab === "learn" && <LearnTab problem={problem} pattern={pattern} concepts={concepts} />}

            {tab === "hints" && (
              <div className="space-y-3">
                {problem.hints.slice(0, hintsShown).map((h, i) => (
                  <div key={i} className="rounded-lg border border-line bg-panel p-3">
                    <div className="mb-1 text-xs text-subtle">Hint {i + 1}</div>
                    <Markdown>{h}</Markdown>
                  </div>
                ))}
                {hintsShown < problem.hints.length ? (
                  <button onClick={() => setHintsShown(hintsShown + 1)} className="rounded-md border border-line-strong px-3 py-1.5 text-sm text-fg-2 hover:bg-hover">
                    Show hint {hintsShown + 1}
                  </button>
                ) : (
                  <p className="text-sm text-subtle">That&apos;s all the hints.</p>
                )}
              </div>
            )}

            {tab === "solution" &&
              (revealed ? (
                <div className="space-y-4">
                  <Markdown>{problem.explanation}</Markdown>
                  <SolutionBreakdown code={problem.solution} lineTags={problem.lineTags} concepts={Object.fromEntries(concepts.map((c) => [c.id, c]))} />
                  <button onClick={() => onCodeChange(problem.solution)} className="text-xs text-subtle hover:text-fg-2">
                    Load solution into editor
                  </button>
                </div>
              ) : (
                <div className="flex flex-col items-start gap-3">
                  <p className="text-sm text-muted">Try for at least 20–30 minutes before looking. Understanding the solution matters more than seeing it.</p>
                  <button onClick={() => setRevealed(true)} className="rounded-md border border-line-strong px-3 py-1.5 text-sm text-fg-2 hover:bg-hover">
                    Reveal solution & explanation
                  </button>
                </div>
              ))}
          </div>
        </section>

        <section className="h-[85vh] min-h-0 lg:h-auto">
          <CodePane
            problem={problem}
            code={code}
            onCodeChange={onCodeChange}
            onRan={onRan}
            onSubmitted={onSubmitted}
            onReset={() => onCodeChange(problem.starter)}
          />
        </section>
      </div>
    </div>
  );
}
