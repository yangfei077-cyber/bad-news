"""界面新闻 (Jiemian) - 社会频道."""

from scraper.base import BaseScraper, HTMLScraper, ScrapedArticle
from bs4 import BeautifulSoup


class JiemianScraper(BaseScraper):
    name = "界面新闻"
    language = "ZH"
    base_url = "https://www.jiemian.com"
    category = "society"

    SECTION_URLS = [
        "https://www.jiemian.com/lists/62.html",  # 社会
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
            for item in soup.select("a[href*='/article/']"):
                href = item.get("href", "")
                if not href.startswith("http"):
                    href = "https:" + href if href.startswith("//") else self.base_url + href
                if href in seen_urls:
                    continue
                seen_urls.add(href)

                title = item.get_text(strip=True)
                if not title or len(title) < 5:
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
