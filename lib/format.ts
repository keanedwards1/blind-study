/** Render a JSON value the way Python would print it (None/True/False, double-quoted strings). */
export function py(v: unknown, max = 3000): string {
  const s = fmt(v);
  return s.length > max ? s.slice(0, max) + " …" : s;
}

function fmt(v: unknown): string {
  if (v === null || v === undefined) return "None";
  if (typeof v === "boolean") return v ? "True" : "False";
  if (typeof v === "number") return String(v);
  if (typeof v === "string") return JSON.stringify(v);
  if (Array.isArray(v)) return "[" + v.map(fmt).join(", ") + "]";
  if (typeof v === "object")
    return "{" + Object.entries(v as Record<string, unknown>).map(([k, x]) => `${JSON.stringify(k)}: ${fmt(x)}`).join(", ") + "}";
  return String(v);
}

/**
 * Show a test value the way the task compares it: printed text as-is, strict (type-exact) values as Python's own repr text
 * (the harness already produced it), an expected exception as "raises X", and everything else via py().
 */
export function show(spec: { out?: string; compare?: string }, v: unknown): string {
  if (v && typeof v === "object" && !Array.isArray(v) && Object.keys(v).length === 1 && "raises" in v) return `raises ${(v as { raises: string }).raises}`;
  if (typeof v === "string" && spec.out === "stdout") return v === "" ? "(nothing printed)" : v;
  if (typeof v === "string" && spec.compare === "strict") return v;
  return py(v);
}

export function clock(totalSeconds: number): string {
  const s = Math.max(0, Math.floor(totalSeconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  const mm = String(m).padStart(h ? 2 : 1, "0");
  return (h ? `${h}:` : "") + `${mm}:${String(sec).padStart(2, "0")}`;
}

export const difficultyColor: Record<string, string> = {
  Easy: "text-ok",
  Medium: "text-warn",
  Hard: "text-bad",
};
