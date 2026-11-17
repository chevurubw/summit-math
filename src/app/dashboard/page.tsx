import { AuthGate } from "@/components/AuthGate";
import { Dashboard } from "@/components/Dashboard";
import { Container } from "@/components/ui";
import { getCourseIndex } from "@/lib/content/load";

export const metadata = { title: "Dashboard" };

export default function Page() {
  return (
    <Container className="py-12">
      <AuthGate>
        <Dashboard index={getCourseIndex()} />
      </AuthGate>
    </Container>
  );
}
