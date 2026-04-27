import time
import logging
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_site(config: dict) -> list[dict]:
    listing_html = _fetch(config["url"])
    if not listing_html:
        return []

    soup = BeautifulSoup(listing_html, "lxml")
    links = _extract_links(soup, config)

    articles = []
    for url in links[: config["max_articles"]]:
        article = _scrape_article(url, config)
        if article:
            articles.append(article)
        time.sleep(1)

    return articles


def _extract_links(soup: BeautifulSoup, config: dict) -> list[str]:
    base = config.get("base_url", config["url"])
    containers = soup.select(config["article_list_selector"])

    seen: set[str] = set()
    links: list[str] = []

    sources = containers if containers else [soup]
    for container in sources:
        for a in container.select(config["article_link_selector"]):
            href = a.get("href", "").strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full_url = urljoin(base, href)
            # Skip non-http URLs and the listing page itself
            parsed = urlparse(full_url)
            if parsed.scheme not in ("http", "https"):
                continue
            if full_url not in seen:
                seen.add(full_url)
                links.append(full_url)
        if len(links) >= config["max_articles"] * 3:
            break

    return links


def _scrape_article(url: str, config: dict) -> Optional[dict]:
    html = _fetch(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")

    title_el = soup.select_one(config["title_selector"])
    title = title_el.get_text(strip=True) if title_el else None
    if not title:
        return None

    body_els = soup.select(config["body_selector"])
    body = " ".join(el.get_text(" ", strip=True) for el in body_els)[:8000]

    date_el = soup.select_one(config["date_selector"])
    published_at = None
    if date_el:
        attr = config.get("date_attr", "datetime")
        if attr == "text":
            published_at = date_el.get_text(strip=True)
        else:
            published_at = date_el.get(attr) or date_el.get_text(strip=True)

    og_image = None
    og_tag = soup.find("meta", property="og:image")
    if og_tag:
        og_image = og_tag.get("content")

    return {
        "url": url,
        "source_name": config["name"],
        "source_slug": config["slug"],
        "title": title,
        "raw_content": body,
        "published_at": published_at,
        "image_url": og_image,
    }


def _fetch(url: str) -> Optional[str]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code in (403, 429):
            return _fetch_with_cloudscraper(url)
        logging.warning(f"HTTP error fetching {url}: {e}")
        return None
    except Exception as e:
        logging.warning(f"Failed to fetch {url}: {e}")
        return None


def _fetch_with_cloudscraper(url: str) -> Optional[str]:
    try:
        import cloudscraper
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(url, timeout=20)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logging.warning(f"cloudscraper also failed for {url}: {e}")
        return None
