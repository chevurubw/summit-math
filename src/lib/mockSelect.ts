import type { Track } from "@/config/exam";
import type { MockProblem } from "@/lib/content/schema";
import type { MockExamRecord } from "@/lib/store/types";

/**
 * Builds one mock exam: 25 problems in five sections of five, getting harder like the real test.
 *
 * Difficulty levels (see scripts/problems/mock_common.py):
 *   1 to 4  warmups through solid middle problems
 *   5       single idea problems from the middle of the test
 *   6       harder problems from the 16 to 22 range
 *   7       true end of exam problems that chain two or three ideas
 * The AMC 12 starts a step higher than the AMC 10 and puts two AMC 12 only topics in each section.
 * Problems within a section are ordered by level, so the test ramps steadily.
 *
 * Rules, in order of importance:
 *   1. Nothing from the student's previous mock: no problem, and no problem family
 *      (so no problem that is an old one with new numbers).
 *   2. Families the student has not seen in a mock come first, then the ones seen longest ago.
 *   3. Topics are balanced like a real exam.
 *   4. Within a family, problems the student has never seen in a mock come first.
 */

/** The level of each of the five questions in each section. */
export const mockSections: Record<Track, number[][]> = {
  amc10: [
    [1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2],
    [3, 3, 4, 4, 4],
    [5, 5, 5, 6, 6],
    [6, 7, 7, 7, 7],
  ],
  amc12: [
    [2, 2, 2, 3, 3],
    [3, 3, 4, 4, 4],
    [5, 5, 5, 5, 5],
    [6, 6, 6, 6, 6],
    [7, 7, 7, 7, 7],
  ],
};

/** How many AMC 12 only problems go in each AMC 12 section. */
const AMC12_ONLY_PER_SECTION = 2;

/** Rough topic counts for the shared problems on a real exam. */
const topicTargets: Record<Track, Record<string, number>> = {
  amc10: { algebra: 8, geometry: 7, number_theory: 5, counting_probability: 5 },
  amc12: { algebra: 4, geometry: 5, number_theory: 3, counting_probability: 3 },
};


export type MockSection = { level: number; problems: MockProblem[] };

export function buildMock(
  bank: MockProblem[],
  track: Track,
  history: MockExamRecord[],
  random: () => number = Math.random,
): MockSection[] {
  const byId = new Map(bank.map((p) => [p.id, p]));
  const byFamily = new Map<string, MockProblem[]>();
  for (const p of bank) {
    const list = byFamily.get(p.family) ?? [];
    list.push(p);
    byFamily.set(p.family, list);
  }

  // Oldest first
  const past = [...history].sort((a, b) => a.at.localeCompare(b.at));
  const last = past[past.length - 1];
  const bannedIds = new Set(last ? Object.keys(last.answers) : []);
  const bannedFamilies = new Set([...bannedIds].map((id) => byId.get(id)?.family).filter((f): f is string => !!f));

  // When each family and problem was last on a mock (higher means more recent)
  const familyLastUsed = new Map<string, number>();
  const seenIds = new Set<string>();
  past.forEach((rec, i) => {
    for (const id of Object.keys(rec.answers)) {
      seenIds.add(id);
      const f = byId.get(id)?.family;
      if (f) familyLastUsed.set(f, i);
    }
  });

  const topicCount = new Map<string, number>();
  const chosenFamilies = new Set<string>();
  const targets = topicTargets[track];

  const pickFamily = (level: number, amc12Only: boolean): string | null => {
    const families = [...byFamily.entries()]
      .filter(([f, ps]) => {
        const p = ps[0];
        if (p.difficulty !== level || chosenFamilies.has(f)) return false;
        return amc12Only ? p.track === "amc12" : p.track === "both";
      })
      .map(([f, ps]) => {
        const topic = ps[0].topic;
        const have = topicCount.get(topic) ?? 0;
        // Shared topics aim for the targets; AMC 12 topics just avoid repeating
        const need = amc12Only ? -have : (targets[topic] ?? 0) - have;
        return { f, banned: bannedFamilies.has(f), last: familyLastUsed.get(f) ?? -1, need, jitter: random() };
      });
    if (families.length === 0) return null;
    families.sort(
      (a, b) =>
        Number(a.banned) - Number(b.banned) || // never repeat a family from the previous mock unless there is no other choice
        a.last - b.last || // unseen families first, then the ones seen longest ago
        b.need - a.need || // balance topics
        a.jitter - b.jitter,
    );
    return families[0].f;
  };

  const pickProblem = (family: string): MockProblem => {
    const versions = byFamily.get(family)!;
    const ranked = versions
      .map((p) => ({ p, rank: bannedIds.has(p.id) ? 2 : seenIds.has(p.id) ? 1 : 0, jitter: random() }))
      .sort((a, b) => a.rank - b.rank || a.jitter - b.jitter);
    return ranked[0].p;
  };

  // Look for a family at this level first, then nearby levels if the bank runs short
  const pickNear = (level: number, amc12Only: boolean): string | null => {
    for (const lv of [level, level - 1, level + 1, level - 2]) {
      const f = pickFamily(lv, amc12Only) ?? pickFamily(lv, !amc12Only);
      if (f) return f;
    }
    return null;
  };

  return mockSections[track].map((levels) => {
    const nOnly = track === "amc12" ? AMC12_ONLY_PER_SECTION : 0;
    const problems: MockProblem[] = [];
    levels.forEach((level, slot) => {
      const f = pickNear(level, slot < nOnly);
      if (!f) return;
      chosenFamilies.add(f);
      const p = pickProblem(f);
      topicCount.set(p.topic, (topicCount.get(p.topic) ?? 0) + 1);
      problems.push(p);
    });
    // Mix the order so AMC 12 topics are not always first, then keep it rising by level
    for (let i = problems.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [problems[i], problems[j]] = [problems[j], problems[i]];
    }
    problems.sort((a, b) => a.difficulty - b.difficulty);
    return { level: Math.max(...levels), problems };
  });
}
