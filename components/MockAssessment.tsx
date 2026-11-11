"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { Difficulty, Problem, RunOutcome } from "@/lib/types";
import { clock, difficultyColor } from "@/lib/format";
import { getRunner } from "@/lib/runner";
import { load, save, useSolved, useStored } from "@/lib/storage";
import CodeEditor from "./CodeEditor";
import CodePane from "./CodePane";
import ProblemDescription from "./ProblemDescription";
import Recorder, { type Recording } from "./Recorder";

type Item = {
  problem: Problem;
  code: string;
  startedAt?: number;
  submittedAt?: number;
  passed?: number;
  total?: number;
  rec?: Recording | null;
};

type Phase = "setup" | "coding" | "explain" | "summary";

type HistoryEntry = {
  at: number;
  minutes: number;
  usedSec: number;
  problems: { slug: string; title: string; difficulty: Difficulty; passed: number | null; total: number; codingSec: number | null; explainSec: number | null }[];
};

const EMPTY_HISTORY: HistoryEntry[] = [];

function difficultyPlan(n: number): Difficulty[] {
  if (n === 1) return ["Medium"];
  const plan: Difficulty[] = Array(n).fill("Medium");
  plan[0] = "Easy";
  if (n >= 3) plan[n - 1] = "Hard";
  return plan;
}

function shuffle<T>(a: T[]): T[] {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}

function pickProblems(all: Problem[], n: number, excludeSolved: Record<string, number> | null): Problem[] {
  const used = new Set<string>();
  return difficultyPlan(n).map((d) => {
    const ofDiff = all.filter((p) => p.difficulty === d && !used.has(p.slug));
    const fresh = excludeSolved ? ofDiff.filter((p) => !excludeSolved[p.slug]) : ofDiff;
    const pool = fresh.length ? fresh : ofDiff.length ? ofDiff : all.filter((p) => !used.has(p.slug));
    const p = shuffle(pool)[0];
    used.add(p.slug);
    return p;
  });
}

export default function MockAssessment({ problems }: { problems: Problem[] }) {
  const solved = useSolved();
  const history = useStored<HistoryEntry[]>("mock-history", EMPTY_HISTORY);

  // Raw text so fields can be cleared and retyped; clamped values are derived below.
  const [countRaw, setCountRaw] = useState("3");
  const [minutesRaw, setMinutesRaw] = useState("90");
  const [explainRaw, setExplainRaw] = useState("3");
  const clampInt = (raw: string, lo: number, hi: number, fallback: number) => {
    const n = Math.round(Number(raw));
    return raw.trim() === "" || !Number.isFinite(n) ? fallback : Math.min(hi, Math.max(lo, n));
  };
  const count = clampInt(countRaw, 1, 5, 3);
  const minutes = clampInt(minutesRaw, 1, 240, 90);
  const explainMin = clampInt(explainRaw, 1, 10, 3);
  const [includeSolved, setIncludeSolved] = useState(false);

  const [phase, setPhase] = useState<Phase>("setup");
  const [items, setItems] = useState<Item[]>([]);
  const [idx, setIdx] = useState(0);
  const [startAt, setStartAt] = useState(0);
  const [deadline, setDeadline] = useState(0);
  const [now, setNow] = useState(0);
  const [timeUp, setTimeUp] = useState(false);
  const [endAt, setEndAt] = useState(0);

  // Latest state for the timer callback.
  const live = useRef({ phase, items, idx });
  useEffect(() => {
    live.current = { phase, items, idx };
  });

  const active = phase === "coding" || phase === "explain";

  useEffect(() => {
    if (!active) return;
    const onBeforeUnload = (e: BeforeUnloadEvent) => e.preventDefault();
    window.addEventListener("beforeunload", onBeforeUnload);
    return () => window.removeEventListener("beforeunload", onBeforeUnload);
  }, [active]);

  // Guards against the time-up handler firing twice (e.g. several queued ticks after the tab sleeps).
  const timeUpFired = useRef(false);

  useEffect(() => {
    if (!active || timeUp) return;
    const t = setInterval(() => {
      const n = Date.now();
      setNow(n);
      if (n >= deadline && !timeUpFired.current) {
        timeUpFired.current = true;
        setTimeUp(true);
        onTimeUp();
      }
    }, 500);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [active, deadline, timeUp]);

  function start() {
    getRunner().warm();
    const picked = pickProblems(problems, count, includeSolved ? null : solved);
    const t = Date.now();
    setItems(picked.map((p, i) => ({ problem: p, code: p.starter, startedAt: i === 0 ? t : undefined })));
    setIdx(0);
    setStartAt(t);
    setDeadline(t + minutes * 60_000);
    setNow(t);
    setTimeUp(false);
    timeUpFired.current = false;
    setPhase("coding");
  }

  function updateItem(i: number, patch: Partial<Item>) {
    setItems((prev) => prev.map((it, j) => (j === i ? { ...it, ...patch } : it)));
  }

  function submissionPatch(it: Item, o: RunOutcome): Partial<Item> {
    return { submittedAt: Date.now(), passed: o.compileError ? 0 : o.passed, total: o.total || it.problem.tests.length };
  }

  async function onTimeUp() {
    const { phase: ph, items: its, idx: i } = live.current;
    if (ph !== "coding") return; // in the explain phase, let the recording finish; the button then shows results
    const it = its[i];
    const o = await getRunner().run(it.problem, it.code, "submit").catch(() => null);
    const final = o ? its.map((x, j) => (j === i ? { ...x, ...submissionPatch(x, o) } : x)) : its;
    setItems(final);
    finish(final);
  }

  function next() {
    if (timeUp || idx === items.length - 1) return finish(items);
    const n = idx + 1;
    updateItem(n, { startedAt: Date.now() });
    setIdx(n);
    setPhase("coding");
  }

  function finish(final: Item[]) {
    const end = Math.min(Date.now(), deadline);
    setEndAt(end);
    setPhase("summary");
    const entry: HistoryEntry = {
      at: Date.now(),
      minutes,
      usedSec: Math.round((end - startAt) / 1000),
      problems: final.map((it) => ({
        slug: it.problem.slug,
        title: it.problem.title,
        difficulty: it.problem.difficulty,
        passed: it.passed ?? null,
        total: it.problem.tests.length,
        codingSec: it.startedAt && it.submittedAt ? Math.round((it.submittedAt - it.startedAt) / 1000) : null,
        explainSec: it.rec?.seconds ?? null,
      })),
    };
    save("mock-history", [entry, ...load<HistoryEntry[]>("mock-history", [])].slice(0, 30));
  }

  function reset() {
    items.forEach((it) => it.rec && URL.revokeObjectURL(it.rec.url));
    setItems([]);
    setPhase("setup");
  }

  const remaining = (deadline - now) / 1000;
  const item = items[idx];

  // ------------------------------------------------------------------ setup
  if (phase === "setup") {
    const num = "w-20 rounded-md border border-line bg-panel px-2 py-1 text-sm text-fg";
    return (
      <div className="mx-auto w-full max-w-2xl px-4 py-8">
        <h1 className="text-2xl font-semibold text-fg">Mock assessment</h1>
        <p className="mt-2 text-sm leading-6 text-muted">
          Simulates a timed online assessment. Problems appear one at a time, in order, and get harder as you go. When you submit a problem its code locks, then you record a
          short webcam explanation of it. <b className="text-fg-2">The clock keeps running while you record</b>, so budget time for it. Hints and solutions are hidden.
        </p>

        <div className="mt-6 grid gap-4 rounded-lg border border-line p-5 sm:grid-cols-2">
          <label className="flex items-center justify-between gap-3 text-sm text-fg-2">
            Problems
            <input type="number" min={1} max={5} value={countRaw} onChange={(e) => setCountRaw(e.target.value)} onBlur={() => setCountRaw(String(count))} className={num} />
          </label>
          <label className="flex items-center justify-between gap-3 text-sm text-fg-2">
            Time limit (min)
            <input type="number" min={1} max={240} value={minutesRaw} onChange={(e) => setMinutesRaw(e.target.value)} onBlur={() => setMinutesRaw(String(minutes))} className={num} />
          </label>
          <label className="flex items-center justify-between gap-3 text-sm text-fg-2">
            Explanation max (min)
            <input type="number" min={1} max={10} value={explainRaw} onChange={(e) => setExplainRaw(e.target.value)} onBlur={() => setExplainRaw(String(explainMin))} className={num} />
          </label>
          <label className="flex items-center gap-2 text-sm text-fg-2">
            <input type="checkbox" checked={includeSolved} onChange={(e) => setIncludeSolved(e.target.checked)} />
            Include problems I&apos;ve solved
          </label>
          <div className="text-xs text-subtle sm:col-span-2">Difficulty order: {difficultyPlan(count).join(" → ")}</div>
        </div>

        <button onClick={start} className="mt-6 rounded-md bg-accent px-6 py-2.5 text-sm font-bold text-on-accent hover:bg-accent-hover">
          Start ({minutes} min)
        </button>

        {history.length > 0 && (
          <div className="mt-10">
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-fg-2">Past sessions</h2>
            <ul className="divide-y divide-line rounded-lg border border-line text-sm">
              {history.map((h) => {
                const full = h.problems.filter((p) => p.passed === p.total).length;
                return (
                  <li key={h.at} className="flex flex-wrap items-center justify-between gap-2 px-4 py-2.5">
                    <span className="text-muted">{new Date(h.at).toLocaleString()}</span>
                    <span className="text-fg-2">
                      {full}/{h.problems.length} fully passed
                    </span>
                    <span className="text-subtle">
                      {clock(h.usedSec)} of {h.minutes}:00
                    </span>
                    <span className="w-full text-xs text-subtle">
                      {h.problems.map((p) => `${p.title} (${p.passed ?? "–"}/${p.total})`).join(" · ")}
                    </span>
                  </li>
                );
              })}
            </ul>
          </div>
        )}
      </div>
    );
  }

  // ------------------------------------------------------------------ summary
  if (phase === "summary") {
    return (
      <div className="mx-auto w-full max-w-4xl px-4 py-8">
        <h1 className="text-2xl font-semibold text-fg">Results</h1>
        <p className="mt-1 text-sm text-muted">
          {timeUp ? "Time ran out. " : ""}Total time used: {clock((endAt - startAt) / 1000)} of {minutes}:00
        </p>
        <div className="mt-6 space-y-4">
          {items.map((it, i) => {
            const codingSec = it.startedAt && it.submittedAt ? (it.submittedAt - it.startedAt) / 1000 : null;
            const full = it.passed !== undefined && it.passed === it.total;
            return (
              <div key={it.problem.slug} className="rounded-lg border border-line p-4">
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <div className="flex items-baseline gap-3">
                    <span className="text-subtle">{i + 1}.</span>
                    <Link href={`/problems/${it.problem.slug}`} className="font-medium text-fg hover:underline">
                      {it.problem.title}
                    </Link>
                    <span className={`text-xs ${difficultyColor[it.problem.difficulty]}`}>{it.problem.difficulty}</span>
                  </div>
                  <div className="text-sm">
                    {it.passed === undefined ? (
                      <span className="text-subtle">Not submitted</span>
                    ) : (
                      <span className={full ? "text-ok" : "text-bad"}>
                        {it.passed}/{it.total} tests
                      </span>
                    )}
                    {codingSec !== null && <span className="ml-3 text-subtle">coding {clock(codingSec)}</span>}
                    {it.rec && <span className="ml-3 text-subtle">explanation {clock(it.rec.seconds)}</span>}
                  </div>
                </div>
                {it.rec && <video src={it.rec.url} controls playsInline className="mt-3 max-h-72 rounded-md bg-black" />}
                {it.passed !== undefined && (
                  <details className="mt-3">
                    <summary className="cursor-pointer text-xs text-subtle hover:text-fg-2">Your code</summary>
                    <pre className="mt-2 overflow-auto rounded-md bg-panel p-3 font-mono text-xs text-fg-2">{it.code}</pre>
                  </details>
                )}
              </div>
            );
          })}
        </div>
        <p className="mt-4 text-xs text-subtle">Recordings exist only in this tab and disappear when you leave the page.</p>
        <button onClick={reset} className="mt-6 rounded-md border border-line-strong px-4 py-2 text-sm text-fg hover:bg-hover">
          New mock assessment
        </button>
      </div>
    );
  }

  // ------------------------------------------------------------------ coding / explain
  const header = (
    <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line px-4 py-2 text-sm">
      <div className="flex items-center gap-3">
        <span className="font-medium text-fg">Mock assessment</span>
        <span className="text-subtle">
          Problem {idx + 1} of {items.length} · {phase === "coding" ? "coding" : "explanation"}
        </span>
      </div>
      <div className="flex items-center gap-4">
        <span className={`font-mono text-base tabular-nums ${remaining < 600 ? "text-bad" : remaining < 1800 ? "text-warn" : "text-fg"}`}>
          {clock(remaining)}
        </span>
        <button onClick={() => window.confirm("End the assessment now?") && finish(items)}className="text-xs text-subtle hover:text-fg-2">
          End
        </button>
      </div>
    </div>
  );

  if (phase === "coding") {
    return (
      <div className="flex flex-1 flex-col lg:h-[calc(100vh-3rem)] lg:overflow-hidden">
        {header}
        <div className="grid min-h-0 flex-1 grid-cols-1 lg:grid-cols-2">
          <section className="overflow-auto border-line p-5 lg:border-r">
            <ProblemDescription problem={item.problem} />
          </section>
          <section className="h-[85vh] min-h-0 lg:h-auto">
            <CodePane
              key={idx}
              problem={item.problem}
              code={item.code}
              onCodeChange={(v) => updateItem(idx, { code: v })}
              submitLabel="Submit & explain"
              confirmSubmit="Submit this problem? Its code locks and you move on to the explanation."
              onSubmitted={(o) => {
                updateItem(idx, submissionPatch(item, o));
                setPhase("explain");
              }}
            />
          </section>
        </div>
      </div>
    );
  }

  // explain
  const isLast = idx === items.length - 1;
  return (
    <div className="flex flex-1 flex-col lg:h-[calc(100vh-3rem)] lg:overflow-hidden">
      {header}
      <div className="grid min-h-0 flex-1 grid-cols-1 lg:grid-cols-2">
        <section className="flex min-h-[50vh] flex-col border-line lg:border-r">
          <div className="border-b border-line px-4 py-2 text-xs text-muted">
            Submitted code (read-only). Highlight the part you&apos;re explaining as you talk.
          </div>
          <div className="min-h-0 flex-1">
            <CodeEditor value={item.code} readOnly />
          </div>
        </section>
        <section className="overflow-auto p-5">
          <div className="mb-4 flex items-baseline justify-between">
            <h2 className="font-medium text-fg">{item.problem.title}</h2>
            <span className={item.passed === item.total ? "text-sm text-ok" : "text-sm text-bad"}>
              {item.passed}/{item.total} tests passed
            </span>
          </div>
          {timeUp && <div className="mb-4 rounded-md border border-rose-700/50 bg-rose-500/10 px-3 py-2 text-sm text-bad">Time&apos;s up. Finish this explanation, then see your results.</div>}
          <Recorder key={idx} maxSeconds={explainMin * 60} onRecorded={(r) => updateItem(idx, { rec: r })} />
          <div className="mt-5 rounded-lg border border-line bg-panel p-4 text-sm text-muted">
            <div className="mb-2 font-medium text-fg-2">Cover these points</div>
            <ul className="list-disc space-y-1 pl-5">
              <li>The approach in one sentence, and why you chose it</li>
              <li>Walk through the key lines (the highlighted part)</li>
              <li>Time and space complexity</li>
              <li>Edge cases you handled (empty input, duplicates, negatives…)</li>
              <li>What you&apos;d improve with more time, or why tests failed</li>
            </ul>
          </div>
          <button onClick={next} className="mt-5 rounded-md bg-accent px-5 py-2 text-sm font-bold text-on-accent hover:bg-accent-hover">
            {timeUp || isLast ? "Finish & see results" : "Next problem →"}
          </button>
          {!item.rec && <span className="ml-3 text-xs text-subtle">You can continue without recording.</span>}
        </section>
      </div>
    </div>
  );
}
