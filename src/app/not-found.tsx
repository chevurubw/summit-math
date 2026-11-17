import { ButtonLink, Container } from "@/components/ui";

export default function NotFound() {
  return (
    <Container className="py-24">
      <h1 className="text-5xl font-bold">Page not found</h1>
      <p className="mt-3 text-muted">That page does not exist or has moved.</p>
      <div className="mt-8 flex gap-3">
        <ButtonLink href="/learn">Open the course</ButtonLink>
        <ButtonLink href="/" variant="secondary">
          Go home
        </ButtonLink>
      </div>
    </Container>
  );
}
