import {
  AMC10_SUMMIT_HEIGHT,
  avatars,
  camps,
  gates,
  SUMMIT_HEIGHT,
  themes,
  type Camp,
  type Gate,
} from "@/config/climb";
import { examConfig } from "@/config/exam";
import { MASTERY_LABELS, MASTERY_LEVELS, MASTERY_POINTS, type MasteryLevel } from "@/config/mastery";
import { allSkills, type CourseIndex } from "@/lib/content/types";
import type { MockExamRecord } from "@/lib/store/types";

export type GateStatus = Gate & { met: boolean; progress: string };

export type Suggestion = {
  unitId: string;
  skillId: string;
  title: string;
  from: MasteryLevel;
  to: MasteryLevel;
  gain: number; // meters
  /** The skill faded from not being practiced and needs review */
  review: boolean;
};

export type Climb = {
  /** Altitude earned from mastery alone */
  earned: number;
  /** Altitude after mock exam gates are applied */
  altitude: number;
  camp: Camp;
  nextCamp: Camp | null;
  /** The gate currently holding the student back, if any */
  blockedBy: GateStatus | null;
  gates: GateStatus[];
  bestMock: number | null; // scaled to 150
  /** Whether every core skill is done and the AMC 10 Summit is reached */
  amc10SummitReached: boolean;
  suggestions: Suggestion[];
};

/** Mock exam score scaled to a full length exam, so shorter exams still count. */
export function scaledMockScore(m: MockExamRecord) {
  const full = examConfig.questionCount * examConfig.scoring.correct;
  return m.maxScore > 0 ? Math.round((m.score / m.maxScore) * full * 10) / 10 : 0;
}

export function computeClimb(
  index: CourseIndex,
  levelOf: (skillId: string) => MasteryLevel,
  mocks: MockExamRecord[],
  reviewDue: (skillId: string) => boolean = () => false,
): Climb {
  // Core skills fill the climb up to the AMC 10 Summit; AMC 12 only skills fill the rest
  const everySkill = allSkills(index);
  const core = everySkill.filter(({ skill }) => !skill.amc12Only);
  const extra = everySkill.filter(({ skill }) => skill.amc12Only);
  const coreMeters = core.length ? AMC10_SUMMIT_HEIGHT / core.length : 0;
  const extraMeters = extra.length ? (SUMMIT_HEIGHT - AMC10_SUMMIT_HEIGHT) / extra.length : 0;
  const metersFor = (amc12Only: boolean) => (amc12Only ? extraMeters : coreMeters);

  const earned = Math.round(
    everySkill.reduce((sum, { skill }) => sum + (MASTERY_POINTS[levelOf(skill.id)] / 100) * metersFor(skill.amc12Only), 0),
  );

  const bestMock = mocks.length ? Math.max(...mocks.map(scaledMockScore)) : null;
  const fullScore = examConfig.questionCount * examConfig.scoring.correct;
  const gateStatus: GateStatus[] = gates.map((g) => {
    if (g.kind === "mockTaken") {
      const met = mocks.length > 0;
      return { ...g, met, progress: met ? "Done" : "No mock exams yet" };
    }
    const which = g.track === "amc10" ? "AMC 10 " : g.track === "amc12" ? "AMC 12 " : "";
    let list = g.track ? mocks.filter((m) => m.track === g.track) : mocks;
    if (g.fullLengthOnly) list = list.filter((m) => m.maxScore >= fullScore);
    const scores = list.map(scaledMockScore); // oldest first

    if (g.times && g.ofLast) {
      const recent = scores.slice(-g.ofLast);
      const hits = recent.filter((s) => s >= g.min).length;
      const met = hits >= g.times;
      const progress = recent.length
        ? `Your last ${recent.length === 1 ? "" : recent.length + " "}full ${which}${recent.length === 1 ? "mock" : "mocks"}: ${recent.join(", ")} (${hits} of ${g.times} needed)`
        : `No full length ${which}mocks yet`;
      return { ...g, met, progress };
    }
    const b = scores.length ? Math.max(...scores) : null;
    return { ...g, met: (b ?? 0) >= g.min, progress: `Your best ${which}score: ${b === null ? "none yet" : b}` };
  });

  // The first gate that is not met caps the altitude
  const blocking = gateStatus.find((g) => !g.met && earned > g.height) ?? null;
  const altitude = blocking ? blocking.height : earned;

  let camp = camps[0];
  for (const c of camps) if (altitude >= c.height) camp = c;
  const nextCamp = camps.find((c) => c.height > altitude) ?? null;

  // Growth suggestions: the skills that would add the most altitude with one more level.
  // Core skills come first until the AMC 10 Summit is reached.
  const coreDone = core.every(({ skill }) => levelOf(skill.id) === "mastered");
  const suggestions: Suggestion[] = (coreDone ? everySkill : core)
    .map(({ unit, skill }) => {
      const from = levelOf(skill.id);
      const r = MASTERY_LEVELS.indexOf(from);
      if (r >= MASTERY_LEVELS.length - 1) return null;
      const to = MASTERY_LEVELS[r + 1];
      const gain = Math.round(((MASTERY_POINTS[to] - MASTERY_POINTS[from]) / 100) * metersFor(skill.amc12Only));
      return { unitId: unit.id, skillId: skill.id, title: skill.title, from, to, gain, review: reviewDue(skill.id) };
    })
    .filter((s): s is Suggestion => s !== null)
    .sort(
      (a, b) =>
        Number(b.review) - Number(a.review) || b.gain - a.gain || MASTERY_LEVELS.indexOf(a.from) - MASTERY_LEVELS.indexOf(b.from),
    )
    .slice(0, 3);

  return {
    earned,
    altitude,
    camp,
    nextCamp,
    blockedBy: blocking,
    gates: gateStatus,
    bestMock,
    amc10SummitReached: altitude >= AMC10_SUMMIT_HEIGHT,
    suggestions,
  };
}

export function campAt(height: number) {
  let camp = camps[0];
  for (const c of camps) if (height >= c.height) camp = c;
  return camp;
}

export function unlockedThemes(best: number) {
  return themes.filter((t) => best >= t.unlockAt);
}

export function unlockedAvatars(best: number) {
  return avatars.filter((a) => best >= a.unlockAt);
}

/** Rewards that unlock somewhere between two heights (used for unlock messages). */
/** The theme and avatar ids unlocked between two altitudes. */
export function unlocksBetween(from: number, to: number) {
  return {
    themes: themes.filter((t) => t.unlockAt > from && t.unlockAt <= to).map((t) => t.id),
    avatars: avatars.filter((a) => a.unlockAt > from && a.unlockAt <= to).map((a) => a.id),
  };
}

export function formatMeters(m: number) {
  return `${Math.round(m).toLocaleString("en-US")} m`;
}

export const levelLabel = (l: MasteryLevel) => MASTERY_LABELS[l];
