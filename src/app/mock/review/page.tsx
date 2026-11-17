import { Suspense } from "react";
import { AuthGate } from "@/components/AuthGate";
import { MockAttempt } from "@/components/MockAttempt";
import { Container } from "@/components/ui";
import { getMockProblems } from "@/lib/content/load";

export const metadata = { title: "Mock exam review" };

export default function Page() {
  return (
    <Container className="py-12">
      <AuthGate>
        <Suspense fallback={null}>
          <MockAttempt problems={getMockProblems()} />
        </Suspense>
      </AuthGate>
    </Container>
  );
}
