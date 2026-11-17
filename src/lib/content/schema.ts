import { z } from "zod";

// The shape every content file must follow. Errors point to the exact field.

export const trackScope = z.enum(["both", "amc12"]);

export const skillSchema = z.object({
  id: z
    .string()
    .regex(/^[a-z0-9_]+$/, "Skill ids can only use lowercase letters, numbers and underscores"),
  title: z.string().min(1),
  description: z.string().default(""),
  // Optional: set to "amc12" to mark one skill as AMC 12 only inside a shared unit
  track: trackScope.optional(),
});

export const unitSchema = z.object({
  id: z
    .string()
    .regex(/^[a-z0-9_]+$/, "Unit ids can only use lowercase letters, numbers and underscores"),
  title: z.string().min(1),
  description: z.string().min(1),
  track: trackScope,
  order: z.number().int(),
  skills: z.array(skillSchema).default([]),
});

export const choiceKey = z.enum(["A", "B", "C", "D", "E"]);

export const problemSchema = z.object({
  id: z.string().min(1),
  skillId: z.string().min(1),
  // The problem type (one template); variants of a type differ only in numbers and names
  family: z.string().optional(),
  level: z.enum(["basics", "challenge"]),
  track: trackScope,
  prompt: z.string().min(1),
  choices: z.object({
    A: z.string().min(1),
    B: z.string().min(1),
    C: z.string().min(1),
    D: z.string().min(1),
    E: z.string().min(1),
  }),
  answer: choiceKey,
  hints: z.array(z.string()).default([]),
  solution: z.string().min(1),
  image: z.string().optional(),
});

// Mock exam problems live in content/mocks. Each one belongs to a family (one problem idea);
// difficulty 1 to 6 places it in a section of the exam (see src/lib/mockSelect.ts).
export const mockProblemSchema = z.object({
  id: z.string().min(1),
  family: z.string().min(1),
  difficulty: z.number().int().min(1).max(6),
  topic: z.string().min(1),
  skillId: z.string().min(1),
  track: trackScope,
  prompt: z.string().min(1),
  choices: z.object({
    A: z.string().min(1),
    B: z.string().min(1),
    C: z.string().min(1),
    D: z.string().min(1),
    E: z.string().min(1),
  }),
  answer: choiceKey,
  hints: z.array(z.string()).default([]),
  solution: z.string().min(1),
  image: z.string().optional(),
});

export const lessonFrontmatterSchema = z.object({
  title: z.string().min(1),
  videoUrl: z.string().url().optional(),
});

export type Skill = z.infer<typeof skillSchema>;
export type Unit = z.infer<typeof unitSchema>;
export type Problem = z.infer<typeof problemSchema>;
export type MockProblem = z.infer<typeof mockProblemSchema>;
export type ChoiceKey = z.infer<typeof choiceKey>;
export type LessonFrontmatter = z.infer<typeof lessonFrontmatterSchema>;
