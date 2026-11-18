"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { Problem, QuizQuestion, RunOutcome } from "@/lib/types";
import { sfx, useMusic } from "@/lib/audio/engine";
import { recordRepCleared } from "@/lib/concept-progress";
import { useHydrated } from "@/lib/python-progress";
import CodePane from "../CodePane";
import Markdown from "../Markdown";
import { QuizCard } from "../Quiz";
import GameShell from "./GameShell";
import { Leaf } from "./icons";
import { ambienceFor, WORLD_THEME } from "./theme";
import { Button } from "./ui";

type Round = { kind: "question"; q: QuizQuestion } | { kind: "task"; task: Problem };

function shuffled<T>(items: T[]): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

/** Up to 4 questions and 2 coding tasks, alternating: Q, Q, task, Q, Q, task. */
function buildSession(questions: QuizQuestion[], tasks: Problem[]): Round[] {
  const qs = shuffled(questions).slice(0, 4).map((q): Round => ({ kind: "question", q }));
  const ts = shuffled(tasks).slice(0, 2).map((task): Round => ({ kind: "task", task }));
  const out: Round[] = [];
  while (qs.length || ts.length) {
    out.push(...qs.splice(0, 2));
    if (ts.length) out.push(ts.shift()!);
  }
  return out;
}

/**
 * The rep room: a short practice set for one concept, drawn from its quiz and rep questions and its coding tasks.
 * Clearing it (every task passed, at most one question missed) marks the concept as no longer shaky.
 */
export default function RepRoom({
  world,
  concept,
  questions,
  tasks,
}: {
  world: { n: number; title: string };
  concept: { id: string; title: string; intro: string };
  questions: QuizQuestion[];
  tasks: Problem[];
}) {
  const hydrated = useHydrated();
  const { biome, color } = WORLD_THEME[world.n];
  useMusic(ambienceFor(world.n, true));
  const back = { href: `/python/world/${world.n}`, label: `World ${world.n}` };
  const [session, setSession] = useState(0);
  return (
    <GameShell
      biome={biome}
      back={back}
      title={
        <div>
          <p className="text-[11px] tracking-[0.2em] text-[#c9bda4] uppercase">Rep room · World {world.n}</p>
          <h1 className="font-display text-lg leading-tight font-extrabold sm:text-xl" style={{ color }}>
            {concept.title}
          </h1>
        </div>
      }
    >
      {hydrated && <Session key={session} world={world} concept={concept} questions={questions} tasks={tasks} onAgain={() => setSession((s) => s + 1)} />}
    </GameShell>
  );
}

function Session({
  world,
  concept,
  questions,
  tasks,
  onAgain,
}: {
  world: { n: number; title: string };
  concept: { id: string; title: string; intro: string };
  questions: QuizQuestion[];
  tasks: Problem[];
  onAgain: () => void;
}) {
  const rounds = useMemo(() => buildSession(questions, tasks), [questions, tasks]);
  const [results, setResults] = useState<boolean[]>([]);
  const [answered, setAnswered] = useState<boolean | null>(null);
  const [lesson, setLesson] = useState(false);
  const [code, setCode] = useState<Record<number, string>>({});
  const { color } = WORLD_THEME[world.n];
  const i = results.length;
  const round = rounds[i];
  const done = i >= rounds.length;

  const hits = results.filter(Boolean).length;
  const tasksPassed = rounds.every((r, k) => r.kind !== "task" || results[k]);
  const cleared = done && tasksPassed && rounds.length - hits <= 1;

  function next() {
    const ok = answered === true;
    const all = [...results, ok];
    setResults(all);
    setAnswered(null);
    if (all.length === rounds.length) {
      const passedTasks = rounds.every((r, k) => r.kind !== "task" || all[k]);
      const win = passedTasks && rounds.length - all.filter(Boolean).length <= 1;
      if (win) recordRepCleared(world.n, concept.id);
      sfx(win ? "clear" : "locked", win ? 1 : 0.6);
    }
  }

  function onSubmitted(o: RunOutcome) {
    const ok = !o.compileError && o.total > 0 && o.passed === o.total;
    if (ok) {
      sfx("star", 1);
      setAnswered(true);
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-5 px-4 pt-6 pb-14" style={{ "--world": color } as React.CSSProperties}>
      <div className="n-card flex flex-wrap items-center justify-between gap-3 p-4">
        <div className="flex items-center gap-1.5" aria-label={`${hits} of ${rounds.length} reps done`}>
          {rounds.map((r, k) => (
            <span
              key={k}
              className="h-2.5 w-7 rounded-md"
              style={{ background: k < results.length ? (results[k] ? color : "rgba(255,90,60,0.6)") : k === i ? "rgba(244,236,220,0.35)" : "rgba(244,236,220,0.12)" }}
              title={r.kind === "task" ? "Coding rep" : "Question"}
            />
          ))}
        </div>
        <div className="flex items-center gap-2">
          <Button ghost className="px-3! py-1.5! text-xs!" onClick={() => setLesson(true)}>
            Read the lesson
          </Button>
        </div>
      </div>

      {!done && round?.kind === "question" && (
        <div className="flex flex-col gap-4">
          <QuizCard
            key={`${i}:${round.q.id}`}
            question={round.q}
            allowRetry={false}
            size="large"
            label={`Rep ${i + 1} of ${rounds.length}`}
            onAnswered={(ok) => {
              sfx(ok ? "star" : "locked", ok ? 1 : 0.6);
              setAnswered(ok);
            }}
          />
          {answered !== null && (
            <div className="flex justify-end">
              <Button color={color} onClick={next}>
                {i + 1 === rounds.length ? "Finish" : "Next rep"}
              </Button>
            </div>
          )}
        </div>
      )}

      {!done && round?.kind === "task" && (
        <div className="flex flex-col gap-3">
          <div className="n-card flex flex-col gap-2 p-5">
            <p className="text-xs tracking-[0.15em] text-[#c9bda4] uppercase">
              Rep {i + 1} of {rounds.length} · Code it from scratch
            </p>
            <h2 className="font-display text-xl font-bold">{round.task.title}</h2>
            <div className="readable text-[#efe6d2]">
              <Markdown>{round.task.desc}</Markdown>
            </div>
          </div>
          <div className="h-[520px] overflow-hidden rounded-md border border-line bg-panel text-fg">
            <CodePane
              key={`${i}:${round.task.slug}`}
              problem={round.task}
              code={code[i] ?? round.task.starter}
              onCodeChange={(v) => setCode((c) => ({ ...c, [i]: v }))}
              onSubmitted={onSubmitted}
              onReset={() => setCode((c) => ({ ...c, [i]: round.task.starter }))}
            />
          </div>
          <div className="flex flex-wrap items-center justify-end gap-3">
            {answered ? (
              <>
                <span className="text-sm text-[#c9f2a6]">Passed every test.</span>
                <Button color={color} onClick={next}>
                  {i + 1 === rounds.length ? "Finish" : "Next rep"}
                </Button>
              </>
            ) : (
              <Button ghost onClick={next} title="Counts as a miss">
                Skip this one
              </Button>
            )}
          </div>
        </div>
      )}

      {done && (
        <div className="n-card n-rise-in flex flex-col items-center gap-4 p-7 text-center">
          <span className="flex gap-1">
            {rounds.map((_, k) => (
              <Leaf key={k} size={22} filled={results[k]} />
            ))}
          </span>
          <p className="font-display text-2xl font-bold">{cleared ? "Concept locked in" : "Keep going"}</p>
          <p className="max-w-md text-[#c9bda4]">
            {cleared
              ? `${hits} of ${rounds.length} right. ${concept.title} is no longer marked as shaky.`
              : `${hits} of ${rounds.length} right. To lock it in, pass both coding reps and miss at most one question. Re-read the lesson, then try a fresh set.`}
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <Button color={color} onClick={onAgain}>
              Rep again
            </Button>
            <Button ghost href={`/python/world/${world.n}`}>
              Back to world {world.n}
            </Button>
          </div>
        </div>
      )}

      {lesson && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm" onClick={() => setLesson(false)} role="presentation">
          <div
            className="game n-card relative max-h-[85vh] w-full max-w-2xl overflow-auto p-6"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
            aria-label={concept.title}
          >
            <div className="mb-3 flex items-start justify-between gap-4">
              <h2 className="font-display text-xl font-bold">{concept.title}</h2>
              <button type="button" onClick={() => setLesson(false)} className="text-sm text-[#c9bda4] hover:text-[#f4ecdc]">
                Close
              </button>
            </div>
            <div className="readable">
              <Markdown>{concept.intro}</Markdown>
            </div>
          </div>
        </div>
      )}

      <p className="text-center text-xs text-[#8f8470]">
        Reps don&apos;t affect your stars. <Link href={`/python/world/${world.n}`} className="underline hover:text-[#c9bda4]">Leave the rep room</Link>
      </p>
    </div>
  );
}
