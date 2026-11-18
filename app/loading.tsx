import PageLoader from "@/components/loader/PageLoader";

/** Shown while any page without its own loading screen streams in. */
export default function Loading() {
  return <PageLoader variant="page" label="Loading" />;
}
