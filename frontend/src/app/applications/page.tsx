"use client";
import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Plus, FileText } from "lucide-react";
import apiClient from "@/lib/api-client";
import toast from "react-hot-toast";
import { formatDate } from "@/lib/utils";

interface ApplicationRecord {
  id: string;
  scheme_id: string;
  scheme_name?: string;
  status:
    | "not_started"
    | "in_progress"
    | "submitted"
    | "under_review"
    | "approved"
    | "rejected"
    | "withdrawn";
  applied_date?: string;
  notes?: string;
}

const STATUS_STEPS: ApplicationRecord["status"][] = [
  "in_progress",
  "submitted",
  "under_review",
  "approved",
];

const statusVariant: Record<
  string,
  "success" | "destructive" | "warning" | "secondary"
> = {
  approved: "success",
  rejected: "destructive",
  submitted: "warning",
  under_review: "warning",
  in_progress: "secondary",
  not_started: "secondary",
  withdrawn: "secondary",
};

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<ApplicationRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .get<ApplicationRecord[]>("/applications")
      .then((r) => setApplications(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  async function updateStatus(
    id: string,
    status: ApplicationRecord["status"]
  ) {
    setUpdating(id);
    try {
      await apiClient.patch(`/applications/${id}`, { status });
      setApplications((prev) =>
        prev.map((a) => (a.id === id ? { ...a, status } : a))
      );
      toast.success("Status updated");
    } catch {
      toast.error("Could not update status");
    } finally {
      setUpdating(null);
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
            <FileText className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Applications
            </h1>
            <p className="text-slate-500 dark:text-slate-400">
              Track your scheme applications in one place.
            </p>
          </div>
        </div>
        <Button
          variant="secondary"
          onClick={() => (window.location.href = "/schemes")}
          className="gap-2 shrink-0"
        >
          <Plus className="w-4 h-4" /> Browse Schemes
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-8 text-slate-500">Loading…</div>
      ) : applications.length === 0 ? (
        <Card>
          <CardContent className="py-16 text-center space-y-3">
            <FileText className="w-10 h-10 text-slate-300 dark:text-slate-700 mx-auto" />
            <p className="font-medium text-slate-700 dark:text-slate-300">
              No applications tracked
            </p>
            <p className="text-sm text-slate-500">
              Browse schemes and start tracking your applications.
            </p>
            <Button
              variant="secondary"
              onClick={() => (window.location.href = "/schemes")}
            >
              Browse Schemes
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {applications.map((app) => (
            <Card key={app.id}>
              <CardContent className="p-5 space-y-4">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-medium text-slate-900 dark:text-white">
                      {app.scheme_name ?? "Scheme Application"}
                    </p>
                    {app.applied_date && (
                      <p className="text-xs text-slate-400 mt-0.5">
                        Applied: {formatDate(app.applied_date)}
                      </p>
                    )}
                  </div>
                  <Badge variant={statusVariant[app.status] ?? "secondary"}>
                    {app.status.replace(/_/g, " ")}
                  </Badge>
                </div>

                {!["approved", "rejected", "withdrawn"].includes(app.status) && (
                  <div className="flex flex-wrap gap-2">
                    {STATUS_STEPS.filter((s) => s !== app.status).map((s) => (
                      <Button
                        key={s}
                        variant="outline"
                        size="sm"
                        loading={updating === app.id}
                        onClick={() => updateStatus(app.id, s)}
                      >
                        Mark as {s.replace(/_/g, " ")}
                      </Button>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
