import type { Problem } from "@/lib/types";
import { difficultyColor, py, show } from "@/lib/format";
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
        <span className="text-subtle">{problem.spec.out === "stdout" ? "Prints: " : "Output: "}</span>
        {problem.spec.out === "stdout" ? <pre className="inline whitespace-pre-wrap">{show(problem.spec, ex.expected)}</pre> : show(problem.spec, ex.expected)}
      </div>
    </div>
  );
}

/** Labels for require/forbid rules, mirroring rule_label() in public/harness.py. */
const RULE_LABELS: Record<string, string> = {
  listcomp: "a list comprehension", dictcomp: "a dict comprehension", setcomp: "a set comprehension", genexp: "a generator expression",
  comprehension: "a comprehension", lambda: "lambda", yield: "yield", with: "a with block", try: "try / except", raise: "raise",
  while: "a while loop", for: "a for loop", if: "an if statement", class: "a class", fstring: "an f-string", walrus: ":=",
  slicing: "slicing", ternary: "x if cond else y", nonlocal: "nonlocal", global: "global", assert: "assert", del: "del",
  import: "an import", augassign: "+= style assignment", unpack: "* unpacking", match: "a match statement", recursion: "recursion", decorator: "a decorator",
};

function ruleLabel(rule: string): string {
  if (RULE_LABELS[rule]) return RULE_LABELS[rule];
  if (rule.startsWith("op:")) return rule.slice(3);
  if (rule.startsWith(".")) return `${rule}()`;
  return rule;
}

export function TaskRules({ problem }: { problem: Problem }) {
  const { require = [], forbid = [], out, compare } = problem.spec;
  if (!require.length && !forbid.length && out !== "stdout" && compare !== "strict") return null;
  return (
    <div className="space-y-1.5 rounded-lg border border-line bg-panel p-3 text-sm" data-testid="task-rules">
      {require.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-subtle">Must use:</span>
          {require.map((r) => (
            <code key={r} className="rounded bg-ok/15 px-1.5 py-0.5 text-xs text-ok">{ruleLabel(r)}</code>
          ))}
        </div>
      )}
      {forbid.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-subtle">Don&apos;t use:</span>
          {forbid.map((r) => (
            <code key={r} className="rounded bg-bad/15 px-1.5 py-0.5 text-xs text-bad">{ruleLabel(r)}</code>
          ))}
        </div>
      )}
      {out === "stdout" && <div className="text-muted">The tests check exactly what your function <b className="text-fg-2">prints</b>, including spaces and new lines.</div>}
      {compare === "strict" && <div className="text-muted">The tests check the <b className="text-fg-2">type</b> as well as the value (for example, <code>3.0</code> is not <code>3</code>).</div>}
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
      <TaskRules problem={problem} />
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
