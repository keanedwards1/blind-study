import type { Metadata } from "next";
import PlacementTest from "@/components/PlacementTest";
import { levels, placementProblems, placementTasks } from "@/lib/python";

export const metadata: Metadata = { title: "Placement test · Learn Python · Blind 75 from Scratch" };

export default function PlacementPage() {
  const problems = placementProblems();
  return (
    <PlacementTest
      tasks={placementTasks.map((t, i) => ({ level: t.level, problem: problems[i] }))}
      levelTitles={Object.fromEntries(levels.map((l) => [l.n, l.title]))}
    />
  );
}
