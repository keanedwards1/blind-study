import Link from "next/link";
import { SiteMark } from "../icons";

/**
 * The logo lockup: the sliding-window mark, "BLIND 75" and "FROM SCRATCH" in Chakra Petch (--font-chakra, set in the root
 * layout). "full" is the main header; "compact" is the slim header on problem pages.
 */
export default function Brand({ size = "full" }: { size?: "full" | "compact" }) {
  const full = size === "full";
  return (
    <Link href="/" aria-label="Blind 75 from Scratch home" className="flex shrink-0 items-center gap-2.5 text-fg">
      <SiteMark className={full ? "h-8 w-8 sm:h-9 sm:w-9 lg:h-10 lg:w-10" : "h-7 w-7"} />
      <span className={`flex-col leading-none font-(family-name:--font-chakra) ${full ? "hidden gap-1 sm:flex" : "flex gap-0.5"}`}>
        <span className={`font-bold tracking-[0.04em] ${full ? "text-xl lg:text-2xl" : "text-base"}`}>BLIND 75</span>
        <span className={`font-semibold tracking-[0.3em] text-accent-text ${full ? "text-[9px] lg:text-[10px]" : "text-[7.5px]"}`}>FROM SCRATCH</span>
      </span>
    </Link>
  );
}
