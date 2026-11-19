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
  tests?: { passed: number; total: number; edges: { note: string; hidden?: boolean; ok: boolean; input: string; output: string; expected: string }[] };
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
  const hasEdges = Boolean(tests && tests.edges.length > 0);
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
        className="game relative flex h-full w-full justify-center overflow-auto p-4"
        data-biome={biome}
      >
        <Scenery biome={biome} />
        <Burst biome={biome} />
        <div className="absolute top-4 right-4">
          <SoundButtons />
        </div>
        {/* Wide screens: the test cases on the left (scrolling on their own) and the result and stats on the right, so the card
            fits the viewport instead of growing tall. Narrow screens put the result first; stages without test cases use one column. */}
        <div
          className={`n-card n-rise-in relative my-auto flex w-full flex-col gap-5 p-6 sm:p-7 ${hasEdges ? "max-w-4xl" : "max-w-lg"}`}
        >
          <div className={`grid w-full gap-6 ${hasEdges ? "md:grid-cols-2 md:gap-8" : ""}`}>
            <div className="flex flex-col items-center gap-3 text-center md:order-2">
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
                size={40}
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
              <div className="w-full text-left text-sm">
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
            </div>
            {hasEdges && tests && (
              <div className="n-rise-in flex min-h-0 w-full flex-col text-left md:order-1" style={{ animationDelay: "1700ms" }}>
                <p className="mb-2 text-xs tracking-wide text-[#c9bda4] uppercase">Test cases</p>
                <ul className="flex max-h-64 flex-col gap-1.5 overflow-auto pr-1 md:max-h-[min(28rem,calc(100dvh-13rem))]">
                  {/* Numbered like the IDE's Test cases list (labelled tests in order, description as a tooltip), with the
                      hidden tests Submit also ran continuing the count. */}
                  {tests.edges.map((e, n) => (
                    <li key={n} className="rounded bg-black/25 px-3 py-2" title={e.note || undefined}>
                      <p className={`flex items-center gap-2 text-sm font-semibold ${e.ok ? "text-[#9bc26b]" : "text-[#ff7a5c]"}`}>
                        <CaseMark ok={e.ok} delay={1900 + n * 140} />
                        Case {n + 1}
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
          </div>
          <div className="flex flex-wrap justify-center gap-3">
            <Button ghost href="/python">
              Main menu
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

/** A ticked-off circle (or a crossed one for a failure) that pops in one after another down the Test cases list. */
function CaseMark({ ok, delay }: { ok: boolean; delay: number }) {
  return (
    <svg
      viewBox="0 0 20 20"
      className="n-pop h-[18px] w-[18px] shrink-0"
      style={{ animationDelay: `${delay}ms` }}
      role="img"
      aria-label={ok ? "Passed" : "Failed"}
    >
      <circle cx="10" cy="10" r="8.75" fill="currentColor" fillOpacity="0.18" stroke="currentColor" strokeWidth="1.5" />
      {ok ? (
        <path d="M6 10.4l2.6 2.6L14 7.6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      ) : (
        <path d="M7 7l6 6M13 7l-6 6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      )}
    </svg>
  );
}
