"use client";

import Link from "next/link";
import { useState } from "react";
import type { Concept, PatternGuide, Problem } from "@/lib/types";
import Markdown from "./Markdown";
import { QuizSet } from "./Quiz";

export function shortTitle(c: Concept) {
  return c.title.split(" (")[0];
}

export function ConceptDetail({ concept, onClose }: { concept: Concept; onClose?: () => void }) {
  return (
    <div className="rounded-lg border border-line bg-panel p-4" data-testid="concept-detail">
      <div className="mb-1 flex items-start justify-between gap-2">
        <h4 className="font-semibold text-fg">{concept.title}</h4>
        {onClose && (
          <button onClick={onClose} className="text-xs text-subtle hover:text-fg-2" aria-label="Close">
            ✕
          </button>
        )}
      </div>
      <Markdown>{concept.summary}</Markdown>
      <Link href={`/learn#py-${concept.id}`} className="text-xs font-medium text-fg underline">
        Open in Python toolkit (runnable examples + quiz) →
      </Link>
    </div>
  );
}

export default function LearnTab({ problem, pattern, concepts }: { problem: Problem; pattern: PatternGuide; concepts: Concept[] }) {
  const [unlocked, setUnlocked] = useState(false);
  const [open, setOpen] = useState<string | null>(null);

  if (!unlocked) {
    return (
      <div className="flex flex-col items-start gap-3">
        <p className="text-sm leading-6 text-muted">
          This tab breaks the problem into its building blocks: the <b className="text-fg-2">pattern</b>, the <b className="text-fg-2">Python tools</b> the solution
          uses, and a <b className="text-fg-2">self-quiz</b> on the key insight and complexity. It gives away part of the approach, so try the problem first if you
          want the full challenge.
        </p>
        <button onClick={() => setUnlocked(true)} className="rounded-md border border-line-strong px-3 py-1.5 text-sm text-fg-2 hover:bg-hover">
          Show building blocks & quiz
        </button>
      </div>
    );
  }

  const openConcept = concepts.find((c) => c.id === open);
  return (
    <div className="space-y-6">
      <section>
        <h3 className="mb-2 text-sm font-semibold text-fg">Pattern: {pattern.category}</h3>
        <Markdown>{pattern.summary}</Markdown>
        <Link href={`/learn#pattern-${pattern.id}`} className="text-xs font-medium text-fg underline">
          Read the {pattern.category} guide (template, signals, pitfalls) →
        </Link>
      </section>

      <section>
        <h3 className="mb-2 text-sm font-semibold text-fg">Python building blocks in the solution</h3>
        <p className="mb-2 text-xs text-subtle">Click one for a quick explanation.</p>
        <div className="mb-3 flex flex-wrap gap-1.5">
          {concepts.map((c) => (
            <button
              key={c.id}
              onClick={() => setOpen(open === c.id ? null : c.id)}
              className={`rounded-full border px-2.5 py-0.5 text-xs ${open === c.id ? "border-accent bg-accent/15 text-fg" : "border-line text-fg-2 hover:bg-hover"}`}
            >
              {shortTitle(c)}
            </button>
          ))}
        </div>
        {openConcept && <ConceptDetail concept={openConcept} onClose={() => setOpen(null)} />}
      </section>

      <QuizSet questions={problem.quiz} />
    </div>
  );
}
