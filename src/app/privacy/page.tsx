import { StaticPage } from "@/components/StaticPage";
import { site } from "@/config/site";

export const metadata = { title: "Privacy" };

export default function Page() {
  const email = <a href={`mailto:${site.contactEmail}`}>{site.contactEmail}</a>;
  return (
    <StaticPage title="Privacy policy" updated="November 15, 2026">
      <p>
        {site.name} is a free practice site for the AMC 10 and AMC 12. This page explains what information we keep, why we
        keep it, and how you can have it removed. We collect as little as we can.
      </p>

      <h2>What we collect</h2>
      <ul>
        <li>
          <strong>Account details.</strong> Your email address and the name you give us. If you sign in with Google, we
          receive your name and email from Google. We never see your Google password.
        </li>
        <li>
          <strong>Your progress.</strong> The problems you answer, whether each answer was right, how long it took, your
          skill levels, mock exam scores, your altitude on the climb, and the settings you choose, such as your theme.
        </li>
      </ul>
      <p>
        We do not use advertising, tracking pixels, or analytics services. We do not ask for your age, address, school, or
        phone number.
      </p>

      <h2>Why we collect it</h2>
      <p>
        Only to run the site: to sign you in, save your progress, and show you your results. We do not sell your
        information, rent it, or share it with advertisers.
      </p>

      <h2>Where it is stored</h2>
      <p>
        Your account and progress are stored with Supabase, the database service that powers the site, and the site
        itself is hosted with a web hosting provider. These companies process the data for us only so the site can work.
        Your browser also keeps a small amount of data on your device so you stay signed in. We do not use cookies for
        tracking.
      </p>

      <h2>Students under 13</h2>
      <p>
        {site.name} is meant for students 13 and older. If you are under 13, please ask a parent or guardian before making
        an account. If a parent or guardian believes their child under 13 made an account without permission, email{" "}
        {email} and we will delete it.
      </p>

      <h2>Your choices</h2>
      <ul>
        <li>You can reset all of your progress at any time from Settings.</li>
        <li>
          To delete your whole account and everything linked to it, email {email} from the address on the account. We
          will delete it within 30 days.
        </li>
        <li>You can also email us to ask for a copy of the information we hold about you.</li>
      </ul>

      <h2>How long we keep it</h2>
      <p>We keep your information while your account exists. When an account is deleted, its progress is deleted with it.</p>

      <h2>Changes</h2>
      <p>
        If this policy changes, we will update this page and the date at the top. If a change is significant, we will
        tell signed in users on the site.
      </p>

      <h2>Contact</h2>
      <p>Questions about privacy? Email {email}.</p>
    </StaticPage>
  );
}
