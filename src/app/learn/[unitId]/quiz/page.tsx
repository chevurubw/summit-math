import { notFound } from "next/navigation";
import { AuthGate } from "@/components/AuthGate";
import { ProblemSession } from "@/components/ProblemSession";
import { Container } from "@/components/ui";
import { masteryRules } from "@/config/mastery";
import { getCourseIndex, getProblemsForUnit, getUnits } from "@/lib/content/load";

// These pages are generated ahead of time for every unit and skill, so waiting on the URL is fine.
export const instant = false;

export function generateStaticParams() {
  return getUnits().map((u) => ({ unitId: u.id }));
}

export async function generateMetadata({ params }: PageProps<"/learn/[unitId]/quiz">) {
  const { unitId } = await params;
  const unit = getCourseIndex().units.find((u) => u.id === unitId);
  return { title: `${unit?.title ?? "Unit"}: Unit quiz` };
}

export default async function Page({ params }: PageProps<"/learn/[unitId]/quiz">) {
  const { unitId } = await params;
  const unit = getCourseIndex().units.find((u) => u.id === unitId);
  if (!unit) notFound();
  const skillTitles = Object.fromEntries(unit.skills.map((s) => [s.id, s.title]));

  return (
    <Container className="py-10">
      <AuthGate>
        <ProblemSession
          problems={getProblemsForUnit(unit.id)}
          kind="quiz"
          limit={masteryRules.quizLength}
          title={unit.title}
          skillTitles={skillTitles}
          backHref={`/learn/${unit.id}`}
          backLabel={`Back to ${unit.title}`}
        />
      </AuthGate>
    </Container>
  );
}
