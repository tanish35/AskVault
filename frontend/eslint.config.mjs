import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    rules: {
      // TypeScript
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-unused-vars": "off",
      "@typescript-eslint/no-empty-function": "off",
      "@typescript-eslint/no-non-null-assertion": "off",
      "@typescript-eslint/ban-ts-comment": "off",
      "@typescript-eslint/no-inferrable-types": "off",
      "@typescript-eslint/ban-types": "off",

      // React
      "react/no-unescaped-entities": "off",
      "react/prop-types": "off",
      "react/jsx-props-no-spreading": "off",

      // General JS
      "no-console": "off",
      "no-unused-vars": "off",
      "no-empty": "off",
      "no-debugger": "off",

      // JSX
      "react/jsx-no-comment-textnodes": "off",
      "react/react-in-jsx-scope": "off",
    },
  },
];

export default eslintConfig;
