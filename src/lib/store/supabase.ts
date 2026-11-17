"use client";

import type { SupabaseClient } from "@supabase/supabase-js";
import { emptyProfile, type ProgressStore, type UserData } from "./types";

// Saves progress to Supabase. Table layouts are in supabase/migrations.

export function createSupabaseStore(sb: SupabaseClient, userId: string, name: string): ProgressStore {
  return {
    async loadAll(): Promise<UserData> {
      const [profileRes, skillsRes, attemptsRes, mocksRes] = await Promise.all([
        sb.from("profiles").select("*").eq("id", userId).maybeSingle(),
        sb.from("skill_progress").select("*").eq("user_id", userId),
        sb
          .from("attempts")
          .select("*")
          .eq("user_id", userId)
          .order("created_at", { ascending: false })
          .limit(2000),
        sb.from("mock_exams").select("*").eq("user_id", userId).order("created_at", { ascending: true }),
      ]);

      let profile = emptyProfile(name);
      if (profileRes.data) {
        profile = {
          displayName: profileRes.data.display_name ?? name,
          streak: profileRes.data.streak ?? 0,
          lastActiveDate: profileRes.data.last_active_date ?? null,
          theme: profileRes.data.theme ?? "summit",
          avatar: profileRes.data.avatar ?? "initial",
          bestAltitude: profileRes.data.best_altitude ?? 0,
        };
      } else {
        // First login (for example with Google): create the profile row if the database trigger has not.
        await sb.from("profiles").upsert({ id: userId, display_name: name });
      }

      const skills: UserData["skills"] = {};
      for (const r of skillsRes.data ?? []) {
        skills[r.skill_id] = { skillId: r.skill_id, level: r.level, points: r.points, updatedAt: r.updated_at };
      }

      return {
        profile,
        skills,
        attempts: (attemptsRes.data ?? [])
          .map((r) => ({
            problemId: r.problem_id,
            skillId: r.skill_id,
            correct: r.correct,
            timeTakenMs: r.time_taken_ms,
            at: r.created_at,
          }))
          .reverse(),
        mocks: (mocksRes.data ?? []).map((r) => ({
          id: r.id,
          track: r.track,
          score: Number(r.score),
          maxScore: Number(r.max_score),
          correct: r.correct,
          wrong: r.wrong,
          blank: r.blank,
          answers: r.answers ?? {},
          breakdown: r.breakdown ?? {},
          at: r.created_at,
        })),
      };
    },

    async saveProfile(p) {
      await sb.from("profiles").upsert({
        id: userId,
        display_name: p.displayName,
        streak: p.streak,
        last_active_date: p.lastActiveDate,
        theme: p.theme,
        avatar: p.avatar,
        best_altitude: p.bestAltitude,
      });
    },

    async saveSkills(list) {
      if (!list.length) return;
      await sb.from("skill_progress").upsert(
        list.map((s) => ({
          user_id: userId,
          skill_id: s.skillId,
          level: s.level,
          points: s.points,
          updated_at: s.updatedAt,
        })),
      );
    },

    async addAttempts(list) {
      if (!list.length) return;
      await sb.from("attempts").insert(
        list.map((a) => ({
          user_id: userId,
          problem_id: a.problemId,
          skill_id: a.skillId,
          correct: a.correct,
          time_taken_ms: a.timeTakenMs,
          created_at: a.at,
        })),
      );
    },

    async addMock(m) {
      await sb.from("mock_exams").insert({
        id: m.id,
        user_id: userId,
        track: m.track,
        score: m.score,
        max_score: m.maxScore,
        correct: m.correct,
        wrong: m.wrong,
        blank: m.blank,
        answers: m.answers,
        breakdown: m.breakdown,
        created_at: m.at,
      });
    },

    async resetProgress() {
      await Promise.all([
        sb.from("skill_progress").delete().eq("user_id", userId),
        sb.from("attempts").delete().eq("user_id", userId),
        sb.from("mock_exams").delete().eq("user_id", userId),
        sb.from("profiles").update({ streak: 0, last_active_date: null, best_altitude: 0 }).eq("id", userId),
      ]);
    },
  };
}
