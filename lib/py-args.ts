import { py } from "./format";

/**
 * The console's custom input: arguments written the way you'd write them in Python, separated by commas.
 *   5                      → [5]
 *   [2, 7, 11, 15], 9      → [[2, 7, 11, 15], 9]
 *   'hi', True, None       → ["hi", true, null]
 *   (1, 2), {"a": 1}       → [[1, 2], {"a": 1}]   (tuples become lists, as in the tests)
 * Throws an Error with a readable message when the text isn't valid.
 */
export function parsePyArgs(text: string): unknown[] {
  let out = "";
  let i = 0;
  const s = text.trim();
  while (i < s.length) {
    const c = s[i];
    if (c === '"' || c === "'") {
      let j = i + 1;
      let inner = "";
      while (j < s.length && s[j] !== c) {
        if (s[j] === "\\" && j + 1 < s.length) {
          inner += s[j] + s[j + 1];
          j += 2;
          continue;
        }
        inner += s[j];
        j++;
      }
      if (j >= s.length) throw new Error("A string is missing its closing quote.");
      // Re-quote as JSON: a single-quoted Python string may contain unescaped double quotes.
      out += '"' + (c === "'" ? inner.replace(/\\'/g, "'").replace(/(?<!\\)"/g, '\\"') : inner) + '"';
      i = j + 1;
    } else if (/[0-9.]/.test(c)) {
      // A whole number literal at once, so the "e" in 1e3 isn't read as a word. Python allows 1_000.
      const num = /^(?:\d[\d_]*)?(?:\.\d*)?(?:[eE][+-]?\d+)?/.exec(s.slice(i))![0] || c;
      out += num.replace(/_/g, "").replace(/\.$/, ".0").replace(/^\./, "0.");
      i += num.length;
    } else if (/[A-Za-z_]/.test(c)) {
      const word = /^[A-Za-z_]\w*/.exec(s.slice(i))![0];
      const map: Record<string, string> = { True: "true", False: "false", None: "null" };
      if (!(word in map)) throw new Error(`"${word}" isn't a value. Use numbers, "strings", [lists], True, False or None.`);
      out += map[word];
      i += word.length;
    } else {
      out += c === "(" ? "[" : c === ")" ? "]" : c;
      i++;
    }
  }
  // Python allows trailing commas, e.g. (5,) or [1, 2,]
  out = out.replace(/,\s*([\]}])/g, "$1");
  try {
    return JSON.parse(`[${out}]`);
  } catch {
    throw new Error("Couldn't read that input. Write the arguments like Python values, separated by commas, e.g. [1, 2], 3");
  }
}

/** The arguments of a test written back as console input. */
export function formatPyArgs(args: unknown[]): string {
  return args.map((a) => py(a)).join(", ");
}
