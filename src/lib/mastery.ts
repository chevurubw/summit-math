import {
  MASTERY_LEVELS,
  MASTERY_POINTS,
  masteryRules,
  type MasteryLevel,
} from "@/config/mastery";

export type SessionKind = "basics" | "challenge" | "quiz" | "test";

const rank = (l: MasteryLevel) => MASTERY_LEVELS.indexOf(l);
const atRank = (r: number) => MASTERY_LEVELS[Math.max(0, Math.min(MASTERY_LEVELS.length - 1, r))];
const maxLevel = (a: MasteryLevel, b: MasteryLevel) => (rank(a) >= rank(b) ? a : b);

/** Works out a skill's new level after a session, using the rules in config/mastery.ts. */
export function nextLevel(current: MasteryLevel, kind: SessionKind, score: number): MasteryLevel {
  const p = masteryRules.practice;
  const q = masteryRules.quizAndTest;

  if (kind === "basics") {
    const result: MasteryLevel = score >= p.basicsFamiliarScore ? "familiar" : "attempted";
    return maxLevel(current, result);
  }

  if (kind === "challenge") {
    const result: MasteryLevel = score >= p.challengeProficientScore ? "proficient" : "attempted";
    return maxLevel(current, result);
  }

  // Quiz or unit test
  const cap = kind === "quiz" ? q.highestLevelFromQuiz : q.highestLevelFromTest;
  if (score >= q.levelUpScore) {
    if (current === "not_started") return maxLevel("familiar", current);
    if (rank(current) >= rank(cap)) return current;
    return atRank(rank(current) + 1);
  }
  if (score < q.levelDownScore) {
    if (current === "not_started") return "attempted";
    const dropped = atRank(rank(current) - 1);
    return rank(dropped) < rank(q.lowestLevelAfterDrop) ? q.lowestLevelAfterDrop : dropped;
  }
  return current === "not_started" ? "attempted" : current;
}

/**
 * A skill's level after review fading: Proficient and Mastered skills that have not been
 * practiced for masteryRules.reviewAfterDays show as one level lower until reviewed.
 */
export function effectiveLevel(level: MasteryLevel, updatedAt: string | undefined, now?: number) {
  if (!updatedAt || rank(level) < rank("proficient")) return { level, reviewDue: false };
  const days = ((now ?? Date.now()) - new Date(updatedAt).getTime()) / 86400000;
  if (days < masteryRules.reviewAfterDays) return { level, reviewDue: false };
  return { level: atRank(rank(level) - 1), reviewDue: true };
}

export function levelPoints(level: MasteryLevel) {
  return MASTERY_POINTS[level];
}

export function levelRank(level: MasteryLevel) {
  return rank(level);
}
