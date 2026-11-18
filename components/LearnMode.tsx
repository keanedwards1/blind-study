"use client";

import { useMemo, useState } from "react";
import type { GrammarSection } from "@/lib/types";
import { save, useStored } from "@/lib/storage";
import Markdown from "./Markdown";

const KEY = "learnMode";

/** Learn mode is a single on/off preference that carries across every problem. */
export function useLearnMode(): boolean {
  return useStored<boolean>(KEY, false);
}

function LearnModeToggle() {
  const on = useLearnMode();
  return (
    <button
      role="switch"
      aria-checked={on}
      onClick={() => save(KEY, !on)}
      className="flex shrink-0 items-center gap-2 rounded-md px-1 py-0.5 text-sm text-muted hover:text-fg"
    >
      <span className={`relative h-5 w-9 shrink-0 rounded-full transition-colors ${on ? "bg-accent" : "bg-line-strong"}`}>
        <span className={`absolute top-0.5 left-0.5 h-4 w-4 rounded-full bg-white shadow transition-transform ${on ? "translate-x-4" : ""}`} />
      </span>
      {on ? "On" : "Off"}
    </button>
  );
}

/** A seeded shuffle (mulberry32 + Fisher-Yates), so one opening of the tab keeps a stable order across re-renders. */
function shuffled<T>(items: T[], seed: number): T[] {
  let s = seed >>> 0;
  const rand = () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let x = s;
    x = Math.imul(x ^ (x >>> 15), x | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

/**
 * Content of the workspace's "Learn mode" tab: an on/off switch, and when on, the Python syntax pieces for this problem.
 * The pieces within each section are shuffled every time the tab opens, so their order never spells out a solution.
 * (Learn mode renders off on the server, so the shuffled list only ever appears client-side and can't mismatch hydration.)
 */
export default function LearnMode({ sections }: { sections: GrammarSection[] }) {
  const on = useLearnMode();
  const [seed] = useState(() => Math.floor(Math.random() * 2 ** 31));
  const mixed = useMemo(() => sections.map((s, i) => ({ ...s, items: shuffled(s.items, seed + i * 7919) })), [sections, seed]);
  return (
    <section className="space-y-3">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-base font-semibold text-fg">Python building blocks</h2>
          <p className="mt-1 text-xs text-subtle">
            The Python pieces you could use, in no particular order. Working out how they fit together is the exercise. Everything from collections, heapq, bisect, functools and math
            is already imported.
          </p>
        </div>
        <LearnModeToggle />
      </div>
      {on ? (
        <div className="space-y-3" data-testid="learn-mode">
          {mixed.map((s) => (
            <div key={s.title}>
              <h3 className="mb-1 text-sm font-semibold text-fg">{s.title}</h3>
              <Markdown>{s.items.map((i) => `- ${i}`).join("\n")}</Markdown>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-muted">Learn mode is off. Turn it on to see the building blocks for this problem. The setting applies to every problem.</p>
      )}
    </section>
  );
}
