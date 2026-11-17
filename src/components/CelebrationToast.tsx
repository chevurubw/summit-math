"use client";

import { Check, X } from "lucide-react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { avatars, themes, type AvatarId, type ThemeId } from "@/config/climb";
import { formatMeters } from "@/lib/climb";
import { useApp } from "./AppProvider";
import { Avatar } from "./Avatar";
import { Burst } from "./motion";

/** Counts up to a number once, for the altitude readout. */
function useCountUp(target: number, ms = 1100) {
  // Starts at the final number when the student prefers less motion
  const [still] = useState(() => typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  const [v, setV] = useState(still ? target : 0);
  useEffect(() => {
    if (still) return;
    let raf = 0;
    const start = performance.now();
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / ms);
      setV(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, ms, still]);
  return still ? target : v;
}

/**
 * Opens when a student reaches a new camp or unlocks a reward.
 * Shows each unlock with a preview and lets them switch to it on the spot.
 */
export function CelebrationToast() {
  const { celebration, dismissCelebration } = useApp();
  if (!celebration) return null;
  return <UnlockDialog key={celebration.id} onClose={dismissCelebration} />;
}

function UnlockDialog({ onClose }: { onClose: () => void }) {
  const { celebration, data, updateProfile } = useApp();
  const meters = useCountUp(celebration?.altitude ?? 0);
  const primary = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    primary.current?.focus();
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  if (!celebration || !data) return null;
  const { camp } = celebration;
  const newThemes = themes.filter((t) => celebration.themes.includes(t.id));
  const newAvatars = avatars.filter((a) => celebration.avatars.includes(a.id));
  const hasUnlocks = newThemes.length + newAvatars.length > 0;
  const name = data.profile.displayName ?? "";

  return (
    <div className="fixed inset-0 z-[70] grid place-items-center p-4" role="dialog" aria-modal="true" aria-labelledby="unlock-title">
      <button type="button" aria-label="Close" onClick={onClose} className="anim-backdrop absolute inset-0 cursor-default bg-black/70 backdrop-blur-sm" />

      <div className="anim-level-up relative w-full max-w-md overflow-hidden rounded-xl border border-accent/40 bg-surface shadow-2xl">
        <button type="button" onClick={onClose} className="absolute right-3 top-3 z-10 grid h-8 w-8 place-items-center rounded-md text-muted hover:text-heading" aria-label="Close">
          <X className="h-4 w-4" />
        </button>

        {/* The ridge draws itself and a flag lands on the new camp */}
        <div className="relative h-28 bg-gradient-to-b from-accent/15 to-transparent">
          <svg viewBox="0 0 400 112" className="absolute inset-0 h-full w-full" preserveAspectRatio="none" aria-hidden>
            <path
              className="anim-ridge"
              pathLength={1}
              d="M0 104 L70 78 L112 88 L170 50 L212 62 L262 26 L300 40 L400 8"
              fill="none"
              stroke="var(--c-accent)"
              strokeWidth="3"
              strokeLinejoin="round"
            />
            <g className="anim-flag">
              <line x1="262" y1="26" x2="262" y2="2" stroke="var(--c-heading)" strokeWidth="2" />
              <path d="M262 3 L280 8 L262 13 Z" fill="var(--c-primary)" />
            </g>
          </svg>
          <span className="absolute left-[65.5%] top-[23%]">
            <Burst count={16} distance={54} colors={["var(--c-accent)", "var(--c-primary)", "#ffffff"]} />
          </span>
          <p className="absolute left-5 top-4 font-display text-sm font-semibold tabular-nums text-accent-soft">{formatMeters(meters)}</p>
        </div>

        <div className="px-5 pb-5">
          <h2 id="unlock-title" className="font-display text-2xl font-bold text-heading">
            {camp ? `You reached ${camp.name}` : "New unlock"}
          </h2>
          {camp && <p className="mt-1 text-sm text-body">{camp.note}</p>}

          {hasUnlocks && (
            <ul className="mt-5 space-y-2.5">
              {newThemes.map((t, i) => (
                <UnlockRow
                  key={t.id}
                  delay={1100 + i * 120}
                  preview={<ThemePreview swatch={t.swatch} />}
                  label={t.name}
                  kind="Color scheme"
                  active={data.profile.theme === t.id}
                  onUse={() => updateProfile({ theme: t.id as ThemeId })}
                />
              ))}
              {newAvatars.map((a, i) => (
                <UnlockRow
                  key={a.id}
                  delay={1100 + (newThemes.length + i) * 120}
                  preview={<Avatar id={a.id as AvatarId} name={name} size={40} />}
                  label={a.name}
                  kind="Profile icon"
                  active={data.profile.avatar === a.id}
                  onUse={() => updateProfile({ avatar: a.id as AvatarId })}
                />
              ))}
            </ul>
          )}

          {hasUnlocks && (
            <p className="mt-3 text-xs text-muted">
              Not now? You can switch anytime in{" "}
              <Link href="/settings" onClick={onClose} className="underline decoration-dotted underline-offset-2 hover:text-body">
                Settings
              </Link>
              .
            </p>
          )}

          <div className="mt-5 flex items-center gap-3">
            <button ref={primary} type="button" onClick={onClose} className="flex-1 rounded-md bg-primary px-4 py-2.5 font-semibold text-white hover:brightness-110">
              Keep climbing
            </button>
            <Link href="/climb" onClick={onClose} className="rounded-md px-3 py-2.5 text-sm font-semibold text-accent-soft hover:underline">
              See the mountain
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

function UnlockRow({
  preview,
  label,
  kind,
  active,
  onUse,
  delay,
}: {
  preview: React.ReactNode;
  label: string;
  kind: string;
  active: boolean;
  onUse: () => Promise<unknown> | void;
  delay: number;
}) {
  const [busy, setBusy] = useState(false);
  return (
    <li className="anim-card-rise flex items-center gap-3 rounded-lg border border-line bg-surface-2 p-3" style={{ animationDelay: `${delay}ms` }}>
      {preview}
      <div className="min-w-0 flex-1">
        <p className="font-semibold text-heading">{label}</p>
        <p className="text-xs text-muted">{kind}</p>
      </div>
      {active ? (
        <span className="anim-pop inline-flex items-center gap-1 rounded-md px-3 py-1.5 text-sm font-semibold text-correct">
          <Check className="h-4 w-4" aria-hidden /> In use
        </span>
      ) : (
        <button
          type="button"
          disabled={busy}
          onClick={async () => {
            setBusy(true);
            try {
              await onUse();
            } finally {
              setBusy(false);
            }
          }}
          className="rounded-md border border-accent/60 px-3 py-1.5 text-sm font-semibold text-heading transition hover:bg-accent hover:text-white disabled:opacity-60"
        >
          Use this
        </button>
      )}
    </li>
  );
}

/** A tiny page mockup painted in the scheme's two colors. */
function ThemePreview({ swatch }: { swatch: [string, string] }) {
  const [main, accent] = swatch;
  return (
    <span className="relative block h-10 w-10 shrink-0 overflow-hidden rounded-md border border-line bg-[#0f0f10]" aria-hidden>
      <span className="absolute inset-x-0 top-0 h-2.5" style={{ background: main }} />
      <span className="absolute left-1.5 top-4 h-1.5 w-5 rounded-full" style={{ background: accent }} />
      <span className="absolute bottom-1.5 left-1.5 h-2 w-4 rounded-sm" style={{ background: main }} />
    </span>
  );
}
