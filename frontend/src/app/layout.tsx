import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "NiyamDrishti — Scholarship & Policy Intelligence",
    template: "%s | NiyamDrishti",
  },
  description:
    "AI-powered platform helping students discover scholarships, understand policy changes, and take personalised action. Serving Andhra Pradesh, Telangana, and India.",
  keywords: [
    "scholarships India",
    "AP scholarships",
    "Telangana scholarships",
    "government schemes students",
    "policy intelligence",
    "eligibility checker",
  ],
  authors: [{ name: "NiyamDrishti Team" }],
  openGraph: {
    title: "NiyamDrishti — Scholarship & Policy Intelligence",
    description:
      "Discover scholarships. Understand policy changes. Take personalised action.",
    type: "website",
    locale: "en_IN",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0f1e" },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full`}
    >
      <body className="min-h-full flex flex-col">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
