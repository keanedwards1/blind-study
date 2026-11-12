"use client";

import { save, useStored } from "@/lib/storage";

export type Theme = "light" | "dark";

export function useTheme(): Theme {
  return useStored<Theme>("theme", "light");
}

/** Runs before first paint (inlined in <head>) so the saved theme applies without a flash. */
export const themeInitScript = `try{var t=JSON.parse(localStorage.getItem("drill:v1:theme"));if(t==="dark")document.documentElement.dataset.theme="dark"}catch(e){}`;

export default function ThemeToggle() {
  const theme = useTheme();
  const next: Theme = theme === "dark" ? "light" : "dark";
  return (
    <button
      onClick={() => {
        document.documentElement.dataset.theme = next;
        save("theme", next);
      }}
      className="grid h-9 w-9 shrink-0 place-items-center rounded-full text-base text-muted hover:bg-hover hover:text-fg sm:h-10 sm:w-10 sm:text-lg lg:h-11 lg:w-11 lg:text-xl"
      aria-label={`Switch to ${next} mode`}
      title={`Switch to ${next} mode`}
    >
      {theme === "dark" ? "☀︎" : "☾"}
    </button>
  );
}
