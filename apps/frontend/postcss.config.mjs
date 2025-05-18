// frontend/postcss.config.mjs
const config = {
  plugins: {
    "@csstools/postcss-global-data": {
      files: ["src/once-ui/styles/breakpoints.scss"],
    },
    "postcss-custom-media": {},
    "postcss-flexbugs-fixes": {},
    "postcss-preset-env": {
      stage: 3,
      autoprefixer: {
        flexbox: "no-2009",
      },
      features: {
        "custom-properties": false,
      },
    },
    "@tailwindcss/postcss": {},
    autoprefixer: {},
  },
};
export default config;
