"use client";

import { useSyncExternalStore } from "react";
import type { CaseResult, Problem, RunOutcome, TestCase } from "./types";

export type RunnerStatus = "idle" | "loading" | "ready" | "running" | "error";

const TEST_TIMEOUT_MS = 6000;

type WorkerMsg =
  | { type: "ready" }
  | { type: "fatal"; error: string }
  | { type: "prepared"; id: number; ok: boolean; error?: string; stdout?: string }
  | { type: "start"; id: number; index: number }
  | { type: "result"; id: number; index: number; result: { ok: boolean; result: unknown; error: string | null; stdout: string; ms: number } }
  | { type: "done"; id: number }
  | { type: "exec"; id: number; stdout: string; error: string | null };

class PyRunner {
  private worker: Worker | null = null;
  private ready: Promise<void> | null = null;
  private status: RunnerStatus = "idle";
  private listeners = new Set<() => void>();
  private nextId = 1;
  fatal: string | null = null;

  getStatus = () => this.status;
  subscribe = (cb: () => void) => {
    this.listeners.add(cb);
    return () => this.listeners.delete(cb);
  };
  private setStatus(s: RunnerStatus) {
    this.status = s;
    this.listeners.forEach((l) => l());
  }

  /** Start loading Pyodide in the background (idempotent). */
  warm() {
    if (!this.worker) this.spawn();
  }

  private spawn() {
    this.setStatus("loading");
    const worker = new Worker("/pyodide-worker.js");
    this.worker = worker;
    this.ready = new Promise<void>((resolve, reject) => {
      const onMsg = (e: MessageEvent<WorkerMsg>) => {
        if (e.data.type === "ready") {
          worker.removeEventListener("message", onMsg);
          this.setStatus("ready");
          resolve();
        } else if (e.data.type === "fatal") {
          this.fatal = e.data.error;
          this.setStatus("error");
          reject(new Error(e.data.error));
        }
      };
      worker.addEventListener("message", onMsg);
      worker.addEventListener("error", (ev) => {
        this.fatal = ev.message || "Failed to start the Python worker";
        this.setStatus("error");
        reject(new Error(this.fatal));
      });
    });
    this.ready.catch(() => {});
  }

  private restart() {
    this.worker?.terminate();
    this.worker = null;
    this.spawn();
  }

  /** Run a free-form snippet (playgrounds). */
  async exec(code: string): Promise<ExecResult> {
    if (!this.worker || this.status === "error") this.restart();
    await this.ready;
    const worker = this.worker!;
    const id = this.nextId++;
    this.setStatus("running");
    return new Promise<ExecResult>((resolve) => {
      const timer = setTimeout(() => {
        worker.removeEventListener("message", onMsg);
        this.restart();
        resolve({ stdout: "", error: `Time limit exceeded (> ${TEST_TIMEOUT_MS / 1000}s). Infinite loop?` });
      }, TEST_TIMEOUT_MS);
      const onMsg = (e: MessageEvent<WorkerMsg>) => {
        const m = e.data;
        if (m.type !== "exec" || m.id !== id) return;
        clearTimeout(timer);
        worker.removeEventListener("message", onMsg);
        if (this.worker === worker) this.setStatus("ready");
        resolve({ stdout: m.stdout, error: m.error });
      };
      worker.addEventListener("message", onMsg);
      worker.postMessage({ id, code, mode: "exec" });
    });
  }

  async run(
    problem: Problem,
    code: string,
    kind: "run" | "submit",
    onProgress?: (cases: CaseResult[]) => void,
  ): Promise<RunOutcome> {
    if (!this.worker || this.status === "error") this.restart();
    await this.ready;
    const worker = this.worker!;
    const tests: TestCase[] = kind === "run" ? problem.examples : problem.tests;
    const id = this.nextId++;
    const cases: CaseResult[] = tests.map(() => ({ status: "skipped" }));
    this.setStatus("running");

    return new Promise<RunOutcome>((resolve) => {
      let timer: ReturnType<typeof setTimeout> | undefined;
      let current = -1;
      let compileError: string | undefined;
      let stdout = "";

      const finish = () => {
        clearTimeout(timer);
        worker.removeEventListener("message", onMsg);
        if (this.worker === worker) this.setStatus("ready");
        const passed = cases.filter((c) => c.status === "pass").length;
        resolve({ kind, compileError, stdout, cases, tests, passed, total: tests.length });
      };
      const arm = () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
          if (current >= 0) cases[current] = { status: "timeout", error: `Time limit exceeded (> ${TEST_TIMEOUT_MS / 1000}s). Infinite loop, or too slow?` };
          else compileError = `Time limit exceeded while loading your code (> ${TEST_TIMEOUT_MS / 1000}s).`;
          worker.removeEventListener("message", onMsg);
          this.restart();
          const passed = cases.filter((c) => c.status === "pass").length;
          resolve({ kind, compileError, stdout, cases, tests, passed, total: tests.length });
        }, TEST_TIMEOUT_MS);
      };

      const onMsg = (e: MessageEvent<WorkerMsg>) => {
        const m = e.data;
        if (!("id" in m) || m.id !== id) return;
        if (m.type === "prepared") {
          clearTimeout(timer);
          stdout = m.stdout ?? "";
          if (!m.ok) compileError = m.error;
        } else if (m.type === "start") {
          current = m.index;
          arm();
        } else if (m.type === "result") {
          clearTimeout(timer);
          const r = m.result;
          cases[m.index] = { status: r.error ? "error" : r.ok ? "pass" : "fail", result: r.result, error: r.error, stdout: r.stdout, ms: r.ms };
          current = -1;
          onProgress?.([...cases]);
        } else if (m.type === "done") {
          finish();
        }
      };

      worker.addEventListener("message", onMsg);
      arm();
      worker.postMessage({ id, code, spec: problem.spec, tests });
    });
  }
}

export type ExecResult = { stdout: string; error: string | null };

let instance: PyRunner | null = null;
export function getRunner(): PyRunner {
  if (!instance) instance = new PyRunner();
  return instance;
}

export function useRunnerStatus(): RunnerStatus {
  const r = getRunner();
  return useSyncExternalStore(r.subscribe, r.getStatus, () => "idle");
}
