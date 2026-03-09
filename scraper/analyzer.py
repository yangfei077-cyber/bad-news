"""News analysis using fine-tuned OpenAI model."""

import json
import logging
from datetime import datetime, timezone

from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from scraper.config import OPENAI_API_KEY, FINE_TUNED_MODEL
from scraper.db import Article, Analysis, generate_cuid

logger = logging.getLogger("analyzer")

SYSTEM_PROMPT = """You are a critical analyst applying the theoretical framework from "The Primal Race and the Architecture of Violence." Your framework includes:

1. **Galtung's Violence Triangle**: Classify violence as Direct (physical harm, femicide, assault), Structural (laws, economic systems, institutional barriers), or Cultural (norms, media, religion that legitimize violence).

2. **Primal Race Theory**: Sex is the original racial construct. Biological females are the "primal race" — colonized before any color-based or class-based racial categories existed. Gender violence follows the same logic as racial violence: subject-making, object-making, exploitation.

3. **Identity Violence**: The dissolution of "woman" as a political category through gender ideology that conflates social gender performance with biological sex, stripping biological females of their political "base."

4. **Meta-Violence**: Male-centered narratives that monopolize interpretation and meaning-making. This is the violence that directs all other violence — controlling who gets to define reality.

5. **Co-conspirators Theory**: Micro-patriarchal units (families, friendships, social cells) that crystallize male-centered narratives. Religion and romantic love serve as social anesthetics. Some "progressives" merely swap one anesthetic for another.

6. **Existential War**: All expression is political. Identity politics is an inevitable alliance/struggle based on phenotype, background, and culture. The "optimal expression" for each person is being systematically distorted by structural power.

Analyze the given news article through this framework. Return a JSON object with these fields:
- violence_categories: array of "direct", "structural", "cultural", "identity", "meta" (which apply)
- galtung_mapping: {"direct": bool, "structural": bool, "cultural": bool}
- identity_violence: bool
- meta_violence: bool
- primal_race_analysis: string (2-4 sentences connecting to primal race theory)
- co_conspiracy_analysis: string (1-3 sentences on complicity structures, or null)
- existential_war_framing: string (1-2 sentences on expression/identity politics angle, or null)
- severity_score: int 1-10 (10 = most severe systemic violence)
- summary_en: string (3-5 sentence analytical summary in English)
- summary_zh: string (3-5 sentence analytical summary in Chinese)

Return ONLY valid JSON, no markdown fences."""

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def analyze_single(article: Article) -> dict | None:
    """Analyze a single article using the fine-tuned model."""
    model = FINE_TUNED_MODEL or "gpt-4o-mini"

    article_text = f"Title: {article.title}\n\n"
    if article.excerpt:
        article_text += f"Excerpt: {article.excerpt}\n\n"
    content = article.content[:4000]
    article_text += f"Content: {content}"

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": article_text},
            ],
            temperature=0.3,
            max_tokens=2000,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        return json.loads(raw)
    except Exception as e:
        logger.error("Analysis failed for article %s: %s", article.id, e)
        return None


async def analyze_articles(session: Session, articles: list[Article]):
    """Analyze a batch of articles and store results."""
    model_version = FINE_TUNED_MODEL or "gpt-4o-mini"

    for article in articles:
        result = await analyze_single(article)
        if not result:
            continue

        violence_cats = result.get("violence_categories", [])
        galtung = result.get("galtung_mapping", {})

        analysis = Analysis(
            id=generate_cuid(),
            articleId=article.id,
            violenceCategories=json.dumps(violence_cats),
            galtungDirect=galtung.get("direct", False),
            galtungStructural=galtung.get("structural", False),
            galtungCultural=galtung.get("cultural", False),
            identityViolence=result.get("identity_violence", False),
            metaViolence=result.get("meta_violence", False),
            primalRaceAnalysis=result.get("primal_race_analysis", ""),
            coConspiracyAnalysis=result.get("co_conspiracy_analysis"),
            existentialWarFraming=result.get("existential_war_framing"),
            severityScore=result.get("severity_score", 5),
            summaryEn=result.get("summary_en", ""),
            summaryZh=result.get("summary_zh", ""),
            modelVersion=model_version,
            analyzedAt=datetime.now(timezone.utc),
        )
        session.add(analysis)
        session.commit()
        logger.info("Analyzed: %s (severity: %d)", article.title[:60], analysis.severityScore)
