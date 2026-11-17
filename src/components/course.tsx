"use client";

import Link from "next/link";
import { MASTERY_POINTS } from "@/config/mastery";
import type { CourseIndex, CourseUnit } from "@/lib/content/types";
import { useApp } from "./AppProvider";
import { MasteryBadge, ProgressBar } from "./progress";
import { UnitArt } from "./UnitArt";

export function useUnitProgress() {
  const { levelOf } = useApp();
  return (unit: CourseUnit) => {
    if (!unit.skills.length) return 0;
    const total = unit.skills.reduce((sum, s) => sum + MASTERY_POINTS[levelOf(s.id)], 0);
    return total / (unit.skills.length * 100);
  };
}

export function UnitCard({ unit, index, layout = "stack" }: { unit: CourseUnit; index: number; layout?: "wide" | "stack" }) {
  const { levelOf, user } = useApp();
  const progress = useUnitProgress()(unit);
  const empty = unit.skills.length === 0;
  const wide = layout === "wide";

  return (
    <Link
      href={`/learn/${unit.id}`}
      className={`group relative flex overflow-hidden rounded-lg border border-line bg-surface transition-colors hover:border-muted ${
        wide ? "flex-col sm:flex-row" : "flex-col"
      }`}
    >
      {unit.track === "amc12" && <Amc12Marker />}
      <div
        className={`shrink-0 border-line bg-surface-2/60 ${wide ? "h-36 border-b sm:h-auto sm:w-[42%] sm:border-b-0 sm:border-r" : "h-32 border-b"} px-4 py-3`}
      >
        <UnitArt unitId={unit.id} />
      </div>
      <div className="flex flex-1 flex-col p-5 sm:p-6">
        <span className="font-display text-sm font-semibold text-muted">Unit {index}</span>
        <h3 className="mt-1.5 text-xl font-bold group-hover:underline group-hover:decoration-primary group-hover:underline-offset-4">
          {unit.title}
        </h3>
        <p className="mt-1 line-clamp-2 text-sm text-muted">{unit.description}</p>
        <div className="mt-auto pt-5">
          {empty ? (
            <p className="text-sm text-muted">Skills coming soon</p>
          ) : (
            <>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="text-muted">
                  {unit.skills.length} {unit.skills.length === 1 ? "skill" : "skills"}
                </span>
                {user && <span className="font-semibold text-heading">{Math.round(progress * 100)}%</span>}
              </div>
              {user && <ProgressBar value={progress} />}
              {user && (
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {unit.skills.slice(0, 10).map((s) => (
                    <MasteryBadge key={s.id} level={levelOf(s.id)} compact />
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </Link>
  );
}

export function CourseMap({ index }: { index: CourseIndex }) {
  const core = index.units.filter((u) => u.track === "both");
  const extra = index.units.filter((u) => u.track === "amc12");

  return (
    <div className="space-y-12">
      <section>
        <h2 className="text-2xl font-bold">Core units</h2>
        <p className="mt-1 text-muted">On both the AMC 10 and the AMC 12.</p>
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          {core.map((u) => (
            <UnitCard key={u.id} unit={u} index={index.units.indexOf(u) + 1} layout="wide" />
          ))}
        </div>
      </section>

      {extra.length > 0 && (
        <section>
          <h2 className="flex items-center gap-2 text-2xl font-bold">
            AMC 12 units <Amc12Marker inline />
          </h2>
          <p className="mt-1 text-muted">Precalculus topics that only appear on the AMC 12. Skip these if you are taking the AMC 10.</p>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {extra.map((u) => (
              <UnitCard key={u.id} unit={u} index={index.units.indexOf(u) + 1} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

/**
 * Marks something as AMC 12 only. By default it sits in the top right corner
 * of its card (the card needs the "relative" class). Use inline next to text.
 */
export function Amc12Marker({ inline = false }: { inline?: boolean }) {
  return (
    <span
      title="Only on the AMC 12"
      className={`${
        inline ? "inline-flex" : "absolute right-0 top-0 flex rounded-bl-md rounded-tr-lg"
      } items-center rounded-sm bg-primary px-1.5 py-0.5 font-display text-[11px] font-bold leading-none text-white`}
    >
      12<span className="sr-only"> only: this is only on the AMC 12</span>
    </span>
  );
}

/** Shows a skill's mastery level, only when signed in. Flags skills that need review. */
export function SkillLevel({ skillId }: { skillId: string }) {
  const { user, levelOf, reviewDue } = useApp();
  if (!user) return null;
  return (
    <span className="inline-flex flex-col items-end gap-1">
      <MasteryBadge level={levelOf(skillId)} />
      {reviewDue(skillId) && (
        <span className="text-xs font-semibold text-primary" title="Not practiced in a while, so it dropped a level">
          Review due
        </span>
      )}
    </span>
  );
}
