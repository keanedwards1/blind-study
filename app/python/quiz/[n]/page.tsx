import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import LevelQuiz from "@/components/LevelQuiz";
import { levels } from "@/lib/python";

type Params = PageProps<"/python/quiz/[n]">["params"];

export function generateStaticParams() {
  return levels.filter((l) => l.ready).map((l) => ({ n: String(l.n) }));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { n } = await params;
  return { title: `Level ${n} quiz · Learn Python · Drill` };
}

export default function LevelQuizPage({ params }: PageProps<"/python/quiz/[n]">) {
  return (
    <Suspense fallback={<div className="p-6 text-sm text-subtle">Loading quiz…</div>}>
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
      levelInfo={levels.map((l) => ({ n: l.n, ready: l.ready, problems: l.problems }))}
    />
  );
}
