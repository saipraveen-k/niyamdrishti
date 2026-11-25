"use client";
import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Map,
  CheckCircle2,
  Circle,
  Clock,
  ChevronDown,
  ChevronUp,
  Plus,
  ExternalLink,
} from "lucide-react";
import apiClient from "@/lib/api-client";
import { formatDate } from "@/lib/utils";

interface ActionTask {
  id: string;
  title: string;
  description?: string;
  task_type: string;
  status: "pending" | "in_progress" | "completed" | "skipped";
  due_date?: string;
  resource_url?: string;
}

interface ActionPlan {
  id: string;
  scheme_id: string;
  scheme_name?: string;
  status: "active" | "completed" | "abandoned";
  tasks: ActionTask[];
  created_at: string;
}

export default function LifeMapPage() {
  const [plans, setPlans] = useState<ActionPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const [updating, setUpdating] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .get<ActionPlan[]>("/lifemap/plans")
      .then((r) => setPlans(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  function toggle(id: string) {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  }

  async function completeTask(planId: string, taskId: string) {
    setUpdating(taskId);
    try {
      await apiClient.patch(`/lifemap/tasks/${taskId}`, { status: "completed" });
      setPlans((prev) =>
        prev.map((p) =>
          p.id === planId
            ? {
                ...p,
                tasks: p.tasks.map((t) =>
                  t.id === taskId ? { ...t, status: "completed" as const } : t
                ),
              }
            : p
        )
      );
    } catch {
      // silent
    } finally {
      setUpdating(null);
    }
  }

  const statusIcon: Record<ActionTask["status"], React.ReactNode> = {
    completed: <CheckCircle2 className="w-4 h-4 text-green-500" />,
    in_progress: <Clock className="w-4 h-4 text-blue-500" />,
    pending: <Circle className="w-4 h-4 text-slate-400" />,
    skipped: <Circle className="w-4 h-4 text-slate-300" />,
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
            <Map className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">LifeMap</h1>
            <p className="text-slate-500 dark:text-slate-400">
              Your personalised action plans for each scheme.
            </p>
          </div>
        </div>
        <Button
          variant="secondary"
          onClick={() => (window.location.href = "/schemes")}
          className="gap-2 shrink-0"
        >
          <Plus className="w-4 h-4" /> Add Plan
        </Button>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      ) : plans.length === 0 ? (
        <Card>
          <CardContent className="py-16 text-center space-y-3">
            <Map className="w-10 h-10 text-slate-300 dark:text-slate-700 mx-auto" />
            <p className="font-medium text-slate-700 dark:text-slate-300">No action plans yet</p>
            <p className="text-sm text-slate-500">
              After checking eligibility for a scheme, you can generate a personalised action plan.
            </p>
            <Button
              variant="secondary"
              onClick={() => (window.location.href = "/eligibility")}
            >
              Check Eligibility
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {plans.map((plan) => {
            const done = plan.tasks.filter((t) => t.status === "completed").length;
            const total = plan.tasks.length;
            const pct = total > 0 ? Math.round((done / total) * 100) : 0;
            const isOpen = expanded[plan.id] ?? true;

            return (
              <Card key={plan.id} className="overflow-hidden">
                <CardContent className="p-0">
                  <button
                    className="w-full p-4 flex items-center justify-between gap-4 text-left hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
                    onClick={() => toggle(plan.id)}
                  >
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-slate-900 dark:text-white truncate">
                        {plan.scheme_name ?? plan.scheme_id}
                      </p>
                      <div className="flex items-center gap-3 mt-1.5">
                        <div className="flex-1 h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden max-w-[160px]">
                          <div
                            className="h-full gradient-primary rounded-full transition-all"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                        <span className="text-xs text-slate-500 shrink-0">
                          {done}/{total} tasks · {pct}%
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <Badge variant={plan.status === "completed" ? "success" : "secondary"}>
                        {plan.status}
                      </Badge>
                      {isOpen ? (
                        <ChevronUp className="w-4 h-4 text-slate-400" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-slate-400" />
                      )}
                    </div>
                  </button>

                  {isOpen && (
                    <div className="border-t border-slate-200 dark:border-slate-800 divide-y divide-slate-100 dark:divide-slate-800">
                      {plan.tasks.map((task) => (
                        <div key={task.id} className="p-4 flex items-start gap-3">
                          <div className="mt-0.5 shrink-0">{statusIcon[task.status]}</div>
                          <div className="flex-1 min-w-0">
                            <p
                              className={`text-sm font-medium ${
                                task.status === "completed"
                                  ? "line-through text-slate-400"
                                  : "text-slate-800 dark:text-slate-200"
                              }`}
                            >
                              {task.title}
                            </p>
                            {task.description && (
                              <p className="text-xs text-slate-500 mt-0.5">{task.description}</p>
                            )}
                            {task.due_date && (
                              <p className="text-xs text-amber-600 dark:text-amber-400 mt-0.5">
                                Due: {formatDate(task.due_date)}
                              </p>
                            )}
                          </div>
                          <div className="flex gap-2 shrink-0">
                            {task.resource_url && (
                              <a
                                href={task.resource_url}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                <Button variant="ghost" size="sm">
                                  <ExternalLink className="w-3.5 h-3.5" />
                                </Button>
                              </a>
                            )}
                            {task.status !== "completed" && (
                              <Button
                                variant="outline"
                                size="sm"
                                loading={updating === task.id}
                                onClick={() => completeTask(plan.id, task.id)}
                              >
                                Done
                              </Button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
