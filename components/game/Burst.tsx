"use client";

import { useEffect, useRef } from "react";
import type { Biome } from "./theme";

const LEAF_COLORS = ["#e9b44c", "#c8913f", "#7fb069", "#9bc26b", "#d4a373", "#a3743a"];
const EMBER_COLORS = ["#ffe08a", "#ffb347", "#ff7a2f", "#ff5a1f"];

type Bit = { x: number; y: number; vx: number; vy: number; rot: number; spin: number; size: number; color: string; life: number; sway: number };

/**
 * A celebration burst: leaves that flutter down (soil and forest worlds) or embers that float up (fire worlds).
 * `waves` > 1 adds more bursts over time. Skipped when the viewer prefers reduced motion.
 */
export default function Burst({ biome, waves = 1 }: { biome: Biome; waves?: number }) {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const fire = biome === "fire";
    const resize = () => {
      canvas.width = canvas.clientWidth;
      canvas.height = canvas.clientHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const bits: Bit[] = [];
    const burst = (n: number) => {
      const colors = fire ? EMBER_COLORS : LEAF_COLORS;
      for (let i = 0; i < n; i++) {
        bits.push(
          fire
            ? { x: Math.random() * canvas.width, y: canvas.height + 10, vx: (Math.random() - 0.5) * 0.8, vy: -(1.5 + Math.random() * 3), rot: 0, spin: 0, size: 2 + Math.random() * 3, color: colors[i % colors.length], life: 200 + Math.random() * 120, sway: Math.random() * 6 }
            : { x: canvas.width / 2 + (Math.random() - 0.5) * 120, y: canvas.height * 0.35, vx: (Math.random() - 0.5) * 12, vy: -3 - Math.random() * 6, rot: Math.random() * 6, spin: (Math.random() - 0.5) * 0.25, size: 7 + Math.random() * 6, color: colors[i % colors.length], life: 240, sway: Math.random() * 6 },
        );
      }
    };
    burst(fire ? 120 : 90);
    const timers = Array.from({ length: waves - 1 }, (_, i) => setTimeout(() => burst(fire ? 80 : 60), 700 * (i + 1)));

    let raf = 0;
    let t = 0;
    const frame = () => {
      t++;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = bits.length - 1; i >= 0; i--) {
        const b = bits[i];
        if (fire) {
          b.x += b.vx + Math.sin((t + b.sway * 20) / 18) * 0.6;
          b.y += b.vy;
        } else {
          b.vy = Math.min(b.vy + 0.12, 1.6);
          b.vx *= 0.97;
          b.x += b.vx + Math.sin((t + b.sway * 20) / 14) * 1.2;
          b.y += b.vy;
          b.rot += b.spin;
        }
        if (--b.life <= 0 || b.y > canvas.height + 30 || b.y < -30) {
          bits.splice(i, 1);
          continue;
        }
        ctx.save();
        ctx.translate(b.x, b.y);
        ctx.globalAlpha = Math.min(1, b.life / 60);
        ctx.fillStyle = b.color;
        if (fire) {
          ctx.shadowColor = b.color;
          ctx.shadowBlur = 8;
          ctx.beginPath();
          ctx.arc(0, 0, b.size, 0, Math.PI * 2);
          ctx.fill();
        } else {
          ctx.rotate(b.rot);
          ctx.beginPath();
          ctx.ellipse(0, 0, b.size, b.size * 0.45, 0, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();
      }
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => {
      cancelAnimationFrame(raf);
      timers.forEach(clearTimeout);
      window.removeEventListener("resize", resize);
    };
  }, [biome, waves]);

  return <canvas ref={ref} className="pointer-events-none absolute inset-0 h-full w-full" aria-hidden />;
}
