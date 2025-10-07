import { getSupabaseClient } from './supabaseClient';

type MagicLinkPayload = {
  email: string;
  redirectTo?: string;
};

export async function sendMagicLink({ email, redirectTo }: MagicLinkPayload) {
  const supabase = getSupabaseClient();
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: redirectTo,
    },
  });

  if (error) {
    throw new Error(error.message);
  }
}

export async function exchangeMagicLinkToken(accessToken: string) {
  const supabase = getSupabaseClient();
  const { data, error } = await supabase.auth.getUser(accessToken);
  if (error) {
    throw new Error(error.message);
  }
  return data.user;
}
