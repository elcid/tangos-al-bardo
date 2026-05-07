import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://tangosalbardo.blogspot.com',
  output: 'static',
  trailingSlash: 'always',
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
});
