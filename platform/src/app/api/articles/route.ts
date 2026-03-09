import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);

  const page = parseInt(searchParams.get("page") || "1");
  const limit = parseInt(searchParams.get("limit") || "20");
  const language = searchParams.get("language");
  const source = searchParams.get("source");
  const violenceType = searchParams.get("violence_type");
  const minSeverity = searchParams.get("min_severity");
  const analyzed = searchParams.get("analyzed");
  const search = searchParams.get("search");

  const where: Record<string, unknown> = {};

  if (language) where.language = language;
  if (source) where.sourceId = source;
  if (search) {
    where.OR = [
      { title: { contains: search, mode: "insensitive" } },
      { content: { contains: search, mode: "insensitive" } },
    ];
  }

  if (analyzed === "true") {
    where.analysis = { isNot: null };
  } else if (analyzed === "false") {
    where.analysis = null;
  }

  if (violenceType || minSeverity) {
    const analysisFilter: Record<string, unknown> = {};
    if (minSeverity) {
      analysisFilter.severityScore = { gte: parseInt(minSeverity) };
    }
    if (violenceType) {
      switch (violenceType) {
        case "direct":
          analysisFilter.galtungDirect = true;
          break;
        case "structural":
          analysisFilter.galtungStructural = true;
          break;
        case "cultural":
          analysisFilter.galtungCultural = true;
          break;
        case "identity":
          analysisFilter.identityViolence = true;
          break;
        case "meta":
          analysisFilter.metaViolence = true;
          break;
      }
    }
    where.analysis = { ...((where.analysis as object) || {}), ...analysisFilter };
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

  return NextResponse.json({
    articles,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
    },
  });
}
