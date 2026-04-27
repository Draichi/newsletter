export interface Article {
  id: string;
  url: string;
  source_name: string;
  source_slug: string;
  title: string;
  summary: string | null;
  published_at: string | null;
  scraped_at: string;
  image_url: string | null;
}
