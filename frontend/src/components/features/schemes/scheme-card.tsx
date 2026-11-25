import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatCurrency, formatDate } from "@/lib/utils";
import { Calendar, IndianRupee, MapPin, ExternalLink } from "lucide-react";
import type { Scheme } from "@/types";

interface SchemeCardProps {
  scheme: Scheme;
  evaluationResult?: "eligible" | "ineligible" | "unknown";
  matchScore?: number;
}

const resultBadge = {
  eligible: { label: "Eligible", variant: "success" as const },
  ineligible: { label: "Not Eligible", variant: "destructive" as const },
  unknown: { label: "Check Eligibility", variant: "secondary" as const },
};

export function SchemeCard({ scheme, evaluationResult, matchScore }: SchemeCardProps) {
  return (
    <Card className="flex flex-col hover:shadow-md transition-shadow">
      <CardContent className="flex flex-col gap-4 p-5">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-slate-900 dark:text-white leading-tight line-clamp-2">
              {scheme.name}
            </h3>
            {scheme.department && (
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 truncate">
                {scheme.department}
              </p>
            )}
          </div>
          {evaluationResult && (
            <Badge variant={resultBadge[evaluationResult].variant} className="shrink-0">
              {resultBadge[evaluationResult].label}
            </Badge>
          )}
        </div>

        {scheme.description && (
          <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-3">
            {scheme.description}
          </p>
        )}

        <div className="flex flex-wrap gap-3 text-xs text-slate-500 dark:text-slate-400">
          {scheme.state && (
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {scheme.state}
            </span>
          )}
          {scheme.latest_amount && (
            <span className="flex items-center gap-1 text-green-600 dark:text-green-400 font-medium">
              <IndianRupee className="w-3 h-3" />
              {formatCurrency(scheme.latest_amount)}
            </span>
          )}
          {scheme.latest_deadline && (
            <span className="flex items-center gap-1 text-amber-600 dark:text-amber-400">
              <Calendar className="w-3 h-3" />
              {formatDate(scheme.latest_deadline)}
            </span>
          )}
        </div>

        <div className="flex flex-wrap gap-1.5">
          <Badge variant="outline">{scheme.scheme_type}</Badge>
          {scheme.education_levels?.slice(0, 2).map((level) => (
            <Badge key={level} variant="secondary">{level.toUpperCase()}</Badge>
          ))}
          {(scheme.education_levels?.length ?? 0) > 2 && (
            <Badge variant="secondary">+{(scheme.education_levels?.length ?? 0) - 2}</Badge>
          )}
        </div>

        {matchScore !== undefined && (
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-slate-500">Match Score</span>
              <span className="font-medium text-slate-700 dark:text-slate-300">{matchScore}%</span>
            </div>
            <div className="h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full gradient-primary rounded-full transition-all"
                style={{ width: matchScore + "%" }}
              />
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Score indicates matched criteria. A mandatory failed criterion overrides this score.
            </p>
          </div>
        )}

        <div className="flex gap-2 mt-auto pt-2">
          <Link href={`/schemes/${scheme.id}`} className="flex-1">
            <Button variant="secondary" size="sm" className="w-full">
              View Details
            </Button>
          </Link>
          {scheme.official_url && (
            <a href={scheme.official_url} target="_blank" rel="noopener noreferrer">
              <Button variant="ghost" size="sm" aria-label="Official site">
                <ExternalLink className="w-4 h-4" />
              </Button>
            </a>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
