export function getPath(id: string, slug: string): string {
  return `/posts/${slug}/`;
}

export function slugifyAllTags(tags: string[]): string[] {
  return tags.map((t) =>
    t
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)+/g, "")
  );
}
