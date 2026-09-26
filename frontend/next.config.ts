import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/research",
        destination: "http://127.0.0.1:8000/research",
      },
    ];
  },
};

export default nextConfig;