import type { Problem } from "@/lib/types";
import { difficultyColor, py } from "@/lib/format";
import Markdown from "./Markdown";

export function ExampleBlock({ problem, index }: { problem: Problem; index: number }) {
  const ex = problem.examples[index];
  return (
    <div className="rounded-lg border border-line bg-panel p-3 font-mono text-[13px] leading-6">
      <div>
        <span className="text-subtle">Input: </span>
        {problem.params.map((p, i) => (
          <span key={p}>
            {i > 0 && ", "}
            {p} = {py(ex.args[i])}
          </span>
        ))}
      </div>
      <div>
        <span className="text-subtle">Output: </span>
        {py(ex.expected)}
      </div>
    </div>
  );
}

export default function ProblemDescription({ problem }: { problem: Problem }) {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-xl font-semibold text-fg">{problem.title}</h1>
        <div className="mt-1 flex items-center gap-3 text-sm">
          <span className={difficultyColor[problem.difficulty]}>{problem.difficulty}</span>
          <span className="text-subtle">{problem.category}</span>
        </div>
      </div>
      <Markdown>{problem.desc}</Markdown>
      <div className="space-y-3">
        {problem.examples.map((_, i) => (
          <div key={i}>
            <div className="mb-1 text-sm font-medium text-fg-2">Example {i + 1}</div>
            <ExampleBlock problem={problem} index={i} />
          </div>
        ))}
      </div>
    </div>
  );
}
