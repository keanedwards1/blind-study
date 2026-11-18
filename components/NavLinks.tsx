"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Problems" },
  { href: "/learn", label: "Learn" },
  { href: "/python", label: "Learn Python", short: "Python" },
  { href: "/quiz", label: "Quiz" },
  { href: "/mock", label: "Mock assessment", short: "Mock" },
];

/** Top navigation; the current section is underlined in the accent colour. */
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
            className={`whitespace-nowrap border-b-2 px-1 py-1 text-sm font-medium transition-colors sm:text-[15px] ${
              active ? "border-accent text-fg" : "border-transparent text-muted hover:text-fg"
            }`}
          >
            {short ? (
              <>
                {/* Full label only once there's room for it at the larger nav size. */}
                <span className="md:hidden">{short}</span>
                <span className="hidden md:inline">{label}</span>
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
