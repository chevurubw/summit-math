import { Container, PlaceholderNote } from "./ui";

export function StaticPage({ title, updated, draft, children }: { title: string; updated?: string; draft?: boolean; children?: React.ReactNode }) {
  return (
    <Container className="py-12">
      <div className="max-w-[68ch]">
        <h1 className="text-4xl font-bold">{title}</h1>
        {updated && <p className="mt-2 text-sm text-muted">Last updated {updated}</p>}
        {draft && (
          <div className="mt-6">
            <PlaceholderNote>This is a placeholder page. Replace the text in this file with your own.</PlaceholderNote>
          </div>
        )}
        <div className="prose-math mt-8 space-y-4">{children}</div>
      </div>
    </Container>
  );
}
