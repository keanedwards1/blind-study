import type { Metadata } from "next";
import { Figtree, JetBrains_Mono } from "next/font/google";
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

export const metadata: Metadata = {
  title: "Drill",
  description: "Personal coding-interview practice: 75 classic problems in Python, run in the browser.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${figtree.variable} ${jetbrainsMono.variable} h-full antialiased`} suppressHydrationWarning>
      <body className="flex min-h-full flex-col">
        {/* Applies the saved theme before first paint (no flash). Next injects it into <head> outside React's hydration tree. */}
        <Script id="theme-init" strategy="beforeInteractive">
          {themeInitScript}
        </Script>
        <header className="flex h-14 shrink-0 items-center justify-between gap-3 border-b border-line bg-panel px-4 sm:px-6">
          <Link href="/" aria-label="drill home" className="flex shrink-0 items-center gap-2 text-lg font-extrabold tracking-tight text-fg">
            <DrillMark className="h-7 w-7" />
            <span className="hidden sm:inline">
              drill
            </span>
          </Link>
          <nav className="flex min-w-0 items-center gap-1 overflow-x-auto">
            <NavLinks />
            <ThemeToggle />
          </nav>
        </header>
        <main className="flex flex-1 flex-col">{children}</main>
        <HydrationMarker />
      </body>
    </html>
  );
}
