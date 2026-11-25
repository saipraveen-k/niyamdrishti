"use client";
import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ChangeEventCard } from "@/components/features/changelens/change-event-card";
import { GitCompare, AlertTriangle, TrendingUp, Info } from "lucide-react";
import apiClient from "@/lib/api-client";
import type { Scheme } from "@/types";

interface PolicyChange {
  id: string;
  rule_category: string;
  rule_key: string;
  change_type: "ADDED" | "REMOVED" | "MODIFIED";
  severity: "HIGH" | "MEDIUM" | "LOW";
  old_condition?: Record<string, unknown>;
  new_condition?: Record<string, unknown>;
  old_source_text?: string;
  new_source_text?: string;
  old_source_page?: number;
  new_source_page?: number;
}

interface ComparisonResult {
  scheme_id: string;
  scheme_name: string;
  old_version: string;
  new_version: string;
  changes: PolicyChange[];
  summary: { high: number; medium: number; low: number; total: number };
}

export default function ChangeLensPage() {
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [selectedScheme, setSelectedScheme] = useState<string>("");
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [schemesLoading, setSchemesLoading] = useState(true);

  useEffect(() => {
    apiClient
      .get<{ items: Scheme[] }>("/schemes?limit=50")
      .then((r) => setSchemes(r.data.items ?? []))
      .catch(() => {})
      .finally(() => setSchemesLoading(false));
  }, []);

  async function runComparison() {
    if (!selectedScheme) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await apiClient.get<ComparisonResult>(
        `/changelens/compare/${selectedScheme}`
      );
      setResult(res.data);
    } catch {
      // silent
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
          <GitCompare className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">ChangeLens</h1>
          <p className="text-slate-500 dark:text-slate-400">
            See exactly what changed between scheme versions — with AI-extracted evidence.
          </p>
        </div>
      </div>

      <div className="rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 p-4 flex gap-3 text-sm text-blue-700 dark:text-blue-300">
        <Info className="w-4 h-4 shrink-0 mt-0.5" />
        <p>
          ChangeLens compares AI-extracted rules from official documents.
          Changes are detected deterministically — no AI guessing.
          Always verify against the original notification before acting.
        </p>
      </div>

      <Card>
        <CardContent className="p-5 flex flex-col sm:flex-row gap-4 items-end">
          <div className="flex-1 space-y-1.5">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
              Select Scheme
            </label>
            {schemesLoading ? (
              <Skeleton className="h-10 w-full" />
            ) : (
              <select
                value={selectedScheme}
                onChange={(e) => setSelectedScheme(e.target.value)}
                className="flex h-10 w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
              >
                <option value="">Choose a scheme to compare versions…</option>
                {schemes.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.state})
                  </option>
                ))}
              </select>
            )}
          </div>
          <Button
            onClick={runComparison}
            disabled={!selectedScheme || loading}
            loading={loading}
            className="shrink-0"
          >
            Compare Versions
          </Button>
        </CardContent>
      </Card>

      {loading && (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      )}

      {result && !loading && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-4 items-center justify-between">
            <div>
              <p className="font-semibold text-slate-900 dark:text-white">{result.scheme_name}</p>
              <p className="text-xs text-slate-500 mt-0.5">
                Version {result.old_version} → {result.new_version}
              </p>
            </div>
            <div className="flex gap-2">
              {result.summary.high > 0 && (
                <Badge variant="destructive">
                  <AlertTriangle className="w-3 h-3 mr-1" />
                  {result.summary.high} High
                </Badge>
              )}
              {result.summary.medium > 0 && (
                <Badge variant="warning">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  {result.summary.medium} Medium
                </Badge>
              )}
              {result.summary.low > 0 && (
                <Badge variant="secondary">{result.summary.low} Low</Badge>
              )}
            </div>
          </div>

          {result.changes.length === 0 ? (
            <Card>
              <CardContent className="py-16 text-center space-y-2">
                <p className="font-medium text-slate-700 dark:text-slate-300">No changes detected</p>
                <p className="text-sm text-slate-500">
                  The latest version matches the previous on all extracted rules.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-3">
              {result.changes.map((change, i) => (
                <ChangeEventCard key={i} change={change} />
              ))}
            </div>
          )}
        </div>
      )}

      {!result && !loading && (
        <div className="text-center py-16 text-slate-400">
          <GitCompare className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p className="text-sm">Select a scheme above to compare its versions.</p>
        </div>
      )}
    </div>
  );
}
