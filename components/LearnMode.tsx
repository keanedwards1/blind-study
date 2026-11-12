"use client";

import type { GrammarSection } from "@/lib/types";
import Markdown from "./Markdown";

/** Content of the workspace's "Learn mode" tab: the Python syntax pieces for this problem. */
export default function LearnMode({ sections }: { sections: GrammarSection[] }) {
  return (
    <section className="space-y-3" data-testid="learn-mode">
      <div>
        <h2 className="text-base font-semibold text-fg">Python building blocks</h2>
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
