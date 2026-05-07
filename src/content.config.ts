import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: 'src/content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.union([z.string(), z.date()]).transform((v) =>
      typeof v === 'string' ? v : v.toISOString().slice(0, 10)
    ),
    original_url: z.string().optional().default(''),
    labels: z.string().nullable().optional().default(''),
    tags: z.array(z.string()).optional().default([]),
  }),
});

export const collections = { posts };
