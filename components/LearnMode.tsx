"use client";

import type { GrammarSection } from "@/lib/types";
import { save, useStored } from "@/lib/storage";
import Markdown from "./Markdown";

const KEY = "learnMode";

/** Learn mode is a single on/off preference that carries across every problem. */
export function useLearnMode(): boolean {
  return useStored<boolean>(KEY, false);
}

export function LearnModeToggle({ onEnable }: { onEnable?: () => void }) {
  const on = useLearnMode();
  return (
    <button
      role="switch"
      aria-checked={on}
      onClick={() => {
        save(KEY, !on);
        if (!on) onEnable?.();
      }}
      title="Show the Python building blocks you could use to write the answer"
      className="flex items-center gap-2 rounded-full px-1 py-0.5 text-sm text-muted hover:text-fg"
    >
      <span className={`relative h-5 w-9 shrink-0 rounded-full transition-colors ${on ? "bg-accent" : "bg-line-strong"}`}>
        <span className={`absolute top-0.5 left-0.5 h-4 w-4 rounded-full bg-white shadow transition-transform ${on ? "translate-x-4" : ""}`} />
      </span>
      Learn mode
    </button>
  );
}

export default function LearnMode({ sections }: { sections: GrammarSection[] }) {
  return (
    <section className="space-y-3 rounded-lg border border-accent/40 bg-panel p-4" data-testid="learn-mode">
      <div>
        <h2 className="text-base font-semibold text-fg">Learn mode: Python building blocks</h2>
        <p className="mt-1 text-xs text-subtle">
          The Python syntax you could use to write an answer. You choose how to put it together. Everything from collections, heapq, bisect, functools and math
          is already imported.
        </p>
      </div>
      {sections.map((s) => (
        <div key={s.title}>
          <h3 className="mb-1 text-sm font-semibold text-fg">{s.title}</h3>
          <Markdown>{s.items.map((i) => `- ${i}`).join("\n")}</Markdown>
        </div>
      ))}
    </section>
  );
}
