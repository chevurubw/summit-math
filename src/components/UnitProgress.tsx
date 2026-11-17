"use client";

import type { CourseUnit } from "@/lib/content/types";
import { useApp } from "./AppProvider";
import { useUnitProgress } from "./course";
import { ProgressRing } from "./progress";

export function UnitProgress({ unit }: { unit: CourseUnit }) {
  const { user } = useApp();
  const progress = useUnitProgress()(unit);
  if (!user || unit.skills.length === 0) return null;
  return (
    <div className="flex items-center gap-4">
      <ProgressRing value={progress} size={76} />
      <div className="text-sm">
        <p className="font-semibold text-heading">Unit mastery</p>
        <p className="text-muted">Across {unit.skills.length} skills</p>
      </div>
    </div>
  );
}
