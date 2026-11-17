"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useApp } from "./AppProvider";
import { LogoMark } from "./Logo";
import { Button } from "./ui";

function safeNext(v: string | null, fallback = "/dashboard") {
  return v && v.startsWith("/") && !v.startsWith("//") ? v : fallback;
}

function Shell({ title, intro, children }: { title: string; intro?: string; children: React.ReactNode }) {
  const { mode } = useApp();
  return (
    <div className="mx-auto w-full max-w-md px-4 py-16">
      <LogoMark size={40} />
      <h1 className="mt-6 text-3xl font-bold">{title}</h1>
      {intro && <p className="mt-2 text-muted">{intro}</p>}
      {mode === "local" && (
        <p className="mt-6 rounded-md border border-dashed border-accent/50 bg-accent/10 px-4 py-3 text-sm text-accent-soft">
          Local mode: Supabase is not connected yet, so accounts are saved only in this browser and passwords are not
          checked. See the README to connect Supabase.
        </p>
      )}
      <div className="mt-8">{children}</div>
    </div>
  );
}

export function Field({
  label,
  ...props
}: React.ComponentProps<"input"> & { label: string }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-semibold text-heading">{label}</span>
      <input
        className="h-11 w-full rounded-md border border-line bg-surface-2 px-3 text-heading placeholder:text-muted/70 focus:border-accent focus:outline-none"
        {...props}
      />
    </label>
  );
}

function Message({ error, message }: { error?: string; message?: string }) {
  if (error)
    return (
      <p role="alert" className="rounded-lg border border-wrong/40 bg-wrong/10 px-3 py-2 text-sm text-wrong">
        {error}
      </p>
    );
  if (message)
    return (
      <p role="status" className="rounded-lg border border-correct/40 bg-correct/10 px-3 py-2 text-sm text-correct">
        {message}
      </p>
    );
  return null;
}

function GoogleButton({ next }: { next: string }) {
  const { mode, signInWithGoogle } = useApp();
  const [error, setError] = useState<string>();
  if (mode === "local")
    return (
      <p className="rounded-md border border-line bg-surface px-4 py-3 text-sm text-muted">
        Continue with Google appears here once Supabase is connected.
      </p>
    );
  return (
    <div className="space-y-2">
      <button
        type="button"
        onClick={async () => setError((await signInWithGoogle(next)).error)}
        className="btn-press flex h-12 w-full items-center justify-center gap-3 rounded-lg bg-white font-semibold text-black shadow-[0_3px_0_0_#71717a] hover:bg-white/90"
      >
        <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden>
          <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z" />
          <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z" />
          <path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z" />
          <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C36.9 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z" />
        </svg>
        Continue with Google
      </button>
      <Message error={error} />
    </div>
  );
}

function Divider() {
  return (
    <div className="my-6 flex items-center gap-3 text-sm text-muted">
      <span className="h-px flex-1 bg-line" />
      or use email
      <span className="h-px flex-1 bg-line" />
    </div>
  );
}

/** Sends signed in visitors on to where they were going. */
function useRedirectWhenSignedIn(next: string) {
  const { user, status } = useApp();
  const router = useRouter();
  useEffect(() => {
    if (status === "ready" && user) router.replace(next);
  }, [status, user, next, router]);
}

export function LoginForm() {
  const params = useSearchParams();
  const next = safeNext(params.get("next"));
  const { signInWithEmail } = useApp();
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{ error?: string; message?: string }>({ error: params.get("error") ?? undefined });
  useRedirectWhenSignedIn(next);

  return (
    <Shell title="Welcome back" intro="Log in to pick up where you left off.">
      <GoogleButton next={next} />
      <Divider />
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          const f = new FormData(e.currentTarget);
          setBusy(true);
          setResult(await signInWithEmail(String(f.get("email")), String(f.get("password"))));
          setBusy(false);
        }}
      >
        <Field label="Email" name="email" type="email" autoComplete="email" required />
        <Field label="Password" name="password" type="password" autoComplete="current-password" required />
        <Message {...result} />
        <Button type="submit" className="w-full" disabled={busy}>
          {busy ? "Logging in" : "Log in"}
        </Button>
      </form>
      <div className="mt-6 flex justify-between text-sm">
        <Link href="/reset" className="text-accent-soft hover:underline">
          Forgot your password?
        </Link>
        <Link href={`/signup?next=${encodeURIComponent(next)}`} className="text-accent-soft hover:underline">
          Create an account
        </Link>
      </div>
    </Shell>
  );
}

export function SignupForm() {
  const params = useSearchParams();
  const next = safeNext(params.get("next"), "/dashboard");
  const { signUpWithEmail } = useApp();
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{ error?: string; message?: string }>({});
  useRedirectWhenSignedIn(next);

  return (
    <Shell title="Create your account" intro="Free to start. Your progress is saved to your account.">
      <GoogleButton next={next} />
      <Divider />
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          const f = new FormData(e.currentTarget);
          setBusy(true);
          setResult(await signUpWithEmail(String(f.get("name")), String(f.get("email")), String(f.get("password"))));
          setBusy(false);
        }}
      >
        <Field label="Name" name="name" autoComplete="name" required />
        <Field label="Email" name="email" type="email" autoComplete="email" required />
        <Field label="Password" name="password" type="password" autoComplete="new-password" minLength={8} required />
        <Message {...result} />
        <Button type="submit" className="w-full" disabled={busy}>
          {busy ? "Creating account" : "Create account"}
        </Button>
      </form>
      <p className="mt-6 text-sm text-muted">
        Already have an account?{" "}
        <Link href="/login" className="text-accent-soft hover:underline">
          Log in
        </Link>
      </p>
    </Shell>
  );
}

export function ResetRequestForm() {
  const { requestPasswordReset } = useApp();
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{ error?: string; message?: string }>({});
  return (
    <Shell title="Reset your password" intro="Enter your email and we will send you a link to set a new password.">
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          setBusy(true);
          setResult(await requestPasswordReset(String(new FormData(e.currentTarget).get("email"))));
          setBusy(false);
        }}
      >
        <Field label="Email" name="email" type="email" autoComplete="email" required />
        <Message {...result} />
        <Button type="submit" className="w-full" disabled={busy}>
          Send reset link
        </Button>
      </form>
      <p className="mt-6 text-sm">
        <Link href="/login" className="text-accent-soft hover:underline">
          Back to log in
        </Link>
      </p>
    </Shell>
  );
}

export function ResetUpdateForm() {
  const { updatePassword } = useApp();
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{ error?: string; message?: string }>({});
  return (
    <Shell title="Set a new password">
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          const f = new FormData(e.currentTarget);
          if (f.get("password") !== f.get("confirm")) return setResult({ error: "The two passwords do not match." });
          setBusy(true);
          setResult(await updatePassword(String(f.get("password"))));
          setBusy(false);
        }}
      >
        <Field label="New password" name="password" type="password" autoComplete="new-password" minLength={8} required />
        <Field label="Confirm new password" name="confirm" type="password" autoComplete="new-password" minLength={8} required />
        <Message {...result} />
        <Button type="submit" className="w-full" disabled={busy}>
          Save new password
        </Button>
      </form>
      {result.message && (
        <p className="mt-6 text-sm">
          <Link href="/dashboard" className="text-accent-soft hover:underline">
            Go to your dashboard
          </Link>
        </p>
      )}
    </Shell>
  );
}
