import { AlertTriangle, BookOpen, Info, Lightbulb, ListChecks, PlayCircle, Sigma, Target } from "lucide-react";
import { BasePlaces, Check, DiceGrid, Figure, FlipCards, ModClock, PathGrid, PowerCycle, SequenceBars, Step, Steps, Telescope, Venn } from "./lesson-widgets";
import type { ReactNode } from "react";

/** Turns a YouTube or Vimeo link into an embeddable player address. */
function embedUrl(url: string): string | null {
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtube.com")) {
      const id = u.searchParams.get("v") ?? u.pathname.split("/embed/")[1];
      return id && id !== "PLACEHOLDER" ? `https://www.youtube-nocookie.com/embed/${id}` : null;
    }
    if (u.hostname === "youtu.be") return `https://www.youtube-nocookie.com/embed${u.pathname}`;
    if (u.hostname.includes("vimeo.com")) {
      const id = u.pathname.split("/").filter(Boolean).pop();
      return id ? `https://player.vimeo.com/video/${id}` : null;
    }
  } catch {
    return null;
  }
  return null;
}

export function VideoEmbed({ url, title }: { url: string; title: string }) {
  const src = embedUrl(url);
  if (!src)
    return (
      <div className="grid aspect-video w-full place-items-center rounded-lg border border-dashed border-line bg-surface text-center">
        <div className="px-6">
          <PlayCircle className="mx-auto h-12 w-12 text-muted" aria-hidden />
          <p className="mt-3 font-semibold text-heading">Video placeholder</p>
          <p className="mt-1 text-sm text-muted">Set videoUrl in this lesson&apos;s frontmatter to a YouTube or Vimeo link.</p>
        </div>
      </div>
    );
  return (
    <div className="aspect-video w-full overflow-hidden rounded-lg border border-line bg-black">
      <iframe
        src={src}
        title={title}
        className="h-full w-full"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
    </div>
  );
}

// Components you can use inside lesson MDX files

export function Callout({ title, children }: { title?: string; children: ReactNode }) {
  return (
    <div className="my-6 flex gap-3 rounded-md border border-accent/40 bg-accent/10 px-5 py-4">
      <Info className="mt-1 h-5 w-5 shrink-0 text-accent-soft" aria-hidden />
      <div>
        {title && <p className="font-display font-bold text-heading">{title}</p>}
        <div className="prose-math">{children}</div>
      </div>
    </div>
  );
}

export function Example({ title = "Example", children }: { title?: string; children: ReactNode }) {
  return (
    <div className="my-6 rounded-md border border-line bg-surface-2 px-5 py-4">
      <p className="mb-2 font-display font-bold text-heading">{title}</p>
      <div className="prose-math">{children}</div>
    </div>
  );
}

type Tone = { icon: typeof Info; ring: string; bg: string; text: string; label: string };
const TONES: Record<string, Tone> = {
  idea: { icon: Lightbulb, ring: "border-accent/50", bg: "bg-accent/10", text: "text-accent-soft", label: "Key idea" },
  trap: { icon: AlertTriangle, ring: "border-wrong/50", bg: "bg-wrong/10", text: "text-wrong", label: "Watch out" },
  tip: { icon: Target, ring: "border-amber-400/50", bg: "bg-amber-400/10", text: "text-amber-300", label: "Test day tip" },
  formula: { icon: Sigma, ring: "border-teal-400/50", bg: "bg-teal-400/10", text: "text-teal-300", label: "Formula" },
  recap: { icon: ListChecks, ring: "border-line", bg: "bg-surface", text: "text-heading", label: "Cheat sheet" },
  further: { icon: BookOpen, ring: "border-line", bg: "bg-surface", text: "text-muted", label: "Go further" },
};

function Box({ tone, title, children }: { tone: keyof typeof TONES; title?: string; children: ReactNode }) {
  const t = TONES[tone];
  const Icon = t.icon;
  return (
    <aside className={`not-prose my-7 rounded-lg border ${t.ring} ${t.bg} px-5 py-4`}>
      <p className={`flex items-center gap-2 font-display font-bold ${t.text}`}>
        <Icon className="h-5 w-5 shrink-0" aria-hidden />
        {title ?? t.label}
      </p>
      <div className="prose-math mt-2 text-body">{children}</div>
    </aside>
  );
}

export const KeyIdea = (p: { title?: string; children: ReactNode }) => <Box tone="idea" {...p} />;
export const Trap = (p: { title?: string; children: ReactNode }) => <Box tone="trap" {...p} />;
export const Tip = (p: { title?: string; children: ReactNode }) => <Box tone="tip" {...p} />;
export const Formula = (p: { title?: string; children: ReactNode }) => <Box tone="formula" {...p} />;
export const Recap = (p: { title?: string; children: ReactNode }) => <Box tone="recap" {...p} />;
export const GoFurther = (p: { title?: string; children: ReactNode }) => <Box tone="further" {...p} />;

/** A link to an AoPS Wiki article, found by title through the wiki's search. */
export function AoPS({ q, children }: { q: string; children?: ReactNode }) {
  const href = `https://artofproblemsolving.com/wiki/index.php?search=${encodeURIComponent(q)}`;
  return (
    <a href={href} target="_blank" rel="noreferrer">
      {children ?? `${q} (AoPS Wiki)`}
    </a>
  );
}

/** Past contests with full solutions, collected on the AoPS Wiki. */
export function Archive({ test = "10" }: { test?: "10" | "12" }) {
  return (
    <a href={`https://artofproblemsolving.com/wiki/index.php/AMC_${test}_Problems_and_Solutions`} target="_blank" rel="noreferrer">
      every past AMC {test} with solutions (AoPS Wiki)
    </a>
  );
}

export function MAA({ children }: { children?: ReactNode }) {
  return (
    <a href="https://www.maa.org/AMC" target="_blank" rel="noreferrer">
      {children ?? "the official MAA AMC page"}
    </a>
  );
}

/** A question you think about first, then open to see the answer. */
export function Reveal({ label = "Show the answer", children }: { label?: string; children: ReactNode }) {
  return (
    <details className="group not-prose my-5 rounded-lg border border-line bg-surface px-5 py-3">
      <summary className="cursor-pointer select-none font-semibold text-accent-soft marker:text-accent-soft">{label}</summary>
      <div className="prose-math mt-3 text-body">{children}</div>
    </details>
  );
}

export const mdxComponents = {
  Callout,
  Example,
  KeyIdea,
  Trap,
  Tip,
  Formula,
  Recap,
  GoFurther,
  Reveal,
  Check,
  Steps,
  Step,
  Figure,
  DiceGrid,
  Venn,
  PathGrid,
  ModClock,
  SequenceBars,
  Telescope,
  FlipCards,
  PowerCycle,
  BasePlaces,
  AoPS,
  Archive,
  MAA,
};
