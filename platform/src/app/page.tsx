import { Suspense } from "react";
import { prisma } from "@/lib/prisma";
import { ArticleCard } from "@/components/ArticleCard";
import { FilterBar } from "@/components/FilterBar";
import Link from "next/link";

export const dynamic = "force-dynamic";

interface PageProps {
  searchParams: Promise<{
    page?: string;
    language?: string;
    violence_type?: string;
    min_severity?: string;
    search?: string;
  }>;
}

async function StatsBar() {
  const [total, analyzed] = await Promise.all([
    prisma.article.count(),
    prisma.analysis.count(),
  ]);

  return (
    <div className="flex items-center gap-6 py-4 text-xs font-mono text-muted">
      <span>
        <span className="text-foreground font-bold">{total}</span> articles
      </span>
      <span>
        <span className="text-foreground font-bold">{analyzed}</span> analyzed
      </span>
      <span>
        <span className="text-accent font-bold">{total - analyzed}</span>{" "}
        pending
      </span>
    </div>
  );
}

async function ArticleFeed({
  searchParams,
}: {
  searchParams: {
    page?: string;
    language?: string;
    violence_type?: string;
    min_severity?: string;
    search?: string;
  };
}) {
  const page = parseInt(searchParams.page || "1");
  const limit = 20;

  const where: Record<string, unknown> = {};

  if (searchParams.language) where.language = searchParams.language;
  if (searchParams.search) {
    where.OR = [
      { title: { contains: searchParams.search } },
      { content: { contains: searchParams.search } },
    ];
  }

  if (searchParams.violence_type || searchParams.min_severity) {
    const analysisFilter: Record<string, unknown> = {};
    if (searchParams.min_severity) {
      analysisFilter.severityScore = {
        gte: parseInt(searchParams.min_severity),
      };
    }
    if (searchParams.violence_type) {
      const vt = searchParams.violence_type;
      if (vt === "direct") analysisFilter.galtungDirect = true;
      else if (vt === "structural") analysisFilter.galtungStructural = true;
      else if (vt === "cultural") analysisFilter.galtungCultural = true;
      else if (vt === "identity") analysisFilter.identityViolence = true;
      else if (vt === "meta") analysisFilter.metaViolence = true;
    }
    where.analysis = analysisFilter;
  }

  const [articles, total] = await Promise.all([
    prisma.article.findMany({
      where,
      include: {
        source: { select: { id: true, name: true, language: true } },
        analysis: true,
      },
      orderBy: { publishedAt: "desc" },
      skip: (page - 1) * limit,
      take: limit,
    }),
    prisma.article.count({ where }),
  ]);

  const totalPages = Math.ceil(total / limit);

  if (articles.length === 0) {
    return (
      <div className="text-center py-20">
        <p className="text-muted font-mono text-sm">No articles found.</p>
        <p className="text-muted/60 font-mono text-xs mt-2">
          Run the scraper to populate the database.
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="grid gap-4">
        {articles.map((article) => (
          <ArticleCard
            key={article.id}
            id={article.id}
            title={article.title}
            excerpt={article.excerpt}
            language={article.language}
            publishedAt={article.publishedAt?.toISOString() ?? null}
            source={article.source}
            analysis={article.analysis}
          />
        ))}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 mt-8">
          {page > 1 && (
            <Link
              href={`/?page=${page - 1}`}
              className="px-4 py-2 text-xs font-mono border border-border rounded hover:border-accent transition-colors"
            >
              Previous
            </Link>
          )}
          <span className="text-xs font-mono text-muted px-4">
            {page} / {totalPages}
          </span>
          {page < totalPages && (
            <Link
              href={`/?page=${page + 1}`}
              className="px-4 py-2 text-xs font-mono border border-border rounded hover:border-accent transition-colors"
            >
              Next
            </Link>
          )}
        </div>
      )}
    </div>
  );
}

export default async function HomePage({ searchParams }: PageProps) {
  const resolvedParams = await searchParams;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-2">
          Violence Architecture
        </h1>
        <p className="text-muted text-sm max-w-2xl">
          Gender violence news analyzed through the Primal Race Theory and
          Galtung&apos;s Violence Triangle framework. Each article is processed
          by a fine-tuned model to surface direct, structural, cultural,
          identity, and meta-violence patterns.
        </p>
      </div>

      <StatsBar />

      <Suspense fallback={null}>
        <FilterBar />
      </Suspense>

      <div className="mt-6">
        <Suspense
          fallback={
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className="border border-border rounded-lg p-5 bg-card animate-pulse h-32"
                />
              ))}
            </div>
          }
        >
          <ArticleFeed searchParams={resolvedParams} />
        </Suspense>
      </div>
    </div>
  );
}
