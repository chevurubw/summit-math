import { MDXRemote } from "next-mdx-remote/rsc";
import Link from "next/link";
import { notFound } from "next/navigation";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { Amc12Marker, SkillLevel } from "@/components/course";
import { mdxComponents, VideoEmbed } from "@/components/lesson";
import { ButtonLink, Container } from "@/components/ui";
import { getCourseIndex, getLesson, getUnits } from "@/lib/content/load";

// These pages are generated ahead of time for every unit and skill, so waiting on the URL is fine.
export const instant = false;

export function generateStaticParams() {
  return getUnits().flatMap((u) => u.skills.map((s) => ({ unitId: u.id, skillId: s.id })));
}

export async function generateMetadata({ params }: PageProps<"/learn/[unitId]/[skillId]">) {
  const { unitId, skillId } = await params;
  const skill = getCourseIndex().units.find((u) => u.id === unitId)?.skills.find((s) => s.id === skillId);
  return { title: skill?.title ?? "Lesson" };
}

export default async function Page({ params }: PageProps<"/learn/[unitId]/[skillId]">) {
  const { unitId, skillId } = await params;
  const unit = getCourseIndex().units.find((u) => u.id === unitId);
  const skill = unit?.skills.find((s) => s.id === skillId);
  if (!unit || !skill) notFound();
  const lesson = getLesson(skillId);
  const position = unit.skills.indexOf(skill);
  const nextSkill = unit.skills[position + 1];

  return (
    <Container className="py-10">
      <div className="grid gap-10 lg:grid-cols-[1fr_260px]">
        <article className="min-w-0">
          <nav aria-label="Breadcrumb" className="text-sm text-muted">
            <Link href="/learn" className="hover:text-heading">
              Course
            </Link>
            <span className="mx-2">/</span>
            <Link href={`/learn/${unit.id}`} className="hover:text-heading">
              {unit.title}
            </Link>
          </nav>
          <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
            <h1 className="flex items-center gap-3 text-4xl font-bold">
              {lesson?.frontmatter.title ?? skill.title}
              {skill.amc12Only && <Amc12Marker inline />}
            </h1>
            <SkillLevel skillId={skill.id} />
          </div>

          {lesson?.frontmatter.videoUrl && (
            <div className="mt-8">
              <VideoEmbed url={lesson.frontmatter.videoUrl} title={skill.title} />
            </div>
          )}

          <div className="prose-math mt-8 max-w-[70ch] text-[1.08rem]">
            {lesson ? (
              <MDXRemote
                source={lesson.body}
                components={mdxComponents}
                options={{ blockJS: false, mdxOptions: { remarkPlugins: [remarkMath, remarkGfm], rehypePlugins: [rehypeKatex] } }}
              />
            ) : (
              <p className="rounded-md border border-line bg-surface px-4 py-3 text-body">
                The lesson for this skill is on its way. You can already practice it below.
              </p>
            )}
          </div>

          <div className="mt-12 rounded-lg border border-line bg-surface p-6">
            <h2 className="text-2xl font-bold">Practice this skill</h2>
            <p className="mt-1 text-muted">Basics takes this skill to Familiar. A perfect Challenge set takes it to Proficient. Pass the unit test to reach Mastered.</p>
            <div className="mt-5 flex flex-wrap gap-3">
              <ButtonLink href={`/learn/${unit.id}/${skill.id}/practice/basics`}>Practice basics</ButtonLink>
              <ButtonLink href={`/learn/${unit.id}/${skill.id}/practice/challenge`} variant="secondary">
                Try the challenge set
              </ButtonLink>
            </div>
          </div>
          {nextSkill && (
            <p className="mt-6 text-sm text-muted">
              Next skill:{" "}
              <Link href={`/learn/${unit.id}/${nextSkill.id}`} className="font-semibold text-accent-soft hover:underline">
                {nextSkill.title}
              </Link>
            </p>
          )}
        </article>

        <aside className="lg:sticky lg:top-24 lg:self-start">
          <nav aria-label={`Skills in ${unit.title}`} className="rounded-lg border border-line bg-surface p-3">
            <p className="px-3 pb-2 pt-1 text-sm font-semibold text-muted">{unit.title}</p>
            {unit.skills.map((s) => (
              <Link
                key={s.id}
                href={`/learn/${unit.id}/${s.id}`}
                aria-current={s.id === skill.id ? "page" : undefined}
                className={`block rounded-lg px-3 py-2 text-[0.95rem] ${
                  s.id === skill.id ? "bg-surface-2 font-semibold text-heading" : "text-body hover:bg-surface-2"
                }`}
              >
                {s.title}
              </Link>
            ))}
          </nav>
        </aside>
      </div>
    </Container>
  );
}
