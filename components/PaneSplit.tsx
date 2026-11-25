"use client";

import { useRef, useState } from "react";
import { save, useStored } from "@/lib/storage";

/**
 * Resizable columns for a CSS grid. The grid gets `style` (it sets --pane-cols) and `lg:grid-cols-(--pane-cols)`; each pane
 * carries `data-pane`, and a <PaneHandle {...handle(i)} /> sits between pane i and pane i + 1 (in a zero-width track).
 * Widths are kept as fr values equal to the panes' pixel widths when last resized, so the proportions hold when the
 * window changes size. They're remembered under `storageKey`.
 */
export function usePaneSplit(storageKey: string, defaults: number[], minPx = 260) {
  const stored = useStored<number[] | null>(storageKey, null);
  const [live, setLive] = useState<number[] | null>(null);
  const sizes = live ?? (stored?.length === defaults.length && stored.every((n) => n > 0) ? stored : defaults);
  const style = { "--pane-cols": sizes.map((s) => `minmax(0,${s}fr)`).join(" 0px ") } as React.CSSProperties;
  const handle = (index: number) => ({ index, storageKey, minPx, panes: defaults.length, onLive: setLive });
  return { style, handle };
}

/** Pane i's new width (the pane after it takes up the difference), keeping both at least `minPx` wide. */
function resized(w: number[], i: number, width: number, minPx: number) {
  const pair = w[i] + w[i + 1];
  const min = Math.min(minPx, pair / 2);
  const left = Math.max(min, Math.min(pair - min, width));
  return w.map((x, j) => (j === i ? left : j === i + 1 ? pair - left : x));
}

/** The pane widths, read from the grid that holds this handle. */
function measure(handle: HTMLElement) {
  const grid = handle.parentElement?.parentElement;
  return Array.from(grid?.querySelectorAll<HTMLElement>(":scope > [data-pane]") ?? [], (el) => el.getBoundingClientRect().width);
}

/** The drag handle between two columns: a thin line that lights up on hover, focus and drag. Hidden below `lg`. */
export function PaneHandle({
  label,
  className = "",
  index,
  storageKey,
  minPx,
  panes,
  onLive,
}: { label: string; className?: string } & ReturnType<ReturnType<typeof usePaneSplit>["handle"]>) {
  const drag = useRef<{ x: number; w: number[]; last?: number[] } | null>(null);

  const end = () => {
    const d = drag.current;
    if (!d) return;
    drag.current = null;
    document.documentElement.classList.remove("pane-resizing");
    if (d.last) save(storageKey, d.last.map(Math.round));
    onLive(null);
  };

  return (
    <div className="relative z-20 hidden w-0 lg:block">
      <div
        role="separator"
        aria-orientation="vertical"
        aria-label={label}
        tabIndex={0}
        title="Drag to resize"
        className={`group absolute inset-y-0 -left-1 w-2.25 cursor-col-resize touch-none outline-none ${className}`}
        onPointerDown={(e) => {
          if (e.button !== 0) return;
          const w = measure(e.currentTarget);
          if (w.length !== panes) return;
          e.preventDefault();
          e.currentTarget.setPointerCapture(e.pointerId);
          drag.current = { x: e.clientX, w };
          document.documentElement.classList.add("pane-resizing");
        }}
        onPointerMove={(e) => {
          const d = drag.current;
          if (!d) return;
          d.last = resized(d.w, index, d.w[index] + e.clientX - d.x, minPx);
          onLive(d.last);
        }}
        onPointerUp={end}
        onLostPointerCapture={end}
        onKeyDown={(e) => {
          const step = e.key === "ArrowLeft" ? -24 : e.key === "ArrowRight" ? 24 : 0;
          if (!step) return;
          const w = measure(e.currentTarget);
          if (w.length !== panes) return;
          e.preventDefault();
          save(storageKey, resized(w, index, w[index] + step, minPx).map(Math.round));
        }}
      >
        <span className="pointer-events-none absolute inset-y-0 left-0.75 w-0.75 bg-current opacity-0 transition-opacity duration-150 group-hover:opacity-100 group-focus-visible:opacity-100 group-active:opacity-100" />
      </div>
    </div>
  );
}
