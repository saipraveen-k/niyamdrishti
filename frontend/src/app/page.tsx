"use client";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/layout/navbar";
import { BookOpen, GitCompare, Map, Shield, Globe, ArrowRight, CheckCircle2, Zap, FileSearch, Users } from "lucide-react";

const features = [
  {
    icon: FileSearch,
    title: "Scholarship Discovery",
    description: "Search thousands of verified scholarships from AP, Telangana, and central schemes with personalised eligibility matching.",
  },
  {
    icon: GitCompare,
    title: "ChangeLens — Policy Intelligence",
    description: "Upload two versions of a government notification. Get a structured side-by-side comparison showing every changed rule with page-level evidence.",
    highlight: true,
  },
  {
    icon: Shield,
    title: "Personalised Impact Engine",
    description: "When a scholarship policy changes, instantly see how YOUR profile is affected. Criterion-by-criterion breakdown with evidence.",
    highlight: true,
  },
  {
    icon: Map,
    title: "LifeMap — Action Planning",
    description: "Get a personalised step-by-step action plan: documents needed, deadlines, alternatives if you became ineligible.",
  },
  {
    icon: Globe,
    title: "Multilingual Support",
    description: "Policy explanations in English, Telugu (తెలుగు), and Hindi (हिंदी). Original source text always preserved separately.",
  },
  {
    icon: CheckCircle2,
    title: "Evidence-Linked AI",
    description: "AI answers are grounded in verified scheme data and original documents — not invented. Every claim links to its source page.",
  },
];

const stats = [
  { label: "Schemes Catalogued", value: "200+" },
  { label: "States Covered", value: "3" },
  { label: "Policy Changes Detected", value: "AI-powered" },
  { label: "Students Served", value: "Free" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      {/* Hero */}
      <section className="flex-1 flex flex-col items-center justify-center px-4 py-24 text-center bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-blue-200 dark:border-blue-900 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm font-medium">
            <Zap className="w-4 h-4" />
            AI-Powered Policy Intelligence for Students
          </div>

          <h1 className="text-5xl sm:text-6xl font-bold tracking-tight leading-tight">
            <span className="text-slate-900 dark:text-white">Don&apos;t just find scholarships.</span>
            <br />
            <span className="gradient-primary-text">Understand when they change.</span>
          </h1>

          <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
            NiyamDrishti discovers government scholarships and scholarships for you — and when eligibility criteria, amounts, or deadlines change, it tells you exactly what changed, why it matters to you, and what to do next.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="gap-2">
                Get started free
                <ArrowRight className="w-5 h-5" />
              </Button>
            </Link>
            <Link href="/schemes">
              <Button size="lg" variant="secondary">
                Browse schemes
              </Button>
            </Link>
          </div>

          <p className="text-sm text-slate-500 dark:text-slate-500">
            Andhra Pradesh · Telangana · Central Government schemes
          </p>
        </div>
      </section>

      {/* Stats */}
      <section className="border-y border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-12">
        <div className="max-w-6xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="text-3xl font-bold gradient-primary-text">{stat.value}</p>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="py-24 px-4 bg-slate-50 dark:bg-slate-950">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">
              Everything students need. Nothing they don&apos;t.
            </h2>
            <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              NiyamDrishti is not another scholarship listing website. It is a policy intelligence platform.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <div
                  key={feature.title}
                  className={`rounded-2xl p-6 border ${feature.highlight ? "border-blue-200 dark:border-blue-900 bg-blue-50/50 dark:bg-blue-900/10" : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"}`}
                >
                  <div className={`w-10 h-10 rounded-xl mb-4 flex items-center justify-center ${feature.highlight ? "gradient-primary" : "bg-slate-100 dark:bg-slate-800"}`}>
                    <Icon className={`w-5 h-5 ${feature.highlight ? "text-white" : "text-slate-600 dark:text-slate-400"}`} />
                  </div>
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-2">{feature.title}</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Differentiator callout */}
      <section className="py-24 px-4 bg-white dark:bg-slate-900">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white">
            &ldquo;We don&apos;t just help students discover opportunities. We help them understand when those opportunities change — and what those changes mean for them.&rdquo;
          </h2>
          <p className="text-slate-500 dark:text-slate-400 text-sm">— NiyamDrishti Product Philosophy</p>
          <Link href="/register">
            <Button size="lg" className="mt-4 gap-2">
              Start discovering <ArrowRight className="w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 py-8 px-4">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-500 dark:text-slate-400">
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            <span>NiyamDrishti — Policy Intelligence for Students</span>
          </div>
          <div className="flex gap-6">
            <Link href="/about" className="hover:text-slate-700 dark:hover:text-slate-300">About</Link>
            <Link href="/privacy" className="hover:text-slate-700 dark:hover:text-slate-300">Privacy</Link>
            <Link href="/terms" className="hover:text-slate-700 dark:hover:text-slate-300">Terms</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
