/**
 * Original nature ambience and sound effects, synthesised with the Web Audio API (no audio files).
 *
 * - forest / forestCalm: wind through trees, birdsong, and the occasional soft marimba-like note.
 * - fire / fireCalm:     wind and a crackling fire (worlds 8-10).
 * The "Calm" versions play while you code: quieter, sparser, nothing sudden.
 */

export type Track = (ctx: AudioContext, out: AudioNode) => () => void;
export type SfxName = "click" | "locked" | "start" | "star" | "clear" | "world";

const midiToHz = (m: number) => 440 * 2 ** ((m - 69) / 12);
const rand = (a: number, b: number) => a + Math.random() * (b - a);

const noiseBuffers = new WeakMap<BaseAudioContext, AudioBuffer>();
function noiseBuffer(ctx: AudioContext): AudioBuffer {
  let buf = noiseBuffers.get(ctx);
  if (!buf) {
    buf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    noiseBuffers.set(ctx, buf);
  }
  return buf;
}

/** Calls `fn` at random intervals (in seconds), scheduled slightly ahead on the audio clock. */
function every(ctx: AudioContext, min: number, max: number, fn: (t: number) => void, firstDelay = rand(min, max) * 0.5): () => void {
  let next = ctx.currentTime + firstDelay;
  const id = setInterval(() => {
    while (next < ctx.currentTime + 0.3) {
      fn(next);
      next += rand(min, max);
    }
  }, 100);
  return () => clearInterval(id);
}

/** Wind: looping noise through a low-pass filter whose cutoff and volume drift slowly. */
function wind(ctx: AudioContext, out: AudioNode, level: number): () => void {
  const src = ctx.createBufferSource();
  src.buffer = noiseBuffer(ctx);
  src.loop = true;
  const filter = ctx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.value = 520;
  filter.Q.value = 0.7;
  const gain = ctx.createGain();
  gain.gain.value = level;
  const lfos = [
    [0.06, 260, filter.frequency],
    [0.09, level * 0.45, gain.gain],
  ] as const;
  const oscs = lfos.map(([rate, depth, param]) => {
    const osc = ctx.createOscillator();
    const d = ctx.createGain();
    osc.frequency.value = rate;
    d.gain.value = depth;
    osc.connect(d).connect(param);
    osc.start();
    return osc;
  });
  src.connect(filter).connect(gain).connect(out);
  src.start();
  return () => {
    src.stop();
    oscs.forEach((o) => o.stop());
  };
}

/** One bird call: a few quick whistled chirps, with a randomly chosen shape. */
function birdCall(ctx: AudioContext, out: AudioNode, t: number, level: number) {
  const kind = Math.floor(Math.random() * 3);
  const base = rand(2200, 3800);
  const chirps = kind === 2 ? 2 : Math.floor(rand(2, 6));
  for (let i = 0; i < chirps; i++) {
    const start = t + i * (kind === 2 ? 0.28 : rand(0.08, 0.14));
    const len = kind === 2 ? 0.22 : rand(0.05, 0.09);
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = "sine";
    const from = kind === 0 ? base * 1.25 : base * 0.85;
    const to = kind === 0 ? base * 0.8 : kind === 1 ? base * 1.3 : base * 1.15;
    osc.frequency.setValueAtTime(from, start);
    osc.frequency.exponentialRampToValueAtTime(to, start + len);
    g.gain.setValueAtTime(0, start);
    g.gain.linearRampToValueAtTime(level, start + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, start + len);
    osc.connect(g).connect(out);
    osc.start(start);
    osc.stop(start + len + 0.02);
  }
}

/** Fire: a low rumble plus random sharp crackles and pops. */
function fire(ctx: AudioContext, out: AudioNode, level: number, density: number): () => void {
  const rumble = ctx.createBufferSource();
  rumble.buffer = noiseBuffer(ctx);
  rumble.loop = true;
  const low = ctx.createBiquadFilter();
  low.type = "lowpass";
  low.frequency.value = 180;
  const rg = ctx.createGain();
  rg.gain.value = level * 0.9;
  rumble.connect(low).connect(rg).connect(out);
  rumble.start();
  const stopCrackle = every(ctx, 0.03 / density, 0.25 / density, (t) => {
    const src = ctx.createBufferSource();
    src.buffer = noiseBuffer(ctx);
    const hp = ctx.createBiquadFilter();
    hp.type = "bandpass";
    hp.frequency.value = rand(1200, 4000);
    const g = ctx.createGain();
    const len = rand(0.006, 0.03);
    const peak = level * rand(0.4, 1.6);
    g.gain.setValueAtTime(peak, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + len);
    src.connect(hp).connect(g).connect(out);
    src.start(t, rand(0, 1.9));
    src.stop(t + len + 0.01);
  });
  return () => {
    rumble.stop();
    stopCrackle();
  };
}

/** A soft wooden, marimba-like note. */
function marimba(ctx: AudioContext, out: AudioNode, midi: number, t: number, level: number) {
  const f = midiToHz(midi);
  for (const [mult, g, decay] of [[1, level, 1.1], [4, level * 0.18, 0.25], [10, level * 0.05, 0.06]] as const) {
    const osc = ctx.createOscillator();
    const env = ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(f * mult, t);
    env.gain.setValueAtTime(0, t);
    env.gain.linearRampToValueAtTime(g, t + 0.004);
    env.gain.exponentialRampToValueAtTime(0.0001, t + decay);
    osc.connect(env).connect(out);
    osc.start(t);
    osc.stop(t + decay + 0.05);
  }
}

// D major pentatonic, D4 to B5.
const SCALE = [62, 64, 66, 69, 71, 74, 76, 78, 81, 83];

/** Now and then, one to three gentle notes drifting down the scale. */
function notes(ctx: AudioContext, out: AudioNode, min: number, max: number, level: number): () => void {
  return every(ctx, min, max, (t) => {
    let i = Math.floor(rand(3, SCALE.length));
    const count = Math.floor(rand(1, 4));
    for (let k = 0; k < count; k++) {
      marimba(ctx, out, SCALE[i], t + k * rand(0.25, 0.45), level * (1 - k * 0.2));
      i = Math.max(0, i - Math.floor(rand(1, 3)));
    }
  });
}

/** An echo so notes and birds sound like they're outdoors. */
function space(ctx: AudioContext, out: AudioNode): AudioNode {
  const input = ctx.createGain();
  const delay = ctx.createDelay(2);
  const fb = ctx.createGain();
  const tone = ctx.createBiquadFilter();
  delay.delayTime.value = 0.33;
  fb.gain.value = 0.3;
  tone.type = "lowpass";
  tone.frequency.value = 2500;
  input.connect(out);
  input.connect(delay);
  delay.connect(tone).connect(fb).connect(delay);
  tone.connect(out);
  return input;
}

const combine = (...stops: (() => void)[]) => () => stops.forEach((s) => s());

export const forestTrack: Track = (ctx, out) => {
  const wet = space(ctx, out);
  return combine(
    wind(ctx, out, 0.5),
    every(ctx, 2.5, 7, (t) => birdCall(ctx, wet, t, 0.05)),
    notes(ctx, wet, 6, 12, 0.16),
  );
};

export const forestCalmTrack: Track = (ctx, out) => {
  const wet = space(ctx, out);
  return combine(
    wind(ctx, out, 0.32),
    every(ctx, 9, 22, (t) => birdCall(ctx, wet, t, 0.025)),
    notes(ctx, wet, 14, 28, 0.09),
  );
};

export const fireTrack: Track = (ctx, out) => {
  const wet = space(ctx, out);
  return combine(wind(ctx, out, 0.35), fire(ctx, out, 0.12, 1), notes(ctx, wet, 9, 16, 0.12));
};

export const fireCalmTrack: Track = (ctx, out) => combine(wind(ctx, out, 0.22), fire(ctx, out, 0.08, 0.6));

// ---------------------------------------------------------------- sound effects
export function playSfx(ctx: AudioContext, out: AudioNode, name: SfxName, index = 0) {
  const t = ctx.currentTime + 0.01;
  const tap = (freq: number, at: number, level: number, len = 0.09) => {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.frequency.setValueAtTime(freq, at);
    osc.frequency.exponentialRampToValueAtTime(freq * 0.55, at + len);
    g.gain.setValueAtTime(level, at);
    g.gain.exponentialRampToValueAtTime(0.0001, at + len);
    osc.connect(g).connect(out);
    osc.start(at);
    osc.stop(at + len + 0.02);
  };
  switch (name) {
    case "click":
      tap(520, t, 0.25, 0.06);
      break;
    case "locked":
      tap(150, t, 0.4, 0.12);
      tap(110, t + 0.1, 0.35, 0.14);
      break;
    case "start":
      marimba(ctx, out, 74, t, 0.3);
      marimba(ctx, out, 81, t + 0.15, 0.3);
      break;
    case "star":
      marimba(ctx, out, [74, 78, 81][Math.min(index, 2)], t, 0.35);
      marimba(ctx, out, [86, 90, 93][Math.min(index, 2)], t + 0.05, 0.1);
      break;
    case "clear":
      [74, 78, 81, 86].forEach((m, i) => marimba(ctx, out, m, t + i * 0.12, 0.3));
      marimba(ctx, out, 50, t, 0.35);
      birdCall(ctx, out, t + 0.6, 0.06);
      break;
    case "world":
      [74, 76, 78, 81, 83, 86].forEach((m, i) => marimba(ctx, out, m, t + i * 0.16, 0.3));
      [62, 69].forEach((m, i) => marimba(ctx, out, m - 12, t + i * 0.48, 0.35));
      birdCall(ctx, out, t + 1.1, 0.06);
      birdCall(ctx, out, t + 1.5, 0.05);
      break;
  }
}
