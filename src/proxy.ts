import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";
import { isSupabaseConfigured, supabaseKey, supabaseUrl } from "@/lib/supabase/env";

// Keeps Supabase login sessions fresh. Does nothing in local mode.
export async function proxy(request: NextRequest) {
  if (!isSupabaseConfigured) return NextResponse.next();

  // When Supabase can't match the return address it sends people to the Site URL with ?code=...
  // Forward that to the real sign in handler so the login still completes.
  if (request.nextUrl.pathname === "/" && request.nextUrl.searchParams.has("code")) {
    const host = request.headers.get("x-forwarded-host") ?? request.headers.get("host");
    const proto = request.headers.get("x-forwarded-proto") ?? request.nextUrl.protocol.replace(":", "");
    const target = new URL(`${proto}://${host ?? request.nextUrl.host}/auth/callback`);
    target.searchParams.set("code", request.nextUrl.searchParams.get("code")!);
    target.searchParams.set("next", "/dashboard");
    return NextResponse.redirect(target);
  }

  let response = NextResponse.next({ request });
  const supabase = createServerClient(supabaseUrl, supabaseKey, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet) {
        cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
        response = NextResponse.next({ request });
        cookiesToSet.forEach(({ name, value, options }) => response.cookies.set(name, value, options));
      },
    },
  });
  await supabase.auth.getUser();
  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|problems/|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)"],
};
