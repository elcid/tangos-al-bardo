import type { CollectionEntry } from "astro:content";
import { SITE } from "../config";

const meses = [
  "ene", "feb", "mar", "abr", "may", "jun",
  "jul", "ago", "sep", "oct", "nov", "dic",
] as const;

export function formatDate(date: string): string {
  const [y, m, d] = date.split("-");
  return `${parseInt(d)} ${meses[parseInt(m) - 1]} ${y}`;
}

export function slugifyStr(str: string): string {
  return str
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)+/g, "");
}

export function slugifyAll(arr: string[]): string[] {
  return arr.map(slugifyStr);
}

export function getSortedPosts(
  posts: CollectionEntry<"posts">[]
): CollectionEntry<"posts">[] {
  return posts
    .filter(({ data }) => {
      if (import.meta.env.PROD) {
        const pubDate = new Date(data.date);
        const now = new Date();
        now.setTime(now.getTime() - SITE.scheduledPostMargin);
        return pubDate <= now;
      }
      return true;
    })
    .sort(
      (a, b) =>
        new Date(b.data.date).getTime() - new Date(a.data.date).getTime()
    );
}

export function getPageNumbers(
  totalPosts: number
): { start: number; end: number }[] {
  const perPage = SITE.postPerPage;
  const pages: { start: number; end: number }[] = [];
  for (let i = 0; i < totalPosts; i += perPage) {
    pages.push({ start: i, end: Math.min(i + perPage, totalPosts) });
  }
  return pages;
}
