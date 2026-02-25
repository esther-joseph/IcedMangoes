interface PageLayoutProps {
  children: React.ReactNode;
  maxWidth?: "sm" | "md" | "lg" | "xl" | "2xl";
  className?: string;
}

const maxWidthClasses = {
  sm: "max-w-2xl",
  md: "max-w-4xl",
  lg: "max-w-6xl",
  xl: "max-w-7xl",
  "2xl": "max-w-[90rem]",
};

export function PageLayout({
  children,
  maxWidth = "lg",
  className = "",
}: PageLayoutProps) {
  return (
    <div
      className={`mx-auto w-full px-4 py-12 ${maxWidthClasses[maxWidth]} ${className}`.trim()}
    >
      {children}
    </div>
  );
}
