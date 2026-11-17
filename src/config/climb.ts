// The climb: students gain altitude (0 to 10,000 m) as their skill mastery grows.
// Edit camp names, heights, mock exam gates, and unlockable rewards here.

export const SUMMIT_HEIGHT = 10000;

// The climb has two parts:
//   Core skills (on both tests) take you from 0 m up to the AMC 10 Summit.
//   AMC 12 only skills take you the rest of the way, from the AMC 10 Summit to the AMC 12 Summit.
export const AMC10_SUMMIT_HEIGHT = 7500;

export type Camp = {
  height: number;
  name: string;
  note: string;
  /** Marks the two summits so the mountain draws them as peaks with flags */
  peak?: "amc10" | "amc12";
};

// Named milestones on the way up. Heights must go from low to high.
export const camps: Camp[] = [
  { height: 0, name: "Trailhead", note: "Every climb starts with one skill." },
  { height: 1000, name: "Base Camp", note: "You have your footing. Keep building the basics." },
  { height: 2500, name: "Tree Line", note: "The forest ends and the real climbing starts here." },
  { height: 4000, name: "Boulder Field", note: "Rough ground, steady progress." },
  { height: 5500, name: "Cloud Pass", note: "Above the clouds. Mistakes cost more up here." },
  { height: 7000, name: "Icefall", note: "Careful footing. The AMC 10 Summit is in sight." },
  {
    height: AMC10_SUMMIT_HEIGHT,
    name: "AMC 10 Summit",
    note: "Every core skill mastered and an AIME level AMC 10 score. The AMC 12 peak is next.",
    peak: "amc10",
  },
  { height: 8500, name: "Knife Ridge", note: "Thin air and a narrow path. AMC 12 only skills from here." },
  {
    height: SUMMIT_HEIGHT,
    name: "AMC 12 Summit",
    note: "Every skill on both tests mastered, with an AIME level AMC 12 score.",
    peak: "amc12",
  },
];

export type Gate =
  | { height: number; kind: "mockTaken"; label: string }
  | {
      height: number;
      kind: "mockScore";
      min: number;
      /** Only count AMC 10 or AMC 12 mocks */
      track?: "amc10" | "amc12";
      /** Only count full length (25 question) mocks. Otherwise shorter mocks are scaled to 150. */
      fullLengthOnly?: boolean;
      /** Consistency: need the score on this many of the most recent mocks (for example 2 of the last 3) */
      times?: number;
      ofLast?: number;
      label: string;
    };

// Checkpoints you cannot climb past until you prove it on mock exams.
// The top checkpoints need full length mocks and the score more than once, so one lucky exam is not enough.
export const gates: Gate[] = [
  { height: 2500, kind: "mockTaken", label: "Take any mock exam" },
  { height: 5500, kind: "mockScore", min: 60, track: "amc10", label: "Score 60 or more on an AMC 10 mock exam" },
  {
    height: 7000,
    kind: "mockScore",
    min: 100,
    track: "amc10",
    fullLengthOnly: true,
    times: 2,
    ofLast: 3,
    label: "Score 100 or more on 2 of your last 3 full AMC 10 mocks",
  },
  {
    height: 8500,
    kind: "mockScore",
    min: 85,
    track: "amc12",
    fullLengthOnly: true,
    times: 2,
    ofLast: 3,
    label: "Score 85 or more on 2 of your last 3 full AMC 12 mocks",
  },
  {
    height: 9500,
    kind: "mockScore",
    min: 100,
    track: "amc12",
    fullLengthOnly: true,
    times: 2,
    ofLast: 3,
    label: "Score 100 or more on 2 of your last 3 full AMC 12 mocks",
  },
];

export type ThemeId = "summit" | "glacier" | "alpenglow" | "pine" | "aurora" | "gold";

// Color schemes. The colors themselves live in src/app/theme.css.
export const themes: { id: ThemeId; name: string; unlockAt: number; swatch: [string, string] }[] = [
  { id: "summit", name: "Summit Red", unlockAt: 0, swatch: ["#dc2626", "#8b5cf6"] },
  { id: "glacier", name: "Glacier", unlockAt: 1000, swatch: ["#2563eb", "#22d3ee"] },
  { id: "alpenglow", name: "Alpenglow", unlockAt: 2500, swatch: ["#ea580c", "#f472b6"] },
  { id: "pine", name: "Pine", unlockAt: 4000, swatch: ["#0d9488", "#fbbf24"] },
  { id: "aurora", name: "Aurora", unlockAt: 7500, swatch: ["#7c3aed", "#38bdf8"] },
  { id: "gold", name: "Summit Gold", unlockAt: 10000, swatch: ["#a16207", "#fde047"] },
];

export type AvatarId = "initial" | "tent" | "backpack" | "compass" | "pickaxe" | "snowflake" | "peak" | "flag";

// Profile icons. The pictures are chosen in src/components/Avatar.tsx.
export const avatars: { id: AvatarId; name: string; unlockAt: number }[] = [
  { id: "initial", name: "Your initial", unlockAt: 0 },
  { id: "tent", name: "Tent", unlockAt: 1000 },
  { id: "backpack", name: "Pack", unlockAt: 2500 },
  { id: "compass", name: "Compass", unlockAt: 5500 },
  { id: "pickaxe", name: "Ice axe", unlockAt: 7000 },
  { id: "snowflake", name: "Snowflake", unlockAt: 8500 },
  { id: "peak", name: "Peak", unlockAt: 7500 },
  { id: "flag", name: "Summit flag", unlockAt: 10000 },
];
