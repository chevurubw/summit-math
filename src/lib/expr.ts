/**
 * A tiny math expression compiler for lesson figures.
 * Lessons describe graphs and shapes with formulas such as "a*x^2 + b" or "cos(t)".
 * Only numbers, operators and the names below are allowed, so a typo fails loudly
 * instead of running arbitrary code.
 */

const FUNCS: Record<string, (...a: number[]) => number> = {
  sin: Math.sin,
  cos: Math.cos,
  tan: Math.tan,
  asin: Math.asin,
  acos: Math.acos,
  atan: Math.atan,
  atan2: Math.atan2,
  sqrt: Math.sqrt,
  cbrt: Math.cbrt,
  abs: Math.abs,
  exp: Math.exp,
  ln: Math.log,
  log: Math.log10,
  log2: Math.log2,
  logb: (b, x) => Math.log(x) / Math.log(b),
  floor: Math.floor,
  ceil: Math.ceil,
  round: Math.round,
  min: Math.min,
  max: Math.max,
  pow: Math.pow,
  sign: Math.sign,
  hypot: Math.hypot,
  /** degrees to radians, so lessons can write sind(30) */
  sind: (d) => Math.sin((d * Math.PI) / 180),
  cosd: (d) => Math.cos((d * Math.PI) / 180),
  tand: (d) => Math.tan((d * Math.PI) / 180),
  rad: (d) => (d * Math.PI) / 180,
  deg: (r) => (r * 180) / Math.PI,
  mod: (a, n) => ((a % n) + n) % n,
  fact: (n) => {
    let p = 1;
    for (let i = 2; i <= n; i++) p *= i;
    return p;
  },
  choose: (n, k) => {
    if (k < 0 || k > n) return 0;
    let p = 1;
    for (let i = 1; i <= k; i++) p = (p * (n - k + i)) / i;
    return Math.round(p);
  },
  gcd: (a, b) => {
    a = Math.abs(Math.round(a));
    b = Math.abs(Math.round(b));
    while (b) [a, b] = [b, a % b];
    return a;
  },
  /** 1 when the condition holds, else 0 */
  when: (c) => (c ? 1 : 0),
};

const CONSTS: Record<string, number> = { pi: Math.PI, e: Math.E };

const cache = new Map<string, (...args: number[]) => number>();

export function compile(expr: string | number, vars: string[]): (...args: number[]) => number {
  if (typeof expr === "number") return () => expr;
  const key = expr + "|" + vars.join(",");
  const hit = cache.get(key);
  if (hit) return hit;
  if (!/^[\w\s+\-*/^().,<>=!?:%&|]*$/.test(expr)) throw new Error(`Bad character in "${expr}"`);
  const body = expr
    .replace(/\^/g, "**")
    .replace(/(?<![\w.])([A-Za-z_]\w*)/g, (name) => {
      if (vars.includes(name)) return name;
      if (name in FUNCS) return `__F.${name}`;
      if (name in CONSTS) return `__C.${name}`;
      throw new Error(`Unknown name "${name}" in "${expr}"`);
    });
  // eslint-disable-next-line @typescript-eslint/no-implied-eval
  const fn = new Function("__F", "__C", ...vars, `"use strict"; return (${body});`) as (...a: unknown[]) => number;
  const out = (...args: number[]) => {
    const v = fn(FUNCS, CONSTS, ...args);
    return typeof v === "boolean" ? (v ? 1 : 0) : v;
  };
  cache.set(key, out);
  return out;
}

/** Evaluate once with a scope object. Returns NaN on any error. */
export function evaluate(expr: string | number, scope: Record<string, number>): number {
  try {
    const names = Object.keys(scope);
    return compile(expr, names)(...names.map((n) => scope[n]));
  } catch {
    return NaN;
  }
}

/** Format a number for display: rounds to `digits` places and drops trailing zeros. */
export function fmt(v: number, digits = 2): string {
  if (!Number.isFinite(v)) return "\\text{undefined}";
  const r = Number(v.toFixed(digits));
  return (Object.is(r, -0) ? 0 : r).toString();
}

/** Replace [[expr]] or [[expr:digits]] inside a template with formatted values. */
export function fill(template: string, scope: Record<string, number>): string {
  return template.replace(/\[\[(.+?)\]\]/g, (_, body: string) => {
    const m = body.match(/^([\s\S]*):(\d)$/);
    return m ? fmt(evaluate(m[1], scope), Number(m[2])) : fmt(evaluate(body, scope), 2);
  });
}
