import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { z } from "zod";
import {
  lessonFrontmatterSchema,
  mockProblemSchema,
  problemSchema,
  unitSchema,
  type LessonFrontmatter,
  type MockProblem,
  type Problem,
  type Unit,
} from "./schema";
import type { CourseIndex } from "./types";
import { masteryRules } from "@/config/mastery";

// Reads and validates everything in /content. Runs on the server at build time.
// Any mistake in a content file stops the build with a message that names the file and field.

const CONTENT_DIR = path.join(process.cwd(), "content");

export class ContentError extends Error {
  constructor(file: string, message: string) {
    super(`\n\nContent error in ${file}\n${message}\n`);
    this.name = "ContentError";
  }
}

function formatZod(err: z.ZodError, prefix = "", items?: unknown[]): string {
  return err.issues
    .map((i) => {
      let path = i.path.join(".") || "(file)";
      // For problem files, say "problem 3 (id: abc)" instead of "0"
      if (items && typeof i.path[0] === "number") {
        const n = i.path[0];
        const id = (items[n] as { id?: string } | undefined)?.id;
        path = `problem ${n + 1}${id ? ` (id: ${id})` : ""}${i.path.length > 1 ? ", field " + i.path.slice(1).join(".") : ""}`;
      }
      return `  • ${prefix}${path}: ${i.message}`;
    })
    .join("\n");
}

function readJson(file: string): unknown {
  const raw = fs.readFileSync(file, "utf8");
  try {
    return JSON.parse(raw);
  } catch (e) {
    throw new ContentError(rel(file), `  • This file is not valid JSON: ${(e as Error).message}`);
  }
}

function rel(file: string) {
  return path.relative(process.cwd(), file);
}

function listFiles(dir: string, ext: string) {
  const full = path.join(CONTENT_DIR, dir);
  if (!fs.existsSync(full)) return [];
  return fs
    .readdirSync(full)
    .filter((f) => f.endsWith(ext))
    .sort()
    .map((f) => path.join(full, f));
}

type Loaded = {
  units: Unit[];
  problems: Problem[];
  mocks: MockProblem[];
  warnings: string[];
};

let cache: Loaded | null = null;

export function loadContent(): Loaded {
  if (cache && process.env.NODE_ENV === "production") return cache;

  const warnings: string[] = [];

  // Units
  const units: Unit[] = listFiles("units", ".json").map((file) => {
    const parsed = unitSchema.safeParse(readJson(file));
    if (!parsed.success) throw new ContentError(rel(file), formatZod(parsed.error));
    return parsed.data;
  });
  units.sort((a, b) => a.order - b.order);

  const unitIds = new Set<string>();
  const skillIds = new Set<string>();
  for (const u of units) {
    if (unitIds.has(u.id)) throw new ContentError(`content/units`, `  • Two units use the id "${u.id}". Unit ids must be unique.`);
    unitIds.add(u.id);
    for (const s of u.skills) {
      if (skillIds.has(s.id))
        throw new ContentError(`content/units/${u.id}`, `  • The skill id "${s.id}" is used more than once. Skill ids must be unique across all units.`);
      skillIds.add(s.id);
    }
  }

  // Problems (each file holds an array of problems)
  const problems: Problem[] = [];
  const problemIds = new Set<string>();
  for (const file of listFiles("problems", ".json")) {
    const data = readJson(file);
    const parsed = z.array(problemSchema).safeParse(data);
    if (!parsed.success) {
      throw new ContentError(rel(file), formatZod(parsed.error, "", Array.isArray(data) ? data : undefined));
    }
    for (const p of parsed.data) {
      if (problemIds.has(p.id))
        throw new ContentError(rel(file), `  • The problem id "${p.id}" is used more than once.`);
      if (!skillIds.has(p.skillId))
        throw new ContentError(
          rel(file),
          `  • Problem "${p.id}" uses skillId "${p.skillId}", but no unit has a skill with that id.`,
        );
      problemIds.add(p.id);
      problems.push(p);
    }
  }

  // Mock exam banks (each file holds an array of mock problems)
  const mocks: MockProblem[] = [];
  for (const file of listFiles("mocks", ".json")) {
    const data = readJson(file);
    const parsed = z.array(mockProblemSchema).safeParse(data);
    if (!parsed.success) {
      throw new ContentError(rel(file), formatZod(parsed.error, "", Array.isArray(data) ? data : undefined));
    }
    for (const p of parsed.data) {
      if (problemIds.has(p.id)) throw new ContentError(rel(file), `  • The problem id "${p.id}" is used more than once.`);
      if (!skillIds.has(p.skillId))
        throw new ContentError(rel(file), `  • Mock problem "${p.id}" uses skillId "${p.skillId}", but no unit has a skill with that id.`);
      if (!unitIds.has(p.topic)) throw new ContentError(rel(file), `  • Mock problem "${p.id}" uses topic "${p.topic}", which is not a unit id.`);
      problemIds.add(p.id);
      mocks.push(p);
    }
  }
  for (const [track, levels] of [["amc10", [1, 2, 3, 4, 5]], ["amc12", [2, 3, 4, 5, 6]]] as const) {
    for (const lv of levels) {
      const fams = new Set(mocks.filter((m) => m.difficulty === lv && (track === "amc12" || m.track === "both")).map((m) => m.family));
      if (fams.size < 10) warnings.push(`Mock level ${lv} (${track}) has only ${fams.size} problem families; aim for 10 or more so back to back mocks never share one.`);
    }
  }

  // Problem banks: warn about skills with too few problems
  for (const u of units) {
    for (const s of u.skills) {
      const b = problems.filter((p) => p.skillId === s.id && p.level === "basics").length;
      const c = problems.filter((p) => p.skillId === s.id && p.level === "challenge").length;
      if (b < masteryRules.basicsBankMinimum)
        warnings.push(`Skill "${s.id}" has ${b} basics problems (aim for ${masteryRules.basicsBankMinimum}).`);
      if (c < masteryRules.challengeBankMinimum)
        warnings.push(`Skill "${s.id}" has ${c} challenge problems (aim for ${masteryRules.challengeBankMinimum}).`);
    }
  }

  // Lessons: warn about skills without a lesson file
  for (const u of units) {
    for (const s of u.skills) {
      if (!fs.existsSync(path.join(CONTENT_DIR, "lessons", `${s.id}.mdx`))) {
        warnings.push(`Skill "${s.id}" in unit "${u.id}" has no lesson file (content/lessons/${s.id}.mdx).`);
      }
    }
  }

  cache = { units, problems, mocks, warnings };
  return cache;
}

export function getUnits() {
  return loadContent().units;
}

export function getUnit(unitId: string) {
  return loadContent().units.find((u) => u.id === unitId) ?? null;
}

export function getMockProblems() {
  return loadContent().mocks;
}

export function getProblems() {
  return loadContent().problems;
}

export function getProblemsForUnit(unitId: string) {
  const unit = getUnit(unitId);
  if (!unit) return [];
  const ids = new Set(unit.skills.map((s) => s.id));
  return getProblems().filter((p) => ids.has(p.skillId));
}

export function getLesson(skillId: string): { frontmatter: LessonFrontmatter; body: string } | null {
  const file = path.join(CONTENT_DIR, "lessons", `${skillId}.mdx`);
  if (!fs.existsSync(file)) return null;
  const { data, content } = matter(fs.readFileSync(file, "utf8"));
  const parsed = lessonFrontmatterSchema.safeParse(data);
  if (!parsed.success) throw new ContentError(rel(file), formatZod(parsed.error, "frontmatter."));
  return { frontmatter: parsed.data, body: content };
}

// A small summary of the course that is safe to send to the browser.
export function getCourseIndex(): CourseIndex {
  const { units, problems } = loadContent();
  return {
    units: units.map((u) => ({
      id: u.id,
      title: u.title,
      description: u.description,
      track: u.track,
      order: u.order,
      skills: u.skills.map((s) => ({
        id: s.id,
        title: s.title,
        description: s.description,
        amc12Only: (s.track ?? u.track) === "amc12",
        basicsCount: problems.filter((p) => p.skillId === s.id && p.level === "basics").length,
        challengeCount: problems.filter((p) => p.skillId === s.id && p.level === "challenge").length,
      })),
    })),
  };
}
