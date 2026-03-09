"""The 19th - US gender politics newsroom."""

from scraper.base import BaseScraper, RSSMixin, ScrapedArticle, clean_html


class The19thScraper(RSSMixin, BaseScraper):
    name = "The 19th"
    language = "EN"
    base_url = "https://19thnews.org"
    category = "gender_politics"

    FEEDS = [
        "https://19thnews.org/feed/",
    ]

    async def fetch_articles(self) -> list[ScrapedArticle]:
        articles = []
        seen_urls = set()
        for feed_url in self.FEEDS:
            try:
                entries = await self.parse_feed(feed_url)
            except Exception:
                continue
            for e in entries:
                if e["url"] in seen_urls or not e["url"]:
                    continue
                seen_urls.add(e["url"])
                content = clean_html(e["content"]) if e["content"] else ""
                articles.append(ScrapedArticle(
                    title=e["title"],
                    url=e["url"],
                    content=content,
                    language=self.language,
                    excerpt=e.get("summary", "")[:300] if e.get("summary") else None,
                    author=e.get("author"),
                    image_url=e.get("image"),
                    published_at=e.get("published"),
                    source_name=self.name,
                ))
        return self._filter_relevant(articles)
