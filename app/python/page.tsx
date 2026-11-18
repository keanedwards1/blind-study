import type { Metadata } from "next";
import WorldMap from "@/components/game/WorldMap";
import { levelInfos, levels } from "@/lib/python";

export const metadata: Metadata = { title: "Learn Python · Blind 75 from Scratch" };

export default function PythonPage() {
  const worlds = levels.map((l, i) => ({
    ...levelInfos()[i],
    title: l.title,
    kind: l.kind,
    concepts: l.concepts.map((c) => ({ id: c.id, title: c.title, problems: c.problems })),
  }));
  const leavesTotal = Object.fromEntries(levels.map((l) => [l.n, l.problems.length * 3]));
  return <WorldMap worlds={worlds} leavesTotal={leavesTotal} />;
}
