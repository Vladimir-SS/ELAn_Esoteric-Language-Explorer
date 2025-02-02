export type Image = {
    src: string;
    alt?: string;
};

export type Video = {
    src: string;
    title: string;
};

export type Media = {
    type: 'image' | 'video';
    data: Image | Video;
};

export type Esolang = {
    name: string;
    url: string | null;
    alias: string | null;
    yearCreated: number | null;
    designedBy: string | null;
    shortDescription: string | null;
    dimensions: string[] | null;
    memorySystem: string[] | null;
    paradigms: string[] | null;
    influencedBy: string[] | null;
    influenced: string[] | null;
    categories: string[] | null;
    fileExtensions: string[] | null;
    computationalClasses: string[] | null;
    typeSystems: string[] | null;
    dialects: string[] | null;
};