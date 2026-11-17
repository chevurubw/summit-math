import type { Problem } from "@/lib/content/schema";
import type { Attempt } from "@/lib/store/types";
import { shuffle } from "@/lib/scoring";

/**
 * Picks `count` problems for a practice set.
 *
 * Problems of the same type (family) differ only in their numbers, so the picker spreads types out:
 * 1. A set never has two problems of the same type, when the bank has enough types.
 * 2. Once a type is done, it is put away until the student has done every other type in the bank.
 * 3. No exact problem repeats until every problem in the bank has been shown once.
 * 4. Otherwise, the type seen least recently comes first.
 * Uses the student's answer history, so it works across visits and devices.
 */
export function pickFresh(pool: Problem[], attempts: Attempt[], count: number): Problem[] {
  if (pool.length === 0) return [];
  const byId = new Map(pool.map((p) => [p.id, p]));
  const fam = (p: Problem) => p.family ?? p.id;

  // Walk the history in order. Two cycles are tracked:
  // the type cycle (a type, once done, is put away until every other type has been done) and
  // the problem cycle (no exact problem repeats until the whole bank has been shown).
  const typeCount = new Set(pool.map(fam)).size;
  let seenTypes = new Set<string>();
  let seen = new Set<string>();
  const lastSeen = new Map<string, number>();
  attempts.forEach((a, i) => {
    const p = byId.get(a.problemId);
    if (!p) return;
    seenTypes.add(fam(p));
    if (seenTypes.size === typeCount) seenTypes = new Set();
    seen.add(p.id);
    if (seen.size === pool.length) seen = new Set();
    lastSeen.set(fam(p), i);
  });

  // Random order first, then a stable sort by the rules above, so ties are broken at random
  const ranked = shuffle(pool).sort((a, b) => {
    const ta = Number(seenTypes.has(fam(a)));
    const tb = Number(seenTypes.has(fam(b)));
    if (ta !== tb) return ta - tb;
    const sa = Number(seen.has(a.id));
    const sb = Number(seen.has(b.id));
    if (sa !== sb) return sa - sb;
    return (lastSeen.get(fam(a)) ?? -1) - (lastSeen.get(fam(b)) ?? -1);
  });

  const chosen: Problem[] = [];
  const usedTypes = new Set<string>();
  // First pass: one problem per type
  for (const p of ranked) {
    if (chosen.length === count) break;
    if (usedTypes.has(fam(p))) continue;
    chosen.push(p);
    usedTypes.add(fam(p));
  }
  // Only if the bank has fewer types than the set size: fill the rest with unused problems
  for (const p of ranked) {
    if (chosen.length === Math.min(count, pool.length)) break;
    if (!chosen.includes(p)) chosen.push(p);
  }
  return shuffle(chosen);
}
