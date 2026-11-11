"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useRef, useState } from "react";
import type { Difficulty, ProblemSummary } from "@/lib/types";
import { difficultyColor } from "@/lib/format";
import { exportAll, importAll, useAttempted, useSolved } from "@/lib/storage";
import { BoltIcon, BookIcon, CategoryIcon, categoryHue, CodeIcon, DownloadIcon, SearchIcon, ShuffleIcon, TimerIcon, UploadIcon } from "./icons";

type Status = "all" | "solved" | "unsolved";

const DIFFS: Difficulty[] = ["Easy", "Medium", "Hard"];

export const categoryId = (cat: string) => "cat-" + cat.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

function SectionHeading({ title, aside }: { title: string; aside?: React.ReactNode }) {
  return (
    <div className="mb-3 flex items-end justify-between gap-3 px-1">
      <h2 className="text-lg font-bold tracking-tight text-fg">{title}</h2>
      {aside}
    </div>
  );
}

/** Square holding a line icon. With a hue, the icon takes the colour over a faint tint of it. */
function IconBox({ children, hue, className = "h-10 w-10" }: { children: React.ReactNode; hue?: string; className?: string }) {
  const style = hue
    ? { color: hue, backgroundColor: `color-mix(in oklab, ${hue} 12%, transparent)`, borderColor: `color-mix(in oklab, ${hue} 22%, transparent)` }
    : undefined;
  return (
    <span className={`grid shrink-0 place-items-center rounded-lg border border-line bg-raised text-muted ${className}`} style={style}>
      {children}
    </span>
  );
}

const diffBar: Record<string, string> = { Easy: "bg-ok", Medium: "bg-warn", Hard: "bg-bad" };

function ProgressRing({ value, total }: { value: number; total: number }) {
  const r = 42;
  const c = 2 * Math.PI * r;
  const pct = total ? value / total : 0;
  return (
    <div className="relative h-24 w-24 shrink-0">
      <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90" aria-hidden="true">
        <circle cx="50" cy="50" r={r} fill="none" strokeWidth="8" className="stroke-line" />
        <circle
          cx="50"
          cy="50"
          r={r}
          fill="none"
          strokeWidth="8"
          strokeLinecap="round"
          className="stroke-ok transition-[stroke-dashoffset] duration-700"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - pct)}
        />
      </svg>
      <div className="absolute inset-0 grid place-items-center font-mono text-xl font-semibold tabular-nums text-fg">{Math.round(pct * 100)}%</div>
    </div>
  );
}

const tile = "flex h-14 min-w-0 items-center gap-3 rounded-lg border border-line bg-panel px-2 text-left text-sm transition-colors hover:border-line-strong hover:bg-hover";

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

  // Most recently touched problems first (solved or attempted).
  const recent = useMemo(
    () =>
      problems
        .map((p) => ({ p, at: Math.max(solved[p.slug] ?? 0, attempted[p.slug] ?? 0) }))
        .filter((x) => x.at > 0)
        .sort((a, b) => b.at - a.at)
        .slice(0, 8)
        .map((x) => x.p),
    [problems, solved, attempted],
  );
  const lastUnsolved = recent.find((p) => !solved[p.slug]);

  const total = problems.length;
  const solvedCount = problems.filter((p) => solved[p.slug]).length;
  const diffStats = DIFFS.map((d) => {
    const all = problems.filter((p) => p.difficulty === d);
    return { d, done: all.filter((p) => solved[p.slug]).length, total: all.length };
  });
  const catStats = (cat: string) => {
    const all = problems.filter((p) => p.category === cat);
    return { done: all.filter((p) => solved[p.slug]).length, total: all.length };
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

  const pillSelect =
    "h-10 cursor-pointer rounded-full border border-line bg-panel px-4 text-sm font-medium text-fg-2 hover:border-line-strong focus:border-fg-2 focus:outline-none";

  return (
    <div className="mx-auto w-full max-w-7xl space-y-10 px-3 pb-16 pt-3 sm:px-5 sm:pt-5">
      {/* ------------------------------------------------ summary */}
      <section className="relative flex flex-wrap items-center gap-8 overflow-hidden rounded-2xl border border-line bg-panel p-6 sm:p-8">
        {/* Background image: a tilted wall of category tiles, faded out toward the text. */}
        <div
          className="pointer-events-none absolute -right-10 -top-28 hidden rotate-12 grid-cols-6 gap-3 opacity-80 [mask-image:linear-gradient(to_left,black_45%,transparent_95%)] lg:grid"
          aria-hidden="true"
        >
          {[...categories, ...categories].slice(0, 30).map((c, i) => (
            <IconBox key={i} hue={categoryHue(c)} className="h-20 w-20 rounded-2xl">
              <CategoryIcon category={c} className="h-9 w-9" />
            </IconBox>
          ))}
        </div>

        <div className="relative min-w-0 flex-1 basis-80">
          <h1 className="text-3xl font-bold tracking-tight text-fg sm:text-4xl">Problems</h1>
          <p className="mt-2 text-[15px] leading-7 text-muted">
            {total} problems in {categories.length} categories. Solutions are written in Python and run in the browser.
          </p>
          <div className="mt-5 flex flex-wrap items-center gap-3">
            <button onClick={pickRandom} className="flex h-11 items-center gap-2 rounded-full bg-fg px-5 text-sm font-semibold text-page transition-opacity hover:opacity-85">
              <ShuffleIcon className="h-4.5 w-4.5" />
              Random unsolved
            </button>
            <Link href="/mock" className="flex h-11 items-center gap-2 rounded-full border border-line-strong px-5 text-sm font-semibold text-fg transition-colors hover:bg-hover">
              <TimerIcon className="h-4.5 w-4.5" />
              Start mock assessment
            </Link>
          </div>
        </div>

        <div className="relative flex w-full flex-wrap items-center gap-6 rounded-xl border border-line bg-panel/70 p-5 backdrop-blur-md sm:w-auto">
          <ProgressRing value={solvedCount} total={total} />
          <div className="min-w-44 space-y-3">
            <p className="text-sm font-semibold text-fg">
              {solvedCount} / {total} solved
            </p>
            {diffStats.map(({ d, done, total: t }) => (
              <div key={d}>
                <div className="mb-1 flex justify-between text-xs">
                  <span className={`font-medium ${difficultyColor[d]}`}>{d}</span>
                  <span className="font-mono tabular-nums text-subtle">
                    {done}/{t}
                  </span>
                </div>
                <div className="h-1.5 overflow-hidden rounded-full bg-line">
                  <div className={`h-full rounded-full ${diffBar[d]}`} style={{ width: `${t ? (done / t) * 100 : 0}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ------------------------------------------------ sections of the site */}
      <section className="grid grid-cols-2 gap-2 sm:gap-2.5 lg:grid-cols-4">
        {lastUnsolved ? (
          <button onClick={() => router.push(`/problems/${lastUnsolved.slug}`)} className={tile}>
            <IconBox hue={categoryHue(lastUnsolved.category)}>
              <CategoryIcon category={lastUnsolved.category} className="h-5 w-5" />
            </IconBox>
            <span className="min-w-0 leading-tight">
              <span className="block truncate text-[11px] text-subtle">Last attempted</span>
              <span className="block truncate font-semibold text-fg">{lastUnsolved.title}</span>
            </span>
          </button>
        ) : (
          <Link href="/quiz#crash-course" className={tile}>
            <IconBox hue="#1F9E89">
              <CodeIcon className="h-5 w-5" />
            </IconBox>
            <span className="truncate font-semibold text-fg">Python crash course</span>
          </Link>
        )}
        <Link href="/learn" className={tile}>
          <IconBox hue="#8D63D2">
            <BookIcon className="h-5 w-5" />
          </IconBox>
          <span className="truncate font-semibold text-fg">Learn</span>
        </Link>
        <Link href="/quiz" className={tile}>
          <IconBox hue="#D9912B">
            <BoltIcon className="h-5 w-5" />
          </IconBox>
          <span className="truncate font-semibold text-fg">Quiz</span>
        </Link>
        <Link href="/mock" className={tile}>
          <IconBox hue="#4A78D6">
            <TimerIcon className="h-5 w-5" />
          </IconBox>
          <span className="truncate font-semibold text-fg">Mock assessment</span>
        </Link>
      </section>

      {/* ------------------------------------------------ recent */}
      {recent.length > 0 && (
        <section>
          <SectionHeading title="Recent" />
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-4">
            {recent.map((p) => (
              <button key={p.slug} onClick={() => router.push(`/problems/${p.slug}`)} className={`${tile} h-16`}>
                <IconBox hue={categoryHue(p.category)}>
                  <CategoryIcon category={p.category} className="h-5 w-5" />
                </IconBox>
                <span className="min-w-0 flex-1 leading-tight">
                  <span className="block truncate font-semibold text-fg">{p.title}</span>
                  <span className="mt-0.5 block truncate text-xs text-subtle">
                    {p.difficulty} · {solved[p.slug] ? "Solved" : "Attempted"}
                  </span>
                </span>
              </button>
            ))}
          </div>
        </section>
      )}

      {/* ------------------------------------------------ all problems */}
      <section>
        <SectionHeading title="All problems" aside={<span className="mb-0.5 text-xs text-subtle">{filtered.length} shown</span>} />

        <div className="sticky top-0 z-10 -mx-3 mb-4 flex flex-wrap gap-2 bg-page/90 px-3 py-3 backdrop-blur-md sm:-mx-5 sm:px-5">
          <label className="relative min-w-0 flex-1 basis-56">
            <SearchIcon className="pointer-events-none absolute left-3.5 top-1/2 h-4.5 w-4.5 -translate-y-1/2 text-subtle" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search problems"
              className="h-10 w-full rounded-full border border-line bg-panel pl-10 pr-4 text-sm text-fg placeholder:text-subtle hover:border-line-strong focus:border-fg-2 focus:outline-none"
            />
          </label>
          <select value={diff} onChange={(e) => setDiff(e.target.value)} className={pillSelect} aria-label="Difficulty">
            <option value="all">All difficulties</option>
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
          <select value={status} onChange={(e) => setStatus(e.target.value as Status)} className={pillSelect} aria-label="Status">
            <option value="all">All</option>
            <option value="unsolved">Unsolved</option>
            <option value="solved">Solved</option>
          </select>
        </div>

        <div className="gap-4 lg:columns-2">
          {categories.map((cat) => {
            const items = filtered.filter((p) => p.category === cat);
            if (!items.length) return null;
            const { done, total: t } = catStats(cat);
            return (
              <section key={cat} id={categoryId(cat)} className="mb-4 scroll-mt-20 break-inside-avoid rounded-2xl border border-line bg-panel p-3 sm:p-4">
                <div className="mb-2 flex items-center gap-3 px-1">
                  <IconBox hue={categoryHue(cat)}>
                    <CategoryIcon category={cat} className="h-5 w-5" />
                  </IconBox>
                  <h2 className="min-w-0 flex-1 truncate text-base font-bold tracking-tight text-fg">{cat}</h2>
                  <span className="font-mono text-xs tabular-nums text-subtle">
                    {done}/{t}
                  </span>
                </div>
                <div className="mx-1 mb-2 h-0.5 overflow-hidden rounded-full bg-line">
                  <div className="h-full rounded-full transition-[width] duration-500" style={{ width: `${(done / t) * 100}%`, backgroundColor: categoryHue(cat) }} />
                </div>
                <ul>
                  {items.map((p) => (
                    <li key={p.slug}>
                      <Link href={`/problems/${p.slug}`} className="group flex items-center gap-3 rounded-lg px-2 py-2 transition-colors hover:bg-hover">
                        <span className="w-6 shrink-0 text-center font-mono text-xs tabular-nums text-subtle">{problems.indexOf(p) + 1}</span>
                        <span className="min-w-0 flex-1 truncate text-sm font-medium text-fg-2 group-hover:text-fg">{p.title}</span>
                        <span className={`text-xs font-medium ${difficultyColor[p.difficulty]}`}>{p.difficulty}</span>
                        <span className="grid w-5 shrink-0 place-items-center">
                          {solved[p.slug] ? (
                            <span className="text-sm font-bold text-ok" title="Solved">
                              ✓
                            </span>
                          ) : attempted[p.slug] ? (
                            <span className="h-1.5 w-1.5 rounded-full bg-warn" title="Attempted" />
                          ) : null}
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </section>
            );
          })}
        </div>
        {!filtered.length && (
          <div className="rounded-2xl border border-dashed border-line-strong p-10 text-center">
            <p className="text-sm text-subtle">No problems match.</p>
          </div>
        )}
      </section>

      <footer className="flex flex-wrap items-center gap-2 border-t border-line pt-6 text-xs text-subtle">
        <span className="mr-2">Progress is saved in this browser.</span>
        <button onClick={doExport} className="flex items-center gap-1.5 rounded-full border border-line px-3 py-1.5 font-medium hover:border-line-strong hover:text-fg-2">
          <DownloadIcon className="h-3.5 w-3.5" />
          Export
        </button>
        <button onClick={() => fileRef.current?.click()} className="flex items-center gap-1.5 rounded-full border border-line px-3 py-1.5 font-medium hover:border-line-strong hover:text-fg-2">
          <UploadIcon className="h-3.5 w-3.5" />
          Import
        </button>
        <input ref={fileRef} type="file" accept="application/json" hidden onChange={(e) => e.target.files?.[0] && doImport(e.target.files[0])} />
      </footer>
    </div>
  );
}
