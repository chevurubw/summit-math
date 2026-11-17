"use client";

import { Flag } from "lucide-react";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { examConfig, TRACK_LABELS, type Track } from "@/config/exam";
import type { ChoiceKey, MockProblem } from "@/lib/content/schema";
import { buildMock } from "@/lib/mockSelect";
import { scoreExam, type ExamAnswer } from "@/lib/scoring";
import type { MockExamRecord } from "@/lib/store/types";
import { useApp } from "./AppProvider";
import { Markdown } from "./Markdown";
import { MockReview } from "./MockReview";
import { CountUp } from "./motion";
import { CHOICE_KEYS, ChoiceButton } from "./problem";
import { ProgressBar } from "./progress";
import { Timer } from "./Timer";
import { Button, ButtonLink, PlaceholderNote } from "./ui";

/** A random UUID. crypto.randomUUID only exists on https or localhost, so fall back for phones on the home network. */
function newId(): string {
  if (typeof crypto.randomUUID === "function") return crypto.randomUUID();
  const b = crypto.getRandomValues(new Uint8Array(16));
  b[6] = (b[6] & 0x0f) | 0x40;
  b[8] = (b[8] & 0x3f) | 0x80;
  const h = Array.from(b, (x) => x.toString(16).padStart(2, "0")).join("");
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
}


type UnitInfo = { id: string; title: string; track: "both" | "amc12" };

export function MockExam({
  track,
  problems: pool,
  units,
}: {
  track: Track;
  problems: MockProblem[];
  units: UnitInfo[];
}) {
  const { recordMock, data } = useApp();
  const unitById = useMemo(() => Object.fromEntries(units.map((u) => [u.id, u])), [units]);

  // AMC 10 mocks only use problems on both tests
  const eligible = useMemo(() => (track === "amc12" ? pool : pool.filter((p) => p.track === "both")), [pool, track]);

  const [phase, setPhase] = useState<"intro" | "exam" | "results">("intro");
  const [problems, setProblems] = useState<MockProblem[]>([]);
  const [answers, setAnswers] = useState<Record<string, ExamAnswer>>({});
  const [flags, setFlags] = useState<Record<string, boolean>>({});
  const [i, setI] = useState(0);
  const [endsAt, setEndsAt] = useState(0);
  const [confirming, setConfirming] = useState(false);
  const [record, setRecord] = useState<MockExamRecord | null>(null);

  const start = () => {
    // Five sections that get harder, with nothing from the previous mock
    const sections = buildMock(eligible, track, data?.mocks ?? []);
    setProblems(sections.flatMap((sec) => sec.problems).slice(0, examConfig.questionCount));
    setAnswers({});
    setFlags({});
    setI(0);
    setEndsAt(Date.now() + examConfig.timeLimitMinutes * 60000);
    setRecord(null);
    setPhase("exam");
    window.scrollTo(0, 0);
  };

  const submit = useCallback(async () => {
    if (phase !== "exam") return;
    setConfirming(false);
    const result = scoreExam(problems, answers);
    const breakdown: MockExamRecord["breakdown"] = {};
    for (const p of problems) {
      const u = p.topic;
      breakdown[u] ??= { correct: 0, total: 0 };
      breakdown[u].total++;
      if (answers[p.id] === p.answer) breakdown[u].correct++;
    }
    const rec: MockExamRecord = {
      id: newId(),
      track,
      ...result,
      answers: Object.fromEntries(problems.map((p) => [p.id, answers[p.id] ?? null])),
      breakdown,
      at: new Date().toISOString(),
    };
    setRecord(rec);
    setPhase("results");
    window.scrollTo(0, 0);
    await recordMock(
      rec,
      problems
        .filter((p) => answers[p.id])
        .map((p) => ({ problemId: p.id, skillId: p.skillId, correct: answers[p.id] === p.answer, timeTakenMs: 0 })),
    );
  }, [phase, problems, answers, track, recordMock]);

  // Warn before leaving the page during an exam
  useEffect(() => {
    if (phase !== "exam") return;
    const warn = (e: BeforeUnloadEvent) => e.preventDefault();
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [phase]);

  const label = TRACK_LABELS[track];
  const cutoff = examConfig.aimeCutoffs[track];

  if (phase === "intro") {
    return (
      <div className="mx-auto max-w-2xl">
        <Link href="/mock" className="text-sm text-muted hover:text-heading">
          All mock exams
        </Link>
        <h1 className="mt-2 text-4xl font-bold">{label} mock exam</h1>
        <ul className="mt-8 space-y-3 rounded-lg border border-line bg-surface p-6 text-body">
          <li>
            <strong className="text-heading">{examConfig.questionCount} questions</strong> in{" "}
            <strong className="text-heading">{examConfig.timeLimitMinutes} minutes</strong>. The exam submits itself when time runs out.
          </li>
          <li>
            {examConfig.scoring.correct} points for a correct answer, {examConfig.scoring.blank} for a blank, {examConfig.scoring.wrong} for a wrong
            answer. Leaving a question blank is better than guessing wildly.
          </li>
          <li>Like the real test, the questions get harder as you go: five sections of five, from warmups to the hardest problems.</li>
          <li>Every mock is a new test. Nothing from your previous mock appears, not even the same kind of problem with new numbers.</li>
          <li>Skip around, flag questions to come back to, and change answers any time before you submit.</li>
          <li>No calculators. Have scratch paper and a pencil ready.</li>
        </ul>
        {eligible.length < examConfig.questionCount && (
          <div className="mt-6">
            <PlaceholderNote>
              The problem bank only has {eligible.length} {label} problems so far, so this exam will have {eligible.length} questions instead
              of {examConfig.questionCount}. Add more problems to get a full length exam.
            </PlaceholderNote>
          </div>
        )}
        <Button size="lg" className="mt-8" onClick={start} disabled={eligible.length === 0}>
          Start the {examConfig.timeLimitMinutes} minute timer
        </Button>
      </div>
    );
  }

  if (phase === "results" && record) {
    const qualified = record.maxScore === examConfig.questionCount * examConfig.scoring.correct && record.score >= cutoff;
    return (
      <div className="mx-auto max-w-3xl">
        <p className="text-muted">{label} mock exam results</p>
        <div className="anim-rise mt-4 grid gap-4 sm:grid-cols-[auto_1fr]">
          <div className="rounded-lg border border-line bg-surface p-6 text-center">
            <p className="font-display text-6xl font-extrabold text-heading tabular-nums">
              <CountUp value={record.score} decimals={1} duration={1200} />
            </p>
            <p className="text-muted">out of {record.maxScore}</p>
          </div>
          <div className="rounded-lg border border-line bg-surface p-6">
            <div className="grid grid-cols-3 gap-3 text-center">
              <Stat value={record.correct} label="Correct" className="text-correct" />
              <Stat value={record.wrong} label="Wrong" className="text-wrong" />
              <Stat value={record.blank} label="Blank" className="text-muted" />
            </div>
            <div className="mt-5 border-t border-line pt-4 text-sm">
              <p className="text-body">
                AIME qualifying score for the {label}: <strong className="text-heading">{cutoff}</strong>
              </p>
              <p className={`mt-1 font-semibold ${qualified ? "text-correct" : "text-muted"}`}>
                {record.maxScore < examConfig.questionCount * examConfig.scoring.correct
                  ? "This was a shortened exam, so it is not compared to the cutoff and does not count for the top climb checkpoints."
                  : qualified
                    ? "This score would qualify for the AIME."
                    : `${(cutoff - record.score).toFixed(1).replace(/\.0$/, "")} more points to reach the cutoff.`}
              </p>
            </div>
          </div>
        </div>

        <h2 className="mt-10 text-xl font-bold">By topic</h2>
        <div className="mt-4 space-y-3 rounded-lg border border-line bg-surface p-6">
          {Object.entries(record.breakdown).map(([unitId, b]) => (
            <div key={unitId}>
              <div className="mb-1 flex justify-between text-sm">
                <span className="text-heading">{unitById[unitId]?.title ?? unitId}</span>
                <span className="text-muted tabular-nums">
                  {b.correct} / {b.total}
                </span>
              </div>
              <ProgressBar value={b.correct / b.total} />
            </div>
          ))}
        </div>

        <MockReview problems={problems} answers={record.answers} />

        <div className="mt-8 flex flex-wrap gap-3">
          <Button onClick={start}>Take another {label} mock</Button>
          <ButtonLink href="/climb" variant="secondary">
            See your climb
          </ButtonLink>
        </div>
      </div>
    );
  }

  // Exam in progress
  const problem = problems[i];
  const answeredCount = problems.filter((p) => answers[p.id]).length;
  const setAnswer = (k: ChoiceKey) => setAnswers((a) => ({ ...a, [problem.id]: a[problem.id] === k ? null : k }));

  return (
    <div className="mx-auto max-w-6xl">
      <div className="sticky top-16 z-30 -mx-4 mb-6 flex items-center justify-between gap-3 border-b border-line bg-bg/95 px-4 py-3 backdrop-blur sm:mx-0 sm:rounded-b-xl sm:border-x">
        <span className="font-display font-bold text-heading">{label} mock</span>
        <span className="hidden text-sm text-muted sm:inline">
          {answeredCount} of {problems.length} answered
        </span>
        <div className="flex items-center gap-2">
          <Timer endsAt={endsAt} onExpire={submit} />
          <Button size="sm" onClick={() => setConfirming(true)}>
            Submit
          </Button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_260px]">
        <div key={problem.id} className="anim-rise rounded-lg border border-line bg-surface p-5 sm:p-7">
          <div className="mb-4 flex items-center justify-between">
            <span className="font-display text-lg font-bold text-heading">Problem {i + 1}</span>
            <button
              type="button"
              onClick={() => setFlags((f) => ({ ...f, [problem.id]: !f[problem.id] }))}
              aria-pressed={!!flags[problem.id]}
              className={`inline-flex items-center gap-2 rounded-lg border px-3 py-1.5 text-sm font-semibold ${
                flags[problem.id] ? "border-accent bg-accent/15 text-heading" : "border-line text-muted hover:text-heading"
              }`}
            >
              <Flag className="h-4 w-4" aria-hidden />
              {flags[problem.id] ? "Flagged" : "Flag for review"}
            </button>
          </div>
          <Markdown className="text-lg text-heading">{problem.prompt}</Markdown>
          {problem.image && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={problem.image} alt="Diagram for this problem" className="mx-auto my-5 max-h-80 rounded-lg bg-white p-2" />
          )}
          <div role="radiogroup" aria-label="Answer choices" className="mt-6 grid gap-2.5">
            {CHOICE_KEYS.map((k) => (
              <ChoiceButton
                key={k}
                letter={k}
                content={problem.choices[k]}
                state={answers[problem.id] === k ? "selected" : "idle"}
                onSelect={() => setAnswer(k)}
              />
            ))}
          </div>
          <p className="mt-3 text-sm text-muted">Click a selected answer again to clear it and leave the question blank.</p>
          <div className="mt-6 flex justify-between gap-3">
            <Button variant="secondary" onClick={() => setI(i - 1)} disabled={i === 0}>
              Previous
            </Button>
            {i < problems.length - 1 ? (
              <Button variant="secondary" onClick={() => setI(i + 1)}>
                Next
              </Button>
            ) : (
              <Button onClick={() => setConfirming(true)}>Review and submit</Button>
            )}
          </div>
        </div>

        <aside className="lg:sticky lg:top-36 lg:self-start">
          <div className="rounded-lg border border-line bg-surface p-4">
            <p className="mb-3 text-sm font-semibold text-muted">Questions</p>
            <div className="grid grid-cols-5 gap-2">
              {problems.map((p, n) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setI(n)}
                  aria-label={`Question ${n + 1}${answers[p.id] ? ", answered" : ""}${flags[p.id] ? ", flagged" : ""}`}
                  aria-current={n === i ? "step" : undefined}
                  className={`relative grid h-10 place-items-center rounded-lg border text-sm font-semibold tabular-nums ${
                    n === i
                      ? "border-primary bg-primary text-white"
                      : answers[p.id]
                        ? "border-accent/60 bg-accent/20 text-heading"
                        : "border-line bg-surface-2 text-muted hover:text-heading"
                  }`}
                >
                  {n + 1}
                  {flags[p.id] && <span className="absolute right-1 top-1 h-1.5 w-1.5 rounded-full bg-accent-soft" aria-hidden />}
                </button>
              ))}
            </div>
            <div className="mt-4 space-y-1.5 text-xs text-muted">
              <p className="flex items-center gap-2">
                <span className="h-3 w-3 rounded bg-accent/40" /> Answered
              </p>
              <p className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-accent-soft" /> Flagged
              </p>
            </div>
          </div>
        </aside>
      </div>

      {confirming && (
        <div className="anim-fade fixed inset-0 z-50 grid place-items-center bg-black/70 px-4" role="dialog" aria-modal="true" aria-labelledby="submit-title">
          <div className="anim-level-up w-full max-w-md rounded-lg border border-line bg-surface p-6">
            <h2 id="submit-title" className="text-2xl font-bold">
              Submit your exam?
            </h2>
            <p className="mt-2 text-body">
              You answered {answeredCount} of {problems.length} questions.
              {problems.length - answeredCount > 0 && ` ${problems.length - answeredCount} will be scored as blank.`}
              {Object.values(flags).filter(Boolean).length > 0 && ` You still have ${Object.values(flags).filter(Boolean).length} flagged.`}
            </p>
            <div className="mt-6 flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setConfirming(false)} autoFocus>
                Keep working
              </Button>
              <Button onClick={() => void submit()}>Submit exam</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Stat({ value, label, className }: { value: number; label: string; className: string }) {
  return (
    <div>
      <p className={`font-display text-3xl font-bold tabular-nums ${className}`}>
        <CountUp value={value} />
      </p>
      <p className="text-sm text-muted">{label}</p>
    </div>
  );
}
