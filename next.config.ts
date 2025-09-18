import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Short-term: ignore ESLint during build inside Docker to avoid failing
  // the production build on code-format/linting issues. Long-term you
  // should fix/prettify the source files or run format/lint steps before
  // building and commit fixes.
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
