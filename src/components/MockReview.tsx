"use client";

import { BookOpen, Dumbbell, Flame } from "lucide-react";
import Link from "next/link";
import { useMemo, useState } from "react";
import type { ChoiceKey, MockProblem } from "@/lib/content/schema";
import { findSkill } from "@/lib/content/types";
import { useApp } from "./AppProvider";
import { Markdown } from "./Markdown";
import { CHOICE_KEYS, ChoiceButton, SolutionPanel } from "./problem";

type Status = "Correct" | "Wrong" | "Blank";
type Filter = "all" | "missed" | "Wrong" | "Blank" | "Correct";

const statusOf = (p: MockProblem, a: ChoiceKey | null | undefined): Status => (!a ? "Blank" : a === p.answer ? "Correct" : "Wrong");

const badge: Record<Status, string> = {
  Correct: "bg-correct/15 text-correct",
  Wrong: "bg-wrong/15 text-wrong",
  Blank: "bg-surface-2 text-muted",
};

/** Section names that match how hard each level feels on the real test. */
const sectionLabel = (difficulty: number) =>
  difficulty <= 2 ? "Warmup" : difficulty <= 4 ? "Middle" : difficulty <= 6 ? "Hard" : "Hardest";

/**
 * Every question from one mock exam: what you answered, the solution, which unit and skill it tests,
 * and the lesson and practice pages to study before trying questions like it again.
 */
export function MockReview({ problems, answers }: { problems: MockProblem[]; answers: Record<string, ChoiceKey | null> }) {
  const { index } = useApp();
  const [filter, setFilter] = useState<Filter>("all");

  const rows = useMemo(
    () =>
      problems.map((p, n) => {
        const found = findSkill(index, p.skillId);
        const unitId = found?.unit.id ?? p.topic;
        return {
          p,
          n: n + 1,
          status: statusOf(p, answers[p.id]),
          unitId,
          unitTitle: found?.unit.title ?? p.topic,
          skillTitle: found?.skill.title ?? p.skillId,
          lesson: `/learn/${unitId}/${p.skillId}`,
        };
      }),
    [problems, answers, index],
  );

  // Missed questions grouped by skill, with the most missed first
  const focus = useMemo(() => {
    const m = new Map<string, { unitTitle: string; skillTitle: string; lesson: string; numbers: number[] }>();
    for (const r of rows) {
      if (r.status === "Correct") continue;
      const cur = m.get(r.p.skillId) ?? { unitTitle: r.unitTitle, skillTitle: r.skillTitle, lesson: r.lesson, numbers: [] };
      cur.numbers.push(r.n);
      m.set(r.p.skillId, cur);
    }
    return [...m.values()].sort((a, b) => b.numbers.length - a.numbers.length || a.numbers[0] - b.numbers[0]);
  }, [rows]);

  const counts = {
    all: rows.length,
    missed: rows.filter((r) => r.status !== "Correct").length,
    Wrong: rows.filter((r) => r.status === "Wrong").length,
    Blank: rows.filter((r) => r.status === "Blank").length,
    Correct: rows.filter((r) => r.status === "Correct").length,
  };
  const shown = rows.filter((r) => (filter === "all" ? true : filter === "missed" ? r.status !== "Correct" : r.status === filter));
  const tabs: { id: Filter; label: string }[] = [
    { id: "all", label: "All" },
    { id: "missed", label: "Missed" },
    { id: "Wrong", label: "Wrong" },
    { id: "Blank", label: "Blank" },
    { id: "Correct", label: "Correct" },
  ];

  return (
    <>
      <h2 className="mt-10 text-xl font-bold">What to review</h2>
      {focus.length === 0 ? (
        <p className="mt-4 rounded-lg border border-line bg-surface px-5 py-4 text-body">You got every question right. Nothing to review here.</p>
      ) : (
        <>
          <p className="mt-1 text-sm text-muted">Skills behind the questions you missed or left blank, most missed first.</p>
          <ul className="mt-4 divide-y divide-line rounded-lg border border-line bg-surface">
            {focus.map((f) => (
              <li key={f.lesson} className="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="font-semibold text-heading">{f.skillTitle}</p>
                  <p className="text-sm text-muted">
                    {f.unitTitle} · {f.numbers.length === 1 ? "Question" : "Questions"} {f.numbers.join(", ")}
                  </p>
                </div>
                <div className="flex shrink-0 flex-wrap gap-2">
                  <StudyLink href={f.lesson} icon="lesson">
                    Lesson
                  </StudyLink>
                  <StudyLink href={`${f.lesson}/practice/basics`} icon="basics">
                    Basics
                  </StudyLink>
                  <StudyLink href={`${f.lesson}/practice/challenge`} icon="challenge">
                    Challenge
                  </StudyLink>
                </div>
              </li>
            ))}
          </ul>
        </>
      )}

      <h2 className="mt-10 text-xl font-bold">Every question</h2>
      <div className="mt-4 flex flex-wrap gap-2" role="tablist" aria-label="Filter questions">
        {tabs.map((t) => (
          <button
            key={t.id}
            role="tab"
            aria-selected={filter === t.id}
            onClick={() => setFilter(t.id)}
            className={`rounded-full border px-3 py-1 text-sm font-semibold transition-colors ${
              filter === t.id ? "border-accent bg-accent/15 text-heading" : "border-line text-muted hover:text-heading"
            }`}
          >
            {t.label} <span className="tabular-nums opacity-70">{counts[t.id]}</span>
          </button>
        ))}
      </div>

      <div className="mt-4 space-y-3">
        {shown.length === 0 && <p className="rounded-lg border border-dashed border-line px-5 py-6 text-center text-muted">No questions here.</p>}
        {shown.map(({ p, n, status, unitTitle, skillTitle, lesson }) => {
          const a = answers[p.id] ?? null;
          return (
            <details key={p.id} className="group rounded-lg border border-line bg-surface">
              <summary className="flex cursor-pointer list-none items-center gap-3 px-5 py-4">
                <span className="font-display font-bold text-heading tabular-nums">{n}.</span>
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-body">
                    <Markdown inline>{p.prompt.split("\n")[0]}</Markdown>
                  </span>
                  <span className="mt-0.5 block truncate text-xs text-muted">
                    {unitTitle} · {skillTitle}
                  </span>
                </span>
                <span className={`shrink-0 rounded-full px-2.5 py-0.5 text-xs font-semibold ${badge[status]}`}>{status}</span>
              </summary>
              <div className="space-y-4 border-t border-line px-5 py-5">
                <div className="flex flex-wrap gap-2 text-xs">
                  <span className="rounded-full border border-line px-2.5 py-0.5 text-body">{unitTitle}</span>
                  <span className="rounded-full border border-line px-2.5 py-0.5 text-body">{skillTitle}</span>
                  <span className="rounded-full border border-line px-2.5 py-0.5 text-muted">{sectionLabel(p.difficulty)} section</span>
                </div>
                <Markdown className="text-heading">{p.prompt}</Markdown>
                <div className="grid gap-2">
                  {CHOICE_KEYS.map((k) => (
                    <ChoiceButton
                      key={k}
                      letter={k}
                      content={p.choices[k]}
                      disabled
                      state={k === p.answer ? (a === k ? "correct" : "answer") : a === k ? "wrong" : "idle"}
                    />
                  ))}
                </div>
                <p className="text-sm text-muted">
                  {status === "Blank" ? "You left this blank." : `You answered ${a}.`} The answer is {p.answer}.
                </p>
                <SolutionPanel solution={p.solution} />
                <div className="rounded-lg border border-accent/30 bg-accent/5 p-4">
                  <p className="font-semibold text-heading">Prepare for questions like this</p>
                  <p className="mt-1 text-sm text-body">
                    This question tests <strong className="text-heading">{skillTitle}</strong> from the {unitTitle} unit. Read the lesson, then
                    practice until the idea feels automatic.
                  </p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <StudyLink href={lesson} icon="lesson">
                      Read the lesson
                    </StudyLink>
                    <StudyLink href={`${lesson}/practice/basics`} icon="basics">
                      Practice basics
                    </StudyLink>
                    <StudyLink href={`${lesson}/practice/challenge`} icon="challenge">
                      Try the challenge set
                    </StudyLink>
                  </div>
                </div>
              </div>
            </details>
          );
        })}
      </div>
    </>
  );
}

function StudyLink({ href, icon, children }: { href: string; icon: "lesson" | "basics" | "challenge"; children: React.ReactNode }) {
  const Icon = icon === "lesson" ? BookOpen : icon === "basics" ? Dumbbell : Flame;
  return (
    <Link
      href={href}
      className="inline-flex items-center gap-1.5 rounded-md border border-line bg-surface-2 px-3 py-1.5 text-sm font-semibold text-body transition-colors hover:border-accent hover:text-heading"
    >
      <Icon aria-hidden className="h-4 w-4" />
      {children}
    </Link>
  );
}
