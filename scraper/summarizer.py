import json
import logging
import re

from google import genai


def configure_gemini(api_key: str) -> None:
    global _client
    _client = genai.Client(api_key=api_key)


_client: genai.Client | None = None


def summarize_articles(articles: list[dict]) -> list[dict]:
    if not articles:
        return articles

    batch = [
        {
            "index": i,
            "title": a["title"],
            "source": a["source_name"],
            "content": a.get("raw_content", "")[:4000],
        }
        for i, a in enumerate(articles)
    ]

    prompt = f"""You are a professional intelligence analyst summarizing news articles.
For each article below, write a concise 2-3 sentence summary that:
- Captures the key finding, event, or argument
- Is written in plain English for a technical audience
- Does NOT start with "This article" or "The author"

Return ONLY a JSON array with objects containing "index" (integer) and "summary" (string) keys.
No markdown fences, no extra text.

Articles:
{json.dumps(batch, ensure_ascii=False)}
"""

    try:
        response = _client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        text = response.text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        results = json.loads(text)
        summaries = {item["index"]: item["summary"] for item in results}
        for i, article in enumerate(articles):
            article["summary"] = summaries.get(i, _fallback_summary(article))
    except Exception as e:
        logging.error(f"Gemini summarization failed: {e}")
        for article in articles:
            if not article.get("summary"):
                article["summary"] = _fallback_summary(article)

    return articles


def _fallback_summary(article: dict) -> str:
    raw = article.get("raw_content", "")
    if not raw:
        return ""
    return raw[:300].rstrip() + ("..." if len(raw) > 300 else "")
