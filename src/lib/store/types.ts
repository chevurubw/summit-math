import type { MasteryLevel } from "@/config/mastery";
import type { AvatarId, ThemeId } from "@/config/climb";
import type { Track } from "@/config/exam";
import type { ChoiceKey } from "@/lib/content/schema";

export type AppUser = {
  id: string;
  email: string;
  name: string;
};

export type Profile = {
  displayName: string;
  streak: number;
  lastActiveDate: string | null; // YYYY-MM-DD
  theme: ThemeId;
  avatar: AvatarId;
  /** Highest altitude ever reached. Unlocks are based on this, so they are never taken away. */
  bestAltitude: number;
};

export type SkillProgress = {
  skillId: string;
  level: MasteryLevel;
  points: number;
  updatedAt: string;
};

export type Attempt = {
  problemId: string;
  skillId: string;
  correct: boolean;
  timeTakenMs: number;
  at: string;
};

export type MockExamRecord = {
  id: string;
  track: Track;
  score: number;
  maxScore: number;
  correct: number;
  wrong: number;
  blank: number;
  answers: Record<string, ChoiceKey | null>;
  breakdown: Record<string, { correct: number; total: number }>; // by unit id
  at: string;
};

export type UserData = {
  profile: Profile;
  skills: Record<string, SkillProgress>;
  attempts: Attempt[];
  mocks: MockExamRecord[];
};

/** Where progress is saved. Two versions: browser storage (local mode) and Supabase. */
export interface ProgressStore {
  loadAll(): Promise<UserData>;
  saveProfile(profile: Profile): Promise<void>;
  saveSkills(skills: SkillProgress[]): Promise<void>;
  addAttempts(attempts: Attempt[]): Promise<void>;
  addMock(mock: MockExamRecord): Promise<void>;
  resetProgress(): Promise<void>;
}

export const emptyProfile = (name = ""): Profile => ({
  displayName: name,
  streak: 0,
  lastActiveDate: null,
  theme: "summit",
  avatar: "initial",
  bestAltitude: 0,
});
