"""澎湃新闻 (The Paper) - 社会/亲权 sections."""

import json
from datetime import datetime

from scraper.base import BaseScraper, HTMLScraper, ScrapedArticle
from bs4 import BeautifulSoup


class ThePaperScraper(BaseScraper):
    name = "澎湃新闻"
    language = "ZH"
    base_url = "https://www.thepaper.cn"
    category = "society"

    CHANNEL_IDS = [
        "25950",  # 法治中国
        "25951",  # 一号专案
        "25952",  # 澎湃质量报告
    ]

    API_URL = "https://api.thepaper.cn/contentapi/nodeCont/getByChannelId"

    async def fetch_articles(self) -> list[ScrapedArticle]:
        articles = []
        seen_urls = set()

        for channel_id in self.CHANNEL_IDS:
            try:
                resp = await self.client.get(
                    self.API_URL,
                    params={"channelId": channel_id, "pageNum": 1, "pageSize": 20},
                )
                resp.raise_for_status()
                data = resp.json()
                items = data.get("data", {}).get("list", [])
            except Exception:
                try:
                    html = await self._get(f"{self.base_url}/channel_{channel_id}")
                    soup = BeautifulSoup(html, "lxml")
                    for a_tag in soup.select("a[href*='newsDetail']"):
                        href = a_tag.get("href", "")
                        if not href.startswith("http"):
                            href = self.base_url + "/" + href.lstrip("/")
                        if href in seen_urls:
                            continue
                        seen_urls.add(href)
                        title = a_tag.get_text(strip=True)
                        if not title:
                            continue
                        extracted = await HTMLScraper.extract_article(self.client, href)
                        if extracted.get("content"):
                            articles.append(ScrapedArticle(
                                title=extracted.get("title", title),
                                url=href,
                                content=extracted["content"],
                                language=self.language,
                                source_name=self.name,
                                published_at=extracted.get("published"),
                            ))
                except Exception:
                    pass
                continue

            for item in items:
                cont_id = item.get("contId", "")
                title = item.get("name", "")
                url = f"{self.base_url}/newsDetail_forward_{cont_id}"
                if url in seen_urls or not title:
                    continue
                seen_urls.add(url)

                pub_time = item.get("pubTimeLong")
                published = None
                if pub_time:
                    try:
                        published = datetime.fromtimestamp(pub_time / 1000)
                    except Exception:
                        pass

                try:
                    extracted = await HTMLScraper.extract_article(self.client, url)
                    content = extracted.get("content", "")
                except Exception:
                    content = item.get("summary", "")

                if content:
                    articles.append(ScrapedArticle(
                        title=title,
                        url=url,
                        content=content,
                        language=self.language,
                        excerpt=item.get("summary", "")[:300],
                        image_url=item.get("pic"),
                        published_at=published,
                        source_name=self.name,
                    ))

        return self._filter_relevant(articles)
