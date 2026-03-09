"""Periodic scraping orchestrator with deduplication and DB insertion."""

import asyncio
import logging
import sys
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scraper.base import ScrapedArticle, run_scrapers
from scraper.db import (
    get_session, get_or_create_source, insert_article,
    get_unanalyzed_articles,
)
from scraper.analyzer import analyze_articles
from scraper.config import SCRAPE_INTERVAL_MINUTES
from scraper.sources import ALL_SCRAPERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("scheduler")


def store_articles(articles: list[ScrapedArticle]) -> int:
    """Persist scraped articles to DB, skipping duplicates. Returns count of new articles."""
    session = get_session()
    new_count = 0
    try:
        for a in articles:
            source = get_or_create_source(
                session,
                name=a.source_name,
                url="",
                language=a.language,
                category=None,
            )
            result = insert_article(
                session,
                source=source,
                title=a.title,
                url=a.url,
                content=a.content,
                language=a.language,
                excerpt=a.excerpt,
                author=a.author,
                image_url=a.image_url,
                published_at=a.published_at,
            )
            if result:
                new_count += 1

        source_names = set(a.source_name for a in articles)
        for name in source_names:
            src = session.query(get_or_create_source.__wrapped__.__class__).filter_by(name=name).first() if False else None  # noqa
            try:
                from scraper.db import Source as SourceModel
                src = session.query(SourceModel).filter_by(name=name).first()
                if src:
                    src.lastScraped = datetime.now(timezone.utc)
                    session.commit()
            except Exception:
                pass
    finally:
        session.close()
    return new_count


async def scrape_cycle():
    """Single scrape + store + analyze cycle."""
    logger.info("Starting scrape cycle...")
    scrapers = [cls() for cls in ALL_SCRAPERS]
    articles = await run_scrapers(scrapers)
    logger.info("Total articles fetched: %d", len(articles))

    new_count = store_articles(articles)
    logger.info("New articles stored: %d (duplicates skipped: %d)",
                new_count, len(articles) - new_count)

    session = get_session()
    try:
        unanalyzed = get_unanalyzed_articles(session)
        if unanalyzed:
            logger.info("Analyzing %d unanalyzed articles...", len(unanalyzed))
            await analyze_articles(session, unanalyzed)
            logger.info("Analysis complete.")
        else:
            logger.info("No unanalyzed articles.")
    finally:
        session.close()


async def _run():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scrape_cycle, "interval", minutes=SCRAPE_INTERVAL_MINUTES)
    scheduler.add_job(scrape_cycle)  # run immediately on start
    scheduler.start()

    stop = asyncio.Event()
    try:
        await stop.wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()


def main():
    logger.info("Bad News Scraper starting...")
    logger.info("Scrape interval: %d minutes", SCRAPE_INTERVAL_MINUTES)

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        logger.info("Shutting down...")


if __name__ == "__main__":
    main()
