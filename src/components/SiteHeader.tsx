"use client";

import { Flame, LogOut, Menu, Settings, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { useApp } from "./AppProvider";
import { Avatar } from "./Avatar";
import { ClimbWidget } from "./climb";
import { Logo } from "./Logo";
import { buttonClass } from "./ui";

const signedInNav = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/learn", label: "Course" },
  { href: "/mock", label: "Mock Exams" },
  { href: "/climb", label: "Climb" },
];

const publicNav = [
  { href: "/learn", label: "Course" },
  { href: "/about", label: "About" },
];

export function SiteHeader() {
  const { user, data, status, signOut } = useApp();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [menu, setMenu] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const nav = user ? signedInNav : publicNav;

  useEffect(() => {
    const close = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setMenu(false);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  const isActive = (href: string) => pathname === href || pathname.startsWith(href + "/");

  return (
    <header className="sticky top-0 z-40 border-b border-line bg-bg/90 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center gap-6 px-4 sm:px-6">
        <Logo />
        <nav aria-label="Main" className="hidden flex-1 items-center gap-1 md:flex">
          {nav.map((n) => (
            <Link
              key={n.href}
              href={n.href}
              className={`rounded-lg px-3 py-2 text-[0.95rem] font-semibold transition-colors ${
                isActive(n.href) ? "text-heading bg-surface-2" : "text-muted hover:text-heading"
              }`}
              aria-current={isActive(n.href) ? "page" : undefined}
            >
              {n.label}
              {isActive(n.href) && <span className="mt-0.5 block h-0.5 rounded-full bg-primary" />}
            </Link>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-2">
          {status === "ready" && !user && (
            <div className="hidden items-center gap-2 sm:flex">
              <Link href="/login" className={buttonClass("ghost", "sm")}>
                Log in
              </Link>
              <Link href="/signup" className={buttonClass("primary", "sm")}>
                Start learning
              </Link>
            </div>
          )}
          {user && data && (
            <>
              <ClimbWidget />
              <span
                className="hidden items-center gap-1.5 px-1 text-sm font-semibold text-heading lg:inline-flex"
                title="Daily streak"
              >
                <Flame className="h-4 w-4 text-accent-soft" aria-hidden />
                {data.profile.streak}
                <span className="sr-only">day streak</span>
              </span>
              <div className="relative" ref={menuRef}>
                <button
                  type="button"
                  onClick={() => setMenu((m) => !m)}
                  aria-expanded={menu}
                  aria-haspopup="menu"
                  className="rounded-full"
                >
                  <Avatar id={data.profile.avatar} name={data.profile.displayName || user.name} />
                  <span className="sr-only">Account menu</span>
                </button>
                {menu && (
                  <div role="menu" className="absolute right-0 mt-2 w-56 overflow-hidden rounded-md border border-line bg-surface shadow-xl">
                    <div className="border-b border-line px-4 py-3">
                      <p className="truncate font-semibold text-heading">{data.profile.displayName || user.name}</p>
                      <p className="truncate text-sm text-muted">{user.email}</p>
                    </div>
                    <Link role="menuitem" href="/settings" onClick={() => setMenu(false)} className="flex items-center gap-2 px-4 py-2.5 text-sm hover:bg-surface-2">
                      <Settings className="h-4 w-4" aria-hidden /> Settings
                    </Link>
                    <button
                      role="menuitem"
                      type="button"
                      onClick={async () => {
                        setMenu(false);
                        await signOut();
                        window.location.href = "/";
                      }}
                      className="flex w-full items-center gap-2 px-4 py-2.5 text-left text-sm hover:bg-surface-2"
                    >
                      <LogOut className="h-4 w-4" aria-hidden /> Log out
                    </button>
                  </div>
                )}
              </div>
            </>
          )}
          <button
            type="button"
            className="grid h-10 w-10 place-items-center rounded-lg text-heading hover:bg-surface-2 md:hidden"
            onClick={() => setOpen((o) => !o)}
            aria-expanded={open}
            aria-controls="mobile-nav"
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            <span className="sr-only">{open ? "Close menu" : "Open menu"}</span>
          </button>
        </div>
      </div>

      {open && (
        <nav id="mobile-nav" aria-label="Mobile" className="border-t border-line bg-bg px-4 pb-4 md:hidden">
          {nav.map((n) => (
            <Link
              key={n.href}
              href={n.href}
              onClick={() => setOpen(false)}
              className={`block rounded-lg px-3 py-3 font-semibold ${isActive(n.href) ? "bg-surface-2 text-heading" : "text-body"}`}
            >
              {n.label}
            </Link>
          ))}
          {!user && status === "ready" && (
            <div className="mt-3 grid grid-cols-2 gap-2">
              <Link href="/login" onClick={() => setOpen(false)} className={buttonClass("secondary", "md")}>
                Log in
              </Link>
              <Link href="/signup" onClick={() => setOpen(false)} className={buttonClass("primary", "md")}>
                Start learning
              </Link>
            </div>
          )}
        </nav>
      )}
    </header>
  );
}
