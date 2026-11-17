"use client";

import { Clock } from "lucide-react";
import { useEffect, useState } from "react";

/** Countdown timer. Calls onExpire once when time runs out. */
export function Timer({ endsAt, onExpire }: { endsAt: number; onExpire: () => void }) {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const remaining = Math.max(0, endsAt - now);
  useEffect(() => {
    if (remaining === 0) onExpire();
  }, [remaining, onExpire]);

  const mins = Math.floor(remaining / 60000);
  const secs = Math.floor((remaining % 60000) / 1000);
  const low = remaining < 5 * 60000;

  return (
    <div
      className={`inline-flex items-center gap-2 rounded-lg border px-3 py-1.5 font-display text-lg font-bold tabular-nums ${
        low ? "anim-pulse-red border-primary bg-primary/15 text-heading" : "border-line bg-surface-2 text-heading"
      }`}
      role="timer"
      aria-label={`${mins} minutes ${secs} seconds left`}
    >
      <Clock className="h-4 w-4" aria-hidden />
      {String(mins).padStart(2, "0")}:{String(secs).padStart(2, "0")}
    </div>
  );
}
