import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        pyrocast: {
          bg: "#0a0e17",
          surface: "#111827",
          border: "#1f2937",
          accent: "#f97316",
          "accent-muted": "#ea580c",
          danger: "#ef4444",
          success: "#22c55e",
          warning: "#eab308",
          muted: "#6b7280",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["var(--font-jetbrains)", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
