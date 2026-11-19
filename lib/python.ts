import raw from "@/data/python.json";
import type { PlacementTask, Problem, PyLevel } from "./types";
import { patterns } from "./learn";
import { getProblem } from "./problems";

const data = raw as unknown as { levels: PyLevel[]; placement: PlacementTask[]; problems: Problem[] };

export const levels: PyLevel[] = data.levels;
export const placementTasks: PlacementTask[] = data.placement;
export const pyProblems: Problem[] = data.problems;

const bySlug = new Map(pyProblems.map((p) => [p.slug, p]));
const placementSlugs = new Set(placementTasks.map((t) => t.slug));

/** A Learn Python level problem (placement tasks are excluded; they only appear inside the test). */
export function getPyProblem(slug: string): Problem | undefined {
  return placementSlugs.has(slug) ? undefined : bySlug.get(slug);
}

export function levelOf(slug: string): PyLevel | undefined {
  return levels.find((l) => l.problems.includes(slug));
}

export function placementProblems(): Problem[] {
  return placementTasks.map((t) => bySlug.get(t.slug)!);
}

/** Title + difficulty for any problem a level lists, whether it's a Learn Python task or a Blind 75 problem. */
export function problemSummary(slug: string): { slug: string; title: string; difficulty: string } {
  const p = bySlug.get(slug) ?? getProblem(slug);
  if (!p) throw new Error(`unknown problem ${slug}`);
  return { slug, title: p.title, difficulty: p.difficulty };
}

/** Every stage, including Blind 75 problems in levels 8-10, plays inside the game at /python/[slug]. */
export function problemHref(slug: string): string {
  return `/python/${slug}`;
}

/** The problem behind a stage: a Learn Python task, or a Blind 75 problem that belongs to level 8-10. */
export function stageProblem(slug: string): Problem | undefined {
  const level = levelOf(slug);
  if (!level) return undefined;
  return level.kind === "blind" ? getProblem(slug) : getPyProblem(slug);
}

/** "4": the stage's number within its world. Every screen that shows it already names the world, so there's no "3-" prefix. */
export function stageLabel(level: PyLevel, slug: string): string {
  return String(level.problems.indexOf(slug) + 1);
}

export type StageInfo = { slug: string; title: string; difficulty: string; label: string };
export type Zone = { id: string; title: string; intro: string; stages: StageInfo[] };

/** A world's stages grouped for the stage map: by concept (levels 1-7) or by Blind 75 pattern (levels 8-10). */
export function zonesFor(level: PyLevel): Zone[] {
  const stage = (slug: string): StageInfo => ({ ...problemSummary(slug), label: stageLabel(level, slug) });
  if (level.kind === "python") return level.concepts.map((c) => ({ id: c.id, title: c.title, intro: c.intro, stages: c.problems.map(stage) }));
  const zones: Zone[] = [];
  for (const slug of level.problems) {
    const category = getProblem(slug)!.category;
    let zone = zones.find((z) => z.title === category);
    if (!zone) {
      zone = { id: category, title: category, intro: patterns.find((pt) => pt.category === category)?.summary ?? "", stages: [] };
      zones.push(zone);
    }
    zone.stages.push(stage(slug));
  }
  return zones;
}

/** The progress calculation only needs these fields of each level. */
export function levelInfos() {
  return levels.map((l) => ({ n: l.n, ready: l.ready, problems: l.problems }));
}
