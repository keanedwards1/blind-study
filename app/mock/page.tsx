import type { Metadata } from "next";
import MockAssessment from "@/components/MockAssessment";
import { problems } from "@/lib/problems";

export const metadata: Metadata = { title: "Mock assessment · Drill" };

export default function MockPage() {
  return <MockAssessment problems={problems} />;
}
