"use client";

import { useEffect, useMemo, useState } from "react";
import { camps, SUMMIT_HEIGHT } from "@/config/climb";
import type { GateStatus } from "@/lib/climb";
import { useReducedMotion } from "./motion";

const W = 600;
const H = 720;
const BASE_Y = 670;
const TOP_Y = 70;

const yAt = (alt: number) => BASE_Y - (alt / SUMMIT_HEIGHT) * (BASE_Y - TOP_Y);
// Half the mountain's width at a given altitude
const halfWidth = (alt: number) => 255 * (1 - alt / SUMMIT_HEIGHT) + 12;

// The trail zigzags up the mountain, with a switchback at every camp
const trail = camps.map((c, i) => ({
  alt: c.height,
  x: i === camps.length - 1 ? W / 2 : W / 2 + (i % 2 ? 1 : -1) * halfWidth(c.height) * 0.55,
  y: yAt(c.height),
}));

// The AMC 10 Summit is a ledge across the mountain face
const amc10Camp = camps.find((c) => c.peak === "amc10");

const segLengths = trail.slice(1).map((p, i) => Math.hypot(p.x - trail[i].x, p.y - trail[i].y));
const totalLength = segLengths.reduce((a, b) => a + b, 0);

function pointAt(alt: number) {
  const a = Math.max(0, Math.min(SUMMIT_HEIGHT, alt));
  let len = 0;
  for (let i = 1; i < trail.length; i++) {
    const p0 = trail[i - 1];
    const p1 = trail[i];
    if (a <= p1.alt || i === trail.length - 1) {
      const t = p1.alt === p0.alt ? 1 : Math.max(0, Math.min(1, (a - p0.alt) / (p1.alt - p0.alt)));
      return { x: p0.x + (p1.x - p0.x) * t, y: p0.y + (p1.y - p0.y) * t, len: len + segLengths[i - 1] * t };
    }
    len += segLengths[i - 1];
  }
  return { x: trail[0].x, y: trail[0].y, len: 0 };
}

const trailPath = trail.map((p, i) => `${i ? "L" : "M"}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" ");

const stars = Array.from({ length: 28 }, (_, i) => ({
  x: (i * 211) % W,
  y: 20 + ((i * 97) % 260),
  r: (i % 3) * 0.5 + 0.6,
}));

/** Animates a number from `from` to `to`. */
function useClimbAnimation(from: number, to: number, duration: number, play: boolean) {
  const reduced = useReducedMotion();
  const [value, setValue] = useState(play ? from : to);
  useEffect(() => {
    if (reduced || !play) {
      setValue(to);
      return;
    }
    let raf = 0;
    const start = performance.now() + 250;
    setValue(from);
    const tick = (now: number) => {
      const t = Math.max(0, Math.min(1, (now - start) / duration));
      const eased = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      setValue(from + (to - from) * eased);
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [from, to, duration, play, reduced]);
  return value;
}

/**
 * The mountain illustration. The climber walks up the trail from `from` to `altitude`.
 * Camps light up as they are reached. Mock exam gates show a lock until their requirement is met ("Unlocked"),
 * and say "Passed" once the climber is above them.
 */
export function Mountain({
  altitude,
  from = 0,
  gates,
  compact = false,
  play = true,
  duration = 1800,
  onDone,
}: {
  altitude: number;
  from?: number;
  gates: GateStatus[];
  compact?: boolean;
  play?: boolean;
  duration?: number;
  onDone?: () => void;
}) {
  const shown = useClimbAnimation(from, altitude, duration, play);
  const climber = pointAt(shown);
  const done = Math.abs(shown - altitude) < 1;

  useEffect(() => {
    if (done) onDone?.();
  }, [done, onDone]);

  const mountain = useMemo(() => {
    // Left and right ridgelines with a few rocky bumps
    const left: string[] = [];
    const right: string[] = [];
    for (let a = 0; a <= SUMMIT_HEIGHT; a += 500) {
      const bump = ((a / 500) % 3 === 1 ? 14 : (a / 500) % 3 === 2 ? -8 : 0) * (1 - a / SUMMIT_HEIGHT);
      left.push(`${(W / 2 - halfWidth(a) - 18 - bump).toFixed(1)},${(yAt(a) + 20).toFixed(1)}`);
      right.unshift(`${(W / 2 + halfWidth(a) + 18 + bump * 0.6).toFixed(1)},${(yAt(a) + 20).toFixed(1)}`);
    }
    return [`0,${H}`, ...left, `${W / 2},${TOP_Y - 18}`, ...right, `${W},${H}`].join(" ");
  }, []);

  const fs = compact ? 20 : 15;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full" role="img" aria-label={`Mountain climb at ${Math.round(altitude)} meters`}>
      <defs>
        <linearGradient id="mtn-face" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="var(--c-surface-2)" />
          <stop offset="1" stopColor="var(--c-surface)" />
        </linearGradient>
      </defs>

      {/* Night sky */}
      {stars.map((s, i) => (
        <circle key={i} cx={s.x} cy={s.y} r={s.r} fill="#fff" opacity={0.25} />
      ))}

      {/* Back range */}
      <polygon points={`0,${H} 0,360 90,250 160,330 230,290 300,420 400,230 470,300 540,200 ${W},280 ${W},${H}`} fill="var(--c-surface)" opacity="0.55" />

      {/* Main mountain */}
      <polygon points={mountain} fill="url(#mtn-face)" stroke="var(--c-line)" strokeWidth="2" />
      {/* Snow cap */}
      <polygon
        points={`${W / 2},${TOP_Y - 18} 268,120 280,128 255,160 286,150 300,172 316,148 342,165 326,126 336,118`}
        fill="#ffffff"
        opacity="0.85"
      />

      {/* Clouds at Cloud Pass */}
      <g opacity="0.07" fill="#fff">
        <ellipse cx="110" cy={yAt(5300)} rx="120" ry="16" />
        <ellipse cx="470" cy={yAt(5000)} rx="140" ry="14" />
      </g>

      {/* AMC 10 Summit ledge: a band across the mountain face */}
      {amc10Camp && (
        <g>
          <line
            x1={W / 2 - halfWidth(amc10Camp.height) - 16}
            x2={W / 2 + halfWidth(amc10Camp.height) + 16}
            y1={yAt(amc10Camp.height) + 12}
            y2={yAt(amc10Camp.height) + 12}
            stroke="var(--c-accent)"
            strokeOpacity="0.55"
            strokeWidth="2"
            strokeDasharray="6 6"
          />
        </g>
      )}

      {/* Altitude scale */}
      {!compact &&
        [0, 2000, 4000, 6000, 8000, 10000].map((a) => (
          <g key={a}>
            <line x1="8" x2="26" y1={yAt(a)} y2={yAt(a)} stroke="var(--c-muted)" opacity="0.5" />
            <text x="8" y={yAt(a) - 6} fontSize="12" fill="var(--c-muted)">
              {a.toLocaleString("en-US")} m
            </text>
          </g>
        ))}

      {/* Trail: dashed ahead, solid behind the climber */}
      <path d={trailPath} fill="none" stroke="var(--c-muted)" strokeOpacity="0.45" strokeWidth="3" strokeDasharray="2 9" strokeLinecap="round" />
      <path
        d={trailPath}
        fill="none"
        stroke="var(--c-primary)"
        strokeWidth="5"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={totalLength}
        strokeDashoffset={totalLength - climber.len}
      />

      {/* Camps */}
      {trail.map((p, i) => {
        const camp = camps[i];
        const reached = shown >= camp.height - 0.5;
        const labelRight = p.x <= W / 2;
        const isSummit = i === camps.length - 1;
        const isPeak = !!camp.peak;
        return (
          <g key={camp.name}>
            {isPeak && (
              // A flag planted on each summit
              <g>
                <line x1={p.x} y1={p.y} x2={p.x} y2={p.y - 34} stroke={reached ? "#fff" : "var(--c-muted)"} strokeWidth="2.5" strokeLinecap="round" />
                <path
                  d={`M ${p.x} ${p.y - 34} L ${p.x + 18} ${p.y - 28} L ${p.x} ${p.y - 21} Z`}
                  fill={reached ? (camp.peak === "amc12" ? "var(--c-primary)" : "var(--c-accent)") : "var(--c-line)"}
                />
              </g>
            )}
            <circle cx={p.x} cy={p.y} r={compact ? 11 : 9} fill="var(--c-bg)" stroke={reached ? "var(--c-accent)" : "var(--c-muted)"} strokeWidth="3" />
            {reached && (
              <circle
                key={`f${camp.name}`}
                cx={p.x}
                cy={p.y}
                r={compact ? 7 : 5.5}
                fill="var(--c-accent)"
                className="anim-bubble"
                style={{ transformOrigin: "center", transformBox: "fill-box" }}
              />
            )}
            {(!compact || isPeak) && (
              <text
                x={isSummit ? p.x : labelRight ? p.x + 18 : p.x - 18}
                y={isSummit ? p.y - 42 : p.y + 5}
                textAnchor={isSummit ? "middle" : labelRight ? "start" : "end"}
                fontSize={fs}
                fontWeight="700"
                fill={reached ? "var(--c-heading)" : "var(--c-muted)"}
                stroke="var(--c-bg)"
                strokeWidth="4"
                paintOrder="stroke"
                style={{ fontFamily: "var(--font-display)" }}
              >
                {camp.name}
                {!compact && !isSummit && (
                  <tspan fontWeight="400" fill="var(--c-muted)">
                    {"  "}
                    {camp.height.toLocaleString("en-US")} m
                  </tspan>
                )}
              </text>
            )}
          </g>
        );
      })}

      {/* Mock exam gates */}
      {gates.map((g) => {
        // Sit the lock beside the camp it guards, on the side away from the camp's name
        const camp = pointAt(g.height);
        const left = camp.x <= W / 2; // camp name is on the right, so the lock goes left
        const x = camp.x + (left ? -32 : 32);
        return (
          <g key={g.height} transform={`translate(${x} ${camp.y})`}>
            <g className={g.met ? "" : "lock-pulse"}>
              <rect x="-13" y="-12" width="26" height="24" rx="6" fill={g.met ? "var(--c-correct)" : "var(--c-primary)"} />
              {/* lock */}
              <rect x="-6" y="-2" width="12" height="9" rx="1.5" fill="#fff" />
              <path d={g.met ? "M -4 -2 v -4 a 4 4 0 0 1 8 0" : "M -4 -2 v -3 a 4 4 0 0 1 8 0 v 3"} stroke="#fff" strokeWidth="2" fill="none" />
            </g>
            {!compact && (
              <text x={left ? -20 : 20} y="5" textAnchor={left ? "end" : "start"} fontSize="12.5" fill={g.met ? "var(--c-correct)" : "var(--c-body)"} stroke="var(--c-bg)" strokeWidth="4" paintOrder="stroke">
                {g.met
                  ? altitude >= g.height
                    ? "Passed"
                    : "Unlocked"
                  : g.kind === "mockTaken"
                    ? "Take a mock exam"
                    : `${g.track === "amc10" ? "AMC 10 " : g.track === "amc12" ? "AMC 12 " : ""}mock ${g.min}+${g.times ? ` (${g.times} of ${g.ofLast})` : ""}`}
              </text>
            )}
          </g>
        );
      })}

      {/* Climber with a little flag */}
      <g transform={`translate(${climber.x} ${climber.y})`}>
        <circle r="18" fill="var(--c-accent)" opacity="0.18">
          <animate attributeName="r" values="14;22;14" dur="2.4s" repeatCount="indefinite" />
        </circle>
        <line x1="0" y1="-8" x2="0" y2="-38" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" />
        <path d="M 0 -38 L 20 -32 L 0 -25 Z" fill="var(--c-primary)" />
        <circle r="9" fill="var(--c-accent)" stroke="#fff" strokeWidth="3" />
      </g>
    </svg>
  );
}
