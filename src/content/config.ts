import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  schema: z.object({
    title: z.string(),
    date: z.union([z.string(), z.date()]).transform((v) =>
      typeof v === 'string' ? v : v.toISOString().slice(0, 10)
    ),
    original_url: z.string().optional().default(''),
    labels: z.string().nullable().optional().default(''),
  }),
});

export const collections = { posts };
