"use client";

import { useSyncExternalStore } from "react";

const PREFIX = "drill:v1:";
const listeners = new Set<() => void>();
const cache = new Map<string, { raw: string | null; value: unknown }>();

function readRaw(key: string): string | null {
  try {
    return window.localStorage.getItem(PREFIX + key);
  } catch {
    return null;
  }
}

export function load<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  const raw = readRaw(key);
  const hit = cache.get(key);
  if (hit && hit.raw === raw) return (hit.value ?? fallback) as T;
  let value: unknown = fallback;
  if (raw !== null) {
    try {
      value = JSON.parse(raw);
    } catch {
      value = fallback;
    }
  }
  cache.set(key, { raw, value: raw === null ? null : value });
  return value as T;
}

export function save(key: string, value: unknown) {
  try {
    if (value === undefined) window.localStorage.removeItem(PREFIX + key);
    else window.localStorage.setItem(PREFIX + key, JSON.stringify(value));
  } catch {
    /* storage unavailable (private mode / quota) — progress just won't persist */
  }
  listeners.forEach((l) => l());
}

function subscribe(cb: () => void) {
  listeners.add(cb);
  const onStorage = (e: StorageEvent) => e.key?.startsWith(PREFIX) && cb();
  window.addEventListener("storage", onStorage);
  return () => {
    listeners.delete(cb);
    window.removeEventListener("storage", onStorage);
  };
}

/** Reactive localStorage value. Returns `fallback` during SSR / before hydration. */
export function useStored<T>(key: string, fallback: T): T {
  return useSyncExternalStore(
    subscribe,
    () => load(key, fallback),
    () => fallback,
  );
}

// ---- progress helpers
export type Progress = Record<string, number>; // slug -> timestamp

const EMPTY: Progress = {};

export function useSolved() {
  return useStored<Progress>("solved", EMPTY);
}
export function useAttempted() {
  return useStored<Progress>("attempted", EMPTY);
}

export function markSolved(slug: string) {
  save("solved", { ...load<Progress>("solved", {}), [slug]: Date.now() });
}
export function markAttempted(slug: string) {
  save("attempted", { ...load<Progress>("attempted", {}), [slug]: Date.now() });
}

export function exportAll(): string {
  const out: Record<string, unknown> = {};
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i)!;
      if (k.startsWith(PREFIX)) out[k.slice(PREFIX.length)] = JSON.parse(localStorage.getItem(k)!);
    }
  } catch {
    /* ignore */
  }
  return JSON.stringify(out, null, 2);
}

export function importAll(json: string) {
  const data = JSON.parse(json) as Record<string, unknown>;
  for (const [k, v] of Object.entries(data)) save(k, v);
}
