"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { formatTime, type StageResult } from "@/lib/game-score";
import { sfx } from "@/lib/audio/engine";
import Burst from "./Burst";
import { SoundButtons } from "./GameShell";
import Scenery from "./Scenery";
import { WORLD_THEME } from "./theme";
import { Button, CountUp, LeafRow } from "./ui";

export type ClearInfo = {
  result: StageResult;
  prev?: StageResult;
  best: StageResult;
  hints: number;
  peeked: boolean;
};

/** The between-stages screen: leaves earned, score, time, tries, best, and where to go next. */
export default function StageClear({
  label,
  title,
  world,
  info,
  nextHref,
  nextLabel,
  onReplay,
}: {
  label: string;
  title: string;
  world: number;
  info: ClearInfo;
  nextHref: string;
  nextLabel: string;
  onReplay: () => void;
}) {
  const router = useRouter();
  const [leavesDone, setLeavesDone] = useState(false);
  const { result, prev, hints, peeked } = info;
  const firstClear = !prev;
  const newBest = Boolean(prev && result.score > prev.score);
  const { color, biome } = WORLD_THEME[world];

  useEffect(() => {
    sfx("clear");
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Enter") {
        sfx("click");
        router.push(nextHref);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [router, nextHref]);

  const row = (k: string, v: React.ReactNode, delay: number) => (
    <div
      className="n-rise-in flex justify-between gap-6 border-b border-white/10 py-1.5 last:border-0"
      style={{ animationDelay: `${delay}ms` }}
    >
      <span className="text-[#c9bda4]">{k}</span>
      <span className="font-semibold tabular-nums">{v}</span>
    </div>
  );

  return (
    // The outer layer owns the fixed positioning; the themed .game box fills it.
    <div
      className="fixed inset-0 z-50"
      role="dialog"
      aria-label={`Stage ${label} cleared`}
    >
      <div
        className="game relative flex h-full w-full items-center justify-center overflow-auto p-4"
        data-biome={biome}
      >
        <Scenery biome={biome} />
        <Burst biome={biome} />
        <div className="absolute top-4 right-4">
          <SoundButtons />
        </div>
        <div className="n-card n-rise-in relative flex w-full max-w-md flex-col items-center gap-4 p-7 text-center">
          <p className="text-xs tracking-[0.25em] text-[#c9bda4] uppercase">
            Stage {label}
          </p>
          <h2
            className="font-display text-4xl font-extrabold"
            style={{ color }}
          >
            Cleared!
          </h2>
          <p className="text-sm text-[#e5dccb]">{title}</p>
          <LeafRow
            leaves={result.stars}
            size={44}
            animate
            onDone={() => setLeavesDone(true)}
          />
          <div className="font-display text-3xl font-extrabold text-[#e9b44c]">
            {leavesDone ? <CountUp value={result.score} /> : "0"}
            <span className="ml-1.5 text-sm font-semibold text-[#c9bda4]">
              points
            </span>
          </div>
          {(firstClear || newBest) && leavesDone && (
            <p className="n-pop text-sm font-semibold text-[#9bc26b]">
              {firstClear ? "First clear!" : "New best!"}
            </p>
          )}
          <div className="w-full text-sm">
            {row("Time", formatTime(result.ms), 1300)}
            {row("Tries", result.tries, 1400)}
            {hints > 0 && row("Hints used", hints, 1500)}
            {peeked && row("Solution", "Peeked", 1500)}
            {row(
              "Best",
              `${info.best.score.toLocaleString("en-US")} points`,
              1600,
            )}
          </div>
          <div className="flex flex-wrap justify-center gap-3 pt-2">
            <Button ghost href={`/python/world/${world}`}>
              Menu
            </Button>
            <Button ghost onClick={onReplay}>
              Replay
            </Button>
            <Button color={color} href={nextHref}>
              {nextLabel} →
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
