"use client";

import { useEffect, useState } from "react";

/** True when the visitor's system asks for less motion. */
export function useReducedMotion() {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduced(mq.matches);
    update();
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, []);
  return reduced;
}

/** Counts a number up from 0 when it first appears. */
export function useCountUp(target: number, duration = 900) {
  const reduced = useReducedMotion();
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (reduced) {
      setValue(target);
      return;
    }
    let raf = 0;
    const start = performance.now();
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      setValue(target * eased);
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, duration, reduced]);
  return value;
}

export function CountUp({ value, decimals = 0, duration }: { value: number; decimals?: number; duration?: number }) {
  const v = useCountUp(value, duration);
  const shown = decimals
    ? v.toFixed(decimals).replace(/\.0+$/, "")
    : Math.round(v).toLocaleString("en-US");
  return (
    <span className="tabular-nums" aria-label={String(value)}>
      {shown}
    </span>
  );
}

/** Small bubbles that fly outward. Place inside a relatively positioned element. */
export function Burst({ count = 10, distance = 46, colors = ["var(--c-correct)", "var(--c-accent-soft)", "#ffffff"] }: {
  count?: number;
  distance?: number;
  colors?: string[];
}) {
  return (
    <span aria-hidden className="pointer-events-none absolute inset-0">
      {Array.from({ length: count }, (_, i) => {
        const angle = (i / count) * Math.PI * 2 + (i % 2) * 0.3;
        const d = distance * (0.7 + ((i * 37) % 10) / 25);
        const size = 4 + ((i * 13) % 4);
        return (
          <span
            key={i}
            className="burst-dot"
            style={
              {
                width: size,
                height: size,
                background: colors[i % colors.length],
                "--dx": `${Math.cos(angle) * d}px`,
                "--dy": `${Math.sin(angle) * d}px`,
                animationDelay: `${(i % 3) * 30}ms`,
              } as React.CSSProperties
            }
          />
        );
      })}
    </span>
  );
}

/** A check mark or X that draws itself like a pen stroke. */
export function PenMark({ kind, className = "" }: { kind: "check" | "x"; className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      {kind === "check" ? (
        <path d="M4 12.5 L9.5 18 L20 6" className="anim-draw" style={{ "--len": 30 } as React.CSSProperties} />
      ) : (
        <>
          <path d="M6 6 L18 18" className="anim-draw" style={{ "--len": 18 } as React.CSSProperties} />
          <path d="M18 6 L6 18" className="anim-draw" style={{ "--len": 18, animationDelay: "120ms" } as React.CSSProperties} />
        </>
      )}
    </svg>
  );
}
