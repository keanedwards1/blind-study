"use client";

import { useState } from "react";
import { getRunner, type ExecResult } from "@/lib/runner";

/** Small editable Python snippet that runs in the browser worker. */
export default function Playground({ code: initial, expected }: { code: string; expected?: string }) {
  const [code, setCode] = useState(initial);
  const [result, setResult] = useState<ExecResult | null>(null);
  const [running, setRunning] = useState(false);

  async function run() {
    setRunning(true);
    try {
      setResult(await getRunner().exec(code));
    } catch (e) {
      setResult({ stdout: "", error: `Python failed to load: ${String(e)}` });
    } finally {
      setRunning(false);
    }
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      run();
    } else if (e.key === "Tab") {
      e.preventDefault();
      const el = e.currentTarget;
      const { selectionStart: s, selectionEnd: end } = el;
      const next = code.slice(0, s) + "    " + code.slice(end);
      setCode(next);
      requestAnimationFrame(() => el.setSelectionRange(s + 4, s + 4));
    }
  }

  const lines = code.split("\n").length;
  const shown = result ?? (expected !== undefined ? { stdout: expected, error: null } : null);

  return (
    <div className="overflow-hidden rounded-lg border border-line" data-testid="playground">
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        onKeyDown={onKeyDown}
        spellCheck={false}
        rows={Math.min(Math.max(lines, 3), 22)}
        className="block w-full resize-y bg-raised p-3 font-mono text-[13px] leading-6 text-fg focus:outline-none"
        aria-label="Python snippet"
      />
      <div className="flex items-center justify-between gap-2 border-t border-line bg-panel px-3 py-1.5">
        <span className="text-xs text-subtle">{result ? "Your output" : expected !== undefined ? "Output" : ""}</span>
        <div className="flex gap-3">
          {code !== initial && (
            <button
              onClick={() => {
                setCode(initial);
                setResult(null);
              }}
              className="text-xs text-subtle hover:text-fg-2"
            >
              Reset
            </button>
          )}
          <button onClick={run} disabled={running} className="rounded bg-btn px-3 py-1 text-xs font-medium text-fg hover:bg-btn-hover disabled:opacity-50">
            {running ? "Running…" : "▶ Run"}
          </button>
        </div>
      </div>
      {shown && (
        <pre className="max-h-64 overflow-auto border-t border-line bg-panel px-3 py-2 font-mono text-[13px] leading-6 text-fg-2" data-testid="playground-output">
          {shown.stdout}
          {shown.error && <span className="text-bad">{(shown.stdout ? "\n" : "") + shown.error}</span>}
          {!shown.stdout && !shown.error && <span className="text-subtle">(no output)</span>}
        </pre>
      )}
    </div>
  );
}
