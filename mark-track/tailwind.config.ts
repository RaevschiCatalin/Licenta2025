import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primaryGreen: '#4CAF50',
        secondaryYellow: '#F5C200',
        neutralDark: '#2E2E2E',
        neutralLight: '#F2F2F2',
        accentBlue: '#4A90E2',
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
    screens: {
      xs: "375px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
    },
  },
  plugins: [require("rippleui")],
};
export default config;
