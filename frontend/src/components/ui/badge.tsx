import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "secondary" | "success" | "warning" | "destructive" | "outline";
}

const variantClasses = {
  default: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  secondary: "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200",
  success: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  warning: "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200",
  destructive: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
  outline: "border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300",
};

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variantClasses[variant],
        className
      )}
      {...props}
    />
  );
}
