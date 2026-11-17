import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { MDXRemote } from "next-mdx-remote/rsc";
import Link from "next/link";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { mdxComponents } from "@/components/lesson";
import { ButtonLink, Container } from "@/components/ui";

export const metadata = { title: "Start here" };

function loadGuide() {
  const file = path.join(process.cwd(), "content", "guides", "start.mdx");
  const { data, content } = matter(fs.readFileSync(file, "utf8"));
  return { title: String(data.title ?? "Start here"), body: content };
}

export default function Page() {
  const guide = loadGuide();
  return (
    <Container className="py-10">
      <article className="mx-auto min-w-0 max-w-[70ch]">
        <nav aria-label="Breadcrumb" className="text-sm text-muted">
          <Link href="/learn" className="hover:text-heading">
            Course
          </Link>
        </nav>
        <h1 className="mt-4 text-4xl font-bold">{guide.title}</h1>
        <div className="prose-math mt-8 text-[1.08rem]">
          <MDXRemote
            source={guide.body}
            components={mdxComponents}
            options={{ blockJS: false, mdxOptions: { remarkPlugins: [remarkMath, remarkGfm], rehypePlugins: [rehypeKatex] } }}
          />
        </div>
        <div className="mt-12 rounded-lg border border-line bg-surface p-6">
          <h2 className="text-2xl font-bold">Ready for your first lesson?</h2>
          <p className="mt-1 text-muted">Algebra is the best place to begin. Every later unit builds on it.</p>
          <div className="mt-5 flex flex-wrap gap-3">
            <ButtonLink href="/learn/algebra/alg_linear">Start with linear equations</ButtonLink>
            <ButtonLink href="/learn" variant="secondary">
              See the whole course
            </ButtonLink>
          </div>
        </div>
      </article>
    </Container>
  );
}
