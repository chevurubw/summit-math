"use client";

import { useState } from "react";
import type { ChoiceKey, Problem } from "@/lib/content/schema";
import { Feedback, HintPanel, ProblemCard, SolutionPanel } from "./problem";
import { Button, ButtonLink } from "./ui";

// The sample problem on the landing page. Replace it with any problem you like.
const sample: Problem = {
  id: "landing_sample",
  skillId: "sample",
  level: "basics",
  track: "both",
  prompt: "How many positive divisors does $36$ have?",
  choices: { A: "$6$", B: "$8$", C: "$9$", D: "$10$", E: "$12$" },
  answer: "C",
  hints: ["Write $36$ as a product of primes: $36 = 2^2 \\cdot 3^2$."],
  solution:
    "Since $36 = 2^2 \\cdot 3^2$, a divisor is $2^a 3^b$ with $a$ and $b$ each from $0$ to $2$. That gives $3 \\times 3 = 9$ divisors, answer **(C)**.",
};

export function TryProblem() {
  const [selected, setSelected] = useState<ChoiceKey | null>(null);
  const [checked, setChecked] = useState(false);
  const [hints, setHints] = useState(0);

  return (
    <ProblemCard
      problem={sample}
      label="Try one now"
      selected={selected}
      checked={checked}
      onSelect={setSelected}
      footer={
        <>
          {!checked && <HintPanel hints={sample.hints} revealed={hints} onReveal={() => setHints((h) => h + 1)} />}
          {checked && (
            <>
              <Feedback correct={selected === sample.answer} answer={sample.answer} />
              <SolutionPanel solution={sample.solution} />
            </>
          )}
          <div className="flex flex-wrap gap-3">
            {!checked ? (
              <Button onClick={() => setChecked(true)} disabled={!selected}>
                Check answer
              </Button>
            ) : (
              <>
                <ButtonLink href="/signup">Practice more problems</ButtonLink>
                <Button
                  variant="secondary"
                  onClick={() => {
                    setChecked(false);
                    setSelected(null);
                    setHints(0);
                  }}
                >
                  Try again
                </Button>
              </>
            )}
          </div>
        </>
      }
    />
  );
}
