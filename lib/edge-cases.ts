import type { Problem, TestCase } from "./types";

/**
 * Edge cases are tests with a `note` ("empty list"). `problem.tests` starts with the examples, then the hidden tests;
 * an example can carry a note too. "Run" checks the examples plus every labelled edge case; "Submit" runs all tests.
 */
type Cases = Pick<Problem, "examples" | "tests">;

/** For each case "Run" checks, its index in `problem.tests`. */
export function runCaseIndexes(p: Cases): number[] {
  const n = p.examples.length;
  return [...p.examples.map((_, i) => i), ...p.tests.map((t, i) => (i >= n && t.note ? i : -1)).filter((i) => i >= 0)];
}

/** The cases "Run" checks: the examples, then the labelled edge cases. */
export function runCases(p: Cases): TestCase[] {
  return runCaseIndexes(p).map((i) => p.tests[i] ?? p.examples[i]);
}

/** Every labelled edge case (examples included), with its index in `problem.tests`. */
export function edgeCases(p: Cases): { test: TestCase; i: number; note: string }[] {
  return p.tests.flatMap((test, i) => (test.note ? [{ test, i, note: test.note }] : []));
}
