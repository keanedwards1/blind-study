import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import Workspace from "@/components/Workspace";
import { conceptById, patternById } from "@/lib/learn";
import { getProblem, neighbours, problems } from "@/lib/problems";

type Params = PageProps<"/problems/[slug]">["params"];

export function generateStaticParams() {
  return problems.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { slug } = await params;
  return { title: `${getProblem(slug)?.title ?? "Problem"} · Drill` };
}

// With Cache Components, `params` must be read inside a <Suspense> boundary so
// navigations between problems can render a shell instantly.
export default function ProblemPage({ params }: PageProps<"/problems/[slug]">) {
  return (
    <Suspense fallback={<div className="p-6 text-sm text-subtle">Loading problem…</div>}>
      <ProblemLoader params={params} />
    </Suspense>
  );
}

async function ProblemLoader({ params }: { params: Params }) {
  const { slug } = await params;
  const problem = getProblem(slug);
  if (!problem) notFound();
  const { prev, next } = neighbours(slug);
  const concepts = problem.concepts.map((id) => conceptById[id]);
  return <Workspace key={slug} problem={problem} prev={prev} next={next} pattern={patternById[problem.pattern]} concepts={concepts} />;
}
