"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Fragment, useState } from "react";
import { audio, sfx, useMusic } from "@/lib/audio/engine";
import { load, save, useSolved } from "@/lib/storage";
import { type LevelInfo, type LevelState, levelStates, savePlacement, useHydrated, usePlacement, useQuizPassed, useResults } from "@/lib/python-progress";
import GameShell from "./GameShell";
import { Leaf, Lock } from "./icons";
import Scenery from "./Scenery";
import { type Biome, BIOME_NAME, WORLD_THEME } from "./theme";
import { Button } from "./ui";

export type MapWorld = LevelInfo & { title: string; kind: "python" | "blind" };

const WELCOME_KEY = "python:welcomed";

/** First visit only: a calm opening scene. Starting also switches the sound on (browsers need a click for that). */
function Welcome({ onBegin }: { onBegin: () => void }) {
  const icons = [1, 4, 6, 9];
  return (
    <div className="relative flex flex-1 flex-col items-center justify-center gap-8 px-6 py-16 text-center">
      <div className="flex items-end gap-4">
        {icons.map((n, i) => {
          const { Icon } = WORLD_THEME[n];
          return (
            <span key={n} className="n-sway n-rise-in" style={{ animationDelay: `${i * 160}ms, ${i * 160}ms` }}>
              <Icon size={i === 2 ? 72 : 52} />
            </span>
          );
        })}
      </div>
      <h1 className="font-display n-rise-in text-5xl font-extrabold text-[#f4ecdc] sm:text-6xl" style={{ animationDelay: "300ms" }}>
        Learn Python
      </h1>
      <p className="n-fade max-w-md text-lg text-[#c9bda4]" style={{ animationDelay: "600ms" }}>
        A trail from the first seed to the firelands. Ten worlds, one guardian at the end of each.
      </p>
      <div className="n-rise-in" style={{ animationDelay: "900ms" }}>
        <Button onClick={onBegin}>Begin the trail</Button>
      </div>
    </div>
  );
}

const BANDS: { biome: Biome; worlds: number[]; reverse: boolean }[] = [
  { biome: "soil", worlds: [1, 2, 3], reverse: false },
  { biome: "forest", worlds: [4, 5, 6, 7], reverse: true },
  { biome: "fire", worlds: [8, 9, 10], reverse: false },
];

const STATE_NOTE: Partial<Record<LevelState, string>> = { mastered: "Complete", "placed-out": "Skipped ahead", "coming-soon": "Coming soon" };

export default function WorldMap({ worlds, leavesTotal }: { worlds: MapWorld[]; leavesTotal: Record<number, number> }) {
  const hydrated = useHydrated();
  const router = useRouter();
  const placement = usePlacement();
  const solved = useSolved();
  const quiz = useQuizPassed();
  const results = useResults();
  const [welcomed, setWelcomed] = useState(false);
  const [shaking, setShaking] = useState<number | null>(null);
  useMusic("forest");

  if (!hydrated) return <GameShell biome="forest">{null}</GameShell>;

  if (!welcomed && !load<boolean>(WELCOME_KEY, false)) {
    return (
      <GameShell biome="forest">
        <Welcome
          onBegin={() => {
            audio().unlock();
            sfx("start");
            save(WELCOME_KEY, true);
            setWelcomed(true);
          }}
        />
      </GameShell>
    );
  }

  const states = levelStates(worlds, placement, solved, quiz);
  const leaves = (w: MapWorld) => w.problems.reduce((s, slug) => s + (results[slug]?.stars ?? 0), 0);

  function open(w: MapWorld, state: LevelState) {
    if (state === "locked" || state === "coming-soon") {
      sfx("locked");
      setShaking(w.n);
      setTimeout(() => setShaking(null), 340);
      return;
    }
    sfx("click");
    router.push(`/python/world/${w.n}`);
  }

  const clearing = (n: number) => {
    const w = worlds[n - 1];
    const state = states[n - 1];
    const { Icon, color } = WORLD_THEME[n];
    const locked = state === "locked" || state === "coming-soon";
    return (
      <button
        type="button"
        onClick={() => open(w, state)}
        className={`n-clearing shrink-0 ${shaking === n ? "n-shake" : ""}`}
        data-current={state === "current"}
        data-locked={locked}
        style={{ "--world": color } as React.CSSProperties}
        aria-label={`World ${n}: ${w.title}${locked ? " (locked)" : ""}`}
      >
        {state === "current" && <span className="absolute -top-6 rounded-full bg-[#e9b44c] px-2 py-0.5 text-[11px] font-semibold text-[#22170e]">You are here</span>}
        <span className="ring relative">
          <span className={locked ? "opacity-40" : "n-sway"}>
            <Icon size={58} />
          </span>
          {locked && (
            <span className="absolute grid h-9 w-9 place-items-center rounded-full bg-[#22170e] text-[#c9bda4]">
              <Lock size={18} />
            </span>
          )}
        </span>
        <span className="text-[11px] tracking-wide text-[#c9bda4] uppercase">World {n}</span>
        <span className="font-display text-sm leading-snug font-semibold" style={{ color: locked ? "#8f8470" : color }}>
          {w.title}
        </span>
        <span className="flex items-center gap-1 text-xs text-[#c9bda4]">
          <Leaf size={13} /> {leaves(w)}/{leavesTotal[n]}
        </span>
        {STATE_NOTE[state] && <span className="text-[11px] text-[#8f8470]">{STATE_NOTE[state]}</span>}
      </button>
    );
  };

  return (
    <GameShell biome="forest" title={<h1 className="font-display text-2xl font-extrabold">The trail</h1>}>
      <div className="mx-auto flex w-full max-w-5xl flex-col px-4 pt-6 pb-14">
        {!placement && (
          <div className="n-card n-rise-in mx-auto mb-8 flex max-w-xl flex-col items-center gap-4 p-6 text-center">
            <p className="font-display text-xl font-semibold">Where does your trail start?</p>
            <p className="text-[#c9bda4]">Take the 20-task placement test to find your starting world, or start at the very first seed.</p>
            <div className="flex flex-wrap justify-center gap-3">
              <Button href="/python/placement">Placement test</Button>
              <Button ghost onClick={() => savePlacement({ level: 1, at: Date.now(), results: [] })}>
                Start at world 1
              </Button>
            </div>
          </div>
        )}

        {BANDS.map((band, b) => (
          <Fragment key={band.biome}>
            {b > 0 && (
              <div className={`flex ${BANDS[b - 1].reverse ? "sm:justify-start" : "sm:justify-end"} justify-center px-16`}>
                <span className="n-trail down" />
              </div>
            )}
            <section className="game relative overflow-hidden rounded-3xl px-4 py-10 sm:px-8" data-biome={band.biome} style={{ minHeight: 280 }}>
              <Scenery biome={band.biome} />
              <p className="font-display relative mb-12 text-center text-sm tracking-[0.2em] text-[#c9bda4] uppercase">{BIOME_NAME[band.biome]}</p>
              <div className={`relative flex flex-col items-center sm:items-start ${band.reverse ? "sm:flex-row-reverse" : "sm:flex-row"}`}>
                {band.worlds.map((n, i) => (
                  <Fragment key={n}>
                    {i > 0 && (
                      <>
                        <span className="n-trail hidden sm:block" />
                        <span className="n-trail down my-2 sm:hidden" />
                      </>
                    )}
                    {clearing(n)}
                  </Fragment>
                ))}
              </div>
            </section>
          </Fragment>
        ))}

        {placement && (
          <p className="mt-8 text-center text-xs text-[#8f8470]">
            Placed at world {placement.level} ·{" "}
            <Link href="/python/placement" className="underline hover:text-[#c9bda4]">
              retake the placement test
            </Link>
          </p>
        )}
      </div>
    </GameShell>
  );
}
