// Course summary types shared by server and browser code.

export type CourseSkill = {
  id: string;
  title: string;
  description: string;
  /** True when this skill only appears on the AMC 12 */
  amc12Only: boolean;
  basicsCount: number;
  challengeCount: number;
};

export type CourseUnit = {
  id: string;
  title: string;
  description: string;
  track: "both" | "amc12";
  order: number;
  skills: CourseSkill[];
};

export type CourseIndex = {
  units: CourseUnit[];
};

/** Every skill in course order, with its unit. */
export function allSkills(index: CourseIndex) {
  return index.units.flatMap((u) => u.skills.map((skill) => ({ unit: u, skill })));
}

export function findSkill(index: CourseIndex, skillId: string) {
  for (const unit of index.units) {
    const skill = unit.skills.find((s) => s.id === skillId);
    if (skill) return { unit, skill };
  }
  return null;
}
