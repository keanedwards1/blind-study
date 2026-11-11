import ProblemList from "@/components/ProblemList";
import { categories, summaries } from "@/lib/problems";

export default function Home() {
  return <ProblemList problems={summaries()} categories={categories} />;
}
