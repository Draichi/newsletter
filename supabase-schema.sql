-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS articles (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url           TEXT NOT NULL UNIQUE,
  source_name   TEXT NOT NULL,
  source_slug   TEXT NOT NULL,
  title         TEXT NOT NULL,
  summary       TEXT,
  published_at  TIMESTAMPTZ,
  scraped_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  summarized_at TIMESTAMPTZ,
  raw_content   TEXT,
  is_featured   BOOLEAN DEFAULT FALSE,
  image_url     TEXT
);

CREATE INDEX IF NOT EXISTS idx_articles_scraped_at   ON articles (scraped_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_source_slug  ON articles (source_slug);
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles (published_at DESC NULLS LAST);

-- Row Level Security: allow public read of summarized articles
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read access"
  ON articles
  FOR SELECT
  TO anon
  USING (summary IS NOT NULL);

-- Weekly cleanup function: null out raw_content older than 30 days
CREATE OR REPLACE FUNCTION cleanup_raw_content()
RETURNS void
LANGUAGE sql
AS $$
  UPDATE articles
  SET raw_content = NULL
  WHERE scraped_at < NOW() - INTERVAL '30 days'
    AND raw_content IS NOT NULL;
$$;
