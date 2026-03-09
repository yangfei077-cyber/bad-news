"""UN Women News - institutional feed on gender equality."""

from scraper.base import BaseScraper, HTMLScraper, ScrapedArticle
from bs4 import BeautifulSoup


class UNWomenScraper(BaseScraper):
    name = "UN Women"
    language = "EN"
    base_url = "https://www.unwomen.org"
    category = "institutional"

    LIST_URL = "https://www.unwomen.org/en/news-stories"

    async def fetch_articles(self) -> list[ScrapedArticle]:
        articles = []
        seen_urls = set()

        try:
            html = await self._get(self.LIST_URL)
        except Exception:
            return articles

        soup = BeautifulSoup(html, "lxml")
        for link_tag in soup.select("a[href*='/en/news-stories/']"):
            href = link_tag.get("href", "")
            if not href.startswith("http"):
                href = self.base_url + href
            if href in seen_urls or href == self.LIST_URL:
                continue
            seen_urls.add(href)

            title = link_tag.get_text(strip=True)
            if not title or len(title) < 10:
                continue

            try:
                extracted = await HTMLScraper.extract_article(self.client, href)
                if not extracted.get("content"):
                    continue
                articles.append(ScrapedArticle(
                    title=extracted.get("title", title),
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
