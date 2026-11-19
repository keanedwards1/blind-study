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
  /** The winning submit's tests: totals, and each edge case with the input it ran, your output and the expected answer. */
  tests?: { passed: number; total: number; edges: { note: string; ok: boolean; input: string; output: string; expected: string }[] };
};

/** The between-stages screen: leaves earned, score, time, tries, tests passed, the edge cases handled, best, and where to go next. */
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
  const { result, prev, hints, peeked, tests } = info;
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
        <div className="n-card n-rise-in relative flex w-full max-w-lg flex-col items-center gap-4 p-7 text-center">
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
            {tests && row("Tests passed", `${tests.passed} / ${tests.total}`, 1450)}
            {hints > 0 && row("Hints used", hints, 1500)}
            {peeked && row("Solution", "Peeked", 1500)}
            {row(
              "Best",
              `${info.best.score.toLocaleString("en-US")} points`,
              1600,
            )}
          </div>
          {tests && tests.edges.length > 0 && (
            <div className="n-rise-in w-full text-left" style={{ animationDelay: "1700ms" }}>
              <p className="mb-1.5 text-xs tracking-wide text-[#c9bda4] uppercase">Edge cases handled</p>
              <ul className="flex max-h-64 flex-col gap-1.5 overflow-auto pr-1">
                {tests.edges.map((e) => (
                  <li key={e.note} className="rounded bg-black/25 px-3 py-2">
                    <p className={`text-sm font-semibold ${e.ok ? "text-[#9bc26b]" : "text-[#ff7a5c]"}`}>
                      {e.ok ? "✓" : "✗"} {e.note}
                    </p>
                    <div className="mt-1 grid grid-cols-[3.5rem_minmax(0,1fr)] gap-x-2 font-mono text-xs leading-5 [font-variant-ligatures:none]">
                      <span className="text-[#c9bda4]">input</span>
                      <span className="break-words whitespace-pre-wrap text-[#f4ecdc]">{e.input}</span>
                      <span className="text-[#c9bda4]">output</span>
                      <span className="break-words whitespace-pre-wrap text-[#f4ecdc]">{e.output}</span>
                      {!e.ok && (
                        <>
                          <span className="text-[#c9bda4]">expected</span>
                          <span className="break-words whitespace-pre-wrap text-[#f4ecdc]">{e.expected}</span>
                        </>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
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
