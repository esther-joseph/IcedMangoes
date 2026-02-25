interface BadgeProps {
  count: number;
  max?: number;
  className?: string;
}

export function Badge({ count, max = 99, className = "" }: BadgeProps) {
  if (count <= 0) return null;
  const display = count > max ? `${max}+` : count;
  return (
    <span
      className={`flex h-4 min-w-4 items-center justify-center rounded-full bg-[var(--accent)] px-1 text-[10px] font-medium text-white ${className}`.trim()}
      aria-label={`${count} items in cart`}
    >
      {display}
    </span>
  );
}
