import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET() {
  const [
    totalArticles,
    totalAnalyzed,
    directCount,
    structuralCount,
    culturalCount,
    identityCount,
    metaCount,
    sources,
    recentArticles,
  ] = await Promise.all([
    prisma.article.count(),
    prisma.analysis.count(),
    prisma.analysis.count({ where: { galtungDirect: true } }),
    prisma.analysis.count({ where: { galtungStructural: true } }),
    prisma.analysis.count({ where: { galtungCultural: true } }),
    prisma.analysis.count({ where: { identityViolence: true } }),
    prisma.analysis.count({ where: { metaViolence: true } }),
    prisma.source.findMany({
      select: {
        id: true,
        name: true,
        language: true,
        _count: { select: { articles: true } },
      },
    }),
    prisma.article.findMany({
      take: 5,
      orderBy: { scrapedAt: "desc" },
      include: {
        source: { select: { name: true } },
        analysis: { select: { severityScore: true, violenceCategories: true } },
      },
    }),
  ]);

  const severityDistribution = await prisma.analysis.groupBy({
    by: ["severityScore"],
    _count: true,
    orderBy: { severityScore: "asc" },
  });

  const languageDistribution = await prisma.article.groupBy({
    by: ["language"],
    _count: true,
  });

  return NextResponse.json({
    overview: {
      totalArticles,
      totalAnalyzed,
      pendingAnalysis: totalArticles - totalAnalyzed,
    },
    violenceTypes: {
      direct: directCount,
      structural: structuralCount,
      cultural: culturalCount,
      identity: identityCount,
      meta: metaCount,
    },
    severityDistribution: severityDistribution.map((s) => ({
      score: s.severityScore,
      count: s._count,
    })),
    languageDistribution: languageDistribution.map((l) => ({
      language: l.language,
      count: l._count,
    })),
    sources: sources.map((s) => ({
      id: s.id,
      name: s.name,
      language: s.language,
      articleCount: s._count.articles,
    })),
    recentArticles,
  });
}
