"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import type { Track } from "@/config/exam";
import { campAt, computeClimb, unlocksBetween, type Climb } from "@/lib/climb";
import type { AvatarId, ThemeId } from "@/config/climb";
import type { CourseIndex } from "@/lib/content/types";
import { emptyProfile } from "@/lib/store/types";
import { MASTERY_POINTS, type MasteryLevel } from "@/config/mastery";
import { effectiveLevel, nextLevel, type SessionKind } from "@/lib/mastery";
import { getSupabaseBrowser } from "@/lib/supabase/client";
import { isSupabaseConfigured } from "@/lib/supabase/env";
import { createLocalStore, getLocalUser, localIdForEmail, setLocalUser } from "@/lib/store/local";
import { createSupabaseStore } from "@/lib/store/supabase";
import type {
  AppUser,
  Attempt,
  MockExamRecord,
  Profile,
  ProgressStore,
  SkillProgress,
  UserData,
} from "@/lib/store/types";

export type SessionResult = { problemId: string; skillId: string; correct: boolean; timeTakenMs: number };

export type SkillChange = {
  skillId: string;
  before: MasteryLevel;
  after: MasteryLevel;
  correct: number;
  total: number;
};

type AuthResult = { error?: string; message?: string };

export type Celebration = {
  id: number;
  /** The camp just reached, or null when only a reward was unlocked */
  camp: { name: string; height: number; note: string } | null;
  altitude: number;
  themes: ThemeId[];
  avatars: AvatarId[];
};

type AppContextValue = {
  index: CourseIndex;
  /** The student's climb, worked out from their mastery and mock exams (null when signed out) */
  climb: Climb | null;
  celebration: Celebration | null;
  dismissCelebration: () => void;
  mode: "supabase" | "local";
  status: "loading" | "ready";
  user: AppUser | null;
  data: UserData | null;
  /** A skill's current level, including review fading */
  levelOf: (skillId: string) => MasteryLevel;
  /** True when a skill has faded a level and needs review */
  reviewDue: (skillId: string) => boolean;

  signInWithGoogle: (next?: string) => Promise<AuthResult>;
  signInWithEmail: (email: string, password: string) => Promise<AuthResult>;
  signUpWithEmail: (name: string, email: string, password: string) => Promise<AuthResult>;
  requestPasswordReset: (email: string) => Promise<AuthResult>;
  updatePassword: (password: string) => Promise<AuthResult>;
  signOut: () => Promise<void>;

  updateProfile: (patch: Partial<Profile>) => Promise<void>;
  recordSession: (kind: SessionKind, results: SessionResult[]) => Promise<SkillChange[]>;
  recordMock: (mock: MockExamRecord, results: SessionResult[]) => Promise<void>;
  resetProgress: () => Promise<void>;
};

const AppContext = createContext<AppContextValue | null>(null);

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used inside <AppProvider>");
  return ctx;
}

const today = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

function withStreak(p: Profile): Profile {
  const t = today();
  if (p.lastActiveDate === t) return p;
  const y = new Date();
  y.setDate(y.getDate() - 1);
  const yesterday = `${y.getFullYear()}-${String(y.getMonth() + 1).padStart(2, "0")}-${String(y.getDate()).padStart(2, "0")}`;
  return { ...p, streak: p.lastActiveDate === yesterday ? p.streak + 1 : 1, lastActiveDate: t };
}

export function AppProvider({ children, index }: { children: React.ReactNode; index: CourseIndex }) {
  const mode = isSupabaseConfigured ? "supabase" : "local";
  const [status, setStatus] = useState<"loading" | "ready">("loading");
  const [user, setUser] = useState<AppUser | null>(null);
  const [data, setData] = useState<UserData | null>(null);
  const storeRef = useRef<ProgressStore | null>(null);
  const dataRef = useRef<UserData | null>(null);
  const setAll = useCallback((d: UserData | null) => {
    dataRef.current = d;
    setData(d);
  }, []);

  // Load the signed in user's data whenever the user changes
  const loadFor = useCallback(
    async (u: AppUser | null) => {
      setUser(u);
      if (!u) {
        storeRef.current = null;
        setAll(null);
        setStatus("ready");
        return;
      }
      const sb = getSupabaseBrowser();
      storeRef.current = sb ? createSupabaseStore(sb, u.id, u.name) : createLocalStore(u.id, u.name);
      try {
        setAll(await storeRef.current.loadAll());
      } catch (e) {
        console.error("Could not load progress", e);
        setAll({ profile: emptyProfile(u.name), skills: {}, attempts: [], mocks: [] });
      }
      setStatus("ready");
    },
    [setAll],
  );

  useEffect(() => {
    const sb = getSupabaseBrowser();
    if (!sb) {
      void loadFor(getLocalUser());
      return;
    }
    const toUser = (u: { id: string; email?: string; user_metadata?: Record<string, unknown> } | null): AppUser | null =>
      u
        ? {
            id: u.id,
            email: u.email ?? "",
            name:
              (u.user_metadata?.full_name as string) ||
              (u.user_metadata?.name as string) ||
              (u.email ?? "").split("@")[0],
          }
        : null;

    let currentId: string | null | undefined = undefined;
    sb.auth.getUser().then(({ data: d }) => {
      currentId = d.user?.id ?? null;
      void loadFor(toUser(d.user));
    });
    const { data: sub } = sb.auth.onAuthStateChange((_event, session) => {
      const id = session?.user?.id ?? null;
      if (currentId === undefined || id === currentId) return;
      currentId = id;
      void loadFor(toUser(session?.user ?? null));
    });
    return () => sub.subscription.unsubscribe();
  }, [loadFor]);

  // The climb, recalculated whenever progress changes
  const climb = useMemo(
    () =>
      data
        ? computeClimb(
            index,
            (id) => effectiveLevel(data.skills[id]?.level ?? "not_started", data.skills[id]?.updatedAt).level,
            data.mocks,
            (id) => effectiveLevel(data.skills[id]?.level ?? "not_started", data.skills[id]?.updatedAt).reviewDue,
          )
        : null,
    [index, data],
  );

  // Record new best altitudes, and celebrate new camps and unlocks
  const [celebration, setCelebration] = useState<Celebration | null>(null);
  useEffect(() => {
    const cur = dataRef.current;
    if (!climb || !cur || !storeRef.current) return;
    const best = cur.profile.bestAltitude ?? 0;
    if (climb.altitude <= best) return;
    const profile = { ...cur.profile, bestAltitude: climb.altitude };
    setAll({ ...cur, profile });
    void storeRef.current.saveProfile(profile);
    const newCamp = campAt(climb.altitude);
    const unlocks = unlocksBetween(best, climb.altitude);
    const reachedCamp = newCamp.height > best;
    if (reachedCamp || unlocks.themes.length || unlocks.avatars.length) {
      setCelebration({
        id: Date.now(),
        camp: reachedCamp ? { name: newCamp.name, height: newCamp.height, note: newCamp.note } : null,
        altitude: climb.altitude,
        ...unlocks,
      });
    }
  }, [climb, setAll]);

  // Apply the chosen color scheme to the whole site
  const theme = data?.profile.theme ?? "summit";
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  const origin = () => (typeof window !== "undefined" ? window.location.origin : "");

  const value = useMemo<AppContextValue>(() => {
    const eff = (skillId: string) => effectiveLevel(data?.skills[skillId]?.level ?? "not_started", data?.skills[skillId]?.updatedAt);
    const levelOf = (skillId: string): MasteryLevel => eff(skillId).level;
    const reviewDue = (skillId: string) => eff(skillId).reviewDue;

    const commit = setAll;

    return {
      index,
      climb,
      celebration,
      dismissCelebration: () => setCelebration(null),
      mode,
      status,
      user,
      data,
      levelOf,
      reviewDue,

      async signInWithGoogle(next = "/dashboard") {
        const sb = getSupabaseBrowser();
        if (!sb) return { error: "Google login needs Supabase connected. See the README." };
        const { error } = await sb.auth.signInWithOAuth({
          provider: "google",
          options: { redirectTo: `${origin()}/auth/callback?next=${encodeURIComponent(next)}` },
        });
        return error ? { error: error.message } : {};
      },

      async signInWithEmail(email, password) {
        const sb = getSupabaseBrowser();
        if (!sb) {
          const u = { id: localIdForEmail(email), email, name: email.split("@")[0] };
          const existing = getLocalUser();
          setLocalUser(existing?.email === email ? existing : u);
          await loadFor(getLocalUser());
          return {};
        }
        const { error } = await sb.auth.signInWithPassword({ email, password });
        return error ? { error: error.message } : {};
      },

      async signUpWithEmail(name, email, password) {
        const sb = getSupabaseBrowser();
        if (!sb) {
          setLocalUser({ id: localIdForEmail(email), email, name });
          await loadFor(getLocalUser());
          return {};
        }
        const { data: d, error } = await sb.auth.signUp({
          email,
          password,
          options: { data: { full_name: name }, emailRedirectTo: `${origin()}/auth/callback?next=/dashboard` },
        });
        if (error) return { error: error.message };
        if (!d.session) return { message: "Check your email for a link to confirm your account." };
        return {};
      },

      async requestPasswordReset(email) {
        const sb = getSupabaseBrowser();
        if (!sb) return { error: "Password reset needs Supabase connected. In local mode, just log in again with your email." };
        const { error } = await sb.auth.resetPasswordForEmail(email, {
          redirectTo: `${origin()}/auth/callback?next=/reset/update`,
        });
        return error ? { error: error.message } : { message: "If an account exists for that email, a reset link is on its way." };
      },

      async updatePassword(password) {
        const sb = getSupabaseBrowser();
        if (!sb) return { error: "Password changes need Supabase connected." };
        const { error } = await sb.auth.updateUser({ password });
        return error ? { error: error.message } : { message: "Password updated." };
      },

      async signOut() {
        const sb = getSupabaseBrowser();
        if (sb) await sb.auth.signOut();
        else setLocalUser(null);
        await loadFor(null);
      },

      async updateProfile(patch) {
        const cur = dataRef.current;
        if (!cur || !storeRef.current) return;
        const profile = { ...cur.profile, ...patch };
        commit({ ...cur, profile });
        await storeRef.current.saveProfile(profile);
      },

      async recordSession(kind, results) {
        const cur = dataRef.current;
        if (!cur || !storeRef.current) return [];
        const now = new Date().toISOString();

        // Group results by skill
        const bySkill = new Map<string, { correct: number; total: number }>();
        for (const r of results) {
          const s = bySkill.get(r.skillId) ?? { correct: 0, total: 0 };
          s.total++;
          if (r.correct) s.correct++;
          bySkill.set(r.skillId, s);
        }

        const changes: SkillChange[] = [];
        const updated: SkillProgress[] = [];
        for (const [skillId, s] of bySkill) {
          const before = effectiveLevel(cur.skills[skillId]?.level ?? "not_started", cur.skills[skillId]?.updatedAt).level;
          const after = nextLevel(before, kind, s.correct / s.total);
          changes.push({ skillId, before, after, ...s });
          updated.push({ skillId, level: after, points: MASTERY_POINTS[after], updatedAt: now });
        }

        const attempts: Attempt[] = results.map((r) => ({ ...r, at: now }));
        const skills = { ...cur.skills };
        updated.forEach((u) => (skills[u.skillId] = u));
        const profile = withStreak(cur.profile);
        commit({ ...cur, skills, attempts: [...cur.attempts, ...attempts], profile });

        await Promise.all([
          storeRef.current.saveSkills(updated),
          storeRef.current.addAttempts(attempts),
          storeRef.current.saveProfile(profile),
        ]);
        return changes;
      },

      async recordMock(mock, results) {
        const cur = dataRef.current;
        if (!cur || !storeRef.current) return;
        const attempts: Attempt[] = results.map((r) => ({ ...r, at: mock.at }));
        const profile = withStreak(cur.profile);
        commit({ ...cur, mocks: [...cur.mocks, mock], attempts: [...cur.attempts, ...attempts], profile });
        await Promise.all([
          storeRef.current.addMock(mock),
          storeRef.current.addAttempts(attempts),
          storeRef.current.saveProfile(profile),
        ]);
      },

      async resetProgress() {
        const cur = dataRef.current;
        if (!cur || !storeRef.current) return;
        await storeRef.current.resetProgress();
        const profile = { ...cur.profile, streak: 0, lastActiveDate: null, bestAltitude: 0, theme: "summit" as const, avatar: "initial" as const };
        commit({ ...cur, skills: {}, attempts: [], mocks: [], profile });
        await storeRef.current.saveProfile(profile);
      },
    };
  }, [index, climb, celebration, mode, status, user, data, loadFor, setAll]);

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export type { Track };
