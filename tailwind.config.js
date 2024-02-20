/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    fontFamily: {
      'lato': ['Lato', 'sans-serif'],
      'open-sans': ['Open Sans', 'sans-serif'],
      'outfit': ['Outfit', 'sans-serif'],
      'arvo': ['Arvo', 'serif'],
      'roboto': ['Roboto', 'sans-serif']
      // Add more custom font families if needed
    },
    extend: {
      colors: {
        'primary-gray': '#2B2B30',
        'secondary-gray': '#1E1E1E',
        'seperator': '#38383E',
        'ternary-gray': '#323233'
      }
    },
  },
  plugins: [],
}