import type { Metadata } from "next";
import { Chakra_Petch, Figtree, JetBrains_Mono } from "next/font/google";
import Script from "next/script";
import Brand from "@/components/header/Brand";
import CompactHeader from "@/components/header/CompactHeader";
import HeaderSwitch from "@/components/header/HeaderSwitch";
import HydrationMarker from "@/components/HydrationMarker";
import NavLinks from "@/components/NavLinks";
import ThemeToggle, { themeInitScript } from "@/components/ThemeToggle";
import "./globals.css";

// Figtree: a warm geometric sans with a large x-height, readable at small UI sizes and bold at display sizes.
// JetBrains Mono: tall, distinct glyphs (0/O, 1/l) for code and numbers.
const figtree = Figtree({ variable: "--font-figtree", subsets: ["latin"] });
const jetbrainsMono = JetBrains_Mono({ variable: "--font-jetbrains-mono", subsets: ["latin"] });
// Chakra Petch: an angular face with cut corners, used only for the "BLIND 75 / FROM SCRATCH" wordmark.
const chakra = Chakra_Petch({ variable: "--font-chakra", subsets: ["latin"], weight: ["600", "700"] });

export const metadata: Metadata = {
  title: "Blind 75 from Scratch",
  description: "Learn Python from the ground up, then work through the Blind 75 interview problems, all in the browser.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${figtree.variable} ${jetbrainsMono.variable} ${chakra.variable} h-full antialiased`} suppressHydrationWarning>
      <body className="flex min-h-full flex-col">
        {/* Applies the saved theme before first paint (no flash). Next injects it into <head> outside React's hydration tree. */}
        <Script id="theme-init" strategy="beforeInteractive">
          {themeInitScript}
        </Script>
        <HeaderSwitch
          compact={<CompactHeader />}
          full={
            <header className="flex h-(--header-h) shrink-0 items-center justify-between gap-2 border-b border-line bg-panel px-(--gutter)">
              <Brand />
              <div className="flex min-w-0 items-center gap-1">
                <nav className="mr-2 flex min-w-0 items-center gap-4 overflow-x-auto sm:mr-4 sm:gap-6">
                  <NavLinks />
                </nav>
                {/* Outside the scrolling nav so it never scrolls offscreen on narrow phones. */}
                <ThemeToggle />
              </div>
            </header>
          }
        />
        <main className="flex flex-1 flex-col">{children}</main>
        <HydrationMarker />
      </body>
    </html>
  );
}
