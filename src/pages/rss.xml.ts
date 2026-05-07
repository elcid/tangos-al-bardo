import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { getSortedPosts } from '@/utils/posts';
import { SITE } from '@/config';

export async function GET() {
  const posts = await getCollection('posts');
  const sorted = getSortedPosts(posts).slice(0, 100);

  return rss({
    title: SITE.title,
    description: SITE.desc,
    site: SITE.website,
    items: sorted.map((p) => ({
      title: p.data.title,
      description: `${p.data.title} — ${SITE.title}`,
      link: `/posts/${p.slug}/`,
      pubDate: new Date(p.data.date),
      categories: p.data.tags || [],
    })),
    customData: `<language>${SITE.lang}</language>`,
  });
}
