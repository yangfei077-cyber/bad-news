# BAD NEWS Platform


Based on Essay: https://xj2vrrpw4b9pyznc.public.blob.vercel-storage.com/primal%20race.pdf


A platform that scrapes gender violence news (EN/ZH), analyzes them through a fine-tuned GPT model embodying the **Primal Race Theory** and **Galtung's Violence Triangle** framework, and presents structured critical analysis on a Next.js web interface.

## Architecture

```
Scraping (Python) -> SQLite -> Analysis (Fine-tuned GPT-4o-mini) -> Next.js Platform
```

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Scraping | Python + httpx + feedparser + newspaper3k | Fetch news from 10 EN/ZH sources |
| Storage | SQLite (via Prisma) | Shared database between scraper and platform |
| Analysis | OpenAI fine-tuned GPT-4o-mini | Analyze articles through the essay's theoretical framework |
| Platform | Next.js 16 + Tailwind CSS | Dark editorial UI with Galtung triangle visualization |

## Quick Start

### 1. Set up the Next.js platform

```bash
cd platform
npm install
echo 'DATABASE_URL="file:./dev.db"' > .env
npx prisma migrate dev --name init
npm run db:seed          # insert sample articles
npm run dev              # http://localhost:3000
```

### 2. Set up the Python scraper

```bash
cd scraper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Fine-tune the model (requires OpenAI API key)

```bash
# Add your key to .env at the project root
# OPENAI_API_KEY="sk-..."

cd fine-tuning
pip install -r requirements.txt
python generate_training.py   # generates training_data.jsonl (uses GPT-4o)
python fine_tune.py            # submits fine-tuning job on GPT-4o-mini
# Update FINE_TUNED_MODEL in .env with the returned model name
```

### 4. Run the scraper

```bash
cd scraper
python -m scraper.scheduler   # scrapes every 60min + analyzes with fine-tuned model
```

## News Sources

**English:**
- The Guardian (gender + domestic violence + global development RSS)
- BBC News (world RSS + women topic)
- Reuters (women's rights + gender tags)
- The 19th (dedicated US gender politics newsroom)
- Al Jazeera (women's rights + gender tags)
- UN Women (news stories)

**Chinese (中文):**
- 澎湃新闻 (法治/专案频道 API + HTML)
- 界面新闻 (社会频道)
- 端传媒 (RSS feed)
- 凤凰网 (社会频道)

## Theoretical Framework

Each article is analyzed through these lenses:

| Framework | Description |
|-----------|-------------|
| **Galtung's Violence Triangle** | Direct (physical), Structural (institutional), Cultural (normative) violence |
| **Primal Race Theory** | Sex as original racial construct; women as first colonized group |
| **Identity Violence** | Dissolution of "woman" as political category |
| **Meta-Violence** | Male-centered narratives controlling interpretation |
| **Co-conspirators Theory** | Micro-patriarchal units; religion and romantic love as anesthetics |
| **Existential War** | Expression as political act; optimal expression distortion |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/articles` | GET | List articles with filters (language, violence_type, min_severity, search) |
| `/api/articles/[id]` | GET | Single article with full analysis |
| `/api/stats` | GET | Aggregated statistics |

## Project Structure

```
news/
├── platform/          Next.js web app
│   ├── prisma/        Schema + migrations + seed
│   └── src/
│       ├── app/       Pages + API routes
│       ├── components/ UI components (ArticleCard, AnalysisPanel, GaltungTriangle, etc.)
│       └── lib/       Prisma client + types
├── scraper/           Python scraping + analysis
│   ├── sources/       Per-source scraper modules (10 sources)
│   ├── base.py        Base scraper class, RSS mixin, HTML extractor
│   ├── analyzer.py    Fine-tuned model analysis pipeline
│   ├── scheduler.py   Periodic scraping orchestrator
│   └── db.py          SQLAlchemy database operations
├── fine-tuning/       Model training pipeline
│   ├── essay.md       Structured essay text
│   ├── system_prompt.txt  System prompt for the model
│   ├── generate_training.py  Generate JSONL training data via GPT-4o
│   └── fine_tune.py   Submit + monitor OpenAI fine-tuning job
└── .env               API keys and database URL
```
