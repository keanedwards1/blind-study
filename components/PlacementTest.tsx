"use client";

import Link from "next/link";
import { useState } from "react";
import type { Problem, RunOutcome } from "@/lib/types";
import { loadDraft, placedLevel, saveDraft, savePlacement, useHydrated, usePlacement } from "@/lib/python-progress";
import { useMusic } from "@/lib/audio/engine";
import CodePane from "./CodePane";
import ProblemDescription from "./ProblemDescription";
import PageLoader from "./loader/PageLoader";

type Task = { level: number; problem: Problem };
type Results = (boolean | null)[];

export default function PlacementTest({ tasks, levelTitles }: { tasks: Task[]; levelTitles: Record<number, string> }) {
  // Everything here comes from localStorage, so render it only after hydration.
  const hydrated = useHydrated();
  if (!hydrated) return <PageLoader variant="workspace" label="Loading placement test" />;
  return <PlacementFlow tasks={tasks} levelTitles={levelTitles} />;
}

/** The test is over once every task is answered, or as soon as one is missed (a miss fixes your level). */
function isFinished(results: Results) {
  return results.includes(false) || results.every((r) => r !== null);
}

function PlacementFlow({ tasks, levelTitles }: { tasks: Task[]; levelTitles: Record<number, string> }) {
  const placement = usePlacement();
  useMusic("forestCalm");
  const [results, setResults] = useState<Results | null>(() => {
    const draft = loadDraft();
    return draft && draft.length === tasks.length ? draft : null;
  });

  function update(next: Results | null) {
    setResults(next);
    if (next && isFinished(next)) {
      savePlacement({ level: placedLevel(tasks.map((t) => t.level), next), at: Date.now(), results: next });
      saveDraft(null);
    } else {
      saveDraft(next);
    }
  }

  if (!results) {
    return (
      <div className="page-shell mx-auto max-w-2xl space-y-5">
        <h1 className="text-2xl font-semibold text-fg">Placement test</h1>
        <ul className="list-disc space-y-2 pl-5 text-sm leading-6 text-muted">
          <li>
            {tasks.length} coding tasks, two per level, from &quot;return a value&quot; (level 1) up to Blind 75 Hard (level 10). It uses the same editor and tests as the
            problem pages.
          </li>
          <li>
            A task counts as passed when <b className="text-fg-2">Submit</b> passes every hidden test. If it fails, you can keep trying.
          </li>
          <li>
            Press <b className="text-fg-2">Can&apos;t solve</b> (next to Submit) to skip a task. It counts as missed.
          </li>
          <li>Your level is the first level where you miss a task, so the test ends at your first miss. Pass all of them and you start at level 10.</li>
          <li>Your progress is saved, so you can leave and come back. Retaking the test never removes problems you&apos;ve solved.</li>
        </ul>
        {placement && <p className="text-sm text-subtle">You&apos;re currently placed at level {placement.level}. Finishing this test replaces that.</p>}
        <div className="flex gap-3">
          <button onClick={() => update(tasks.map(() => null))} className="rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-500">
            Start the test
          </button>
          <Link href="/python" className="rounded-md border border-line-strong px-4 py-2 text-sm text-fg-2 hover:bg-hover">
            Back
          </Link>
        </div>
      </div>
    );
  }

  if (isFinished(results)) return <ResultsView tasks={tasks} results={results} levelTitles={levelTitles} onRetake={() => update(tasks.map(() => null))} />;

  const index = results.indexOf(null);
  return <TaskView key={tasks[index].problem.slug} tasks={tasks} index={index} results={results} onAnswer={(ok) => update(results.map((r, i) => (i === index ? ok : r)))} />;
}

function TaskView({ tasks, index, results, onAnswer }: { tasks: Task[]; index: number; results: Results; onAnswer: (ok: boolean) => void }) {
  const { problem, level } = tasks[index];
  const [code, setCode] = useState(problem.starter);
  const [failed, setFailed] = useState(false);

  function onSubmitted(o: RunOutcome) {
    if (!o.compileError && o.passed === o.total) onAnswer(true);
    else setFailed(true);
  }

  return (
    <div className="page-workspace flex flex-1 flex-col lg:h-[calc(100vh-var(--header-h))] lg:overflow-hidden">
      {/* Equal-width outer columns keep the progress dots centred on the page. */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2 border-b border-line px-4 py-2 text-sm">
        <div className="flex min-w-0 items-center gap-3">
          <Link href="/python" className="text-muted hover:text-fg">
            ← Learn Python
          </Link>
          <span className="font-medium text-fg">
            Task {index + 1} / {tasks.length}
          </span>
          <span className="text-subtle">Level {level}</span>
        </div>
        <div className="flex items-center gap-1" aria-label="Progress">
          {tasks.map((_, i) => (
            <span key={i} className={`h-2 w-2 rounded-full ${results[i] === true ? "bg-ok" : i === index ? "bg-accent" : "bg-line-strong"}`} />
          ))}
        </div>
        <div aria-hidden />
      </div>
      <div className="grid min-h-0 min-w-0 flex-1 grid-cols-1 lg:grid-cols-2 lg:grid-rows-[minmax(0,1fr)]">
        {/* Same structure as Workspace: a tab row (styled by .page-workspace in globals.css), then the padded scroll area. */}
        <section className="flex min-h-0 min-w-0 flex-col border-line lg:border-r">
          <div className="flex border-b border-line px-2">
            <span className="border-b-2 border-accent px-3 py-2 text-sm text-fg">Description</span>
          </div>
          <div className="flex-1 overflow-auto p-5">
          <div className="mx-auto max-w-3xl space-y-4">
            <ProblemDescription problem={problem} />
            {failed && (
              <p className="rounded-md border border-line bg-panel p-3 text-sm text-muted">
                Not all tests passed yet. Fix it and submit again, or press <b className="text-fg-2">Can&apos;t solve</b>.
              </p>
            )}
          </div>
          </div>
        </section>
        <section className="h-[85vh] min-h-0 min-w-0 lg:h-auto">
          <CodePane
            problem={problem}
            code={code}
            onCodeChange={setCode}
            onSubmitted={onSubmitted}
            onReset={() => setCode(problem.starter)}
            extraAction={
              <button
                onClick={() => window.confirm("Mark this task as can't solve? It counts as missed, which ends the test and places you at this level.") && onAnswer(false)}
                className="rounded-md bg-orange-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-orange-500"
              >
                Can&apos;t solve
              </button>
            }
          />
        </section>
      </div>
    </div>
  );
}

function ResultsView({ tasks, results, levelTitles, onRetake }: { tasks: Task[]; results: Results; levelTitles: Record<number, string>; onRetake: () => void }) {
  const level = placedLevel(tasks.map((t) => t.level), results);
  const allPassed = results.every((r) => r === true);
  const levelNums = [...new Set(tasks.map((t) => t.level))];
  return (
    <div className="page-shell mx-auto max-w-2xl space-y-5">
      <h1 className="text-2xl font-semibold text-fg">You&apos;re starting at level {level}</h1>
      <p className="text-sm text-muted">
        <b className="text-fg-2">{levelTitles[level]}.</b>{" "}
        {allPassed
          ? "You passed every task, so you start at the top level."
          : `You missed a level ${level} task, so that's where you start. Levels below it are marked as placed out: they stay open for practice but aren't required.`}
      </p>
      <div className="grid grid-cols-5 gap-2 sm:grid-cols-10">
        {levelNums.map((lv) => {
          const marks = tasks.map((t, i) => (t.level === lv ? results[i] : undefined)).filter((r) => r !== undefined);
          return (
            <div key={lv} className={`rounded-md border p-2 text-center ${lv === level ? "border-accent" : "border-line"}`}>
              <div className="text-xs text-subtle">L{lv}</div>
              <div className="text-sm">
                {marks.map((m, i) => (
                  <span key={i} className={m === true ? "text-ok" : m === false ? "text-bad" : "text-subtle"}>
                    {m === true ? "✓" : m === false ? "✗" : "–"}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
      <div className="flex flex-wrap gap-3">
        <Link href={`/python/world/${level}`} className="rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-500">
          Go to level {level}
        </Link>
        <button onClick={() => window.confirm("Start the placement test again?") && onRetake()} className="rounded-md border border-line-strong px-4 py-2 text-sm text-fg-2 hover:bg-hover">
          Retake the test
        </button>
      </div>
    </div>
  );
}
