import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { Plus, Minus, Edit3, FileText } from "lucide-react";
import type { PolicyChangeEvent } from "@/types";

interface ChangeEventCardProps {
  change: PolicyChangeEvent;
}

const changeConfig = {
  ADDED: {
    icon: Plus,
    label: "Added",
    color: "text-green-600 dark:text-green-400",
    bg: "bg-green-50 dark:bg-green-900/20",
  },
  REMOVED: {
    icon: Minus,
    label: "Removed",
    color: "text-red-600 dark:text-red-400",
    bg: "bg-red-50 dark:bg-red-900/20",
  },
  MODIFIED: {
    icon: Edit3,
    label: "Modified",
    color: "text-amber-600 dark:text-amber-400",
    bg: "bg-amber-50 dark:bg-amber-900/20",
  },
};

const severityBadge: Record<string, "destructive" | "warning" | "secondary"> = {
  HIGH: "destructive",
  MEDIUM: "warning",
  LOW: "secondary",
};

export function ChangeEventCard({ change }: ChangeEventCardProps) {
  const config = changeConfig[change.change_type];
  const Icon = config.icon;

  return (
    <Card className="overflow-hidden">
      <CardContent className="p-0">
        <div
          className={cn(
            "flex items-center gap-3 px-4 py-3 border-b border-slate-200 dark:border-slate-800",
            config.bg
          )}
        >
          <div
            className={cn(
              "p-1.5 rounded-lg bg-white dark:bg-slate-900 shadow-sm",
              config.color
            )}
          >
            <Icon className="w-3.5 h-3.5" />
          </div>
          <div className="flex-1 min-w-0">
            <span className={cn("text-sm font-medium", config.color)}>
              {config.label}
            </span>
            <span className="text-sm text-slate-500 dark:text-slate-400 ml-2">
              {change.rule_key}
            </span>
            <span className="text-xs text-slate-400 ml-2">({change.rule_category})</span>
          </div>
          <Badge variant={severityBadge[change.severity] ?? "secondary"}>
            {change.severity.toLowerCase()} impact
          </Badge>
        </div>

        <div className="p-4 space-y-3">
          {change.human_summary && (
            <p className="text-sm text-slate-700 dark:text-slate-300">
              {change.human_summary}
            </p>
          )}

          {(change.old_condition || change.new_condition) && (
            <div className="grid grid-cols-2 gap-3">
              {change.old_condition && (
                <div className="rounded-lg bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 p-3">
                  <p className="text-xs font-medium text-red-600 dark:text-red-400 mb-1">
                    Previous
                  </p>
                  <code className="text-xs text-red-700 dark:text-red-300">
                    {String(change.old_condition.operator)}{" "}
                    {String(change.old_condition.value)}{" "}
                    {change.old_condition.unit ? String(change.old_condition.unit) : ""}
                  </code>
                </div>
              )}
              {change.new_condition && (
                <div className="rounded-lg bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800 p-3">
                  <p className="text-xs font-medium text-green-600 dark:text-green-400 mb-1">
                    Updated
                  </p>
                  <code className="text-xs text-green-700 dark:text-green-300">
                    {String(change.new_condition.operator)}{" "}
                    {String(change.new_condition.value)}{" "}
                    {change.new_condition.unit ? String(change.new_condition.unit) : ""}
                  </code>
                </div>
              )}
            </div>
          )}

          {(change.old_source_text || change.new_source_text) && (
            <details className="text-xs">
              <summary className="cursor-pointer text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 flex items-center gap-1">
                <FileText className="w-3 h-3" />
                Source text
                {change.old_source_page ? ` (page ${change.old_source_page})` : ""}
              </summary>
              <div className="mt-2 p-2 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 font-mono leading-relaxed">
                {change.old_source_text || change.new_source_text}
              </div>
            </details>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
