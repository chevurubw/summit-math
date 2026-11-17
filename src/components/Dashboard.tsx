"use client";

import { Lock, MountainSnow, PlayCircle, Sparkles, Trophy } from "lucide-react";
import Link from "next/link";
import { examConfig, TRACK_LABELS } from "@/config/exam";
import { MASTERY_LEVELS, MASTERY_POINTS } from "@/config/mastery";
import { formatMeters } from "@/lib/climb";
import { allSkills, findSkill, type CourseIndex } from "@/lib/content/types";
import { useApp } from "./AppProvider";
import { MasteryBadge, ProgressRing } from "./progress";
import { ButtonLink, Card } from "./ui";

export function Dashboard({ index }: { index: CourseIndex }) {
  const { data, user, levelOf, climb } = useApp();
  if (!data || !user || !climb) return null;
  const { profile, attempts, mocks } = data;
  const everySkill = allSkills(index);
  const skills = everySkill.filter(({ skill }) => !skill.amc12Only);
  const amc12Skills = everySkill.filter(({ skill }) => skill.amc12Only);
  const pctOf = (list: typeof skills) =>
    list.length ? list.reduce((sum, { skill }) => sum + MASTERY_POINTS[levelOf(skill.id)], 0) / (list.length * 100) : 0;

  const mastery = pctOf(skills);
  const masteredCount = skills.filter(({ skill }) => levelOf(skill.id) === "mastered").length;

  const last = attempts.length ? findSkill(index, attempts[attempts.length - 1].skillId) : null;
  const recommended =
    skills.find(({ skill }) => MASTERY_LEVELS.indexOf(levelOf(skill.id)) < MASTERY_LEVELS.indexOf("proficient")) ??
    skills.find(({ skill }) => levelOf(skill.id) !== "mastered");
  const latestMock = mocks[mocks.length - 1];

  // Recent activity: answers grouped by day and skill
  const groups = new Map<string, { day: string; skillId: string; correct: number; total: number }>();
  for (const a of [...attempts].reverse()) {
    const day = new Date(a.at).toLocaleDateString();
    const key = `${day}|${a.skillId}`;
    const g = groups.get(key) ?? { day, skillId: a.skillId, correct: 0, total: 0 };
    g.total++;
    if (a.correct) g.correct++;
    groups.set(key, g);
    if (groups.size > 5) break;
  }
  const recent = [...groups.values()].slice(0, 5);

  return (
    <>
      <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold">Good to see you, {profile.displayName || user.name}.</h1>
          <p className="mt-2 text-muted">
            {profile.streak > 1 ? `${profile.streak} days in a row. ` : ""}You are at {climb.camp.name}, {formatMeters(climb.altitude)} up.
          </p>
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-3">
        {/* Continue */}
        <Card className="p-6 lg:col-span-2">
          <p className="flex items-center gap-2 text-sm font-semibold text-muted">
            <PlayCircle className="h-4 w-4" aria-hidden /> Continue where you left off
          </p>
          {last ? (
            <>
              <h2 className="mt-3 text-2xl font-bold">{last.skill.title}</h2>
              <p className="text-muted">{last.unit.title}</p>
              <div className="mt-4">
                <MasteryBadge level={levelOf(last.skill.id)} />
              </div>
              <div className="mt-6 flex flex-wrap gap-3">
                <ButtonLink href={`/learn/${last.unit.id}/${last.skill.id}/practice/basics`}>Keep practicing</ButtonLink>
                <ButtonLink href={`/learn/${last.unit.id}/${last.skill.id}`} variant="secondary">
                  Review the lesson
                </ButtonLink>
              </div>
            </>
          ) : (
            <>
              <h2 className="mt-3 text-2xl font-bold">Start your first skill</h2>
              <p className="text-muted">Your most recent skill will show up here.</p>
              <ButtonLink href="/learn" className="mt-6">
                Open the course
              </ButtonLink>
            </>
          )}
        </Card>

        {/* Mastery */}
        <Card className="flex items-center gap-5 p-6">
          <ProgressRing value={mastery} size={104} stroke={10} />
          <div>
            <p className="font-display text-xl font-bold text-heading">Core mastery</p>
            <p className="mt-1 text-sm text-muted">
              {masteredCount} of {skills.length} core skills mastered
              {amc12Skills.length > 0 && (
                <>
                  <br />
                  AMC 12 only skills: {Math.round(pctOf(amc12Skills) * 100)}%
                </>
              )}
            </p>
            <Link href="/climb" className="mt-3 inline-block text-sm font-semibold text-accent-soft hover:underline">
              See all progress
            </Link>
          </div>
        </Card>

        {/* Recommended */}
        <Card className="p-6">
          <p className="flex items-center gap-2 text-sm font-semibold text-muted">
            <Sparkles className="h-4 w-4 text-accent-soft" aria-hidden /> Recommended next
          </p>
          {recommended ? (
            <>
              <h2 className="mt-3 text-xl font-bold">{recommended.skill.title}</h2>
              <p className="text-sm text-muted">{recommended.unit.title}</p>
              <div className="mt-3">
                <MasteryBadge level={levelOf(recommended.skill.id)} />
              </div>
              <ButtonLink href={`/learn/${recommended.unit.id}/${recommended.skill.id}`} variant="secondary" size="sm" className="mt-5">
                Start this skill
              </ButtonLink>
            </>
          ) : (
            <p className="mt-3 text-body">Every skill is mastered. Take a mock exam to stay sharp.</p>
          )}
        </Card>

        {/* Climb */}
        <Card className="graph-paper p-6">
          <p className="flex items-center gap-2 text-sm font-semibold text-muted">
            <MountainSnow className="h-4 w-4 text-accent-soft" aria-hidden /> Your climb
          </p>
          <p className="mt-3 font-display text-5xl font-extrabold text-heading tabular-nums">{formatMeters(climb.altitude)}</p>
          <p className="text-sm text-muted">
            {climb.camp.name}
            {climb.nextCamp ? `. ${formatMeters(climb.nextCamp.height - climb.altitude)} to ${climb.nextCamp.name}.` : "."}
          </p>
          {climb.blockedBy && (
            <p className="mt-3 flex items-start gap-2 text-sm text-body">
              <Lock className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden />
              {climb.blockedBy.label} to pass the checkpoint.
            </p>
          )}
          <ButtonLink href="/climb" variant="secondary" size="sm" className="mt-5">
            See the mountain
          </ButtonLink>
        </Card>

        {/* Latest mock */}
        <Card className="p-6">
          <p className="flex items-center gap-2 text-sm font-semibold text-muted">
            <Trophy className="h-4 w-4 text-accent-soft" aria-hidden /> Latest mock exam
          </p>
          {latestMock ? (
            <>
              <p className="mt-3 font-display text-5xl font-extrabold text-heading tabular-nums">{latestMock.score}</p>
              <p className="text-sm text-muted">
                out of {latestMock.maxScore} on the {TRACK_LABELS[latestMock.track]}. AIME cutoff: {examConfig.aimeCutoffs[latestMock.track]}.
              </p>
            </>
          ) : (
            <>
              <p className="mt-3 text-body">No mock exams yet.</p>
              <ButtonLink href="/mock" variant="secondary" size="sm" className="mt-5">
                Take a mock exam
              </ButtonLink>
            </>
          )}
        </Card>

        {/* Recent activity */}
        <Card className="p-6 lg:col-span-3">
          <h2 className="text-xl font-bold">Recent activity</h2>
          {recent.length === 0 ? (
            <p className="mt-3 text-muted">Nothing yet. Answer a few problems and your activity will show up here.</p>
          ) : (
            <ul className="mt-4 divide-y divide-line">
              {recent.map((g) => {
                const found = findSkill(index, g.skillId);
                return (
                  <li key={`${g.day}${g.skillId}`} className="flex flex-wrap items-center justify-between gap-2 py-3">
                    <span>
                      <span className="font-semibold text-heading">{found?.skill.title ?? g.skillId}</span>
                      <span className="ml-2 text-sm text-muted">{found?.unit.title}</span>
                    </span>
                    <span className="text-sm text-muted">
                      {g.correct} of {g.total} correct, {g.day}
                    </span>
                  </li>
                );
              })}
            </ul>
          )}
        </Card>
      </div>
    </>
  );
}
