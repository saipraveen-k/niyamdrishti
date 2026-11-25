"use client";
import { useState } from "react";
import { SchemeCard } from "@/components/features/schemes/scheme-card";
import { SchemeCardSkeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/layout/navbar";
import { useSchemes } from "@/hooks/use-schemes";
import { Search, Filter, RefreshCw } from "lucide-react";

const STATES = ["Andhra Pradesh", "Telangana", "Central"];
const EDUCATION_LEVELS = ["10th", "12th", "UG", "PG", "PhD"];
const SCHEME_TYPES = ["scholarship", "fellowship", "stipend", "benefit"];

export default function SchemesPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedState, setSelectedState] = useState("");
  const [selectedLevel, setSelectedLevel] = useState("");
  const [selectedType, setSelectedType] = useState("");

  const { data, loading, error, refetch } = useSchemes({
    q: searchQuery || undefined,
    state: selectedState || undefined,
    education_level: selectedLevel ? selectedLevel.toLowerCase() : undefined,
    scheme_type: selectedType || undefined,
  });

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      <Navbar />
      <div className="max-w-7xl mx-auto w-full px-4 py-8 space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Discover Schemes</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            Scholarships, fellowships, and government benefits for students in AP, Telangana, and India.
          </p>
        </div>

        {/* Search & Filters */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search schemes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 h-10 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 transition-colors"
            />
          </div>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="h-10 px-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
          >
            <option value="">All States</option>
            {STATES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="h-10 px-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
          >
            <option value="">All Levels</option>
            {EDUCATION_LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
          </select>
        </div>

        {/* Results */}
        {error ? (
          <div className="text-center py-16 space-y-4">
            <p className="text-slate-500 dark:text-slate-400">Could not load schemes. The backend API may not be running.</p>
            <Button variant="secondary" onClick={refetch} className="gap-2">
              <RefreshCw className="w-4 h-4" /> Try again
            </Button>
            <p className="text-xs text-slate-400">Make sure the backend is running at {process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}</p>
          </div>
        ) : loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => <SchemeCardSkeleton key={i} />)}
          </div>
        ) : data?.items.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-slate-500 dark:text-slate-400">No schemes found matching your filters.</p>
            <Button variant="ghost" className="mt-4" onClick={() => { setSearchQuery(""); setSelectedState(""); setSelectedLevel(""); setSelectedType(""); }}>
              Clear filters
            </Button>
          </div>
        ) : (
          <>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              {data?.total ?? 0} schemes found
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data?.items.map((scheme) => (
                <SchemeCard key={scheme.id} scheme={scheme} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
