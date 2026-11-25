"use client";
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { FileCheck, CheckCircle2, XCircle } from "lucide-react";
import apiClient from "@/lib/api-client";
import toast from "react-hot-toast";

interface ReviewItem {
  id: string;
  rule_category: string;
  rule_key: string;
  condition: Record<string, unknown>;
  source_text?: string;
  source_page?: number;
  confidence?: number;
}

export default function ReviewerPage() {
  const [queue, setQueue] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState<string | null>(null);

  async function loadQueue() {
    try {
      const res = await apiClient.get<ReviewItem[]>("/reviews/queue");
      setQueue(res.data);
    } catch (err: any) {
      if (err?.response?.status !== 403) toast.error("Failed to load review queue");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadQueue();
  }, []);

  async function decide(id: string, decision: "approved" | "rejected") {
    setProcessing(id);
    try {
      await apiClient.post(`/reviews/${id}/approve`, { decision });
      toast.success(`Rule ${decision}`);
      setQueue((prev) => prev.filter((r) => r.id !== id));
    } catch {
      toast.error("Failed to submit decision");
    } finally {
      setProcessing(null);
    }
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
          <FileCheck className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            Document Review Queue
          </h1>
          <p className="text-slate-500 dark:text-slate-400">
            Review and approve AI-extracted scheme rules.
          </p>
        </div>
      </div>

      <div className="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 p-4 text-sm text-amber-700 dark:text-amber-300">
        Only approved rules are used for eligibility evaluation and ChangeLens comparisons.
        Review each rule against the original document text.
      </div>

      {loading ? (
        <div className="text-center py-8 text-slate-500">Loading queue…</div>
      ) : queue.length === 0 ? (
        <Card>
          <CardContent className="py-16 text-center space-y-2">
            <CheckCircle2 className="w-10 h-10 text-green-400 mx-auto" />
            <p className="font-medium text-slate-700 dark:text-slate-300">
              Review queue is empty
            </p>
            <p className="text-sm text-slate-500">All extracted rules have been reviewed.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          <p className="text-sm text-slate-500">
            {queue.length} rule{queue.length !== 1 ? "s" : ""} pending review
          </p>
          {queue.map((rule) => (
            <Card key={rule.id} className="overflow-hidden">
              <CardContent className="p-0">
                <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <Badge variant="secondary">{rule.rule_category}</Badge>
                    <span className="font-mono text-sm text-slate-700 dark:text-slate-300">
                      {rule.rule_key}
                    </span>
                    {rule.confidence !== undefined && (
                      <span className="text-xs text-slate-400">
                        confidence: {Math.round(rule.confidence * 100)}%
                      </span>
                    )}
                  </div>
                  <Badge
                    variant={
                      rule.confidence && rule.confidence >= 0.8 ? "success" : "warning"
                    }
                  >
                    {rule.confidence && rule.confidence >= 0.8
                      ? "High confidence"
                      : "Low confidence"}
                  </Badge>
                </div>

                <div className="p-4 space-y-3">
                  <div className="rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-3">
                    <p className="text-xs font-medium text-slate-500 mb-1">Extracted Condition</p>
                    <pre className="text-xs text-slate-700 dark:text-slate-300 overflow-x-auto">
                      {JSON.stringify(rule.condition, null, 2)}
                    </pre>
                  </div>

                  {rule.source_text && (
                    <div className="rounded-lg bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800 p-3">
                      <p className="text-xs font-medium text-blue-600 dark:text-blue-400 mb-1">
                        Source text {rule.source_page ? `(page ${rule.source_page})` : ""}
                      </p>
                      <p className="text-xs text-blue-700 dark:text-blue-300 leading-relaxed">
                        {rule.source_text}
                      </p>
                    </div>
                  )}

                  <div className="flex gap-3 pt-2">
                    <Button
                      size="sm"
                      loading={processing === rule.id}
                      onClick={() => decide(rule.id, "approved")}
                      className="gap-1.5"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" /> Approve
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      loading={processing === rule.id}
                      onClick={() => decide(rule.id, "rejected")}
                      className="gap-1.5"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Reject
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
