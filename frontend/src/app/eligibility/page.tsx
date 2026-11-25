"use client";
import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { CriterionResult } from "@/components/features/eligibility/criterion-result";
import { CheckCircle2, XCircle, HelpCircle, Info, Shield } from "lucide-react";
import apiClient from "@/lib/api-client";
import type { Scheme, EvaluationReport } from "@/types";

function EligibilityContent() {
  const searchParams = useSearchParams();
  const preselected = searchParams.get("scheme_id") ?? "";
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [selectedScheme, setSelectedScheme] = useState(preselected);
  const [report, setReport] = useState<EvaluationReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [schemesLoading, setSchemesLoading] = useState(true);
  const [profileMissing, setProfileMissing] = useState(false);

  useEffect(() => {
    apiClient
      .get<{ items: Scheme[] }>("/schemes?limit=50")
      .then((r) => setSchemes(r.data.items ?? []))
      .catch(() => {})
      .finally(() => setSchemesLoading(false));
  }, []);

  async function checkEligibility() {
    if (!selectedScheme) return;
    setLoading(true);
    setReport(null);
    setProfileMissing(false);
    try {
      const res = await apiClient.post<EvaluationReport>("/eligibility/evaluate", {
        scheme_id: selectedScheme,
      });
      setReport(res.data);
    } catch (err: any) {
      if (err?.response?.status === 404) setProfileMissing(true);
    } finally {
      setLoading(false);
    }
  }

  const icons: Record<string, React.ReactNode> = {
    PASSED: <CheckCircle2 className="w-6 h-6 text-green-500" />,
    FAILED: <XCircle className="w-6 h-6 text-red-500" />,
    UNKNOWN: <HelpCircle className="w-6 h-6 text-amber-500" />,
    NEEDS_VERIFICATION: <HelpCircle className="w-6 h-6 text-blue-500" />,
  };

  const badgeVariant: Record<string, "success" | "destructive" | "warning"> = {
    PASSED: "success",
    FAILED: "destructive",
    UNKNOWN: "warning",
    NEEDS_VERIFICATION: "warning",
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
          <Shield className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Eligibility Checker</h1>
          <p className="text-slate-500 dark:text-slate-400">
            Rule-based evaluation against your profile — no AI guessing.
          </p>
        </div>
      </div>

      <div className="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 p-4 flex gap-3 text-sm text-amber-700 dark:text-amber-300">
        <Info className="w-4 h-4 shrink-0 mt-0.5" />
        <p>
          Results are based on approved rules extracted from official notifications.
          UNKNOWN means your profile is missing that field — not that you are ineligible.
          Always verify with the official scheme notification.
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
                <option value="">Choose a scheme to check eligibility…</option>
                {schemes.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.state})
                  </option>
                ))}
              </select>
            )}
          </div>
          <Button
            onClick={checkEligibility}
            disabled={!selectedScheme || loading}
            loading={loading}
            className="shrink-0"
          >
            Check Eligibility
          </Button>
        </CardContent>
      </Card>

      {profileMissing && (
        <div className="rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 p-5 space-y-3">
          <p className="font-medium text-blue-800 dark:text-blue-200">Profile not found</p>
          <p className="text-sm text-blue-700 dark:text-blue-300">
            You need to complete your student profile before checking eligibility.
          </p>
          <Button
            variant="secondary"
            onClick={() => (window.location.href = "/settings/profile")}
          >
            Complete Profile
          </Button>
        </div>
      )}

      {loading && (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </div>
      )}

      {report && !loading && (
        <div className="space-y-4">
          <Card>
            <CardContent className="p-5 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                {icons[report.overall_result]}
                <div>
                  <p className="font-semibold text-slate-900 dark:text-white">Overall Result</p>
                  <p className="text-sm text-slate-500 mt-0.5">
                    {report.passed_mandatory} of {report.total_mandatory} mandatory criteria met ·{" "}
                    {report.match_score.toFixed(0)}% match score
                  </p>
                </div>
              </div>
              <Badge variant={badgeVariant[report.overall_result]}>{report.overall_result}</Badge>
            </CardContent>
          </Card>
          <div>
            <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-3">
              Criterion-by-criterion breakdown
            </p>
            <div className="space-y-2">
              {report.criteria.map((c, i) => (
                <CriterionResult key={i} criterion={c} />
              ))}
            </div>
          </div>
        </div>
      )}

      {!report && !loading && !profileMissing && (
        <div className="text-center py-16 text-slate-400">
          <Shield className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p className="text-sm">Select a scheme above to check your eligibility.</p>
        </div>
      )}
    </div>
  );
}

export default function EligibilityPage() {
  return (
    <Suspense fallback={<div className="p-6 text-slate-500">Loading…</div>}>
      <EligibilityContent />
    </Suspense>
  );
}
