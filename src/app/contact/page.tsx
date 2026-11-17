import { StaticPage } from "@/components/StaticPage";
import { site } from "@/config/site";

export const metadata = { title: "Contact" };

export default function Page() {
  return (
    <StaticPage title="Contact">
      <p>
        Questions, feedback, or found a mistake in a problem? Email{" "}
        <a href={`mailto:${site.contactEmail}`}>{site.contactEmail}</a>.
      </p>
    </StaticPage>
  );
}
