import { examConfig } from "@/config/exam";
import type { ChoiceKey } from "@/lib/content/schema";

export type ExamAnswer = ChoiceKey | null;

export function scoreExam(
  problems: { id: string; answer: ChoiceKey }[],
  answers: Record<string, ExamAnswer>,
) {
  let correct = 0;
  let wrong = 0;
  let blank = 0;
  for (const p of problems) {
    const a = answers[p.id] ?? null;
    if (a === null) blank++;
    else if (a === p.answer) correct++;
    else wrong++;
  }
  const s = examConfig.scoring;
  const score = correct * s.correct + blank * s.blank + wrong * s.wrong;
  const maxScore = problems.length * s.correct;
  return { correct, wrong, blank, score, maxScore };
}

/** Shuffles a copy of an array. */
export function shuffle<T>(items: T[]): T[] {
  const a = [...items];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
