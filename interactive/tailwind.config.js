/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Category colors
        federation: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
        },
        stadium: {
          50: '#fef3c7',
          500: '#f59e0b',
          600: '#d97706',
        },
        club: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
        },
        toy: {
          50: '#fdf4ff',
          500: '#a855f7',
          600: '#9333ea',
        },
      },
    },
  },
  plugins: [],
}
