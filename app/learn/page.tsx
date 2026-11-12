import type { Metadata } from "next";
import Link from "next/link";
import { ConceptCard, PatternCard } from "@/components/LearnCards";
import { conceptGroups, concepts, patterns } from "@/lib/learn";
import { summaries } from "@/lib/problems";

export const metadata: Metadata = { title: "Learn · Drill" };

export default function LearnPage() {
  const bySlug = Object.fromEntries(summaries().map((p) => [p.slug, p]));
  return (
    <div className="page-shell page-learn flex w-full min-w-0 gap-8">
      <nav className="sticky top-4 hidden max-h-[calc(100vh-5rem)] w-56 shrink-0 self-start overflow-auto text-sm lg:block">
        <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-subtle">Patterns</div>
        <ul className="mb-5 space-y-1">
          {patterns.map((p) => (
            <li key={p.id}>
              <a href={`#pattern-${p.id}`} className="text-muted hover:text-fg">
                {p.category}
              </a>
            </li>
          ))}
        </ul>
        {conceptGroups.map((g) => (
          <div key={g} className="mb-4">
            <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-subtle">{g}</div>
            <ul className="space-y-1">
              {concepts
                .filter((c) => c.group === g)
                .map((c) => (
                  <li key={c.id}>
                    <a href={`#py-${c.id}`} className="text-muted hover:text-fg">
                      {c.title}
                    </a>
                  </li>
                ))}
            </ul>
          </div>
        ))}
      </nav>

      <div className="min-w-0 flex-1 space-y-10">
        <header>
          <h1 className="text-2xl font-semibold text-fg">Learn the building blocks</h1>
          <p className="page-intro">
            Every problem is a <b className="text-fg-2">pattern</b> (the idea) built from <b className="text-fg-2">Python pieces</b> (the tools). Learn the pattern guides,
            run and edit the Python snippets, then check yourself with the quizzes. For mixed practice, try the{" "}
            <Link href="/quiz" className="text-fg underline">
              quiz drill
            </Link>
            .
          </p>
        </header>

        <section className="space-y-5">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-fg-2">Patterns ({patterns.length})</h2>
          {patterns.map((p) => (
            <PatternCard key={p.id} pattern={p} bySlug={bySlug} />
          ))}
        </section>

        <section className="space-y-5">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-fg-2">Python toolkit ({concepts.length})</h2>
          {concepts.map((c) => (
            <ConceptCard key={c.id} concept={c} bySlug={bySlug} />
          ))}
        </section>
      </div>
    </div>
  );
}
