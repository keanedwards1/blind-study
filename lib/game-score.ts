/**
 * Learn Python game rules: scoring a cleared stage and which stages are open. Pure functions (no React, no storage)
 * so they can be unit-tested and shared by the server and the client.
 */

/** An attempt in progress: active milliseconds, Submit presses, hints opened, and whether the solution was revealed. */
export type Attempt = { ms: number; tries: number; hints: number; peeked: boolean };
export type Stars = 0 | 1 | 2 | 3;
export type StageResult = { score: number; stars: Stars; ms: number; tries: number; at: number };
export type StageState = "cleared" | "open" | "locked";

export const NEW_ATTEMPT: Attempt = { ms: 0, tries: 0, hints: 0, peeked: false };

/** Par time per difficulty: the time bonus shrinks to zero here, and 3 stars need to be under it. */
export const PAR_MS: Record<string, number> = { Easy: 5 * 60_000, Medium: 15 * 60_000, Hard: 30 * 60_000 };

const BASE = 1000;
const PER_EXTRA_TRY = 100;
const MIN_BASE = 200;
const PER_HINT = 150;
const MAX_TIME_BONUS = 500;
const PEEKED_SCORE = 100;

/** Score and stars for a cleared stage. `tries` counts the accepted Submit too, so a first-time clear has tries = 1. */
export function scoreAttempt(a: Attempt, difficulty: string): { score: number; stars: Stars } {
  if (a.peeked) return { score: PEEKED_SCORE, stars: 1 };
  const tries = Math.max(1, a.tries);
  const base = Math.max(MIN_BASE, BASE - PER_EXTRA_TRY * (tries - 1)) - PER_HINT * a.hints;
  const par = PAR_MS[difficulty] ?? PAR_MS.Easy;
  const timeBonus = Math.round(MAX_TIME_BONUS * Math.max(0, 1 - a.ms / par));
  const score = Math.max(PEEKED_SCORE, base + timeBonus);
  const stars: Stars = tries <= 2 && a.hints === 0 && a.ms <= par ? 3 : tries <= 5 ? 2 : 1;
  return { score, stars };
}

/** Keep the best score, and the best star count ever earned. */
export function mergeResult(prev: StageResult | undefined, next: StageResult): StageResult {
  if (!prev) return next;
  const best = next.score > prev.score ? next : prev;
  return { ...best, stars: Math.max(prev.stars, next.stars) as Stars };
}

/**
 * Stage states for one world, in order. Cleared stages stay cleared; otherwise the first uncleared stage is open and the rest
 * are locked (one after another). With `allOpen` (a world you placed out of or already mastered) every stage is open.
 */
export function stageStates(slugs: string[], cleared: (slug: string) => boolean, allOpen: boolean): StageState[] {
  let openGiven = false;
  return slugs.map((s) => {
    if (cleared(s)) return "cleared";
    if (allOpen) return "open";
    if (!openGiven) {
      openGiven = true;
      return "open";
    }
    return "locked";
  });
}

export function bossOpen(states: StageState[]): boolean {
  return states.length > 0 && states.every((s) => s === "cleared");
}

/** "m:ss" for a duration in milliseconds. */
export function formatTime(ms: number): string {
  const s = Math.floor(ms / 1000);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}
