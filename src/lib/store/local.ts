"use client";

import { emptyProfile, type ProgressStore, type UserData } from "./types";

// Saves progress in the browser (localStorage). Used when Supabase is not connected.

const key = (userId: string) => `summit:data:${userId}`;

function read(userId: string, name: string): UserData {
  try {
    const raw = localStorage.getItem(key(userId));
    if (raw) {
      const d = JSON.parse(raw) as UserData;
      // Fill in fields added after this browser first saved data
      d.profile = { ...emptyProfile(name), ...d.profile };
      return d;
    }
  } catch {
    // Storage can be unavailable (private mode) or hold bad data. Start fresh.
  }
  return { profile: emptyProfile(name), skills: {}, attempts: [], mocks: [] };
}

function write(userId: string, data: UserData) {
  try {
    localStorage.setItem(key(userId), JSON.stringify(data));
  } catch {
    // Ignore storage errors so the page keeps working.
  }
}

export function createLocalStore(userId: string, name: string): ProgressStore {
  const update = (fn: (d: UserData) => void) => {
    const d = read(userId, name);
    fn(d);
    write(userId, d);
  };
  return {
    async loadAll() {
      return read(userId, name);
    },
    async saveProfile(profile) {
      update((d) => (d.profile = profile));
    },
    async saveSkills(skills) {
      update((d) => skills.forEach((s) => (d.skills[s.skillId] = s)));
    },
    async addAttempts(attempts) {
      update((d) => (d.attempts = [...d.attempts, ...attempts].slice(-2000)));
    },
    async addMock(mock) {
      update((d) => d.mocks.push(mock));
    },
    async resetProgress() {
      update((d) => {
        d.skills = {};
        d.attempts = [];
        d.mocks = [];
        d.profile = { ...d.profile, streak: 0, lastActiveDate: null };
      });
    },
  };
}

// Local mode "accounts". No real passwords: this is only for trying the site on your own computer.
const LOCAL_USER_KEY = "summit:localUser";

export function getLocalUser(): { id: string; email: string; name: string } | null {
  try {
    const raw = localStorage.getItem(LOCAL_USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function setLocalUser(user: { id: string; email: string; name: string } | null) {
  try {
    if (user) localStorage.setItem(LOCAL_USER_KEY, JSON.stringify(user));
    else localStorage.removeItem(LOCAL_USER_KEY);
  } catch {
    // ignore
  }
}

export function localIdForEmail(email: string) {
  return "local_" + email.trim().toLowerCase().replace(/[^a-z0-9]/g, "_");
}
