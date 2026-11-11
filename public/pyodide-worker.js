/* Classic web worker: loads Pyodide + harness.py, runs a problem's tests one at a time.
   The main thread enforces timeouts by terminating this worker. */
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
importScripts(PYODIDE_URL + "pyodide.js");

const ready = (async () => {
  const py = await loadPyodide({ indexURL: PYODIDE_URL });
  const src = await (await fetch("/harness.py")).text();
  py.runPython(src);
  return { prepare: py.globals.get("js_prepare"), runOne: py.globals.get("js_run_one"), exec: py.globals.get("js_exec") };
})();

ready.then(
  () => postMessage({ type: "ready" }),
  (err) => postMessage({ type: "fatal", error: String(err) }),
);

onmessage = async (e) => {
  const { id, code, spec, tests, mode } = e.data;
  const h = await ready;
  if (mode === "exec") {
    postMessage({ type: "exec", id, ...JSON.parse(h.exec(code)) });
    return;
  }
  const prepared = JSON.parse(h.prepare(code, JSON.stringify(spec)));
  postMessage({ type: "prepared", id, ...prepared });
  if (prepared.ok) {
    for (let i = 0; i < tests.length; i++) {
      postMessage({ type: "start", id, index: i });
      const result = JSON.parse(h.runOne(JSON.stringify(tests[i].args), JSON.stringify(tests[i].expected)));
      postMessage({ type: "result", id, index: i, result });
    }
  }
  postMessage({ type: "done", id });
};
