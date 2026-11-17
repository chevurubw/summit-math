"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useMemo } from "react";
import { examConfig, TRACK_LABELS } from "@/config/exam";
import type { MockProblem } from "@/lib/content/schema";
import { useApp } from "./AppProvider";
import { MockReview } from "./MockReview";
import { ProgressBar } from "./progress";
import { ButtonLink } from "./ui";

/** One past mock exam, opened from the history table: the score, a topic breakdown, and every question. */
export function MockAttempt({ problems: bank }: { problems: MockProblem[] }) {
  const id = useSearchParams().get("id");
  const { data, index } = useApp();
  const record = data?.mocks.find((m) => m.id === id);

  // Saved answers don't keep question order everywhere, so rebuild it: sections run from easiest to hardest.
  const { problems, missing } = useMemo(() => {
    if (!record) return { problems: [], missing: 0 };
    const byId = new Map(bank.map((p) => [p.id, p]));
    const found = Object.keys(record.answers).map((pid) => byId.get(pid));
    const ps = found.filter((p): p is MockProblem => !!p).sort((a, b) => a.difficulty - b.difficulty);
    return { problems: ps, missing: found.length - ps.length };
  }, [record, bank]);

  if (!data) return null;
  if (!record) {
    return (
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="text-3xl font-bold">Exam not found</h1>
        <p className="mt-3 text-muted">This mock exam isn't in your history. It may have been from another account, or your progress was reset.</p>
        <ButtonLink href="/mock" className="mt-6">
          See your mock exams
        </ButtonLink>
      </div>
    );
  }

  const label = TRACK_LABELS[record.track];
  const cutoff = examConfig.aimeCutoffs[record.track];
  const unitTitle = (u: string) => index.units.find((x) => x.id === u)?.title ?? u;

  return (
    <div className="mx-auto max-w-3xl">
      <Link href="/mock" className="text-sm text-muted hover:text-heading">
        All mock exams
      </Link>
      <h1 className="mt-2 text-4xl font-bold">{label} mock review</h1>
      <p className="mt-1 text-muted">
        Taken {new Date(record.at).toLocaleDateString(undefined, { month: "long", day: "numeric", year: "numeric" })}
      </p>

      <div className="mt-6 grid gap-4 sm:grid-cols-[auto_1fr]">
        <div className="rounded-lg border border-line bg-surface p-6 text-center">
          <p className="font-display text-5xl font-extrabold text-heading tabular-nums">{record.score}</p>
          <p className="text-muted">out of {record.maxScore}</p>
        </div>
        <div className="rounded-lg border border-line bg-surface p-6">
          <div className="grid grid-cols-3 gap-3 text-center">
            <Stat value={record.correct} label="Correct" className="text-correct" />
            <Stat value={record.wrong} label="Wrong" className="text-wrong" />
            <Stat value={record.blank} label="Blank" className="text-muted" />
          </div>
          <p className="mt-4 border-t border-line pt-4 text-sm text-body">
            AIME qualifying score: <strong className="text-heading">{cutoff}</strong>.{" "}
            {record.score >= cutoff ? "This score would qualify." : `${(cutoff - record.score).toFixed(1).replace(/\.0$/, "")} points short.`}
          </p>
        </div>
      </div>

      <h2 className="mt-10 text-xl font-bold">By topic</h2>
      <div className="mt-4 space-y-3 rounded-lg border border-line bg-surface p-6">
        {Object.entries(record.breakdown).map(([unitId, b]) => (
          <div key={unitId}>
            <div className="mb-1 flex justify-between text-sm">
              <span className="text-heading">{unitTitle(unitId)}</span>
              <span className="text-muted tabular-nums">
                {b.correct} / {b.total}
              </span>
            </div>
            <ProgressBar value={b.total ? b.correct / b.total : 0} />
          </div>
        ))}
      </div>

      {missing > 0 && (
        <p className="mt-6 text-sm text-muted">
          {missing} {missing === 1 ? "question" : "questions"} from this exam are no longer in the problem bank, so they aren't shown below.
        </p>
      )}

      <MockReview problems={problems} answers={record.answers} />

      <div className="mt-8 flex flex-wrap gap-3">
        <ButtonLink href={`/mock/${record.track}`}>Take another {label} mock</ButtonLink>
        <ButtonLink href="/mock" variant="secondary">
          All mock exams
        </ButtonLink>
      </div>
    </div>
  );
}

function Stat({ value, label, className }: { value: number; label: string; className: string }) {
  return (
    <div>
      <p className={`font-display text-3xl font-bold tabular-nums ${className}`}>{value}</p>
      <p className="text-sm text-muted">{label}</p>
    </div>
  );
}
