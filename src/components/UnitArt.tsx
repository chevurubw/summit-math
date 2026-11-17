/**
 * A small line drawing for each unit. Each one moves when its card is hovered
 * (the card needs the "group" class). The motions live in globals.css under "Unit art".
 */

const S = { fill: "none", stroke: "currentColor", strokeWidth: 2.5, strokeLinecap: "round", strokeLinejoin: "round" } as const;
const faint = { ...S, strokeWidth: 1.2, opacity: 0.35 };

function Axes() {
  return (
    <g {...faint}>
      <line x1="16" y1="96" x2="184" y2="96" />
      <line x1="40" y1="12" x2="40" y2="108" />
    </g>
  );
}

const arts: Record<string, () => React.ReactElement> = {
  // A parabola, traced by a point on hover
  algebra: () => (
    <>
      <Axes />
      <path className="ua-draw text-accent" pathLength={1} d="M48 24 Q100 168 152 24" {...S} />
      <circle className="ua-trace text-primary" r="5" fill="currentColor" style={{ offsetPath: "path('M48 24 Q100 168 152 24')" }} />
    </>
  ),
  // A triangle with its incircle; the triangle turns and the circle pulses
  geometry: () => (
    <>
      <g className="ua-spin" style={{ transformOrigin: "100px 66px" }}>
        <path className="text-accent" d="M100 14 L156 104 L44 104 Z" {...S} />
      </g>
      <circle className="ua-pulse text-primary" cx="100" cy="74" r="25" {...S} style={{ transformOrigin: "100px 74px" }} />
      <circle cx="100" cy="74" r="2.5" fill="currentColor" className="text-heading" />
    </>
  ),
  // A grid of dots where the primes light up one after another
  number_theory: () => {
    const dots = [];
    const primes = new Set([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
    for (let n = 1; n <= 30; n++) {
      const col = (n - 1) % 10;
      const row = Math.floor((n - 1) / 10);
      const prime = primes.has(n);
      dots.push(
        <circle
          key={n}
          cx={28 + col * 16}
          cy={34 + row * 26}
          r={prime ? 5 : 3}
          fill="currentColor"
          className={prime ? "ua-blink text-primary" : "text-muted"}
          style={prime ? { animationDelay: `${n * 35}ms`, transformOrigin: `${28 + col * 16}px ${34 + row * 26}px` } : { opacity: 0.4 }}
        />,
      );
    }
    return <>{dots}</>;
  },
  // Two dice that tumble
  counting_probability: () => {
    const pips = (cx: number, cy: number, spots: [number, number][]) =>
      spots.map(([x, y], i) => <circle key={i} cx={cx + x * 13} cy={cy + y * 13} r="4" fill="currentColor" />);
    return (
      <>
        <g className="ua-tumble text-accent" style={{ transformOrigin: "70px 62px" }}>
          <rect x="44" y="36" width="52" height="52" rx="10" {...S} />
          {pips(70, 62, [[-1, -1], [0, 0], [1, 1]])}
        </g>
        <g className="ua-tumble ua-late text-primary" style={{ transformOrigin: "134px 62px" }}>
          <rect x="108" y="36" width="52" height="52" rx="10" {...S} />
          {pips(134, 62, [[-1, -1], [1, -1], [-1, 1], [1, 1]])}
        </g>
      </>
    );
  },
  // The unit circle with a sweeping radius
  trigonometry: () => (
    <>
      <g {...faint}>
        <line x1="40" y1="60" x2="160" y2="60" />
        <line x1="100" y1="8" x2="100" y2="112" />
      </g>
      <circle cx="100" cy="60" r="44" className="text-accent" {...S} />
      <g className="ua-sweep text-primary" style={{ transformOrigin: "100px 60px" }}>
        <line x1="100" y1="60" x2="138" y2="38" {...S} />
        <circle cx="138" cy="38" r="5" fill="currentColor" />
      </g>
    </>
  ),
  // A log curve that redraws
  logarithms: () => (
    <>
      <Axes />
      <path className="ua-draw text-accent" pathLength={1} d="M46 108 C52 60 70 44 100 36 S160 24 184 20" {...S} />
      <circle cx="58" cy="96" r="4" fill="currentColor" className="ua-pulse text-primary" style={{ transformOrigin: "58px 96px" }} />
    </>
  ),
  // Roots of unity: a hexagon on a circle that turns
  complex_numbers: () => {
    const pts = Array.from({ length: 6 }, (_, k) => {
      const a = (Math.PI / 3) * k;
      return [Math.round((100 + 42 * Math.cos(a)) * 100) / 100, Math.round((60 - 42 * Math.sin(a)) * 100) / 100];
    });
    return (
      <>
        <circle cx="100" cy="60" r="42" {...faint} />
        <g className="ua-spin text-accent" style={{ transformOrigin: "100px 60px" }}>
          <path d={`M${pts.map((p) => p.join(" ")).join(" L")} Z`} {...S} />
          {pts.map(([x, y], i) => (
            <circle key={i} cx={x} cy={y} r="4.5" fill="currentColor" className="text-primary" />
          ))}
        </g>
      </>
    );
  },
  // A cubic crossing the axis at three roots
  polynomials: () => (
    <>
      <g {...faint}>
        <line x1="16" y1="64" x2="184" y2="64" />
      </g>
      <path className="ua-draw text-accent" pathLength={1} d="M28 112 C48 -10 84 -6 100 64 S152 138 172 16" {...S} />
      {[49, 100, 151].map((x, i) => (
        <circle key={x} cx={x} cy="64" r="5" fill="currentColor" className="ua-blink text-primary" style={{ animationDelay: `${300 + i * 150}ms`, transformOrigin: `${x}px 64px` }} />
      ))}
    </>
  ),
  // An ellipse with its foci; a point travels around it
  conics: () => (
    <>
      <ellipse cx="100" cy="60" rx="66" ry="38" className="text-accent" {...S} />
      <circle cx="49" cy="60" r="3" fill="currentColor" className="text-muted" />
      <circle cx="151" cy="60" r="3" fill="currentColor" className="text-muted" />
      <circle
        className="ua-trace ua-loop text-primary"
        r="5"
        fill="currentColor"
        style={{ offsetPath: "path('M166 60 A66 38 0 1 1 34 60 A66 38 0 1 1 166 60')" }}
      />
    </>
  ),
  // Bars that grow like a geometric sequence
  sequences_series: () => (
    <>
      <line x1="20" y1="104" x2="180" y2="104" {...faint} />
      {[6, 10, 16, 26, 42, 68, 88].map((h, i) => (
        <rect
          key={i}
          x={26 + i * 22}
          y={104 - h}
          width="14"
          height={h}
          rx="2"
          fill="currentColor"
          className={`ua-grow ${i % 2 ? "text-primary" : "text-accent"}`}
          style={{ animationDelay: `${i * 70}ms`, transformOrigin: `${33 + i * 22}px 104px` }}
        />
      ))}
    </>
  ),
};

export function UnitArt({ unitId, className = "" }: { unitId: string; className?: string }) {
  const Art = arts[unitId];
  if (!Art) return null;
  return (
    <svg viewBox="0 0 200 120" className={`unit-art h-full w-full ${className}`} aria-hidden>
      <Art />
    </svg>
  );
}
