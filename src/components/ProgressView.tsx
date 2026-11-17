"use client";

import { ChevronDown } from "lucide-react";
import Link from "next/link";
import { examConfig, TRACK_LABELS } from "@/config/exam";
import { MASTERY_POINTS } from "@/config/mastery";
import { scaledMockScore } from "@/lib/climb";
import type { CourseSkill, CourseUnit } from "@/lib/content/types";
import { useApp } from "./AppProvider";
import { ClimbPanel } from "./climb";
import { Amc12Marker } from "./course";
import { LineChart } from "./LineChart";
import { MasteryBadge, MasteryLegend, ProgressBar } from "./progress";
import { Card } from "./ui";

type Group = { unit: CourseUnit; skills: CourseSkill[] };

/** The Climb page: mastery and scores on the left, the mountain on the right. */
export function ClimbView() {
  const { data, levelOf, index } = useApp();
  if (!data) return null;

  // Split skills into the shared core and AMC 12 only
  const core: Group[] = [];
  const amc12: Group[] = [];
  for (const unit of index.units) {
    const c = unit.skills.filter((s) => !s.amc12Only);
    const t = unit.skills.filter((s) => s.amc12Only);
    if (unit.track === "both" || c.length) core.push({ unit, skills: c });
    if (unit.track === "amc12" || t.length) amc12.push({ unit, skills: t });
  }

  // Accuracy by unit from every answered problem
  const skillUnit = new Map<string, string>();
  index.units.forEach((u) => u.skills.forEach((s) => skillUnit.set(s.id, u.id)));
  const acc = new Map<string, { correct: number; total: number }>();
  for (const a of data.attempts) {
    const u = skillUnit.get(a.skillId);
    if (!u) continue;
    const v = acc.get(u) ?? { correct: 0, total: 0 };
    v.total++;
    if (a.correct) v.correct++;
    acc.set(u, v);
  }
  const accuracy = index.units
    .filter((u) => acc.has(u.id))
    .map((u) => ({ unit: u, ...acc.get(u.id)! }))
    .sort((a, b) => a.correct / a.total - b.correct / b.total);

  const mocks = data.mocks;
  const full = examConfig.questionCount * examConfig.scoring.correct;

  return (
    <div className="grid gap-8 lg:grid-cols-[1fr_1.12fr]">
      {/* Mountain first on phones, on the right on wide screens */}
      <div className="lg:order-2">
        <ClimbPanel />
      </div>

      <div className="min-w-0 space-y-6 lg:order-1">
        <div>
          <h1 className="text-4xl font-bold">Your climb</h1>
          <p className="mt-2 text-muted">
            Every skill you master lifts you higher. Mock exams unlock the checkpoints on the way to the summit.
          </p>
        </div>

        <MasteryGroup
          title="Core skills"
          subtitle="On both the AMC 10 and the AMC 12"
          groups={core}
          levelOf={levelOf}
          defaultOpen
        />
        <MasteryGroup
          title="AMC 12 only skills"
          subtitle="Tracked separately. Only needed for the AMC 12."
          groups={amc12}
          levelOf={levelOf}
          amc12
        />

        <Card className="p-6">
          <h2 className="text-xl font-bold">Mock exam scores</h2>
          <p className="mt-1 text-sm text-muted">Scaled to a full {full} point exam.</p>
          {mocks.length === 0 ? (
            <p className="mt-3 text-muted">
              Take a{" "}
              <Link href="/mock" className="text-accent-soft hover:underline">
                mock exam
              </Link>{" "}
              to start tracking your score and unlock the first checkpoint.
            </p>
          ) : (
            <div className="mt-4">
              <LineChart
                points={mocks.map((m) => ({
                  label: `${new Date(m.at).toLocaleDateString(undefined, { month: "short", day: "numeric" })} ${TRACK_LABELS[m.track].replace("AMC ", "")}`,
                  value: scaledMockScore(m),
                }))}
                max={full}
                target={examConfig.aimeCutoffs.amc12}
                targetLabel={`AMC 12 AIME cutoff ${examConfig.aimeCutoffs.amc12}`}
              />
            </div>
          )}
        </Card>

        <Card className="p-6">
          <h2 className="text-xl font-bold">Accuracy by topic</h2>
          <p className="mt-1 text-sm text-muted">Weakest topics first.</p>
          {accuracy.length === 0 ? (
            <p className="mt-3 text-muted">Answer some problems to see your accuracy by topic.</p>
          ) : (
            <div className="mt-5 space-y-4">
              {accuracy.map((a) => {
                const pct = a.correct / a.total;
                return (
                  <div key={a.unit.id}>
                    <div className="mb-1 flex justify-between gap-3 text-sm">
                      <span className="text-heading">
                        {a.unit.title}
                        {pct < 0.6 && <span className="ml-2 text-xs font-semibold text-primary">Needs work</span>}
                      </span>
                      <span className="text-muted tabular-nums">
                        {Math.round(pct * 100)}% of {a.total}
                      </span>
                    </div>
                    <ProgressBar value={pct} color={pct < 0.6 ? "primary" : "accent"} />
                  </div>
                );
              })}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

function MasteryGroup({
  title,
  subtitle,
  groups,
  levelOf,
  defaultOpen,
  amc12,
}: {
  title: string;
  subtitle: string;
  groups: Group[];
  levelOf: (id: string) => import("@/config/mastery").MasteryLevel;
  defaultOpen?: boolean;
  amc12?: boolean;
}) {
  const skills = groups.flatMap((g) => g.skills);
  const pct = skills.length ? skills.reduce((s, sk) => s + MASTERY_POINTS[levelOf(sk.id)], 0) / (skills.length * 100) : 0;
  const mastered = skills.filter((s) => levelOf(s.id) === "mastered").length;

  return (
    <details open={defaultOpen} className="group rounded-lg border border-line bg-surface">
      <summary className="flex cursor-pointer list-none items-center gap-4 p-6">
        <div className="min-w-0 flex-1">
          <h2 className="flex items-center gap-2 text-xl font-bold">
            {title}
            {amc12 && <Amc12Marker inline />}
          </h2>
          <p className="text-sm text-muted">{subtitle}</p>
          <div className="mt-3 flex items-center gap-3">
            <ProgressBar value={pct} />
            <span className="shrink-0 text-sm font-semibold tabular-nums text-heading">{Math.round(pct * 100)}%</span>
          </div>
          <p className="mt-1 text-xs text-muted">
            {mastered} of {skills.length} skills mastered
          </p>
        </div>
        <ChevronDown className="h-5 w-5 shrink-0 text-muted transition-transform group-open:rotate-180" aria-hidden />
      </summary>
      <div className="anim-rise space-y-5 border-t border-line px-6 py-5">
        <MasteryLegend />
        {groups.map(({ unit, skills: list }) => (
          <div key={unit.id}>
            <div className="mb-2 flex items-center justify-between gap-3">
              <Link href={`/learn/${unit.id}`} className="font-display font-bold text-heading hover:underline">
                {unit.title}
              </Link>
            </div>
            {list.length === 0 ? (
              <p className="text-sm text-muted">Skills coming soon</p>
            ) : (
              <ul className="grid gap-2 sm:grid-cols-2">
                {list.map((s) => (
                  <li key={s.id} className="flex items-center justify-between gap-3 rounded-md bg-surface-2 px-3 py-2">
                    <Link href={`/learn/${unit.id}/${s.id}`} className="truncate text-sm text-heading hover:underline">
                      {s.title}
                    </Link>
                    <MasteryBadge level={levelOf(s.id)} compact />
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </details>
  );
}
