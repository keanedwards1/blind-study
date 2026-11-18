"use client";

import { useSyncExternalStore } from "react";
import { load, save, useStored, type Progress } from "./storage";
import { type Attempt, mergeResult, NEW_ATTEMPT, type StageResult } from "./game-score";
import { DEV_UNLOCK_ALL } from "./dev-unlock";

/** Placement results: one entry per task in test order. `null` = not answered yet. */
export type Placement = { level: number; at: number; results: (boolean | null)[] };
export type QuizPassed = Record<string, number>;

export type LevelState = "locked" | "current" | "unlocked" | "mastered" | "placed-out" | "coming-soon";

/** The minimum a progress calculation needs about a level (so this file never imports the big data JSON). */
export type LevelInfo = { n: number; ready: boolean; problems: string[] };

const PLACEMENT_KEY = "python:placement";
const DRAFT_KEY = "python:placement-draft";
const QUIZ_KEY = "python:quiz-passed";
const NO_QUIZ: QuizPassed = {};

export const QUIZ_SIZE = 10;
export const QUIZ_PASS = 0.8;

/** The lowest level where you didn't pass every task; pass all of them and you start at the top level. */
export function placedLevel(taskLevels: number[], results: (boolean | null)[], top = 10): number {
  let lowest = top;
  taskLevels.forEach((lv, i) => {
    if (results[i] !== true) lowest = Math.min(lowest, lv);
  });
  return lowest;
}

/**
 * Beating a world's guardian masters it. (You can only fight the guardian once every stage is cleared, so this also means
 * the stages were done, and stages added to a world later never take away a mastery you already earned.)
 */
export function isMastered(level: LevelInfo, _solved: Progress, quiz: QuizPassed): boolean {
  return level.ready && level.problems.length > 0 && Boolean(quiz[level.n]);
}

/**
 * State of every level, in order. A level is open if placement put you at or above it, or the level before it is open and
 * mastered. Levels whose content isn't written yet never block you: the next level opens straight after them.
 */
export function levelStates(levels: LevelInfo[], placement: Placement | null, solved: Progress, quiz: QuizPassed): LevelState[] {
  const out: LevelState[] = [];
  let open = placement !== null;
  let currentFound = false;
  for (const lv of levels) {
    const mastered = isMastered(lv, solved, quiz);
    const placedOut = placement !== null && lv.n < placement.level;
    let state: LevelState;
    if (!lv.ready) state = "coming-soon";
    else if (mastered) state = "mastered";
    else if (placedOut) state = "placed-out";
    else if (!open && !DEV_UNLOCK_ALL) state = "locked";
    else if (!currentFound) state = "current";
    else state = "unlocked";
    if (state === "current") currentFound = true;
    out.push(state);
    // Whether the *next* level opens.
    const reachedByPlacement = placement !== null && lv.n + 1 <= placement.level;
    open = reachedByPlacement || (open && (mastered || !lv.ready));
  }
  return out;
}

// ---- storage hooks
export function usePlacement(): Placement | null {
  return useStored<Placement | null>(PLACEMENT_KEY, null);
}
export function savePlacement(p: Placement | null) {
  save(PLACEMENT_KEY, p ?? undefined);
}

/** In-progress placement answers, so a refresh resumes the test. */
export function loadDraft(): (boolean | null)[] | null {
  return load<(boolean | null)[] | null>(DRAFT_KEY, null);
}
export function saveDraft(results: (boolean | null)[] | null) {
  save(DRAFT_KEY, results ?? undefined);
}

export function useQuizPassed(): QuizPassed {
  return useStored<QuizPassed>(QUIZ_KEY, NO_QUIZ);
}
export function markQuizPassed(level: number) {
  save(QUIZ_KEY, { ...load<QuizPassed>(QUIZ_KEY, {}), [level]: Date.now() });
}

const noop = () => () => {};
/** False during the server render and hydration, true afterwards: for pages that depend entirely on localStorage. */
export function useHydrated(): boolean {
  return useSyncExternalStore(noop, () => true, () => false);
}

// ---- game: stage results, attempts in progress, world intros
const RESULTS_KEY = "python:results";
const INTROS_KEY = "python:seen-intros";
const NO_RESULTS: Record<string, StageResult> = {};
const NO_INTROS: Record<string, number> = {};

export function useResults(): Record<string, StageResult> {
  return useStored<Record<string, StageResult>>(RESULTS_KEY, NO_RESULTS);
}

/** Record a cleared stage, keeping the best score. Returns the previous best (if any) and the merged result. */
export function recordResult(slug: string, result: StageResult): { prev?: StageResult; best: StageResult } {
  const all = load<Record<string, StageResult>>(RESULTS_KEY, {});
  const prev = all[slug];
  const best = mergeResult(prev, result);
  save(RESULTS_KEY, { ...all, [slug]: best });
  return { prev, best };
}

const attemptKey = (slug: string) => `python:attempt:${slug}`;
export function loadAttempt(slug: string): Attempt {
  return { ...NEW_ATTEMPT, ...load<Partial<Attempt>>(attemptKey(slug), {}) };
}
export function saveAttempt(slug: string, a: Attempt | null) {
  save(attemptKey(slug), a ?? undefined);
}

export function useSeenIntros(): Record<string, number> {
  return useStored<Record<string, number>>(INTROS_KEY, NO_INTROS);
}
export function markIntroSeen(world: number) {
  save(INTROS_KEY, { ...load<Record<string, number>>(INTROS_KEY, {}), [world]: Date.now() });
}

/** Worlds whose stages are all open (no one-after-another unlocking). */
export function worldAllOpen(state: LevelState): boolean {
  return DEV_UNLOCK_ALL || state === "placed-out" || state === "mastered";
}
