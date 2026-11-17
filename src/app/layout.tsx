import type { Metadata } from "next";
import "@fontsource-variable/bricolage-grotesque";
import "@fontsource-variable/instrument-sans";
import "katex/dist/katex.min.css";
import "./globals.css";
import { AppProvider } from "@/components/AppProvider";
import { BackToDashboard } from "@/components/BackToDashboard";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { site } from "@/config/site";
import { CelebrationToast } from "@/components/CelebrationToast";
import { WindBackground } from "@/components/WindBackground";
import { getCourseIndex } from "@/lib/content/load";

export const metadata: Metadata = {
  title: { default: `${site.name}: ${site.tagline}`, template: `%s | ${site.name}` },
  description: site.description,
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased" data-theme="summit" suppressHydrationWarning>
      <body className="flex min-h-full flex-col">
        <WindBackground />
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-primary focus:px-4 focus:py-2 focus:text-white"
        >
          Skip to content
        </a>
        <AppProvider index={getCourseIndex()}>
          <SiteHeader />
          <main id="main" className="flex-1">
            {children}
            <BackToDashboard />
          </main>
          <SiteFooter />
          <CelebrationToast />
        </AppProvider>
      </body>
    </html>
  );
}
