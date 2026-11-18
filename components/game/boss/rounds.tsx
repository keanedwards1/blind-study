"use client";

/**
 * The guardian's mini-games. Each one is a self-contained round that reports how it went through `onDone`:
 * `damage` is how much of the guardian's resolve it breaks, `hurt` is how many acorns you lose.
 *
 * - Predict: read a snippet, type exactly what it prints.
 * - Match: pair each expression with its value against the clock (wrong pairs cost seconds).
 * - Falling: expressions drift down; type each value before it lands.
 * - Lightning: quick true-or-false statements, each on a short fuse.
 * - Strike: write a tiny function that passes its tests (double damage; the finishing blow).
 *
 * `relaxed` slows every timer down (and is on automatically when the system asks for reduced motion).
 */
import { useMemo, useRef, useState } from "react";
import type { Problem, QuizQuestion, RunOutcome } from "@/lib/types";
import { sfx } from "@/lib/audio/engine";
import CodePane from "../../CodePane";
import Markdown from "../../Markdown";
import { Button } from "../ui";
import "./rounds.css";

export type RoundResult = { damage: number; hurt: number; note: string };

function shuffled<T>(items: T[]): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

const normalise = (s: string) => s.replace(/[ \t]+$/gm, "").replace(/\n+$/, "").trim();

function RoundHead({ kind, children }: { kind: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1">
      <p className="text-xs tracking-[0.18em] text-[#c9bda4] uppercase">{kind}</p>
      <div className="text-[#efe6d2]">{children}</div>
    </div>
  );
}

function Finish({ result, color, onNext }: { result: RoundResult; color: string; onNext: () => void }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 border-t border-[rgba(244,236,220,0.1)] pt-4">
      <p className={result.damage ? "text-[#c9f2a6]" : "text-[#ffb27a]"}>{result.note}</p>
      <Button color={color} onClick={onNext}>
        Continue
      </Button>
    </div>
  );
}

// ------------------------------------------------------------------ predict the output
export function PredictRound({ q, color, onDone }: { q: QuizQuestion; color: string; onDone: (r: RoundResult) => void }) {
  const [typed, setTyped] = useState("");
  const [result, setResult] = useState<RoundResult | null>(null);
  const answer = q.options[q.answer];
  function check() {
    const ok = normalise(typed) === normalise(answer);
    sfx(ok ? "star" : "locked", 1);
    setResult(ok ? { damage: 1, hurt: 0, note: "Exactly right. The guardian staggers." } : { damage: 0, hurt: 1, note: "Not quite. You lose an acorn." });
  }
  return (
    <div className="n-card flex flex-col gap-4 p-5">
      <RoundHead kind="Predict the output">Type exactly what this prints.</RoundHead>
      <pre className="overflow-x-auto rounded-md bg-black/40 p-4 font-mono text-sm leading-6 text-[#f4ecdc]">{q.code}</pre>
      <label htmlFor="predict-answer" className="sr-only">
        What it prints
      </label>
      <textarea
        id="predict-answer"
        value={typed}
        onChange={(e) => setTyped(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey && !result) {
            e.preventDefault();
            check();
          }
        }}
        disabled={!!result}
        rows={Math.max(1, answer.split("\n").length)}
        spellCheck={false}
        autoFocus
        placeholder="Its output…"
        className="rounded-md border border-[rgba(244,236,220,0.2)] bg-black/30 px-3 py-2 font-mono text-sm text-[#f4ecdc] outline-none focus:border-[var(--world)]"
      />
      {!result ? (
        <div className="flex justify-end">
          <Button color={color} onClick={check} disabled={!typed.trim()}>
            Check
          </Button>
        </div>
      ) : (
        <>
          <div className="rounded-md bg-black/25 p-3 text-sm">
            <p className="text-[#c9bda4]">It prints:</p>
            <pre className="font-mono text-[#f4ecdc]">{answer}</pre>
            {q.why && (
              <div className="readable mt-2 text-[#efe6d2]">
                <Markdown>{q.why}</Markdown>
              </div>
            )}
          </div>
          <Finish result={result} color={color} onNext={() => onDone(result)} />
        </>
      )}
    </div>
  );
}

// ------------------------------------------------------------------ match
export function MatchRound({
  pairs: pool,
  relaxed,
  color,
  onDone,
}: {
  pairs: { left: string; right: string }[];
  relaxed: boolean;
  color: string;
  onDone: (r: RoundResult) => void;
}) {
  const pairs = useMemo(() => shuffled(pool).slice(0, 5), [pool]);
  const [lefts] = useState(() => shuffled(pairs.map((_, i) => i)));
  const [rights] = useState(() => shuffled(pairs.map((_, i) => i)));
  const [picked, setPicked] = useState<number | null>(null);
  const [done, setDone] = useState<Set<number>>(() => new Set());
  const [wrong, setWrong] = useState<number | null>(null);
  const [penalty, setPenalty] = useState(0);
  const [result, setResult] = useState<RoundResult | null>(null);
  const seconds = relaxed ? 75 : 45;

  function finish(matched: number) {
    const r: RoundResult =
      matched === pairs.length
        ? { damage: 2, hurt: 0, note: "Every pair matched in time. A heavy blow!" }
        : matched * 2 >= pairs.length
          ? { damage: 1, hurt: 0, note: `${matched} of ${pairs.length} pairs before time ran out. A glancing hit.` }
          : { damage: 0, hurt: 1, note: `Only ${matched} of ${pairs.length} pairs. You lose an acorn.` };
    sfx(r.damage ? "star" : "locked", 1);
    setResult(r);
  }

  function pickRight(i: number) {
    if (picked === null || result) return;
    if (picked === i) {
      const next = new Set(done).add(i);
      setDone(next);
      setPicked(null);
      sfx("click", 0.6);
      if (next.size === pairs.length) finish(next.size);
    } else {
      setWrong(i);
      setPenalty((p) => p + 3);
      sfx("locked", 0.5);
      setTimeout(() => setWrong(null), 400);
    }
  }

  return (
    <div className="n-card flex flex-col gap-4 p-5">
      <RoundHead kind="Match">Tap an expression, then the value it gives. Wrong pairs cost 3 seconds.</RoundHead>
      {!result && (
        <div className="h-2 overflow-hidden rounded-md bg-black/30" aria-hidden="true">
          <div
            key={penalty}
            className="boss-fuse h-full"
            style={{ background: color, animationDuration: `${Math.max(1, seconds - penalty)}s` }}
            onAnimationEnd={() => !result && finish(done.size)}
          />
        </div>
      )}
      <div className="grid grid-cols-2 gap-3">
        <div className="flex flex-col gap-2">
          {lefts.map((i) => (
            <button
              key={i}
              type="button"
              disabled={done.has(i) || !!result}
              onClick={() => setPicked(i)}
              className={`boss-tile font-mono ${done.has(i) ? "is-done" : picked === i ? "is-picked" : ""}`}
            >
              {pairs[i].left}
            </button>
          ))}
        </div>
        <div className="flex flex-col gap-2">
          {rights.map((i) => (
            <button
              key={i}
              type="button"
              disabled={done.has(i) || !!result}
              onClick={() => pickRight(i)}
              className={`boss-tile font-mono ${done.has(i) ? "is-done" : ""} ${wrong === i ? "n-shake is-wrong" : ""}`}
            >
              {pairs[i].right}
            </button>
          ))}
        </div>
      </div>
      {result && <Finish result={result} color={color} onNext={() => onDone(result)} />}
    </div>
  );
}

// ------------------------------------------------------------------ falling expressions
export function FallingRound({
  exprs: pool,
  relaxed,
  color,
  onDone,
}: {
  exprs: { expr: string; answer: string; alts: string[] }[];
  relaxed: boolean;
  color: string;
  onDone: (r: RoundResult) => void;
}) {
  const exprs = useMemo(() => shuffled(pool).slice(0, 6), [pool]);
  const [i, setI] = useState(0);
  const [caught, setCaught] = useState<boolean[]>([]);
  const [typed, setTyped] = useState("");
  const [flash, setFlash] = useState<string | null>(null);
  const [result, setResult] = useState<RoundResult | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const current = exprs[i];
  // Each one falls a little faster than the last.
  const duration = (relaxed ? 15 : 10) - i * (relaxed ? 0.6 : 0.8);

  function advance(ok: boolean) {
    const all = [...caught, ok];
    setCaught(all);
    setTyped("");
    setFlash(ok ? "Caught!" : `It landed: ${current.expr} is ${current.answer}`);
    sfx(ok ? "star" : "locked", ok ? 0.8 : 0.5);
    if (all.length === exprs.length) {
      const n = all.filter(Boolean).length;
      const r: RoundResult =
        n >= 5
          ? { damage: 2, hurt: 0, note: `${n} of ${exprs.length} caught. A heavy blow!` }
          : n >= 3
            ? { damage: 1, hurt: 0, note: `${n} of ${exprs.length} caught. A glancing hit.` }
            : { damage: 0, hurt: 1, note: `Only ${n} of ${exprs.length} caught. You lose an acorn.` };
      setResult(r);
    } else {
      setI(i + 1);
      inputRef.current?.focus();
    }
  }

  function check(value: string) {
    setTyped(value);
    const v = value.trim();
    if (current && (v === current.answer || current.alts.includes(v))) advance(true);
  }

  return (
    <div className="n-card flex flex-col gap-4 p-5">
      <RoundHead kind="Falling expressions">Type each value before it hits the forest floor.</RoundHead>
      <div className="boss-sky relative h-56 overflow-hidden rounded-md bg-black/30">
        {!result && current && (
          <div
            key={i}
            className="boss-fall absolute left-1/2 rounded-md px-3 py-2 font-mono text-base text-[#22170e] shadow-lg"
            style={{ background: color, animationDuration: `${duration}s` }}
            onAnimationEnd={() => advance(false)}
          >
            {current.expr}
          </div>
        )}
        <div className="absolute inset-x-0 bottom-0 h-3 bg-[#3b2a1c]" aria-hidden="true" />
        {flash && <p className="absolute top-2 left-3 text-xs text-[#c9bda4]">{flash}</p>}
      </div>
      {!result ? (
        <>
          <label htmlFor="falling-answer" className="sr-only">
            Value
          </label>
          <input
            id="falling-answer"
            ref={inputRef}
            value={typed}
            onChange={(e) => check(e.target.value)}
            autoFocus
            spellCheck={false}
            autoComplete="off"
            placeholder="Type the value…"
            className="rounded-md border border-[rgba(244,236,220,0.2)] bg-black/30 px-3 py-2 font-mono text-[#f4ecdc] outline-none focus:border-[var(--world)]"
          />
          <p className="text-xs text-[#8f8470]">
            {caught.filter(Boolean).length} caught · {i + 1} of {exprs.length} · text values can be typed with or without quotes
          </p>
        </>
      ) : (
        <Finish result={result} color={color} onNext={() => onDone(result)} />
      )}
    </div>
  );
}

// ------------------------------------------------------------------ lightning round
export function LightningRound({
  facts: pool,
  relaxed,
  color,
  onDone,
}: {
  facts: { text: string; truth: boolean }[];
  relaxed: boolean;
  color: string;
  onDone: (r: RoundResult) => void;
}) {
  const facts = useMemo(() => shuffled(pool).slice(0, 8), [pool]);
  const [i, setI] = useState(0);
  const [marks, setMarks] = useState<boolean[]>([]);
  const [result, setResult] = useState<RoundResult | null>(null);
  const fuse = relaxed ? 10 : 6;

  function answer(said: boolean | null) {
    const ok = said !== null && said === facts[i].truth;
    sfx(ok ? "star" : "locked", ok ? 0.7 : 0.5);
    const all = [...marks, ok];
    setMarks(all);
    if (all.length === facts.length) {
      const n = all.filter(Boolean).length;
      setResult(
        n >= 7
          ? { damage: 2, hurt: 0, note: `${n} of ${facts.length} right. Lightning strikes twice!` }
          : n >= 5
            ? { damage: 1, hurt: 0, note: `${n} of ${facts.length} right. A glancing hit.` }
            : { damage: 0, hurt: 1, note: `${n} of ${facts.length} right. You lose an acorn.` },
      );
    } else setI(i + 1);
  }

  return (
    <div className="n-card flex flex-col gap-4 p-5">
      <RoundHead kind="Lightning round">True or false? Each one has a short fuse.</RoundHead>
      <div className="flex gap-1" aria-hidden="true">
        {facts.map((_, k) => (
          <span key={k} className="h-1.5 flex-1 rounded-md" style={{ background: k < marks.length ? (marks[k] ? color : "rgba(255,90,60,0.7)") : "rgba(244,236,220,0.12)" }} />
        ))}
      </div>
      {!result ? (
        <>
          <div className="readable min-h-16 rounded-md bg-black/25 p-4 text-lg">
            <Markdown>{facts[i].text}</Markdown>
          </div>
          <div className="h-2 overflow-hidden rounded-md bg-black/30" aria-hidden="true">
            <div key={i} className="boss-fuse h-full" style={{ background: color, animationDuration: `${fuse}s` }} onAnimationEnd={() => answer(null)} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Button color={color} onClick={() => answer(true)}>
              True
            </Button>
            <Button ghost onClick={() => answer(false)}>
              False
            </Button>
          </div>
        </>
      ) : (
        <Finish result={result} color={color} onNext={() => onDone(result)} />
      )}
    </div>
  );
}

// ------------------------------------------------------------------ coding strike
export function StrikeRound({ task, color, onDone }: { task: Problem; color: string; onDone: (r: RoundResult) => void }) {
  const [code, setCode] = useState(task.starter);
  const [result, setResult] = useState<RoundResult | null>(null);
  function onSubmitted(o: RunOutcome) {
    if (!o.compileError && o.total > 0 && o.passed === o.total) {
      sfx("clear", 1);
      setResult({ damage: 2, hurt: 0, note: "Every test passes. The finishing blow lands for double damage!" });
    }
  }
  return (
    <div className="flex flex-col gap-3">
      <div className="n-card flex flex-col gap-2 p-5">
        <RoundHead kind="Coding strike · double damage">Write it, Submit it, land the blow.</RoundHead>
        <h2 className="font-display text-xl font-bold">{task.title}</h2>
        <div className="readable text-[#efe6d2]">
          <Markdown>{task.desc}</Markdown>
        </div>
      </div>
      {!result && (
        <div className="h-[460px] overflow-hidden rounded-md border border-line bg-panel text-fg">
          <CodePane problem={task} code={code} onCodeChange={setCode} onSubmitted={onSubmitted} onReset={() => setCode(task.starter)} />
        </div>
      )}
      <div className="n-card p-4">
        {result ? (
          <Finish result={result} color={color} onNext={() => onDone(result)} />
        ) : (
          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-[#c9bda4]">Submit runs every test. Pass them all to strike.</p>
            <Button ghost onClick={() => onDone({ damage: 0, hurt: 1, note: "" })}>
              Give up this strike
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
