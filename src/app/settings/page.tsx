"use client";

import Link from "next/link";
import { useState } from "react";
import { Field } from "@/components/AuthForms";
import { useApp } from "@/components/AppProvider";
import { AuthGate } from "@/components/AuthGate";
import { Avatar } from "@/components/Avatar";
import { avatars, themes } from "@/config/climb";
import { campAt, formatMeters } from "@/lib/climb";
import { Check, Lock } from "lucide-react";
import { Button, Card, Container, PageHeader } from "@/components/ui";

function Settings() {
  const { data, user, mode, updateProfile, resetProgress, signOut } = useApp();
  const [name, setName] = useState(data?.profile.displayName ?? "");
  const [saved, setSaved] = useState<string | null>(null);
  const [confirmReset, setConfirmReset] = useState(false);
  if (!data || !user) return null;
  const best = data.profile.bestAltitude ?? 0;

  const flash = (msg: string) => {
    setSaved(msg);
    setTimeout(() => setSaved(null), 2500);
  };

  return (
    <>
      <PageHeader title="Settings" />
      <p role="status" aria-live="polite" className="sr-only">
        {saved}
      </p>
      {saved && (
        <div className="pointer-events-none fixed inset-x-0 bottom-6 z-50 flex justify-center">
          <div className="anim-rise rounded-md border border-correct/40 bg-surface px-4 py-2.5 text-sm font-semibold text-correct shadow-xl">{saved}</div>
        </div>
      )}

      <div className="max-w-3xl space-y-6">
        <Card className="p-6">
          <h2 className="text-xl font-bold">Color scheme</h2>
          <p className="mt-1 text-sm text-muted">Unlock new color schemes by climbing higher. You have reached {formatMeters(best)}.</p>
          <div role="radiogroup" aria-label="Color scheme" className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-3">
            {themes.map((t) => {
              const locked = best < t.unlockAt;
              const on = data.profile.theme === t.id;
              return (
                <button
                  key={t.id}
                  type="button"
                  role="radio"
                  aria-checked={on}
                  disabled={locked}
                  onClick={async () => {
                    await updateProfile({ theme: t.id });
                    flash(`${t.name} applied`);
                  }}
                  className={`btn-press relative flex flex-col items-start gap-3 rounded-md border-2 p-4 text-left disabled:cursor-not-allowed ${
                    on ? "border-heading bg-surface-2" : "border-line bg-surface-2 hover:border-muted"
                  } ${locked ? "opacity-60" : ""}`}
                >
                  <span className="flex" aria-hidden>
                    <span className="h-8 w-8 rounded-full border-2 border-surface-2" style={{ background: t.swatch[0] }} />
                    <span className="-ml-3 h-8 w-8 rounded-full border-2 border-surface-2" style={{ background: t.swatch[1] }} />
                  </span>
                  <span>
                    <span className="block font-semibold text-heading">{t.name}</span>
                    <span className="flex items-center gap-1 text-xs text-muted">
                      {locked ? (
                        <>
                          <Lock className="h-3 w-3" aria-hidden /> {campAt(t.unlockAt).name}, {formatMeters(t.unlockAt)}
                        </>
                      ) : on ? (
                        "In use"
                      ) : (
                        "Unlocked"
                      )}
                    </span>
                  </span>
                  {on && <Check className="absolute right-3 top-3 h-4 w-4 text-heading" aria-hidden />}
                </button>
              );
            })}
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="text-xl font-bold">Profile icon</h2>
          <p className="mt-1 text-sm text-muted">Climbing gear you have earned on the way up.</p>
          <div role="radiogroup" aria-label="Profile icon" className="mt-5 grid grid-cols-4 gap-3 sm:grid-cols-8">
            {avatars.map((a) => {
              const locked = best < a.unlockAt;
              const on = data.profile.avatar === a.id;
              return (
                <button
                  key={a.id}
                  type="button"
                  role="radio"
                  aria-checked={on}
                  disabled={locked}
                  title={locked ? `Unlocks at ${campAt(a.unlockAt).name} (${formatMeters(a.unlockAt)})` : a.name}
                  onClick={async () => {
                    await updateProfile({ avatar: a.id });
                    flash("Profile icon saved");
                  }}
                  className={`relative flex flex-col items-center gap-2 rounded-md border-2 p-3 disabled:cursor-not-allowed ${
                    on ? "border-heading bg-surface-2" : "border-transparent hover:border-line"
                  }`}
                >
                  <span className={locked ? "opacity-30 grayscale" : ""}>
                    <Avatar id={a.id} name={data.profile.displayName || user.name} size={44} />
                  </span>
                  {locked && <Lock className="absolute right-2 top-2 h-3.5 w-3.5 text-muted" aria-hidden />}
                  <span className="text-center text-xs text-muted">{locked ? formatMeters(a.unlockAt) : a.name}</span>
                  <span className="sr-only">{locked ? `${a.name}, locked until ${formatMeters(a.unlockAt)}` : a.name}</span>
                </button>
              );
            })}
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="text-xl font-bold">Account</h2>
          <form
            className="mt-5 space-y-4"
            onSubmit={async (e) => {
              e.preventDefault();
              await updateProfile({ displayName: name.trim() });
              flash("Name saved");
            }}
          >
            <Field label="Display name" value={name} onChange={(e) => setName(e.target.value)} required />
            <Field label="Email" value={user.email} readOnly disabled />
            <div className="flex flex-wrap gap-3">
              <Button type="submit">Save name</Button>
              {mode === "supabase" && (
                <Link href="/reset/update" className="inline-flex h-11 items-center rounded-md px-4 font-semibold text-accent-soft hover:bg-surface-2">
                  Change password
                </Link>
              )}
            </div>
          </form>
          <div className="mt-6 border-t border-line pt-5">
            <Button
              variant="secondary"
              onClick={async () => {
                await signOut();
                window.location.href = "/";
              }}
            >
              Log out
            </Button>
          </div>
        </Card>

        <Card className="border-primary/40 p-6">
          <h2 className="text-xl font-bold">Reset progress</h2>
          <p className="mt-1 text-sm text-muted">
            Clears every mastery level, answer history, mock exam score, your streak, and your climb back to the trailhead (unlocked colors and icons lock again). Your account stays. This cannot be undone.
          </p>
          <Button variant="secondary" className="mt-5 !border-primary/60" onClick={() => setConfirmReset(true)}>
            Reset all progress
          </Button>
        </Card>
      </div>

      {confirmReset && (
        <div className="fixed inset-0 z-50 grid place-items-center bg-black/70 px-4" role="dialog" aria-modal="true" aria-labelledby="reset-title">
          <div className="anim-level-up w-full max-w-md rounded-lg border border-line bg-surface p-6">
            <h2 id="reset-title" className="text-2xl font-bold">
              Reset all progress?
            </h2>
            <p className="mt-2 text-body">Every skill goes back to Not Started and your mock exam history is deleted. This cannot be undone.</p>
            <div className="mt-6 flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setConfirmReset(false)} autoFocus>
                Cancel
              </Button>
              <Button
                onClick={async () => {
                  await resetProgress();
                  setConfirmReset(false);
                  flash("Progress reset");
                }}
              >
                Reset progress
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default function Page() {
  return (
    <Container className="py-12">
      <AuthGate>
        <Settings />
      </AuthGate>
    </Container>
  );
}
