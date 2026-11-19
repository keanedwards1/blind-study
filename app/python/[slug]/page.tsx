import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import PageLoader from "@/components/loader/PageLoader";
import GameStage from "@/components/game/GameStage";
import { conceptById } from "@/lib/learn";
import { levelInfos, levelOf, levels, stageLabel, stageProblem } from "@/lib/python";

type Params = PageProps<"/python/[slug]">["params"];

/** Every stage of every world, including the Blind 75 problems in worlds 8-10. */
export function generateStaticParams() {
  return levels.flatMap((l) => l.problems.map((slug) => ({ slug })));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { slug } = await params;
  return { title: `${stageProblem(slug)?.title ?? "Stage"} · Learn Python · Blind 75 from Scratch` };
}

export default function StagePage({ params }: PageProps<"/python/[slug]">) {
  return (
    <Suspense fallback={<PageLoader variant="workspace" label="Loading stage" />}>
      <StageLoader params={params} />
    </Suspense>
  );
}

async function StageLoader({ params }: { params: Params }) {
  const { slug } = await params;
  const level = levelOf(slug);
  const problem = stageProblem(slug);
  if (!level || !problem) notFound();
  const i = level.problems.indexOf(slug);
  const nextSlug = level.problems[i + 1];
  const concept = level.kind === "python" ? level.concepts.find((c) => c.problems.includes(slug)) : undefined;
  return (
    <GameStage
      key={slug}
      problem={problem}
      concepts={problem.concepts.map((id) => conceptById[id])}
      stage={{
        label: stageLabel(level, slug),
        world: { n: level.n, title: level.title },
        worldSlugs: level.problems,
        next: nextSlug ? { slug: nextSlug, label: stageLabel(level, nextSlug) } : undefined,
        lesson: concept ? { title: concept.title, intro: concept.intro } : undefined,
      }}
      levelInfo={levelInfos()}
    />
  );
}
