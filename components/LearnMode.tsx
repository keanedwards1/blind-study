"use client";

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
      className="flex shrink-0 items-center gap-2 rounded-full px-1 py-0.5 text-sm text-muted hover:text-fg"
    >
      <span className={`relative h-5 w-9 shrink-0 rounded-full transition-colors ${on ? "bg-accent" : "bg-line-strong"}`}>
        <span className={`absolute top-0.5 left-0.5 h-4 w-4 rounded-full bg-white shadow transition-transform ${on ? "translate-x-4" : ""}`} />
      </span>
      {on ? "On" : "Off"}
    </button>
  );
}

/** Content of the workspace's "Learn mode" tab: an on/off switch, and when on, the Python syntax pieces for this problem. */
export default function LearnMode({ sections }: { sections: GrammarSection[] }) {
  const on = useLearnMode();
  return (
    <section className="space-y-3">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-base font-semibold text-fg">Python building blocks</h2>
          <p className="mt-1 text-xs text-subtle">
            The Python syntax you could use to write an answer. You choose how to put it together. Everything from collections, heapq, bisect, functools and math
            is already imported.
          </p>
        </div>
        <LearnModeToggle />
      </div>
      {on ? (
        <div className="space-y-3" data-testid="learn-mode">
          {sections.map((s) => (
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
