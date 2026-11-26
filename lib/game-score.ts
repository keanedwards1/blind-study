/**
 * Learn Python game rules: scoring a cleared stage and which stages are open. Pure functions (no React, no storage)
 * so they can be unit-tested and shared by the server and the client.
 */

import { DEV_UNLOCK_ALL } from "./dev-unlock";

/** An attempt in progress: active milliseconds, Submit presses, hints opened, and whether the solution was revealed. */
export type Attempt = { ms: number; tries: number; hints: number; peeked: boolean };
export type Stars = 0 | 1 | 2 | 3;
export type StageResult = { score: number; stars: Stars; ms: number; tries: number; at: number };
export type StageState = "cleared" | "open" | "locked";

export const NEW_ATTEMPT: Attempt = { ms: 0, tries: 0, hints: 0, peeked: false };

/*
 * A cleared stage scores up to 1500 from three parts, so time, mistakes and help all move the number on their own:
 *
 * - Accuracy (600): each wrong Submit keeps 75% of what's left (600, 450, 338, 253, ...). Run is always free.
 * - Independence (500): hints get dearer as they give more away (100, 150, 200, then 250 each). Learn mode and the
 *   lesson are free.
 * - Speed (400): halves every par time (400 at once, 200 at par, 100 at twice par, ...). Par comes from the size of
 *   this task's reference solution, so a one-liner and a 15-line task aren't timed alike. Hints save time, so speed
 *   points shrink with the independence you gave up (down to half).
 *
 * Revealing the solution scores 15% of accuracy + speed (at most 120). Leaves: 3 need no hints and 1200+,
 * 2 need 700+.
 */
const MAX_ACCURACY = 600;
const WRONG_SUBMIT_KEEPS = 0.75;
const MAX_INDEPENDENCE = 500;
const MAX_SPEED = 400;
const PEEKED_SHARE = 0.15;
const MIN_SCORE = 50;
const THREE_LEAVES = 1200;
const TWO_LEAVES = 700;

/** Par per difficulty, scaled by the reference solution's size: reading time, plus a little per line of real code. */
const PAR_BASE_MS = 45_000;
const PAR_PER_LINE_MS = 40_000;
const PAR_SCALE: Record<string, number> = { Easy: 1, Medium: 1.5, Hard: 2 };

/** Lines of the reference solution that do something (not `def`/`class` headers, decorators, imports, comments or blanks). */
function solutionLines(solution: string): number {
  const body = solution.split("\n").filter((l) => l.trim() && !/^\s*(def |class |@|#|from |import |pass\s*$)/.test(l));
  return Math.max(1, body.length);
}

/** The time at which half the speed points are gone. */
export function parMs(problem: { difficulty: string; solution: string }): number {
  return Math.round((PAR_BASE_MS + PAR_PER_LINE_MS * solutionLines(problem.solution)) * (PAR_SCALE[problem.difficulty] ?? 1));
}

/** What opening hints 1..n costs: 100, 150, 200, then 250 for each one after that. */
export function hintCost(hints: number): number {
  let cost = 0;
  for (let i = 0; i < hints; i++) cost += Math.min(250, 100 + 50 * i);
  return cost;
}

export type ScoreBreakdown = { accuracy: number; independence: number; speed: number; parMs: number; wrong: number };

/** Score, leaves and the parts behind them for a cleared stage. `tries` counts the accepted Submit, so a first-time clear has tries = 1. */
export function scoreAttempt(
  a: Attempt,
  problem: { difficulty: string; solution: string },
): { score: number; stars: Stars; breakdown: ScoreBreakdown } {
  const wrong = Math.max(0, a.tries - 1);
  const par = parMs(problem);
  const accuracy = MAX_ACCURACY * WRONG_SUBMIT_KEEPS ** wrong;
  const independence = a.peeked ? 0 : Math.max(0, MAX_INDEPENDENCE - hintCost(a.hints));
  const speed = MAX_SPEED * 2 ** (-a.ms / par) * (0.5 + (0.5 * independence) / MAX_INDEPENDENCE);
  const parts = { accuracy: Math.round(accuracy), independence: Math.round(independence), speed: Math.round(speed) };
  if (a.peeked) {
    const score = Math.max(MIN_SCORE, Math.round(PEEKED_SHARE * (accuracy + speed)));
    return { score, stars: 1, breakdown: { accuracy: 0, independence: 0, speed: 0, parMs: par, wrong } };
  }
  const score = Math.max(MIN_SCORE, parts.accuracy + parts.independence + parts.speed);
  const stars: Stars = a.hints === 0 && score >= THREE_LEAVES ? 3 : score >= TWO_LEAVES ? 2 : 1;
  return { score, stars, breakdown: { ...parts, parMs: par, wrong } };
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
  return states.length > 0 && (DEV_UNLOCK_ALL || states.every((s) => s === "cleared"));
}

/** "m:ss" for a duration in milliseconds. */
export function formatTime(ms: number): string {
  const s = Math.floor(ms / 1000);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}
