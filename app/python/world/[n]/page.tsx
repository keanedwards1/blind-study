import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import StageSelect from "@/components/game/StageSelect";
import { levelInfos, levels, zonesFor } from "@/lib/python";

type Params = PageProps<"/python/world/[n]">["params"];

export function generateStaticParams() {
  return levels.map((l) => ({ n: String(l.n) }));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { n } = await params;
  return { title: `World ${n} · Learn Python · Drill` };
}

export default function WorldPage({ params }: PageProps<"/python/world/[n]">) {
  return (
    <Suspense fallback={<div className="p-6 text-sm text-subtle">Loading world…</div>}>
      <WorldLoader params={params} />
    </Suspense>
  );
}

async function WorldLoader({ params }: { params: Params }) {
  const { n } = await params;
  const level = levels.find((l) => String(l.n) === n);
  if (!level) notFound();
  return (
    <StageSelect
      world={{ n: level.n, title: level.title, summary: level.summary, kind: level.kind, zones: zonesFor(level) }}
      levelInfo={levelInfos()}
    />
  );
}
