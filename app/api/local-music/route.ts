import { readdir } from "node:fs/promises";
import path from "node:path";
import { connection } from "next/server";

const AUDIO = /\.(mp3|m4a|aac|ogg|oga|opus|wav|flac|webm)$/i;
const SLOTS = ["menu", "coding"] as const;

/** Lists the music files in public/audio/local/{menu,coding}. Empty lists when the folders don't exist (e.g. a deploy). */
export async function GET() {
  await connection(); // read the folders on every request, so newly added files are picked up
  const base = path.join(process.cwd(), "public", "audio", "local");
  const list = async (slot: (typeof SLOTS)[number]) => {
    try {
      return (await readdir(path.join(base, slot)))
        .filter((f) => AUDIO.test(f) && !f.startsWith("."))
        .sort()
        .map((f) => `/audio/local/${slot}/${encodeURIComponent(f)}`);
    } catch {
      return [];
    }
  };
  const [menu, coding] = await Promise.all(SLOTS.map(list));
  return Response.json({ menu, coding });
}
