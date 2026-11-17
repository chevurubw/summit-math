import { AuthGate } from "@/components/AuthGate";
import { ClimbView } from "@/components/ProgressView";
import { Container } from "@/components/ui";

export const metadata = { title: "Your climb" };

export default function Page() {
  return (
    <Container className="py-10">
      <AuthGate>
        <ClimbView />
      </AuthGate>
    </Container>
  );
}
