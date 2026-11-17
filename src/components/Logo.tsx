import Link from "next/link";
import { site } from "@/config/site";

export function LogoMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" aria-hidden>
      <path d="M2 27 L13 8 L19 18 L22 13 L30 27 Z" fill="var(--c-primary)" />
      <path d="M13 8 L16.2 13.5 L13 12 L9.8 13.5 Z" fill="#fff" opacity="0.9" />
      <circle cx="25" cy="6" r="3" fill="var(--c-accent)" />
    </svg>
  );
}

export function Logo() {
  return (
    <Link href="/" className="flex items-center gap-2.5 rounded-md">
      <LogoMark />
      <span className="whitespace-nowrap font-display text-xl font-bold tracking-tight text-heading max-[430px]:sr-only">{site.name}</span>
    </Link>
  );
}
