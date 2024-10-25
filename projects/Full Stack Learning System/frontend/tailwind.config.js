/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      flex: {
        '4': '4 1 0%',
        '2': '2 1 0%'
      }
    },
  },
  plugins: [],
}

