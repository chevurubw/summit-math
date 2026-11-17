import { redirect } from "next/navigation";

// The Progress page is now part of the Climb page.
export default function Page() {
  redirect("/climb");
}
