"use client";

/**
 * Which Learn Python concepts you're struggling with, and the rep room's record.
 *
 * A concept is "shaky" when any of these happened since you last cleared its rep room:
 * - a stage was cleared with 1 leaf (solution revealed or lots of tries), or after 4+ tries;
 * - a stage still in progress has 3+ failed submits, or its solution was revealed;
 * - you missed 2+ of the guardian's questions about it.
 *
 * Everything is derived from data the game already stores, plus two small records here:
 * python:quiz-misses ({ "4:dict-basics": { n, at } }) and python:reps ({ "4:dict-basics": clearedAt }).
 */
import { load, save, useStored } from "./storage";
import type { Attempt, StageResult } from "./game-score";
import type { PyConcept } from "./types";

const MISSES_KEY = "python:quiz-misses";
const REPS_KEY = "python:reps";

export type Misses = Record<string, { n: number; at: number }>;
export type RepClears = Record<string, number>;
const NO_MISSES: Misses = {};
const NO_REPS: RepClears = {};

export const conceptKey = (level: number, id: string) => `${level}:${id}`;

/** The concept a quiz or rep question belongs to, from its id ("py:4:dict-basics:0" or "py:4:dict-basics:rep:2"). */
export function conceptOfQuestion(questionId: string): { level: number; id: string } | null {
  const m = /^py:(\d+):([^:]+):/.exec(questionId);
  return m ? { level: Number(m[1]), id: m[2] } : null;
}

export function useMisses(): Misses {
  return useStored<Misses>(MISSES_KEY, NO_MISSES);
}
export function useRepClears(): RepClears {
  return useStored<RepClears>(REPS_KEY, NO_REPS);
}

/** A wrong guardian answer counts against the question's concept. */
export function recordMiss(questionId: string) {
  const c = conceptOfQuestion(questionId);
  if (!c) return;
  const all = load<Misses>(MISSES_KEY, {});
  const key = conceptKey(c.level, c.id);
  save(MISSES_KEY, { ...all, [key]: { n: (all[key]?.n ?? 0) + 1, at: Date.now() } });
}

/** Clearing a rep session resets the concept: the misses are forgiven and earlier struggles stop counting. */
export function recordRepCleared(level: number, id: string) {
  const key = conceptKey(level, id);
  save(REPS_KEY, { ...load<RepClears>(REPS_KEY, {}), [key]: Date.now() });
  const misses = load<Misses>(MISSES_KEY, {});
  if (misses[key]) {
    const { [key]: _gone, ...rest } = misses;
    void _gone;
    save(MISSES_KEY, rest);
  }
}

export type Struggle = { id: string; title: string; reasons: string[] };

/**
 * The shaky concepts of one world, with plain-English reasons.
 * `attempt` reads the in-progress attempt for a stage (python:attempt:<slug>); `titleOf` names a stage.
 */
export function struggles(
  level: number,
  concepts: Pick<PyConcept, "id" | "title" | "problems">[],
  results: Record<string, StageResult>,
  attempt: (slug: string) => Attempt,
  misses: Misses,
  reps: RepClears,
  titleOf: (slug: string) => string,
): Struggle[] {
  const out: Struggle[] = [];
  for (const c of concepts) {
    const key = conceptKey(level, c.id);
    const clearedAt = reps[key] ?? 0;
    const reasons: string[] = [];
    for (const slug of c.problems) {
      const r = results[slug];
      if (r) {
        if (r.at <= clearedAt) continue;
        if (r.stars <= 1) reasons.push(`“${titleOf(slug)}” took the solution or a lot of tries`);
        else if (r.tries >= 4) reasons.push(`“${titleOf(slug)}” took ${r.tries} tries`);
      } else if (!clearedAt) {
        const a = attempt(slug);
        if (a.peeked) reasons.push(`you revealed the solution to “${titleOf(slug)}”`);
        else if (a.tries >= 3) reasons.push(`“${titleOf(slug)}” has failed ${a.tries} times so far`);
      }
    }
    const m = misses[key];
    if (m && m.n >= 2 && m.at > clearedAt) reasons.push(`the guardian caught you out ${m.n} times`);
    if (reasons.length) out.push({ id: c.id, title: c.title, reasons });
  }
  return out;
}
