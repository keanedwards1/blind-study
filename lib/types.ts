export type Difficulty = "Easy" | "Medium" | "Hard";

export type TestCase = { args: unknown[]; expected: unknown };

export type RunSpec = {
  fn?: string;
  kind?: "class";
  cls?: string;
  in?: (string | null)[];
  out?: string;
  compare?: string;
  mutate?: number;
  driver?: string;
  checker?: string;
  /** Learn Python task formats (see public/harness.py). */
  stdin?: boolean;
  raises?: boolean;
  require?: string[];
  forbid?: string[];
};

export type Problem = {
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: string;
  desc: string;
  params: string[];
  starter: string;
  hints: string[];
  solution: string;
  explanation: string;
  spec: RunSpec;
  examples: TestCase[];
  tests: TestCase[];
  pattern: string;
  concepts: string[];
  lineTags: Record<string, string[]>;
  quiz: QuizQuestion[];
  /** Learn mode: the Python building blocks you could use to write an answer. */
  grammar: GrammarSection[];
};

export type GrammarSection = { title: string; items: string[] };

export type QuizQuestion = {
  id: string;
  kind: "insight" | "pattern" | "time" | "space" | "python" | "pattern-guide" | "python-basics" | "term";
  q: string;
  code?: string;
  options: string[];
  answer: number;
  why: string;
};

export type Concept = {
  id: string;
  title: string;
  group: string;
  summary: string;
  snippet: string;
  template: string;
  exampleSlug: string;
  exampleQuestion: string;
  output: string;
  notes: string;
  quiz: QuizQuestion[];
  usedIn: string[];
};

export type PatternGuide = {
  id: string;
  category: string;
  summary: string;
  signals: string[];
  template: string;
  complexity: string;
  pitfalls: string[];
  quiz: QuizQuestion[];
  problems: string[];
};

export type ProblemSummary = Pick<Problem, "slug" | "title" | "difficulty" | "category">;

export type CaseStatus = "pass" | "fail" | "error" | "timeout" | "skipped";

export type CaseResult = {
  status: CaseStatus;
  result?: unknown;
  error?: string | null;
  stdout?: string;
  ms?: number;
};

export type RunOutcome = {
  kind: "run" | "submit";
  compileError?: string;
  stdout?: string;
  cases: CaseResult[];
  tests: TestCase[];
  passed: number;
  total: number;
};

// ---- Learn Python
export type PyConcept = {
  id: string;
  title: string;
  intro: string;
  builtins: string[];
  problems: string[];
  /** Extra predict-the-output questions for the rep room (the concept's quiz questions are in the level's pool). */
  reps: QuizQuestion[];
  /** The mixed review group at the end of a world. */
  review: boolean;
};

export type PyLevel = {
  n: number;
  /** "python": authored fundamentals (levels 1-7); "blind": Blind 75 problems (levels 8-10). */
  kind: "python" | "blind";
  title: string;
  summary: string;
  /** False while a level's content hasn't been written yet. */
  ready: boolean;
  concepts: PyConcept[];
  problems: string[];
  /** Pool the level quiz draws from. */
  quiz: QuizQuestion[];
  /** Guardian mini-game content (Learn Python worlds only). */
  boss?: BossData;
};

/** Content for the guardian's mini-games, built and checked by scripts/python_levels.py. */
export type BossData = {
  /** Falling expressions: type the value. `alts` are other accepted spellings (a string without quotes). */
  exprs: { expr: string; answer: string; alts: string[] }[];
  /** Lightning round statements, each verified true or false at build time. */
  facts: { text: string; truth: boolean }[];
  /** Match pairs: an expression and what it gives. */
  pairs: { left: string; right: string }[];
  /** Slugs of short tasks for the coding strike. */
  strikes: string[];
};

export type PlacementTask = { level: number; slug: string };
