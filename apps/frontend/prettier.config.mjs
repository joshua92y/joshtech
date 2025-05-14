// prettier.config.mjs
import * as prettierPluginTailwindcss from "prettier-plugin-tailwindcss";

/** @type {import("prettier").Config} */

const prettierConfig = {
  plugins: [prettierPluginTailwindcss],
  tailwindConfig: "./tailwind.config.ts",
  semi: true,
  singleQuote: false,
  printWidth: 100,
  tabWidth: 2,
  trailingComma: "es5",
};

export default prettierConfig;
