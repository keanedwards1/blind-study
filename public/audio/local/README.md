# Your own music

Put music files you own here and the Learn Python game plays them instead of the bundled CC0 tracks:

Files in `menu/` and `coding/` all go into one shuffled playlist that keeps playing as you move between screens.
Only the volume changes: fuller on the trail map, world screens and between stages, much quieter while you solve a stage.
(The two folders are just there for sorting; it doesn't matter which one a file is in.) Supported formats: mp3, m4a/aac, ogg, opus, wav, flac, webm.
Everything in this folder except this README is gitignored, so it is never committed or deployed.
No restart needed with `npm run dev`: after adding files, reload the page and the game picks them up.
With `next start`, rebuild after adding files, because a production build only serves files that existed at build time.

Volumes are set in `lib/audio/custom.ts` (`MUSIC_VOLUME`).
