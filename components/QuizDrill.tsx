"use client";

import Link from "next/link";
import { useState } from "react";
import type { QuizQuestion } from "@/lib/types";
import { difficultyColor } from "@/lib/format";
import Markdown from "./Markdown";
import { QuizCard, kindLabel, useQuizStats } from "./Quiz";

export type DrillContext =
  | { kind: "problem"; title: string; difficulty: string; statement: string; example: string; solution: string }
  | { kind: "pattern"; title: string; summary: string; signals: string[]; template: string }
  | { kind: "concept"; title: string; summary: string; snippet: string; output: string };

export type DrillQuestion = QuizQuestion & {
  source: "problem" | "python" | "pattern";
  sourceTitle: string;
  href: string;
  category?: string;
  context: DrillContext;
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
    <div className="mb-3 rounded-lg border border-line bg-raised/60 p-4" data-testid="quiz-context">
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
      {context.kind === "concept" && <Markdown>{context.summary}</Markdown>}
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

function shuffle<T>(a: T[]): T[] {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}

export default function QuizDrill({ questions, categories }: { questions: DrillQuestion[]; categories: string[] }) {
  const stats = useQuizStats();
  const [source, setSource] = useState<Source>("all");
  const [category, setCategory] = useState("all");
  const [onlyMissed, setOnlyMissed] = useState(false);
  const [size, setSize] = useState(10);
  const [round, setRound] = useState<DrillQuestion[] | null>(null);
  const [idx, setIdx] = useState(0);
  const [results, setResults] = useState<boolean[]>([]);

  const pool = questions.filter(
    (q) =>
      (source === "all" || q.source === source) &&
      (category === "all" || q.category === category) &&
      (!onlyMissed || (stats[q.id] && !stats[q.id].last)),
  );

  const seen = questions.filter((q) => stats[q.id]).length;
  const mastered = questions.filter((q) => stats[q.id]?.last).length;
  const missed = questions.filter((q) => stats[q.id] && !stats[q.id].last).length;

  function start() {
    setRound(shuffle(pool).slice(0, size));
    setIdx(0);
    setResults([]);
  }

  if (round) {
    const done = results.length === round.length && idx >= round.length - 1 && results.length > 0;
    const q = round[idx];
    const right = results.filter(Boolean).length;
    return (
      <div className="mx-auto w-full max-w-2xl px-4 py-8">
        <div className="mb-4 flex items-center justify-between text-sm">
          <span className="text-muted">
            Question {idx + 1} of {round.length} · {right} correct
          </span>
          <button onClick={() => setRound(null)} className="text-subtle hover:text-fg-2">
            End round
          </button>
        </div>
        <div className="mb-4 h-1.5 overflow-hidden rounded-full bg-raised">
          <div className="h-full bg-accent transition-all" style={{ width: `${(results.length / round.length) * 100}%` }} />
        </div>
        <ContextPanel key={"ctx" + q.id + idx} context={q.context} href={q.href} />
        <QuizCard
          key={q.id + idx}
          question={q}
          allowRetry={false}
          label={kindLabel[q.kind]}
          onAnswered={(ok) => setResults((r) => [...r, ok])}
        />
        <div className="mt-4 flex justify-end">
          {results.length > idx && !done && (
            <button onClick={() => setIdx(idx + 1)} className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-zinc-950 hover:opacity-90">
              Next question →
            </button>
          )}
        </div>
        {done && (
          <div className="mt-6 rounded-lg border border-line bg-panel p-5 text-center">
            <div className="text-2xl font-semibold text-fg">
              {right} / {round.length}
            </div>
            <p className="mt-1 text-sm text-muted">{right === round.length ? "Perfect round." : "Missed questions go into your “review missed” pile."}</p>
            <div className="mt-4 flex justify-center gap-3">
              <button onClick={start} className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-zinc-950 hover:opacity-90">
                Another round
              </button>
              <button onClick={() => setRound(null)} className="rounded-md border border-line-strong px-4 py-2 text-sm text-fg-2 hover:bg-hover">
                Change settings
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  const select = "rounded-md border border-line bg-panel px-2 py-1.5 text-sm text-fg-2";
  return (
    <div className="mx-auto w-full max-w-2xl px-4 py-8">
      <h1 className="text-2xl font-semibold text-fg">Quiz drill</h1>
      <p className="mt-2 text-sm leading-6 text-muted">
        Quick-fire questions on key insights, complexity, patterns and Python behaviour, drawn from all {questions.length} questions. Wrong answers go into a review pile
        until you get them right.
      </p>

      <div className="mt-5 grid grid-cols-3 gap-3 text-center">
        {[
          ["Answered", `${seen} / ${questions.length}`],
          ["Last answer right", String(mastered)],
          ["To review", String(missed)],
        ].map(([k, v]) => (
          <div key={k} className="rounded-lg border border-line bg-panel p-3">
            <div className="text-lg font-semibold text-fg">{v}</div>
            <div className="text-xs text-subtle">{k}</div>
          </div>
        ))}
      </div>

      <div className="mt-6 grid gap-3 rounded-lg border border-line bg-panel p-5 sm:grid-cols-2">
        <label className="flex items-center justify-between gap-2 text-sm text-fg-2">
          Questions about
          <select value={source} onChange={(e) => setSource(e.target.value as Source)} className={select}>
            <option value="all">Everything</option>
            <option value="problem">Problems</option>
            <option value="pattern">Pattern guides</option>
            <option value="python">Python</option>
          </select>
        </label>
        <label className="flex items-center justify-between gap-2 text-sm text-fg-2">
          Category
          <select value={category} onChange={(e) => setCategory(e.target.value)} className={select}>
            <option value="all">All</option>
            {categories.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <label className="flex items-center justify-between gap-2 text-sm text-fg-2">
          Round size
          <select value={size} onChange={(e) => setSize(+e.target.value)} className={select}>
            {[5, 10, 20, 50].map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
        <label className="flex items-center gap-2 text-sm text-fg-2">
          <input type="checkbox" checked={onlyMissed} onChange={(e) => setOnlyMissed(e.target.checked)} />
          Only review missed ({missed})
        </label>
      </div>

      <div className="mt-5 flex items-center gap-3">
        <button
          onClick={start}
          disabled={!pool.length}
          className="rounded-md bg-accent px-5 py-2 text-sm font-semibold text-zinc-950 hover:opacity-90 disabled:opacity-40"
        >
          Start ({Math.min(size, pool.length)} questions)
        </button>
        <span className="text-xs text-subtle">{pool.length} match these filters</span>
      </div>
    </div>
  );
}
