/**
 * A quiet mountain range along the bottom of the screen, with faint gusts of wind drifting across the whole site,
 * behind everything.
 * Pure SVG and CSS (see "Wind" in globals.css); it holds still for people who prefer less motion.
 */

// Each gust: a soft wavy line across the screen, with its own height, speed and start time.
const gusts = [
  { y: 8, amp: 10, dur: 14, delay: 0, len: 0.16, w: 1.4 },
  { y: 18, amp: 6, dur: 19, delay: -6, len: 0.1, w: 1 },
  { y: 27, amp: 12, dur: 16, delay: -11, len: 0.18, w: 1.6 },
  { y: 38, amp: 8, dur: 22, delay: -3, len: 0.12, w: 1 },
  { y: 47, amp: 14, dur: 15, delay: -9, len: 0.2, w: 1.5 },
  { y: 58, amp: 7, dur: 20, delay: -15, len: 0.1, w: 1 },
  { y: 67, amp: 11, dur: 17, delay: -5, len: 0.16, w: 1.4 },
  { y: 78, amp: 9, dur: 23, delay: -13, len: 0.12, w: 1.1 },
  { y: 88, amp: 13, dur: 18, delay: -8, len: 0.18, w: 1.5 },
  { y: 96, amp: 6, dur: 21, delay: -17, len: 0.1, w: 1 },
];

function wave(y: number, amp: number) {
  // Coordinates in a 1000 by 100 box, stretched to the screen
  const yy = y;
  return `M-100 ${yy} C 100 ${yy - amp}, 250 ${yy + amp}, 400 ${yy} S 700 ${yy - amp}, 850 ${yy} S 1050 ${yy + amp * 0.6}, 1150 ${yy}`;
}

// Three ridgelines in a 1600 by 400 box, back to front. Each is filled with the page color so nearer ranges hide
// the lines of the ranges behind them, leaving only outlines.
const ranges = [
  {
    d: "M0 250 L120 200 L210 230 L330 140 L420 190 L520 120 L600 170 L700 95 L790 160 L880 130 L980 185 L1080 110 L1180 165 L1290 125 L1380 180 L1480 150 L1600 200 V400 H0 Z",
    detail: "M700 95 L728 150 L716 190 M520 120 L540 170 M1080 110 L1102 160 L1094 195 M330 140 L348 185",
    tone: "mtn-back",
  },
  {
    d: "M0 300 L90 270 L200 300 L310 230 L400 275 L500 215 L590 260 L720 190 L840 265 L960 225 L1060 280 L1170 215 L1290 270 L1400 240 L1500 285 L1600 255 V400 H0 Z",
    detail: "M720 190 L742 235 M1170 215 L1190 255 M310 230 L326 268",
    tone: "mtn-mid",
  },
  {
    d: "M0 350 L140 320 L260 345 L380 300 L500 340 L640 310 L780 350 L900 315 L1040 345 L1160 305 L1300 340 L1440 315 L1600 345 V400 H0 Z",
    detail: "",
    tone: "mtn-front",
  },
];

export function WindBackground() {
  return (
    <div aria-hidden className="wind pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <svg className="absolute inset-x-0 bottom-0 h-[42vh] w-full" viewBox="0 0 1600 400" preserveAspectRatio="xMidYMax slice">
        {ranges.map((m) => (
          <g key={m.tone} className={`mtn ${m.tone}`}>
            <path d={m.d} />
            {m.detail && <path d={m.detail} className="mtn-detail" />}
          </g>
        ))}
      </svg>
      <svg className="absolute inset-0 h-full w-full" viewBox="0 0 1000 100" preserveAspectRatio="none">
        {gusts.map((g, i) => (
          <path
            key={i}
            d={wave(g.y, g.amp)}
            pathLength={1}
            vectorEffect="non-scaling-stroke"
            strokeWidth={g.w}
            className="wind-gust"
            style={{
              strokeDasharray: `${g.len} ${1 - g.len + 0.35}`,
              animationDuration: `${g.dur}s`,
              animationDelay: `${g.delay}s`,
            }}
          />
        ))}
      </svg>
    </div>
  );
}
