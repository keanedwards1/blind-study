"use client";

import { useEffect } from "react";

/** Sets <html data-hydrated> once React has hydrated the layout (used by the Cypress tests). */
export default function HydrationMarker() {
  useEffect(() => {
    document.documentElement.dataset.hydrated = "1";
  }, []);
  return null;
}
