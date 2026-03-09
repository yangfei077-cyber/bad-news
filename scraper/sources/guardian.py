"""The Guardian - Global Development and Gender sections."""

from scraper.base import BaseScraper, RSSMixin, ScrapedArticle, clean_html


class GuardianScraper(RSSMixin, BaseScraper):
    name = "The Guardian"
    language = "EN"
    base_url = "https://www.theguardian.com"
    category = "gender"

    FEEDS = [
        "https://www.theguardian.com/world/gender/rss",
        "https://www.theguardian.com/society/domestic-violence/rss",
        "https://www.theguardian.com/global-development/rss",
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
                content = clean_html(e["content"]) if e["content"] else e.get("summary", "")
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
