import type { Metadata } from "next";
import QuizDrill, { type DrillContext, type DrillQuestion } from "@/components/QuizDrill";
import { py } from "@/lib/format";
import { concepts, patterns } from "@/lib/learn";
import { categories, problems } from "@/lib/problems";
import type { Problem } from "@/lib/types";

export const metadata: Metadata = { title: "Quiz drill · Drill" };

/** The statement without constraints/footnotes, so the context box stays short. */
function statement(p: Problem) {
  return p.desc.split(/\n\*\*Constraints\*\*/)[0].trim();
}

function example(p: Problem) {
  const ex = p.examples[0];
  const input = p.params.map((name, i) => `${name} = ${py(ex.args[i])}`).join(", ");
  return `Input: ${input}\nOutput: ${py(ex.expected)}`;
}

export default function QuizPage() {
  const questions: DrillQuestion[] = [
    ...problems.flatMap((p) => {
      const context: DrillContext = {
        kind: "problem",
        title: p.title,
        difficulty: p.difficulty,
        statement: statement(p),
        example: example(p),
        solution: p.solution,
      };
      return p.quiz.map((q) => ({ ...q, source: "problem" as const, sourceTitle: p.title, href: `/problems/${p.slug}`, category: p.category, context }));
    }),
    ...patterns.flatMap((pt) => {
      const context: DrillContext = { kind: "pattern", title: pt.category, summary: pt.summary, signals: pt.signals, template: pt.template };
      return pt.quiz.map((q) => ({ ...q, source: "pattern" as const, sourceTitle: pt.category, href: `/learn#pattern-${pt.id}`, category: pt.category, context }));
    }),
    ...concepts.flatMap((c) => {
      const usedIn = c.usedIn.slice(0, 6).map((slug) => ({ slug, title: problems.find((p) => p.slug === slug)?.title ?? slug }));
      const context: DrillContext = { kind: "concept", title: c.title, summary: c.summary, snippet: c.snippet, output: c.output, usedIn, usedInTotal: c.usedIn.length };
      return c.quiz.map((q) => ({ ...q, source: "python" as const, sourceTitle: c.title, href: `/learn#py-${c.id}`, context }));
    }),
  ];
  return <QuizDrill questions={questions} categories={categories} />;
}
