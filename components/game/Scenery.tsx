import type { Biome } from "./theme";

/** Deterministic pseudo-random numbers so server and client render the same scenery. */
function seeded(seed: number) {
  let s = seed;
  return () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

/** A row of pine silhouettes along the bottom of a 1200-wide strip. */
function pines(seed: number, base: number, height: number, count: number): string {
  const r = seeded(seed);
  let d = "";
  for (let i = 0; i < count; i++) {
    const x = (i / count) * 1240 - 20 + r() * 30;
    const h = height * (0.6 + r() * 0.5);
    const w = h * 0.38;
    d += `M${x} ${base}L${x + w / 2} ${base - h}L${x + w} ${base}Z`;
  }
  return d;
}

function Particles({ kind, count, seed }: { kind: "n-firefly" | "n-ember" | "n-leaf"; count: number; seed: number }) {
  const r = seeded(seed);
  return (
    <>
      {Array.from({ length: count }, (_, i) => (
        <span
          key={i}
          className={`n-particle ${kind}`}
          style={{
            left: `${(r() * 100).toFixed(2)}%`,
            top: kind === "n-ember" ? "100%" : kind === "n-leaf" ? "0%" : `${(20 + r() * 70).toFixed(2)}%`,
            animationDelay: `${(-r() * 12).toFixed(2)}s`,
            animationDuration: kind === "n-firefly" ? undefined : `${(7 + r() * 8).toFixed(2)}s`,
          }}
        />
      ))}
    </>
  );
}

/** Illustrated background for a biome. Sits behind the page content and ignores the pointer. */
export default function Scenery({ biome }: { biome: Biome }) {
  return (
    <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden" aria-hidden>
      {biome === "soil" && (
        <>
          <svg className="absolute top-0 left-0 h-56 w-full" viewBox="0 0 1200 220" preserveAspectRatio="xMidYMin slice">
            <rect width="1200" height="26" fill="#4f7a3a" />
            <path d="M0 26q30-14 60 0t60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0 60 0V0H0z" fill="#6c9a4a" />
            {[90, 260, 470, 640, 860, 1050].map((x, i) => (
              <path
                key={x}
                d={`M${x} 26c${i % 2 ? 10 : -12} 40 ${i % 2 ? -30 : 26} 70 ${i % 2 ? -12 : 8} 120s${i % 2 ? 30 : -24} 40 ${i % 2 ? 10 : -6} 90`}
                stroke="#a37b52"
                strokeOpacity="0.35"
                strokeWidth={5 - (i % 3)}
                fill="none"
                strokeLinecap="round"
              />
            ))}
          </svg>
          <svg className="absolute bottom-0 left-0 h-40 w-full opacity-40" viewBox="0 0 1200 160" preserveAspectRatio="xMidYMax slice">
            {Array.from({ length: 26 }, (_, i) => {
              const r = seeded(i + 7);
              return <ellipse key={i} cx={r() * 1200} cy={40 + r() * 110} rx={6 + r() * 14} ry={4 + r() * 7} fill="#5a4330" />;
            })}
          </svg>
          <Particles kind="n-leaf" count={9} seed={3} />
        </>
      )}

      {biome === "forest" && (
        <>
          <div className="absolute inset-x-0 top-0 h-64 bg-[radial-gradient(ellipse_at_70%_0%,rgba(246,240,160,0.12),transparent_60%)]" />
          <svg className="absolute bottom-0 left-0 h-[55%] w-full" viewBox="0 0 1200 400" preserveAspectRatio="xMidYMax slice">
            <path d={pines(11, 400, 300, 26)} fill="#163222" />
            <path d={pines(23, 400, 220, 22)} fill="#11281b" />
            <path d={pines(37, 400, 140, 30)} fill="#0b1c13" />
          </svg>
          <Particles kind="n-firefly" count={18} seed={5} />
        </>
      )}

      {biome === "fire" && (
        <>
          <div className="absolute inset-x-0 bottom-0 h-[60%] bg-[radial-gradient(ellipse_at_50%_100%,rgba(255,122,47,0.45),transparent_65%)]" />
          <svg className="absolute bottom-0 left-0 h-[45%] w-full" viewBox="0 0 1200 300" preserveAspectRatio="xMidYMax slice">
            <path d={pines(41, 300, 230, 18)} fill="#1f0b07" />
            {Array.from({ length: 9 }, (_, i) => {
              const r = seeded(i + 51);
              const x = 60 + i * 135 + r() * 40;
              return <path key={i} d={`M${x} 300V${170 - r() * 60}M${x} ${230 - r() * 30}l${-18 - r() * 10} -26M${x} ${200 - r() * 20}l${16 + r() * 10} -22`} stroke="#140705" strokeWidth={6} strokeLinecap="round" />;
            })}
          </svg>
          <Particles kind="n-ember" count={26} seed={9} />
        </>
      )}
    </div>
  );
}
