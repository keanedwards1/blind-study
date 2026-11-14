"use client";

import Link from "next/link";
import { useEffect } from "react";
import { audio, sfx, useAudioSettings } from "@/lib/audio/engine";
import { MusicNote, Speaker } from "./icons";
import Scenery from "./Scenery";
import type { Biome } from "./theme";

/** Browsers only allow sound after a user gesture, so the first click or key press anywhere unlocks audio. */
export function useAudioUnlock() {
  useEffect(() => {
    const unlock = () => audio().unlock();
    document.addEventListener("pointerdown", unlock);
    document.addEventListener("keydown", unlock);
    return () => {
      document.removeEventListener("pointerdown", unlock);
      document.removeEventListener("keydown", unlock);
    };
  }, []);
}

/** Two separate switches: a music note for the music, a speaker for sound effects. Both are remembered. */
export function SoundButtons({ tone = "game" }: { tone?: "game" | "site" }) {
  const [settings, setSettings] = useAudioSettings();
  const cls = (on: boolean) =>
    `grid h-9 w-9 place-items-center rounded-full transition-opacity ${on ? "" : "opacity-50"} ${
      tone === "game" ? "text-[#f4ecdc] hover:bg-white/10" : "text-muted hover:bg-hover hover:text-fg"
    }`;
  return (
    <div className="flex items-center gap-1">
      <button
        type="button"
        aria-pressed={settings.music}
        aria-label="Music"
        title={`Music: ${settings.music ? "on" : "off"}`}
        onClick={() => setSettings({ ...settings, music: !settings.music })}
        className={cls(settings.music)}
      >
        <MusicNote muted={!settings.music} />
      </button>
      <button
        type="button"
        aria-pressed={settings.sfx}
        aria-label="Sound effects"
        title={`Sound effects: ${settings.sfx ? "on" : "off"}`}
        onClick={() => {
          setSettings({ ...settings, sfx: !settings.sfx });
          if (!settings.sfx) setTimeout(() => sfx("click"), 50);
        }}
        className={cls(settings.sfx)}
      >
        <Speaker muted={!settings.sfx} />
      </button>
    </div>
  );
}

type Back = { href: string; label: string };

/** Full-height game screen: biome scenery behind, and a top bar with an optional back link, a title, and the sound menu. */
export default function GameShell({ biome, back, title, children }: { biome: Biome; back?: Back; title?: React.ReactNode; children: React.ReactNode }) {
  useAudioUnlock();
  return (
    <div className="game relative flex min-h-[calc(100vh-var(--header-h))] flex-1 flex-col" data-biome={biome}>
      <Scenery biome={biome} />
      <div className={`relative z-10 mx-auto grid w-full max-w-5xl grid-cols-[1fr_auto_1fr] items-center gap-3 px-4 ${biome === "soil" ? "pt-12" : "pt-5"}`}>
        <div>
          {back && (
            <Link href={back.href} onClick={() => sfx("click")} className="text-sm text-[#c9bda4] hover:text-[#f4ecdc]">
              ← {back.label}
            </Link>
          )}
        </div>
        <div className="text-center">{title}</div>
        <div className="flex justify-end">
          <SoundButtons />
        </div>
      </div>
      {children}
    </div>
  );
}
