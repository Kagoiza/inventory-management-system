/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ictaRed: '#b21e27',     // Use for alerts only
        ictaDark: '#1b1b1b',    // Sidebar & text
        ictaGray: '#f2f2f2',    // Backgrounds
        ictaGreen: '#006644',   // Accent color
      },
    },
  },
  plugins: [],
};
