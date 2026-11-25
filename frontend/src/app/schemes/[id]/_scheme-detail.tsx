"use client";
import { useScheme } from "@/hooks/use-schemes";
import { Navbar } from "@/components/layout/navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { formatCurrency, formatDate } from "@/lib/utils";
import Link from "next/link";
import {
  Calendar,
  IndianRupee,
  MapPin,
  ExternalLink,
  ArrowLeft,
  FileCheck,
  Bookmark,
} from "lucide-react";
import apiClient from "@/lib/api-client";
import toast from "react-hot-toast";

export default function SchemeDetailContent({ id }: { id: string }) {
  const { scheme, loading, error } = useScheme(id);

  async function handleBookmark() {
    try {
      await apiClient.post(`/schemes/${id}/bookmark`);
      toast.success("Bookmark toggled");
    } catch {
      toast.error("Please log in to bookmark");
    }
  }

  if (loading)
    return (
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <div className="max-w-4xl mx-auto w-full px-4 py-8 space-y-4">
          <Skeleton className="h-8 w-2/3" />
          <Skeleton className="h-4 w-1/3" />
          <Skeleton className="h-32 w-full" />
        </div>
      </div>
    );

  if (error || !scheme)
    return (
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <div className="max-w-4xl mx-auto w-full px-4 py-16 text-center space-y-4">
          <p className="text-slate-500">Scheme not found or could not be loaded.</p>
          <Link href="/schemes">
            <Button variant="secondary">Back to Schemes</Button>
          </Link>
        </div>
      </div>
    );

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      <Navbar />
      <div className="max-w-4xl mx-auto w-full px-4 py-8 space-y-6">
        <Link
          href="/schemes"
          className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700 dark:hover:text-slate-300"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Schemes
        </Link>

        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 space-y-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                {scheme.name}
              </h1>
              {scheme.department && (
                <p className="text-slate-500 dark:text-slate-400 mt-1">
                  {scheme.department}
                </p>
              )}
            </div>
            <div className="flex gap-2 shrink-0">
              <Button variant="ghost" size="sm" onClick={handleBookmark} className="gap-1.5">
                <Bookmark className="w-4 h-4" /> Save
              </Button>
              {scheme.official_url && (
                <a href={scheme.official_url} target="_blank" rel="noopener noreferrer">
                  <Button variant="outline" size="sm" className="gap-1.5">
                    <ExternalLink className="w-4 h-4" /> Official Site
                  </Button>
                </a>
              )}
            </div>
          </div>

          <div className="flex flex-wrap gap-4 text-sm">
            {scheme.state && (
              <span className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
                <MapPin className="w-4 h-4" />
                {scheme.state}
              </span>
            )}
            {scheme.latest_amount && (
              <span className="flex items-center gap-1.5 text-green-600 dark:text-green-400 font-medium">
                <IndianRupee className="w-4 h-4" />
                {formatCurrency(scheme.latest_amount)}
              </span>
            )}
            {scheme.latest_deadline && (
              <span className="flex items-center gap-1.5 text-amber-600 dark:text-amber-400">
                <Calendar className="w-4 h-4" />
                Deadline: {formatDate(scheme.latest_deadline)}
              </span>
            )}
          </div>

          <div className="flex flex-wrap gap-2">
            <Badge variant="outline">{scheme.scheme_type}</Badge>
            {scheme.education_levels?.map((l) => (
              <Badge key={l} variant="secondary">
                {l.toUpperCase()}
              </Badge>
            ))}
            {scheme.eligible_categories?.map((c) => (
              <Badge key={c} variant="secondary">
                {c}
              </Badge>
            ))}
          </div>

          {scheme.description && (
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              {scheme.description}
            </p>
          )}
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          <Card>
            <CardContent className="p-5 space-y-3">
              <h3 className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                <FileCheck className="w-4 h-4" /> Check Eligibility
              </h3>
              <p className="text-sm text-slate-500">
                See if you meet the criteria based on your profile.
              </p>
              <Link href={`/eligibility?scheme_id=${scheme.id}`}>
                <Button className="w-full">Check My Eligibility</Button>
              </Link>
            </CardContent>
          </Card>
          {scheme.application_url && (
            <Card>
              <CardContent className="p-5 space-y-3">
                <h3 className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                  <ExternalLink className="w-4 h-4" /> Apply
                </h3>
                <p className="text-sm text-slate-500">
                  Visit the official application portal.
                </p>
                <a
                  href={scheme.application_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block"
                >
                  <Button variant="secondary" className="w-full">
                    Go to Application Portal
                  </Button>
                </a>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
