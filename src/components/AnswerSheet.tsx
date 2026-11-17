"use client";

import { useState } from "react";
import { CHOICE_KEYS } from "./problem";

// A fixed, made up set of answers so the sheet looks the same on every visit
const PATTERN = [2, 0, 3, 1, 4, 2, 2, 0, 1, 3, 4, 0, 2, 1, 3, 3, 0, 4, 1, 2, 0, 3, 2, 4, 1];

/**
 * An AMC style answer sheet (rows of A to E bubbles, in blocks of five questions)
 * that fills itself in when the page loads. Visitors can click any bubble to change it.
 */
export function AnswerSheet({ count = 25 }: { count?: number }) {
  const [answers, setAnswers] = useState<number[]>(PATTERN.slice(0, count));
  const [touched, setTouched] = useState<Record<number, boolean>>({});
  const blocks = Array.from({ length: Math.ceil(count / 5) }, (_, b) => b);

  return (
    <div className="overflow-x-auto" role="group" aria-label="Sample answer sheet">
      <div className="grid min-w-[340px] grid-cols-5 gap-x-2.5 sm:gap-x-4">
        {blocks.map((b) => (
          <div key={b}>
            <div className="mb-1.5 grid grid-cols-[18px_repeat(5,1fr)] items-center gap-x-[3px]" aria-hidden>
              <span />
              {CHOICE_KEYS.map((k) => (
                <span key={k} className="text-center text-[10px] font-semibold text-muted/70">
                  {k}
                </span>
              ))}
            </div>
            {Array.from({ length: 5 }, (_, r) => {
              const q = b * 5 + r;
              if (q >= count) return null;
              return (
                <div key={q} className="mb-[5px] grid grid-cols-[18px_repeat(5,1fr)] items-center gap-x-[3px]">
                  <span className="font-display text-[11px] font-semibold tabular-nums text-muted">{q + 1}</span>
                  {CHOICE_KEYS.map((k, c) => {
                    const on = answers[q] === c;
                    return (
                      <button
                        key={k}
                        type="button"
                        aria-label={`Question ${q + 1}, choice ${k}${on ? ", filled" : ""}`}
                        onClick={() => {
                          setAnswers((prev) => prev.map((v, i) => (i === q ? c : v)));
                          setTouched((t) => ({ ...t, [q]: true }));
                        }}
                        className="relative mx-auto block aspect-square w-full max-w-[17px] rounded-full border border-muted/40 transition-colors hover:border-heading"
                      >
                        {on && (
                          <span
                            key={touched[q] ? `t${c}` : `i${c}`}
                            className="anim-bubble absolute -inset-px rounded-full bg-primary"
                            style={touched[q] ? undefined : { animationDelay: `${650 + q * 55}ms` }}
                          />
                        )}
                      </button>
                    );
                  })}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
