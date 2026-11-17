"use client";

import Link from "next/link";
import { examConfig, TRACK_LABELS, type Track } from "@/config/exam";
import { useApp } from "./AppProvider";
import { PageHeader } from "./ui";

export function MockHome() {
  const { data } = useApp();
  const order: Track[] = ["amc10", "amc12"];
  const history = [...(data?.mocks ?? [])].reverse();

  return (
    <>
      <PageHeader
        title="Mock exams"
        intro={`Full practice tests: ${examConfig.questionCount} questions, ${examConfig.timeLimitMinutes} minutes, and official scoring. Your best score unlocks checkpoints on your climb.`}
      />
      <div className="grid gap-4 md:grid-cols-2">
        {order.map((t) => (
          <Link
            key={t}
            href={`/mock/${t}`}
            className="btn-press relative overflow-hidden rounded-lg border-2 border-line bg-surface p-7 shadow-[0_3px_0_0_#050507] transition-colors hover:border-primary"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">{TRACK_LABELS[t]}</h2>

            </div>
            <p className="mt-2 text-muted">
              {t === "amc10" ? "Core topics only." : "Core topics plus AMC 12 only topics."} AIME qualifying score: {examConfig.aimeCutoffs[t]}
            </p>
            <p className="mt-6 font-semibold text-heading">Start a {TRACK_LABELS[t]} mock</p>
          </Link>
        ))}
      </div>

      <h2 className="mt-12 text-2xl font-bold">Your past exams</h2>
      {history.length > 0 && <p className="mt-1 text-sm text-muted">Open any exam to see the questions you missed and what to study for each one.</p>}
      {history.length === 0 ? (
        <p className="mt-4 rounded-lg border border-dashed border-line px-6 py-8 text-center text-muted">
          No mock exams yet. Your scores will show up here after your first one.
        </p>
      ) : (
        <div className="mt-4 overflow-x-auto rounded-lg border border-line bg-surface">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-line text-muted">
              <tr>
                <th className="px-5 py-3 font-semibold">Date</th>
                <th className="px-5 py-3 font-semibold">Test</th>
                <th className="px-5 py-3 font-semibold">Score</th>
                <th className="px-5 py-3 font-semibold">Correct</th>
                <th className="px-5 py-3 font-semibold">Wrong</th>
                <th className="px-5 py-3 font-semibold">Blank</th>
                <th className="px-5 py-3 font-semibold">
                  <span className="sr-only">Review</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {history.map((m) => (
                <tr key={m.id} className="transition-colors hover:bg-surface-2/60">
                  <td className="px-5 py-3 text-body">{new Date(m.at).toLocaleDateString()}</td>
                  <td className="px-5 py-3 text-body">{TRACK_LABELS[m.track]}</td>
                  <td className="px-5 py-3 font-semibold text-heading tabular-nums">
                    {m.score} / {m.maxScore}
                  </td>
                  <td className="px-5 py-3 tabular-nums">{m.correct}</td>
                  <td className="px-5 py-3 tabular-nums">{m.wrong}</td>
                  <td className="px-5 py-3 tabular-nums">{m.blank}</td>
                  <td className="px-5 py-3 text-right">
                    <Link
                      href={`/mock/review?id=${encodeURIComponent(m.id)}`}
                      className="inline-flex items-center rounded-md border border-line bg-surface-2 px-3 py-1.5 text-sm font-semibold text-body transition-colors hover:border-accent hover:text-heading"
                    >
                      Review
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
