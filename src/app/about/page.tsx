import Image from "next/image";
import Link from "next/link";
import { StaticPage } from "@/components/StaticPage";
import { site } from "@/config/site";

export const metadata = { title: "About" };

export default function Page() {
  return (
    <StaticPage title="About">
      <div className="flex flex-col items-start gap-6 sm:flex-row sm:items-center">
        <Image
          src="/about/rohan.png"
          alt="Rohan Chevuru"
          width={160}
          height={160}
          priority
          className="!m-0 h-36 w-36 shrink-0 !rounded-full !border-0 shadow-lg ring-2 ring-accent/50 sm:h-40 sm:w-40"
        />
        <p className="!m-0 text-lg">
          Hi, I&apos;m Rohan Chevuru. I&apos;m 17 years old, a junior in high school, and the person who built Summit Math.
        </p>
      </div>

      <h2>Why math</h2>
      <p>
        For as long as I can remember, I&apos;ve been curious about math. Not just getting the right answer, but
        understanding why it&apos;s right. I love the moment when a problem that looked impossible suddenly clicks, and a
        clever idea turns a page of work into two lines.
      </p>
      <p>
        That curiosity led me to competition math. I&apos;ve qualified for the AIME, the invitational exam that follows
        the AMC 10 and AMC 12, and the problems I worked through along the way taught me more about thinking clearly than
        anything else I&apos;ve studied.
      </p>

      <h2>Why I built this</h2>
      <p>
        When I started preparing for the AMC, good resources were out there, but they weren&apos;t always easy to find or
        easy to start with if you didn&apos;t already know what you were doing. I wanted to build the site I wish I&apos;d
        had: one that starts from zero, explains every idea in plain language, and lets you play with the math instead of
        just reading about it.
      </p>
      <p>
        I&apos;ve always loved teaching. Helping a friend finally get a concept they were stuck on is one of my favorite
        feelings, and {site.name} is my way of doing that for a lot more people at once. It&apos;s free because I think
        anyone curious enough to try should be able to.
      </p>

      <h2>Get in touch</h2>
      <p>
        If you have feedback, find a mistake, or just want to say hi, I&apos;d love to hear from you on the{" "}
        <Link href="/contact">contact page</Link>. And if you&apos;re just getting started, the{" "}
        <Link href="/learn/start">Start here</Link> guide is the best first step.
      </p>
      <p>Happy problem solving!</p>
      <p>Rohan</p>
    </StaticPage>
  );
}
