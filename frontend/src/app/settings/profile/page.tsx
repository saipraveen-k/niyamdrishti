"use client";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import apiClient from "@/lib/api-client";
import toast from "react-hot-toast";
import type { StudentProfile } from "@/types";

const STATES = [
  "Andhra Pradesh",
  "Telangana",
  "Karnataka",
  "Tamil Nadu",
  "Maharashtra",
  "Other",
];
const EDU_LEVELS = ["10th", "12th", "ug", "pg", "phd"];
const CATEGORIES = ["GEN", "OBC", "SC", "ST", "EWS"];

export default function ProfilePage() {
  const [profile, setProfile] = useState<Partial<StudentProfile>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [exists, setExists] = useState(false);

  useEffect(() => {
    apiClient
      .get<StudentProfile>("/profiles/me")
      .then((r) => {
        setProfile(r.data);
        setExists(true);
      })
      .catch((err) => {
        if (err?.response?.status !== 404) toast.error("Could not load profile");
      })
      .finally(() => setLoading(false));
  }, []);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    try {
      if (exists) {
        await apiClient.patch("/profiles/me", profile);
      } else {
        await apiClient.post("/profiles", profile);
        setExists(true);
      }
      toast.success("Profile saved!");
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || "Save failed");
    } finally {
      setSaving(false);
    }
  }

  function set<K extends keyof StudentProfile>(key: K, value: StudentProfile[K]) {
    setProfile((prev) => ({ ...prev, [key]: value }));
  }

  if (loading)
    return <div className="p-8 text-center text-slate-500">Loading profile…</div>;

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Student Profile</h1>
        <p className="text-slate-500 dark:text-slate-400 mt-1">
          Complete your profile for accurate eligibility evaluation.
        </p>
      </div>

      <div className="rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 p-4 text-sm text-blue-700 dark:text-blue-300">
        Your profile data is used only for eligibility evaluation.
        We do not collect Aadhaar numbers or bank details.
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Education</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Education Level
              </label>
              <select
                value={profile.education_level || ""}
                onChange={(e) => set("education_level", e.target.value)}
                className="flex h-10 w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
              >
                <option value="">Select level</option>
                {EDU_LEVELS.map((l) => (
                  <option key={l} value={l}>
                    {l.toUpperCase()}
                  </option>
                ))}
              </select>
            </div>
            <Input
              label="Course Name"
              value={profile.course_name || ""}
              onChange={(e) => set("course_name", e.target.value)}
              placeholder="B.Tech, B.Com, etc."
            />
            <Input
              label="College Name"
              value={profile.college_name || ""}
              onChange={(e) => set("college_name", e.target.value)}
              placeholder="Name of your college"
            />
            <Input
              label="Current Year / Semester"
              value={profile.current_year_semester || ""}
              onChange={(e) => set("current_year_semester", e.target.value)}
              placeholder="2nd Year / 3rd Semester"
            />
            <Input
              label="Marks %"
              type="number"
              min={0}
              max={100}
              step={0.01}
              value={profile.marks_percentage?.toString() || ""}
              onChange={(e) => set("marks_percentage", parseFloat(e.target.value))}
              placeholder="e.g. 78.5"
            />
            <Input
              label="CGPA"
              type="number"
              min={0}
              max={10}
              step={0.01}
              value={profile.cgpa?.toString() || ""}
              onChange={(e) => set("cgpa", parseFloat(e.target.value))}
              placeholder="e.g. 8.2"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Location &amp; Domicile</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
                State
              </label>
              <select
                value={profile.state || ""}
                onChange={(e) => set("state", e.target.value)}
                className="flex h-10 w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
              >
                <option value="">Select state</option>
                {STATES.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>
            <Input
              label="District"
              value={profile.district || ""}
              onChange={(e) => set("district", e.target.value)}
              placeholder="Your district"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Economic Information</CardTitle>
            <CardDescription>
              Used only to evaluate income-based eligibility criteria. User-declared; not verified.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Input
              label="Annual Family Income (₹)"
              type="number"
              min={0}
              value={profile.annual_family_income?.toString() || ""}
              onChange={(e) =>
                set("annual_family_income", parseInt(e.target.value))
              }
              placeholder="e.g. 200000"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Category (Optional)</CardTitle>
            <CardDescription>
              Some schemes have category-specific eligibility. Provide only if relevant.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Caste Category
              </label>
              <select
                value={profile.caste_category || ""}
                onChange={(e) => set("caste_category", e.target.value)}
                className="flex h-10 w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
              >
                <option value="">Prefer not to say</option>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="is_pwd"
                checked={profile.is_pwd || false}
                onChange={(e) => set("is_pwd", e.target.checked)}
                className="w-4 h-4 rounded border-slate-300"
              />
              <label
                htmlFor="is_pwd"
                className="text-sm text-slate-700 dark:text-slate-300"
              >
                Person with Disability (PwD)
              </label>
            </div>
          </CardContent>
        </Card>

        <Button type="submit" loading={saving} size="lg" className="w-full">
          Save Profile
        </Button>
      </form>
    </div>
  );
}
