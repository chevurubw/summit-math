"use client";

/** A simple line chart for mock exam scores, with an optional target line. */
export function LineChart({
  points,
  max,
  target,
  targetLabel,
}: {
  points: { label: string; value: number }[];
  max: number;
  target?: number;
  targetLabel?: string;
}) {
  const w = 640;
  const h = 240;
  const pad = { l: 40, r: 16, t: 16, b: 32 };
  const iw = w - pad.l - pad.r;
  const ih = h - pad.t - pad.b;
  const x = (i: number) => pad.l + (points.length === 1 ? iw / 2 : (i / (points.length - 1)) * iw);
  const y = (v: number) => pad.t + ih - (v / max) * ih;
  const ticks = [0, max / 2, max];
  const path = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(i)},${y(p.value)}`).join(" ");

  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="h-auto w-full" role="img" aria-label="Mock exam scores over time">
      {ticks.map((t) => (
        <g key={t}>
          <line x1={pad.l} x2={w - pad.r} y1={y(t)} y2={y(t)} stroke="var(--c-line)" />
          <text x={pad.l - 8} y={y(t) + 4} textAnchor="end" fontSize="12" fill="var(--c-muted)">
            {t}
          </text>
        </g>
      ))}
      {target !== undefined && (
        <g>
          <line x1={pad.l} x2={w - pad.r} y1={y(target)} y2={y(target)} stroke="var(--c-primary)" strokeDasharray="6 5" />
          <text x={w - pad.r} y={y(target) - 6} textAnchor="end" fontSize="12" fill="var(--c-body)">
            {targetLabel}
          </text>
        </g>
      )}
      <path d={path} fill="none" stroke="var(--c-accent)" strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" />
      {points.map((p, i) => (
        <g key={i}>
          <circle cx={x(i)} cy={y(p.value)} r="5" fill="var(--c-bg)" stroke="var(--c-accent)" strokeWidth="3">
            <title>{`${p.label}: ${p.value}`}</title>
          </circle>
          <text x={x(i)} y={h - 10} textAnchor="middle" fontSize="11" fill="var(--c-muted)">
            {p.label}
          </text>
        </g>
      ))}
    </svg>
  );
}
