"""Al Jazeera - women's rights coverage."""

from scraper.base import BaseScraper, RSSMixin, HTMLScraper, ScrapedArticle, clean_html
from bs4 import BeautifulSoup


class AlJazeeraScraper(RSSMixin, BaseScraper):
    name = "Al Jazeera"
    language = "EN"
    base_url = "https://www.aljazeera.com"
    category = "gender"

    FEEDS = [
        "https://www.aljazeera.com/xml/rss/all.xml",
    ]

    TAG_URLS = [
        "https://www.aljazeera.com/tag/womens-rights/",
        "https://www.aljazeera.com/tag/gender/",
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

        for tag_url in self.TAG_URLS:
            try:
                html = await self._get(tag_url)
                soup = BeautifulSoup(html, "lxml")
                for link_tag in soup.select("a.u-clickable-card__link"):
                    href = link_tag.get("href", "")
                    if not href.startswith("http"):
                        href = self.base_url + href
                    if href in seen_urls:
                        continue
                    seen_urls.add(href)
                    extracted = await HTMLScraper.extract_article(self.client, href)
                    if not extracted.get("content"):
                        continue
                    articles.append(ScrapedArticle(
                        title=extracted.get("title", ""),
                        url=href,
                        content=extracted["content"],
                        language=self.language,
                        author=extracted.get("author"),
                        image_url=extracted.get("image"),
                        published_at=extracted.get("published"),
                        source_name=self.name,
                    ))
            except Exception:
                continue

        return self._filter_relevant(articles)
