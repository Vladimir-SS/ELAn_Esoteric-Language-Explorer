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