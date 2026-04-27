import logging
from datetime import datetime, timezone
from typing import Optional

from dateutil import parser as dateparser
from supabase import Client, create_client


def get_client(url: str, key: str) -> Client:
    return create_client(url, key)


def get_existing_urls(client: Client) -> set[str]:
    result = (
        client.table("articles")
        .select("url")
        .not_.is_("summary", "null")
        .execute()
    )
    return {row["url"] for row in result.data}


def upsert_articles(client: Client, articles: list[dict]) -> int:
    now = datetime.now(timezone.utc).isoformat()
    count = 0

    for article in articles:
        payload: dict = {
            "url": article["url"],
            "source_name": article["source_name"],
            "source_slug": article["source_slug"],
            "title": article["title"],
            "scraped_at": now,
        }

        if article.get("summary"):
            payload["summary"] = article["summary"]
            payload["summarized_at"] = now

        if article.get("published_at"):
            normalized = _normalize_date(article["published_at"])
            if normalized:
                payload["published_at"] = normalized

        if article.get("raw_content"):
            payload["raw_content"] = article["raw_content"]

        if article.get("image_url"):
            payload["image_url"] = article["image_url"]

        try:
            client.table("articles").upsert(payload, on_conflict="url").execute()
            count += 1
        except Exception as e:
            logging.error(f"Upsert failed for {article['url']}: {e}")

    return count


def cleanup_old_raw_content(client: Client) -> None:
    try:
        client.rpc(
            "cleanup_raw_content",
            {},
        ).execute()
    except Exception:
        pass


def _normalize_date(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    try:
        dt = dateparser.parse(date_str, fuzzy=True)
        return dt.isoformat() if dt else None
    except Exception:
        return None
