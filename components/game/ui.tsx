"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { sfx } from "@/lib/audio/engine";
import { Leaf } from "./icons";

type ButtonProps = {
  children: React.ReactNode;
  href?: string;
  onClick?: () => void;
  color?: string;
  ghost?: boolean;
  disabled?: boolean;
  className?: string;
  title?: string;
};

/** Rounded nature-style button with a soft wooden click. Disabled buttons give a dull knock instead. */
export function Button({ children, href, onClick, color, ghost, disabled, className = "", title }: ButtonProps) {
  const style = color ? ({ "--btn": color } as React.CSSProperties) : undefined;
  const cls = `n-btn ${ghost ? "ghost" : ""} ${className}`;
  if (href && !disabled)
    return (
      <Link href={href} className={cls} style={style} title={title} onClick={() => sfx("click")}>
        {children}
      </Link>
    );
  return (
    <button
      type="button"
      className={cls}
      style={style}
      title={title}
      aria-disabled={disabled || undefined}
      onClick={() => {
        if (disabled) return sfx("locked");
        sfx("click");
        onClick?.();
      }}
    >
      {children}
    </button>
  );
}

/** 0-3 leaves (the game's stars). With `animate`, they pop in one by one with a note each. */
export function LeafRow({ leaves, size = 18, animate = false, onDone }: { leaves: number; size?: number; animate?: boolean; onDone?: () => void }) {
  const [shown, setShown] = useState(animate ? 0 : 3);
  const done = useRef(onDone);
  useEffect(() => {
    done.current = onDone;
  });
  useEffect(() => {
    if (!animate) return;
    const timers = [1, 2, 3].map((i) =>
      setTimeout(() => {
        setShown(i);
        if (i <= leaves) sfx("star", i - 1);
        if (i === 3) done.current?.();
      }, 380 * i),
    );
    return () => timers.forEach(clearTimeout);
  }, [animate, leaves]);
  return (
    <span className="inline-flex items-center gap-0.5" aria-label={`${leaves} of 3 leaves`}>
      {[0, 1, 2].map((i) => (
        <span key={i} className={animate && i < shown ? "n-pop" : animate ? "opacity-0" : ""}>
          <Leaf size={size} filled={i < leaves} />
        </span>
      ))}
    </span>
  );
}

/** Counts up to `value` over `ms` milliseconds. */
export function CountUp({ value, ms = 1200 }: { value: number; ms?: number }) {
  const [n, setN] = useState(0);
  useEffect(() => {
    let raf = 0;
    const start = performance.now();
    const step = (now: number) => {
      const t = Math.min(1, (now - start) / ms);
      setN(Math.round(value * (1 - (1 - t) ** 3)));
      if (t < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [value, ms]);
  return <>{n.toLocaleString("en-US")}</>;
}
