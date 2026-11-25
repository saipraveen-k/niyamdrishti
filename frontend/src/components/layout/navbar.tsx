"use client";
import Link from "next/link";
import { useAuth } from "@/hooks/use-auth";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import { Moon, Sun, Menu, X, BookOpen } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const { user, signOut, loading } = useAuth();
  const { theme, setTheme } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-950/80 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center">
              <BookOpen className="w-4 h-4 text-white" />
            </div>
            <span className="gradient-primary-text">NiyamDrishti</span>
          </Link>

          <nav className="hidden md:flex items-center gap-6">
            <Link href="/schemes" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors">
              Schemes
            </Link>
            <Link href="/changelens" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors">
              ChangeLens
            </Link>
            <Link href="/about" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors">
              About
            </Link>
          </nav>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>

            {!loading && (
              user ? (
                <div className="flex items-center gap-2">
                  <Link href="/dashboard">
                    <Button size="sm" variant="secondary">Dashboard</Button>
                  </Link>
                  <Button size="sm" variant="ghost" onClick={signOut}>Sign out</Button>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Link href="/login">
                    <Button size="sm" variant="ghost">Log in</Button>
                  </Link>
                  <Link href="/register">
                    <Button size="sm">Get started</Button>
                  </Link>
                </div>
              )
            )}

            <button
              className="md:hidden p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label="Toggle menu"
            >
              {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {menuOpen && (
          <div className="md:hidden border-t border-slate-200 dark:border-slate-800 py-4 space-y-2">
            <Link href="/schemes" className="block px-2 py-2 text-sm rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800" onClick={() => setMenuOpen(false)}>Schemes</Link>
            <Link href="/changelens" className="block px-2 py-2 text-sm rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800" onClick={() => setMenuOpen(false)}>ChangeLens</Link>
            <Link href="/about" className="block px-2 py-2 text-sm rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800" onClick={() => setMenuOpen(false)}>About</Link>
          </div>
        )}
      </div>
    </header>
  );
}
