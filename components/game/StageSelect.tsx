"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { bossOpen, stageStates } from "@/lib/game-score";
import { sfx, useMusic } from "@/lib/audio/engine";
import {
  type LevelInfo,
  levelStates,
  loadAttempt,
  markIntroSeen,
  useHydrated,
  usePlacement,
  useQuizPassed,
  useResults,
  useSeenIntros,
  worldAllOpen,
} from "@/lib/python-progress";
import type { Zone } from "@/lib/python";
import { struggles, useMisses, useRepClears } from "@/lib/concept-progress";
import { useSolved } from "@/lib/storage";
import Markdown from "../Markdown";
import GameShell from "./GameShell";
import { Leaf, Lock, Owl } from "./icons";
import Scenery from "./Scenery";
import { ambienceFor, WORLD_THEME } from "./theme";
import { Button, LeafRow } from "./ui";

export type WorldInfo = {
  n: number;
  title: string;
  summary: string;
  kind: "python" | "blind";
  zones: Zone[];
};

/** Full-screen scene the first time you enter a world. */
export function WorldIntro({
  world,
  onEnter,
}: {
  world: { n: number; title: string; summary: string };
  onEnter: () => void;
}) {
  const { Icon, color, biome } = WORLD_THEME[world.n];
  return (
    // The outer layer owns the fixed positioning; the themed .game box fills it.
    <div
      className="fixed inset-0 z-50"
      role="dialog"
      aria-label={`World ${world.n}`}
    >
      <div
        className="game relative flex h-full w-full flex-col items-center justify-center gap-6 overflow-auto px-6 text-center"
        data-biome={biome}
      >
        <Scenery biome={biome} />
        <p className="n-rise-in text-sm tracking-[0.25em] text-[#c9bda4] uppercase">
          World {world.n}
        </p>
        <span className="n-rise-in" style={{ animationDelay: "150ms" }}>
          <span className="n-sway inline-block">
            <Icon size={120} />
          </span>
        </span>
        <h2
          className="font-display n-rise-in text-4xl font-extrabold sm:text-5xl"
          style={{ color, animationDelay: "300ms" }}
        >
          {world.title}
        </h2>
        {world.summary && (
          <div
            className="n-fade n-on-dark max-w-xl text-[#e5dccb]"
            style={{ animationDelay: "600ms" }}
          >
            <Markdown>{world.summary}</Markdown>
          </div>
        )}
        <div className="n-rise-in" style={{ animationDelay: "850ms" }}>
          <Button color={color} onClick={onEnter}>
            Enter the world
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function StageSelect({
  world,
  levelInfo,
}: {
  world: WorldInfo;
  levelInfo: LevelInfo[];
}) {
  const hydrated = useHydrated();
  const router = useRouter();
  const placement = usePlacement();
  const solved = useSolved();
  const quiz = useQuizPassed();
  const results = useResults();
  const intros = useSeenIntros();
  const [lesson, setLesson] = useState<Zone | null>(null);
  const misses = useMisses();
  const reps = useRepClears();
  const [shaking, setShaking] = useState<string | null>(null);
  const { Icon, color, biome } = WORLD_THEME[world.n];
  useMusic(ambienceFor(world.n, false));

  const back = { href: "/python", label: "Trail map" };
  if (!hydrated)
    return (
      <GameShell biome={biome} back={back}>
        {null}
      </GameShell>
    );

  const worldState = levelStates(levelInfo, placement, solved, quiz)[
    world.n - 1
  ];
  const playable = worldState !== "locked" && worldState !== "coming-soon";
  const slugs = world.zones.flatMap((z) => z.stages.map((s) => s.slug));
  const states = stageStates(
    slugs,
    (s) => Boolean(results[s] || solved[s]),
    worldAllOpen(worldState),
  );
  const stateOf = Object.fromEntries(slugs.map((s, i) => [s, states[i]]));
  const boss = bossOpen(states);
  const shaky =
    world.kind === "python"
      ? Object.fromEntries(
          struggles(
            world.n,
            world.zones.map((z) => ({ id: z.id, title: z.title, problems: z.stages.map((s) => s.slug) })),
            results,
            loadAttempt,
            misses,
            reps,
            (slug) => world.zones.flatMap((z) => z.stages).find((s) => s.slug === slug)?.title ?? slug,
          ).map((s) => [s.id, s]),
        )
      : {};
  const leafCount = slugs.reduce(
    (s, slug) => s + (results[slug]?.stars ?? 0),
    0,
  );

  if (!playable) {
    return (
      <GameShell biome={biome} back={back}>
        <div className="flex flex-1 flex-col items-center justify-center gap-5 px-4 text-center">
          <span className="grid h-20 w-20 place-items-center rounded-full bg-black/30 text-[#c9bda4]">
            <Lock size={36} />
          </span>
          <p className="font-display text-2xl font-bold">
            World {world.n} is still overgrown
          </p>
          <p className="max-w-md text-[#c9bda4]">
            {placement
              ? `Clear every stage of world ${world.n - 1} and get past its guardian to open this path.`
              : "Start your trail from the map first."}
          </p>
          <Button href="/python">Back to the trail</Button>
        </div>
      </GameShell>
    );
  }

  function play(slug: string) {
    if (stateOf[slug] === "locked") {
      sfx("locked");
      setShaking(slug);
      setTimeout(() => setShaking(null), 340);
      return;
    }
    sfx("click");
    router.push(`/python/${slug}`);
  }

  return (
    <GameShell
      biome={biome}
      back={back}
      title={
        <div className="flex items-center gap-3">
          <span className="n-sway">
            <Icon size={42} />
          </span>
          <div className="text-left">
            <p className="text-[11px] tracking-[0.2em] text-[#c9bda4] uppercase">
              World {world.n}
            </p>
            <h1
              className="font-display text-xl leading-tight font-extrabold sm:text-2xl"
              style={{ color }}
            >
              {world.title}
            </h1>
          </div>
        </div>
      }
    >
      {!intros[world.n] && (
        <WorldIntro
          world={world}
          onEnter={() => {
            sfx("start");
            markIntroSeen(world.n);
          }}
        />
      )}

      <div
        className="mx-auto flex w-full max-w-5xl flex-col gap-5 px-4 pt-6 pb-14"
        style={{ "--world": color } as React.CSSProperties}
      >
        <p className="flex items-center justify-center gap-1.5 text-sm text-[#c9bda4]">
          <Leaf size={15} /> {leafCount} of {slugs.length * 3} leaves collected
        </p>

        {world.zones.map((zone) => (
          <section key={zone.id} className="n-card flex flex-col gap-4 p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="font-display text-lg font-semibold">
                {zone.title}
              </h2>
              <div className="flex flex-wrap items-center gap-2">
                {shaky[zone.id] && (
                  <span
                    className="rounded-md bg-[#ff7a2f]/20 px-2 py-1 text-[11px] font-semibold text-[#ffb27a]"
                    title={`Why: ${shaky[zone.id].reasons.join("; ")}.`}
                  >
                    Shaky · rep it
                  </span>
                )}
                {zone.intro && (
                  <Button
                    ghost
                    className="px-3! py-1.5! text-xs!"
                    onClick={() => setLesson(zone)}
                  >
                    {world.kind === "python"
                      ? "Read the lesson"
                      : "About this pattern"}
                  </Button>
                )}
                {world.kind === "python" && playable && (
                  <Button
                    ghost={!shaky[zone.id]}
                    color={shaky[zone.id] ? "#ff7a2f" : undefined}
                    className="px-3! py-1.5! text-xs!"
                    href={`/python/reps/${world.n}/${zone.id}`}
                    title="A short practice set: questions and coding reps for this concept"
                  >
                    {shaky[zone.id] ? "Rep it" : "Practice"}
                  </Button>
                )}
              </div>
            </div>
            {shaky[zone.id] && (
              <p className="-mt-1 text-xs text-[#ffb27a]">
                Why: {shaky[zone.id].reasons.join("; ")}.
              </p>
            )}
            <div className="flex flex-wrap gap-4">
              {zone.stages.map((s) => {
                const state = stateOf[s.slug];
                return (
                  <div
                    key={s.slug}
                    className="flex w-[4.75rem] flex-col items-center gap-1"
                  >
                    <button
                      type="button"
                      onClick={() => play(s.slug)}
                      data-state={state}
                      className={`n-stone ${shaking === s.slug ? "n-shake" : ""}`}
                      title={
                        state === "locked"
                          ? "Clear the stage before this one to unlock it"
                          : s.title
                      }
                      aria-label={`Stage ${s.label}: ${s.title}${state === "locked" ? " (locked)" : ""}`}
                    >
                      {state === "locked" ? (
                        <Lock size={18} />
                      ) : (
                        <span className="flex flex-col items-center leading-none">
                          <span className="text-[9px] font-semibold tracking-[0.15em] uppercase opacity-60">Lvl</span>
                          <span className="mt-0.5 text-xl font-bold tabular-nums">{s.label}</span>
                        </span>
                      )}
                    </button>
                    {state !== "locked" && (
                      <LeafRow leaves={results[s.slug]?.stars ?? 0} size={13} />
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        ))}

        <section
          className="n-card flex flex-wrap items-center justify-between gap-4 p-5"
          style={boss ? { borderColor: `${color}66` } : undefined}
        >
          <div className="flex items-center gap-4">
            <span className={boss ? "n-sway" : "opacity-50 grayscale"}>
              <Owl size={64} />
            </span>
            <div>
              <p className="text-[11px] tracking-[0.2em] text-[#c9bda4] uppercase">
                The guardian
              </p>
              <p className="font-display text-lg font-semibold">
                Guardian of {world.title}
              </p>
              <p className="mt-1 text-sm text-[#c9bda4]">
                {quiz[world.n]
                  ? "You've earned its respect. Visit again any time."
                  : boss
                    ? "10 questions. Answer 8 correctly to pass."
                    : "Clear every stage to meet the guardian."}
              </p>
            </div>
          </div>
          <Button
            color={color}
            href={boss ? `/python/quiz/${world.n}` : undefined}
            disabled={!boss}
          >
            {quiz[world.n] ? "Visit again" : "Face the guardian"}
          </Button>
        </section>
      </div>

      {lesson && (
        <div
          className="fixed inset-0 z-40 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
          onClick={() => setLesson(null)}
          role="dialog"
          aria-label={lesson.title}
        >
          <div
            className="n-rise-in max-h-[85vh] w-full max-w-2xl overflow-auto rounded-2xl bg-panel p-6 text-fg shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-3 flex items-start justify-between gap-4">
              <h3 className="font-display text-xl font-semibold">
                {lesson.title}
              </h3>
              <button
                type="button"
                onClick={() => setLesson(null)}
                className="text-subtle hover:text-fg"
                aria-label="Close"
              >
                ✕
              </button>
            </div>
            <Markdown>{lesson.intro}</Markdown>
          </div>
        </div>
      )}
    </GameShell>
  );
}
