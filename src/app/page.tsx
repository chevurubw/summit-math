import { Lightbulb } from "lucide-react";
import { AnswerSheet } from "@/components/AnswerSheet";
import { MasteryBadge } from "@/components/progress";
import { TryProblem } from "@/components/TryProblem";
import { ButtonLink, Container } from "@/components/ui";
import { examConfig } from "@/config/exam";
import { site } from "@/config/site";

const steps = [
  { title: "Learn", text: "Watch a short video or read a lesson on one skill." },
  { title: "Practice", text: "Work through problems with hints and full solutions." },
  { title: "Master", text: "Level up each skill from Familiar to Mastered." },
  { title: "Test", text: "Take timed mock exams scored like the real thing." },
];

const shared = ["Algebra", "Geometry", "Number theory", "Counting and probability"];
const amc12Only = ["Trigonometry", "Logarithms", "Complex numbers", "Polynomials", "Conic sections", "Series"];

export default function Home() {
  return (
    <>
      {/* Hero: scratch paper background, a real problem to try, and an answer sheet that fills itself in */}
      <section className="graph-paper anim-fade border-b border-line">
        <Container className="grid items-center gap-12 py-12 lg:grid-cols-[1fr_1.05fr] lg:py-16">
          <div className="min-w-0">
            <h1 className="anim-rise text-[2.6rem] font-extrabold leading-[1] sm:text-[3.6rem]">
              Get ready for the AMC, one skill at a time.
            </h1>
            <p className="anim-rise mt-6 max-w-lg text-lg text-body" style={{ animationDelay: "120ms" }}>
              {site.description}
            </p>
            <div className="anim-rise mt-8 flex flex-wrap gap-3" style={{ animationDelay: "220ms" }}>
              <ButtonLink href="/signup" size="lg">
                Start learning
              </ButtonLink>
              <ButtonLink href="/learn" size="lg" variant="secondary">
                Browse the course
              </ButtonLink>
            </div>
            <div className="anim-rise mt-12 border-t border-line pt-5" style={{ animationDelay: "320ms" }}>
              <div className="mb-4 flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
                <p className="font-display font-semibold text-heading">
                  {examConfig.questionCount} questions. {examConfig.timeLimitMinutes} minutes. No calculator.
                </p>
                <p className="text-sm text-muted">Go ahead, fill in a bubble.</p>
              </div>
              <AnswerSheet count={examConfig.questionCount} />
            </div>
          </div>
          <div className="anim-rise min-w-0" style={{ animationDelay: "300ms" }}>
            <TryProblem />
          </div>
        </Container>
      </section>

      {/* How it works: a real sequence, so it is numbered */}
      <section className="py-20">
        <Container>
          <h2 className="text-3xl font-bold sm:text-4xl">How it works</h2>
          <ol className="mt-10 grid gap-x-8 gap-y-10 sm:grid-cols-2 lg:grid-cols-4">
            {steps.map((s, i) => (
              <li key={s.title} className="border-l-2 border-line pl-5">
                <span className="font-display text-sm font-bold tabular-nums text-primary">Step {i + 1}</span>
                <h3 className="mt-1 text-2xl font-bold">{s.title}</h3>
                <p className="mt-1 text-muted">{s.text}</p>
              </li>
            ))}
          </ol>
        </Container>
      </section>

      {/* Tracks */}
      <section className="border-y border-line py-20">
        <Container>
          <div className="grid gap-10 lg:grid-cols-[1fr_2fr]">
            <div>
              <h2 className="text-3xl font-bold sm:text-4xl">AMC 10 or AMC 12</h2>
              <p className="mt-3 text-muted">
                Same length, same scoring. The AMC 12 adds precalculus, and asks for a lower score to reach the AIME.
              </p>
            </div>
            <div className="grid overflow-hidden rounded-lg border border-line sm:grid-cols-2">
              <div className="bg-surface p-7">
                <h3 className="text-2xl font-bold">AMC 10</h3>
                <p className="mt-1 text-sm text-muted">Grade 10 and below</p>
                <ul className="mt-5 space-y-1.5 text-heading">
                  {shared.map((t) => (
                    <li key={t}>{t}</li>
                  ))}
                </ul>
                <p className="mt-6 border-t border-line pt-4 text-sm text-muted">
                  AIME qualifying score <span className="font-display font-bold text-heading">{examConfig.aimeCutoffs.amc10}</span>
                </p>
              </div>
              <div className="border-t border-line bg-surface-2 p-7 sm:border-l sm:border-t-0">
                <h3 className="text-2xl font-bold">AMC 12</h3>
                <p className="mt-1 text-sm text-muted">Grade 12 and below. Everything on the AMC 10, plus</p>
                <ul className="mt-5 grid grid-cols-2 gap-x-4 gap-y-1.5 text-heading">
                  {amc12Only.map((t) => (
                    <li key={t} className="flex items-center gap-2">
                      <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-primary" aria-hidden />
                      {t}
                    </li>
                  ))}
                </ul>
                <p className="mt-6 border-t border-line pt-4 text-sm text-muted">
                  AIME qualifying score <span className="font-display font-bold text-heading">{examConfig.aimeCutoffs.amc12}</span>
                </p>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* What studying looks like: real pieces of the interface instead of icons */}
      <section className="py-20">
        <Container>
          <h2 className="max-w-2xl text-3xl font-bold sm:text-4xl">What a study session looks like</h2>
          <div className="mt-12 grid gap-12 md:grid-cols-3">
            <div>
              <div className="flex h-36 items-center rounded-lg border border-line bg-surface p-5">
                <div className="flex w-full gap-3 rounded-md border border-accent/40 bg-accent/10 px-4 py-3">
                  <Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-accent-soft" aria-hidden />
                  <div className="text-sm">
                    <p className="text-xs font-semibold text-accent-soft">Hint 1 of 2</p>
                    <p className="text-body">Start by writing 36 as a product of primes.</p>
                  </div>
                </div>
              </div>
              <h3 className="mt-5 text-xl font-bold">Hints when you are stuck</h3>
              <p className="mt-1 text-muted">One hint at a time, then a full worked solution after you answer.</p>
            </div>
            <div>
              <div className="flex h-36 flex-col justify-center gap-2.5 rounded-lg border border-line bg-surface p-5">
                <MasteryBadge level="attempted" />
                <MasteryBadge level="familiar" />
                <MasteryBadge level="proficient" />
                <MasteryBadge level="mastered" />
              </div>
              <h3 className="mt-5 text-xl font-bold">A level for every skill</h3>
              <p className="mt-1 text-muted">
                Practice fills in your first bubbles. Only a unit test fills the last one, and skills you stop practicing fade.
              </p>
            </div>
            <div>
              <div className="flex h-36 items-center justify-between gap-4 rounded-lg border border-line bg-surface p-5">
                <span className="font-display text-4xl font-extrabold tabular-nums text-heading">74:59</span>
                <span className="grid grid-cols-5 gap-1.5" aria-hidden>
                  {Array.from({ length: 15 }, (_, i) => (
                    <span key={i} className={`h-3.5 w-3.5 rounded-full ${i < 9 ? "bg-accent" : "border border-muted/40"}`} />
                  ))}
                </span>
              </div>
              <h3 className="mt-5 text-xl font-bold">Mock exams on the clock</h3>
              <p className="mt-1 text-muted">Official scoring, a question navigator, and a full review of every problem.</p>
            </div>
          </div>
        </Container>
      </section>


      {/* Closing */}
      <section className="graph-paper border-t border-line">
        <Container className="flex flex-col gap-8 py-20 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="max-w-xl text-4xl font-extrabold sm:text-5xl">Problem 1 is waiting.</h2>
            <p className="mt-3 max-w-md text-muted">Make a free account and take your first step up the mountain.</p>
          </div>
          <ButtonLink href="/signup" size="lg">
            Start learning
          </ButtonLink>
        </Container>
      </section>
    </>
  );
}
