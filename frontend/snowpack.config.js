/** @type {import("snowpack").SnowpackUserConfig } */
module.exports = {
  mount: {
    public: "/",

    src: "/_dist_",
  },
  plugins: ["@snowpack/plugin-svelte"],
  install: [
    /* ... */
  ],
  installOptions: {
    rollup: {
      plugins: [
        require("rollup-plugin-svelte")({
          include: ["./node_modules"],
        }),
        require("rollup-plugin-postcss")({
          use: [
            [
              "sass",
              {
                includePaths: ["./src/theme", "./node_modules"],
              },
            ],
          ],
        }),
      ],
    },
  },
  devOptions: {
    /* ... */
  },
  buildOptions: {
    /* ... */
  },
  proxy: {
    /* ... */
  },
  alias: {
    /* ... */
  },
};
