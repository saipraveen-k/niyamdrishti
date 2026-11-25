// Core domain types

export type AppRole =
  | "student"
  | "college_coordinator"
  | "document_reviewer"
  | "admin"
  | "super_admin";

export type Language = "en" | "te" | "hi";

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  app_role: AppRole;
  preferred_language: Language;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface StudentProfile {
  id: string;
  user_id: string;
  date_of_birth?: string;
  gender?: string;
  state?: string;
  district?: string;
  caste_category?: string;
  is_pwd?: boolean;
  education_level?: string;
  course_name?: string;
  college_name?: string;
  current_year_semester?: string;
  marks_percentage?: number;
  cgpa?: number;
  annual_family_income?: number;
  domicile_state?: string;
  profile_completeness: number;
}

export interface Scheme {
  id: string;
  name: string;
  slug: string;
  description?: string;
  department?: string;
  state: string;
  scheme_type: string;
  education_levels?: string[];
  eligible_categories?: string[];
  latest_amount?: number;
  latest_deadline?: string;
  official_url?: string;
  application_url?: string;
  is_active: boolean;
  is_published: boolean;
  created_at: string;
}

export interface SchemeListResponse {
  items: Scheme[];
  total: number;
  page: number;
  per_page: number;
  has_next: boolean;
}

export type EligibilityResult = "PASSED" | "FAILED" | "UNKNOWN" | "NEEDS_VERIFICATION";

export interface CriterionResult {
  rule_id: string;
  rule_category: string;
  rule_key: string;
  result: EligibilityResult;
  is_mandatory: boolean;
  student_value?: unknown;
  required_condition: Record<string, unknown>;
  explanation: string;
  source_page?: number;
  source_text?: string;
  confidence?: number;
}

export interface EligibilityEvaluationResponse {
  scheme_id: string;
  scheme_name: string;
  overall_result: EligibilityResult;
  match_score: number;
  criterion_results: CriterionResult[];
  /** Alias for criterion_results — used by UI components */
  criteria: CriterionResult[];
  missing_fields: string[];
  unknown_rules: string[];
  passed_mandatory: number;
  failed_mandatory: number;
  total_mandatory: number;
  is_simulation: boolean;
  evaluation_id?: string;
  disclaimer: string;
}

/** Convenience alias used by page components */
export type EvaluationReport = EligibilityEvaluationResponse;

export interface PolicyChangeEvent {
  id: string;
  change_type: "ADDED" | "REMOVED" | "MODIFIED";
  rule_category: string;
  rule_key: string;
  old_condition?: Record<string, unknown>;
  new_condition?: Record<string, unknown>;
  old_source_text?: string;
  new_source_text?: string;
  old_source_page?: number;
  new_source_page?: number;
  severity: "HIGH" | "MEDIUM" | "LOW";
  human_summary?: string;
}

export interface PolicyComparisonResponse {
  comparison_id: string;
  scheme_id: string;
  old_version_id: string;
  new_version_id: string;
  total_changes: number;
  high_severity: number;
  medium_severity: number;
  low_severity: number;
  changes: PolicyChangeEvent[];
}

export interface ActionPlan {
  id: string;
  scheme_id: string;
  status: string;
  tasks: ActionTask[];
}

export interface ActionTask {
  id: string;
  task_type: string;
  title: string;
  description?: string;
  order_index: number;
  due_date?: string;
  is_completed: boolean;
}

export interface StudentApplication {
  id: string;
  scheme_id: string;
  status: string;
  applied_at?: string;
  notes?: string;
}

export interface ApiError {
  detail: string;
  status?: number;
}
