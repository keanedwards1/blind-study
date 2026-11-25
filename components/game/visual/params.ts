/** Settings for the stage music visual. Everything the control panel can change lives here. */

export type Shape = "cloud" | "sphere" | "torus" | "helix" | "galaxy";
export type ShapeMode = Shape | "auto";
export type Blend = "auto" | "normal" | "additive" | "multiply";

/**
 * Colours: a hex value, or a token resolved from the page at runtime so the visual follows light/dark mode:
 * "theme:fg" (main text colour), "theme:muted" (secondary text), "world" (the current world's colour).
 */
export type ColorRef = string;

export type VisualParams = {
  shape: ShapeMode;
  morphSeconds: number;
  nodes: number;
  dust: number;
  linkDistance: number;
  maxLinks: number;
  linkOpacity: number;
  nodeSize: number;
  dustSize: number;
  packetRate: number;
  packetSpeed: number;
  packetSize: number;
  packetHops: number;
  packetTrail: number;
  flowSpeed: number;
  turbulence: number;
  rotation: number;
  tilt: number;
  zoom: number;
  trails: number;
  glow: number;
  sensitivity: number;
  bassPulse: number;
  midFlow: number;
  highSpark: number;
  shockwaves: boolean;
  lightning: boolean;
  /** What counts as a beat: any sharp attack (piano notes, Minecraft) or only the low end (drums). */
  beatSource: "full" | "bass";
  beatThreshold: number;
  beatGap: number;
  latencyMs: number;
  surge: boolean;
  surgeAmount: number;
  surgeSeconds: number;
  blend: Blend;
  nodeColor: ColorRef;
  linkColor: ColorRef;
  packetColor: ColorRef;
  dustColor: ColorRef;
};

export const DEFAULTS: VisualParams = {
  shape: "auto",
  morphSeconds: 14,
  nodes: 220,
  dust: 700,
  linkDistance: 0.32,
  maxLinks: 5,
  linkOpacity: 0.4,
  nodeSize: 1.7,
  dustSize: 0.9,
  packetRate: 9,
  packetSpeed: 1.2,
  packetSize: 2.4,
  packetHops: 5,
  packetTrail: 0.6,
  flowSpeed: 0.5,
  turbulence: 0.22,
  rotation: 0.18,
  tilt: 0.35,
  zoom: 1,
  trails: 0.35,
  glow: 0.55,
  sensitivity: 1.4,
  bassPulse: 1,
  midFlow: 1,
  highSpark: 1,
  shockwaves: true,
  lightning: false,
  beatSource: "full",
  beatThreshold: 1.6,
  beatGap: 0.28,
  latencyMs: 0,
  surge: true,
  surgeAmount: 1.2,
  surgeSeconds: 1,
  blend: "auto",
  nodeColor: "theme:fg",
  linkColor: "theme:muted",
  packetColor: "world",
  dustColor: "theme:muted",
};

/**
 * Full presets: every setting at once (shape, motion, beats and colours). Add one by pasting a "Copy settings" result here.
 * The Palette dropdown, below, changes colours only.
 */
export const PRESETS: Record<string, VisualParams> = {
  Default: DEFAULTS,
  "Navy ink": {
    shape: "auto",
    morphSeconds: 14,
    nodes: 220,
    dust: 750,
    linkDistance: 0.32,
    maxLinks: 6,
    linkOpacity: 0.4,
    nodeSize: 1.7,
    dustSize: 0.9,
    packetRate: 9,
    packetSpeed: 1.2,
    packetSize: 2.4,
    packetHops: 5,
    packetTrail: 0.5,
    flowSpeed: 0.5,
    turbulence: 0.22,
    rotation: 0.18,
    tilt: 0.35,
    zoom: 0.8,
    trails: 0.72,
    glow: 0.55,
    sensitivity: 0.3,
    bassPulse: 1,
    midFlow: 1,
    highSpark: 0.6,
    shockwaves: false,
    lightning: false,
    beatSource: "full",
    beatThreshold: 3.7,
    beatGap: 0.28,
    latencyMs: 0,
    surge: false,
    surgeAmount: 0.2,
    surgeSeconds: 1,
    blend: "additive",
    nodeColor: "theme:fg",
    linkColor: "theme:fg",
    packetColor: "#1c2f92",
    dustColor: "#000000",
  },
  "Ember galaxy": {
    shape: "galaxy",
    morphSeconds: 23,
    nodes: 220,
    dust: 850,
    linkDistance: 0.7,
    maxLinks: 3,
    linkOpacity: 0.68,
    nodeSize: 3,
    dustSize: 0.9,
    packetRate: 15,
    packetSpeed: 0.4,
    packetSize: 1.8,
    packetHops: 10,
    packetTrail: 0.38,
    flowSpeed: 1.6,
    turbulence: 0.51,
    rotation: -0.21,
    tilt: -1.12,
    zoom: 0.55,
    trails: 0.03,
    glow: 0.54,
    sensitivity: 1.05,
    bassPulse: 2.4,
    midFlow: 0.15,
    highSpark: 0.35,
    shockwaves: false,
    lightning: false,
    beatSource: "full",
    beatThreshold: 4,
    beatGap: 0.28,
    latencyMs: 0,
    surge: false,
    surgeAmount: 1.1,
    surgeSeconds: 0.45,
    blend: "additive",
    nodeColor: "#1d1b1a",
    linkColor: "#8a7f75",
    packetColor: "#ff6a1f",
    dustColor: "#544f4a",
  },
  "Mono sphere": {
    shape: "sphere",
    morphSeconds: 6,
    nodes: 220,
    dust: 750,
    linkDistance: 0.29,
    maxLinks: 4,
    linkOpacity: 0.16,
    nodeSize: 4.2,
    dustSize: 2.9,
    packetRate: 12,
    packetSpeed: 4.6,
    packetSize: 2.6,
    packetHops: 2,
    packetTrail: 0.76,
    flowSpeed: 1.15,
    turbulence: 0.94,
    rotation: -0.07,
    tilt: 0.11,
    zoom: 0.75,
    trails: 0.14,
    glow: 0.37,
    sensitivity: 0.15,
    bassPulse: 1.15,
    midFlow: 1.2,
    highSpark: 0.85,
    shockwaves: false,
    lightning: false,
    beatSource: "full",
    beatThreshold: 4,
    beatGap: 1.04,
    latencyMs: 0,
    surge: false,
    surgeAmount: 0.4,
    surgeSeconds: 1.1,
    blend: "additive",
    nodeColor: "theme:fg",
    linkColor: "theme:fg",
    packetColor: "theme:fg",
    dustColor: "theme:muted",
  },
};

/** The preset these settings exactly match, or null when they've been changed. */
export function matchingPreset(p: VisualParams): string | null {
  return Object.entries(PRESETS).find(([, preset]) => (Object.keys(preset) as (keyof VisualParams)[]).every((k) => preset[k] === p[k]))?.[0] ?? null;
}

export const SHAPES: Shape[] = ["cloud", "sphere", "torus", "helix", "galaxy"];

/** Colour presets. Each sets nodes, links, packets and dust. */
export const PALETTES: Record<string, Pick<VisualParams, "nodeColor" | "linkColor" | "packetColor" | "dustColor">> = {
  "Theme + world": { nodeColor: "theme:fg", linkColor: "theme:muted", packetColor: "world", dustColor: "theme:muted" },
  "Ink & ember": { nodeColor: "#1d1b1a", linkColor: "#8a7f75", packetColor: "#ff6a1f", dustColor: "#b8aea4" },
  "Deep sea": { nodeColor: "#0f3d5c", linkColor: "#4f8fb5", packetColor: "#18e0c8", dustColor: "#8fb8cf" },
  Aurora: { nodeColor: "#2b2d6e", linkColor: "#7c6cf0", packetColor: "#2fe6a8", dustColor: "#a99cf5" },
  "Neon (dark mode)": { nodeColor: "#9fe8ff", linkColor: "#5a7cff", packetColor: "#ff4fd8", dustColor: "#3c4c9a" },
  "Gold leaf": { nodeColor: "#5b4320", linkColor: "#b88a3e", packetColor: "#f2b134", dustColor: "#d8c39a" },
  Monochrome: { nodeColor: "theme:fg", linkColor: "theme:fg", packetColor: "theme:fg", dustColor: "theme:muted" },
};

const KEY = "drill:v1:python:visual";

export function loadParams(): VisualParams {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? { ...DEFAULTS, ...JSON.parse(raw) } : DEFAULTS;
  } catch {
    return DEFAULTS;
  }
}

export function saveParams(p: VisualParams) {
  try {
    localStorage.setItem(KEY, JSON.stringify(p));
  } catch {
    /* storage unavailable: settings just won't persist */
  }
}

/** Slider definitions: [key, label, min, max, step]. Grouped for the panel. */
export const SLIDERS: { group: string; items: [keyof VisualParams, string, number, number, number][] }[] = [
  {
    group: "Structure",
    items: [
      ["morphSeconds", "Seconds per shape", 4, 40, 1],
      ["nodes", "Nodes", 40, 500, 10],
      ["dust", "Dust particles", 0, 2500, 50],
      ["linkDistance", "Link distance", 0.08, 0.7, 0.01],
      ["maxLinks", "Links per node", 1, 12, 1],
      ["zoom", "Zoom", 0.5, 1.8, 0.05],
    ],
  },
  {
    group: "Look",
    items: [
      ["linkOpacity", "Link opacity", 0, 1, 0.01],
      ["nodeSize", "Node size", 0.3, 5, 0.1],
      ["dustSize", "Dust size", 0.2, 3, 0.1],
      ["glow", "Glow", 0, 1, 0.01],
      ["trails", "Trails", 0, 0.95, 0.01],
    ],
  },
  {
    group: "Packets",
    items: [
      ["packetRate", "Packets per second", 0, 60, 1],
      ["packetSpeed", "Packet speed", 0.1, 5, 0.1],
      ["packetSize", "Packet size", 0.5, 6, 0.1],
      ["packetHops", "Hops per packet", 1, 15, 1],
      ["packetTrail", "Packet trail", 0, 1, 0.01],
    ],
  },
  {
    group: "Motion",
    items: [
      ["flowSpeed", "Flow speed", 0, 3, 0.05],
      ["turbulence", "Turbulence", 0, 1, 0.01],
      ["rotation", "Rotation speed", -1.5, 1.5, 0.01],
      ["tilt", "Tilt", -1.2, 1.2, 0.01],
    ],
  },
  {
    group: "Beats",
    items: [
      ["beatThreshold", "Beat threshold (higher = fewer)", 0.3, 4, 0.05],
      ["beatGap", "Minimum gap between beats (s)", 0.08, 1.2, 0.01],
      ["latencyMs", "Latency (ms, for Bluetooth audio)", 0, 400, 5],
      ["surgeAmount", "Surge strength", 0, 4, 0.05],
      ["surgeSeconds", "Surge length (s)", 0.2, 3, 0.05],
    ],
  },
  {
    group: "Music",
    items: [
      ["sensitivity", "Sensitivity", 0, 3, 0.05],
      ["bassPulse", "Bass: pulse & shockwaves", 0, 3, 0.05],
      ["midFlow", "Mids: flow & spin", 0, 3, 0.05],
      ["highSpark", "Highs: sparks & packets", 0, 3, 0.05],
    ],
  },
];
