import { notFound } from "next/navigation";
import { AuthGate } from "@/components/AuthGate";
import { ProblemSession } from "@/components/ProblemSession";
import { Container } from "@/components/ui";
import { getCourseIndex, getProblems, getUnits } from "@/lib/content/load";

// These pages are generated ahead of time for every unit and skill, so waiting on the URL is fine.
export const instant = false;

const LEVELS = ["basics", "challenge"] as const;

export function generateStaticParams() {
  return getUnits().flatMap((u) =>
    u.skills.flatMap((s) => LEVELS.map((level) => ({ unitId: u.id, skillId: s.id, level }))),
  );
}

export async function generateMetadata({ params }: PageProps<"/learn/[unitId]/[skillId]/practice/[level]">) {
  const { unitId, skillId, level } = await params;
  const skill = getCourseIndex().units.find((u) => u.id === unitId)?.skills.find((s) => s.id === skillId);
  return { title: `${skill?.title ?? "Practice"}: ${level === "challenge" ? "Challenge" : "Basics"}` };
}

export default async function Page({ params }: PageProps<"/learn/[unitId]/[skillId]/practice/[level]">) {
  const { unitId, skillId, level } = await params;
  const unit = getCourseIndex().units.find((u) => u.id === unitId);
  const skill = unit?.skills.find((s) => s.id === skillId);
  if (!unit || !skill || !LEVELS.includes(level as (typeof LEVELS)[number])) notFound();
  const problems = getProblems().filter((p) => p.skillId === skillId && p.level === level);

  return (
    <Container className="py-10">
      <AuthGate>
        <ProblemSession
          problems={problems}
          kind={level as "basics" | "challenge"}
          title={skill.title}
          skillTitles={{ [skill.id]: skill.title }}
          backHref={`/learn/${unit.id}`}
          backLabel={`Back to ${unit.title}`}
        />
      </AuthGate>
    </Container>
  );
}
