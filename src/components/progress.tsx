"use client";

import { useEffect, useState } from "react";
import { MASTERY_LABELS, MASTERY_LEVELS, type MasteryLevel } from "@/config/mastery";

const levelBg: Record<MasteryLevel, string> = {
  not_started: "bg-level-0",
  attempted: "bg-level-1",
  familiar: "bg-level-2",
  proficient: "bg-level-3",
  mastered: "bg-level-4",
};

/**
 * A skill's mastery level, drawn as four answer sheet bubbles.
 * Each level fills one more bubble. Set animate to fill them one by one.
 */
export function MasteryBadge({ level, compact = false, animate = false }: { level: MasteryLevel; compact?: boolean; animate?: boolean }) {
  const rank = MASTERY_LEVELS.indexOf(level);
  return (
    <span className="inline-flex items-center gap-2 whitespace-nowrap text-xs font-semibold text-body" title={MASTERY_LABELS[level]}>
      <span className="flex gap-[3px]" aria-hidden>
        {MASTERY_LEVELS.slice(1).map((l, i) => (
          <span key={l} className="relative h-3 w-3 rounded-full border border-level-1/70">
            {i < rank && (
              <span
                className={`absolute -inset-px rounded-full ${levelBg[level]} ${animate ? "anim-bubble" : ""}`}
                style={animate ? { animationDelay: `${200 + i * 120}ms` } : undefined}
              />
            )}
          </span>
        ))}
      </span>
      {compact ? <span className="sr-only">{MASTERY_LABELS[level]}</span> : MASTERY_LABELS[level]}
    </span>
  );
}

export function MasteryLegend() {
  return (
    <div className="flex flex-wrap gap-x-5 gap-y-2">
      {MASTERY_LEVELS.map((l) => (
        <MasteryBadge key={l} level={l} />
      ))}
    </div>
  );
}

/** Starts at 0 and animates to the real value after the first paint. */
function useGrow(value: number) {
  const [shown, setShown] = useState(0);
  useEffect(() => {
    const id = requestAnimationFrame(() => setShown(value));
    return () => cancelAnimationFrame(id);
  }, [value]);
  return shown;
}

/** A circular progress indicator. value is between 0 and 1. */
export function ProgressRing({
  value,
  size = 64,
  stroke = 7,
  label,
}: {
  value: number;
  size?: number;
  stroke?: number;
  label?: string;
}) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const v = Math.max(0, Math.min(1, value));
  const shown = useGrow(v);
  return (
    <div className="relative inline-grid place-items-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90" role="img" aria-label={`${Math.round(v * 100)} percent`}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--c-line)" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="var(--c-accent)"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - shown)}
          style={{ transition: "stroke-dashoffset 1100ms cubic-bezier(0.2, 0.8, 0.2, 1)" }}
        />
      </svg>
      <span className="absolute font-display font-bold text-heading" style={{ fontSize: size * 0.24 }}>
        {label ?? `${Math.round(v * 100)}%`}
      </span>
    </div>
  );
}

export function ProgressBar({ value, color = "accent", className = "" }: { value: number; color?: "accent" | "primary"; className?: string }) {
  const v = Math.max(0, Math.min(1, value));
  const shown = useGrow(v);
  return (
    <div className={`h-2 w-full overflow-hidden rounded-full bg-line ${className}`} role="progressbar" aria-valuenow={Math.round(v * 100)} aria-valuemin={0} aria-valuemax={100}>
      <div
        className={`h-full rounded-full ${color === "accent" ? "bg-accent" : "bg-primary"}`}
        style={{ width: `${shown * 100}%`, transition: "width 700ms cubic-bezier(0.2, 0.8, 0.2, 1)" }}
      />
    </div>
  );
}
