"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useRef, useState } from "react";
import type { ProblemSummary } from "@/lib/types";
import { difficultyColor } from "@/lib/format";
import { exportAll, importAll, useAttempted, useSolved } from "@/lib/storage";

type Status = "all" | "solved" | "unsolved";

export default function ProblemList({ problems, categories }: { problems: ProblemSummary[]; categories: string[] }) {
  const solved = useSolved();
  const attempted = useAttempted();
  const router = useRouter();
  const [q, setQ] = useState("");
  const [diff, setDiff] = useState("all");
  const [status, setStatus] = useState<Status>("all");
  const fileRef = useRef<HTMLInputElement>(null);

  const filtered = useMemo(
    () =>
      problems.filter(
        (p) =>
          (!q || p.title.toLowerCase().includes(q.toLowerCase())) &&
          (diff === "all" || p.difficulty === diff) &&
          (status === "all" || (status === "solved" ? !!solved[p.slug] : !solved[p.slug])),
      ),
    [problems, q, diff, status, solved],
  );

  const total = problems.length;
  const solvedCount = problems.filter((p) => solved[p.slug]).length;
  const byDiff = (d: string) => {
    const all = problems.filter((p) => p.difficulty === d);
    return `${all.filter((p) => solved[p.slug]).length}/${all.length}`;
  };

  function pickRandom() {
    const pool = problems.filter((p) => !solved[p.slug]);
    const from = pool.length ? pool : problems;
    router.push(`/problems/${from[Math.floor(Math.random() * from.length)].slug}`);
  }

  function doExport() {
    const blob = new Blob([exportAll()], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `drill-progress-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  async function doImport(f: File) {
    try {
      importAll(await f.text());
    } catch {
      alert("That file isn't a valid progress export.");
    }
  }

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-8">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-fg">Problems</h1>
          <p className="mt-1 text-sm text-muted">
            {solvedCount} / {total} solved · <span className={difficultyColor.Easy}>Easy {byDiff("Easy")}</span> ·{" "}
            <span className={difficultyColor.Medium}>Medium {byDiff("Medium")}</span> · <span className={difficultyColor.Hard}>Hard {byDiff("Hard")}</span>
          </p>
          <div className="mt-2 h-1.5 w-64 max-w-full overflow-hidden rounded-full bg-raised">
            <div className="h-full bg-emerald-500" style={{ width: `${(solvedCount / total) * 100}%` }} />
          </div>
        </div>
        <div className="flex gap-2">
          <button onClick={pickRandom} className="rounded-md border border-line-strong px-3 py-1.5 text-sm text-fg-2 hover:bg-hover">
            Random unsolved
          </button>
          <Link href="/mock" className="rounded-md bg-amber-500 px-3 py-1.5 text-sm font-medium text-zinc-950 hover:bg-amber-400">
            Start mock assessment
          </Link>
        </div>
      </div>

      <div className="mb-6 flex flex-wrap gap-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search problems"
          className="min-w-0 flex-1 rounded-md border border-line bg-panel px-3 py-1.5 text-sm text-fg placeholder:text-subtle focus:border-line-strong focus:outline-none"
        />
        <select value={diff} onChange={(e) => setDiff(e.target.value)} className="rounded-md border border-line bg-panel px-2 py-1.5 text-sm text-fg-2">
          <option value="all">All difficulties</option>
          <option>Easy</option>
          <option>Medium</option>
          <option>Hard</option>
        </select>
        <select value={status} onChange={(e) => setStatus(e.target.value as Status)} className="rounded-md border border-line bg-panel px-2 py-1.5 text-sm text-fg-2">
          <option value="all">All</option>
          <option value="unsolved">Unsolved</option>
          <option value="solved">Solved</option>
        </select>
      </div>

      <div className="space-y-6">
        {categories.map((cat) => {
          const items = filtered.filter((p) => p.category === cat);
          if (!items.length) return null;
          const all = problems.filter((p) => p.category === cat);
          const done = all.filter((p) => solved[p.slug]).length;
          return (
            <section key={cat}>
              <div className="mb-2 flex items-center justify-between">
                <h2 className="text-sm font-semibold uppercase tracking-wide text-fg-2">{cat}</h2>
                <span className="text-xs text-subtle">
                  {done}/{all.length}
                </span>
              </div>
              <ul className="divide-y divide-line overflow-hidden rounded-lg border border-line">
                {items.map((p) => (
                  <li key={p.slug}>
                    <Link href={`/problems/${p.slug}`} className="flex items-center gap-3 px-4 py-2.5 hover:bg-hover">
                      <span className="w-4 text-center text-sm">
                        {solved[p.slug] ? <span className="text-ok">✓</span> : attempted[p.slug] ? <span className="text-warn/70">•</span> : ""}
                      </span>
                      <span className="flex-1 text-sm text-fg">{p.title}</span>
                      <span className={`text-xs ${difficultyColor[p.difficulty]}`}>{p.difficulty}</span>
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          );
        })}
        {!filtered.length && <p className="text-sm text-subtle">No problems match.</p>}
      </div>

      <div className="mt-10 flex gap-4 text-xs text-subtle">
        <span>Progress is saved in this browser.</span>
        <button onClick={doExport} className="hover:text-fg-2">
          Export
        </button>
        <button onClick={() => fileRef.current?.click()} className="hover:text-fg-2">
          Import
        </button>
        <input ref={fileRef} type="file" accept="application/json" hidden onChange={(e) => e.target.files?.[0] && doImport(e.target.files[0])} />
      </div>
    </div>
  );
}
