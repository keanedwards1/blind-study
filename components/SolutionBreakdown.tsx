"use client";

import { useState } from "react";
import type { Concept } from "@/lib/types";
import { ConceptDetail, shortTitle } from "./LearnTab";

/** Reference solution with each line tagged by the Python concepts it uses. */
export default function SolutionBreakdown({ code, lineTags, concepts }: { code: string; lineTags: Record<string, string[]>; concepts: Record<string, Concept> }) {
  const [open, setOpen] = useState<string | null>(null);
  const lines = code.replace(/\n$/, "").split("\n");
  const openConcept = open ? concepts[open] : undefined;

  return (
    <div className="space-y-3">
      <div className="overflow-x-auto rounded-lg border border-line bg-raised py-2 font-mono text-[13px] leading-6" data-testid="solution-breakdown">
        {lines.map((line, i) => {
          const tags = lineTags[String(i + 1)] ?? [];
          const indent = line.length - line.trimStart().length;
          return (
            <div key={i} className={`flex px-2 ${tags.includes(open ?? "") ? "bg-accent/15" : ""}`}>
              <span className="w-7 shrink-0 select-none pr-3 text-right text-subtle">{i + 1}</span>
              <div className="min-w-0">
                <div className="whitespace-pre text-fg">{line || " "}</div>
                {tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 pb-1 font-sans" style={{ paddingLeft: `${indent}ch` }}>
                    {tags.map((t) => (
                      <button
                        key={t}
                        onClick={() => setOpen(open === t ? null : t)}
                        className={`rounded-full border px-1.5 text-[11px] leading-5 ${open === t ? "border-accent bg-accent/20 text-fg" : "border-line-strong text-muted hover:text-fg"}`}
                      >
                        {concepts[t] ? shortTitle(concepts[t]) : t}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
      <p className="text-xs text-subtle">Tags mark the Python features each line uses. Click one to see what it does.</p>
      {openConcept && <ConceptDetail concept={openConcept} onClose={() => setOpen(null)} />}
    </div>
  );
}
