"use client";

import { useEffect } from "react";
import { load, save, useStored } from "@/lib/storage";
import { CUSTOM_TRACKS, MUSIC_VOLUME } from "./custom";
import { fireCalmTrack, fireTrack, forestCalmTrack, forestTrack, playSfx, type SfxName, type Track } from "./tracks";

/** Map and transition screens use the menu music; coding stages use the quiet coding music. */
export type TrackId = "forest" | "forestCalm" | "fire" | "fireCalm";
export type AudioSettings = { music: boolean; sfx: boolean };
type Slot = "menu" | "coding";

const SETTINGS_KEY = "python:audio";
const DEFAULT_SETTINGS: AudioSettings = { music: true, sfx: true };
const GENERATED: Record<TrackId, Track> = { forest: forestTrack, forestCalm: forestCalmTrack, fire: fireTrack, fireCalm: fireCalmTrack };
const SLOT: Record<TrackId, Slot> = { forest: "menu", fire: "menu", forestCalm: "coding", fireCalm: "coding" };
/** The generated fallback is quieter by nature, so it gets its own levels. */
const GENERATED_LEVEL: Record<Slot, number> = { menu: 0.22, coding: 0.22 };
const FADE = 0.8;
/** Per-effect volume. The celebration sounds on the in-between screens (stage cleared, world intro/complete) sit lower than clicks. */
const SFX_LEVEL: Record<SfxName, number> = { click: 1, locked: 1, start: 0.45, star: 0.45, clear: 0.45, world: 0.45 };

type Source = { key: string; bus: GainNode; stop: () => void; pause?: () => void; resume?: () => void };
export type MusicLevels = { bass: number; mid: number; high: number; level: number };
const SILENT: MusicLevels = { bass: 0, mid: 0, high: 0, level: 0 };

function shuffle<T>(items: T[]): T[] {
  const a = [...items];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * One shared audio engine for the whole tab. It survives client-side navigation, so music carries on between game screens.
 * Browsers only allow sound after a click or key press, so nothing plays until unlock() is called from one.
 *
 * Music comes from, in order: your own files in public/audio/local/<slot>/ (a shuffled playlist), the bundled track in
 * lib/audio/custom.ts, or the generated ambience in tracks.ts.
 */
class Engine {
  private ctx: AudioContext | null = null;
  private master: GainNode | null = null;
  private sfxBus: GainNode | null = null;
  /** All music passes through here, so the analyser can measure it (for visuals) without touching sound effects. */
  private musicBus: GainNode | null = null;
  private analyser: AnalyserNode | null = null;
  private freq: Uint8Array<ArrayBuffer> = new Uint8Array(0);
  /** A second, unsmoothed analyser for beat (onset) detection: smoothing blurs and delays attacks. */
  private onsetAnalyser: AnalyserNode | null = null;
  private onsetFreq: Uint8Array<ArrayBuffer> = new Uint8Array(0);
  private playing: Source | null = null;
  /** File-based sources keep their element, so leaving a screen and coming back resumes where the music was. */
  private files = new Map<string, Source>();
  private desired: TrackId | null = null;
  private stopTimer: ReturnType<typeof setTimeout> | undefined;
  private settings: AudioSettings = DEFAULT_SETTINGS;
  /** Your own files per slot, from /api/local-music. Null until that answers, so the bundled track never plays first by mistake. */
  private local: Record<Slot, string[]> | null = null;

  unlock() {
    if (typeof window === "undefined") return;
    if (!this.ctx) {
      const Ctor = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (!Ctor) return;
      this.ctx = new Ctor();
      this.master = this.ctx.createGain();
      this.master.connect(this.ctx.destination);
      this.sfxBus = this.ctx.createGain();
      this.sfxBus.gain.value = 0.9;
      this.sfxBus.connect(this.master);
      this.musicBus = this.ctx.createGain();
      this.analyser = this.ctx.createAnalyser();
      this.analyser.fftSize = 1024;
      this.analyser.smoothingTimeConstant = 0.82;
      this.freq = new Uint8Array(this.analyser.frequencyBinCount);
      this.musicBus.connect(this.analyser);
      this.analyser.connect(this.master);
      this.onsetAnalyser = this.ctx.createAnalyser();
      this.onsetAnalyser.fftSize = 1024;
      this.onsetAnalyser.smoothingTimeConstant = 0;
      this.onsetFreq = new Uint8Array(this.onsetAnalyser.frequencyBinCount);
      this.musicBus.connect(this.onsetAnalyser);
      this.settings = load<AudioSettings>(SETTINGS_KEY, DEFAULT_SETTINGS);
      // Music keeps playing while the tab is in the background. If the browser suspended the audio anyway (some do after
      // a while), pick it back up when the tab is visible again.
      document.addEventListener("visibilitychange", () => {
        if (!this.ctx || document.hidden) return;
        if (this.ctx.state !== "running") void this.ctx.resume().then(() => this.sync());
        this.playing?.resume?.();
      });
      fetch("/api/local-music")
        .then((r) => (r.ok ? r.json() : null))
        .catch(() => null)
        .then((data: Record<Slot, string[]> | null) => {
          this.local = { menu: data?.menu ?? [], coding: data?.coding ?? [] };
          this.sync();
        });
    }
    if (this.ctx.state !== "running") void this.ctx.resume().then(() => this.sync());
    else this.sync();
  }

  /**
   * The track the current screen wants. When a screen goes away (null), the music only stops once you've actually left the
   * game: while you're still under /python, the next screen may just be loading, so the music carries on unchanged.
   */
  setTrack(id: TrackId | null) {
    clearTimeout(this.stopTimer);
    if (id !== null) {
      this.desired = id;
      this.sync();
      return;
    }
    this.stopTimer = setTimeout(() => {
      if (window.location.pathname.startsWith("/python")) return;
      this.desired = null;
      this.sync();
    }, 1200);
  }

  setSettings(s: AudioSettings) {
    this.settings = s;
    this.sync();
  }

  /** How loud the music is right now, per band (0-1, raw: quiet music gives small numbers). All zero when nothing plays. */
  levels(): MusicLevels {
    const a = this.analyser;
    if (!a || !this.ctx || this.ctx.state !== "running" || !this.playing) return SILENT;
    a.getByteFrequencyData(this.freq);
    const hz = this.ctx.sampleRate / a.fftSize;
    const band = (lo: number, hi: number) => {
      const from = Math.max(1, Math.floor(lo / hz));
      const to = Math.min(this.freq.length - 1, Math.ceil(hi / hz));
      let sum = 0;
      for (let i = from; i <= to; i++) sum += this.freq[i];
      return sum / ((to - from + 1) * 255);
    };
    const bass = band(30, 250);
    const mid = band(250, 2000);
    const high = band(2000, 9000);
    return { bass, mid, high, level: (bass + mid + high) / 3 };
  }

  /** The current, unsmoothed spectrum (0-255 per bin) and the width of each bin in Hz; null when nothing plays. */
  spectrum(): { data: Uint8Array<ArrayBuffer>; hz: number } | null {
    const a = this.onsetAnalyser;
    if (!a || !this.ctx || this.ctx.state !== "running" || !this.playing) return null;
    a.getByteFrequencyData(this.onsetFreq);
    return { data: this.onsetFreq, hz: this.ctx.sampleRate / a.fftSize };
  }

  sfx(name: SfxName, index = 0) {
    if (!this.ctx || !this.sfxBus || !this.settings.sfx || this.ctx.state !== "running") return;
    const level = this.ctx.createGain();
    level.gain.value = SFX_LEVEL[name];
    level.connect(this.sfxBus);
    playSfx(this.ctx, level, name, index);
    setTimeout(() => level.disconnect(), 4000);
  }

  /** The files a slot plays: your own (if any), else the bundled track, else none (generated ambience). */
  /**
   * The music files. Menus and coding share ONE playlist, so moving between screens never changes the track, only its
   * volume (see MUSIC_VOLUME). With no files at all, the generated ambience is used instead.
   */
  private filesFor(): { key: string; urls: string[] } | null {
    const own = [...new Set([...(this.local?.menu ?? []), ...(this.local?.coding ?? [])])];
    if (own.length) return { key: `local:${own.join("|")}`, urls: own };
    const bundled = [...new Set([CUSTOM_TRACKS.menu, CUSTOM_TRACKS.coding].filter((u): u is string => Boolean(u)))];
    return bundled.length ? { key: `bundled:${bundled.join("|")}`, urls: bundled } : null;
  }

  private level(id: TrackId): number {
    const slot = SLOT[id];
    return this.filesFor() ? MUSIC_VOLUME[slot] : GENERATED_LEVEL[slot];
  }

  private sync() {
    const ctx = this.ctx;
    if (!ctx || !this.master || ctx.state !== "running" || this.local === null) return;
    const want = this.settings.music ? this.desired : null;
    const files = want ? this.filesFor() : null;
    const key = want ? (files?.key ?? `generated:${want}`) : null;
    const now = ctx.currentTime;

    if (this.playing && this.playing.key === key) {
      // Same source (e.g. map → world screen): keep playing, just glide to the right volume.
      this.playing.bus.gain.cancelScheduledValues(now);
      this.playing.bus.gain.setValueAtTime(this.playing.bus.gain.value, now);
      this.playing.bus.gain.linearRampToValueAtTime(this.level(want!), now + FADE);
      return;
    }
    if (this.playing) {
      const old = this.playing;
      old.bus.gain.cancelScheduledValues(now);
      old.bus.gain.setValueAtTime(old.bus.gain.value, now);
      old.bus.gain.linearRampToValueAtTime(0, now + FADE);
      setTimeout(() => {
        if (this.playing !== old) old.stop();
      }, FADE * 1000 + 100);
      this.playing = null;
    }
    if (!want || !key) return;
    const source = files ? this.playlist(ctx, key, files.urls) : this.generated(ctx, want, key);
    source.bus.gain.cancelScheduledValues(now);
    source.bus.gain.setValueAtTime(source.bus.gain.value, now);
    source.bus.gain.linearRampToValueAtTime(this.level(want), now + FADE);
    this.playing = source;
  }

  private generated(ctx: AudioContext, id: TrackId, key: string): Source {
    const bus = ctx.createGain();
    bus.gain.value = 0;
    bus.connect(this.musicBus!);
    const stop = GENERATED[id](ctx, bus);
    return { key, bus, stop: () => (stop(), bus.disconnect()) };
  }

  /** One looping track, or a shuffled playlist that moves to the next track when one ends. */
  private playlist(ctx: AudioContext, key: string, urls: string[]): Source {
    let source = this.files.get(key);
    if (!source) {
      const order = shuffle(urls);
      let index = 0;
      const el = new Audio(order[0]);
      el.preload = "auto";
      el.loop = order.length === 1;
      const next = () => {
        index = (index + 1) % order.length;
        el.src = order[index];
        void el.play().catch(() => {});
      };
      el.addEventListener("ended", next);
      // A file that can't be played (unsupported format, deleted) is skipped rather than stopping the music.
      el.addEventListener("error", () => order.length > 1 && setTimeout(next, 500));
      const bus = ctx.createGain();
      bus.gain.value = 0;
      ctx.createMediaElementSource(el).connect(bus);
      bus.connect(this.musicBus!);
      source = { key, bus, stop: () => el.pause(), pause: () => el.pause(), resume: () => void el.play().catch(() => {}) };
      this.files.set(key, source);
    }
    source.resume?.();
    return source;
  }
}

let engine: Engine | null = null;
export function audio(): Engine {
  if (!engine) engine = new Engine();
  return engine;
}

/** Play this track while the calling screen is mounted. */
export function useMusic(track: TrackId | null) {
  useEffect(() => {
    audio().setTrack(track);
    return () => audio().setTrack(null);
  }, [track]);
}

export function sfx(name: SfxName, index = 0) {
  audio().sfx(name, index);
}

export function useAudioSettings(): [AudioSettings, (s: AudioSettings) => void] {
  const settings = useStored<AudioSettings>(SETTINGS_KEY, DEFAULT_SETTINGS);
  const set = (s: AudioSettings) => {
    save(SETTINGS_KEY, s);
    audio().setSettings(s);
  };
  return [settings, set];
}
