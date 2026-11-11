import raw from "@/data/problems.json";
import type { Problem, ProblemSummary } from "./types";

const data = raw as unknown as { categories: string[]; problems: Problem[] };

export const categories: string[] = data.categories;
export const problems: Problem[] = data.problems;

export function getProblem(slug: string): Problem | undefined {
  return problems.find((p) => p.slug === slug);
}

export function summaries(): ProblemSummary[] {
  return problems.map(({ slug, title, difficulty, category }) => ({ slug, title, difficulty, category }));
}

export function neighbours(slug: string): { prev?: ProblemSummary; next?: ProblemSummary } {
  const i = problems.findIndex((p) => p.slug === slug);
  const pick = (p?: Problem) => (p ? { slug: p.slug, title: p.title, difficulty: p.difficulty, category: p.category } : undefined);
  return { prev: pick(problems[i - 1]), next: pick(problems[i + 1]) };
}
