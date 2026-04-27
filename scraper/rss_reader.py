import logging
from bs4 import BeautifulSoup

import feedparser


def read_rss(config: dict) -> list[dict]:
    try:
        feed = feedparser.parse(config["url"])
    except Exception as e:
        logging.error(f"RSS parse failed for {config['url']}: {e}")
        return []

    articles = []
    for entry in feed.entries[: config["max_articles"]]:
        url = entry.get("link", "").strip()
        if not url:
            continue

        title = entry.get("title", "").strip()
        if not title:
            continue

        raw = entry.get("summary", entry.get("description", ""))
        # Strip HTML tags from RSS summaries
        if raw:
            raw = BeautifulSoup(raw, "lxml").get_text(" ", strip=True)

        published_at = entry.get("published", entry.get("updated"))

        articles.append(
            {
                "url": url,
                "source_name": config["name"],
                "source_slug": config["slug"],
                "title": title,
                "raw_content": raw[:8000],
                "published_at": published_at,
                "image_url": None,
            }
        )

    return articles
