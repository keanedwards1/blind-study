import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import RepRoom from "@/components/game/RepRoom";
import PageLoader from "@/components/loader/PageLoader";
import { levels, stageProblem } from "@/lib/python";

type Params = PageProps<"/python/reps/[n]/[concept]">["params"];

/** One rep room per concept in the Learn Python worlds (1-7). */
export function generateStaticParams() {
  return levels.filter((l) => l.kind === "python").flatMap((l) => l.concepts.map((c) => ({ n: String(l.n), concept: c.id })));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { n, concept } = await params;
  const title = levels.find((l) => String(l.n) === n)?.concepts.find((c) => c.id === concept)?.title ?? "Rep room";
  return { title: `Rep room: ${title} · Learn Python · Blind 75 from Scratch` };
}

export default function RepRoomPage({ params }: PageProps<"/python/reps/[n]/[concept]">) {
  return (
    <Suspense fallback={<PageLoader variant="game" label="Opening the rep room" />}>
      <RepLoader params={params} />
    </Suspense>
  );
}

async function RepLoader({ params }: { params: Params }) {
  const { n, concept: id } = await params;
  const level = levels.find((l) => String(l.n) === n && l.kind === "python");
  const concept = level?.concepts.find((c) => c.id === id);
  if (!level || !concept) notFound();
  const questions = [...level.quiz.filter((q) => q.id.startsWith(`py:${level.n}:${concept.id}:`)), ...concept.reps];
  const tasks = concept.problems.map((s) => stageProblem(s)!).filter(Boolean);
  return (
    <RepRoom
      world={{ n: level.n, title: level.title }}
      concept={{ id: concept.id, title: concept.title, intro: concept.intro }}
      questions={questions}
      tasks={tasks}
    />
  );
}
