import type { Metadata } from "next";
import WorldMap from "@/components/game/WorldMap";
import { levelInfos, levels } from "@/lib/python";

export const metadata: Metadata = { title: "Learn Python · Drill" };

export default function PythonPage() {
  const worlds = levels.map((l, i) => ({ ...levelInfos()[i], title: l.title, kind: l.kind }));
  const leavesTotal = Object.fromEntries(levels.map((l) => [l.n, l.problems.length * 3]));
  return <WorldMap worlds={worlds} leavesTotal={leavesTotal} />;
}
