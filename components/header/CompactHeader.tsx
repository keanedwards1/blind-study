import Link from "next/link";
import { DrillMark } from "../icons";
import "./compact-header.css";

/**
 * The slim header on individual problem pages: only the logo and the site name, so the workspace gets the room.
 * Its height is --header-h-compact (compact-header.css), which also becomes --header-h for full-height pages below it.
 */
export default function CompactHeader() {
  return (
    <header className="site-header-compact flex h-(--header-h-compact) shrink-0 items-center border-b border-line bg-panel px-4">
      <Link href="/" aria-label="drill home" className="flex items-center gap-2 text-fg">
        <DrillMark className="h-6 w-6" />
        <span className="font-(family-name:--font-bricolage) text-lg font-extrabold tracking-[-0.04em]">drill</span>
      </Link>
    </header>
  );
}
