"use client";

import { useEffect, useRef, useState } from "react";
import { save, useStored } from "@/lib/storage";
import { NetworkIcon } from "../icons";
import { DEFAULTS, loadParams, matchingPreset, PALETTES, PRESETS, saveParams, SHAPES, SLIDERS, type Blend, type ShapeMode, type VisualParams } from "./params";
import Plexus, { liveMeters, type Meters, resolveColor, toHex } from "./Plexus";

const ENABLED_KEY = "python:visual-on";

/** Whether the stage visual is shown (remembered between visits; on by default). */
export function useVisualEnabled(): boolean {
  return useStored<boolean>(ENABLED_KEY, true);
}

/** On/off switch for the stage visual, styled to sit beside the music and sound buttons. */
export function VisualToggle() {
  const on = useVisualEnabled();
  return (
    <button
      type="button"
      aria-pressed={on}
      aria-label="Visual"
      title={`Visual: ${on ? "on" : "off"}`}
      onClick={() => save(ENABLED_KEY, !on)}
      className={`grid h-9 w-9 place-items-center rounded-full text-muted transition-opacity hover:bg-hover hover:text-fg ${on ? "" : "opacity-50"}`}
    >
      <NetworkIcon off={!on} />
    </button>
  );
}

/** The stage music visual: drawn straight on the page (no background of its own), with a tuning panel for testing. */
export default function MusicVisual({ accent }: { accent: string }) {
  // Saved settings (localStorage; the server gets the defaults, which is fine because nothing it renders depends on them).
  const [params, setParams] = useState<VisualParams>(loadParams);
  const paramsRef = useRef<VisualParams>(params);
  const [open, setOpen] = useState(false);

  const update = (patch: Partial<VisualParams>) => {
    const next = { ...paramsRef.current, ...patch };
    paramsRef.current = next;
    setParams(next);
    saveParams(next);
  };

  return (
    <div className="relative h-full min-h-[300px] w-full">
      <Plexus params={paramsRef} accent={accent} />
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="absolute top-1 right-1 z-10 rounded-full border border-line bg-panel/80 px-2.5 py-1 text-xs text-muted backdrop-blur hover:text-fg"
        aria-expanded={open}
      >
        {open ? "Close tuning" : "Tune visual"}
      </button>
      {open && <ControlPanel params={params} update={update} accent={accent} onClose={() => setOpen(false)} />}
    </div>
  );
}

function ControlPanel({
  params,
  update,
  accent,
  onClose,
}: {
  params: VisualParams;
  update: (p: Partial<VisualParams>) => void;
  accent: string;
  onClose: () => void;
}) {
  const [m, setM] = useState<Meters & { beatLit: boolean }>({ ...liveMeters, beatLit: false });
  const [copied, setCopied] = useState(false);

  // Live meters, refreshed while the panel is open.
  useEffect(() => {
    let raf = 0;
    const tick = (now: number) => {
      setM({ ...liveMeters, beatLit: now / 1000 - liveMeters.beatAt < 0.15 });
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  const palette = Object.entries(PALETTES).find(([, v]) => v.nodeColor === params.nodeColor && v.linkColor === params.linkColor && v.packetColor === params.packetColor && v.dustColor === params.dustColor)?.[0] ?? "Custom";

  const bar = (label: string, v: number) => (
    <div className="flex items-center gap-2 text-xs">
      <span className="w-10 text-muted">{label}</span>
      <span className="h-2 flex-1 overflow-hidden rounded-full bg-hover">
        <span className="block h-full rounded-full bg-accent transition-[width] duration-75" style={{ width: `${Math.min(100, (v / 1.5) * 100)}%` }} />
      </span>
    </div>
  );

  const randomize = () => {
    const patch: Partial<VisualParams> = {};
    for (const g of SLIDERS)
      for (const [key, , min, max, step] of g.items) {
        // Keep performance and beat-detection settings: those depend on your machine, music and headphones, not on taste.
        if (["nodes", "dust", "sensitivity", "beatThreshold", "beatGap", "latencyMs"].includes(key)) continue;
        (patch as Record<string, number>)[key] = Math.round((min + Math.random() * (max - min)) / step) * step;
      }
    const names = Object.keys(PALETTES);
    Object.assign(patch, PALETTES[names[Math.floor(Math.random() * names.length)]]);
    patch.shape = (["auto", ...SHAPES] as ShapeMode[])[Math.floor(Math.random() * (SHAPES.length + 1))];
    update(patch);
  };

  const copy = () => {
    const text = JSON.stringify(params, null, 2);
    navigator.clipboard?.writeText(text).then(
      () => {
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      },
      () => setCopied(false),
    );
  };

  return (
    <div className="fixed bottom-4 left-4 z-50 flex max-h-[78vh] w-[330px] flex-col overflow-hidden rounded-xl border border-line bg-panel text-sm text-fg shadow-2xl">
      <div className="flex items-center justify-between border-b border-line px-3 py-2">
        <span className="font-semibold">Visual tuning</span>
        <button type="button" onClick={onClose} className="text-subtle hover:text-fg" aria-label="Close">
          ✕
        </button>
      </div>
      <div className="flex flex-col gap-4 overflow-auto px-3 py-3">
        <section className="flex flex-col gap-1.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold">Music</span>
            <span className="flex items-center gap-1.5 text-muted">
              <span className={`h-2.5 w-2.5 rounded-full ${m.beatLit ? "bg-accent" : "bg-hover"}`} /> beat · {m.playing ? "playing" : "no music"}
            </span>
          </div>
          {bar("Bass", m.bass)}
          {bar("Mids", m.mid)}
          {bar("Highs", m.high)}
          {/* Onset strength against the beat threshold: a beat fires when the bar crosses the line. */}
          <div className="flex items-center gap-2 text-xs" title="A beat fires when the bar crosses the line">
            <span className="w-10 text-muted">Onset</span>
            <span className="relative h-2 flex-1 overflow-hidden rounded-full bg-hover">
              <span className={`block h-full rounded-full ${m.beatLit ? "bg-accent" : "bg-fg-2"}`} style={{ width: `${Math.min(100, (m.onset / Math.max(m.threshold * 2, 0.02)) * 100)}%` }} />
              <span className="absolute top-0 left-1/2 h-full w-0.5 bg-bad" />
            </span>
          </div>
        </section>

        <section className="grid grid-cols-2 gap-2">
          <label className="col-span-2 flex flex-col gap-1 text-xs text-muted">
            Preset (all settings)
            <select
              value={matchingPreset(params) ?? "Custom"}
              onChange={(e) => PRESETS[e.target.value] && update(PRESETS[e.target.value])}
              className="rounded-md border border-line bg-page px-2 py-1 text-sm font-medium text-fg"
            >
              {Object.keys(PRESETS).map((n) => (
                <option key={n}>{n}</option>
              ))}
              {!matchingPreset(params) && <option>Custom</option>}
            </select>
          </label>
          <label className="flex flex-col gap-1 text-xs text-muted">
            Shape
            <select value={params.shape} onChange={(e) => update({ shape: e.target.value as ShapeMode })} className="rounded-md border border-line bg-page px-2 py-1 text-sm text-fg">
              <option value="auto">Morph through all</option>
              {SHAPES.map((s) => (
                <option key={s} value={s}>
                  {s[0].toUpperCase() + s.slice(1)}
                </option>
              ))}
            </select>
          </label>
          <label className="flex flex-col gap-1 text-xs text-muted">
            Blend
            <select value={params.blend} onChange={(e) => update({ blend: e.target.value as Blend })} className="rounded-md border border-line bg-page px-2 py-1 text-sm text-fg">
              <option value="auto">Auto (light/dark)</option>
              <option value="normal">Normal</option>
              <option value="additive">Additive glow</option>
              <option value="multiply">Multiply (ink)</option>
            </select>
          </label>
          <label className="col-span-2 flex flex-col gap-1 text-xs text-muted">
            Palette (colours only)
            <select
              value={palette}
              onChange={(e) => PALETTES[e.target.value] && update(PALETTES[e.target.value])}
              className="rounded-md border border-line bg-page px-2 py-1 text-sm text-fg"
            >
              {Object.keys(PALETTES).map((n) => (
                <option key={n}>{n}</option>
              ))}
              {palette === "Custom" && <option>Custom</option>}
            </select>
          </label>
          {(
            [
              ["nodeColor", "Nodes"],
              ["linkColor", "Links"],
              ["packetColor", "Packets"],
              ["dustColor", "Dust"],
            ] as const
          ).map(([key, label]) => (
            <label key={key} className="flex items-center gap-2 text-xs text-muted">
              <input type="color" value={toHex(resolveColor(params[key], accent))} onChange={(e) => update({ [key]: e.target.value })} className="h-6 w-8 cursor-pointer rounded border border-line bg-transparent" />
              {label}
            </label>
          ))}
          <label className="flex items-center gap-2 text-xs text-muted">
            <input type="checkbox" checked={params.shockwaves} onChange={(e) => update({ shockwaves: e.target.checked })} /> Beat shockwaves
          </label>
          <label className="flex items-center gap-2 text-xs text-muted">
            <input type="checkbox" checked={params.lightning} onChange={(e) => update({ lightning: e.target.checked })} /> Beat lightning
          </label>
          <label className="flex items-center gap-2 text-xs text-muted">
            <input type="checkbox" checked={params.surge} onChange={(e) => update({ surge: e.target.checked })} /> Beat surge (speed-up)
          </label>
          <label className="flex flex-col gap-1 text-xs text-muted">
            Beat source
            <select value={params.beatSource} onChange={(e) => update({ beatSource: e.target.value as "full" | "bass" })} className="rounded-md border border-line bg-page px-2 py-1 text-sm text-fg">
              <option value="full">Any attack (piano)</option>
              <option value="bass">Bass only (drums)</option>
            </select>
          </label>
        </section>

        {SLIDERS.map((g) => (
          <section key={g.group} className="flex flex-col gap-1.5">
            <span className="text-xs font-semibold">{g.group}</span>
            {g.items.map(([key, label, min, max, step]) => (
              <label key={key} className="grid grid-cols-[1fr_auto] items-center gap-x-2 text-xs text-muted">
                <span>{label}</span>
                <span className="tabular-nums text-fg-2">{Number(params[key]).toFixed(step < 1 ? 2 : 0)}</span>
                <input
                  type="range"
                  min={min}
                  max={max}
                  step={step}
                  value={Number(params[key])}
                  onChange={(e) => update({ [key]: Number(e.target.value) })}
                  className="col-span-2 accent-[var(--accent)]"
                />
              </label>
            ))}
          </section>
        ))}
      </div>
      <div className="flex flex-wrap items-center gap-2 border-t border-line px-3 py-2">
        <button type="button" onClick={copy} className="rounded-md bg-fg px-2.5 py-1 text-xs font-semibold text-page hover:opacity-90">
          {copied ? "Copied" : "Copy settings"}
        </button>
        <button type="button" onClick={randomize} className="rounded-md border border-line px-2.5 py-1 text-xs hover:bg-hover">
          Randomize
        </button>
        <button type="button" onClick={() => update(DEFAULTS)} className="rounded-md border border-line px-2.5 py-1 text-xs hover:bg-hover">
          Reset
        </button>
      </div>
    </div>
  );
}
