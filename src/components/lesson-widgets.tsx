"use client";

import katex from "katex";
import { Check as CheckIcon, ChevronRight, Pause, Play, RotateCcw, X } from "lucide-react";
import { Children, isValidElement, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { compile, evaluate, fill } from "@/lib/expr";

/* ------------------------------------------------------------------
   Shared helpers
------------------------------------------------------------------- */

const PALETTE: Record<string, string> = {
  accent: "var(--c-accent-soft)",
  primary: "var(--c-primary)",
  correct: "var(--c-correct)",
  wrong: "var(--c-wrong)",
  muted: "var(--c-muted)",
  heading: "var(--c-heading)",
  body: "var(--c-body)",
  blue: "#60a5fa",
  amber: "#fbbf24",
  teal: "#2dd4bf",
  pink: "#f472b6",
};
/** Round SVG coordinates so server and browser trig agree to the last digit (avoids hydration mismatches). */
const r2 = (v: number) => Math.round(v * 100) / 100;

const color = (c?: string, fallback = "accent") => PALETTE[c ?? fallback] ?? c ?? PALETTE[fallback];

/** Renders text that may contain $inline math$. */
export function MathText({ text, className }: { text: string; className?: string }) {
  const html = useMemo(() => renderInline(text), [text]);
  return <span className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}

function renderInline(text: string): string {
  return text
    .split(/(\$[^$]+\$)/g)
    .map((part) => {
      if (part.startsWith("$") && part.endsWith("$") && part.length > 1) {
        try {
          return katex.renderToString(part.slice(1, -1), { throwOnError: false });
        } catch {
          return part;
        }
      }
      return part.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c] as string);
    })
    .join("");
}

function Tex({ tex, display = false }: { tex: string; display?: boolean }) {
  const html = useMemo(() => katex.renderToString(tex, { throwOnError: false, displayMode: display }), [tex, display]);
  return <span dangerouslySetInnerHTML={{ __html: html }} />;
}

function usePrefersReducedMotion() {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const m = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(m.matches);
    const on = () => setReduced(m.matches);
    m.addEventListener("change", on);
    return () => m.removeEventListener("change", on);
  }, []);
  return reduced;
}

function Panel({ children, caption }: { children: ReactNode; caption?: string }) {
  return (
    <figure className="not-prose my-7 overflow-hidden rounded-lg border border-line bg-surface">
      {children}
      {caption && (
        <figcaption className="border-t border-line px-4 py-2.5 text-sm text-muted">
          <MathText text={caption} />
        </figcaption>
      )}
    </figure>
  );
}

function SmallButton({ onClick, children, label, active }: { onClick: () => void; children: ReactNode; label?: string; active?: boolean }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      aria-pressed={active}
      className={`inline-flex items-center gap-1.5 rounded-md border px-3 py-1.5 text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${
        active ? "border-accent bg-accent/20 text-heading" : "border-line bg-surface-2 text-body hover:text-heading"
      }`}
    >
      {children}
    </button>
  );
}

/* ------------------------------------------------------------------
   Sliders shared by Figure and other widgets
------------------------------------------------------------------- */

export type Param = { name: string; min: number; max: number; step?: number; value: number; label?: string; play?: boolean; speed?: number };

function useParams(params: Param[] = []) {
  const [values, setValues] = useState<Record<string, number>>(() => Object.fromEntries(params.map((p) => [p.name, p.value])));
  const [playing, setPlaying] = useState(false);
  const raf = useRef<number | null>(null);
  const playable = params.find((p) => p.play);

  useEffect(() => {
    if (!playing || !playable) return;
    let last = performance.now();
    const span = playable.max - playable.min;
    const perSecond = span / (playable.speed ?? 6);
    const tick = (now: number) => {
      const dt = (now - last) / 1000;
      last = now;
      setValues((v) => {
        let next = v[playable.name] + perSecond * dt;
        if (next > playable.max) next = playable.min + (next - playable.max);
        return { ...v, [playable.name]: next };
      });
      raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => {
      if (raf.current) cancelAnimationFrame(raf.current);
    };
  }, [playing, playable]);

  const reset = () => {
    setPlaying(false);
    setValues(Object.fromEntries(params.map((p) => [p.name, p.value])));
  };
  return { values, setValues, playing, setPlaying, playable, reset };
}

function Controls({
  params,
  state,
}: {
  params: Param[];
  state: ReturnType<typeof useParams>;
}) {
  if (!params.length) return null;
  const { values, setValues, playing, setPlaying, playable, reset } = state;
  return (
    <div className="flex flex-col gap-3 border-t border-line bg-surface-2/50 px-4 py-3">
      {params.map((p) => (
        <label key={p.name} className="grid grid-cols-[minmax(5rem,auto)_1fr_3.5rem] items-center gap-3 text-sm">
          <span className="text-body">
            <MathText text={p.label ?? `$${p.name}$`} />
          </span>
          <input
            type="range"
            min={p.min}
            max={p.max}
            step={p.step ?? (p.max - p.min) / 200}
            value={values[p.name]}
            onChange={(e) => {
              setPlaying(false);
              setValues((v) => ({ ...v, [p.name]: Number(e.target.value) }));
            }}
            className="w-full accent-[var(--c-accent)]"
          />
          <span className="text-right font-mono text-heading tabular-nums">{Number(values[p.name].toFixed(2))}</span>
        </label>
      ))}
      <div className="flex gap-2">
        {playable && (
          <SmallButton onClick={() => setPlaying(!playing)} label={playing ? "Pause animation" : "Play animation"}>
            {playing ? <Pause className="h-4 w-4" aria-hidden /> : <Play className="h-4 w-4" aria-hidden />}
            {playing ? "Pause" : "Animate"}
          </SmallButton>
        )}
        <SmallButton onClick={reset} label="Reset">
          <RotateCcw className="h-4 w-4" aria-hidden /> Reset
        </SmallButton>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------
   Figure: graphs, geometry and animations described by formulas
------------------------------------------------------------------- */

type Expr = string | number;
type Ref = string | [Expr, Expr];
type Common = { color?: string; show?: Expr; dashed?: boolean; width?: number; opacity?: number };
export type FigureElement =
  | ({ type: "point"; id?: string; x: Expr; y: Expr; label?: string; labelDir?: "n" | "s" | "e" | "w" | "ne" | "nw" | "se" | "sw"; size?: number } & Common)
  | ({ type: "segment" | "line" | "vector"; a: Ref; b: Ref; label?: string } & Common)
  | ({ type: "circle"; c: Ref; r: Expr; fill?: string } & Common)
  | ({ type: "polygon"; pts: Ref[]; fill?: string } & Common)
  | ({ type: "func"; f: Expr; from?: Expr; to?: Expr; label?: string } & Common)
  | ({ type: "curve"; x: Expr; y: Expr; from: Expr; to: Expr } & Common)
  | ({ type: "text"; x: Expr; y: Expr; text: string; size?: number; anchor?: "start" | "middle" | "end" } & Common)
  | ({ type: "angle"; a: Ref; o: Ref; b: Ref; r?: number; label?: string; right?: boolean } & Common)
  | ({ type: "area"; f: Expr; g?: Expr; from: Expr; to: Expr; fill?: string } & Common)
  | ({ type: "region"; test: Expr; fill?: string; cells?: number } & Common);

export function Figure({
  bounds = [-5, 5, -5, 5],
  elements = [],
  params = [],
  readouts = [],
  caption,
  axes = true,
  grid = true,
  ticks,
  height,
  equal,
}: {
  bounds?: [number, number, number, number];
  elements?: FigureElement[];
  params?: Param[];
  readouts?: string[];
  caption?: string;
  axes?: boolean | "x";
  grid?: boolean;
  ticks?: number;
  height?: number;
  /** Keep one unit the same size across and up. Defaults on for roughly square bounds. */
  equal?: boolean;
}) {
  const state = useParams(params);
  const scope = state.values;
  const [x0, x1, y0, y1] = bounds;
  const W = 600;
  // Geometry figures keep a true aspect ratio so circles stay round; graphs may stretch to fit.
  const ratio = (y1 - y0) / (x1 - x0);
  const keep = equal ?? (ratio >= 0.4 && ratio <= 1.25);
  const H = keep ? W * ratio : (height ?? Math.min(520, Math.max(160, W * ratio)));
  const maxH = keep ? (height ?? 520) : undefined;
  const sx = (x: number) => r2(((x - x0) / (x1 - x0)) * W);
  const sy = (y: number) => r2(H - ((y - y0) / (y1 - y0)) * H);
  const ev = (e: Expr, extra: Record<string, number> = {}) => evaluate(e, { ...scope, ...extra });

  // Resolve named points first so other elements can refer to them.
  const pts: Record<string, [number, number]> = {};
  for (const el of elements) if (el.type === "point" && el.id) pts[el.id] = [ev(el.x), ev(el.y)];
  const at = (r: Ref): [number, number] => (typeof r === "string" ? (pts[r] ?? [NaN, NaN]) : [ev(r[0]), ev(r[1])]);

  const step = ticks ?? niceStep(x1 - x0);
  const gridLines: ReactNode[] = [];
  if (grid) {
    for (let x = Math.ceil(x0 / step) * step; x <= x1 + 1e-9; x += step)
      gridLines.push(<line key={`gx${x}`} x1={sx(x)} x2={sx(x)} y1={0} y2={H} stroke="rgb(255 255 255 / 0.06)" />);
    if (axes !== "x")
      for (let y = Math.ceil(y0 / step) * step; y <= y1 + 1e-9; y += step)
        gridLines.push(<line key={`gy${y}`} x1={0} x2={W} y1={sy(y)} y2={sy(y)} stroke="rgb(255 255 255 / 0.06)" />);
  }
  const tickLabels: ReactNode[] = [];
  if (axes) {
    const yAxis = Math.min(Math.max(0, y0), y1);
    for (let x = Math.ceil(x0 / step) * step; x <= x1 + 1e-9; x += step) {
      if ((Math.abs(x) < 1e-9 && axes !== "x") || x - x0 < step * 0.4 || x1 - x < step * 0.4) continue;
      tickLabels.push(
        <text key={`tx${x}`} x={sx(x)} y={sy(yAxis) + 16} fill="var(--c-muted)" fontSize="12" textAnchor="middle">
          {Number(x.toFixed(2))}
        </text>,
      );
    }
    if (axes !== "x")
      for (let y = Math.ceil(y0 / step) * step; y <= y1 + 1e-9; y += step) {
        if (Math.abs(y) < 1e-9 || y - y0 < step * 0.4 || y1 - y < step * 0.4) continue;
        tickLabels.push(
          <text key={`ty${y}`} x={sx(Math.min(Math.max(0, x0), x1)) - 6} y={sy(y) + 4} fill="var(--c-muted)" fontSize="12" textAnchor="end">
            {Number(y.toFixed(2))}
          </text>,
        );
      }
  }

  const drawn = elements.map((el, i) => {
    if (el.show !== undefined && !ev(el.show)) return null;
    const stroke = color(el.color);
    const sw = el.width ?? 2.5;
    const dash = el.dashed ? "6 5" : undefined;
    const op = el.opacity;
    switch (el.type) {
      case "point": {
        const [x, y] = el.id ? pts[el.id] : [ev(el.x), ev(el.y)];
        if (!Number.isFinite(x) || !Number.isFinite(y)) return null;
        const off = labelOffset(el.labelDir ?? "ne");
        return (
          <g key={i} opacity={op}>
            <circle cx={sx(x)} cy={sy(y)} r={el.size ?? 5} fill={stroke} stroke="var(--c-bg)" strokeWidth={1.5} />
            {el.label && (
              <text x={sx(x) + off[0]} y={sy(y) + off[1]} fill="var(--c-heading)" fontSize="16" fontStyle="italic" fontFamily="KaTeX_Main, serif" textAnchor={off[2]}>
                {fill(el.label, scope)}
              </text>
            )}
          </g>
        );
      }
      case "segment":
      case "vector":
      case "line": {
        let [ax, ay] = at(el.a);
        let [bx, by] = at(el.b);
        if (![ax, ay, bx, by].every(Number.isFinite)) return null;
        if (el.type === "line") {
          const dx = bx - ax,
            dy = by - ay,
            big = 4 * (x1 - x0 + y1 - y0);
          const len = Math.hypot(dx, dy) || 1;
          [ax, ay, bx, by] = [ax - (dx / len) * big, ay - (dy / len) * big, bx + (dx / len) * big, by + (dy / len) * big];
        }
        const id = `arrow${i}`;
        return (
          <g key={i} opacity={op}>
            {el.type === "vector" && (
              <defs>
                <marker id={id} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                  <path d="M0,0 L10,5 L0,10 z" fill={stroke} />
                </marker>
              </defs>
            )}
            <line x1={sx(ax)} y1={sy(ay)} x2={sx(bx)} y2={sy(by)} stroke={stroke} strokeWidth={sw} strokeDasharray={dash} markerEnd={el.type === "vector" ? `url(#${id})` : undefined} strokeLinecap="round" />
            {el.label && (
              <text x={(sx(ax) + sx(bx)) / 2 + 8} y={(sy(ay) + sy(by)) / 2 - 8} fill={stroke} fontSize="15" fontFamily="KaTeX_Main, serif">
                {fill(el.label, scope)}
              </text>
            )}
          </g>
        );
      }
      case "circle": {
        const [cx, cy] = at(el.c);
        const r = ev(el.r);
        if (![cx, cy, r].every(Number.isFinite)) return null;
        return (
          <ellipse key={i} cx={sx(cx)} cy={sy(cy)} rx={Math.abs(sx(cx + r) - sx(cx))} ry={Math.abs(sy(cy + r) - sy(cy))} fill={el.fill ? color(el.fill) : "none"} fillOpacity={el.fill ? 0.18 : undefined} stroke={stroke} strokeWidth={sw} strokeDasharray={dash} opacity={op} />
        );
      }
      case "polygon": {
        const p = el.pts.map(at);
        if (!p.flat().every(Number.isFinite)) return null;
        return (
          <polygon key={i} points={p.map(([x, y]) => `${sx(x)},${sy(y)}`).join(" ")} fill={el.fill ? color(el.fill) : "none"} fillOpacity={el.fill ? 0.2 : undefined} stroke={stroke} strokeWidth={sw} strokeDasharray={dash} strokeLinejoin="round" opacity={op} />
        );
      }
      case "func": {
        const a = el.from !== undefined ? ev(el.from) : x0;
        const b = el.to !== undefined ? ev(el.to) : x1;
        const d = pathFrom((t) => [t, ev(el.f, { x: t })], a, b, 400, sx, sy, y0, y1);
        return <path key={i} d={d} fill="none" stroke={stroke} strokeWidth={sw} strokeDasharray={dash} opacity={op} strokeLinejoin="round" />;
      }
      case "curve": {
        const d = pathFrom((s) => [ev(el.x, { s }), ev(el.y, { s })], ev(el.from), ev(el.to), 500, sx, sy, y0, y1);
        return <path key={i} d={d} fill="none" stroke={stroke} strokeWidth={sw} strokeDasharray={dash} opacity={op} strokeLinejoin="round" />;
      }
      case "area": {
        const a = ev(el.from),
          b = ev(el.to);
        if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
        const n = 120;
        const top: string[] = [],
          bot: string[] = [];
        for (let k = 0; k <= n; k++) {
          const x = a + ((b - a) * k) / n;
          const f = ev(el.f, { x });
          const g = el.g !== undefined ? ev(el.g, { x }) : 0;
          top.push(`${sx(x)},${sy(clamp(f, y0, y1))}`);
          bot.unshift(`${sx(x)},${sy(clamp(g, y0, y1))}`);
        }
        return <polygon key={i} points={[...top, ...bot].join(" ")} fill={color(el.fill ?? el.color)} fillOpacity={0.25} stroke="none" />;
      }
      case "region": {
        const n = el.cells ?? 90;
        const cw = (x1 - x0) / n,
          ch = (y1 - y0) / Math.round((n * H) / W);
        const rects: ReactNode[] = [];
        let f: (x: number, y: number, ...rest: number[]) => number;
        try {
          const names = Object.keys(scope);
          const c = compile(el.test, ["x", "y", ...names]);
          f = (x, y) => c(x, y, ...names.map((k) => scope[k]));
        } catch {
          return null;
        }
        for (let x = x0; x < x1; x += cw)
          for (let y = y0; y < y1; y += ch)
            if (f(x + cw / 2, y + ch / 2)) rects.push(<rect key={`${x},${y}`} x={sx(x)} y={sy(y + ch)} width={sx(x + cw) - sx(x) + 0.6} height={sy(y) - sy(y + ch) + 0.6} />);
        return (
          <g key={i} fill={color(el.fill ?? el.color)} opacity={el.opacity ?? 0.25}>
            {rects}
          </g>
        );
      }
      case "text": {
        const x = ev(el.x),
          y = ev(el.y);
        return (
          <text key={i} x={sx(x)} y={sy(y)} fill={color(el.color, "heading")} fontSize={el.size ?? 15} textAnchor={el.anchor ?? "middle"} fontFamily="KaTeX_Main, serif" opacity={op}>
            {fill(el.text, scope)}
          </text>
        );
      }
      case "angle": {
        const [ax, ay] = at(el.a),
          [ox, oy] = at(el.o),
          [bx, by] = at(el.b);
        if (![ax, ay, ox, oy, bx, by].every(Number.isFinite)) return null;
        const rr = el.r ?? 26;
        const a1 = Math.atan2(sy(ay) - sy(oy), sx(ax) - sx(ox));
        let a2 = Math.atan2(sy(by) - sy(oy), sx(bx) - sx(ox));
        let diff = a2 - a1;
        while (diff <= -Math.PI) diff += 2 * Math.PI;
        while (diff > Math.PI) diff -= 2 * Math.PI;
        a2 = a1 + diff;
        const p1 = [r2(sx(ox) + rr * Math.cos(a1)), r2(sy(oy) + rr * Math.sin(a1))];
        const p2 = [r2(sx(ox) + rr * Math.cos(a2)), r2(sy(oy) + rr * Math.sin(a2))];
        const mid = a1 + diff / 2;
        if (el.right) {
          const s = rr * 0.6;
          const u = [r2(Math.cos(a1)), r2(Math.sin(a1))],
            v = [r2(Math.cos(a2)), r2(Math.sin(a2))];
          const c0 = [sx(ox), sy(oy)];
          return (
            <path key={i} d={`M${c0[0] + u[0] * s},${c0[1] + u[1] * s} L${c0[0] + (u[0] + v[0]) * s},${c0[1] + (u[1] + v[1]) * s} L${c0[0] + v[0] * s},${c0[1] + v[1] * s}`} fill="none" stroke={stroke} strokeWidth={1.8} />
          );
        }
        return (
          <g key={i}>
            <path d={`M${sx(ox)},${sy(oy)} L${p1[0]},${p1[1]} A${rr},${rr} 0 0 ${diff > 0 ? 1 : 0} ${p2[0]},${p2[1]} Z`} fill={stroke} fillOpacity={0.18} stroke={stroke} strokeWidth={1.5} />
            {el.label && (
              <text x={r2(sx(ox) + (rr + 14) * Math.cos(mid))} y={r2(sy(oy) + (rr + 14) * Math.sin(mid) + 5)} fill={stroke} fontSize="15" textAnchor="middle" fontFamily="KaTeX_Main, serif">
                {fill(el.label, scope)}
              </text>
            )}
          </g>
        );
      }
    }
  });

  return (
    <Panel caption={caption}>
      <svg viewBox={`0 0 ${W} ${H}`} className="mx-auto block h-auto w-full bg-bg/60" style={{ maxHeight: maxH }} role="img" aria-label={caption ?? "Diagram"}>
        {gridLines}
        {axes && (
          <g stroke="rgb(255 255 255 / 0.35)" strokeWidth={1.4}>
            {y0 <= 0 && y1 >= 0 && <line x1={0} x2={W} y1={sy(0)} y2={sy(0)} />}
            {axes !== "x" && x0 <= 0 && x1 >= 0 && <line y1={0} y2={H} x1={sx(0)} x2={sx(0)} />}
          </g>
        )}
        {tickLabels}
        {drawn}
      </svg>
      {readouts.length > 0 && (
        <div className="flex flex-wrap gap-x-6 gap-y-1 border-t border-line px-4 py-2.5 text-body">
          {readouts.map((r, i) => (
            <Tex key={i} tex={fill(r, scope)} />
          ))}
        </div>
      )}
      <Controls params={params} state={state} />
    </Panel>
  );
}

function clamp(v: number, lo: number, hi: number) {
  const pad = (hi - lo) * 2;
  return Math.max(lo - pad, Math.min(hi + pad, v));
}

function niceStep(span: number) {
  const raw = span / 10;
  const p = Math.pow(10, Math.floor(Math.log10(raw)));
  for (const m of [1, 2, 5, 10]) if (raw <= m * p) return m * p;
  return 10 * p;
}

function labelOffset(dir: string): [number, number, "start" | "middle" | "end"] {
  const d = 10;
  switch (dir) {
    case "n":
      return [0, -d, "middle"];
    case "s":
      return [0, d + 12, "middle"];
    case "e":
      return [d, 5, "start"];
    case "w":
      return [-d, 5, "end"];
    case "nw":
      return [-d, -d, "end"];
    case "sw":
      return [-d, d + 10, "end"];
    case "se":
      return [d, d + 10, "start"];
    default:
      return [d, -d, "start"];
  }
}

function pathFrom(
  f: (t: number) => [number, number],
  a: number,
  b: number,
  n: number,
  sx: (x: number) => number,
  sy: (y: number) => number,
  y0: number,
  y1: number,
) {
  let d = "";
  let pen = false;
  const span = y1 - y0;
  for (let k = 0; k <= n; k++) {
    const [x, y] = f(a + ((b - a) * k) / n);
    if (!Number.isFinite(x) || !Number.isFinite(y) || y < y0 - span * 3 || y > y1 + span * 3) {
      pen = false;
      continue;
    }
    d += `${pen ? "L" : "M"}${sx(x).toFixed(2)},${sy(y).toFixed(2)} `;
    pen = true;
  }
  return d;
}

/* ------------------------------------------------------------------
   Quick check: one multiple choice question with feedback
------------------------------------------------------------------- */

export function Check({ choices, answer, explain, children }: { choices: string[]; answer: number; explain?: string; children: ReactNode }) {
  const [picked, setPicked] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  const right = checked && picked === answer;
  return (
    <div className="not-prose my-7 rounded-lg border border-accent/40 bg-surface p-5">
      <p className="mb-1 text-sm font-semibold text-accent-soft">Quick check</p>
      <div className="prose-math text-heading">{children}</div>
      <div className="mt-4 grid gap-2 sm:grid-cols-2">
        {choices.map((c, i) => {
          const state = checked && i === answer ? "border-correct bg-correct/10" : checked && i === picked ? "border-wrong bg-wrong/10" : picked === i ? "border-accent bg-accent/15" : "border-line bg-surface-2 hover:border-accent/60";
          return (
            <button
              key={i}
              type="button"
              disabled={right}
              onClick={() => {
                setPicked(i);
                setChecked(false);
              }}
              className={`flex items-center gap-3 rounded-md border px-3 py-2.5 text-left transition-colors focus-visible:outline-2 focus-visible:outline-accent ${state}`}
            >
              <span className="grid h-6 w-6 shrink-0 place-items-center rounded-full border border-line text-xs font-bold text-muted">{"ABCDE"[i]}</span>
              <MathText text={c} className="text-body" />
            </button>
          );
        })}
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <button
          type="button"
          disabled={picked === null || right}
          onClick={() => setChecked(true)}
          className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        >
          Check
        </button>
        {checked && (
          <p role="status" className={`flex items-center gap-1.5 text-sm font-semibold ${right ? "text-correct" : "text-wrong"}`}>
            {right ? <CheckIcon className="h-4 w-4" aria-hidden /> : <X className="h-4 w-4" aria-hidden />}
            {right ? "Correct." : "Not quite. Try another choice."}
          </p>
        )}
      </div>
      {right && explain && (
        <p className="mt-3 rounded-md bg-surface-2 px-4 py-3 text-body">
          <MathText text={explain} />
        </p>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------
   Worked solution revealed one step at a time
------------------------------------------------------------------- */

export function Step({ title, children }: { title?: string; children: ReactNode }) {
  return (
    <div>
      {title && (
        <p className="font-semibold text-heading">
          <MathText text={title} />
        </p>
      )}
      <div className="prose-math">{children}</div>
    </div>
  );
}

export function Steps({ title = "Worked example", problem, children }: { title?: string; problem?: string; children: ReactNode }) {
  const steps = Children.toArray(children).filter(isValidElement);
  const [shown, setShown] = useState(0);
  return (
    <div className="not-prose my-7 rounded-lg border border-line bg-surface-2 p-5">
      <p className="text-sm font-semibold text-accent-soft">{title}</p>
      {problem && (
        <p className="mt-2 text-[1.05rem] text-heading">
          <MathText text={problem} />
        </p>
      )}
      <ol className="mt-4 space-y-4">
        {steps.slice(0, shown).map((s, i) => (
          <li key={i} className="flex gap-3">
            <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-accent/20 text-sm font-bold text-accent-soft">{i + 1}</span>
            <div className="min-w-0 flex-1 text-body">{s}</div>
          </li>
        ))}
      </ol>
      <div className="mt-4 flex flex-wrap gap-2">
        {shown < steps.length ? (
          <>
            <SmallButton onClick={() => setShown(shown + 1)}>
              {shown === 0 ? "Start solving" : "Next step"} <ChevronRight className="h-4 w-4" aria-hidden />
            </SmallButton>
            <SmallButton onClick={() => setShown(steps.length)}>Show all</SmallButton>
          </>
        ) : (
          <SmallButton onClick={() => setShown(0)}>
            <RotateCcw className="h-4 w-4" aria-hidden /> Hide steps
          </SmallButton>
        )}
        <span className="self-center text-sm text-muted">
          {shown} of {steps.length} steps
        </span>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------
   Dice grid: every outcome of two dice, with a rule highlighted
------------------------------------------------------------------- */

export function DiceGrid({ rules, caption }: { rules: { label: string; when: string }[]; caption?: string }) {
  const [k, setK] = useState(0);
  const rule = rules[k];
  let hits = 0;
  const cells: ReactNode[] = [];
  for (let a = 1; a <= 6; a++)
    for (let b = 1; b <= 6; b++) {
      const on = evaluate(rule.when, { a, b }) ? true : false;
      if (on) hits++;
      cells.push(
        <div key={`${a}${b}`} className={`grid aspect-square place-items-center rounded text-xs font-semibold transition-colors sm:text-sm ${on ? "bg-accent text-white" : "bg-surface-2 text-muted"}`}>
          {a},{b}
        </div>,
      );
    }
  return (
    <Panel caption={caption}>
      <div className="p-4">
        <div className="mb-3 flex flex-wrap gap-2">
          {rules.map((r, i) => (
            <SmallButton key={i} onClick={() => setK(i)} active={i === k}>
              <MathText text={r.label} />
            </SmallButton>
          ))}
        </div>
        <div className="grid grid-cols-[auto_repeat(6,1fr)] gap-1">
          <div />
          {[1, 2, 3, 4, 5, 6].map((b) => (
            <div key={b} className="text-center text-xs text-muted">
              blue {b}
            </div>
          ))}
          {[1, 2, 3, 4, 5, 6].map((a) => (
            <div key={a} className="contents">
              <div className="self-center pr-2 text-xs text-muted">red {a}</div>
              {cells.slice((a - 1) * 6, a * 6)}
            </div>
          ))}
        </div>
        <p className="mt-3 text-body">
          <Tex tex={`${hits}\\text{ of }36\\text{ outcomes} \\Rightarrow P = \\tfrac{${hits}}{36}`} />
        </p>
      </div>
    </Panel>
  );
}

/* ------------------------------------------------------------------
   Venn diagram with clickable views
------------------------------------------------------------------- */

const VENN2: Record<string, [number, number]> = { A: [175, 160], B: [425, 160], AB: [300, 160], none: [560, 300] };
const VENN3: Record<string, [number, number]> = {
  A: [200, 120],
  B: [400, 120],
  C: [300, 305],
  AB: [300, 98],
  AC: [233, 222],
  BC: [367, 222],
  ABC: [300, 172],
  none: [565, 378],
};

export function Venn({ labels, counts, views = [], caption }: { labels: string[]; counts: Record<string, number | string>; views?: { label: string; regions: string[] }[]; caption?: string }) {
  const [v, setV] = useState(-1);
  const three = labels.length === 3;
  const pos = three ? VENN3 : VENN2;
  const circles: [number, number][] = three
    ? [
        [240, 145],
        [360, 145],
        [300, 248],
      ]
    : [
        [235, 160],
        [365, 160],
      ];
  const lit = v >= 0 ? new Set(views[v].regions) : null;
  const H = three ? 400 : 320;
  return (
    <Panel caption={caption}>
      <svg viewBox={`0 0 600 ${H}`} className="block h-auto w-full bg-bg/60" role="img" aria-label={`Venn diagram of ${labels.join(", ")}`}>
        <rect x={6} y={6} width={588} height={H - 12} rx={12} fill={lit?.has("none") ? "var(--c-accent)" : "none"} fillOpacity={0.18} stroke="rgb(255 255 255 / 0.25)" />
        {lit && (
          <defs>
            {circles.map(([cx, cy], i) => (
              <clipPath key={i} id={`vc${i}`}>
                <circle cx={cx} cy={cy} r={three ? 110 : 130} />
              </clipPath>
            ))}
          </defs>
        )}
        {lit &&
          [...lit].filter((r) => r !== "none").map((r) => <VennRegion key={r} code={r} circles={circles} three={three} />)}
        {circles.map(([cx, cy], i) => (
          <circle key={i} cx={cx} cy={cy} r={three ? 110 : 130} fill="none" stroke={[PALETTE.accent, PALETTE.blue, PALETTE.amber][i]} strokeWidth={2.5} />
        ))}
        {labels.map((l, i) => {
          const [cx, cy] = circles[i];
          const lx = three ? (i === 0 ? cx - 110 : i === 1 ? cx + 110 : cx) : i === 0 ? cx - 120 : cx + 120;
          const ly = three ? (i === 2 ? cy + 134 : cy - 112) : 30;
          return (
            <text key={l} x={lx} y={ly} fill={[PALETTE.accent, PALETTE.blue, PALETTE.amber][i]} fontSize="17" fontWeight={700} textAnchor="middle">
              {l}
            </text>
          );
        })}
        {Object.entries(counts).map(([code, n]) =>
          pos[code] ? (
            <text key={code} x={pos[code][0]} y={pos[code][1] + 6} fill="var(--c-heading)" fontSize="19" fontWeight={700} textAnchor="middle">
              {n}
            </text>
          ) : null,
        )}
      </svg>
      {views.length > 0 && (
        <div className="flex flex-wrap gap-2 border-t border-line px-4 py-3">
          {views.map((vw, i) => (
            <SmallButton key={i} onClick={() => setV(i === v ? -1 : i)} active={i === v}>
              <MathText text={vw.label} />
            </SmallButton>
          ))}
        </div>
      )}
    </Panel>
  );
}

function VennRegion({ code, circles, three }: { code: string; circles: [number, number][]; three: boolean }) {
  const idx = (ch: string) => "ABC".indexOf(ch);
  const inside = code.split("").map(idx);
  const outside = [0, 1, 2].slice(0, three ? 3 : 2).filter((i) => !inside.includes(i));
  const r = three ? 110 : 130;
  const id = `vm-${code}`;
  // Fill the first inside circle, clipped by the others, minus the outside circles.
  let shape: ReactNode = <circle cx={circles[inside[0]][0]} cy={circles[inside[0]][1]} r={r} fill="var(--c-accent)" fillOpacity={0.35} mask={`url(#${id})`} />;
  for (const k of inside.slice(1)) shape = <g clipPath={`url(#vc${k})`}>{shape}</g>;
  return (
    <g>
      <defs>
        <mask id={id}>
          <rect width="600" height="400" fill="white" />
          {outside.map((o) => (
            <circle key={o} cx={circles[o][0]} cy={circles[o][1]} r={r} fill="black" />
          ))}
        </mask>
      </defs>
      {shape}
    </g>
  );
}

/* ------------------------------------------------------------------
   Lattice path counter: fills in Pascal's triangle on a grid
------------------------------------------------------------------- */

export function PathGrid({ m = 4, n = 3, blocked = [], caption }: { m?: number; n?: number; blocked?: [number, number][]; caption?: string }) {
  const reduced = usePrefersReducedMotion();
  const counts = useMemo(() => {
    const c: number[][] = [];
    const isBlocked = (x: number, y: number) => blocked.some(([bx, by]) => bx === x && by === y);
    for (let x = 0; x <= m; x++) {
      c[x] = [];
      for (let y = 0; y <= n; y++) {
        if (isBlocked(x, y)) c[x][y] = 0;
        else if (x === 0 && y === 0) c[x][y] = 1;
        else c[x][y] = (x > 0 ? c[x - 1][y] : 0) + (y > 0 ? c[x][y - 1] : 0);
      }
    }
    return c;
  }, [m, n, blocked]);
  const order = useMemo(() => {
    const o: [number, number][] = [];
    for (let s = 0; s <= m + n; s++) for (let x = 0; x <= m; x++) if (s - x >= 0 && s - x <= n) o.push([x, s - x]);
    return o;
  }, [m, n]);
  const [shown, setShown] = useState(1);
  const [running, setRunning] = useState(false);
  useEffect(() => {
    if (!running) return;
    if (shown >= order.length) {
      setRunning(false);
      return;
    }
    const t = setTimeout(() => setShown((s) => s + 1), reduced ? 0 : 260);
    return () => clearTimeout(t);
  }, [running, shown, order.length, reduced]);
  const cell = Math.min(110, 520 / Math.max(m, n));
  const W = m * cell + 80,
    H = n * cell + 80;
  const X = (x: number) => 40 + x * cell,
    Y = (y: number) => H - 40 - y * cell;
  const vis = new Set(order.slice(0, shown).map(([x, y]) => `${x},${y}`));
  return (
    <Panel caption={caption}>
      <svg viewBox={`0 0 ${W} ${H}`} className="mx-auto block h-auto w-full max-w-xl bg-bg/60" role="img" aria-label="Grid of path counts">
        {Array.from({ length: m + 1 }, (_, x) => (
          <line key={`v${x}`} x1={X(x)} x2={X(x)} y1={Y(0)} y2={Y(n)} stroke="rgb(255 255 255 / 0.25)" />
        ))}
        {Array.from({ length: n + 1 }, (_, y) => (
          <line key={`h${y}`} y1={Y(y)} y2={Y(y)} x1={X(0)} x2={X(m)} stroke="rgb(255 255 255 / 0.25)" />
        ))}
        {order.map(([x, y]) => {
          const on = vis.has(`${x},${y}`);
          const bad = blocked.some(([bx, by]) => bx === x && by === y);
          return (
            <g key={`${x},${y}`}>
              <circle cx={X(x)} cy={Y(y)} r={16} fill={bad ? "var(--c-wrong)" : on ? "var(--c-accent)" : "var(--c-surface-2)"} stroke="var(--c-bg)" strokeWidth={2} />
              {on && (
                <text x={X(x)} y={Y(y) + 5} fill="white" fontSize="14" fontWeight={700} textAnchor="middle">
                  {bad ? "×" : counts[x][y]}
                </text>
              )}
            </g>
          );
        })}
        <text x={X(0)} y={Y(0) + 34} fill="var(--c-muted)" fontSize="13" textAnchor="middle">
          start
        </text>
        <text x={X(m)} y={Y(n) - 24} fill="var(--c-muted)" fontSize="13" textAnchor="middle">
          end
        </text>
      </svg>
      <div className="flex flex-wrap items-center gap-2 border-t border-line px-4 py-3">
        <SmallButton onClick={() => (shown >= order.length ? setShown(1) : setRunning(!running))}>
          {running ? <Pause className="h-4 w-4" aria-hidden /> : <Play className="h-4 w-4" aria-hidden />}
          {shown >= order.length ? "Start over" : running ? "Pause" : "Fill in the counts"}
        </SmallButton>
        <SmallButton onClick={() => setShown(Math.min(order.length, shown + 1))}>One more point</SmallButton>
        <span className="text-sm text-muted">Each number is the one to its left plus the one below it.</span>
      </div>
    </Panel>
  );
}

/* ------------------------------------------------------------------
   Clock arithmetic: hop around a clock of n hours
------------------------------------------------------------------- */

export function ModClock({ n = 12, start = 0, step = 5, hops = 6, caption }: { n?: number; start?: number; step?: number; hops?: number; caption?: string }) {
  const [N, setN] = useState(n);
  const [s, setS] = useState(step);
  const [k, setK] = useState(0);
  const pos = (i: number) => (((start + i * s) % N) + N) % N;
  const R = 130,
    C = 170;
  const xy = (h: number): [number, number] => [r2(C + R * Math.sin((2 * Math.PI * h) / N)), r2(C - R * Math.cos((2 * Math.PI * h) / N))];
  const path = Array.from({ length: k + 1 }, (_, i) => xy(pos(i)));
  return (
    <Panel caption={caption}>
      <div className="grid gap-4 p-4 sm:grid-cols-[340px_1fr]">
        <svg viewBox="0 0 340 340" className="h-auto w-full" role="img" aria-label={`Clock with ${N} positions`}>
          <circle cx={C} cy={C} r={R} fill="none" stroke="rgb(255 255 255 / 0.2)" strokeWidth={2} />
          {path.slice(1).map(([x, y], i) => (
            <line key={i} x1={path[i][0]} y1={path[i][1]} x2={x} y2={y} stroke="var(--c-accent-soft)" strokeWidth={2.5} opacity={0.4 + (0.6 * (i + 1)) / path.length} />
          ))}
          {Array.from({ length: N }, (_, h) => {
            const [x, y] = xy(h);
            const here = pos(k) === h;
            return (
              <g key={h}>
                <circle cx={x} cy={y} r={15} fill={here ? "var(--c-accent)" : "var(--c-surface-2)"} stroke="var(--c-line)" />
                <text x={x} y={y + 5} fill="white" fontSize="13" fontWeight={700} textAnchor="middle">
                  {h}
                </text>
              </g>
            );
          })}
        </svg>
        <div className="space-y-3 text-body">
          <label className="block text-sm">
            Clock size: <b className="text-heading">{N}</b>
            <input type="range" min={2} max={16} value={N} onChange={(e) => (setN(Number(e.target.value)), setK(0))} className="mt-1 w-full accent-[var(--c-accent)]" />
          </label>
          <label className="block text-sm">
            Hop size: <b className="text-heading">{s}</b>
            <input type="range" min={1} max={15} value={s} onChange={(e) => (setS(Number(e.target.value)), setK(0))} className="mt-1 w-full accent-[var(--c-accent)]" />
          </label>
          <p>
            <Tex tex={`${start} + ${k}\\cdot ${s} = ${start + k * s} \\equiv ${pos(k)} \\pmod{${N}}`} />
          </p>
          <div className="flex flex-wrap gap-2">
            <SmallButton onClick={() => setK(k + 1)}>Hop</SmallButton>
            <SmallButton onClick={() => setK(Math.max(0, k + hops))}>Hop {hops} times</SmallButton>
            <SmallButton onClick={() => setK(0)}>
              <RotateCcw className="h-4 w-4" aria-hidden /> Reset
            </SmallButton>
          </div>
        </div>
      </div>
    </Panel>
  );
}

/* ------------------------------------------------------------------
   Sequence bars: arithmetic or geometric terms and running sums
------------------------------------------------------------------- */

export function SequenceBars({ kind = "arithmetic", a = 2, d = 3, terms = 8, caption }: { kind?: "arithmetic" | "geometric"; a?: number; d?: number; terms?: number; caption?: string }) {
  const [A, setA] = useState(a);
  const [D, setD] = useState(d);
  const [sum, setSum] = useState(false);
  const vals = Array.from({ length: terms }, (_, i) => (kind === "arithmetic" ? A + i * D : A * Math.pow(D, i)));
  const shown = sum ? vals.map((_, i) => vals.slice(0, i + 1).reduce((p, q) => p + q, 0)) : vals;
  const top = Math.max(1, ...shown.map(Math.abs));
  const hasNeg = shown.some((v) => v < 0);
  const H = 240,
    W = 600,
    bw = W / terms;
  const base = hasNeg ? H / 2 : H - 20;
  const scale = (hasNeg ? H / 2 - 20 : H - 40) / top;
  return (
    <Panel caption={caption}>
      <svg viewBox={`0 0 ${W} ${H}`} className="block h-auto w-full bg-bg/60" role="img" aria-label="Bar chart of sequence terms">
        <line x1={0} x2={W} y1={base} y2={base} stroke="rgb(255 255 255 / 0.3)" />
        {shown.map((v, i) => {
          const h = v * scale;
          return (
            <g key={i}>
              <rect x={i * bw + 8} y={h >= 0 ? base - h : base} width={bw - 16} height={Math.abs(h)} rx={4} fill={sum ? "var(--c-primary)" : "var(--c-accent)"} opacity={0.85} style={{ transition: "all 250ms ease" }} />
              <text x={i * bw + bw / 2} y={h >= 0 ? base - h - 6 : base - h + 16} fill="var(--c-heading)" fontSize="13" textAnchor="middle">
                {Number(v.toFixed(2))}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="grid gap-3 border-t border-line bg-surface-2/50 px-4 py-3 text-sm sm:grid-cols-2">
        <label>
          First term: <b className="text-heading">{A}</b>
          <input type="range" min={kind === "arithmetic" ? -10 : 1} max={10} step={1} value={A} onChange={(e) => setA(Number(e.target.value))} className="mt-1 w-full accent-[var(--c-accent)]" />
        </label>
        <label>
          {kind === "arithmetic" ? "Common difference d" : "Common ratio r"}: <b className="text-heading">{D}</b>
          <input type="range" min={kind === "arithmetic" ? -5 : -2} max={kind === "arithmetic" ? 5 : 2} step={kind === "arithmetic" ? 1 : 0.25} value={D} onChange={(e) => setD(Number(e.target.value))} className="mt-1 w-full accent-[var(--c-accent)]" />
        </label>
        <div className="flex gap-2 sm:col-span-2">
          <SmallButton onClick={() => setSum(false)} active={!sum}>
            Terms
          </SmallButton>
          <SmallButton onClick={() => setSum(true)} active={sum}>
            Running sums
          </SmallButton>
        </div>
      </div>
    </Panel>
  );
}

/* ------------------------------------------------------------------
   Telescoping: watch the middle terms cancel
------------------------------------------------------------------- */

export function Telescope({ terms, result, caption }: { terms: [string, string][]; result: string; caption?: string }) {
  const [gone, setGone] = useState(false);
  return (
    <Panel caption={caption}>
      <div className="flex flex-wrap items-center gap-x-1.5 gap-y-3 p-5 text-lg text-body">
        {terms.map(([plus, minus], i) => {
          const cancelPlus = gone && i > 0;
          const cancelMinus = gone && i < terms.length - 1;
          return (
            <span key={i} className="inline-flex items-center gap-1.5">
              {i > 0 && <span className="text-muted">+</span>}
              <span className="rounded-md bg-surface-2 px-2 py-1">
                (
                <span className={`transition-opacity duration-500 ${cancelPlus ? "line-through decoration-wrong decoration-2 opacity-30" : "text-heading"}`}>
                  <Tex tex={plus} />
                </span>
                <span className="mx-1">−</span>
                <span className={`transition-opacity duration-500 ${cancelMinus ? "line-through decoration-wrong decoration-2 opacity-30" : "text-heading"}`}>
                  <Tex tex={minus} />
                </span>
                )
              </span>
            </span>
          );
        })}
      </div>
      <div className="flex flex-wrap items-center gap-3 border-t border-line px-4 py-3">
        <SmallButton onClick={() => setGone(!gone)} active={gone}>
          {gone ? "Bring the terms back" : "Cancel the matching terms"}
        </SmallButton>
        {gone && (
          <span className="text-body">
            What survives: <Tex tex={result} />
          </span>
        )}
      </div>
    </Panel>
  );
}

/* ------------------------------------------------------------------
   Card flip for vocabulary and formulas
------------------------------------------------------------------- */

export function FlipCards({ cards }: { cards: { front: string; back: string }[] }) {
  const [open, setOpen] = useState<Set<number>>(new Set());
  return (
    <div className="not-prose my-7 grid gap-3 sm:grid-cols-2">
      {cards.map((c, i) => {
        const on = open.has(i);
        return (
          <button
            key={i}
            type="button"
            onClick={() => setOpen((s) => (s.has(i) ? new Set([...s].filter((x) => x !== i)) : new Set([...s, i])))}
            className={`min-h-24 rounded-lg border px-4 py-3 text-left transition-colors focus-visible:outline-2 focus-visible:outline-accent ${on ? "border-accent bg-accent/10" : "border-line bg-surface hover:border-accent/60"}`}
          >
            <span className="block text-xs font-semibold text-muted">{on ? "Answer" : "Tap to reveal"}</span>
            <span className="mt-1 block text-body">
              <MathText text={on ? c.back : c.front} />
            </span>
          </button>
        );
      })}
    </div>
  );
}

/* ------------------------------------------------------------------
   Power cycles: last digits (or remainders) of b, b^2, b^3, ...
------------------------------------------------------------------- */

export function PowerCycle({ base = 7, mod = 10, terms = 12, caption }: { base?: number; mod?: number; terms?: number; caption?: string }) {
  const [b, setB] = useState(base);
  const [m, setM] = useState(mod);
  const seq: number[] = [];
  let v = 1;
  for (let k = 1; k <= terms; k++) {
    v = (v * b) % m;
    seq.push(v);
  }
  // cycle length: first repeat of the first value that recurs
  let cycle = 0;
  outer: for (let i = 0; i < seq.length; i++)
    for (let j = i + 1; j < seq.length; j++)
      if (seq[j] === seq[i]) {
        let ok = true;
        for (let t = 0; j + t < seq.length; t++) if (seq[i + t] !== seq[j + t]) ok = false;
        if (ok) {
          cycle = j - i;
          break outer;
        }
      }
  const colors = ["bg-accent/70", "bg-blue-400/60", "bg-amber-400/60", "bg-teal-400/60", "bg-pink-400/60", "bg-correct/50"];
  return (
    <Panel caption={caption}>
      <div className="space-y-4 p-4">
        <div className="flex flex-wrap gap-2">
          {seq.map((r, i) => (
            <div key={i} className={`min-w-14 rounded-md px-2 py-1.5 text-center ${cycle ? colors[i % cycle % colors.length] : "bg-surface-2"}`}>
              <div className="text-xs text-white/80">
                <Tex tex={`${b}^{${i + 1}}`} />
              </div>
              <div className="text-lg font-bold text-white">{r}</div>
            </div>
          ))}
        </div>
        <p className="text-body">
          {cycle ? (
            <Tex tex={`\\text{remainders mod } ${m} \\text{ repeat every } ${cycle} \\text{ steps}`} />
          ) : (
            <Tex tex={`\\text{no repeat yet in the first ${terms} powers}`} />
          )}
        </p>
        <div className="grid gap-3 text-sm sm:grid-cols-2">
          <label>
            Base: <b className="text-heading">{b}</b>
            <input type="range" min={2} max={12} value={b} onChange={(e) => setB(Number(e.target.value))} className="mt-1 w-full accent-[var(--c-accent)]" />
          </label>
          <label>
            Divide by (10 gives the last digit): <b className="text-heading">{m}</b>
            <input type="range" min={3} max={13} value={m} onChange={(e) => setM(Number(e.target.value))} className="mt-1 w-full accent-[var(--c-accent)]" />
          </label>
        </div>
      </div>
    </Panel>
  );
}

/* ------------------------------------------------------------------
   Place values in any base
------------------------------------------------------------------- */

export function BasePlaces({ value = 45, base = 3, caption }: { value?: number; base?: number; caption?: string }) {
  const [n, setN] = useState(value);
  const [b, setB] = useState(base);
  const digits: number[] = [];
  let x = n;
  if (x === 0) digits.push(0);
  while (x > 0) {
    digits.unshift(x % b);
    x = Math.floor(x / b);
  }
  const sym = (d: number) => (d < 10 ? String(d) : String.fromCharCode(55 + d));
  return (
    <Panel caption={caption}>
      <div className="space-y-4 p-4">
        <div className="flex flex-wrap justify-center gap-2">
          {digits.map((d, i) => {
            const p = digits.length - 1 - i;
            return (
              <div key={i} className="w-20 rounded-md border border-line bg-surface-2 p-2 text-center">
                <div className="text-3xl font-bold text-heading">{sym(d)}</div>
                <div className="mt-1 text-xs text-muted">
                  <Tex tex={`${b}^{${p}} = ${Math.pow(b, p)}`} />
                </div>
                <div className="text-xs text-accent-soft">
                  <Tex tex={`${d} \\times ${Math.pow(b, p)}`} />
                </div>
              </div>
            );
          })}
        </div>
        <p className="text-center text-body">
          <Tex tex={`${digits.map(sym).join("")}_{${b}} = ${digits.map((d, i) => `${d}\\cdot ${b}^{${digits.length - 1 - i}}`).join(" + ")} = ${n}`} />
        </p>
        <div className="grid gap-3 text-sm sm:grid-cols-2">
          <label>
            Number (in base 10): <b className="text-heading">{n}</b>
            <input type="range" min={0} max={300} value={n} onChange={(e) => setN(Number(e.target.value))} className="mt-1 w-full accent-[var(--c-accent)]" />
          </label>
          <label>
            Base: <b className="text-heading">{b}</b>
            <input type="range" min={2} max={16} value={b} onChange={(e) => setB(Number(e.target.value))} className="mt-1 w-full accent-[var(--c-accent)]" />
          </label>
        </div>
      </div>
    </Panel>
  );
}
