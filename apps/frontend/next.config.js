// next.config.js
const withMDX = require("@next/mdx")({
  extension: /\.mdx?$/,
  options: {
    // optional: remarkPlugins, rehypePlugins 등
  },
});

/** @type {import('next').NextConfig} */
const baseConfig = {
  pageExtensions: ["ts", "tsx", "md", "mdx"],
  output: "export",
  images: {
    unoptimized: true,
  },
  turbopack: {
    rules: {
      "*.svg": ["@svgr/webpack"], // SVG만 명시적으로 설정
    },
  },
};

module.exports = withMDX(baseConfig);
