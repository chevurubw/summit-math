import { AuthGate } from "@/components/AuthGate";
import { MockHome } from "@/components/MockHome";
import { Container } from "@/components/ui";

export const metadata = { title: "Mock exams" };

export default function Page() {
  return (
    <Container className="py-12">
      <AuthGate>
        <MockHome />
      </AuthGate>
    </Container>
  );
}
