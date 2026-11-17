"use client";

import { Lightbulb } from "lucide-react";
import type { ReactNode } from "react";
import type { ChoiceKey, Problem } from "@/lib/content/schema";
import { Markdown } from "./Markdown";
import { Burst, PenMark } from "./motion";

export const CHOICE_KEYS: ChoiceKey[] = ["A", "B", "C", "D", "E"];

export type ChoiceState = "idle" | "selected" | "correct" | "wrong" | "answer";

// Row styles for each state. Wrong answers shake, correct answers glow (see globals.css).
const rowStyles: Record<ChoiceState, string> = {
  idle: "border-line bg-surface-2 hover:border-muted hover:-translate-y-px",
  selected: "border-accent bg-accent/10",
  correct: "border-correct bg-correct/10 anim-glow-correct",
  wrong: "border-wrong bg-wrong/10 anim-shake",
  answer: "border-correct/70 border-dashed bg-surface-2",
};

// The filled part of the answer bubble
const fillStyles: Partial<Record<ChoiceState, string>> = {
  selected: "bg-accent",
  correct: "bg-correct",
  wrong: "bg-wrong",
};

/** One answer choice, drawn as a row with an answer sheet bubble that fills in when chosen. */
export function ChoiceButton({
  letter,
  content,
  state,
  disabled,
  onSelect,
}: {
  letter: ChoiceKey;
  content: string;
  state: ChoiceState;
  disabled?: boolean;
  onSelect?: () => void;
}) {
  const fill = fillStyles[state];
  return (
    <button
      type="button"
      role="radio"
      aria-checked={state === "selected"}
      disabled={disabled}
      onClick={onSelect}
      className={`group flex w-full items-center gap-4 rounded-md border-2 px-4 py-3 text-left transition-[border-color,background-color,transform] duration-150 active:scale-[0.99] disabled:cursor-default disabled:active:scale-100 ${rowStyles[state]}`}
    >
      <span
        className={`relative grid h-9 w-9 shrink-0 place-items-center rounded-full border-2 font-display font-bold transition-colors ${
          state === "answer" ? "border-correct text-correct" : fill ? "border-transparent" : "border-muted/60 text-heading group-hover:border-heading"
        }`}
      >
        {fill && <span key={state} className={`anim-bubble absolute -inset-0.5 rounded-full ${fill}`} />}
        <span className={`relative ${state === "correct" || state === "wrong" ? "text-black" : fill ? "text-white" : ""}`}>{letter}</span>
        {state === "correct" && <Burst />}
      </span>
      <span className="flex-1 text-heading">
        <Markdown inline>{content}</Markdown>
      </span>
      {state === "correct" && <PenMark kind="check" className="h-6 w-6 text-correct" />}
      {state === "wrong" && <PenMark kind="x" className="h-5 w-5 text-wrong" />}
      {state === "answer" && <span className="anim-fade text-xs font-semibold text-correct">Correct answer</span>}
      <span className="sr-only">
        {state === "correct" ? "Correct" : state === "wrong" ? "Incorrect" : state === "answer" ? "This is the correct answer" : ""}
      </span>
    </button>
  );
}

/** The line under a checked problem: a drawn check or X with a short message. */
export function Feedback({ correct, answer, streak = 0 }: { correct: boolean; answer: ChoiceKey; streak?: number }) {
  return (
    <div role="status" className="anim-slide flex items-center gap-3">
      <span className={`grid h-9 w-9 place-items-center rounded-full ${correct ? "bg-correct/15 text-correct" : "bg-wrong/15 text-wrong"}`}>
        <PenMark kind={correct ? "check" : "x"} className="h-5 w-5" />
      </span>
      <p className={`font-display text-xl font-bold ${correct ? "text-correct" : "text-wrong"}`}>
        {correct ? (streak >= 3 ? `${streak} in a row.` : "Correct.") : `Not quite. The answer is (${answer}).`}
      </p>
    </div>
  );
}

/** Hints revealed one at a time. */
export function HintPanel({
  hints,
  revealed,
  onReveal,
  disabled,
}: {
  hints: string[];
  revealed: number;
  onReveal: () => void;
  disabled?: boolean;
}) {
  if (!hints.length) return null;
  return (
    <div className="space-y-3">
      {hints.slice(0, revealed).map((h, i) => (
        <div key={i} className="anim-rise flex gap-3 rounded-md border border-accent/40 bg-accent/10 px-4 py-3">
          <Lightbulb className="mt-1 h-4 w-4 shrink-0 text-accent-soft" aria-hidden />
          <div>
            <p className="text-xs font-semibold text-accent-soft">
              Hint {i + 1} of {hints.length}
            </p>
            <Markdown className="text-body">{h}</Markdown>
          </div>
        </div>
      ))}
      {revealed < hints.length && !disabled && (
        <button
          type="button"
          onClick={onReveal}
          className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold text-accent-soft hover:bg-accent/10"
        >
          <Lightbulb className="h-4 w-4" aria-hidden />
          {revealed === 0 ? "Get a hint" : "Show next hint"}
        </button>
      )}
    </div>
  );
}

export function SolutionPanel({ solution }: { solution: string }) {
  return (
    <div className="anim-rise rounded-md border border-line bg-surface-2 px-5 py-4" style={{ animationDelay: "120ms" }}>
      <p className="mb-1 font-display font-bold text-heading">Solution</p>
      <Markdown>{solution}</Markdown>
    </div>
  );
}

/** Shows one problem: its text, optional image, and the five answer choices. */
export function ProblemCard({
  problem,
  label,
  selected,
  checked,
  onSelect,
  footer,
}: {
  problem: Problem;
  label?: ReactNode;
  selected: ChoiceKey | null;
  checked: boolean;
  onSelect: (key: ChoiceKey) => void;
  footer?: ReactNode;
}) {
  const stateFor = (key: ChoiceKey): ChoiceState => {
    if (!checked) return selected === key ? "selected" : "idle";
    if (key === problem.answer) return selected === key ? "correct" : "answer";
    if (key === selected) return "wrong";
    return "idle";
  };

  return (
    <div className="anim-rise rounded-lg border border-line bg-surface p-5 sm:p-7">
      {label && <div className="mb-4 text-sm text-muted">{label}</div>}
      <Markdown className="text-lg text-heading">{problem.prompt}</Markdown>
      {problem.image && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={problem.image} alt="Diagram for this problem" className="mx-auto my-5 max-h-80 rounded-lg bg-white p-2" />
      )}
      <div role="radiogroup" aria-label="Answer choices" className="mt-6 grid gap-2.5">
        {CHOICE_KEYS.map((k, n) => (
          <div key={k} className="anim-rise" style={{ animationDelay: `${120 + n * 55}ms` }}>
            <ChoiceButton
              letter={k}
              content={problem.choices[k]}
              state={stateFor(k)}
              disabled={checked}
              onSelect={() => onSelect(k)}
            />
          </div>
        ))}
      </div>
      {footer && <div className="mt-6 space-y-4">{footer}</div>}
    </div>
  );
}
