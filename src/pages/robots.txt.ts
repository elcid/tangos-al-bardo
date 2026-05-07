export function GET() {
  const siteUrl = "https://elcid.github.io/tangos-al-bardo";
  const body = [
    "User-agent: *",
    "Allow: /",
    "Disallow: /tags/",
    "",
    `Sitemap: ${siteUrl}/sitemap-index.xml`,
    "",
    "# AI agent discovery",
    `Schemamap: ${siteUrl}/schemamap.xml`,
  ].join("\n");

  return new Response(body, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
