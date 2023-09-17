/** @type {import('tailwindcss').Config} */
import withMT from "@material-tailwind/react/utils/withMT";

export default withMT({
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {},

    colors: {
      mainColor: "#2167AE",
      lightBlue: "#2543a3",
      lightGray: "#EBEEEF",
      lightPink: "#F7C8DC",
      lightGreen: "#8FE9C2",
      lightOrange: "#FFD09B",
      grey: "#d3d3d3",
      lightPurple: "#5454c0",
      activeColor: "#7272c5",
      cardBg: "#8f81e6",
      headerBg: "#0F0C36",
    },
  },
  plugins: [],
});
