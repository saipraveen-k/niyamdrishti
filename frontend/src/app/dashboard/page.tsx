"use client";
import { useAuth } from "@/hooks/use-auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import Link from "next/link";
import { Search, GitCompare, Map, FileText, Bell, ArrowRight, TrendingUp, Calendar, Award } from "lucide-react";

function WelcomeBanner({ name }: { name: string }) {
  return (
    <div className="rounded-2xl gradient-primary p-6 text-white mb-6">
      <h1 className="text-2xl font-bold">Welcome back, {name.split(" ")[0]}!</h1>
      <p className="text-blue-100 mt-1">Your personalised scholarship intelligence dashboard.</p>
    </div>
  );
}

const quickActions = [
  { href: "/schemes", icon: Search, label: "Discover Schemes", desc: "Find matching scholarships" },
  { href: "/changelens", icon: GitCompare, label: "ChangeLens", desc: "Compare policy versions" },
  { href: "/eligibility", icon: TrendingUp, label: "My Eligibility", desc: "Check your matches" },
  { href: "/lifemap", icon: Map, label: "LifeMap", desc: "My action plan" },
];

export default function DashboardPage() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="p-8 space-y-6">
        <Skeleton className="h-24 w-full" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-28 w-full" />)}
        </div>
      </div>
    );
  }

  const name = user?.user_metadata?.full_name || user?.email || "Student";

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <WelcomeBanner name={name} />

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link key={action.href} href={action.href}>
              <Card className="hover:shadow-md transition-all hover:border-blue-200 dark:hover:border-blue-900 cursor-pointer h-full">
                <CardContent className="p-4 flex flex-col gap-3">
                  <div className="w-9 h-9 rounded-xl gradient-primary flex items-center justify-center">
                    <Icon className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <p className="font-medium text-sm text-slate-900 dark:text-white">{action.label}</p>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{action.desc}</p>
                  </div>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Profile completion */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Complete Your Profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-slate-500 dark:text-slate-400">
              A complete profile enables accurate eligibility evaluation. 
            </p>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Profile completeness</span>
                <span className="font-medium text-slate-700 dark:text-slate-300">0%</span>
              </div>
              <div className="h-2 bg-slate-100 dark:bg-slate-800 rounded-full">
                <div className="h-full w-0 gradient-primary rounded-full" />
              </div>
            </div>
            <Link href="/settings/profile">
              <Button size="sm" className="w-full">Complete profile</Button>
            </Link>
          </CardContent>
        </Card>

        {/* Recent schemes */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-base">Recent Schemes</CardTitle>
            <Link href="/schemes" className="text-xs text-blue-600 dark:text-blue-400 hover:underline">View all</Link>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-4">
                Complete your profile to see personalised recommendations.
              </p>
              <Link href="/schemes">
                <Button variant="secondary" size="sm" className="w-full gap-1">
                  <Search className="w-3 h-3" /> Browse all schemes
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-base">Notifications</CardTitle>
            <Badge variant="secondary">0 new</Badge>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-4">
              Policy change alerts will appear here when schemes you follow are updated.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
