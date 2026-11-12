import type { Metadata } from "next";
import { Bricolage_Grotesque, Figtree, JetBrains_Mono } from "next/font/google";
import Link from "next/link";
import Script from "next/script";
import HydrationMarker from "@/components/HydrationMarker";
import { DrillMark } from "@/components/icons";
import NavLinks from "@/components/NavLinks";
import ThemeToggle, { themeInitScript } from "@/components/ThemeToggle";
import "./globals.css";

// Figtree: a warm geometric sans with a large x-height, readable at small UI sizes and bold at display sizes.
// JetBrains Mono: tall, distinct glyphs (0/O, 1/l) for code and numbers.
const figtree = Figtree({ variable: "--font-figtree", subsets: ["latin"] });
const jetbrainsMono = JetBrains_Mono({ variable: "--font-jetbrains-mono", subsets: ["latin"] });
// Bricolage Grotesque: a characterful grotesque used only for the "drill" wordmark.
const bricolage = Bricolage_Grotesque({ variable: "--font-bricolage", subsets: ["latin"], weight: ["800"] });

export const metadata: Metadata = {
  title: "Drill",
  description: "Personal coding-interview practice: 75 classic problems in Python, run in the browser.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${figtree.variable} ${jetbrainsMono.variable} ${bricolage.variable} h-full antialiased`} suppressHydrationWarning>
      <body className="flex min-h-full flex-col">
        {/* Applies the saved theme before first paint (no flash). Next injects it into <head> outside React's hydration tree. */}
        <Script id="theme-init" strategy="beforeInteractive">
          {themeInitScript}
        </Script>
        <header className="flex h-(--header-h) shrink-0 items-center justify-between gap-2 border-b border-line bg-panel px-(--gutter)">
          <Link href="/" aria-label="drill home" className="flex shrink-0 items-center gap-2.5 text-fg">
            <DrillMark className="h-8 w-8 sm:h-9 sm:w-9 lg:h-10 lg:w-10" />
            <span className="hidden font-(family-name:--font-bricolage) text-2xl font-extrabold tracking-[-0.04em] sm:inline lg:text-[1.75rem]">drill</span>
          </Link>
          <div className="flex min-w-0 items-center gap-1">
            <nav className="flex min-w-0 items-center gap-0.5 overflow-x-auto sm:gap-1">
              <NavLinks />
            </nav>
            {/* Outside the scrolling nav so it never scrolls offscreen on narrow phones. */}
            <ThemeToggle />
          </div>
        </header>
        <main className="flex flex-1 flex-col">{children}</main>
        <HydrationMarker />
      </body>
    </html>
  );
}
