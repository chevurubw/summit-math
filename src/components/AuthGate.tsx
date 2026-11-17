"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { useApp } from "./AppProvider";

export function LoadingScreen() {
  return (
    <div className="grid min-h-[50vh] place-items-center" role="status">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-line border-t-accent" />
      <span className="sr-only">Loading</span>
    </div>
  );
}

/** Shows its children only to signed in students. */
export function AuthGate({ children }: { children: React.ReactNode }) {
  const { status, user, data } = useApp();
  const router = useRouter();
  const pathname = usePathname();

  const needsLogin = status === "ready" && !user;

  useEffect(() => {
    if (needsLogin) router.replace(`/login?next=${encodeURIComponent(pathname)}`);
  }, [needsLogin, pathname, router]);

  if (status === "loading" || needsLogin || !data) return <LoadingScreen />;
  return <>{children}</>;
}
