import { Fraunces } from "next/font/google";

// Fraunces (SIL Open Font License): a warm, organic serif for the Learn Python game titles. Loaded only under /python.
const display = Fraunces({ variable: "--font-display", subsets: ["latin"], weight: ["600", "800"] });

export default function PythonLayout({ children }: { children: React.ReactNode }) {
  return <div className={`${display.variable} flex min-h-0 flex-1 flex-col`}>{children}</div>;
}
