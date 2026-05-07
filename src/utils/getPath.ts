export function getPath(id: string, slug: string): string {
  const base = import.meta.env.BASE_URL || '/';
  return `${base}posts/${slug}/`;
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
