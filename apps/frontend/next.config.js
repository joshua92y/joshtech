// apps/frontend/next.config.js

const withMDX = require("@next/mdx")({
  extension: /\.mdx?$/,
  options: {
    // optional: remarkPlugins, rehypePlugins 등
  },
});

/** @type {import('next').NextConfig} */
const baseConfig = {
  pageExtensions: ["ts", "tsx", "md", "mdx"],
  // output: 'export',
  async rewrites() {
    return [
      {
        source: "/og",
        destination: "https://api.joshuatech.dev/og",
      },
    ];
  },
  transpilePackages: ["next-mdx-remote"],
  sassOptions: {
    compiler: "modern",
    silenceDeprecations: ["legacy-js-api"],
  },
  images: {
    unoptimized: true,
  },
  experimental: {
    runtime: "edge", // ✅ Cloudflare Pages + Functions 필수
    appDir: true, // ✅ App Router 사용 시
    serverActions: true, // ✅ 필요 시 활성화
  },
  turbopack: {
    rules: {
      "*.svg": ["@svgr/webpack"], // SVG만 명시적으로 설정
    },
  },
};

module.exports = withMDX(baseConfig);
