"use client";

import { useMemo, useState } from "react";
import type { QuizQuestion } from "@/lib/types";
import { load, save, useStored } from "@/lib/storage";
import Markdown from "./Markdown";

export type QuizStat = { right: number; wrong: number; last: boolean; at: number };
export type QuizStats = Record<string, QuizStat>;
const EMPTY: QuizStats = {};

export function useQuizStats() {
  return useStored<QuizStats>("quiz-stats", EMPTY);
}

function recordAnswer(id: string, correct: boolean) {
  const stats = load<QuizStats>("quiz-stats", {});
  const prev = stats[id] ?? { right: 0, wrong: 0, last: false, at: 0 };
  save("quiz-stats", {
    ...stats,
    [id]: { right: prev.right + (correct ? 1 : 0), wrong: prev.wrong + (correct ? 0 : 1), last: correct, at: Date.now() },
  });
}

/** Deterministic shuffle so options don't jump around between renders. */
function seededOrder(id: string, n: number): number[] {
  let h = 2166136261;
  for (let i = 0; i < id.length; i++) h = Math.imul(h ^ id.charCodeAt(i), 16777619);
  const order = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    h = Math.imul(h ^ (h >>> 15), 2246822507) >>> 0;
    const j = h % (i + 1);
    [order[i], order[j]] = [order[j], order[i]];
  }
  return order;
}

export const kindLabel: Record<QuizQuestion["kind"], string> = {
  insight: "Key insight",
  pattern: "Pattern",
  time: "Time complexity",
  space: "Space complexity",
  python: "Python",
  "pattern-guide": "Pattern",
};

export function QuizCard({
  question,
  label,
  onAnswered,
  allowRetry = true,
}: {
  question: QuizQuestion;
  label?: React.ReactNode;
  onAnswered?: (correct: boolean) => void;
  allowRetry?: boolean;
}) {
  const [picked, setPicked] = useState<number | null>(null);
  const order = useMemo(() => seededOrder(question.id, question.options.length), [question]);
  const answered = picked !== null;
  const correct = picked === question.answer;

  function pick(i: number) {
    if (answered) return;
    setPicked(i);
    recordAnswer(question.id, i === question.answer);
    onAnswered?.(i === question.answer);
  }

  return (
    <div className="rounded-lg border border-line bg-panel p-4" data-testid="quiz-card">
      <div className="mb-2 flex items-center justify-between gap-2 text-xs text-subtle">
        <span>{label ?? kindLabel[question.kind]}</span>
        {answered && <span className={correct ? "font-medium text-ok" : "font-medium text-bad"}>{correct ? "Correct" : "Not quite"}</span>}
      </div>
      <Markdown>{question.q}</Markdown>
      {question.code && <pre className="mt-2 overflow-auto rounded-md bg-raised p-3 font-mono text-[13px] leading-6 text-fg">{question.code}</pre>}
      <div className="mt-3 grid gap-2">
        {order.map((i) => {
          const opt = question.options[i];
          let tone = "border-line hover:border-line-strong hover:bg-hover";
          if (answered && i === question.answer) tone = "border-ok bg-ok/10 text-fg";
          else if (answered && i === picked) tone = "border-bad bg-bad/10";
          else if (answered) tone = "border-line opacity-60";
          return (
            <button
              key={i}
              onClick={() => pick(i)}
              disabled={answered}
              className={`rounded-md border px-3 py-2 text-left text-sm text-fg-2 ${tone} ${opt.includes("\n") ? "whitespace-pre font-mono" : ""}`}
            >
              {opt}
            </button>
          );
        })}
      </div>
      {answered && (
        <div className="mt-3 border-t border-line pt-3">
          {question.why && <Markdown>{question.why}</Markdown>}
          {allowRetry && (
            <button onClick={() => setPicked(null)} className="mt-1 text-xs text-subtle hover:text-fg-2">
              Try again
            </button>
          )}
        </div>
      )}
    </div>
  );
}

/** A list of questions with a running score for this visit. */
export function QuizSet({ questions, title = "Self-quiz" }: { questions: QuizQuestion[]; title?: string }) {
  const [results, setResults] = useState<Record<string, boolean>>({});
  const answered = Object.keys(results).length;
  const right = Object.values(results).filter(Boolean).length;
  if (!questions.length) return null;
  return (
    <section className="space-y-3">
      <div className="flex items-baseline justify-between">
        <h3 className="text-sm font-semibold text-fg">{title}</h3>
        <span className="text-xs text-subtle">
          {answered ? `${right} / ${answered} correct` : `${questions.length} question${questions.length > 1 ? "s" : ""}`}
        </span>
      </div>
      {questions.map((q) => (
        <QuizCard key={q.id} question={q} onAnswered={(ok) => setResults((r) => ({ ...r, [q.id]: ok }))} />
      ))}
    </section>
  );
}
