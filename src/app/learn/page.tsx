import Link from "next/link";
import { CourseMap } from "@/components/course";
import { MasteryLegend } from "@/components/progress";
import { Container, PageHeader } from "@/components/ui";
import { getCourseIndex } from "@/lib/content/load";

export const metadata = { title: "Course" };

export default function Page() {
  const index = getCourseIndex();
  return (
    <Container className="py-12">
      <PageHeader title="Course" intro="Work through each unit skill by skill. Your mastery level for every skill shows on its unit card." />
      <Link
        href="/learn/start"
        className="mb-8 block rounded-lg border border-accent/40 bg-surface p-5 transition-colors hover:border-accent"
      >
        <span className="text-lg font-bold text-heading">New to the AMC? Start here.</span>
        <span className="mt-1 block text-body">What the contest is, how scoring and guessing work, how to use this site, and test day strategy.</span>
      </Link>
      <div className="mb-10">
        <MasteryLegend />
      </div>
      <CourseMap index={index} />
    </Container>
  );
}
