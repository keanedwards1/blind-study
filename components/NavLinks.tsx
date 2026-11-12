"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Problems" },
  { href: "/learn", label: "Learn" },
  { href: "/quiz", label: "Quiz" },
  { href: "/mock", label: "Mock assessment", short: "Mock" },
];

/** Pill-style top navigation; the current section is filled. */
export default function NavLinks() {
  const path = usePathname();
  return (
    <>
      {links.map(({ href, label, short }) => {
        const active = href === "/" ? path === "/" || path.startsWith("/problems") : path.startsWith(href);
        return (
          <Link
            key={href}
            href={href}
            aria-current={active ? "page" : undefined}
            className={`whitespace-nowrap rounded-full px-3 py-1.5 text-sm font-semibold transition-colors sm:px-3.5 ${
              active ? "bg-fg text-page" : "text-muted hover:bg-hover hover:text-fg"
            }`}
          >
            {short ? (
              <>
                <span className="sm:hidden">{short}</span>
                <span className="hidden sm:inline">{label}</span>
              </>
            ) : (
              label
            )}
          </Link>
        );
      })}
    </>
  );
}
