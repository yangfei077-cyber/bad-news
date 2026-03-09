"use client";

import Link from "next/link";
import { ViolenceTag, SeverityBadge } from "./ViolenceTag";

interface ArticleAnalysis {
  violenceCategories: string;
  galtungDirect: boolean;
  galtungStructural: boolean;
  galtungCultural: boolean;
  identityViolence: boolean;
  metaViolence: boolean;
  severityScore: number;
  summaryEn: string;
  summaryZh: string;
}

interface ArticleCardProps {
  id: string;
  title: string;
  excerpt: string | null;
  language: string;
  publishedAt: string | null;
  source: { name: string };
  analysis: ArticleAnalysis | null;
}

function parseCategories(raw: string): string[] {
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function ArticleCard({
  id,
  title,
  excerpt,
  language,
  publishedAt,
  source,
  analysis,
}: ArticleCardProps) {
  const categories = analysis ? parseCategories(analysis.violenceCategories) : [];
  const summary =
    analysis && language === "ZH" ? analysis.summaryZh : analysis?.summaryEn;

  return (
    <Link href={`/article/${id}`} className="block group">
      <article className="border border-border rounded-lg p-5 bg-card hover:bg-card-hover transition-colors duration-200 hover:border-accent/30">
        <div className="flex items-start justify-between gap-4 mb-3">
          <div className="flex items-center gap-2 text-xs text-muted font-mono">
            <span className="text-accent">{source.name}</span>
            <span>·</span>
            <span>{formatDate(publishedAt)}</span>
            <span>·</span>
            <span className="uppercase">{language}</span>
          </div>
          {analysis && <SeverityBadge score={analysis.severityScore} />}
        </div>

        <h2 className="text-lg font-semibold leading-tight mb-2 group-hover:text-accent transition-colors">
          {title}
        </h2>

        {summary && (
          <p className="text-sm text-muted leading-relaxed mb-3 line-clamp-2">
            {summary}
          </p>
        )}

        {!summary && excerpt && (
          <p className="text-sm text-muted leading-relaxed mb-3 line-clamp-2">
            {excerpt}
          </p>
        )}

        {categories.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {categories.map((cat) => (
              <ViolenceTag key={cat} type={cat} />
            ))}
          </div>
        )}

        {!analysis && (
          <div className="flex items-center gap-2 mt-2">
            <span className="inline-flex items-center px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider border rounded bg-zinc-800/50 text-zinc-500 border-zinc-700">
              Pending Analysis
            </span>
          </div>
        )}
      </article>
    </Link>
  );
}
