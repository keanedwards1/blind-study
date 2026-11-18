/**
 * Blind 75 from Scratch's own icon set: hand-drawn 24×24 stroke icons (no icon library).
 * Each category has its own line icon.
 */
import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

function Svg({ children, ...props }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...props}>
      {children}
    </svg>
  );
}

// ---------------------------------------------------------------- category icons

const ArraysIcon = (p: IconProps) => (
  <Svg {...p}>
    <rect x="2.5" y="9" width="19" height="7" rx="1.5" />
    <path d="M8.8 9v7M15.2 9v7" />
    <path d="M10 3.5 9.3 6.5M13.6 3.5l-.7 3M8.6 4.5h5.6M8.2 5.6h5.6" strokeWidth={1.4} />
  </Svg>
);
const TwoPointersIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M3 18h18" />
    <path d="M6 15V6M3.8 8.2 6 6l2.2 2.2M18 15V6M15.8 8.2 18 6l2.2 2.2" />
    <path d="M9.5 11.5h1.5M13 11.5h1.5" />
  </Svg>
);
const SlidingWindowIcon = (p: IconProps) => (
  <Svg {...p}>
    <rect x="6.5" y="7.5" width="11" height="9" rx="2.5" />
    {[3, 9, 15, 21].map((x) => (
      <circle key={x} cx={x} cy="12" r="1.1" fill="currentColor" stroke="none" />
    ))}
    <path d="M19.5 4.5h-4M17.5 2.5l2 2-2 2" strokeWidth={1.4} />
  </Svg>
);
const StackIcon = (p: IconProps) => (
  <Svg {...p}>
    <rect x="5" y="16" width="14" height="4" rx="1.2" />
    <rect x="5" y="10.5" width="14" height="4" rx="1.2" />
    <path d="M12 2.5v5.5M9.6 5.8 12 8.2l2.4-2.4" />
  </Svg>
);
const BinarySearchIcon = (p: IconProps) => (
  <Svg {...p}>
    <circle cx="10.5" cy="10.5" r="6.5" />
    <path d="m15.3 15.3 5.2 5.2M10.5 6.5v8" />
    <path d="M7.6 10.5h1M12.4 10.5h1" strokeWidth={1.4} />
  </Svg>
);
const LinkedListIcon = (p: IconProps) => (
  <Svg {...p}>
    <rect x="1.8" y="9" width="5.4" height="6" rx="1.4" />
    <rect x="9.3" y="9" width="5.4" height="6" rx="1.4" />
    <rect x="16.8" y="9" width="5.4" height="6" rx="1.4" />
    <path d="M7.2 12h2.1M14.7 12h2.1" />
  </Svg>
);
const TreesIcon = (p: IconProps) => (
  <Svg {...p}>
    <circle cx="12" cy="4.8" r="2.3" />
    <circle cx="6" cy="12.5" r="2.3" />
    <circle cx="18" cy="12.5" r="2.3" />
    <circle cx="3.6" cy="19.8" r="1.6" />
    <circle cx="9.4" cy="19.8" r="1.6" />
    <path d="M10.6 6.6 7.3 10.6M13.4 6.6l3.3 4M5.1 14.6 4.2 18.3M7 14.6l1.6 3.7" />
  </Svg>
);
const TriesIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M12 3v5M12 8l-6.5 7M12 8v7M12 8l6.5 7" />
    <circle cx="12" cy="8" r="1.4" fill="currentColor" stroke="none" />
    <path d="M3.6 20.5l1.9-5 1.9 5M4.3 18.7h2.4M10.5 15.5v5h1.6a1.4 1.4 0 0 0 0-2.8h-1.6M19.8 16a2.3 2.3 0 1 0 0 4" strokeWidth={1.4} />
  </Svg>
);
const HeapIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M12 3.5 21 19.5H3z" />
    <path d="M7.6 14.5h8.8M9.8 10h4.4" strokeWidth={1.4} />
    <circle cx="12" cy="7.2" r="1.1" fill="currentColor" stroke="none" />
  </Svg>
);
const BacktrackingIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M3 19h7.5a5.5 5.5 0 0 0 0-11H6" />
    <path d="M8.5 5.5 6 8l2.5 2.5" />
    <path d="M14.5 6.5 19 2.5M16.5 12h4.5" strokeDasharray="1.6 2.2" />
  </Svg>
);
const GraphsIcon = (p: IconProps) => (
  <Svg {...p}>
    <circle cx="5" cy="6" r="2.2" />
    <circle cx="18.5" cy="5" r="2.2" />
    <circle cx="6.5" cy="18.5" r="2.2" />
    <circle cx="18" cy="17" r="2.2" />
    <path d="M7.2 5.8 16.3 5.2M5.4 8.2l.7 8.1M8.7 18.2 15.8 17.2M17.7 7.2l.2 7.6M6.8 7.6l9.6 7.8" />
  </Svg>
);
const AdvancedGraphsIcon = (p: IconProps) => (
  <Svg {...p}>
    <circle cx="4.5" cy="18" r="2" />
    <circle cx="10" cy="8" r="2" />
    <circle cx="15" cy="15" r="2" />
    <circle cx="20" cy="5" r="2" />
    <path d="M5.5 16.2 9 9.8M11.2 9.7l2.7 3.6M16 13.2l3-6.4" />
    <path d="M3 9.5h3M4.5 8v3" strokeWidth={1.4} />
  </Svg>
);
const DP1Icon = (p: IconProps) => (
  <Svg {...p}>
    <rect x="2.5" y="13" width="19" height="6.5" rx="1.4" />
    <path d="M8.8 13v6.5M15.2 13v6.5" />
    <path d="M5.6 11c.6-3.5 5-3.5 6.4-.6M12.4 11c.6-3.5 5-3.5 6.4-.6" />
    <path d="m10.6 9.4 1.5 1.3 1.1-1.7M17.2 9.4l1.5 1.3 1.1-1.7" strokeWidth={1.4} />
  </Svg>
);
const DP2Icon = (p: IconProps) => (
  <Svg {...p}>
    <rect x="3" y="3" width="18" height="18" rx="2" />
    <path d="M9 3v18M15 3v18M3 9h18M3 15h18" strokeWidth={1.3} />
    <rect x="15" y="15" width="6" height="6" rx="0.5" fill="currentColor" stroke="none" opacity="0.9" />
    <path d="M6 12.2V6h6.2" strokeWidth={1.4} />
  </Svg>
);
const GreedyIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M6.5 4h11l3.5 5-9 11L3 9z" />
    <path d="M3 9h18M9.5 4 12 9l2.5-5M12 9v11" strokeWidth={1.4} />
  </Svg>
);
const IntervalsIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M3 7h10M10 12h11M5 17h9" />
    <path d="M3 5.5v3M13 5.5v3M10 10.5v3M21 10.5v3M5 15.5v3M14 15.5v3" strokeWidth={1.4} />
  </Svg>
);
const MathIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M4 20V5.5L18.5 20z" />
    <path d="M4 16.5h3.5V20" strokeWidth={1.4} />
    <circle cx="17" cy="7" r="3.5" />
    <path d="M17 3.5v7M13.5 7h7" strokeWidth={1.1} />
  </Svg>
);
const BitsIcon = (p: IconProps) => (
  <Svg {...p}>
    <rect x="2.5" y="4" width="19" height="7" rx="3.5" />
    <circle cx="18" cy="7.5" r="2" fill="currentColor" stroke="none" />
    <rect x="2.5" y="13" width="19" height="7" rx="3.5" />
    <circle cx="6" cy="16.5" r="2" />
  </Svg>
);

const categoryIcons: Record<string, (p: IconProps) => React.JSX.Element> = {
  "Arrays & Hashing": ArraysIcon,
  "Two Pointers": TwoPointersIcon,
  "Sliding Window": SlidingWindowIcon,
  Stack: StackIcon,
  "Binary Search": BinarySearchIcon,
  "Linked List": LinkedListIcon,
  Trees: TreesIcon,
  Tries: TriesIcon,
  "Heap / Priority Queue": HeapIcon,
  Backtracking: BacktrackingIcon,
  Graphs: GraphsIcon,
  "Advanced Graphs": AdvancedGraphsIcon,
  "1-D Dynamic Programming": DP1Icon,
  "2-D Dynamic Programming": DP2Icon,
  Greedy: GreedyIcon,
  Intervals: IntervalsIcon,
  "Math & Geometry": MathIcon,
  "Bit Manipulation": BitsIcon,
};

/**
 * Category colours: four shades from the site palette (theme tokens in globals.css), one per group of related categories:
 * sequences (Sky blue), structures and graphs (Lagoon), pointer and choice problems (Ember orange), DP and maths (Slate).
 */
const categoryHues: Record<string, string> = {
  "Arrays & Hashing": "var(--cat-sky)",
  "Two Pointers": "var(--cat-sky)",
  "Sliding Window": "var(--cat-sky)",
  Stack: "var(--cat-sky)",
  "Binary Search": "var(--cat-sky)",
  Trees: "var(--cat-lagoon)",
  Tries: "var(--cat-lagoon)",
  "Heap / Priority Queue": "var(--cat-lagoon)",
  Graphs: "var(--cat-lagoon)",
  "Advanced Graphs": "var(--cat-lagoon)",
  "Linked List": "var(--cat-ember)",
  Backtracking: "var(--cat-ember)",
  Intervals: "var(--cat-ember)",
  Greedy: "var(--cat-ember)",
  "1-D Dynamic Programming": "var(--cat-slate)",
  "2-D Dynamic Programming": "var(--cat-slate)",
  "Math & Geometry": "var(--cat-slate)",
  "Bit Manipulation": "var(--cat-slate)",
};

export function categoryHue(category: string): string {
  return categoryHues[category] ?? "var(--cat-slate)";
}

/** The line icon for a category (falls back to the arrays icon). */
export function CategoryIcon({ category, ...props }: IconProps & { category: string }) {
  const Icon = categoryIcons[category] ?? ArraysIcon;
  return <Icon {...props} />;
}

// ---------------------------------------------------------------- UI icons

export const ShuffleIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M3 7h3.5c4.5 0 6.5 10 11 10H21M3 17h3.5c1.7 0 3-1.4 4.1-3.2M13.4 10.2C14.5 8.4 15.8 7 17.5 7H21" />
    <path d="m18.5 4.5 2.5 2.5-2.5 2.5M18.5 14.5l2.5 2.5-2.5 2.5" />
  </Svg>
);
export const BookIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M12 6.5C10 5 7 4.5 3.5 5v13.5c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5z" />
    <path d="M12 6.5V20" />
  </Svg>
);
export const BoltIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M13 2.5 4.5 13.5H11l-1 8 8.5-11H12z" />
  </Svg>
);
export const TimerIcon = (p: IconProps) => (
  <Svg {...p}>
    <circle cx="12" cy="13.5" r="7.5" />
    <path d="M12 13.5V9.5M9.5 2.5h5M18.5 6.5l1.5-1.5" />
  </Svg>
);
export const CodeIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M8 6.5 3 12l5 5.5M16 6.5l5 5.5-5 5.5M13.5 4.5l-3 15" />
  </Svg>
);
export const SearchIcon = (p: IconProps) => (
  <Svg {...p}>
    <circle cx="11" cy="11" r="6.5" />
    <path d="m16 16 4.5 4.5" />
  </Svg>
);
export const DownloadIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M12 4v11M7.5 10.5 12 15l4.5-4.5M4.5 19.5h15" />
  </Svg>
);
export const UploadIcon = (p: IconProps) => (
  <Svg {...p}>
    <path d="M12 15V4M7.5 8.5 12 4l4.5 4.5M4.5 19.5h15" />
  </Svg>
);

/**
 * Logo: a sliding window. Five array cells, corner brackets framing the middle three (Lapis), and an arrow (Lagoon) moving
 * the window along. Brackets and the outer cells use the text colour, so the mark follows the theme.
 * Keep in sync with app/icon.svg (the favicon).
 */
export function SiteMark({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden="true">
      {[1.5, 7.5, 13.5, 19.5, 25.5].map((x, i) => (
        <rect key={x} x={x} y="13" width="5" height="6" className={i >= 1 && i <= 3 ? "fill-accent" : "fill-current opacity-35"} />
      ))}
      <path d="M6 13V8.5H10.5M21.5 8.5H26V13M26 19V23.5H21.5M10.5 23.5H6V19" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="square" />
      <path d="M9 28.5H22.5M19.5 25.5L22.5 28.5L19.5 31.5" fill="none" className="stroke-done" strokeWidth="2.2" strokeLinecap="square" />
    </svg>
  );
}
