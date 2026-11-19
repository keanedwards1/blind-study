import { Blaze, Campfire, FlameTree, Fern, Oak, Pines, Roots, Sapling, Seed, Sprout } from "./icons";

export type Biome = "soil" | "forest" | "fire";

/** The forest trail: soil & roots (worlds 1-3), deep forest (4-7), firelands (8-10). */
export const WORLD_THEME: Record<number, { biome: Biome; color: string; Icon: (p: { size?: number; className?: string }) => React.ReactNode }> = {
  1: { biome: "soil", color: "#c8913f", Icon: Seed },
  2: { biome: "soil", color: "#9bc26b", Icon: Sprout },
  3: { biome: "soil", color: "#d4a373", Icon: Roots },
  4: { biome: "forest", color: "#7fb069", Icon: Fern },
  5: { biome: "forest", color: "#a3c96b", Icon: Sapling },
  6: { biome: "forest", color: "#6fbf8f", Icon: Oak },
  7: { biome: "forest", color: "#5fa37a", Icon: Pines },
  8: { biome: "fire", color: "#ffb347", Icon: Campfire },
  9: { biome: "fire", color: "#ff8c42", Icon: FlameTree },
  10: { biome: "fire", color: "#ff5a1f", Icon: Blaze },
};

/** A world colour used as text: full strength on dark scenes, darkened on the light trail and world pages (--n-world-ink). */
export const worldInk = (color: string) => `color-mix(in srgb, ${color} var(--n-world-ink, 100%), #1b120b)`;

export const BIOME_NAME: Record<Biome, string> = { soil: "Soil & roots", forest: "The deep forest", fire: "The firelands" };

/** Full ambience between stages; the calm version while coding. Worlds 8-10 crackle with fire. */
export function ambienceFor(world: number, calm: boolean): "forest" | "forestCalm" | "fire" | "fireCalm" {
  const burning = WORLD_THEME[world]?.biome === "fire";
  if (burning) return calm ? "fireCalm" : "fire";
  return calm ? "forestCalm" : "forest";
}
