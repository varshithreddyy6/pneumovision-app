/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F6F5F2",
        ink: "#1A1A1A",
        mute: "#6B6B6B",
        line: "#E2DFD8",
        stone: "#9A958C",
      },
      fontFamily: {
        serif: ["Newsreader", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        label: "0.18em",
      },
    },
  },
  plugins: [],
};
