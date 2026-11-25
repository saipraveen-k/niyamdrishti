"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/use-auth";
import { cn } from "@/lib/utils";
import {
  BookOpen, LayoutDashboard, Search, GitCompare, Map, FileText,
  MessageSquare, Bell, Settings, Shield, Users, FileCheck, Building2
} from "lucide-react";

interface NavItem {
  href: string;
  label: string;
  icon: React.ElementType;
  roles?: string[];
}

const navItems: NavItem[] = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/schemes", label: "Discover Schemes", icon: Search },
  { href: "/eligibility", label: "My Eligibility", icon: FileCheck, roles: ["student"] },
  { href: "/changelens", label: "ChangeLens", icon: GitCompare },
  { href: "/lifemap", label: "LifeMap", icon: Map, roles: ["student"] },
  { href: "/applications", label: "Applications", icon: FileText, roles: ["student"] },
  { href: "/assistant", label: "AI Assistant", icon: MessageSquare },
  { href: "/notifications", label: "Notifications", icon: Bell },
  { href: "/admin", label: "Admin Panel", icon: Shield, roles: ["admin", "super_admin"] },
  { href: "/reviewer", label: "Review Queue", icon: FileCheck, roles: ["document_reviewer", "admin", "super_admin"] },
  { href: "/coordinator", label: "College Coordinator", icon: Building2, roles: ["college_coordinator", "admin", "super_admin"] },
  { href: "/admin/users", label: "User Management", icon: Users, roles: ["super_admin"] },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { appRole } = useAuth();

  const visibleItems = navItems.filter(
    (item) => !item.roles || (appRole && item.roles.includes(appRole))
  );

  return (
    <aside className="w-64 h-full border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 flex flex-col">
      <div className="p-4 border-b border-slate-200 dark:border-slate-800">
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <div className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center">
            <BookOpen className="w-3.5 h-3.5 text-white" />
          </div>
          <span className="gradient-primary-text">NiyamDrishti</span>
        </Link>
      </div>

      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {visibleItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-xl text-sm font-medium transition-colors",
                isActive
                  ? "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
                  : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white"
              )}
            >
              <Icon className="w-4 h-4 shrink-0" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
