"use client";

import { useEffect, useState } from "react";
import type { CaseResult, Problem, RunOutcome } from "@/lib/types";
import { getRunner, useRunnerStatus } from "@/lib/runner";
import CodeEditor from "./CodeEditor";
import ResultsPanel from "./ResultsPanel";

export function RunnerBadge() {
  const status = useRunnerStatus();
  const text: Record<string, string> = {
    idle: "Python idle",
    loading: "Loading Python…",
    ready: "Python ready",
    running: "Running…",
    error: "Python failed to load",
  };
  const dot: Record<string, string> = {
    idle: "bg-zinc-500",
    loading: "bg-amber-400 animate-pulse",
    ready: "bg-emerald-400",
    running: "bg-sky-400 animate-pulse",
    error: "bg-rose-500",
  };
  return (
    <span className="flex items-center gap-1.5 text-xs text-muted" title={status === "error" ? getRunner().fatal ?? "" : ""}>
      <span className={`h-2 w-2 rounded-full ${dot[status]}`} />
      {text[status]}
    </span>
  );
}

export default function CodePane({
  problem,
  code,
  onCodeChange,
  onRan,
  onSubmitted,
  onReset,
  submitLabel = "Submit",
  confirmSubmit,
}: {
  problem: Problem;
  code: string;
  onCodeChange: (v: string) => void;
  onRan?: (o: RunOutcome) => void;
  onSubmitted?: (o: RunOutcome) => void;
  onReset?: () => void;
  submitLabel?: string;
  confirmSubmit?: string;
}) {
  const [outcome, setOutcome] = useState<RunOutcome | null>(null);
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState<CaseResult[] | null>(null);
  const status = useRunnerStatus();

  useEffect(() => getRunner().warm(), []);

  async function exec(kind: "run" | "submit") {
    if (running) return;
    if (kind === "submit" && confirmSubmit && !window.confirm(confirmSubmit)) return;
    setRunning(true);
    setOutcome(null);
    setProgress(null);
    try {
      const o = await getRunner().run(problem, code, kind, setProgress);
      setOutcome(o);
      onRan?.(o);
      if (kind === "submit") onSubmitted?.(o);
    } catch (e) {
      setOutcome({ kind, compileError: `Python runtime failed to load: ${String(e)}. Check your connection and try again.`, cases: [], tests: [], passed: 0, total: 0 });
    } finally {
      setRunning(false);
    }
  }

  const busy = running || status === "loading";

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="flex items-center justify-between border-b border-line bg-panel px-3 py-1.5">
        <span className="text-xs font-medium text-muted">Python 3</span>
        <div className="flex items-center gap-3">
          <RunnerBadge />
          {onReset && (
            <button
              onClick={() => window.confirm("Reset to the starter code? Your current code will be lost.") && onReset()}
              className="text-xs text-subtle hover:text-fg-2"
            >
              Reset
            </button>
          )}
        </div>
      </div>
      <div className="min-h-[240px] flex-[3]">
        <CodeEditor value={code} onChange={onCodeChange} onRun={() => exec("run")} onSubmit={() => exec("submit")} />
      </div>
      <div className="flex items-center justify-end gap-2 border-y border-line bg-panel px-3 py-2">
        <button
          onClick={() => exec("run")}
          disabled={busy}
          className="rounded-md bg-btn px-4 py-1.5 text-sm font-medium text-fg hover:bg-btn-hover disabled:opacity-50"
        >
          Run
        </button>
        <button
          onClick={() => exec("submit")}
          disabled={busy}
          className="rounded-md bg-emerald-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-emerald-500 disabled:opacity-50"
        >
          {submitLabel}
        </button>
      </div>
      <div className="min-h-[200px] flex-[2] overflow-hidden">
        <ResultsPanel problem={problem} outcome={outcome} running={running} progress={progress} />
      </div>
    </div>
  );
}
