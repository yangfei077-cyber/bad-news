"""Base scraper class and utilities for news fetching."""

from __future__ import annotations

import asyncio
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import feedparser
import httpx
from bs4 import BeautifulSoup

from scraper.config import KEYWORDS_EN, KEYWORDS_ZH, USER_AGENT

logger = logging.getLogger("scraper")


@dataclass
class ScrapedArticle:
    title: str
    url: str
    content: str
    language: str
    excerpt: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    published_at: Optional[datetime] = None
    source_name: str = ""
    tags: list[str] = field(default_factory=list)


def matches_keywords(text: str, language: str) -> bool:
    """Check if text contains any relevant keywords."""
    text_lower = text.lower()
    keywords = KEYWORDS_EN if language == "EN" else KEYWORDS_ZH
    return any(kw.lower() in text_lower for kw in keywords)


def clean_html(html: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class BaseScraper(ABC):
    """Abstract base class for all news source scrapers."""

    name: str = "base"
    language: str = "EN"
    base_url: str = ""
    category: str = "general"

    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
            timeout=30.0,
        )

    async def close(self):
        await self.client.aclose()

    @abstractmethod
    async def fetch_articles(self) -> list[ScrapedArticle]:
        """Fetch and return a list of articles from this source."""
        ...

    async def _get(self, url: str) -> str:
        resp = await self.client.get(url)
        resp.raise_for_status()
        return resp.text

    def _filter_relevant(self, articles: list[ScrapedArticle]) -> list[ScrapedArticle]:
        """Keep only articles matching gender violence keywords."""
        result = []
        for a in articles:
            search_text = f"{a.title} {a.excerpt or ''} {a.content[:500]}"
            if matches_keywords(search_text, a.language):
                result.append(a)
        return result


class RSSMixin:
    """Mixin for scrapers that consume RSS/Atom feeds."""

    async def parse_feed(self: BaseScraper, feed_url: str) -> list[dict]:
        raw = await self._get(feed_url)
        feed = feedparser.parse(raw)
        entries = []
        for entry in feed.entries:
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])

            content = ""
            if hasattr(entry, "content"):
                content = entry.content[0].get("value", "")
            elif hasattr(entry, "summary"):
                content = entry.summary

            image = None
            if hasattr(entry, "media_content"):
                media = entry.media_content
                if media:
                    image = media[0].get("url")

            entries.append({
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "content": content,
                "summary": entry.get("summary", ""),
                "published": published,
                "author": entry.get("author"),
                "image": image,
            })
        return entries


class HTMLScraper:
    """Utility for extracting article content from HTML pages."""

    @staticmethod
    async def extract_article(client: httpx.AsyncClient, url: str) -> dict:
        try:
            from newspaper import Article as NArticle
            article = NArticle(url)
            resp = await client.get(url)
            resp.raise_for_status()
            article.download(input_html=resp.text)
            article.parse()
            return {
                "title": article.title,
                "content": article.text,
                "author": ", ".join(article.authors) if article.authors else None,
                "image": article.top_image,
                "published": article.publish_date,
            }
        except Exception as e:
            logger.warning("Failed to extract %s: %s", url, e)
            return {}


async def run_scrapers(scrapers: list[BaseScraper]) -> list[ScrapedArticle]:
    """Run multiple scrapers concurrently and aggregate results."""
    all_articles = []

    async def _run_one(scraper: BaseScraper):
        try:
            articles = await scraper.fetch_articles()
            logger.info("%s: fetched %d articles", scraper.name, len(articles))
            return articles
        except Exception as e:
            logger.error("%s: failed with %s", scraper.name, e)
            return []
        finally:
            await scraper.close()

    results = await asyncio.gather(*[_run_one(s) for s in scrapers])
    for batch in results:
        all_articles.extend(batch)
    return all_articles
