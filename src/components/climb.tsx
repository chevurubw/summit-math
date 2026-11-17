"use client";

import { ArrowUpRight, Lock, LockOpen, MountainSnow, TrendingDown, TrendingUp } from "lucide-react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { AMC10_SUMMIT_HEIGHT, avatars, camps, SUMMIT_HEIGHT, themes } from "@/config/climb";
import { formatMeters, type Climb } from "@/lib/climb";
import { useApp } from "./AppProvider";
import { Avatar } from "./Avatar";
import { CountUp } from "./motion";
import { Mountain } from "./Mountain";
import { MasteryBadge, ProgressBar } from "./progress";
import { ButtonLink } from "./ui";

const lowerFirst = (s: string) => s.charAt(0).toLowerCase() + s.slice(1);

/** Altitude the student saw last time, so the climb animates from there. */
function useSeenAltitude(userId: string | undefined, altitude: number | undefined) {
  const [from, setFrom] = useState<number | null>(null);
  useEffect(() => {
    if (!userId || altitude === undefined) return;
    const key = `summit:seenAltitude:${userId}`;
    let seen = 0;
    try {
      seen = Number(localStorage.getItem(key) ?? 0) || 0;
      localStorage.setItem(key, String(altitude));
    } catch {
      // ignore storage errors
    }
    setFrom(seen);
  }, [userId, altitude]);
  return from;
}

function campProgress(climb: Climb) {
  if (!climb.nextCamp) return 1;
  return (climb.altitude - climb.camp.height) / (climb.nextCamp.height - climb.camp.height);
}

/** The big mountain panel on the Climb page. */
export function ClimbPanel() {
  const { climb, user, data } = useApp();
  const from = useSeenAltitude(user?.id, climb?.altitude);
  if (!climb || !data || from === null) return <div className="aspect-[5/6] rounded-lg border border-line bg-surface" />;

  const change = climb.altitude - from;
  const nextGate = climb.gates.find((g) => !g.met);
  const nextTheme = themes.find((t) => t.unlockAt > data.profile.bestAltitude);
  const nextAvatar = avatars.find((a) => a.unlockAt > data.profile.bestAltitude);

  return (
    <div className="overflow-hidden rounded-lg border border-line bg-surface">
      <div className="graph-paper border-b border-line px-6 pb-5 pt-6">
        <p className="text-sm font-semibold text-muted">Your altitude</p>
        <p className="mt-1 font-display text-5xl font-extrabold text-heading sm:text-6xl">
          <CountUp value={climb.altitude} duration={1800} />
          <span className="ml-2 text-2xl font-bold text-muted">m</span>
        </p>
        <p className="mt-2 text-body">
          <span className="font-semibold text-heading">{climb.camp.name}.</span> {climb.camp.note}
        </p>
        {change !== 0 && (
          <p className={`anim-slide mt-3 flex items-center gap-2 text-sm font-semibold ${change > 0 ? "text-correct" : "text-wrong"}`}>
            {change > 0 ? <TrendingUp className="h-4 w-4" aria-hidden /> : <TrendingDown className="h-4 w-4" aria-hidden />}
            {change > 0
              ? `You climbed ${formatMeters(change)} since your last visit.`
              : `You slipped ${formatMeters(-change)} since your last visit. A quiz or test showed a skill needs review.`}
          </p>
        )}
      </div>

      <div className="relative px-2 pt-2 sm:px-6">
        <Mountain altitude={climb.altitude} from={from} gates={climb.gates} />
      </div>

      <div className="space-y-6 border-t border-line px-6 py-6">
        {climb.nextCamp && (
          <div>
            <div className="mb-2 flex justify-between gap-3 text-sm">
              <span className="text-body">
                Next: <span className="font-semibold text-heading">{climb.nextCamp.name}</span>
              </span>
              <span className="tabular-nums text-muted">{formatMeters(climb.nextCamp.height - climb.altitude)} to go</span>
            </div>
            <ProgressBar value={campProgress(climb)} color="primary" />
          </div>
        )}

        <div className="grid grid-cols-2 gap-3">
          {[
            { name: "AMC 10 Summit", height: AMC10_SUMMIT_HEIGHT, note: "Core skills" },
            { name: "AMC 12 Summit", height: SUMMIT_HEIGHT, note: "Core plus AMC 12 only skills" },
          ].map((peak) => {
            const done = climb.altitude >= peak.height;
            return (
              <div key={peak.name} className={`rounded-md border p-3 ${done ? "border-accent/60 bg-accent/10" : "border-line bg-surface-2"}`}>
                <p className="font-display font-bold text-heading">{peak.name}</p>
                <p className="text-xs text-muted">{peak.note}</p>
                <p className="mt-2 text-sm tabular-nums text-body">
                  {done ? "Reached" : `${formatMeters(Math.max(0, peak.height - climb.altitude))} to go`}
                </p>
              </div>
            );
          })}
        </div>

        {climb.blockedBy ? (
          <div className="rounded-md border border-primary/60 bg-primary/10 p-4">
            <p className="flex items-center gap-2 font-display font-bold text-heading">
              <Lock className="h-4 w-4" aria-hidden /> Checkpoint at {formatMeters(climb.blockedBy.height)}
            </p>
            <p className="mt-1 text-sm text-body">
              Your skills would put you at {formatMeters(climb.earned)}, but you need to prove it first. {climb.blockedBy.label}.{" "}
              {climb.blockedBy.progress}.
            </p>
            <ButtonLink href="/mock" size="sm" className="mt-3">
              Take a mock exam
            </ButtonLink>
          </div>
        ) : (
          nextGate && (
            <p className="flex items-start gap-2 text-sm text-muted">
              <Lock className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />
              Next checkpoint at {formatMeters(nextGate.height)}: {lowerFirst(nextGate.label)}. {nextGate.progress}.
            </p>
          )
        )}

        {climb.suggestions.length > 0 && (
          <div>
            <h3 className="font-display text-lg font-bold">Your next steps up</h3>
            <p className="text-sm text-muted">The skills that would lift you the most right now.</p>
            <ul className="mt-3 divide-y divide-line rounded-md border border-line">
              {climb.suggestions.map((s) => (
                <li key={s.skillId}>
                  <Link href={`/learn/${s.unitId}/${s.skillId}`} className="group flex items-center gap-3 px-4 py-3 hover:bg-surface-2">
                    <span className="min-w-0 flex-1">
                      <span className="block truncate font-semibold text-heading group-hover:underline">
                        {s.review && <span className="mr-2 text-xs font-bold text-primary">Review</span>}
                        {s.title}
                      </span>
                      <span className="mt-1 flex items-center gap-2">
                        <MasteryBadge level={s.from} compact />
                        <span className="text-xs text-muted">to</span>
                        <MasteryBadge level={s.to} />
                      </span>
                    </span>
                    <span className="font-display font-bold tabular-nums text-correct">+{formatMeters(s.gain)}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}

        {(nextTheme || nextAvatar) && (
          <div className="flex flex-wrap items-center gap-4 text-sm">
            <span className="text-muted">Coming up:</span>
            {nextTheme && (
              <span className="flex items-center gap-2 text-body">
                <span className="flex" aria-hidden>
                  <span className="h-4 w-4 rounded-full border-2 border-bg" style={{ background: nextTheme.swatch[0] }} />
                  <span className="-ml-1.5 h-4 w-4 rounded-full border-2 border-bg" style={{ background: nextTheme.swatch[1] }} />
                </span>
                {nextTheme.name} at {formatMeters(nextTheme.unlockAt)}
              </span>
            )}
            {nextAvatar && (
              <span className="flex items-center gap-2 text-body">
                <Avatar id={nextAvatar.id} name="" size={20} />
                {nextAvatar.name} at {formatMeters(nextAvatar.unlockAt)}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/** The altitude chip in the header. Click it to watch the climb and see what is next. */
export function ClimbWidget() {
  const { climb } = useApp();
  const [open, setOpen] = useState(false);
  const [plays, setPlays] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const close = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    const esc = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    document.addEventListener("mousedown", close);
    document.addEventListener("keydown", esc);
    return () => {
      document.removeEventListener("mousedown", close);
      document.removeEventListener("keydown", esc);
    };
  }, []);

  if (!climb) return null;
  const startFrom = Math.max(0, (camps.filter((c) => c.height < climb.altitude).slice(-2)[0]?.height ?? 0));

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        onClick={() => {
          setOpen((o) => !o);
          setPlays((p) => p + 1);
        }}
        aria-expanded={open}
        aria-haspopup="dialog"
        className="btn-press inline-flex items-center gap-1.5 whitespace-nowrap rounded-md border border-line bg-surface px-2.5 py-1.5 text-sm font-semibold text-heading shadow-[0_2px_0_0_#050507] hover:border-muted"
      >
        <MountainSnow className="h-4 w-4 text-accent-soft" aria-hidden />
        <span className="tabular-nums">{formatMeters(climb.altitude)}</span>
        {climb.blockedBy && <Lock className="h-3.5 w-3.5 text-primary" aria-label="Checkpoint locked" />}
      </button>

      {open && (
        <div role="dialog" aria-label="Your climb" className="anim-drop absolute right-0 z-50 mt-2 w-[min(22rem,calc(100vw-2rem))] overflow-hidden rounded-lg border border-line bg-surface shadow-2xl">
          <div className="flex items-start justify-between gap-3 px-5 pt-4">
            <div>
              <p className="font-display text-2xl font-extrabold text-heading">{formatMeters(climb.altitude)}</p>
              <p className="text-sm text-body">{climb.camp.name}</p>
            </div>
            {climb.nextCamp && (
              <p className="text-right text-xs text-muted">
                {formatMeters(climb.nextCamp.height - climb.altitude)} to
                <br />
                <span className="font-semibold text-heading">{climb.nextCamp.name}</span>
              </p>
            )}
          </div>
          <div className="px-6">
            <Mountain key={plays} altitude={climb.altitude} from={startFrom} gates={climb.gates} compact duration={1500} />
          </div>
          <div className="space-y-3 border-t border-line px-5 py-4">
            {climb.blockedBy ? (
              <p className="flex items-start gap-2 text-sm text-body">
                <Lock className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden />
                Checkpoint: {lowerFirst(climb.blockedBy.label)} to keep climbing. {climb.blockedBy.progress}.
              </p>
            ) : climb.suggestions[0] ? (
              <p className="flex items-start gap-2 text-sm text-body">
                <LockOpen className="mt-0.5 h-4 w-4 shrink-0 text-correct" aria-hidden />
                Next step: level up {climb.suggestions[0].title} for +{formatMeters(climb.suggestions[0].gain)}.
              </p>
            ) : null}
            <Link
              href="/climb"
              onClick={() => setOpen(false)}
              className="inline-flex items-center gap-1 text-sm font-semibold text-accent-soft hover:underline"
            >
              Open your climb <ArrowUpRight className="h-4 w-4" aria-hidden />
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
