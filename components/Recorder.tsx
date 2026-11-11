"use client";

import { useEffect, useRef, useState } from "react";
import { clock } from "@/lib/format";

export type Recording = { url: string; seconds: number };

function pickMime(): string | undefined {
  if (typeof MediaRecorder === "undefined") return undefined;
  return ["video/webm;codecs=vp9,opus", "video/webm;codecs=vp8,opus", "video/webm", "video/mp4"].find((m) => MediaRecorder.isTypeSupported(m));
}

/** Webcam + mic recorder. Everything stays in memory in this tab; nothing is uploaded. */
export default function Recorder({ maxSeconds, onRecorded }: { maxSeconds: number; onRecorded: (r: Recording | null) => void }) {
  const [phase, setPhase] = useState<"off" | "preview" | "recording" | "done">("off");
  const [error, setError] = useState<string | null>(null);
  const [elapsed, setElapsed] = useState(0);
  const [url, setUrl] = useState<string | null>(null);
  const [requesting, setRequesting] = useState(false);
  const liveRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const recRef = useRef<MediaRecorder | null>(null);
  const tickRef = useRef<ReturnType<typeof setInterval> | undefined>(undefined);

  useEffect(
    () => () => {
      clearInterval(tickRef.current);
      if (recRef.current?.state === "recording") recRef.current.stop();
      streamRef.current?.getTracks().forEach((t) => t.stop());
    },
    [],
  );

  async function enable() {
    setError(null);
    setRequesting(true);
    try {
      let stream: MediaStream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      } catch {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        setError("Microphone unavailable, so this will record video only. Check your mic before the real assessment!");
      }
      streamRef.current = stream;
      if (liveRef.current) liveRef.current.srcObject = stream;
      setPhase("preview");
    } catch (e) {
      setError(`Couldn't access the camera: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setRequesting(false);
    }
  }

  function start() {
    const stream = streamRef.current;
    if (!stream) return;
    const mime = pickMime();
    const rec = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined);
    const chunks: Blob[] = [];
    const startedAt = Date.now();
    rec.ondataavailable = (e) => e.data.size && chunks.push(e.data);
    rec.onstop = () => {
      clearInterval(tickRef.current);
      const blob = new Blob(chunks, { type: rec.mimeType || "video/webm" });
      const u = URL.createObjectURL(blob);
      const seconds = Math.round((Date.now() - startedAt) / 1000);
      setUrl(u);
      setPhase("done");
      onRecorded({ url: u, seconds });
    };
    recRef.current = rec;
    rec.start(1000);
    setElapsed(0);
    setPhase("recording");
    tickRef.current = setInterval(() => {
      const s = (Date.now() - startedAt) / 1000;
      setElapsed(s);
      if (s >= maxSeconds && rec.state === "recording") rec.stop();
    }, 250);
  }

  function stop() {
    if (recRef.current?.state === "recording") recRef.current.stop();
  }

  function redo() {
    setUrl(null);
    onRecorded(null);
    setPhase("preview");
  }

  const left = maxSeconds - elapsed;

  return (
    <div className="space-y-3">
      <div className="relative aspect-video w-full overflow-hidden rounded-lg border border-line bg-black">
        <video ref={liveRef} autoPlay muted playsInline className={`h-full w-full -scale-x-100 object-cover ${phase === "preview" || phase === "recording" ? "" : "hidden"}`} />
        {phase === "done" && url && <video src={url} controls playsInline className="h-full w-full object-contain" />}
        {phase === "off" && (
          <div className="absolute inset-0 flex items-center justify-center p-4 text-center text-sm text-subtle">Camera is off. Turning it on also checks your camera and mic.</div>
        )}
        {phase === "recording" && (
          <div className="absolute left-2 top-2 flex items-center gap-2 rounded bg-black/70 px-2 py-1 text-xs text-white">
            <span className="h-2 w-2 animate-pulse rounded-full bg-rose-500" /> REC {clock(elapsed)} / {clock(maxSeconds)}
          </div>
        )}
      </div>

      {error && <p className="text-sm text-bad">{error}</p>}

      <div className="flex flex-wrap items-center gap-2">
        {phase === "off" && (
          <button onClick={enable} disabled={requesting} className="rounded-md bg-btn px-3 py-1.5 text-sm text-fg hover:bg-btn-hover disabled:opacity-60">
            {requesting ? "Waiting for camera permission…" : "Turn on camera"}
          </button>
        )}
        {phase === "preview" && (
          <button onClick={start} className="rounded-md bg-rose-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-rose-500">
            ● Start recording
          </button>
        )}
        {phase === "recording" && (
          <>
            <button onClick={stop} className="rounded-md bg-fg px-3 py-1.5 text-sm font-medium text-page hover:opacity-90">
              ■ Stop
            </button>
            <span className={`text-sm ${left < 30 ? "text-bad" : "text-muted"}`}>{clock(left)} left</span>
          </>
        )}
        {phase === "done" && (
          <button onClick={redo} className="rounded-md border border-line-strong px-3 py-1.5 text-sm text-fg-2 hover:bg-hover">
            Re-record
          </button>
        )}
      </div>
    </div>
  );
}
