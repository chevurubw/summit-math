"use client";

import { ArrowUp, ArrowDown, Minus } from "lucide-react";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { MASTERY_LEVELS } from "@/config/mastery";
import type { ChoiceKey, Problem } from "@/lib/content/schema";
import type { SessionKind } from "@/lib/mastery";
import { masteryRules } from "@/config/mastery";
import { pickFresh } from "@/lib/rotation";
import { useApp, type SessionResult, type SkillChange } from "./AppProvider";
import { Burst, CountUp } from "./motion";
import { CHOICE_KEYS, Feedback, HintPanel, ProblemCard, SolutionPanel } from "./problem";
import { MasteryBadge, ProgressBar, ProgressRing } from "./progress";
import { Button, ButtonLink, PlaceholderNote } from "./ui";

const kindLabel: Record<SessionKind, string> = {
  basics: "Basics practice",
  challenge: "Challenge practice",
  quiz: "Unit quiz",
  test: "Unit test",
};

/**
 * Runs a set of problems one at a time: practice sets, quizzes and unit tests.
 * Hints are only offered in practice.
 */
export function ProblemSession({
  problems: pool,
  kind,
  title,
  skillTitles,
  backHref,
  backLabel,
  limit,
}: {
  problems: Problem[];
  kind: SessionKind;
  title: string;
  skillTitles: Record<string, string>;
  backHref: string;
  backLabel: string;
  limit?: number;
}) {
  const { recordSession, data, status } = useApp();
  const eligible = pool;
  // The latest answer history, read when a new set is picked
  const attemptsRef = useRef(data?.attempts ?? []);
  useEffect(() => {
    attemptsRef.current = data?.attempts ?? [];
  }, [data]);

  // How many problems this session has. Practice sets use the sizes in config/mastery.ts.
  const size =
    limit ?? (kind === "basics" ? masteryRules.basicsSetSize : kind === "challenge" ? masteryRules.challengeSetSize : eligible.length);

  // Never repeat a problem until the whole bank has been used.
  // Waits for the student's history to load so the rotation can see it.
  const ready = status === "ready";
  const pick = useCallback(() => pickFresh(eligible, attemptsRef.current, size), [eligible, size]);

  const [round, setRound] = useState(0);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [i, setI] = useState(0);
  const [selected, setSelected] = useState<ChoiceKey | null>(null);
  const [checked, setChecked] = useState(false);
  const [hints, setHints] = useState(0);
  const [results, setResults] = useState<SessionResult[]>([]);
  const [changes, setChanges] = useState<SkillChange[] | null>(null);
  const startRef = useRef(0);

  // Sets are picked after the page loads so the server and browser agree
  useEffect(() => {
    if (!ready) return;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- the set depends on browser only history
    setProblems(pick());
  }, [pick, round, ready]);

  useEffect(() => {
    startRef.current = Date.now();
  }, [i, round]);

  const problem = problems[i];
  const done = problems.length > 0 && results.length === problems.length && i === problems.length - 1 && checked;

  const check = useCallback(() => {
    if (!problem || !selected || checked) return;
    setChecked(true);
    setResults((r) => [
      ...r,
      {
        problemId: problem.id,
        skillId: problem.skillId,
        correct: selected === problem.answer,
        timeTakenMs: Date.now() - startRef.current,
      },
    ]);
  }, [problem, selected, checked]);

  const next = useCallback(async () => {
    if (i < problems.length - 1) {
      setI(i + 1);
      setSelected(null);
      setChecked(false);
      setHints(0);
    } else {
      setChanges(await recordSession(kind, results));
    }
  }, [i, problems.length, recordSession, kind, results]);

  // Keyboard shortcuts: A to E pick an answer, Enter checks or moves on
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (changes || e.metaKey || e.ctrlKey || e.altKey) return;
      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      const k = e.key.toUpperCase();
      if (!checked && (CHOICE_KEYS as string[]).includes(k)) setSelected(k as ChoiceKey);
      if (e.key === "Enter" && (e.target as HTMLElement)?.tagName !== "BUTTON") {
        if (!checked) check();
        else void next();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [checked, check, next, changes]);

  const restart = () => {
    setRound((r) => r + 1);
    setI(0);
    setSelected(null);
    setChecked(false);
    setHints(0);
    setResults([]);
    setChanges(null);
  };

  if (eligible.length === 0) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        <h1 className="text-3xl font-bold">{title}</h1>
        <p className="text-lg text-heading">There are no problems here yet.</p>
        <PlaceholderNote>
          Add problems to a file in <code>content/problems</code>. For practice sets, set <code>skillId</code> to this skill and{" "}
          <code>level</code> to <code>&quot;{kind === "challenge" ? "challenge" : "basics"}&quot;</code>.
        </PlaceholderNote>
        <ButtonLink href={backHref} variant="secondary">
          {backLabel}
        </ButtonLink>
      </div>
    );
  }

  if (!problem) return null;

  // Results screen
  if (changes) {
    const correct = results.filter((r) => r.correct).length;
    const leveledUp = changes.some((c) => MASTERY_LEVELS.indexOf(c.after) > MASTERY_LEVELS.indexOf(c.before));
    return (
      <div className="mx-auto max-w-2xl">
        <p className="anim-fade text-muted">{kindLabel[kind]} complete</p>
        <h1 className="anim-rise mt-1 text-4xl font-bold">{leveledUp ? "You leveled up." : title}</h1>
        <div className="anim-rise mt-8 flex items-center gap-6 rounded-lg border border-line bg-surface p-6" style={{ animationDelay: "100ms" }}>
          <ProgressRing value={correct / results.length} size={96} stroke={9} />
          <div>
            <p className="font-display text-3xl font-bold text-heading">
              <CountUp value={correct} duration={700} /> of {results.length} correct
            </p>
            <p className="mt-1 text-muted">
              {correct === results.length ? "A perfect set." : "Review the solutions, then try again to level up."}
            </p>
          </div>
        </div>

        <h2 className="mt-10 text-xl font-bold">Skill changes</h2>
        <ul className="mt-4 divide-y divide-line rounded-lg border border-line bg-surface">
          {changes.map((c, n) => {
            const dir = MASTERY_LEVELS.indexOf(c.after) - MASTERY_LEVELS.indexOf(c.before);
            return (
              <li key={c.skillId} className="anim-rise flex flex-wrap items-center gap-3 px-5 py-4" style={{ animationDelay: `${250 + n * 90}ms` }}>
                <span className="mr-auto">
                  <span className="block font-semibold text-heading">{skillTitles[c.skillId] ?? c.skillId}</span>
                  <span className="text-sm text-muted">
                    {c.correct} of {c.total} correct
                  </span>
                </span>
                <MasteryBadge level={c.before} />
                {dir > 0 ? (
                  <ArrowUp className="h-4 w-4 text-correct" aria-label="went up to" />
                ) : dir < 0 ? (
                  <ArrowDown className="h-4 w-4 text-wrong" aria-label="went down to" />
                ) : (
                  <Minus className="h-4 w-4 text-muted" aria-label="stayed at" />
                )}
                <span className={`relative ${dir > 0 ? "anim-level-up" : ""}`} style={{ animationDelay: `${450 + n * 90}ms` }}>
                  <MasteryBadge level={c.after} animate={dir > 0} />
                  {dir > 0 && <Burst count={12} distance={40} colors={["var(--c-accent)", "var(--c-accent-soft)", "#ffffff"]} />}
                </span>
              </li>
            );
          })}
        </ul>

        <div className="mt-8 flex flex-wrap gap-3">
          <Button onClick={restart}>Try again</Button>
          <ButtonLink href={backHref} variant="secondary">
            {backLabel}
          </ButtonLink>
        </div>
      </div>
    );
  }

  const isPractice = kind === "basics" || kind === "challenge";
  const correctNow = checked && selected === problem.answer;
  // Correct answers in a row during this session
  let streak = 0;
  for (let n = results.length - 1; n >= 0 && results[n].correct; n--) streak++;

  return (
    <div className="mx-auto max-w-3xl">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <Link href={backHref} className="text-sm text-muted hover:text-heading">
            {backLabel}
          </Link>
          <h1 className="mt-1 text-2xl font-bold sm:text-3xl">{title}</h1>
        </div>
        <div className="flex items-center gap-3">
          {streak >= 2 && (
            <span key={streak} className="anim-pop inline-flex items-center gap-1.5 text-sm font-semibold text-accent-soft" aria-live="polite">
              <span className="h-2.5 w-2.5 rounded-full bg-accent" aria-hidden />
              {streak} in a row
            </span>
          )}
          <span className="text-sm font-semibold text-muted">{kindLabel[kind]}</span>
        </div>
      </div>
      <div className="mb-6 flex items-center gap-4">
        <ProgressBar value={(i + (checked ? 1 : 0)) / problems.length} />
        <span className="shrink-0 text-sm tabular-nums text-muted">
          {i + 1} / {problems.length}
        </span>
      </div>

      <ProblemCard
        key={`${round}-${problem.id}`}
        problem={problem}
        label={
          kind === "quiz" || kind === "test" ? <span>{skillTitles[problem.skillId] ?? ""}</span> : undefined
        }
        selected={selected}
        checked={checked}
        onSelect={setSelected}
        footer={
          <>
            {isPractice && !checked && (
              <HintPanel hints={problem.hints} revealed={hints} onReveal={() => setHints((h) => h + 1)} />
            )}
            {checked && (
              <>
                <Feedback correct={correctNow} answer={problem.answer} streak={streak} />
                <SolutionPanel solution={problem.solution} />
              </>
            )}
            <div className="flex flex-wrap items-center gap-3">
              {!checked ? (
                <Button onClick={check} disabled={!selected}>
                  Check answer
                </Button>
              ) : (
                <Button onClick={() => void next()}>{done ? "See results" : "Next problem"}</Button>
              )}
              <span className="hidden text-sm text-muted sm:inline">Tip: press A to E to choose, Enter to continue.</span>
            </div>
          </>
        }
      />
    </div>
  );
}
