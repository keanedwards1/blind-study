/**
 * Music for the Learn Python game.
 *
 * 1. Your own files: everything in public/audio/local/menu/ and public/audio/local/coding/ (gitignored) goes into ONE shuffled
 *    playlist that keeps playing across screens; only the volume changes between menus and coding. See public/audio/local/README.md.
 * 2. Otherwise these bundled CC0 tracks (see public/audio/CREDITS.md). Set a slot to null to use the generated ambience instead.
 */
export const CUSTOM_TRACKS: Record<"menu" | "coding", string | null> = {
  menu: "/audio/menu-lifewave-2k.m4a",
  coding: "/audio/coding-another-august.m4a",
};

/** Music volume (0-1) on menus and while coding. Both are the same, so moving between screens never changes the volume. */
export const MUSIC_VOLUME = { menu: 0.14, coding: 0.14 };
