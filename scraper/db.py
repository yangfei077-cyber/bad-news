"""Database operations for the scraper using SQLAlchemy, sharing the same DB as Prisma."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Text,
    ForeignKey, Index, create_engine, TypeDecorator,
)
from sqlalchemy.orm import DeclarativeBase, Session, relationship, sessionmaker

from scraper.config import DATABASE_URL

_is_sqlite = DATABASE_URL.startswith("sqlite")


class PrismaDateTime(TypeDecorator):
    """Handle Prisma's ISO-8601 datetime format in SQLite (stored as text)."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 1000:03d}Z"
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None


DateTimeColumn = PrismaDateTime if _is_sqlite else DateTime(timezone=True)


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "Source"

    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    language = Column(String, nullable=False)
    category = Column(String, nullable=True)
    scrapeConfig = Column(String, nullable=True)
    enabled = Column(Boolean, default=True)
    lastScraped = Column(DateTimeColumn, nullable=True)
    createdAt = Column(DateTimeColumn, default=lambda: datetime.now(timezone.utc))
    articles = relationship("Article", back_populates="source")


class Article(Base):
    __tablename__ = "Article"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    sourceId = Column(String, ForeignKey("Source.id"), nullable=False)
    language = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(String, nullable=True)
    author = Column(String, nullable=True)
    imageUrl = Column(String, nullable=True)
    publishedAt = Column(DateTimeColumn, nullable=True)
    scrapedAt = Column(DateTimeColumn, default=lambda: datetime.now(timezone.utc))
    source = relationship("Source", back_populates="articles")
    analysis = relationship("Analysis", back_populates="article", uselist=False)

    __table_args__ = (
        Index("Article_language_idx", "language"),
        Index("Article_publishedAt_idx", "publishedAt"),
        Index("Article_sourceId_idx", "sourceId"),
    )


class Analysis(Base):
    __tablename__ = "Analysis"

    id = Column(String, primary_key=True)
    articleId = Column(String, ForeignKey("Article.id", ondelete="CASCADE"), unique=True)
    violenceCategories = Column(String, nullable=False)
    galtungDirect = Column(Boolean, default=False)
    galtungStructural = Column(Boolean, default=False)
    galtungCultural = Column(Boolean, default=False)
    identityViolence = Column(Boolean, default=False)
    metaViolence = Column(Boolean, default=False)
    primalRaceAnalysis = Column(Text, nullable=False)
    coConspiracyAnalysis = Column(Text, nullable=True)
    existentialWarFraming = Column(Text, nullable=True)
    severityScore = Column(Integer, nullable=False)
    summaryEn = Column(Text, nullable=False)
    summaryZh = Column(Text, nullable=False)
    modelVersion = Column(String, nullable=False)
    analyzedAt = Column(DateTimeColumn, default=lambda: datetime.now(timezone.utc))
    article = relationship("Article", back_populates="analysis")

    __table_args__ = (
        Index("Analysis_severityScore_idx", "severityScore"),
        Index("Analysis_analyzedAt_idx", "analyzedAt"),
    )


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def get_session() -> Session:
    return SessionLocal()


def generate_cuid() -> str:
    """Generate a CUID-like ID compatible with Prisma's format."""
    import time
    import random
    import string
    timestamp = int(time.time() * 1000)
    ts_part = ""
    while timestamp > 0:
        ts_part = string.ascii_lowercase[timestamp % 26] + ts_part
        timestamp //= 26
    rand_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"c{ts_part}{rand_part}"


def get_or_create_source(
    session: Session,
    name: str,
    url: str,
    language: str,
    category: Optional[str] = None,
) -> Source:
    source = session.query(Source).filter_by(name=name).first()
    if not source:
        source = Source(
            id=generate_cuid(),
            name=name,
            url=url,
            language=language,
            category=category,
        )
        session.add(source)
        session.commit()
    return source


def article_exists(session: Session, url: str) -> bool:
    return session.query(Article).filter_by(url=url).first() is not None


def insert_article(
    session: Session,
    source: Source,
    title: str,
    url: str,
    content: str,
    language: str,
    excerpt: Optional[str] = None,
    author: Optional[str] = None,
    image_url: Optional[str] = None,
    published_at: Optional[datetime] = None,
) -> Optional[Article]:
    if article_exists(session, url):
        return None

    article = Article(
        id=generate_cuid(),
        title=title,
        url=url,
        sourceId=source.id,
        language=language,
        content=content,
        excerpt=excerpt,
        author=author,
        imageUrl=image_url,
        publishedAt=published_at,
        scrapedAt=datetime.now(timezone.utc),
    )
    session.add(article)
    session.commit()
    return article


def get_unanalyzed_articles(session: Session, limit: int = 50) -> list[Article]:
    return (
        session.query(Article)
        .outerjoin(Analysis)
        .filter(Analysis.id.is_(None))
        .order_by(Article.scrapedAt.desc())
        .limit(limit)
        .all()
    )
