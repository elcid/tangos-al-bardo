export type SiteConfig = {
  website: string;
  author: string;
  profile: string;
  desc: string;
  title: string;
  ogImage?: string;
  lightAndDarkMode: boolean;
  postPerIndex: number;
  postPerPage: number;
  scheduledPostMargin: number;
  showArchives: boolean;
  showBackButton: boolean;
  editPost: {
    enabled: boolean;
    text: string;
    url: string;
  };
  dynamicOgImage: boolean;
  dir: "ltr" | "rtl" | "auto";
  lang: string;
  timezone: string;
};

export type SocialObjects = {
  name: string;
  href: string;
  active: boolean;
  linkTitle: string;
}[];

export type SocialMedia = Record<
  string,
  { href: string; active: boolean; linkTitle: string }
>;
