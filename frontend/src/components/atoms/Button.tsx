import type { ButtonHTMLAttributes } from "react";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  isLoading?: boolean;
  children: React.ReactNode;
}

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    "rounded-lg bg-[var(--accent)] px-4 py-2.5 text-sm font-medium text-white hover:bg-[var(--accent-hover)] disabled:opacity-50",
  secondary:
    "rounded-lg border border-[var(--border)] bg-[var(--card-bg)] px-4 py-2.5 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--border)] disabled:opacity-50",
  ghost:
    "rounded-lg px-4 py-2.5 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--border)] disabled:opacity-50",
  danger:
    "rounded-lg text-sm font-medium text-red-600 hover:underline dark:text-red-400 disabled:opacity-50",
};

export function Button({
  variant = "primary",
  isLoading = false,
  disabled,
  className = "",
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      type="button"
      disabled={disabled || isLoading}
      className={`${variantClasses[variant]} ${className}`.trim()}
      {...props}
    >
      {isLoading ? "Loading..." : children}
    </button>
  );
}
