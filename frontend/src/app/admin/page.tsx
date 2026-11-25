"use client";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shield, Users, FileText, Activity, Database } from "lucide-react";
import apiClient from "@/lib/api-client";
import Link from "next/link";

interface SystemHealth {
  status: string;
  database: string;
  ai: string;
  storage: string;
}

export default function AdminPage() {
  const [health, setHealth] = useState<SystemHealth | null>(null);

  useEffect(() => {
    apiClient
      .get<SystemHealth>("/admin/system-health")
      .then((r) => setHealth(r.data))
      .catch(() => {});
  }, []);

  const sections = [
    {
      href: "/admin/schemes",
      icon: Database,
      label: "Scheme Management",
      desc: "Create, edit, and publish schemes",
    },
    {
      href: "/admin/documents",
      icon: FileText,
      label: "Document Management",
      desc: "Upload and manage official notifications",
    },
    {
      href: "/admin/jobs",
      icon: Activity,
      label: "Processing Jobs",
      desc: "Monitor background document jobs",
    },
    {
      href: "/admin/users",
      icon: Users,
      label: "User Management",
      desc: "Manage users and roles (Super Admin)",
    },
  ];

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
          <Shield className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Admin Dashboard</h1>
          <p className="text-slate-500 dark:text-slate-400">
            Manage schemes, documents, and platform settings.
          </p>
        </div>
      </div>

      {health && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">System Health</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {Object.entries(health).map(([key, val]) => (
                <div key={key} className="flex items-center gap-2">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      ["ok", "connected", "configured"].includes(val)
                        ? "bg-green-500"
                        : "bg-red-500"
                    }`}
                  />
                  <div>
                    <p className="text-xs text-slate-500 capitalize">
                      {key.replace(/_/g, " ")}
                    </p>
                    <p className="text-sm font-medium text-slate-800 dark:text-slate-200 capitalize">
                      {val}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid sm:grid-cols-2 gap-4">
        {sections.map((section) => {
          const Icon = section.icon;
          return (
            <Link key={section.href} href={section.href}>
              <Card className="hover:shadow-md transition-shadow cursor-pointer h-full">
                <CardContent className="p-5 flex gap-4 items-start">
                  <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center shrink-0">
                    <Icon className="w-5 h-5 text-slate-600 dark:text-slate-400" />
                  </div>
                  <div>
                    <p className="font-medium text-slate-900 dark:text-white">
                      {section.label}
                    </p>
                    <p className="text-sm text-slate-500 mt-0.5">{section.desc}</p>
                  </div>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
