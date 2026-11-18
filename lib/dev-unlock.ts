/**
 * Under `npm run dev`, every world, stage and guardian is open so content can be checked without playing through it.
 * Production builds (`next build`/`next start`) always lock normally. Set NEXT_PUBLIC_DEV_LOCKS=1 to see real locks in dev.
 */
export const DEV_UNLOCK_ALL = process.env.NODE_ENV === "development" && process.env.NEXT_PUBLIC_DEV_LOCKS !== "1";
