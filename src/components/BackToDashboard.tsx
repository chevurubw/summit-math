"use client";

import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useApp } from "./AppProvider";

// Pages where a "back" button makes no sense: the destinations themselves and the sign in screens.
const HIDDEN = ["/", "/dashboard", "/login", "/signup"];
const HIDDEN_PREFIXES = ["/reset", "/auth"];

/** A small boxed arrow at the bottom left of the page, just above the footer, that returns to the dashboard (or the home page when signed out). */
export function BackToDashboard() {
  const pathname = usePathname();
  const { user, status } = useApp();
  if (HIDDEN.includes(pathname) || HIDDEN_PREFIXES.some((p) => pathname.startsWith(p))) return null;

  // Hide it until we know whether someone is signed in, so the label never flickers.
  const signedIn = status === "ready" && !!user;
  const href = signedIn || status === "loading" ? "/dashboard" : "/";
  const label = signedIn || status === "loading" ? "Back to dashboard" : "Back to home";

  return (
    <div className="mx-auto w-full max-w-6xl px-4 pt-10 sm:px-6">
      <Link
        href={href}
        className={`group inline-flex items-center gap-2 rounded-lg border border-line bg-surface px-3 py-2 text-sm font-semibold text-body transition-colors hover:border-accent hover:text-heading focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${
          status === "loading" ? "invisible" : ""
        }`}
      >
        <ArrowLeft aria-hidden className="h-4 w-4 transition-transform group-hover:-translate-x-0.5" />
        {label}
      </Link>
    </div>
  );
}
