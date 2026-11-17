import Link from "next/link";
import { site } from "@/config/site";
import { LogoMark } from "./Logo";

const links = [
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
  { href: "/privacy", label: "Privacy" },
  { href: "/terms", label: "Terms" },
];

export function SiteFooter() {
  return (
    <footer className="mt-20 border-t border-line">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10 sm:flex-row sm:items-start sm:justify-between sm:px-6">
        <div className="max-w-sm">
          <div className="flex items-center gap-2">
            <LogoMark size={22} />
            <span className="font-display font-bold text-heading">{site.name}</span>
          </div>
          <p className="mt-3 text-sm text-muted">
            Not affiliated with or endorsed by the Mathematical Association of America. AMC 10, AMC 12 and AIME are
            trademarks of the MAA.
          </p>
        </div>
        <nav aria-label="Footer" className="flex flex-wrap gap-x-6 gap-y-2">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className="text-sm text-muted hover:text-heading">
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </footer>
  );
}
