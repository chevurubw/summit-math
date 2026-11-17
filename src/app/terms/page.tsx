import { StaticPage } from "@/components/StaticPage";
import { site } from "@/config/site";

export const metadata = { title: "Terms" };

export default function Page() {
  const email = <a href={`mailto:${site.contactEmail}`}>{site.contactEmail}</a>;
  return (
    <StaticPage title="Terms of use" updated="November 15, 2026">
      <p>
        These terms apply when you use {site.name}. By making an account or using the site, you agree to them. If you
        are under 18, please read them with a parent or guardian.
      </p>

      <h2>What the site is</h2>
      <p>
        {site.name} is a free study tool for the AMC 10 and AMC 12. It is not affiliated with or endorsed by the
        Mathematical Association of America (MAA). AMC 10, AMC 12, and AIME are trademarks of the MAA. Our practice
        problems and mock exams are original problems written in the style of the contests. They are not official
        contest problems, and mock exam scores are estimates, not predictions of a real score.
      </p>

      <h2>Your account</h2>
      <ul>
        <li>You must be at least 13, or have permission from a parent or guardian, to make an account.</li>
        <li>Give accurate information and keep your sign in details private. You are responsible for activity on your account.</li>
        <li>You can stop using the site at any time, and you can ask us to delete your account by emailing {email}.</li>
      </ul>

      <h2>Fair use of the site</h2>
      <p>Please do not:</p>
      <ul>
        <li>try to break, overload, or get around the security of the site;</li>
        <li>copy the problem banks in bulk, scrape the site, or republish our content as your own;</li>
        <li>use the site to harass anyone or to do anything illegal.</li>
      </ul>
      <p>We may suspend or remove accounts that break these rules.</p>

      <h2>Our content</h2>
      <p>
        The lessons, problems, solutions, and design of {site.name} belong to us. You may use them for your own studying,
        and teachers may use them with their own students. Please ask before using them in any other way.
      </p>

      <h2>No guarantees</h2>
      <p>
        We work hard to keep problems and solutions correct, but mistakes can happen. If you find one, please tell us at{" "}
        {email}. The site is provided as is, without any warranty, and we cannot promise it will always be available or
        error free. We are not responsible for contest results or for any loss that comes from using the site, to the
        extent the law allows.
      </p>

      <h2>Changes</h2>
      <p>
        We may update these terms as the site grows. When we do, we will change the date at the top of this page.
        Continuing to use the site after a change means you accept the new terms.
      </p>

      <h2>Contact</h2>
      <p>Questions about these terms? Email {email}.</p>
    </StaticPage>
  );
}
