// Mastery rules. Adjust these numbers to change how students level up.

export const MASTERY_LEVELS = [
  "not_started",
  "attempted",
  "familiar",
  "proficient",
  "mastered",
] as const;

export type MasteryLevel = (typeof MASTERY_LEVELS)[number];

export const MASTERY_LABELS: Record<MasteryLevel, string> = {
  not_started: "Not Started",
  attempted: "Attempted",
  familiar: "Familiar",
  proficient: "Proficient",
  mastered: "Mastered",
};

// Points each level is worth. Used for course progress bars (out of 100 per skill).
export const MASTERY_POINTS: Record<MasteryLevel, number> = {
  not_started: 0,
  attempted: 20,
  familiar: 50,
  proficient: 80,
  mastered: 100,
};

// The ladder for each skill:
//   Basics practice  -> up to Familiar
//   Challenge practice -> up to Proficient
//   Unit test        -> the only way to reach Mastered
export const masteryRules = {
  practice: {
    // Basics set: score at or above this moves a skill to Familiar
    basicsFamiliarScore: 0.7,
    // Challenge set: score at or above this moves a skill to Proficient
    challengeProficientScore: 1.0,
    // Practice never lowers a level, it only raises it, and never past Proficient
  },
  quizAndTest: {
    // A skill scored at or above this on a quiz or unit test goes up one level
    levelUpScore: 1.0,
    // A skill scored below this on a quiz or unit test goes down one level
    levelDownScore: 0.5,
    // Quizzes and tests can raise a skill up to this level, but no higher
    highestLevelFromQuiz: "proficient" as MasteryLevel,
    highestLevelFromTest: "mastered" as MasteryLevel,
    // A level drop never goes below this
    lowestLevelAfterDrop: "attempted" as MasteryLevel,
  },
  // Skills fade without practice: a Proficient or Mastered skill not practiced for this many days
  // shows as one level lower ("review due") until the student practices or tests it again.
  reviewAfterDays: 30,
  // Problems per practice set. Each set is drawn from the skill's bank without repeats
  // until every problem in the bank has been used.
  basicsSetSize: 4,
  challengeSetSize: 2,
  // Recommended bank sizes (the content checker warns when a skill has fewer)
  basicsBankMinimum: 20,
  challengeBankMinimum: 10,
  // Number of problems in a quiz and a unit test (fewer if the unit has fewer problems)
  quizLength: 5,
  unitTestLength: 10,
};
