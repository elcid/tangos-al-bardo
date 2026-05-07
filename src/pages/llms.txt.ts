import { getCollection } from "astro:content";
import { getSortedPosts } from "@/utils/posts";
import { SITE } from "@/config";

export async function GET() {
  const posts = await getCollection("posts");
  const sorted = getSortedPosts(posts).slice(0, 30);

  const lines = [
    `# ${SITE.title}`,
    "",
    `> ${SITE.desc}`,
    "",
    "## Informacion",
    "",
    `- **Autor**: ${SITE.author}`,
    "- **Idioma**: es",
    `- **URL**: ${SITE.website}`,
    `- **Articulos**: ${sorted.length}`,
    "- **Creadores etiquetados**: disponible en /tags/",
    "",
    "## Articulos recientes",
    "",
    ...sorted.map(
      (p) => `- [${p.data.title}](https://elcid.github.io/tangos-al-bardo/posts/${p.slug}/) (${p.data.date})`
    ),
    "",
    "## Opcional",
    "",
    `- RSS: ${SITE.website}rss.xml`,
    `- Sitemap: ${SITE.website}sitemap-index.xml`,
  ];

  return new Response(lines.join("\n"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
