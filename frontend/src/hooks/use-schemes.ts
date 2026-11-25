"use client";

import { useState, useEffect, useCallback } from "react";
import apiClient from "@/lib/api-client";
import type { Scheme, SchemeListResponse } from "@/types";

interface UseSchemeParams {
  q?: string;
  state?: string;
  education_level?: string;
  scheme_type?: string;
  page?: number;
}

export function useSchemes(params: UseSchemeParams = {}) {
  const [data, setData] = useState<SchemeListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<SchemeListResponse>("/schemes", {
        params: {
          q: params.q || undefined,
          state: params.state || undefined,
          education_level: params.education_level || undefined,
          scheme_type: params.scheme_type || undefined,
          page: params.page || 1,
          per_page: 20,
        },
      });
      setData(response.data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load schemes";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, [params.q, params.state, params.education_level, params.scheme_type, params.page]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { data, loading, error, refetch: fetch };
}

export function useScheme(id: string) {
  const [scheme, setScheme] = useState<Scheme | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    apiClient
      .get<Scheme>(`/schemes/${id}`)
      .then((r) => setScheme(r.data))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  return { scheme, loading, error };
}
