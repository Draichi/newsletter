import logging
import os

from config import SITE_CONFIGS
from db import get_client, get_existing_urls, upsert_articles
from rss_reader import read_rss
from scraper import scrape_site
from summarizer import configure_gemini, summarize_articles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def main() -> None:
    gemini_key = os.environ["GEMINI_API_KEY"]
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_ANON_KEY"]

    configure_gemini(gemini_key)
    db = get_client(supabase_url, supabase_key)
    existing_urls = get_existing_urls(db)
    logging.info(f"Already summarized: {len(existing_urls)} URLs")

    all_articles: list[dict] = []

    for config in SITE_CONFIGS:
        logging.info(f"Scraping: {config['name']}")
        try:
            if config["type"] == "rss":
                raw = read_rss(config)
            else:
                raw = scrape_site(config)
        except Exception as e:
            logging.error(f"Source {config['name']} failed: {e}")
            raw = []

        new = [a for a in raw if a["url"] not in existing_urls]
        logging.info(f"  {config['name']}: {len(raw)} scraped, {len(new)} new")
        all_articles.extend(new)

    logging.info(f"Total new articles to summarize: {len(all_articles)}")

    if all_articles:
        all_articles = summarize_articles(all_articles)
        count = upsert_articles(db, all_articles)
        logging.info(f"Upserted {count} articles to Supabase")
    else:
        logging.info("No new articles found")


if __name__ == "__main__":
    main()
