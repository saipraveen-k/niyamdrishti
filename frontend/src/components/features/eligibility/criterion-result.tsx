import { cn } from "@/lib/utils";
import { CheckCircle2, XCircle, HelpCircle, AlertCircle } from "lucide-react";
import type { CriterionResult as CriterionResultType } from "@/types";

interface CriterionResultProps {
  criterion: CriterionResultType;
}

const resultConfig = {
  PASSED: { icon: CheckCircle2, color: "text-green-600 dark:text-green-400", bg: "bg-green-50 dark:bg-green-900/20", border: "border-green-200 dark:border-green-800" },
  FAILED: { icon: XCircle, color: "text-red-600 dark:text-red-400", bg: "bg-red-50 dark:bg-red-900/20", border: "border-red-200 dark:border-red-800" },
  UNKNOWN: { icon: HelpCircle, color: "text-slate-500 dark:text-slate-400", bg: "bg-slate-50 dark:bg-slate-900/20", border: "border-slate-200 dark:border-slate-700" },
  NEEDS_VERIFICATION: { icon: AlertCircle, color: "text-amber-600 dark:text-amber-400", bg: "bg-amber-50 dark:bg-amber-900/20", border: "border-amber-200 dark:border-amber-800" },
};

export function CriterionResult({ criterion }: CriterionResultProps) {
  const config = resultConfig[criterion.result];
  const Icon = config.icon;

  return (
    <div className={cn("flex items-start gap-3 p-3 rounded-xl border", config.bg, config.border)}>
      <Icon className={cn("w-5 h-5 mt-0.5 shrink-0", config.color)} />
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-sm font-medium text-slate-900 dark:text-white capitalize">
            {criterion.rule_key.replace(/_/g, " ")}
          </span>
          {criterion.is_mandatory && (
            <span className="text-xs text-slate-500">mandatory</span>
          )}
        </div>
        <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">{criterion.explanation}</p>
        {criterion.source_page && (
          <p className="text-xs text-slate-400 mt-1">
            Source: page {criterion.source_page}
            {criterion.confidence ? ` · confidence: ${Math.round(criterion.confidence * 100)}%` : ""}
          </p>
        )}
      </div>
    </div>
  );
}
