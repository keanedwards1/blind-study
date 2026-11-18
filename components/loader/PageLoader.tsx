import "./page-loader.css";

/**
 * Loading screens. The centrepiece is the logo's sliding window stepping across its cells, over a skeleton shaped like the
 * page that's on its way, so the layout doesn't jump when it arrives. It fades in after a short delay, so fast loads never
 * show it. Server-safe (no hooks); all motion is CSS and stops under prefers-reduced-motion.
 *
 * - "workspace": a problem page or Learn Python stage (back bar plus three panes).
 * - "page": a regular page (hero card plus a grid of cards).
 * - "game": a forest screen (world map, stage map, guardian).
 * - "inline": just the mark and label, for a panel that's still loading (the code editor).
 */
type Variant = "workspace" | "page" | "game" | "inline";

/** The sliding-window mark, animated: the bracketed window (and its three lit cells) steps along five cells. */
function LoaderMark({ className = "h-12 w-12" }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={`overflow-visible ${className}`} aria-hidden="true">
      {[1.5, 7.5, 13.5, 19.5, 25.5].map((x) => (
        <rect key={x} x={x} y="13" width="5" height="6" className="fill-current opacity-25" />
      ))}
      <g className="pl-window">
        {[7.5, 13.5, 19.5].map((x) => (
          <rect key={x} x={x} y="13" width="5" height="6" className="fill-accent" />
        ))}
        <path d="M6 13V8.5H10.5M21.5 8.5H26V13M26 19V23.5H21.5M10.5 23.5H6V19" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="square" />
      </g>
      <g className="pl-arrow">
        <path d="M9 28.5H22.5M19.5 25.5L22.5 28.5L19.5 31.5" fill="none" className="stroke-done" strokeWidth="2.2" strokeLinecap="square" />
      </g>
    </svg>
  );
}

function Status({ label, tone = "text-muted" }: { label: string; tone?: string }) {
  return (
    <div className="flex flex-col items-center gap-3">
      <LoaderMark />
      <p className={`pl-label text-sm font-medium ${tone}`}>{label}</p>
    </div>
  );
}

/** A shimmering placeholder block (6px corners unless the caller sets its own). */
const Skel = ({ className }: { className: string }) => <div className={`pl-skel ${className.includes("rounded-") ? "" : "rounded-md"} ${className}`} />;

export default function PageLoader({ variant = "page", label = "Loading" }: { variant?: Variant; label?: string }) {
  if (variant === "inline") {
    return (
      <div role="status" aria-live="polite" className="pl-root grid h-full w-full place-items-center p-6">
        <Status label={label} />
      </div>
    );
  }

  if (variant === "game") {
    return (
      <div role="status" aria-live="polite" className="pl-root pl-forest relative flex min-h-[calc(100vh-var(--header-h))] flex-1 flex-col items-center justify-center gap-10 overflow-hidden px-4">
        <div className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-[linear-gradient(180deg,transparent,rgba(12,26,18,0.9))]" />
        <Status label={label} tone="text-[#c9bda4]" />
        <div className="flex w-full max-w-md items-center justify-between gap-3" aria-hidden="true">
          {Array.from({ length: 5 }, (_, i) => (
            <Skel key={i} className={`h-12 w-12 rounded-full ${i % 2 ? "translate-y-4" : ""}`} />
          ))}
        </div>
      </div>
    );
  }

  if (variant === "workspace") {
    return (
      <div role="status" aria-live="polite" className="pl-root pl-site flex min-w-0 flex-1 flex-col lg:h-[calc(100vh-var(--header-h))] lg:overflow-hidden">
        <div className="flex min-h-11 items-center justify-between gap-3 border-b border-line bg-panel px-4" aria-hidden="true">
          <Skel className="h-3 w-24" />
          <Skel className="h-3 w-16" />
        </div>
        <div className="relative grid min-h-[70vh] flex-1 grid-cols-1 lg:grid-cols-[0.95fr_1.2fr_0.95fr]" aria-hidden="true">
          <div className="flex flex-col gap-4 border-line bg-panel p-5 lg:border-r">
            <div className="flex gap-2">
              <Skel className="h-6 w-14" />
              <Skel className="ml-auto h-6 w-20" />
              <Skel className="h-6 w-16" />
            </div>
            <Skel className="mt-2 h-6 w-2/3" />
            <Skel className="h-3 w-full" />
            <Skel className="h-3 w-11/12" />
            <Skel className="h-3 w-3/4" />
            <Skel className="mt-3 h-20 w-full" />
            <Skel className="h-20 w-full" />
          </div>
          <div className="flex flex-col gap-3 border-line bg-page p-5 lg:border-r">
            {[60, 45, 70, 30, 55].map((w) => (
              <div key={w} style={{ width: `${w}%` }}>
                <Skel className="h-3 w-full" />
              </div>
            ))}
          </div>
          <div className="hidden flex-col gap-3 bg-panel p-5 lg:flex">
            <div className="flex gap-2">
              <Skel className="h-8 w-24" />
              <Skel className="h-8 w-28" />
              <Skel className="h-8 w-16" />
            </div>
            <Skel className="h-9 w-full" />
          </div>
          <div className="pointer-events-none absolute inset-0 grid place-items-center">
            <div className="rounded-md border border-line bg-panel/90 px-8 py-6 shadow-sm backdrop-blur-sm">
              <Status label={label} />
            </div>
          </div>
        </div>
        <span className="sr-only">{label}</span>
      </div>
    );
  }

  return (
    <div role="status" aria-live="polite" className="pl-root pl-site page-shell space-y-8">
      <div className="flex flex-wrap items-center gap-8 rounded-md border border-line bg-panel p-6 sm:p-8">
        <div className="flex min-w-0 flex-1 basis-80 flex-col gap-4" aria-hidden="true">
          <Skel className="h-10 w-56" />
          <Skel className="h-3 w-full max-w-lg" />
          <div className="mt-2 flex gap-3">
            <Skel className="h-10 w-36" />
            <Skel className="h-10 w-44" />
          </div>
        </div>
        <div className="grid w-full place-items-center sm:w-72">
          <Status label={label} />
        </div>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4" aria-hidden="true">
        {Array.from({ length: 8 }, (_, i) => (
          <Skel key={i} className="h-16" />
        ))}
      </div>
    </div>
  );
}

export { LoaderMark };
