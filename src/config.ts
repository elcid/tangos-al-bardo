import type { SiteConfig } from "./types";

export const SITE: SiteConfig = {
  website: "https://elcid.github.io/tangos-al-bardo/",
  author: "José María Otero",
  profile: "https://tangosalbardo.blogspot.com/",
  desc: "Blog de tango, música y nostalgia porteña — 2012 a 2026.",
  title: "Tangos al bardo",
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: false,
  postPerIndex: 6,
  postPerPage: 12,
  scheduledPostMargin: 15 * 60 * 1000,
  showArchives: false,
  showBackButton: true,
  editPost: {
    enabled: false,
    text: "Edit page",
    url: "",
  },
  dynamicOgImage: false,
  dir: "ltr",
  lang: "es",
  timezone: "America/Argentina/Buenos_Aires",
};
