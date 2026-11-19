"use client";

import { usePathname } from "next/navigation";
import { WORLD_THEME } from "../game/theme";
import "./section-python.css";

/** An individual problem: a Blind 75 problem, or a Learn Python stage (not the world map, worlds, quizzes or placement). */
export function isProblemPage(path: string) {
  return /^\/problems\/[^/]+\/?$/.test(path) || /^\/python\/(?!placement\/?$)[^/]+\/?$/.test(path);
}

/** The biome of the world a Learn Python path belongs to (/python/world/8, /python/quiz/8, /python/reps/8/…), if any. */
function worldBiome(path: string): string | undefined {
  const m = /^\/python\/(?:world|quiz|reps)\/(\d+)/.exec(path);
  return m ? WORLD_THEME[Number(m[1])]?.biome : undefined;
}

/**
 * Shows the compact header on individual problem pages and the full one everywhere else. On Learn Python pages other than
 * the stages themselves, the header is wrapped in a data-section="python" box (display: contents, so layout is unchanged)
 * that turns it green.
 */
export default function HeaderSwitch({ full, compact }: { full: React.ReactNode; compact: React.ReactNode }) {
  const path = usePathname();
  const problem = isProblemPage(path);
  const header = problem ? compact : full;
  // Green on the trail, world pages and guardian fights; a stage you're coding in keeps the site's normal header.
  return !problem && (path === "/python" || path.startsWith("/python/")) ? (
    <div className="contents" data-section="python" data-biome={worldBiome(path)}>
      {header}
    </div>
  ) : (
    header
  );
}
