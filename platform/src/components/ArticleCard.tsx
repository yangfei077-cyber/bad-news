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
  const categories = analysis
    ? parseCategories(analysis.violenceCategories)
    : [];
  const summary =
    analysis && language === "ZH" ? analysis.summaryZh : analysis?.summaryEn;

  return (
    <Link href={`/article/${id}`} className="block group">
      <article className="bg-card border border-border rounded-2xl p-6 hover:shadow-md transition-all duration-200">
        <div className="flex items-center gap-2 text-[11px] text-muted font-mono uppercase tracking-wide mb-3">
          <span className="text-accent font-semibold">{source.name}</span>
          <span className="text-border">&middot;</span>
          <span>{formatDate(publishedAt)}</span>
          <span className="text-border">&middot;</span>
          <span>{language}</span>
        </div>

        <div className="flex gap-5">
          <div className="flex-1 min-w-0">
            <h2 className="font-serif text-xl font-bold leading-snug mb-2 group-hover:text-accent transition-colors">
              {title}
            </h2>

            {summary && (
              <p className="text-sm text-muted leading-relaxed mb-4 line-clamp-3">
                {summary}
              </p>
            )}

            {!summary && excerpt && (
              <p className="text-sm text-muted leading-relaxed mb-4 line-clamp-3">
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
              <span className="inline-flex items-center px-2.5 py-1 text-[11px] font-medium rounded-full border bg-stone-50 text-stone-400 border-stone-200">
                Pending Analysis
              </span>
            )}
          </div>

          {analysis && (
            <div className="flex-shrink-0 flex items-start pt-1">
              <SeverityBadge score={analysis.severityScore} />
            </div>
          )}
        </div>
      </article>
    </Link>
  );
}
