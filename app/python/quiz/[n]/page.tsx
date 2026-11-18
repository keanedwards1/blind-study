import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import PageLoader from "@/components/loader/PageLoader";
import LevelQuiz from "@/components/LevelQuiz";
import { levels, stageProblem } from "@/lib/python";

type Params = PageProps<"/python/quiz/[n]">["params"];

export function generateStaticParams() {
  return levels.filter((l) => l.ready).map((l) => ({ n: String(l.n) }));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { n } = await params;
  return { title: `Level ${n} quiz · Learn Python · Blind 75 from Scratch` };
}

export default function LevelQuizPage({ params }: PageProps<"/python/quiz/[n]">) {
  return (
    <Suspense fallback={<PageLoader variant="game" label="Summoning the guardian" />}>
      <QuizLoader params={params} />
    </Suspense>
  );
}

async function QuizLoader({ params }: { params: Params }) {
  const { n } = await params;
  const level = levels.find((l) => String(l.n) === n);
  if (!level || !level.ready) notFound();
  return (
    <LevelQuiz
      level={{ n: level.n, title: level.title }}
      pool={level.quiz}
      boss={level.boss}
      predicts={[...level.quiz, ...level.concepts.flatMap((c) => c.reps)].filter((q) => q.q === "What does this print?" && q.code)}
      strikes={(level.boss?.strikes ?? []).map((s) => stageProblem(s)!).filter(Boolean)}
      concepts={level.concepts.map((c) => ({
        id: c.id,
        title: c.title,
        problems: c.problems,
        stages: c.problems.map((s) => stageProblem(s)?.title ?? s),
      }))}
      levelInfo={levels.map((l) => ({ n: l.n, ready: l.ready, problems: l.problems }))}
    />
  );
}
