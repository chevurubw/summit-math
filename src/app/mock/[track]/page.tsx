import { notFound } from "next/navigation";
import { AuthGate } from "@/components/AuthGate";
import { MockExam } from "@/components/MockExam";
import { Container } from "@/components/ui";
import { TRACK_LABELS, type Track } from "@/config/exam";
import { getCourseIndex, getMockProblems } from "@/lib/content/load";

// These pages are generated ahead of time for every unit and skill, so waiting on the URL is fine.
export const instant = false;

export function generateStaticParams() {
  return [{ track: "amc10" }, { track: "amc12" }];
}

export async function generateMetadata({ params }: PageProps<"/mock/[track]">) {
  const { track } = await params;
  return { title: `${TRACK_LABELS[track as Track] ?? "Mock"} mock exam` };
}

export default async function Page({ params }: PageProps<"/mock/[track]">) {
  const { track } = await params;
  if (track !== "amc10" && track !== "amc12") notFound();
  const index = getCourseIndex();

  return (
    <Container className="py-6">
      <AuthGate>
        <MockExam
          track={track}
          problems={getMockProblems()}
          units={index.units.map((u) => ({ id: u.id, title: u.title, track: u.track }))}
        />
      </AuthGate>
    </Container>
  );
}
