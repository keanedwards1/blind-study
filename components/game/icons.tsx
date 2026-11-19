/** Original SVG illustrations for the Learn Python game (48×48 viewBox). */

type IconProps = { size?: number; className?: string };
const svg = (size: number, className: string | undefined, children: React.ReactNode) => (
  <svg width={size} height={size} viewBox="0 0 48 48" className={className} aria-hidden>
    {children}
  </svg>
);

const SOIL = "#6b4a2f";
const BARK = "#7a5234";
const LEAF = "#7fb069";
const LEAF_DARK = "#4f7a3a";
const FLAME = "#ff7a2f";
const FLAME_LIGHT = "#ffc15e";

export function Seed({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <ellipse cx="24" cy="40" rx="16" ry="4" fill={SOIL} />
    <ellipse cx="24" cy="29" rx="9" ry="11" fill="#b07a45" />
    <path d="M20 22c2 3 2 9 0 14" stroke="#8b5a2b" strokeWidth="2" fill="none" strokeLinecap="round" />
    <path d="M24 18c1-5 5-8 10-8-1 5-5 8-10 8z" fill={LEAF} />
  </>);
}

export function Sprout({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <ellipse cx="24" cy="41" rx="17" ry="4.5" fill={SOIL} />
    <path d="M24 40V20" stroke={LEAF_DARK} strokeWidth="3" strokeLinecap="round" />
    <path d="M24 26c-9 0-13-6-13-12 8 0 13 5 13 12z" fill={LEAF} />
    <path d="M24 21c0-8 6-12 13-12 0 8-6 12-13 12z" fill={LEAF} />
  </>);
}

export function Roots({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <rect x="4" y="18" width="40" height="3" rx="1.5" fill={LEAF_DARK} />
    <path d="M21 4h6v15h-6z" fill={BARK} />
    <path d="M24 20c0 8-6 10-12 18M24 20c0 9 3 14 1 24M24 20c2 7 9 9 15 16M24 22c-4 5-12 4-17 9" stroke="#c49a6c" strokeWidth="2.5" fill="none" strokeLinecap="round" />
  </>);
}

export function Fern({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <path d="M24 44C24 28 30 14 40 6" stroke={LEAF_DARK} strokeWidth="2.5" fill="none" strokeLinecap="round" />
    {[0, 1, 2, 3, 4].map((i) => (
      <g key={i}>
        <ellipse cx={26 + i * 3} cy={36 - i * 6.5} rx="6" ry="2.4" fill={LEAF} transform={`rotate(${-35 + i * 4} ${26 + i * 3} ${36 - i * 6.5})`} />
        <ellipse cx={20 + i * 3.6} cy={33 - i * 6.5} rx="6" ry="2.4" fill={LEAF} transform={`rotate(${35 - i * 6} ${20 + i * 3.6} ${33 - i * 6.5})`} />
      </g>
    ))}
  </>);
}

export function Sapling({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <ellipse cx="24" cy="43" rx="14" ry="3.5" fill={SOIL} />
    <path d="M24 43V24" stroke={BARK} strokeWidth="4" strokeLinecap="round" />
    <circle cx="24" cy="18" r="11" fill={LEAF} />
    <circle cx="18" cy="21" r="6" fill={LEAF_DARK} opacity="0.6" />
  </>);
}

export function Oak({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <path d="M20 44l2-16h4l2 16z" fill={BARK} />
    <circle cx="15" cy="20" r="9" fill={LEAF_DARK} />
    <circle cx="33" cy="20" r="9" fill={LEAF_DARK} />
    <circle cx="24" cy="13" r="11" fill={LEAF} />
    <circle cx="24" cy="24" r="9" fill={LEAF} />
  </>);
}

export function Pines({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <path d="M15 6l9 16h-5l7 12H4l7-12H6z" fill={LEAF_DARK} />
    <path d="M33 10l8 14h-4l6 11H23l6-11h-4z" fill={LEAF} />
    <rect x="13.5" y="34" width="3" height="8" fill={BARK} />
    <rect x="31.5" y="35" width="3" height="7" fill={BARK} />
  </>);
}

export function Campfire({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <path d="M8 42l32-8M8 34l32 8" stroke={BARK} strokeWidth="5" strokeLinecap="round" />
    <path d="M24 6c6 8 11 13 11 21a11 11 0 0 1-22 0c0-5 3-8 5-11 1 4 3 6 5 6-2-6-1-11 1-16z" fill={FLAME} />
    <path d="M24 20c3 4 5 7 5 10a5 5 0 0 1-10 0c0-3 2-6 5-10z" fill={FLAME_LIGHT} />
  </>);
}

export function FlameTree({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <path d="M21 44l1.5-14h3L27 44z" fill="#3b2418" />
    <path d="M24 4c7 7 13 13 13 20a13 13 0 0 1-26 0c0-6 4-10 7-13 0 4 2 6 4 7-1-6 0-10 2-14z" fill={FLAME} />
    <path d="M24 16c4 4 7 8 7 11a7 7 0 0 1-14 0c0-3 3-7 7-11z" fill={FLAME_LIGHT} />
  </>);
}

export function Blaze({ size = 48, className }: IconProps) {
  return svg(size, className, <>
    <path d="M24 2c8 9 16 16 16 26a16 16 0 0 1-32 0c0-8 5-12 8-16 0 5 3 8 6 9-2-7-1-13 2-19z" fill="#ff5a1f" />
    <path d="M24 14c5 5 10 10 10 16a10 10 0 0 1-20 0c0-4 3-8 5-10 1 3 2 4 4 5-1-4 0-7 1-11z" fill={FLAME} />
    <path d="M24 26c3 3 5 5 5 8a5 5 0 0 1-10 0c0-3 2-5 5-8z" fill="#ffe08a" />
  </>);
}

export function Leaf({ size = 20, filled = true, className }: IconProps & { filled?: boolean }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden>
      {/* An empty leaf takes its colours from --n-leaf-empty(-line), so it shows on the light trail and world pages too. */}
      <path
        d="M4 20C4 9 11 3 21 3c0 11-6 18-17 17z"
        style={filled ? { fill: "#e9b44c", stroke: "#b98326" } : { fill: "var(--n-leaf-empty, rgba(244,236,220,0.14))", stroke: "var(--n-leaf-empty-line, rgba(244,236,220,0.3))" }}
        strokeWidth="1.2"
      />
      <path
        d="M5 19C9 14 13 10 18 6"
        style={{ stroke: filled ? "#b98326" : "var(--n-leaf-empty-line, rgba(244,236,220,0.3))" }}
        strokeWidth="1.2"
        fill="none"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function Lock({ size = 22, className }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden>
      <path d="M7 10V7a5 5 0 0 1 10 0v3" stroke="currentColor" strokeWidth="2.2" fill="none" />
      <rect x="4.5" y="10" width="15" height="11" rx="2.5" fill="currentColor" />
    </svg>
  );
}

/** The world guardian (boss): a wise old owl. */
export function Owl({ size = 72, className, angry = false }: IconProps & { angry?: boolean }) {
  return svg(size, className, <>
    <path d="M10 14l6 6M38 14l-6 6" stroke="#5a3e2b" strokeWidth="4" strokeLinecap="round" />
    <ellipse cx="24" cy="29" rx="15" ry="16" fill="#8a6440" />
    <ellipse cx="24" cy="34" rx="9" ry="10" fill="#d9c4a0" />
    <circle cx="18" cy="23" r="6" fill="#f4ecdc" />
    <circle cx="30" cy="23" r="6" fill="#f4ecdc" />
    <circle cx="18" cy="23" r="3" fill={angry ? "#c0392b" : "#22170e"} />
    <circle cx="30" cy="23" r="3" fill={angry ? "#c0392b" : "#22170e"} />
    <path d="M22 28l2 4 2-4z" fill="#e9b44c" />
    {angry && <path d="M12 16l9 4M36 16l-9 4" stroke="#22170e" strokeWidth="2.5" strokeLinecap="round" />}
  </>);
}

export function Acorn({ size = 22, spent = false, className }: IconProps & { spent?: boolean }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden style={spent ? { opacity: 0.25, filter: "grayscale(1)" } : undefined}>
      <path d="M12 2v3" stroke="#5a3e2b" strokeWidth="2" strokeLinecap="round" />
      <path d="M4 10c0-3 4-5 8-5s8 2 8 5z" fill="#7a5234" />
      <path d="M5.5 10h13c0 7-3 11-6.5 12C8.5 21 5.5 17 5.5 10z" fill="#c8913f" />
    </svg>
  );
}

export function Trophy({ size = 96, className }: IconProps) {
  return svg(size, className, <>
    <path d="M14 8h20v8a10 10 0 0 1-20 0z" fill="#e9b44c" />
    <path d="M14 11H8a6 6 0 0 0 7 7M34 11h6a6 6 0 0 1-7 7" stroke="#e9b44c" strokeWidth="3" fill="none" />
    <path d="M21 26h6v8h-6z" fill="#b98326" />
    <rect x="15" y="34" width="18" height="6" rx="2" fill={BARK} />
    <path d="M24 10c2 2 2 5 0 7-2-2-2-5 0-7z" fill={LEAF} />
  </>);
}

export function Speaker({ size = 20, muted = false, className }: IconProps & { muted?: boolean }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden>
      <path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor" />
      {muted ? (
        <path d="M16 9l5 6M21 9l-5 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      ) : (
        <path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" />
      )}
    </svg>
  );
}

export function MusicNote({ size = 20, muted = false, className }: IconProps & { muted?: boolean }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden>
      <path d="M9 17V5l10-2v12" stroke="currentColor" strokeWidth="2" fill="none" strokeLinejoin="round" />
      <circle cx="6.5" cy="17.5" r="2.5" fill="currentColor" />
      <circle cx="16.5" cy="15.5" r="2.5" fill="currentColor" />
      {muted && <path d="M3 3l18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />}
    </svg>
  );
}

/** Three linked nodes: the stage visual. Struck through when it's off. */
export function NetworkIcon({ size = 20, off = false, className }: IconProps & { off?: boolean }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden>
      <path d="M6 7l11 3M6 7l4 11M17 10l-7 8" stroke="currentColor" strokeWidth="1.6" fill="none" strokeLinecap="round" />
      <circle cx="6" cy="7" r="2.6" fill="currentColor" />
      <circle cx="17.5" cy="10" r="2.2" fill="currentColor" />
      <circle cx="10" cy="18.5" r="2.2" fill="currentColor" />
      {off && <path d="M3 3l18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />}
    </svg>
  );
}
