import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import Script from "next/script";
import HydrationMarker from "@/components/HydrationMarker";
import ThemeToggle, { themeInitScript } from "@/components/ThemeToggle";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Drill",
  description: "Personal coding-interview practice: 75 classic problems in Python, run in the browser.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`} suppressHydrationWarning>
      <body className="flex min-h-full flex-col">
        {/* Applies the saved theme before first paint (no flash). Next injects it into <head> outside React's hydration tree. */}
        <Script id="theme-init" strategy="beforeInteractive">
          {themeInitScript}
        </Script>
        <header className="flex h-12 shrink-0 items-center justify-between gap-3 border-b border-line bg-panel px-4">
          <Link href="/" className="font-semibold tracking-tight text-fg">
            drill<span className="text-warn">.</span>
          </Link>
          <nav className="flex items-center gap-4 overflow-x-auto text-sm sm:gap-5">
            <Link href="/" className="text-muted hover:text-fg">
              Problems
            </Link>
            <Link href="/learn" className="text-muted hover:text-fg">
              Learn
            </Link>
            <Link href="/quiz" className="text-muted hover:text-fg">
              Quiz
            </Link>
            <Link href="/mock" className="whitespace-nowrap text-muted hover:text-fg">
              Mock assessment
            </Link>
            <ThemeToggle />
          </nav>
        </header>
        <main className="flex flex-1 flex-col">{children}</main>
        <HydrationMarker />
      </body>
    </html>
  );
}
