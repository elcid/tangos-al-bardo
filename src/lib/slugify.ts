export default function slugify(str: string): string {
    return str
        .toLowerCase()
        .normalize('NFD')
        .replace(/\p{Diacritic}/gu, '')
        .replace(/\W+/g, '-')
        .replace(/^-+|-+$/g, '');
}