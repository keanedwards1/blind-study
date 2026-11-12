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
};

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
