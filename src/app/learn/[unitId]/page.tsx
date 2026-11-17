import { masteryRules } from "@/config/mastery";
import { BookOpen, ClipboardCheck, Dumbbell, FileCheck2, Mountain } from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Amc12Marker, SkillLevel } from "@/components/course";
import { UnitProgress } from "@/components/UnitProgress";
import { ButtonLink, Container, PlaceholderNote } from "@/components/ui";
import { getCourseIndex, getLesson, getUnits } from "@/lib/content/load";

// These pages are generated ahead of time for every unit and skill, so waiting on the URL is fine.
export const instant = false;

export function generateStaticParams() {
  return getUnits().map((u) => ({ unitId: u.id }));
}

export async function generateMetadata({ params }: PageProps<"/learn/[unitId]">) {
  const { unitId } = await params;
  const unit = getCourseIndex().units.find((u) => u.id === unitId);
  return { title: unit?.title ?? "Unit" };
}

export default async function Page({ params }: PageProps<"/learn/[unitId]">) {
  const { unitId } = await params;
  const index = getCourseIndex();
  const unit = index.units.find((u) => u.id === unitId);
  if (!unit) notFound();
  const unitNumber = index.units.indexOf(unit) + 1;
  const hasProblems = unit.skills.some((s) => s.basicsCount + s.challengeCount > 0);

  return (
    <Container className="py-10">
      <nav aria-label="Breadcrumb" className="text-sm text-muted">
        <Link href="/learn" className="hover:text-heading">
          Course
        </Link>
        <span className="mx-2">/</span>
        <span className="text-body">Unit {unitNumber}</span>
      </nav>

      <div className="mt-4 flex flex-col gap-6 border-b border-line pb-8 sm:flex-row sm:items-center sm:justify-between">
        <div className="max-w-2xl">
          <div className="flex items-center gap-3">
            <h1 className="text-4xl font-bold">{unit.title}</h1>
            {unit.track === "amc12" && <Amc12Marker inline />}
          </div>
          <p className="mt-2 text-muted">{unit.description}</p>
        </div>
        <UnitProgress unit={unit} />
      </div>

      {unit.skills.length === 0 ? (
        <div className="mt-10 max-w-2xl space-y-4">
          <p className="text-lg text-heading">This unit does not have any skills yet.</p>
          <PlaceholderNote>
            Add skills to this unit in <code>content/units</code>, then add a lesson for each one in{" "}
            <code>content/lessons</code> and problems in <code>content/problems</code>. The README walks through it.
          </PlaceholderNote>
        </div>
      ) : (
        <div className="mt-8 grid gap-8 lg:grid-cols-[260px_1fr]">
          <aside className="lg:sticky lg:top-24 lg:self-start">
            <nav aria-label="Skills in this unit" className="rounded-lg border border-line bg-surface p-3">
              <p className="px-3 pb-2 pt-1 text-sm font-semibold text-muted">Skills</p>
              {unit.skills.map((s) => (
                <a key={s.id} href={`#${s.id}`} className="block rounded-lg px-3 py-2 text-[0.95rem] text-body hover:bg-surface-2 hover:text-heading">
                  {s.title}
                  {s.amc12Only && <span className="ml-2 font-display text-[11px] font-bold text-primary">12</span>}
                </a>
              ))}
              <div className="mt-2 border-t border-line pt-2">
                <Link href={`/learn/${unit.id}/quiz`} className="flex items-center gap-2 rounded-lg px-3 py-2 text-[0.95rem] text-body hover:bg-surface-2 hover:text-heading">
                  <ClipboardCheck className="h-4 w-4 text-accent-soft" aria-hidden /> Unit quiz
                </Link>
                <Link href={`/learn/${unit.id}/test`} className="flex items-center gap-2 rounded-lg px-3 py-2 text-[0.95rem] text-body hover:bg-surface-2 hover:text-heading">
                  <FileCheck2 className="h-4 w-4 text-accent-soft" aria-hidden /> Unit test
                </Link>
              </div>
            </nav>
          </aside>

          <div className="space-y-5">
            {unit.skills.map((s, i) => {
              const lesson = getLesson(s.id);
              return (
                <section key={s.id} id={s.id} className="relative scroll-mt-24 overflow-hidden rounded-lg border border-line bg-surface p-6">
                  {s.amc12Only && <Amc12Marker />}
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="text-sm text-muted">Skill {i + 1}</p>
                      <h2 className="mt-1 text-2xl font-bold">{s.title}</h2>
                      {s.description && <p className="mt-1 text-muted">{s.description}</p>}
                    </div>
                    <SkillLevel skillId={s.id} />
                  </div>
                  <div className="mt-6 grid gap-3 sm:grid-cols-3">
                    <Activity
                      href={`/learn/${unit.id}/${s.id}`}
                      icon={<BookOpen className="h-5 w-5" />}
                      title={lesson?.frontmatter.videoUrl ? "Watch and read" : "Read the lesson"}
                      detail={lesson ? "Lesson" : "Lesson coming soon"}
                    />
                    <Activity
                      href={`/learn/${unit.id}/${s.id}/practice/basics`}
                      icon={<Dumbbell className="h-5 w-5" />}
                      title="Basics"
                      detail={`Try ${masteryRules.basicsSetSize} basic questions`}
                    />
                    <Activity
                      href={`/learn/${unit.id}/${s.id}/practice/challenge`}
                      icon={<Mountain className="h-5 w-5" />}
                      title="Challenge"
                      detail={`Try ${masteryRules.challengeSetSize} challenging questions`}
                    />
                  </div>
                </section>
              );
            })}

            <section className="grid gap-4 rounded-lg border border-line bg-surface p-6 sm:grid-cols-2">
              <div>
                <h2 className="text-xl font-bold">Unit quiz</h2>
                <p className="mt-1 text-sm text-muted">A short mixed set. Do well and your skills level up.</p>
                <ButtonLink href={`/learn/${unit.id}/quiz`} variant="secondary" className="mt-4" aria-disabled={!hasProblems}>
                  Start quiz
                </ButtonLink>
              </div>
              <div>
                <h2 className="text-xl font-bold">Unit test</h2>
                <p className="mt-1 text-sm text-muted">Every skill in the unit. The only way to take a skill from Proficient to Mastered.</p>
                <ButtonLink href={`/learn/${unit.id}/test`} className="mt-4" aria-disabled={!hasProblems}>
                  Start unit test
                </ButtonLink>
              </div>
            </section>
          </div>
        </div>
      )}
    </Container>
  );
}

function Activity({ href, icon, title, detail }: { href: string; icon: React.ReactNode; title: string; detail: string }) {
  return (
    <Link href={href} className="btn-press flex items-center gap-3 rounded-md border border-line bg-surface-2 px-4 py-3 shadow-[0_3px_0_0_#050507] hover:border-muted">
      <span className="shrink-0 text-accent-soft">{icon}</span>
      <span>
        <span className="block font-semibold text-heading">{title}</span>
        <span className="block text-sm text-muted">{detail}</span>
      </span>
    </Link>
  );
}
