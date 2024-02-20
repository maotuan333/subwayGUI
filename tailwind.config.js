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
      'roboto': ['Roboto', 'sans-serif'],
      'inter': ['Inter', 'sans-serif']
      // Add more custom font families if needed
    },
    extend: {
      colors: {
        'primary-gray': '#2C2C2C',
        'secondary-gray': '#1E1E1E',
        'seperator': '#38383E',
        'ternary-gray': '#1A1A1A'
      }
    },
  },
  plugins: [],
}