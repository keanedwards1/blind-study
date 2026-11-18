"use client";

import { useEffect, useRef, useState } from "react";
import type { BossData, Problem, QuizQuestion } from "@/lib/types";
import { sfx, useMusic } from "@/lib/audio/engine";
import { type LevelInfo, levelStates, markQuizPassed, QUIZ_PASS, QUIZ_SIZE, useHydrated, usePlacement, useQuizPassed } from "@/lib/python-progress";
import { save, useSolved, useStored } from "@/lib/storage";
import { recordMiss, struggles, useMisses, useRepClears } from "@/lib/concept-progress";
import { loadAttempt, useResults } from "@/lib/python-progress";
import Burst from "./game/Burst";
import GameShell from "./game/GameShell";
import { Acorn, Lock, Owl, Trophy } from "./game/icons";
import { ambienceFor, WORLD_THEME } from "./game/theme";
import { Button } from "./game/ui";
import { FallingRound, LightningRound, MatchRound, PredictRound, type RoundResult, StrikeRound } from "./game/boss/rounds";
import { QuizCard } from "./Quiz";

/** Each world's guardian: the level quiz, as an encounter. */
type ConceptInfo = { id: string; title: string; problems: string[]; stages: string[] };

export default function LevelQuiz({
  level,
  pool,
  levelInfo,
  concepts = [],
  boss,
  predicts = [],
  strikes = [],
}: {
  level: { n: number; title: string };
  pool: QuizQuestion[];
  levelInfo: LevelInfo[];
  /** The world's concepts (Learn Python worlds only), to warn about shaky ones before the fight. */
  concepts?: ConceptInfo[];
  /** Mini-game content (Learn Python worlds only). */
  boss?: BossData;
  /** Predict-the-output questions for the typed predict rounds. */
  predicts?: QuizQuestion[];
  /** Short tasks for the coding strike. */
  strikes?: Problem[];
}) {
  const results = useResults();
  const misses = useMisses();
  const reps = useRepClears();
  const [fightAnyway, setFightAnyway] = useState(false);
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
          <span className="grid h-20 w-20 place-items-center rounded-md bg-black/30 text-[#c9bda4]">
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
  const titles = Object.fromEntries(concepts.flatMap((c) => c.problems.map((s, i) => [s, c.stages[i]])));
  const shaky = struggles(level.n, concepts, results, loadAttempt, misses, reps, (s) => titles[s] ?? s);
  if (shaky.length && !fightAnyway) {
    return (
      <GameShell biome={biome} back={back}>
        <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-center justify-center gap-5 px-4 py-10 text-center">
          <span className="n-sway">
            <Owl size={76} />
          </span>
          <p className="font-display text-2xl font-bold">The guardian senses a weak spot</p>
          <p className="max-w-md text-[#c9bda4]">
            Before you fight, these concepts could use a few reps. A short practice set locks them in.
          </p>
          <ul className="flex w-full flex-col gap-2 text-left">
            {shaky.map((s) => (
              <li key={s.id} className="n-card flex flex-wrap items-center justify-between gap-3 p-4">
                <div className="min-w-0">
                  <p className="font-semibold">{s.title}</p>
                  <p className="text-xs text-[#c9bda4]">Why: {s.reasons.join("; ")}.</p>
                </div>
                <Button color="#ff7a2f" className="px-3! py-1.5! text-xs!" href={`/python/reps/${level.n}/${s.id}`}>
                  Rep it
                </Button>
              </li>
            ))}
          </ul>
          <Button ghost onClick={() => setFightAnyway(true)}>
            Fight anyway
          </Button>
        </div>
      </GameShell>
    );
  }
  return <Encounter key={level.n} level={level} pool={pool} boss={boss} predicts={predicts} strikes={strikes} />;
}

type Round =
  | { kind: "mc"; q: QuizQuestion }
  | { kind: "predict"; q: QuizQuestion }
  | { kind: "match" }
  | { kind: "falling" }
  | { kind: "lightning" }
  | { kind: "strike"; task: Problem };

const ROUND_LABEL: Record<Round["kind"], string> = {
  mc: "Question",
  predict: "Predict the output",
  match: "Match",
  falling: "Falling expressions",
  lightning: "Lightning round",
  strike: "Coding strike",
};

/**
 * The fight plan. Learn Python worlds mix six mini-games and end with a coding strike (resolve 10, 3 acorns; a strike
 * and the timed games can deal 2). Blind 75 worlds stay a 10-question duel (resolve 8, 3 acorns), like before.
 * A game whose content is missing for this world falls back to a multiple-choice question.
 */
function plan(pool: QuizQuestion[], predicts: QuizQuestion[], boss: BossData | undefined, strikes: Problem[]): { rounds: Round[]; resolve: number } {
  const mc = shuffleAll(pool);
  const pr = shuffleAll(predicts);
  const nextMc = (): Round => ({ kind: "mc", q: mc.shift() ?? pool[0] });
  if (!boss) return { rounds: Array.from({ length: Math.min(QUIZ_SIZE, pool.length) }, nextMc), resolve: Math.ceil(QUIZ_SIZE * QUIZ_PASS) };
  const order: Round["kind"][] = ["mc", "predict", "match", "mc", "falling", "predict", "lightning", "mc", "strike"];
  const rounds = order.map((kind): Round => {
    if (kind === "predict") return pr.length ? { kind, q: pr.shift()! } : nextMc();
    if (kind === "match") return boss.pairs.length >= 4 ? { kind } : nextMc();
    if (kind === "falling") return boss.exprs.length >= 6 ? { kind } : nextMc();
    if (kind === "lightning") return boss.facts.length >= 8 ? { kind } : nextMc();
    if (kind === "strike") return strikes.length ? { kind, task: shuffleAll(strikes)[0] } : nextMc();
    return nextMc();
  });
  return { rounds, resolve: 10 };
}

function shuffleAll<T>(items: T[]): T[] {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

const ACORNS = 3;

function Encounter({
  level,
  pool,
  boss,
  predicts,
  strikes,
}: {
  level: { n: number; title: string };
  pool: QuizQuestion[];
  boss?: BossData;
  predicts: QuizQuestion[];
  strikes: Problem[];
}) {
  const [fight, setFight] = useState(() => plan(pool, predicts, boss, strikes));
  const [index, setIndex] = useState(0);
  const [damage, setDamage] = useState(0);
  const [hurt, setHurt] = useState(0);
  const [round, setRound] = useState(0);
  const [hit, setHit] = useState<"guardian" | "you" | null>(null);
  const relaxedSaved = useStored<boolean>("python:boss-relaxed", false);
  const [prefersReduced] = useState(() => typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  const relaxed = relaxedSaved || prefersReduced;
  const resolveLeft = Math.max(0, fight.resolve - damage);
  const acornsLeft = ACORNS - hurt;
  const won = resolveLeft === 0;
  const lost = !won && (acornsLeft <= 0 || index >= fight.rounds.length);
  const current = fight.rounds[index];
  const { color, biome } = WORLD_THEME[level.n];

  // Keep the page steady while you're scrolled down: the round area never shrinks during a fight (a shorter next round
  // would otherwise pull the page up under you), and a new round that starts above the screen is brought into view just
  // below the pinned status bar.
  const hudRef = useRef<HTMLDivElement>(null);
  const areaRef = useRef<HTMLDivElement>(null);
  const [minHeight, setMinHeight] = useState(0);
  useEffect(() => {
    const el = areaRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setMinHeight((h) => Math.max(h, el.offsetHeight)));
    ro.observe(el);
    return () => ro.disconnect();
  }, [round]);
  useEffect(() => {
    const el = areaRef.current;
    const hud = hudRef.current?.offsetHeight ?? 0;
    if (!el || index === 0) return;
    const top = el.getBoundingClientRect().top;
    if (top < hud + 8) {
      window.scrollTo({ top: window.scrollY + top - hud - 16, behavior: relaxed ? "auto" : "smooth" });
    }
  }, [index, relaxed]);

  // The coding strike is the finishing blow: until it lands, the guardian always clings on to its last 2 resolve.
  const hasStrike = fight.rounds.some((r) => r.kind === "strike");
  const clinging = hasStrike && current?.kind !== "strike" && fight.resolve - damage <= 2;

  function apply(r: RoundResult) {
    const isStrike = current?.kind === "strike";
    const nextDamage = hasStrike && !isStrike ? Math.min(damage + r.damage, fight.resolve - 2) : damage + r.damage;
    setHit(r.damage ? "guardian" : r.hurt ? "you" : null);
    setDamage(nextDamage);
    setHurt(hurt + r.hurt);
    if (nextDamage >= fight.resolve) markQuizPassed(level.n);
    setIndex(index + 1);
  }

  function answerMc(q: QuizQuestion, ok: boolean) {
    sfx(ok ? "star" : "locked", 1);
    if (!ok) recordMiss(q.id);
    setHit(ok ? "guardian" : "you");
    // Leave the explanation on screen for a moment before the next round.
    setTimeout(() => apply({ damage: ok ? 1 : 0, hurt: ok ? 0 : 1, note: "" }), ok ? 900 : 2600);
  }

  function retry() {
    setMinHeight(0);
    setFight(plan(pool, predicts, boss, strikes));
    setIndex(0);
    setDamage(0);
    setHurt(0);
    setHit(null);
    setRound((r) => r + 1);
  }

  if (won) return <WorldComplete world={level.n} title={level.title} />;

  return (
    <GameShell biome={biome} back={{ href: `/python/world/${level.n}`, label: "Leave" }} title={<p className="text-[11px] tracking-[0.2em] text-[#c9bda4] uppercase">Guardian · World {level.n}</p>}>
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-4 pt-6 pb-14" style={{ "--world": color } as React.CSSProperties}>
        <div ref={hudRef} className="n-card sticky top-2 z-20 flex flex-col gap-3 bg-[rgba(18,13,9,0.94)]! p-4 [backdrop-filter:none]!">
          <div className="flex items-center gap-4">
            <span className={hit === "guardian" ? "n-shake" : "n-sway"}>
              <Owl size={56} angry={hit === "you"} />
            </span>
            <div className="flex-1">
              <p className="font-display mb-2 font-semibold">Guardian of {level.title}</p>
              <div className="flex gap-1" aria-label={`The guardian's resolve: ${resolveLeft} of ${fight.resolve}`}>
                {Array.from({ length: fight.resolve }, (_, i) => (
                  <span key={i} className="h-3 flex-1 rounded-md transition-colors" style={{ background: i < resolveLeft ? color : "rgba(244,236,220,0.12)" }} />
                ))}
              </div>
              <p className="mt-1.5 text-xs text-[#c9bda4]">
                Its resolve: {resolveLeft} left to break
                {clinging && " · it clings on: only the coding strike can finish it"}
              </p>
            </div>
          </div>
          <div className="flex flex-wrap items-center justify-between gap-3">
            <span className={`flex items-center gap-1 ${hit === "you" ? "n-shake" : ""}`} aria-label={`${acornsLeft} acorns left`}>
              {Array.from({ length: ACORNS }, (_, i) => (
                <Acorn key={i} size={22} spent={i >= acornsLeft} />
              ))}
            </span>
            <span className="flex items-center gap-3 text-xs text-[#c9bda4]">
              {boss && (
                <button
                  type="button"
                  onClick={() => save("python:boss-relaxed", !relaxedSaved)}
                  className="rounded-md border border-[rgba(244,236,220,0.2)] px-2 py-0.5 hover:text-[#f4ecdc]"
                  title="Slows down every timer in the fight"
                  aria-pressed={relaxed}
                >
                  Relaxed pace: {relaxed ? "on" : "off"}
                </button>
              )}
              {!lost && current && (
                <span>
                  Round {Math.min(index + 1, fight.rounds.length)} of {fight.rounds.length} · {ROUND_LABEL[current.kind]}
                </span>
              )}
            </span>
          </div>
        </div>

        <div ref={areaRef} style={{ minHeight }} className="flex flex-col">
          {lost ? (
            <div className="n-card n-rise-in flex flex-col items-center gap-4 p-6 text-center">
              <p className="font-display text-2xl font-bold">The guardian stands firm</p>
              <p className="text-[#c9bda4]">
                You broke {damage} of its {fight.resolve} resolve{acornsLeft <= 0 ? ", but your acorns ran out" : ""}. Every fight is a fresh mix of
                challenges, so try again when you&apos;re ready.
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
              <div key={`${round}:${index}`}>
                {current.kind === "mc" && (
                  <QuizCard question={current.q} allowRetry={false} size="large" onAnswered={(ok) => answerMc(current.q, ok)} label={`Round ${index + 1}`} />
                )}
                {current.kind === "predict" && (
                  <PredictRound
                    q={current.q}
                    color={color}
                    onDone={(r) => {
                      if (r.hurt) recordMiss(current.q.id);
                      apply(r);
                    }}
                  />
                )}
                {current.kind === "match" && boss && <MatchRound pairs={boss.pairs} relaxed={relaxed} color={color} onDone={apply} />}
                {current.kind === "falling" && boss && <FallingRound exprs={boss.exprs} relaxed={relaxed} color={color} onDone={apply} />}
                {current.kind === "lightning" && boss && <LightningRound facts={boss.facts} relaxed={relaxed} color={color} onDone={apply} />}
                {current.kind === "strike" && <StrikeRound task={current.task} color={color} onDone={apply} />}
              </div>
            )
          )}
        </div>
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
