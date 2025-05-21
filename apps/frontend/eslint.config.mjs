// frontend/eslint.config.mjs
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";
import js from "@eslint/js";
import next from "@next/eslint-plugin-next";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import prettier from "eslint-plugin-prettier";
import globals from "globals";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

export default [
  {
    ignores: [
      "node_modules/**",
      ".next/**",
      "out/**",
      "dist/**",
      "src/components/**", // 컴포넌트 제외
      "src/once-ui/**", // 컴포넌트 제외
    ],
  },
  js.configs.recommended,
  ...compat.extends("next/core-web-vitals", "plugin:prettier/recommended"), //"plugin:@typescript-eslint/recommended",
  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        project: "./tsconfig.json",
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      }, // ✅ Node.js + 브라우저 global 객체 자동 등록
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      prettier: prettier,
      next: next,
    },
    rules: {
      "prettier/prettier": "error",
      "no-unused-vars": "off",
      "no-undef": "off",
    },
  },
];
