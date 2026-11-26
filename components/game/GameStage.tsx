"use client";

import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import type { Concept, Problem, RunOutcome } from "@/lib/types";
import { show } from "@/lib/format";
import { formatPyArgs } from "@/lib/py-args";
import { type Attempt, NEW_ATTEMPT, scoreAttempt, stageStates } from "@/lib/game-score";
import { useMusic } from "@/lib/audio/engine";
import {
  type LevelInfo,
  levelStates,
  loadAttempt,
  recordResult,
  saveAttempt,
  useHydrated,
  usePlacement,
  useQuizPassed,
  useResults,
  worldAllOpen,
} from "@/lib/python-progress";
import { save, useSolved } from "@/lib/storage";
import StageIDE from "./StageIDE";
import GameShell, { SoundButtons, useAudioUnlock } from "./GameShell";
import { Lock } from "./icons";
import MusicVisual, { useVisualEnabled, VisualToggle } from "./visual/MusicVisual";
import StageClear, { type ClearInfo } from "./StageClear";
import { ambienceFor, WORLD_THEME } from "./theme";
import { Button } from "./ui";

export type StageContext = {
  label: string;
  world: { n: number; title: string };
  worldSlugs: string[];
  next?: { slug: string; label: string };
  /** The concept group's lesson (Learn Python worlds only). */
  lesson?: { title: string; intro: string };
};

/** A playable stage: the normal workspace plus sound switches, quiet tracking of time and tries, and the Stage Cleared screen. */
export default function GameStage({
  problem,
  concepts,
  stage,
  levelInfo,
}: {
  problem: Problem;
  concepts: Concept[];
  stage: StageContext;
  levelInfo: LevelInfo[];
}) {
  const slug = problem.slug;
  const hydrated = useHydrated();
  const placement = usePlacement();
  const solved = useSolved();
  const quiz = useQuizPassed();
  const results = useResults();
  const visualOn = useVisualEnabled();
  const [cleared, setCleared] = useState<ClearInfo | null>(null);
  // Next keeps a page you leave alive but hidden. When this stage hides, drop its Stage Cleared screen so coming back
  // starts a fresh attempt instead of showing the old result again.
  useLayoutEffect(() => () => setCleared(null), []);
  const [workspaceKey, setWorkspaceKey] = useState(0);
  const attempt = useRef<Attempt>(NEW_ATTEMPT);
  const lastTick = useRef<number | null>(null);
  /** Set once the stage is cleared, so the timer's cleanup doesn't save a fresh attempt over the finished one. */
  const done = useRef(false);
  useAudioUnlock();
  useMusic(ambienceFor(stage.world.n, !cleared));

  /** Add the active time since the last tick (only while the tab is visible). Not shown while coding; it appears on the Stage Cleared screen. */
  const tick = useCallback(() => {
    const now = performance.now();
    if (lastTick.current !== null && !document.hidden) attempt.current = { ...attempt.current, ms: attempt.current.ms + (now - lastTick.current) };
    lastTick.current = document.hidden ? null : now;
  }, []);

  // Load the attempt in progress (time and tries carry over between visits until the stage is cleared).
  useEffect(() => {
    attempt.current = loadAttempt(slug);
    done.current = false;
    lastTick.current = performance.now();
  }, [slug, workspaceKey]);

  // The clock runs until the stage is cleared; progress is saved every few seconds and when leaving.
  useEffect(() => {
    if (cleared) return;
    let n = 0;
    const id = setInterval(() => {
      tick();
      if (++n % 5 === 0) saveAttempt(slug, attempt.current);
    }, 1000);
    const onVisibility = () => tick();
    const persist = () => {
      if (done.current) return;
      tick();
      saveAttempt(slug, attempt.current);
    };
    document.addEventListener("visibilitychange", onVisibility);
    window.addEventListener("pagehide", persist);
    return () => {
      clearInterval(id);
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("pagehide", persist);
      persist();
    };
  }, [cleared, slug, tick]);

  function onSubmitted(o: RunOutcome) {
    tick();
    attempt.current = { ...attempt.current, tries: attempt.current.tries + 1 };
    if (o.compileError || o.passed !== o.total) {
      saveAttempt(slug, attempt.current);
      return;
    }
    const a = attempt.current;
    const { score, stars, breakdown } = scoreAttempt(a, problem);
    const result = { score, stars, ms: Math.round(a.ms), tries: a.tries, at: Date.now() };
    const { prev, best } = recordResult(slug, result);
    done.current = true;
    attempt.current = NEW_ATTEMPT;
    saveAttempt(slug, null);
    // The submit's test results, for the clear screen: the totals plus each labelled test case, then each hidden test
    // (unlabelled, past the examples), with its input and answer.
    const clip = (text: string) => (text.length > 120 ? `${text.slice(0, 117)}…` : text);
    const entry = (i: number, hidden: boolean) => ({
      note: o.tests[i].note ?? "",
      hidden,
      ok: o.cases[i]?.status === "pass",
      input: clip(formatPyArgs(o.tests[i].args)),
      output: clip(show(problem.spec, o.cases[i]?.result)),
      expected: clip(show(problem.spec, o.tests[i].expected)),
    });
    const indexes = o.tests.map((_, i) => i);
    const edges = [
      ...indexes.filter((i) => o.tests[i].note).map((i) => entry(i, false)),
      ...indexes.filter((i) => i >= problem.examples.length && !o.tests[i].note).map((i) => entry(i, true)),
    ];
    setCleared({ result, prev, best, hints: a.hints, peeked: a.peeked, breakdown, tests: { passed: o.passed, total: o.total, edges } });
  }

  function bump(change: Partial<Attempt>) {
    attempt.current = { ...attempt.current, ...change };
    saveAttempt(slug, attempt.current);
  }

  function replay() {
    save(`code:${slug}`, undefined);
    saveAttempt(slug, null);
    attempt.current = NEW_ATTEMPT;
    setCleared(null);
    setWorkspaceKey((k) => k + 1);
  }

  if (hydrated) {
    const worldState = levelStates(levelInfo, placement, solved, quiz)[stage.world.n - 1];
    const states = stageStates(stage.worldSlugs, (s) => Boolean(results[s] || solved[s]), worldAllOpen(worldState));
    const locked = worldState === "locked" || worldState === "coming-soon" || states[stage.worldSlugs.indexOf(slug)] === "locked";
    if (locked && !cleared) {
      return (
        <GameShell biome={WORLD_THEME[stage.world.n].biome} back={{ href: `/python/world/${stage.world.n}`, label: `World ${stage.world.n}` }}>
          <div className="flex flex-1 flex-col items-center justify-center gap-5 px-4 text-center">
            <span className="grid h-20 w-20 place-items-center rounded-full bg-black/30 text-[#c9bda4]">
              <Lock size={36} />
            </span>
            <p className="font-display text-2xl font-bold">Stage {stage.label} is still locked</p>
            <p className="max-w-md text-[#c9bda4]">
              {!placement
                ? "Start a new game from the world map first."
                : worldState === "locked" || worldState === "coming-soon"
                  ? `World ${stage.world.n} isn't open yet. Beat the boss of world ${stage.world.n - 1} first.`
                  : "Clear the stages before it first."}
            </p>
            <Button href={`/python/world/${stage.world.n}`}>Back to world {stage.world.n}</Button>
          </div>
        </GameShell>
      );
    }
  }

  // Only the sound switches while you work; tries and time are tracked quietly and shown on the Stage Cleared screen.
  const hudView = (
    <div className="flex items-center gap-1">
      <VisualToggle />
      <SoundButtons tone="site" />
    </div>
  );

  return (
    <>
      <StageIDE
        key={`${slug}:${workspaceKey}`}
        problem={problem}
        concepts={concepts}
        lesson={stage.lesson}
        back={{ href: `/python/world/${stage.world.n}`, label: `World ${stage.world.n}` }}
        barRight={hudView}
        visual={visualOn ? <MusicVisual accent={WORLD_THEME[stage.world.n].color} /> : undefined}
        onSubmitted={onSubmitted}
        // Charged by the deepest hint opened, so showing hints again after coming back to the stage costs nothing more.
        onHintShown={(n) => bump({ hints: Math.max(attempt.current.hints, n) })}
        onSolutionRevealed={() => bump({ peeked: true })}
      />
      {cleared && (
        <StageClear
          label={stage.label}
          title={problem.title}
          world={stage.world.n}
          info={cleared}
          // Next returns to this world's stage select (with the next stage highlighted); after the last stage it goes on to the boss.
          nextHref={stage.next ? `/python/world/${stage.world.n}?next=${stage.next.slug}` : `/python/quiz/${stage.world.n}`}
          nextLabel={stage.next ? "Next" : "Boss"}
          onReplay={replay}
        />
      )}
    </>
  );
}
