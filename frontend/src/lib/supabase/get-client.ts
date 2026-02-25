import { createClient as createServerClient } from "./server";

/**
 * Server-only: Get Supabase client for data fetching.
 * Returns null if env vars are not configured.
 */
export async function getSupabaseClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key =
    process.env.SUPABASE_SERVICE_ROLE_KEY ||
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !key) return null;
  return createServerClient();
}
