import Link from "next/link";
import type { Concept, PatternGuide, ProblemSummary } from "@/lib/types";
import { difficultyColor } from "@/lib/format";
import Markdown from "./Markdown";
import Playground from "./Playground";
import { QuizSet } from "./Quiz";

function ProblemLinks({ slugs, bySlug }: { slugs: string[]; bySlug: Record<string, ProblemSummary> }) {
  if (!slugs.length) return null;
  return (
    <div className="flex flex-wrap gap-1.5">
      {slugs.map((s) => (
        <Link
          key={s}
          href={`/problems/${s}`}
          title={bySlug[s]?.difficulty}
          className="inline-flex items-center gap-1.5 rounded-md border border-line px-2 py-1 text-xs text-fg-2 hover:bg-hover"
        >
          <span aria-hidden="true" className={`h-1.5 w-1.5 shrink-0 rounded-full bg-current ${difficultyColor[bySlug[s]?.difficulty ?? ""] ?? "text-subtle"}`} />
          {bySlug[s]?.title ?? s}
        </Link>
      ))}
    </div>
  );
}

function Label({ children }: { children: React.ReactNode }) {
  return <h3 className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-subtle">{children}</h3>;
}

export function ConceptCard({ concept, bySlug }: { concept: Concept; bySlug: Record<string, ProblemSummary> }) {
  return (
    <article id={`py-${concept.id}`} className="scroll-mt-16 space-y-4 rounded-xl border border-line bg-panel p-5">
      <header>
        <div className="text-xs text-subtle">{concept.group}</div>
        <h2 className="text-lg font-semibold text-fg">{concept.title}</h2>
      </header>
      <Markdown>{concept.summary}</Markdown>
      <div className="rounded-lg border border-line bg-raised/60 p-3.5">
        <Label>Example question</Label>
        <Markdown>{concept.exampleQuestion}</Markdown>
        <Link href={`/problems/${concept.exampleSlug}`} className="mt-2 inline-block text-xs font-medium text-fg underline">
          Open {bySlug[concept.exampleSlug]?.title ?? "example problem"} →
        </Link>
      </div>
      <div>
        <Label>Template, broken down line by line</Label>
        <pre className="overflow-auto whitespace-pre-wrap break-words rounded-lg bg-raised p-4 font-mono text-[13px] leading-6 text-fg">{concept.template}</pre>
      </div>
      <div>
        <Label>Try it (edit and run)</Label>
        <Playground code={concept.snippet} expected={concept.output} />
      </div>
      <div>
        <Label>Notes & gotchas</Label>
        <Markdown>{concept.notes}</Markdown>
      </div>
      {concept.usedIn.length > 0 && (
        <div>
          <Label>Used in {concept.usedIn.length} problem solutions</Label>
          <ProblemLinks slugs={concept.usedIn} bySlug={bySlug} />
        </div>
      )}
      <QuizSet questions={concept.quiz} title="Check yourself" />
    </article>
  );
}

export function PatternCard({ pattern, bySlug }: { pattern: PatternGuide; bySlug: Record<string, ProblemSummary> }) {
  return (
    <article id={`pattern-${pattern.id}`} className="scroll-mt-16 space-y-4 rounded-xl border border-line bg-panel p-5">
      <header>
        <div className="text-xs text-subtle">Pattern</div>
        <h2 className="text-lg font-semibold text-fg">{pattern.category}</h2>
      </header>
      <Markdown>{pattern.summary}</Markdown>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label>When to use it</Label>
          <Markdown>{pattern.signals.map((s) => `- ${s}`).join("\n")}</Markdown>
        </div>
        <div>
          <Label>Common mistakes</Label>
          <Markdown>{pattern.pitfalls.map((s) => `- ${s}`).join("\n")}</Markdown>
        </div>
      </div>
      <div>
        <Label>Template</Label>
        <pre className="overflow-auto rounded-lg bg-raised p-4 font-mono text-[13px] leading-6 text-fg">{pattern.template}</pre>
      </div>
      <div>
        <Label>Typical complexity</Label>
        <Markdown>{pattern.complexity}</Markdown>
      </div>
      <div>
        <Label>Practice</Label>
        <ProblemLinks slugs={pattern.problems} bySlug={bySlug} />
      </div>
      <QuizSet questions={pattern.quiz} title="Check yourself" />
    </article>
  );
}
