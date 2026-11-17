"use client";

import { Backpack, Compass, Flag, MountainSnow, Pickaxe, Snowflake, Tent } from "lucide-react";
import type { AvatarId } from "@/config/climb";

const icons = {
  tent: Tent,
  backpack: Backpack,
  compass: Compass,
  pickaxe: Pickaxe,
  snowflake: Snowflake,
  peak: MountainSnow,
  flag: Flag,
} as const;

/** The student's profile icon: their initial, or a climbing icon they unlocked. */
export function Avatar({ id, name, size = 36 }: { id: AvatarId; name: string; size?: number }) {
  const Icon = id === "initial" ? null : icons[id];
  return (
    <span
      className="grid shrink-0 place-items-center rounded-full bg-accent font-display font-bold text-white"
      style={{ width: size, height: size, fontSize: size * 0.42 }}
      aria-hidden
    >
      {Icon ? <Icon style={{ width: size * 0.52, height: size * 0.52 }} strokeWidth={2.2} /> : (name || "?").charAt(0).toUpperCase()}
    </span>
  );
}
