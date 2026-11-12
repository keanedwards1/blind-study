"use client";

import Link from "next/link";
import { useRef, useState } from "react";
import type { QuizQuestion } from "@/lib/types";
import { difficultyColor } from "@/lib/format";
import Markdown from "./Markdown";
import { load } from "@/lib/storage";
import { QuizCard, kindLabel, resetQuizStats, useQuizStats, type QuizStats } from "./Quiz";

export type DrillContext =
  | { kind: "problem"; title: string; difficulty: string; statement: string; example: string; solution: string }
  | { kind: "pattern"; title: string; summary: string; signals: string[]; template: string }
  | { kind: "concept"; title: string; summary: string; snippet: string; output: string; usedIn: { slug: string; title: string }[]; usedInTotal: number };

export type DrillQuestion = QuizQuestion & {
  source: "problem" | "python" | "pattern" | "basics" | "terms";
  sourceTitle: string;
  href?: string;
  category?: string;
  context?: DrillContext;
};

const reveal: Record<DrillContext["kind"], string> = {
  problem: "Show the reference solution",
  pattern: "Show the pattern template",
  concept: "Show example code",
};

/** What the question is about, so it can be answered without leaving the drill. */
function ContextPanel({ context, href }: { context: DrillContext; href: string }) {
  const [showCode, setShowCode] = useState(false);
  const heading = { problem: "Problem", pattern: "Pattern", concept: "Python concept" }[context.kind];
  const code = context.kind === "problem" ? context.solution : context.kind === "pattern" ? context.template : context.snippet;
  return (
    <div className="mt-3 rounded-xl border border-line bg-raised/60 p-4" data-testid="quiz-context">
      <div className="mb-1 flex items-baseline justify-between gap-2">
        <div className="text-xs font-semibold uppercase tracking-wide text-subtle">{heading}</div>
        <Link href={href} className="text-xs text-subtle underline hover:text-fg-2">
          Open full {heading.toLowerCase()} →
        </Link>
      </div>
      <h2 className="font-semibold text-fg">
        {context.title}
        {context.kind === "problem" && <span className={`ml-2 text-xs font-normal ${difficultyColor[context.difficulty]}`}>{context.difficulty}</span>}
      </h2>
      {context.kind === "problem" && (
        <>
          <Markdown>{context.statement}</Markdown>
          <pre className="mt-2 overflow-auto rounded-md bg-panel p-3 font-mono text-[12.5px] leading-6 text-fg-2">{context.example}</pre>
        </>
      )}
      {context.kind === "pattern" && (
        <>
          <Markdown>{context.summary}</Markdown>
          <Markdown>{"**When to use it:**\n" + context.signals.map((s) => `- ${s}`).join("\n")}</Markdown>
        </>
      )}
      {context.kind === "concept" && (
        <>
          <Markdown>{context.summary}</Markdown>
          {context.usedIn.length > 0 && (
            <div className="mt-2">
              <div className="mb-1.5 text-xs text-subtle">
                You&apos;ll need this in {context.usedInTotal} problem{context.usedInTotal === 1 ? "" : "s"}, including:
              </div>
              <div className="flex flex-wrap gap-1.5">
                {context.usedIn.map((p) => (
                  <Link key={p.slug} href={`/problems/${p.slug}`} className="rounded-full border border-line bg-panel px-2.5 py-0.5 text-xs text-fg-2 hover:border-line-strong hover:text-fg">
                    {p.title}
                  </Link>
                ))}
              </div>
            </div>
          )}
        </>
      )}
      <button onClick={() => setShowCode(!showCode)} className="mt-2 text-xs font-medium text-fg-2 underline hover:text-fg">
        {showCode ? "Hide code" : reveal[context.kind]}
      </button>
      {showCode && (
        <pre className="mt-2 overflow-auto rounded-md bg-panel p-3 font-mono text-[12.5px] leading-6 text-fg">
          {code}
          {context.kind === "concept" && context.output && <span className="text-subtle">{"\n# output:\n" + context.output.split("\n").map((l) => "# " + l).join("\n")}</span>}
        </pre>
      )}
    </div>
  );
}

type Source = "all" | DrillQuestion["source"];
type Show = "all" | "unanswered" | "missed";

function shuffle<T>(a: T[]): T[] {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}

/** One quiz per question source, each tracked to 100%. Ordered from first steps to the full problem set. */
type QuizSetDef = { source: DrillQuestion["source"]; title: string; description: string };
const QUIZ_SETS: QuizSetDef[] = [
  {
    source: "basics",
    title: "Python basics",
    description: "Variables, control flow, containers, text, and the built-in functions useful for solving problems. One idea per question.",
  },
  { source: "terms", title: "Programming terms", description: "Plain-language definitions for algorithms, data structures, complexity, and common Python concepts." },
  { source: "python", title: "Problem-solving Python", description: "The Python tools used across the problem set. Each question links to problems that use it." },
  { source: "pattern", title: "Pattern guides", description: "When to reach for each pattern, how its template works, and the mistakes to avoid." },
  { source: "problem", title: "Problems", description: "The key insight, pattern, and time and space complexity of every problem." },
];

type Tally = { total: number; right: number; missed: number; fresh: number };

/** "Right" means the most recent answer was correct, so a question you later miss drops back out. */
function tally(qs: DrillQuestion[], stats: QuizStats): Tally {
  let right = 0;
  let missed = 0;
  for (const q of qs) {
    const s = stats[q.id];
    if (s?.last) right++;
    else if (s) missed++;
  }
  return { total: qs.length, right, missed, fresh: qs.length - right - missed };
}

const pct = (t: Tally) => (t.total ? Math.floor((t.right / t.total) * 100) : 0);

/** Right / to retry / new, as one segmented bar. */
function ProgressBar({ t, className = "h-2" }: { t: Tally; className?: string }) {
  const w = (n: number) => `${t.total ? (n / t.total) * 100 : 0}%`;
  return (
    <div
      className={`flex overflow-hidden rounded-full bg-line ${className}`}
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={t.total}
      aria-valuenow={t.right}
      aria-valuetext={`${t.right} of ${t.total} right`}
    >
      <div className="h-full bg-ok transition-[width] duration-500" style={{ width: w(t.right) }} />
      <div className="h-full bg-bad/70 transition-[width] duration-500" style={{ width: w(t.missed) }} />
    </div>
  );
}

const smallBtn = "rounded-full border border-line px-3 py-1 text-xs font-semibold text-fg-2 hover:border-line-strong hover:bg-hover hover:text-fg disabled:opacity-40";

function QuizSetCard({
  set,
  questions,
  stats,
  onPractice,
}: {
  set: QuizSetDef;
  questions: DrillQuestion[];
  stats: QuizStats;
  onPractice: (category?: string) => void;
}) {
  const t = tally(questions, stats);
  const complete = t.total > 0 && t.right === t.total;
  const started = t.right + t.missed > 0;
  const left = t.total - t.right;
  // First-appearance order keeps each set's own learning order (e.g. Fundamentals before Control flow).
  const cats = [...new Set(questions.flatMap((q) => (q.category ? [q.category] : [])))];
  const dialog = useRef<HTMLDialogElement>(null);

  function reset(label: string, qs: DrillQuestion[]) {
    const answered = qs.filter((q) => stats[q.id]).length;
    if (window.confirm(`Reset your progress in “${label}”? This clears ${answered} answer${answered === 1 ? "" : "s"}, so every question counts as new.`)) {
      resetQuizStats(qs.map((q) => q.id));
    }
  }

  return (
    // h-full + equal grid rows keep every card the same height; mt-auto pins the progress block to the bottom so bars line up.
    <section className="flex h-full flex-col gap-4 rounded-2xl border border-line bg-panel p-5" data-testid="quiz-set">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="flex flex-wrap items-center gap-2 text-base font-semibold text-fg">
            {set.title}
            {complete && <span className="rounded-full bg-ok/15 px-2 py-0.5 text-xs font-semibold text-ok">Mastered</span>}
          </h3>
          <p className="mt-1 text-sm leading-6 text-muted">{set.description}</p>
        </div>
        <div className={`shrink-0 text-2xl font-bold tabular-nums ${complete ? "text-ok" : "text-fg"}`}>{pct(t)}%</div>
      </div>

      <div className="mt-auto">
        <ProgressBar t={t} />
        <div className="mt-2 flex flex-wrap justify-between gap-x-3 gap-y-1 text-xs tabular-nums">
          <span className="font-medium text-fg-2">
            {t.right} / {t.total} right
          </span>
          <span className="text-subtle">
            {t.missed > 0 && <span className="text-bad">{t.missed} to retry · </span>}
            {t.fresh} new
          </span>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={() => onPractice()}
          className={`whitespace-nowrap rounded-full px-5 py-2 text-sm font-bold ${
            complete ? "border border-line-strong text-fg hover:border-fg-2 hover:bg-hover" : "bg-accent text-on-accent hover:bg-accent-hover"
          }`}
        >
          {complete ? "Practice again" : started ? `Continue · ${left} left` : `Start · ${t.total} questions`}
        </button>
      </div>

      <button
        onClick={() => dialog.current?.showModal()}
        className="flex items-center justify-between border-t border-line pt-3 text-left text-sm font-medium text-fg-2 hover:text-fg"
      >
        <span>By category ({cats.length})</span>
        <span aria-hidden="true" className="text-subtle">
          →
        </span>
      </button>

      {/* A modal rather than an inline expander, so browsing categories never changes the card heights. */}
      <dialog
        ref={dialog}
        onClick={(e) => e.target === e.currentTarget && dialog.current?.close()}
        aria-labelledby={`${set.source}-cats`}
        className="m-auto max-h-[85vh] w-[min(36rem,calc(100vw-2rem))] overflow-y-auto rounded-2xl border border-line bg-panel p-0 text-fg shadow-2xl backdrop:bg-black/40"
        data-testid="quiz-set-categories"
      >
        <div className="flex items-start justify-between gap-4 border-b border-line p-5">
          <div>
            <h3 id={`${set.source}-cats`} className="text-base font-semibold text-fg">
              {set.title} by category
            </h3>
            <p className="mt-1 text-xs tabular-nums text-subtle">
              {t.right} / {t.total} right · {pct(t)}%
            </p>
          </div>
          <button onClick={() => dialog.current?.close()} className={smallBtn}>
            Close
          </button>
        </div>
        <ul className="divide-y divide-line px-5">
          {cats.map((c) => {
            const qs = questions.filter((q) => q.category === c);
            const ct = tally(qs, stats);
            const catDone = ct.right === ct.total;
            return (
              <li key={c} className="flex items-center gap-3 py-2.5">
                <div className="min-w-0 flex-1">
                  <div className="mb-1.5 flex items-baseline justify-between gap-2 text-sm">
                    <span className={`truncate ${catDone ? "text-ok" : "text-fg-2"}`}>
                      {catDone && <span aria-label="mastered">✓ </span>}
                      {c}
                    </span>
                    <span className="shrink-0 text-xs tabular-nums text-subtle">
                      {ct.right}/{ct.total}
                    </span>
                  </div>
                  <ProgressBar t={ct} className="h-1" />
                </div>
                <button
                  onClick={() => {
                    dialog.current?.close();
                    onPractice(c);
                  }}
                  className={smallBtn}
                  aria-label={`Practice ${c}`}
                >
                  {catDone ? "Again" : "Practice"}
                </button>
                <button onClick={() => reset(c, qs)} disabled={ct.right + ct.missed === 0} className={smallBtn} aria-label={`Reset ${c}`}>
                  Reset
                </button>
              </li>
            );
          })}
        </ul>
        <div className="border-t border-line p-5">
          <button
            onClick={() => reset(set.title, questions)}
            disabled={!started}
            className="text-xs font-medium text-subtle underline hover:text-bad disabled:pointer-events-none disabled:opacity-40"
          >
            Reset all {set.title} progress
          </button>
        </div>
      </dialog>
    </section>
  );
}

export default function QuizDrill({ questions, categories }: { questions: DrillQuestion[]; categories: string[] }) {
  const stats = useQuizStats();
  const [source, setSource] = useState<Source>("all");
  const [category, setCategory] = useState("all");
  const [show, setShow] = useState<Show>("all");
  const [size, setSize] = useState(10);
  const [round, setRound] = useState<DrillQuestion[] | null>(null);
  const [idx, setIdx] = useState(0);
  const [results, setResults] = useState<boolean[]>([]);
  const [repeatRound, setRepeatRound] = useState<() => void>(() => {});
  // The quiz (and optional category) the current round practices, so the summary can show its progress.
  const [roundSet, setRoundSet] = useState<{ set: QuizSetDef; category?: string } | null>(null);

  const pool = questions.filter(
    (q) =>
      (source === "all" || q.source === source) &&
      (category === "all" || q.category === category) &&
      (show === "all" || (show === "unanswered" ? !stats[q.id] : stats[q.id] && !stats[q.id].last)),
  );

  const seen = questions.filter((q) => stats[q.id]).length;
  const mastered = questions.filter((q) => stats[q.id]?.last).length;
  const missed = questions.filter((q) => stats[q.id] && !stats[q.id].last).length;

  const setQuestions = (set: QuizSetDef, category?: string) => questions.filter((q) => q.source === set.source && (!category || q.category === category));

  function startWith(qs: DrillQuestion[]) {
    setRound(qs);
    setIdx(0);
    setResults([]);
  }

  function start() {
    const next = () => startWith(shuffle(pool).slice(0, size));
    next();
    setRepeatRound(() => next);
    setRoundSet(null);
  }

  /**
   * Practice a quiz (or one of its categories): only the questions not yet right, in a fresh random order.
   * Recomputed on every "Continue", so each round works through what's left; once everything is right, it drills the lot.
   */
  function practice(set: QuizSetDef, category?: string) {
    const next = () => {
      const st = load<QuizStats>("quiz-stats", {});
      const qs = setQuestions(set, category);
      const left = qs.filter((q) => !st[q.id]?.last);
      startWith(shuffle(left.length ? left : qs));
    };
    next();
    setRepeatRound(() => next);
    setRoundSet({ set, category });
  }

  if (round) {
    const done = results.length === round.length && idx >= round.length - 1 && results.length > 0;
    const q = round[idx];
    const right = results.filter(Boolean).length;
    // Ending early scores only the questions answered so far; with none answered there's nothing to score.
    const endRound = () => {
      if (!results.length) return setRound(null);
      setRound(round.slice(0, results.length));
      setIdx(results.length - 1);
    };
    return (
      <div className="page-shell page-quiz page-quiz-round">
        <div className="mb-5 flex items-center justify-between gap-3">
          <button
            onClick={() => setRound(null)}
            className="inline-flex items-center gap-1.5 rounded-full border border-line-strong bg-panel px-4 py-2 text-sm font-semibold text-fg-2 hover:bg-hover hover:text-fg"
          >
            <span aria-hidden="true">←</span> Back
          </button>
          {!done && (
            <button onClick={endRound} className="rounded-full border border-bad/50 bg-panel px-4 py-2 text-sm font-semibold text-bad hover:bg-bad/10">
              End round
            </button>
          )}
        </div>
        <div className="mb-2 text-sm tabular-nums text-muted">
          Question {idx + 1} of {round.length} · {right} correct
        </div>
        <div className="mb-4 h-1.5 overflow-hidden rounded-full bg-raised">
          <div className="h-full bg-accent transition-all" style={{ width: `${(results.length / round.length) * 100}%` }} />
        </div>
        <QuizCard
          key={q.id + idx}
          question={q}
          allowRetry={false}
          label={kindLabel[q.kind]}
          onAnswered={(ok) => setResults((r) => [...r, ok])}
        />
        {results.length > idx && !done && (
          <div className="mt-3 flex justify-end">
            <button onClick={() => setIdx(idx + 1)} className="rounded-full bg-accent px-5 py-2 text-sm font-bold text-on-accent hover:bg-accent-hover">
              Next question →
            </button>
          </div>
        )}
        {q.context && q.href && <ContextPanel key={"ctx" + q.id + idx} context={q.context} href={q.href} />}
        {done && (
          <div className="mt-6 rounded-lg border border-line bg-panel p-5 text-center">
            <div className="text-2xl font-semibold text-fg">
              {right} / {round.length}
            </div>
            <p className="mt-1 text-sm text-muted">
              {right === round.length
                ? "Perfect round."
                : roundSet
                  ? "Missed questions stay in this quiz until you get them right."
                  : "Missed questions are saved. Pick “Missed only” under Show to review them."}
            </p>
            {roundSet &&
              (() => {
                const t = tally(setQuestions(roundSet.set, roundSet.category), stats);
                return (
                  <div className="mx-auto mt-5 max-w-sm text-left" data-testid="round-progress">
                    <div className="mb-1.5 flex items-baseline justify-between gap-2 text-xs">
                      <span className="font-medium text-fg-2">
                        {roundSet.set.title}
                        {roundSet.category && ` · ${roundSet.category}`}
                      </span>
                      <span className="tabular-nums text-subtle">
                        {t.right} / {t.total} right · {pct(t)}%
                      </span>
                    </div>
                    <ProgressBar t={t} />
                    {t.right === t.total && <p className="mt-2 text-center text-sm font-semibold text-ok">Mastered. Every question right.</p>}
                  </div>
                );
              })()}
            <div className="mt-5 flex flex-wrap justify-center gap-3">
              <button onClick={repeatRound} className="rounded-full bg-accent px-5 py-2 text-sm font-bold text-on-accent hover:bg-accent-hover">
                {(() => {
                  if (!roundSet) return "Another round";
                  const t = tally(setQuestions(roundSet.set, roundSet.category), stats);
                  return t.right === t.total ? "Practice again" : `Continue · ${t.total - t.right} left`;
                })()}
              </button>
              <button onClick={() => setRound(null)} className="rounded-full border border-line-strong px-5 py-2 text-sm font-semibold text-fg-2 hover:bg-hover">
                Change settings
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  const select = "h-11 rounded-lg border border-line bg-panel px-3 text-sm text-fg";
  const sourceQuestions = source === "all" ? questions : questions.filter((q) => q.source === source);
  const sourceCategories = [...new Set(sourceQuestions.flatMap((q) => (q.category ? [q.category] : [])))];
  const availableCategories = source === "all" ? [...categories, ...sourceCategories.filter((c) => !categories.includes(c))] : sourceCategories;
  return (
    <div className="page-shell page-quiz">
      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] xl:items-end">
        <div>
          <h1 className="text-fg">Quiz drill</h1>
          <p className="page-intro">
            Quick-fire questions on problem solving, Python fundamentals, programming terms and complexity, drawn from all {questions.length} questions. Wrong answers go into a review pile until you get them right.
          </p>
        </div>
        <div className="grid grid-cols-3 gap-3">
          {[
            ["Answered", `${seen} / ${questions.length}`],
            ["Last answer right", String(mastered)],
            ["To review", String(missed)],
          ].map(([k, v]) => (
            <div key={k} className="flex min-w-0 flex-col gap-0.5 rounded-xl border border-line bg-panel px-4 py-3">
              <div className="text-lg font-semibold tabular-nums text-fg">{v}</div>
              <div className="text-xs text-subtle">{k}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8 grid gap-4 rounded-2xl border border-line bg-panel p-5 xl:grid-cols-[minmax(0,1fr)_minmax(18rem,24rem)]">
        <div className="grid items-end gap-x-4 gap-y-4 sm:grid-cols-2 xl:self-center xl:grid-cols-[minmax(12rem,1fr)_minmax(12rem,1fr)_minmax(7rem,0.5fr)_minmax(13rem,1fr)]">
          <label className="grid min-w-0 gap-2 text-sm text-fg-2">
            Questions about
            <select
              value={source}
              onChange={(e) => {
                setSource(e.target.value as Source);
                setCategory("all");
              }}
              className={`${select} w-full`}
            >
              <option value="all">Everything</option>
              <option value="problem">Problems</option>
              <option value="pattern">Pattern guides</option>
              <option value="python">Problem-solving Python</option>
              <option value="basics">Python basics</option>
              <option value="terms">Programming terms</option>
            </select>
          </label>
          <label className="grid min-w-0 gap-2 text-sm text-fg-2">
            Category
            <select value={category} onChange={(e) => setCategory(e.target.value)} className={`${select} w-full`}>
              <option value="all">All categories</option>
              {availableCategories.map((c) => (
                <option key={c}>{c}</option>
              ))}
            </select>
          </label>
          <label className="grid gap-2 text-sm text-fg-2">
            Round size
            <select value={size} onChange={(e) => setSize(+e.target.value)} className={`${select} w-full`}>
              {[5, 10, 20, 50].map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </label>
          <label className="grid min-w-0 gap-2 text-sm text-fg-2">
            Show
            <select value={show} onChange={(e) => setShow(e.target.value as Show)} className={`${select} w-full`}>
              <option value="all">All questions</option>
              <option value="unanswered">Unanswered only ({questions.length - seen})</option>
              <option value="missed">Missed only ({missed})</option>
            </select>
          </label>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl bg-raised p-4 xl:flex-col xl:items-start xl:justify-center">
          <div>
            <div className="text-sm font-semibold text-fg">Ready for a round?</div>
            <div className="mt-1 text-xs text-subtle">{pool.length} questions match these filters.</div>
          </div>
          <button
            onClick={start}
            disabled={!pool.length}
            className="rounded-full bg-accent px-6 py-2.5 text-sm font-bold text-on-accent hover:bg-accent-hover disabled:opacity-40"
          >
            Start ({Math.min(size, pool.length)} questions)
          </button>
        </div>
      </div>

      <div id="crash-course" className="mt-10 scroll-mt-6">
        <div className="mb-3 flex flex-wrap items-end justify-between gap-x-4 gap-y-1">
          <h2 className="text-lg font-bold tracking-tight text-fg">Your quizzes</h2>
          <p className="text-sm text-muted">Work through each quiz until every question is right. A question counts once your latest answer is correct.</p>
        </div>
        <div className="grid auto-rows-fr gap-3 md:grid-cols-2 xl:grid-cols-3">
          {QUIZ_SETS.map((set) => (
            <QuizSetCard key={set.source} set={set} questions={setQuestions(set)} stats={stats} onPractice={(c) => practice(set, c)} />
          ))}
        </div>
      </div>
    </div>
  );
}
