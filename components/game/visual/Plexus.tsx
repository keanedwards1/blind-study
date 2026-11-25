"use client";

import { useEffect, useRef } from "react";
import { audio } from "@/lib/audio/engine";
import { type ColorRef, type Shape, SHAPES, type VisualParams } from "./params";

/**
 * A living 3D network drawn straight onto the page.
 *
 * - Nodes sit on one of several shapes (cloud, sphere, torus, double helix, spiral galaxy) and glide between them, while a
 *   3D flow field keeps everything gently liquid. Each node links to its nearest neighbours.
 * - Packets of light travel along the links, hopping from node to node and leaving short trails; a node flares as one arrives.
 * - A layer of fine dust behind gives depth. Perspective makes near lines and nodes stronger than far ones.
 * - Music: bass makes the structure breathe. Each beat (detected from sharp rises in the spectrum) makes the network surge
 *   faster for about a second and sends a shockwave outward that lights the links and pushes nodes as it passes, plus a burst
 *   of packets. Mids speed up the flow and the spin. Highs make nodes spark and send more packets.
 */

export type Meters = { bass: number; mid: number; high: number; beatAt: number; playing: boolean; onset: number; threshold: number };
/** Live music readings, published each frame for the tuning panel's meters (one visual is on screen at a time). */
export const liveMeters: Meters = { bass: 0, mid: 0, high: 0, beatAt: -10, playing: false, onset: 0, threshold: 0 };
type RGB = [number, number, number];
type Packet = { from: number; to: number; progress: number; hops: number; trail: number[] };
type Wave = { born: number; strength: number };

const TAU = Math.PI * 2;
const MAX_NODES = 500;
const MAX_DUST = 2500;
const MAX_PACKETS = 400;

// ---------------------------------------------------------------- colour helpers
function parseColor(css: string, fallback: RGB): RGB {
  const s = css.trim();
  const m = s.match(/rgba?\(\s*([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)/);
  if (m) return [Number(m[1]), Number(m[2]), Number(m[3])];
  const hex = s.replace("#", "");
  if (/^[0-9a-f]{6}$/i.test(hex)) return [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16)) as RGB;
  if (/^[0-9a-f]{3}$/i.test(hex)) return [0, 1, 2].map((i) => parseInt(hex[i] + hex[i], 16)) as RGB;
  return fallback;
}

/** Resolve a palette entry: a hex colour, a theme token, or the world's colour. */
export function resolveColor(ref: ColorRef, accent: string): RGB {
  if (ref === "world") return parseColor(accent, [233, 180, 76]);
  if (ref.startsWith("theme:")) {
    const v = getComputedStyle(document.documentElement).getPropertyValue(`--${ref.slice(6)}`);
    return parseColor(v || "#777777", [120, 120, 120]);
  }
  return parseColor(ref, [120, 120, 120]);
}

export const toHex = ([r, g, b]: RGB) => `#${[r, g, b].map((v) => Math.round(v).toString(16).padStart(2, "0")).join("")}`;
const rgba = ([r, g, b]: RGB, a: number) => `rgba(${r | 0},${g | 0},${b | 0},${Math.max(0, Math.min(1, a)).toFixed(3)})`;
const mix = (a: RGB, b: RGB, t: number): RGB => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];

const spriteCache = new Map<string, HTMLCanvasElement>();
function glow(c: RGB): HTMLCanvasElement {
  const key = c.map((v) => v | 0).join(",");
  let s = spriteCache.get(key);
  if (!s) {
    s = document.createElement("canvas");
    s.width = s.height = 64;
    const g = s.getContext("2d")!;
    const grad = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, `rgba(${key},0.9)`);
    grad.addColorStop(0.3, `rgba(${key},0.35)`);
    grad.addColorStop(1, `rgba(${key},0)`);
    g.fillStyle = grad;
    g.fillRect(0, 0, 64, 64);
    spriteCache.set(key, s);
  }
  return s;
}

// ---------------------------------------------------------------- shapes
function gaussian() {
  return Math.sqrt(-2 * Math.log(Math.random() + 1e-9)) * Math.cos(TAU * Math.random());
}

/** Target positions for every shape, in one shared random order so any prefix of nodes covers each shape evenly. */
function buildShapes(): Record<Shape, Float32Array> {
  const out = Object.fromEntries(SHAPES.map((s) => [s, new Float32Array(MAX_NODES * 3)])) as Record<Shape, Float32Array>;
  const order = Array.from({ length: MAX_NODES }, (_, i) => i).sort(() => Math.random() - 0.5);
  const golden = Math.PI * (3 - Math.sqrt(5));
  for (let k = 0; k < MAX_NODES; k++) {
    const i = order[k] * 3;
    // cloud: a soft ball, denser in the middle
    {
      const r = Math.pow(Math.random(), 0.55);
      const th = TAU * Math.random();
      const ph = Math.acos(2 * Math.random() - 1);
      out.cloud.set([r * Math.sin(ph) * Math.cos(th), r * Math.cos(ph) * 0.85, r * Math.sin(ph) * Math.sin(th)], i);
    }
    // sphere: even (Fibonacci) spacing
    {
      const y = 1 - (2 * (k + 0.5)) / MAX_NODES;
      const r = Math.sqrt(1 - y * y);
      out.sphere.set([r * Math.cos(golden * k) * 0.9, y * 0.9, r * Math.sin(golden * k) * 0.9], i);
    }
    // torus
    {
      const u = TAU * Math.random();
      const v = TAU * Math.random();
      out.torus.set([(0.68 + 0.27 * Math.cos(v)) * Math.cos(u), 0.27 * Math.sin(v), (0.68 + 0.27 * Math.cos(v)) * Math.sin(u)], i);
    }
    // double helix, with some nodes forming the rungs between the strands
    {
      const t = Math.random();
      const a = t * TAU * 2.2;
      const y = (t - 0.5) * 1.9;
      if (Math.random() < 0.18) {
        const f = Math.random() * 2 - 1;
        out.helix.set([0.45 * Math.cos(a) * f, y, 0.45 * Math.sin(a) * f], i);
      } else {
        const strand = Math.random() < 0.5 ? 0 : Math.PI;
        out.helix.set([0.45 * Math.cos(a + strand), y, 0.45 * Math.sin(a + strand)], i);
      }
    }
    // spiral galaxy: three arms around a bright core
    {
      const core = Math.random() < 0.18;
      const r = core ? Math.abs(gaussian()) * 0.12 : 0.15 + Math.pow(Math.random(), 0.8) * 0.85;
      const arm = Math.floor(Math.random() * 3);
      const a = arm * (TAU / 3) + r * 3.6 + gaussian() * 0.18;
      out.galaxy.set([r * Math.cos(a), gaussian() * 0.05 * (1.2 - r), r * Math.sin(a)], i);
    }
  }
  return out;
}

/** A smooth 3D flow: three domain-warped sine fields, one per axis, so motion curls instead of just waving. */
function flow(x: number, y: number, z: number, t: number, out: Float32Array) {
  out[0] = Math.sin(1.9 * y + 0.8 * t + Math.sin(1.4 * z - 0.5 * t));
  out[1] = Math.sin(1.7 * z - 0.7 * t + Math.cos(1.6 * x + 0.4 * t));
  out[2] = Math.sin(2.1 * x + 0.6 * t + Math.sin(1.3 * y + 0.9 * t));
}

// ---------------------------------------------------------------- component
export default function Plexus({ params, accent }: { params: React.RefObject<VisualParams>; accent: string }) {
  const wrap = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const box = wrap.current;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!box || !canvas || !ctx) return;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let w = 0;
    let h = 0;
    let ready = false;
    const resize = () => {
      const r = box.getBoundingClientRect();
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      w = r.width;
      h = r.height;
      canvas.width = Math.max(1, Math.round(w * dpr));
      canvas.height = Math.max(1, Math.round(h * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      // Setting the size clears the canvas, and this runs after the frame's draw but before the paint, so redraw now or
      // the visual flashes blank on every frame of a resize (e.g. while dragging a pane divider).
      if (ready) draw(performance.now());
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(box);

    // ---- state
    const shapes = buildShapes();
    let shapeIndex = 0;
    let shapeSince = 0;
    const cur = new Float32Array(shapes.cloud); // current (morphing) positions
    const pos = new Float32Array(MAX_NODES * 3); // after flow displacement (unit space)
    const sx = new Float32Array(MAX_NODES);
    const sy = new Float32Array(MAX_NODES);
    const sp = new Float32Array(MAX_NODES); // perspective scale
    const flare = new Float32Array(MAX_NODES); // brightens when a packet arrives
    const linkCount = new Uint8Array(MAX_NODES);
    const neighbours: number[][] = Array.from({ length: MAX_NODES }, () => []);
    const links: number[] = []; // pairs, flattened
    const dust = new Float32Array(MAX_DUST * 3);
    for (let i = 0; i < MAX_DUST; i++) {
      const r = 0.3 + Math.pow(Math.random(), 0.7) * 1.1;
      const th = TAU * Math.random();
      const ph = Math.acos(2 * Math.random() - 1);
      dust.set([r * Math.sin(ph) * Math.cos(th), r * Math.cos(ph) * 0.7, r * Math.sin(ph) * Math.sin(th)], i * 3);
    }
    let packets: Packet[] = [];
    let waves: Wave[] = [];
    const fv = new Float32Array(3);

    // music
    const lv = { bass: 0, mid: 0, high: 0 };
    let peak = 0.04;
    let lastBeat = -10;
    let breath = 0;
    // Beat (onset) detection: how sharply the spectrum is rising (spectral flux), against its own recent average.
    const prevSpec = new Float32Array(1024);
    const fluxHist: number[] = [];
    let lastDetect = -10;
    let pending: { at: number; strength: number }[] = []; // detected beats, delayed by the latency setting
    let surge = 0; // the speed-up after a beat, fading over about a second
    let packetDebt = 0;

    // colours (re-resolved every few frames, so palette edits and light/dark switches apply live)
    let colors = { node: [0, 0, 0] as RGB, link: [0, 0, 0] as RGB, packet: [0, 0, 0] as RGB, dust: [0, 0, 0] as RGB };
    let darkPage = false;
    const refreshColors = () => {
      const p = params.current;
      colors = {
        node: resolveColor(p.nodeColor, accent),
        link: resolveColor(p.linkColor, accent),
        packet: resolveColor(p.packetColor, accent),
        dust: resolveColor(p.dustColor, accent),
      };
      const page = parseColor(getComputedStyle(document.documentElement).getPropertyValue("--page") || "#ffffff", [255, 255, 255]);
      darkPage = (0.2126 * page[0] + 0.7152 * page[1] + 0.0722 * page[2]) / 255 < 0.45;
    };
    refreshColors();

    let flowT = 0;
    let spin = 0;
    let frame = 0;
    const start = performance.now();
    let last = start;

    const spawnPacket = (near?: boolean) => {
      if (packets.length >= MAX_PACKETS) return;
      const N = Math.min(params.current.nodes, MAX_NODES);
      for (let tries = 0; tries < 12; tries++) {
        const a = Math.floor(Math.random() * N);
        if (near && Math.hypot(pos[a * 3], pos[a * 3 + 1], pos[a * 3 + 2]) > 0.45) continue;
        const nb = neighbours[a];
        if (!nb.length) continue;
        packets.push({ from: a, to: nb[Math.floor(Math.random() * nb.length)], progress: 0, hops: params.current.packetHops, trail: [] });
        return;
      }
    };

    const draw = (now: number) => {
      const p = params.current;
      const t = (now - start) / 1000;
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      frame++;
      if (frame % 20 === 0) refreshColors();
      const N = Math.min(p.nodes, MAX_NODES);

      // ---- music
      const raw = audio().levels();
      peak = Math.max(peak * 0.997, raw.level * 1.1, 0.03);
      const norm = (v: number) => Math.min(1.5, (v / peak) * p.sensitivity * 0.8);
      const env = (c: number, target: number) => c + (target - c) * (target > c ? 0.4 : 0.07);
      const nb = norm(raw.bass);
      lv.bass = env(lv.bass, nb);
      lv.mid = env(lv.mid, norm(raw.mid));
      lv.high = env(lv.high, norm(raw.high));
      const playing = raw.level > 0.0015;

      // ---- beats: spectral flux over the chosen band, compared with mean + k·spread of the last ~0.8 s
      let onset = 0;
      let threshold = 0;
      const spec = audio().spectrum();
      if (spec) {
        const { data, hz } = spec;
        const lo = Math.max(1, Math.floor(30 / hz));
        const hi = Math.min(data.length - 1, Math.ceil((p.beatSource === "bass" ? 180 : 5000) / hz));
        let rise = 0;
        for (let i = lo; i <= hi; i++) {
          const d = data[i] - prevSpec[i];
          if (d > 0) rise += d;
        }
        for (let i = 0; i < data.length; i++) prevSpec[i] = data[i];
        onset = rise / ((hi - lo + 1) * 255);
        fluxHist.push(onset);
        if (fluxHist.length > 48) fluxHist.shift();
        const mean = fluxHist.reduce((s, v) => s + v, 0) / fluxHist.length;
        const spread = Math.sqrt(fluxHist.reduce((s, v) => s + (v - mean) ** 2, 0) / fluxHist.length);
        threshold = mean + spread * p.beatThreshold + 0.004;
        if (fluxHist.length > 12 && onset > threshold && t - lastDetect > p.beatGap) {
          lastDetect = t;
          pending.push({ at: t + p.latencyMs / 1000, strength: Math.min(1.5, onset / threshold - 0.4) });
        }
      } else {
        prevSpec.fill(0);
        fluxHist.length = 0;
      }
      while (pending.length && pending[0].at <= t) {
        const beat = pending.shift()!;
        lastBeat = t;
        breath = 1;
        if (p.surge) surge = Math.min(1.6, surge + 0.6 + 0.4 * beat.strength);
        if (p.shockwaves) waves.push({ born: t, strength: Math.min(1.4, 0.5 + 0.5 * beat.strength * p.bassPulse) });
        const burst = Math.round(3 + 4 * beat.strength * p.bassPulse);
        for (let i = 0; i < burst; i++) spawnPacket(true);
      }
      if (!playing) pending = [];
      breath *= Math.pow(0.03, dt);
      surge *= Math.exp(-dt / Math.max(0.1, p.surgeSeconds * 0.45));
      const rush = 1 + surge * p.surgeAmount * 2.5;
      Object.assign(liveMeters, { bass: lv.bass, mid: lv.mid, high: lv.high, beatAt: (start + lastBeat * 1000) / 1000, playing, onset, threshold });

      // ---- shape morph
      let target: Shape = p.shape === "auto" ? SHAPES[shapeIndex] : p.shape;
      if (p.shape === "auto" && t - shapeSince > p.morphSeconds) {
        shapeIndex = (shapeIndex + 1) % SHAPES.length;
        shapeSince = t;
        target = SHAPES[shapeIndex];
      }
      const tgt = shapes[target];
      const k = 1 - Math.exp(-dt * 0.9);
      for (let i = 0; i < N * 3; i++) cur[i] += (tgt[i] - cur[i]) * k;

      // ---- motion
      flowT += dt * p.flowSpeed * (1 + lv.mid * p.midFlow * 1.6) * rush;
      spin += dt * p.rotation * (1 + lv.mid * p.midFlow * 1.2) * rush;
      const swell = 1 + (0.1 * lv.bass + 0.14 * breath) * p.bassPulse;
      const turb = p.turbulence * (1 + lv.bass * p.bassPulse * 0.8);
      const R = Math.min(w, h) * 0.42 * p.zoom;
      const cx = w / 2;
      const cy = h / 2;
      const cosY = Math.cos(spin), sinY = Math.sin(spin), cosX = Math.cos(p.tilt), sinX = Math.sin(p.tilt);
      const fov = 2.8;
      const project = (x: number, y: number, z: number, i: number, xs: Float32Array, ys: Float32Array, ps: Float32Array) => {
        const x1 = x * cosY + z * sinY;
        const z1 = -x * sinY + z * cosY;
        const y1 = y * cosX - z1 * sinX;
        const z2 = y * sinX + z1 * cosX;
        const s = fov / (fov + z2);
        xs[i] = cx + x1 * R * s;
        ys[i] = cy + y1 * R * s;
        ps[i] = s;
      };
      waves = waves.filter((wv) => t - wv.born < 1.3);
      for (let i = 0; i < N; i++) {
        const o = i * 3;
        flow(cur[o] * 1.5, cur[o + 1] * 1.5, cur[o + 2] * 1.5, flowT, fv);
        let push = 1;
        if (waves.length) {
          const r = Math.hypot(cur[o], cur[o + 1], cur[o + 2]);
          for (const wv of waves) {
            const age = t - wv.born;
            push += 0.16 * wv.strength * (1 - age / 1.3) * Math.exp(-(((r - age * 1.25) / 0.14) ** 2));
          }
        }
        const k3 = swell * push;
        pos[o] = (cur[o] + fv[0] * turb * 0.25) * k3;
        pos[o + 1] = (cur[o + 1] + fv[1] * turb * 0.25) * k3;
        pos[o + 2] = (cur[o + 2] + fv[2] * turb * 0.25) * k3;
        project(pos[o], pos[o + 1], pos[o + 2], i, sx, sy, sp);
      }

      // ---- links: nearest neighbours within reach, capped per node
      links.length = 0;
      linkCount.fill(0, 0, N);
      for (let i = 0; i < N; i++) neighbours[i].length = 0;
      const L = p.linkDistance * swell;
      const L2 = L * L;
      for (let i = 0; i < N; i++) {
        if (linkCount[i] >= p.maxLinks) continue;
        const ox = pos[i * 3], oy = pos[i * 3 + 1], oz = pos[i * 3 + 2];
        for (let j = i + 1; j < N; j++) {
          const dx = pos[j * 3] - ox, dy = pos[j * 3 + 1] - oy, dz = pos[j * 3 + 2] - oz;
          const d2 = dx * dx + dy * dy + dz * dz;
          if (d2 < L2 && linkCount[j] < p.maxLinks) {
            links.push(i, j);
            linkCount[i]++;
            linkCount[j]++;
            neighbours[i].push(j);
            neighbours[j].push(i);
            if (linkCount[i] >= p.maxLinks) break;
          }
        }
      }

      // ---- draw
      ctx.globalCompositeOperation = "destination-out";
      ctx.fillStyle = `rgba(0,0,0,${1 - p.trails})`;
      ctx.fillRect(0, 0, w, h);
      const blend: GlobalCompositeOperation =
        p.blend === "additive" ? "lighter" : p.blend === "multiply" ? "multiply" : p.blend === "normal" ? "source-over" : darkPage ? "lighter" : "source-over";
      ctx.globalCompositeOperation = blend;
      const depthOf = (s: number) => Math.max(0, Math.min(1, (s - 0.72) / 0.55));

      // dust
      const D = Math.min(p.dust, MAX_DUST);
      if (D) {
        ctx.fillStyle = rgba(colors.dust, 1);
        const dsx = new Float32Array(1), dsy = new Float32Array(1), dsp = new Float32Array(1);
        for (let i = 0; i < D; i++) {
          const o = i * 3;
          const drift = Math.sin(flowT * 0.6 + i) * 0.03 * p.turbulence;
          project(dust[o] * swell + drift, dust[o + 1] * swell, dust[o + 2] * swell, 0, dsx, dsy, dsp);
          const dd = depthOf(dsp[0]);
          ctx.globalAlpha = 0.08 + 0.3 * dd;
          const s = p.dustSize * (0.6 + dd);
          ctx.fillRect(dsx[0] - s / 2, dsy[0] - s / 2, s, s);
        }
      }

      // shockwaves: a ring expanding through the network, lighting links as it passes
      waves = waves.filter((wv) => t - wv.born < 1.3);
      const waveBoost = (mx: number, my: number, mz: number) => {
        if (!waves.length) return 0;
        const r = Math.hypot(mx, my, mz);
        let b = 0;
        for (const wv of waves) {
          const age = t - wv.born;
          const front = age * 1.25;
          b += wv.strength * (1 - age / 1.3) * Math.exp(-(((r - front) / 0.09) ** 2));
        }
        return b;
      };

      // links
      ctx.lineCap = "round";
      for (let l = 0; l < links.length; l += 2) {
        const a = links[l], b = links[l + 1];
        const dd = (depthOf(sp[a]) + depthOf(sp[b])) / 2;
        const dist = Math.hypot(pos[a * 3] - pos[b * 3], pos[a * 3 + 1] - pos[b * 3 + 1], pos[a * 3 + 2] - pos[b * 3 + 2]);
        const fade = 1 - dist / L;
        const boost = waveBoost((pos[a * 3] + pos[b * 3]) / 2, (pos[a * 3 + 1] + pos[b * 3 + 1]) / 2, (pos[a * 3 + 2] + pos[b * 3 + 2]) / 2);
        ctx.globalAlpha = Math.min(1, p.linkOpacity * fade * (0.35 + 0.65 * dd) + boost * 0.8);
        ctx.strokeStyle = rgba(boost > 0.05 ? mix(colors.link, colors.packet, Math.min(1, boost)) : colors.link, 1);
        ctx.lineWidth = (0.5 + dd * 0.9) * (1 + boost * 1.5);
        ctx.beginPath();
        ctx.moveTo(sx[a], sy[a]);
        ctx.lineTo(sx[b], sy[b]);
        ctx.stroke();
      }

      // nodes
      const sparkChance = lv.high * p.highSpark * 0.03;
      for (let i = 0; i < N; i++) {
        flare[i] *= Math.pow(0.05, dt);
        if (Math.random() < sparkChance) flare[i] = Math.max(flare[i], 0.8);
        const dd = depthOf(sp[i]);
        const f = flare[i];
        const r = p.nodeSize * (0.55 + dd * 0.9) * (1 + f * 1.4);
        const col = f > 0.05 ? mix(colors.node, colors.packet, Math.min(1, f)) : colors.node;
        if (p.glow > 0.01 && (dd > 0.35 || f > 0.1)) {
          ctx.globalAlpha = p.glow * (0.18 + 0.5 * f) * (0.4 + dd);
          const g = r * (4 + f * 4);
          ctx.drawImage(glow(col), sx[i] - g, sy[i] - g, g * 2, g * 2);
        }
        ctx.globalAlpha = 0.35 + 0.6 * dd + 0.3 * f;
        ctx.fillStyle = rgba(col, 1);
        ctx.beginPath();
        ctx.arc(sx[i], sy[i], r, 0, TAU);
        ctx.fill();
      }

      // packets: spawn, travel along links, hop onward from node to node
      packetDebt += dt * p.packetRate * (1 + lv.high * p.highSpark * 1.5);
      while (packetDebt >= 1) {
        spawnPacket();
        packetDebt -= 1;
      }
      const trailLen = Math.round(2 + p.packetTrail * 14);
      packets = packets.filter((pk) => {
        if (pk.from >= N || pk.to >= N) return false;
        const dist = Math.hypot(pos[pk.from * 3] - pos[pk.to * 3], pos[pk.from * 3 + 1] - pos[pk.to * 3 + 1], pos[pk.from * 3 + 2] - pos[pk.to * 3 + 2]) || 0.05;
        pk.progress += (dt * p.packetSpeed * 0.45 * (1 + lv.mid * p.midFlow * 0.6) * (1 + surge * p.surgeAmount * 1.5)) / dist;
        if (pk.progress >= 1) {
          flare[pk.to] = 1;
          const options = neighbours[pk.to].filter((n) => n !== pk.from);
          if (--pk.hops <= 0 || !options.length) return false;
          pk.from = pk.to;
          pk.to = options[Math.floor(Math.random() * options.length)];
          pk.progress = 0;
        }
        const e = pk.progress;
        const x = sx[pk.from] + (sx[pk.to] - sx[pk.from]) * e;
        const y = sy[pk.from] + (sy[pk.to] - sy[pk.from]) * e;
        pk.trail.push(x, y);
        if (pk.trail.length > trailLen * 2) pk.trail.splice(0, pk.trail.length - trailLen * 2);
        return true;
      });
      for (const pk of packets) {
        const tr = pk.trail;
        const n = tr.length / 2;
        if (n > 1 && p.packetTrail > 0) {
          ctx.strokeStyle = rgba(colors.packet, 1);
          for (let i = 1; i < n; i++) {
            ctx.globalAlpha = (i / n) * 0.7;
            ctx.lineWidth = p.packetSize * 0.55 * (i / n);
            ctx.beginPath();
            ctx.moveTo(tr[i * 2 - 2], tr[i * 2 - 1]);
            ctx.lineTo(tr[i * 2], tr[i * 2 + 1]);
            ctx.stroke();
          }
        }
        const x = tr[tr.length - 2];
        const y = tr[tr.length - 1];
        const s = p.packetSize;
        if (p.glow > 0.01) {
          ctx.globalAlpha = 0.25 + p.glow * 0.6;
          ctx.drawImage(glow(colors.packet), x - s * 5, y - s * 5, s * 10, s * 10);
        }
        ctx.globalAlpha = 1;
        ctx.fillStyle = rgba(colors.packet, 1);
        ctx.beginPath();
        ctx.arc(x, y, s * 0.75, 0, TAU);
        ctx.fill();
      }

      // optional lightning on beats, along existing links
      if (p.lightning && t - lastBeat < 0.18 && links.length) {
        ctx.strokeStyle = rgba(mix(colors.packet, [255, 255, 255], darkPage ? 0.6 : 0.1), 1);
        for (let n = 0; n < 4; n++) {
          const l = Math.floor((Math.random() * links.length) / 2) * 2;
          const a = links[l], b = links[l + 1];
          ctx.globalAlpha = 0.7;
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.moveTo(sx[a], sy[a]);
          const steps = 6;
          for (let s = 1; s < steps; s++) {
            const f = s / steps;
            ctx.lineTo(sx[a] + (sx[b] - sx[a]) * f + (Math.random() - 0.5) * 10, sy[a] + (sy[b] - sy[a]) * f + (Math.random() - 0.5) * 10);
          }
          ctx.lineTo(sx[b], sy[b]);
          ctx.stroke();
        }
      }

      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation = "source-over";
    };

    let raf = 0;
    let running = false;
    const loop = (now: number) => {
      draw(now);
      raf = requestAnimationFrame(loop);
    };
    const play = () => {
      if (running || reduceMotion) return;
      running = true;
      last = performance.now();
      raf = requestAnimationFrame(loop);
    };
    const pause = () => {
      running = false;
      cancelAnimationFrame(raf);
    };
    if (reduceMotion) for (let i = 0; i < 40; i++) draw(start + i * 33);
    ready = true;

    let onScreen = true;
    const io = new IntersectionObserver(([e]) => {
      onScreen = e.isIntersecting;
      if (onScreen && !document.hidden) play();
      else pause();
    });
    io.observe(box);
    const onVisibility = () => (document.hidden || !onScreen ? pause() : play());
    document.addEventListener("visibilitychange", onVisibility);
    play();
    return () => {
      pause();
      io.disconnect();
      ro.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, [accent, params]);

  return (
    <div ref={wrap} className="absolute inset-0" aria-hidden>
      <canvas ref={canvasRef} className="absolute inset-0 h-full w-full" />
    </div>
  );
}
