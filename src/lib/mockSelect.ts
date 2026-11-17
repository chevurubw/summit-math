import type { Track } from "@/config/exam";
import type { MockProblem } from "@/lib/content/schema";
import type { MockExamRecord } from "@/lib/store/types";

/**
 * Builds one mock exam: 25 problems in five sections of five, getting harder like the real test.
 *
 * Difficulty levels follow the AoPS competition ratings. The AMC 12 runs about one section
 * harder than the AMC 10, so:
 *   AMC 10 sections use levels 1, 2, 3, 4, 5
 *   AMC 12 sections use levels 2, 3, 4, 5, 6, with two AMC 12 only topics in each section
 *
 * Rules, in order of importance:
 *   1. Nothing from the student's previous mock: no problem, and no problem family
 *      (so no problem that is an old one with new numbers).
 *   2. Families the student has not seen in a mock come first, then the ones seen longest ago.
 *   3. Topics are balanced like a real exam.
 *   4. Within a family, problems the student has never seen in a mock come first.
 */

export const mockSections: Record<Track, number[]> = {
  amc10: [1, 2, 3, 4, 5],
  amc12: [2, 3, 4, 5, 6],
};

/** How many AMC 12 only problems go in each AMC 12 section. */
const AMC12_ONLY_PER_SECTION = 2;

/** Rough topic counts for the shared problems on a real exam. */
const topicTargets: Record<Track, Record<string, number>> = {
  amc10: { algebra: 8, geometry: 7, number_theory: 5, counting_probability: 5 },
  amc12: { algebra: 4, geometry: 5, number_theory: 3, counting_probability: 3 },
};

const PER_SECTION = 5;

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

  return mockSections[track].map((level) => {
    const slots: boolean[] = [];
    const nOnly = track === "amc12" ? AMC12_ONLY_PER_SECTION : 0;
    for (let i = 0; i < PER_SECTION; i++) slots.push(i < nOnly);
    const problems: MockProblem[] = [];
    for (const amc12Only of slots) {
      const f = pickFamily(level, amc12Only) ?? pickFamily(level, !amc12Only);
      if (!f) continue;
      chosenFamilies.add(f);
      const p = pickProblem(f);
      topicCount.set(p.topic, (topicCount.get(p.topic) ?? 0) + 1);
      problems.push(p);
    }
    // Mix the order inside a section so AMC 12 topics are not always first
    for (let i = problems.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [problems[i], problems[j]] = [problems[j], problems[i]];
    }
    return { level, problems };
  });
}
