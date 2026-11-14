"use client";

import { useEffect, useState } from "react";
import type { QuizQuestion } from "@/lib/types";
import { sfx, useMusic } from "@/lib/audio/engine";
import { type LevelInfo, levelStates, markQuizPassed, QUIZ_PASS, QUIZ_SIZE, useHydrated, usePlacement, useQuizPassed } from "@/lib/python-progress";
import { useSolved } from "@/lib/storage";
import Burst from "./game/Burst";
import GameShell from "./game/GameShell";
import { Acorn, Lock, Owl, Trophy } from "./game/icons";
import { ambienceFor, WORLD_THEME } from "./game/theme";
import { Button } from "./game/ui";
import { QuizCard } from "./Quiz";

/** A fresh random draw for each attempt. */
function draw(pool: QuizQuestion[]): QuizQuestion[] {
  const copy = [...pool];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, QUIZ_SIZE);
}

/** Each world's guardian: the level quiz, as an encounter. */
export default function LevelQuiz({ level, pool, levelInfo }: { level: { n: number; title: string }; pool: QuizQuestion[]; levelInfo: LevelInfo[] }) {
  const hydrated = useHydrated();
  const placement = usePlacement();
  const solved = useSolved();
  const passed = useQuizPassed();
  const { biome } = WORLD_THEME[level.n];
  useMusic(ambienceFor(level.n, false));
  const back = { href: `/python/world/${level.n}`, label: `World ${level.n}` };
  if (!hydrated) return <GameShell biome={biome} back={back}>{null}</GameShell>;

  const idx = levelInfo.findIndex((l) => l.n === level.n);
  const state = levelStates(levelInfo, placement, solved, passed)[idx];
  const unsolved = levelInfo[idx].problems.filter((s) => !solved[s]).length;

  if (state === "locked" || state === "coming-soon" || unsolved > 0) {
    return (
      <GameShell biome={biome} back={back}>
        <div className="flex flex-1 flex-col items-center justify-center gap-5 px-4 text-center">
          <span className="grid h-20 w-20 place-items-center rounded-full bg-black/30 text-[#c9bda4]">
            <Lock size={36} />
          </span>
          <p className="font-display text-2xl font-bold">The guardian is waiting</p>
          <p className="max-w-md text-[#c9bda4]">
            {state === "locked" ? "This world is still locked." : `Clear the remaining ${unsolved} stage${unsolved === 1 ? "" : "s"} of world ${level.n} first.`}
          </p>
          <Button href={back.href}>Back to world {level.n}</Button>
        </div>
      </GameShell>
    );
  }
  return <Encounter key={level.n} level={level} pool={pool} />;
}

function Encounter({ level, pool }: { level: { n: number; title: string }; pool: QuizQuestion[] }) {
  const [questions, setQuestions] = useState(() => draw(pool));
  const [answers, setAnswers] = useState<boolean[]>([]);
  const [round, setRound] = useState(0);
  const [hit, setHit] = useState<"guardian" | "you" | null>(null);
  const need = Math.ceil(questions.length * QUIZ_PASS);
  const lives = questions.length - need + 1;
  const right = answers.filter(Boolean).length;
  const wrong = answers.length - right;
  const won = right >= need;
  const lost = wrong >= lives;
  const current = questions[answers.length];
  const { color, biome } = WORLD_THEME[level.n];

  function answer(ok: boolean) {
    sfx(ok ? "star" : "locked", 1);
    setHit(ok ? "guardian" : "you");
    const next = [...answers, ok];
    if (next.filter(Boolean).length >= need) markQuizPassed(level.n);
    // Leave the explanation on screen for a moment before the next question.
    setTimeout(() => {
      setAnswers(next);
      setHit(null);
    }, ok ? 900 : 2600);
  }

  function retry() {
    setQuestions(draw(pool));
    setAnswers([]);
    setRound((r) => r + 1);
  }

  if (won) return <WorldComplete world={level.n} title={level.title} />;

  return (
    <GameShell biome={biome} back={{ href: `/python/world/${level.n}`, label: "Leave" }} title={<p className="text-[11px] tracking-[0.2em] text-[#c9bda4] uppercase">Guardian · World {level.n}</p>}>
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-4 pt-6 pb-14">
        <div className="n-card flex flex-col gap-4 p-5">
          <div className="flex items-center gap-5">
            <span className={hit === "guardian" ? "n-shake" : "n-sway"}>
              <Owl size={76} angry={hit === "you"} />
            </span>
            <div className="flex-1">
              <p className="font-display mb-2 font-semibold">Guardian of {level.title}</p>
              <div className="flex gap-1" aria-label={`The guardian needs ${need - right} more correct answers`}>
                {Array.from({ length: need }, (_, i) => (
                  <span key={i} className="h-3 flex-1 rounded-full transition-colors" style={{ background: i < need - right ? color : "rgba(244,236,220,0.12)" }} />
                ))}
              </div>
              <p className="mt-1.5 text-xs text-[#c9bda4]">Its resolve: {need - right} left to break</p>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className={`flex items-center gap-1 ${hit === "you" ? "n-shake" : ""}`} aria-label={`${lives - wrong} acorns left`}>
              {Array.from({ length: lives }, (_, i) => (
                <Acorn key={i} size={22} spent={i >= lives - wrong} />
              ))}
            </span>
            <span className="text-xs text-[#c9bda4]">
              Question {Math.min(answers.length + 1, questions.length)} of {questions.length}
            </span>
          </div>
        </div>

        {lost ? (
          <div className="n-card n-rise-in flex flex-col items-center gap-4 p-6 text-center">
            <p className="font-display text-2xl font-bold">The guardian stands firm</p>
            <p className="text-[#c9bda4]">
              {right} right and {wrong} wrong. You need {need} right before your {lives} acorns run out.
            </p>
            <div className="flex flex-wrap justify-center gap-3">
              <Button color={color} onClick={retry}>
                Try again
              </Button>
              <Button ghost href={`/python/world/${level.n}`}>
                Back to world {level.n}
              </Button>
            </div>
          </div>
        ) : (
          current && (
            <QuizCard key={`${round}:${current.id}`} question={current} allowRetry={false} size="large" onAnswered={answer} label={`Question ${answers.length + 1}`} />
          )
        )}
      </div>
    </GameShell>
  );
}

/** After the guardian: a celebration, then on to the next world. */
function WorldComplete({ world, title }: { world: number; title: string }) {
  const { color, biome, Icon } = WORLD_THEME[world];
  const last = world === 10;
  useEffect(() => sfx("world"), []);
  return (
    <GameShell biome={biome}>
      <Burst biome={biome} waves={6} />
      <div className="relative flex flex-1 flex-col items-center justify-center gap-6 px-4 py-16 text-center">
        <p className="n-rise-in text-xs tracking-[0.25em] text-[#c9bda4] uppercase">The guardian steps aside</p>
        <span className="n-pop">
          <span className="n-sway inline-block">{last ? <Icon size={130} /> : <Trophy size={120} />}</span>
        </span>
        <h1 className="font-display n-rise-in text-4xl font-extrabold sm:text-5xl" style={{ color, animationDelay: "250ms" }}>
          {last ? "You reached the end of the trail" : `World ${world} complete`}
        </h1>
        <p className="n-fade max-w-lg text-[#e5dccb]" style={{ animationDelay: "600ms" }}>
          {last ? "Every world cleared, all the way through the Blind 75. You're ready for the interview." : `${title} is behind you. The path to world ${world + 1} is open.`}
        </p>
        <div className="n-rise-in" style={{ animationDelay: "900ms" }}>
          <Button color={color} href={last ? "/python" : `/python/world/${world + 1}`}>
            {last ? "Back to the trail" : `On to world ${world + 1}`} →
          </Button>
        </div>
      </div>
    </GameShell>
  );
}
