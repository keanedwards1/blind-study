# drill

A personal coding-interview practice site: 75 classic problems in Python. Code runs in the browser
(Pyodide in a Web Worker), so there is no backend and nothing to configure on Vercel.

- **Problems** (`/`): grouped by pattern, with solved/attempted tracking, search, and filters.
- **Problem page**: Monaco editor, **Run** (examples, ⌘/Ctrl+Enter) and **Submit** (all hidden tests, ⌘/Ctrl+Shift+Enter),
  per-test diffs, captured `print` output, a 6-second time limit per test, hints, and a reveal-on-demand solution with explanation.
- **Mock assessment** (`/mock`): timed session, problems in order (Easy → Medium → Hard), code locks on submit, then a
  webcam explanation step with its own time cap. The global clock keeps running while you record.
  Recordings stay in memory in the tab and are never uploaded.
- **Learn** (`/learn`): a guide for each of the 18 patterns (when to use it, template, complexity, pitfalls, quiz) and a
  **Python toolkit** of 26 concepts (dict, heapq, deque, slicing, closures/`nonlocal`, bit ops…). Each concept has a
  snippet you can edit and run, gotchas, the problems that use it, and a mini-quiz.
- **Learn tab on each problem**: the pattern and the Python building blocks its solution uses, plus a self-quiz (key insight,
  time and space complexity, pattern). The **Solution** tab tags every line of the reference solution with the concepts it uses.
- **Quiz drill** (`/quiz`): mixed rounds from all question banks, each shown with its problem or concept as context. It tracks
  your answers and keeps a "review missed" pile.
- **Light mode** by default, with a dark-mode toggle in the header.

Progress (solved problems, your code, quiz answers, mock history) lives in `localStorage` in your browser. Use Export/Import
at the bottom of the problem list to move it between browsers.

## Develop

```bash
npm install
npm run dev            # http://localhost:3000
npm run problems       # validate content/ and regenerate data/problems.json + data/learn.json
npm run build
```

## Tests (Cypress)

```bash
npm run test:e2e:dev   # against your running `npm run dev` on :3000 (catches dev-only React/Next errors)
npm run test:e2e       # builds, starts a production server on :3100, runs everything
npm run cy:open        # interactive runner
npm test               # content validation + production e2e
```

Specs live in `cypress/e2e/`. Every test also fails if the page logs a `console.error`, which catches hydration
mismatches and Next.js dev warnings. `solutions.cy.ts` runs all 75 reference solutions through the in-browser Python.
If Cypress fails with `bad option: --smoke-test`, your shell has `ELECTRON_RUN_AS_NODE` set
(VS Code's extension host does this); run `unset ELECTRON_RUN_AS_NODE` first.

## Deploy

`npx vercel` (or push to GitHub and import the repo in Vercel). Default settings work.
`data/problems.json` is committed, so the Vercel build doesn't need Python.

## Adding or editing problems

Problems are authored in `content/NN_category.py` as plain Python dicts:

```python
dict(
    slug="two-sum",
    title="Two Sum",
    difficulty="Easy",
    sig="def two_sum(nums: List[int], target: int) -> List[int]:",  # starter + param names come from this
    compare="unordered",          # exact (default) | unordered | unordered_nested
    desc="""Markdown statement...""",
    hints=["..."],
    solution="""def two_sum(...): ...""",
    explanation="""Markdown: approach + complexity""",
    examples=[([[2, 7, 11, 15], 9], [0, 1])],   # (args, expected), shown to the user and used by Run
    tests=[[[3, 3], 6]],                         # args only; expected comes from the reference solution
)
```

Other options: `in=["list" | "tree" | "lists" | "graph" | None, ...]` and `out="list" | "tree"` convert to and from
`ListNode`/`TreeNode`/`Node`; `mutate=0` checks an argument modified in place; `kind="class"` + `cls="Trie"` for
design problems (tests are `[operations, arguments]`); `driver` and `checker` hold custom Python for special cases.

Learning content lives in `content/learn/`: `concepts.py` (Python toolkit), `patterns.py` (one guide per category) and
`insights.py` (one key-insight question per problem). Python concept tags on each solution line come from parsing the
solution's syntax tree (`scripts/learn.py`), and complexity/pattern questions are generated from each problem's explanation.
"Predict the output" questions are verified by running their code.

`npm run problems` runs every reference solution against its examples (and fails if any don't match), fills in
the hidden tests' expected outputs, checks that every starter compiles, and writes `data/problems.json`.
The test harness (`public/harness.py`) is the same file the browser worker loads.
