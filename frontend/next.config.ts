import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Silence lockfile warning when frontend is in monorepo
  turbopack: { root: process.cwd() },
};

export default nextConfig;
