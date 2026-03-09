"""Reuters - gender and human rights wire."""

from scraper.base import BaseScraper, HTMLScraper, ScrapedArticle, clean_html

from bs4 import BeautifulSoup


class ReutersScraper(BaseScraper):
    name = "Reuters"
    language = "EN"
    base_url = "https://www.reuters.com"
    category = "gender"

    SECTION_URLS = [
        "https://www.reuters.com/tags/women-rights/",
        "https://www.reuters.com/tags/gender/",
    ]

    async def fetch_articles(self) -> list[ScrapedArticle]:
        articles = []
        seen_urls = set()

        for section_url in self.SECTION_URLS:
            try:
                html = await self._get(section_url)
            except Exception:
                continue

            soup = BeautifulSoup(html, "lxml")
            for link_tag in soup.select("a[href*='/article/'], a[href*='/world/']"):
                href = link_tag.get("href", "")
                if not href.startswith("http"):
                    href = self.base_url + href
                if href in seen_urls:
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
