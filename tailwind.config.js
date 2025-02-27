// @ts-check
import { join } from "path";

// 1. Import the Skeleton plugin
import { skeleton } from "@skeletonlabs/tw-plugin";

import { myCustomTheme } from "./my-custom-theme";

import forms from '@tailwindcss/forms';


/** @type {import('tailwindcss').Config} */
export default {
  // 2. Opt for dark mode to be handled via the class method
  darkMode: "selector",
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    // 3. Append the path to the Skeleton package
    join(
      require.resolve("@skeletonlabs/skeleton"),
      "../**/*.{html,js,svelte,ts}"
    ),
  ],
  plugins: [
    skeleton({
      themes: {
        custom: [
          myCustomTheme
        ]
      }
    })
  ]
};
