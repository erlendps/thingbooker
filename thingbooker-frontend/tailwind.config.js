/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'willow-grove': {
          DEFAULT: '#607466',
          dark: '#3a4b3f',
          50: '#f6f7f6',
          100: '#e1e6e2',
          200: '#c2cdc5',
          300: '#9caca1',
          400: '#778a7d',
          500: '#607466',
          600: '#49584e',
          700: '#3c4940',
          800: '#333c36',
          900: '#2d342f',
          950: '#171c19'
        },
        whisper: {
          DEFAULT: '#fdfdfd',
          dark: '#cfcfcf'
        },
        'solid-pink': {
          DEFAULT: '#772f3d',
          dark: '#602531',
          50: '#fcf4f4',
          100: '#f9eaea',
          200: '#f3d8d9',
          300: '#e9b8ba',
          400: '#dc9095',
          500: '#cb6871',
          600: '#b44a58',
          700: '#973948',
          800: '#772f3d',
          900: '#602531',
          950: '#3c151d'
        },
        marshland: {
          DEFAULT: '#161817',
          dark: '#111211',
          50: '#f6f7f7',
          100: '#e2e5e3',
          200: '#c5cac7',
          300: '#a0a8a2',
          400: '#7c8580',
          500: '#626a65',
          600: '#4d5450',
          700: '#404543',
          800: '#363938',
          900: '#2f3231',
          950: '#161817',
          1000: '#111211'
        },
        tropaz: {
          DEFAULT: '#3e5889',
          dark: '#2f4367',
          50: '#f5f6fa',
          100: '#e9ecf5',
          200: '#cfd8e8',
          300: '#a4b6d5',
          400: '#738fbd',
          500: '#5170a6',
          600: '#3e5889',
          700: '#344870',
          800: '#2e3e5e',
          900: '#2a3650',
          950: '#1c2335'
        }
      }
    },
    fontFamily: {
      sans: '"Nunito", ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
      serif: 'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
      mono: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace'
    }
  },
  plugins: []
};
