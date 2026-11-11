import data from "../../data/problems.json";

type Msg = { type: string; id?: number; ok?: boolean; error?: string; result?: { ok: boolean; error: string | null } };

/**
 * Runs every reference solution (and every starter) through the real browser worker,
 * i.e. under Pyodide rather than the CPython used by `npm run problems`.
 */
describe("All reference solutions under Pyodide", () => {
  it(`accepts all ${data.problems.length} solutions and loads every starter`, () => {
    cy.visit("/");
    cy.window().then({ timeout: 180000 }, async (win) => {
      const worker = new win.Worker("/pyodide-worker.js");
      await new Promise<void>((resolve, reject) =>
        worker.addEventListener("message", (e: MessageEvent<Msg>) => {
          if (e.data.type === "ready") resolve();
          if (e.data.type === "fatal") reject(new Error(e.data.error));
        }),
      );

      let nextId = 0;
      const run = (p: (typeof data.problems)[number], code: string) =>
        new Promise<{ prepared: Msg; results: NonNullable<Msg["result"]>[] }>((resolve) => {
          const id = ++nextId;
          let prepared: Msg = { type: "" };
          const results: NonNullable<Msg["result"]>[] = [];
          const onMsg = (e: MessageEvent<Msg>) => {
            if (e.data.id !== id) return;
            if (e.data.type === "prepared") prepared = e.data;
            if (e.data.type === "result") results.push(e.data.result!);
            if (e.data.type === "done") {
              worker.removeEventListener("message", onMsg);
              resolve({ prepared, results });
            }
          };
          worker.addEventListener("message", onMsg);
          worker.postMessage({ id, code, spec: p.spec, tests: p.tests });
        });

      const problems: string[] = [];
      for (const p of data.problems) {
        const sol = await run(p, p.solution);
        const failed = sol.results.findIndex((r) => !r.ok);
        if (!sol.prepared.ok) problems.push(`${p.slug}: solution failed to load: ${sol.prepared.error}`);
        else if (sol.results.length !== p.tests.length) problems.push(`${p.slug}: ran ${sol.results.length}/${p.tests.length} tests`);
        else if (failed >= 0) problems.push(`${p.slug}: test ${failed} failed: ${sol.results[failed].error ?? "wrong answer"}`);

        const starter = await run(p, p.starter);
        if (!starter.prepared.ok) problems.push(`${p.slug}: starter failed to load: ${starter.prepared.error}`);
      }
      worker.terminate();
      expect(problems).to.deep.equal([]);
    });
  });
});
