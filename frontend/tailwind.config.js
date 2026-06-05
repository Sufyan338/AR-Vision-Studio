/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: { neon: "#00d4ff", cyber: "#ff00aa" },
      fontFamily: { mono: ["JetBrains Mono", "monospace"] },
    },
  },
  plugins: [],
};
