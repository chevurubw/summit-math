"use client";

import ReactMarkdown from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

/** Renders Markdown with LaTeX math. Used for problems, choices, hints and solutions. */
export function Markdown({ children, inline = false, className = "" }: { children: string; inline?: boolean; className?: string }) {
  const md = (
    <ReactMarkdown
      remarkPlugins={[remarkMath, remarkGfm]}
      rehypePlugins={[rehypeKatex]}
      components={inline ? { p: ({ children }) => <>{children}</> } : undefined}
    >
      {children}
    </ReactMarkdown>
  );
  return inline ? <span className={className}>{md}</span> : <div className={`prose-math ${className}`}>{md}</div>;
}
