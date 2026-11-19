"use client";

import { useState } from "react";
import type { CaseResult, Problem, RunOutcome } from "@/lib/types";
import { runCases } from "@/lib/edge-cases";
import { py, show } from "@/lib/format";

const chip: Record<string, string> = {
  pass: "bg-emerald-500/15 text-ok border-emerald-600/40",
  fail: "bg-rose-500/15 text-bad border-rose-600/40",
  error: "bg-rose-500/15 text-bad border-rose-600/40",
  timeout: "bg-orange-500/15 text-tle border-orange-600/40",
  skipped: "bg-raised text-subtle border-line-strong",
};

function verdict(o: RunOutcome): { label: string; color: string } {
  if (o.compileError?.startsWith("Task rule:")) return { label: "Task rule not met", color: "text-bad" };
  if (o.compileError) return { label: o.compileError.includes("Time limit") ? "Time Limit Exceeded" : "Compile / Load Error", color: "text-bad" };
  if (o.passed === o.total) return { label: o.kind === "submit" ? "Accepted" : "All examples passed", color: "text-ok" };
  if (o.cases.some((c) => c.status === "timeout")) return { label: "Time Limit Exceeded", color: "text-tle" };
  if (o.cases.some((c) => c.status === "error")) return { label: "Runtime Error", color: "text-bad" };
  return { label: "Wrong Answer", color: "text-bad" };
}

function Field({ label, children, tone }: { label: string; children: React.ReactNode; tone?: string }) {
  return (
    <div>
      <div className="mb-1 text-xs text-subtle">{label}</div>
      <pre className={`whitespace-pre-wrap break-all rounded-md bg-panel px-3 py-2 font-mono text-[13px] ${tone ?? "text-fg"}`}>{children}</pre>
    </div>
  );
}

function Inputs({ problem, args }: { problem: Problem; args: unknown[] }) {
  return (
    <Field label="Input">
      {problem.params.map((p, i) => `${p} = ${py(args[i])}`).join("\n")}
    </Field>
  );
}

export default function ResultsPanel({
  problem,
  outcome,
  running,
  progress,
}: {
  problem: Problem;
  outcome: RunOutcome | null;
  running: boolean;
  progress: CaseResult[] | null;
}) {
  const [tab, setTab] = useState<"cases" | "result">("cases");
  const [sel, setSel] = useState(0);
  const [seenOutcome, setSeenOutcome] = useState(outcome);
  const [seenRunning, setSeenRunning] = useState(running);

  // Adjust state when props change (React's "derive during render" pattern).
  if (running !== seenRunning) {
    setSeenRunning(running);
    if (running) setTab("result");
  }
  if (outcome !== seenOutcome) {
    setSeenOutcome(outcome);
    if (outcome) {
      setTab("result");
      const firstBad = outcome.cases.findIndex((c) => c.status !== "pass" && c.status !== "skipped");
      setSel(firstBad >= 0 ? firstBad : 0);
    }
  }

  const cases = runCases(problem);
  const tabBtn = (id: "cases" | "result", label: string) => (
    <button
      onClick={() => setTab(id)}
      className={`px-3 py-2 text-sm ${tab === id ? "text-fg border-b-2 border-accent" : "text-subtle hover:text-fg-2"}`}
    >
      {label}
    </button>
  );

  return (
    <div className="flex h-full flex-col">
      <div className="flex border-b border-line px-2">
        {tabBtn("cases", "Testcases")}
        {tabBtn("result", "Result")}
      </div>
      <div className="flex-1 overflow-auto p-3 space-y-3">
        {tab === "cases" && (
          <>
            <div className="flex flex-wrap gap-2">
              {cases.map((t, i) => (
                <button
                  key={i}
                  onClick={() => setSel(i)}
                  className={`rounded-md border px-2.5 py-1 text-xs ${sel === i ? "border-line-strong bg-raised text-fg" : "border-line text-muted"}`}
                >
                  {i < problem.examples.length ? `Case ${i + 1}` : t.note}
                </button>
              ))}
            </div>
            {cases[sel] && (
              <>
                {cases[sel].note && <div className="text-xs text-subtle">{sel < problem.examples.length ? `Case ${sel + 1} · ` : "Edge case · "}{cases[sel].note}</div>}
                <Inputs problem={problem} args={cases[sel].args} />
                <Field label={problem.spec.out === "stdout" ? "Expected printed output" : "Expected"}>{show(problem.spec, cases[sel].expected)}</Field>
              </>
            )}
            <p className="text-xs text-subtle">
              <b>Run</b> (⌘/Ctrl + Enter) checks the examples and the edge cases. <b>Submit</b> (⌘/Ctrl + Shift + Enter) runs all {problem.tests.length} tests,
              including {problem.tests.length - cases.length} hidden ones.
            </p>
          </>
        )}

        {tab === "result" && running && !outcome && (
          <div className="text-sm text-muted">
            Running… {progress && `${progress.filter((c) => c.status !== "skipped").length} / ${progress.length}`}
          </div>
        )}

        {tab === "result" && !running && !outcome && <div className="text-sm text-subtle">Run your code to see results.</div>}

        {tab === "result" && outcome && <OutcomeView problem={problem} outcome={outcome} sel={sel} setSel={setSel} />}
      </div>
    </div>
  );
}

function OutcomeView({ problem, outcome, sel, setSel }: { problem: Problem; outcome: RunOutcome; sel: number; setSel: (i: number) => void }) {
  const v = verdict(outcome);
  const totalMs = outcome.cases.reduce((s, c) => s + (c.ms ?? 0), 0);
  const c = outcome.cases[sel];
  const t = outcome.tests[sel];
  const hidden = outcome.kind === "submit" && sel >= problem.examples.length;

  return (
    <>
      <div className="flex items-baseline gap-3">
        <span className={`text-lg font-semibold ${v.color}`}>{v.label}</span>
        {!outcome.compileError && (
          <span className="text-sm text-muted">
            {outcome.passed} / {outcome.total} passed · {totalMs.toFixed(1)} ms
          </span>
        )}
      </div>

      {outcome.stdout && <Field label="Stdout (module level)">{outcome.stdout}</Field>}

      {outcome.compileError ? (
        <Field label="Error" tone="text-bad">{outcome.compileError}</Field>
      ) : (
        <>
          <div className="flex flex-wrap gap-1.5">
            {outcome.cases.map((cr, i) => (
              <button
                key={i}
                onClick={() => setSel(i)}
                className={`rounded-md border px-2 py-0.5 text-xs ${chip[cr.status]} ${sel === i ? "ring-1 ring-fg-2" : ""}`}
                title={outcome.tests[i]?.note ? `${cr.status} · ${outcome.tests[i].note}` : cr.status}
              >
                {i < problem.examples.length ? `Case ${i + 1}` : outcome.kind === "run" ? outcome.tests[i]?.note : `T${i - problem.examples.length + 1}`}
              </button>
            ))}
          </div>
          {c && t && (
            <div className="space-y-3">
              {(hidden || t.note) && (
                <div className="text-xs text-subtle">
                  {sel < problem.examples.length ? `Case ${sel + 1}` : t.note ? "Edge case" : `Hidden test ${sel - problem.examples.length + 1}`}
                  {t.note && ` · ${t.note}`}
                </div>
              )}
              <Inputs problem={problem} args={t.args} />
              {c.status === "skipped" ? (
                <div className="text-sm text-subtle">Not run (an earlier test timed out).</div>
              ) : (
                <>
                  {c.error ? (
                    <Field label={c.status === "timeout" ? "Timeout" : "Error"} tone="text-bad">{c.error}</Field>
                  ) : (
                    <Field label={problem.spec.out === "stdout" ? "You printed" : "Your output"} tone={c.status === "pass" ? "text-ok" : "text-bad"}>
                      {show(problem.spec, c.result)}
                    </Field>
                  )}
                  <Field label={problem.spec.out === "stdout" ? "Expected printed output" : "Expected"}>{show(problem.spec, t.expected)}</Field>
                  {problem.spec.compare === "strict" && <div className="text-xs text-subtle">This task checks the type too: a tuple isn&apos;t a list, and 3 isn&apos;t 3.0.</div>}
                  {problem.spec.checker && <div className="text-xs text-subtle">Several answers are valid here; a checker validates yours.</div>}
                  {c.stdout && <Field label="Stdout">{c.stdout}</Field>}
                </>
              )}
            </div>
          )}
        </>
      )}
    </>
  );
}
