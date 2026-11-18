"use client";

import { usePathname } from "next/navigation";

/** An individual problem: a Blind 75 problem, or a Learn Python stage (not the world map, worlds, quizzes or placement). */
export function isProblemPage(path: string) {
  return /^\/problems\/[^/]+\/?$/.test(path) || /^\/python\/(?!placement\/?$)[^/]+\/?$/.test(path);
}

/** Shows the compact header on individual problem pages and the full one everywhere else. */
export default function HeaderSwitch({ full, compact }: { full: React.ReactNode; compact: React.ReactNode }) {
  return isProblemPage(usePathname()) ? compact : full;
}
