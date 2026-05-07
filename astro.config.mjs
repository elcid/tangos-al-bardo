import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://elcid.github.io',
  base: '/tangos-al-bardo/',
  output: 'static',
  trailingSlash: 'always',

  integrations: [
    sitemap({
      filter: (page) => !page.includes('/tags/'),
      changefreq: 'monthly',
      priority: 0.7,
      lastmod: new Date(),
      serialize(item) {
        if (/\/posts\/\d+\/$/.test(item.url)) {
          return { ...item, changefreq: 'yearly', priority: 0.3 };
        }
        if (/\/posts\/[^/]+\/$/.test(item.url)) {
          return { ...item, changefreq: 'monthly', priority: 0.8 };
        }
        return item;
      },
    }),
  ],

  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },

  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        '@': '/src',
      },
    },
  },
});
