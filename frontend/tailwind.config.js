/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
    "./types/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-charcoal': '#0B0B0E',
        'soft-graphite': '#1A1A1F',
        'royal-gold': '#C9A24D',
        'emerald-green': '#10B981',
        'soft-crimson': '#EF4444',
        'off-white': '#F5F5F7',
      },
      gradientColorStops: {
        'charcoal': '#0B0B0E',
        'graphite': '#1A1A1F',
        'gold': '#C9A24D',
      }
    },
  },
  plugins: [],
}