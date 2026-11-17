import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost" | "accent";
type Size = "sm" | "md" | "lg";

const base =
  "btn-press inline-flex items-center justify-center gap-2 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed select-none";

// Buttons sit on a darker bottom edge and press down when clicked (see .btn-press in globals.css)
const variants: Record<Variant, string> = {
  primary: "bg-primary text-white hover:brightness-110 shadow-[0_3px_0_0_var(--c-primary-edge)]",
  accent: "bg-accent text-white hover:brightness-110 shadow-[0_3px_0_0_var(--c-accent-edge)]",
  secondary: "bg-surface-2 text-heading border border-line hover:border-muted shadow-[0_3px_0_0_#050507]",
  ghost: "text-body hover:text-heading hover:bg-surface-2",
};

const sizes: Record<Size, string> = {
  sm: "h-9 px-3 text-sm",
  md: "h-11 px-5 text-[0.95rem]",
  lg: "h-13 px-7 text-base",
};

export function buttonClass(variant: Variant = "primary", size: Size = "md", extra = "") {
  return `${base} ${variants[variant]} ${sizes[size]} ${extra}`;
}

export function Button({
  variant = "primary",
  size = "md",
  className = "",
  ...props
}: ComponentProps<"button"> & { variant?: Variant; size?: Size }) {
  return <button className={buttonClass(variant, size, className)} {...props} />;
}

export function ButtonLink({
  variant = "primary",
  size = "md",
  className = "",
  ...props
}: ComponentProps<typeof Link> & { variant?: Variant; size?: Size }) {
  return <Link className={buttonClass(variant, size, className)} {...props} />;
}

export function Card({ className = "", children, ...props }: ComponentProps<"div">) {
  return (
    <div className={`rounded-lg border border-line bg-surface ${className}`} {...props}>
      {children}
    </div>
  );
}

export function PageHeader({ title, intro, children }: { title: string; intro?: ReactNode; children?: ReactNode }) {
  return (
    <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div className="max-w-2xl">
        <h1 className="text-3xl sm:text-4xl font-bold">{title}</h1>
        {intro && <p className="mt-2 text-muted">{intro}</p>}
      </div>
      {children}
    </div>
  );
}

export function Container({ className = "", children }: { className?: string; children: ReactNode }) {
  return <div className={`mx-auto w-full max-w-6xl px-4 sm:px-6 ${className}`}>{children}</div>;
}

export function PlaceholderNote({ children }: { children: ReactNode }) {
  return (
    <p className="rounded-md border border-dashed border-accent/50 bg-accent/10 px-4 py-3 text-sm text-accent-soft">
      {children}
    </p>
  );
}
