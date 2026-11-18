import Brand from "./Brand";
import "./compact-header.css";

/**
 * The slim header on individual problem pages: only the logo, so the workspace gets the room.
 * Its height is --header-h-compact (compact-header.css), which also becomes --header-h for full-height pages below it.
 */
export default function CompactHeader() {
  return (
    <header className="site-header-compact flex h-(--header-h-compact) shrink-0 items-center border-b border-line bg-panel px-4">
      <Brand size="compact" />
    </header>
  );
}
