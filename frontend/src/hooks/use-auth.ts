"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import type { User, Session } from "@supabase/supabase-js";
import type { AppRole } from "@/types";

interface AuthState {
  user: User | null;
  session: Session | null;
  appRole: AppRole | null;
  loading: boolean;
  signOut: () => Promise<void>;
}

export function useAuth(): AuthState {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  const supabase = createClient();

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      if (session?.access_token) {
        localStorage.setItem("nd_access_token", session.access_token);
      }
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
        if (session?.access_token) {
          localStorage.setItem("nd_access_token", session.access_token);
        } else {
          localStorage.removeItem("nd_access_token");
        }
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const appRole = (user?.user_metadata?.app_role as AppRole) ?? null;

  const signOut = async () => {
    await supabase.auth.signOut();
    localStorage.removeItem("nd_access_token");
    window.location.href = "/";
  };

  return { user, session, appRole, loading, signOut };
}
