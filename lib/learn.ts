import raw from "@/data/learn.json";
import type { Concept, PatternGuide } from "./types";

const data = raw as unknown as { concepts: Concept[]; patterns: PatternGuide[] };

export const concepts: Concept[] = data.concepts;
export const patterns: PatternGuide[] = data.patterns;
export const conceptById: Record<string, Concept> = Object.fromEntries(concepts.map((c) => [c.id, c]));
export const patternById: Record<string, PatternGuide> = Object.fromEntries(patterns.map((p) => [p.id, p]));
export const conceptGroups: string[] = [...new Set(concepts.map((c) => c.group))];
