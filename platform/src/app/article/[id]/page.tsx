import { notFound } from "next/navigation";
import Link from "next/link";
import { prisma } from "@/lib/prisma";
import { AnalysisPanel } from "@/components/AnalysisPanel";
import { ViolenceTag } from "@/components/ViolenceTag";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function ArticlePage({ params }: PageProps) {
  const { id } = await params;

  const article = await prisma.article.findUnique({
    where: { id },
    include: {
      source: true,
      analysis: true,
    },
  });

  if (!article) notFound();

  const categories: string[] = article.analysis
    ? (() => {
        try {
          return JSON.parse(article.analysis.violenceCategories);
        } catch {
          return [];
        }
      })()
    : [];

  return (
    <div>
      <Link
        href="/"
        className="inline-flex items-center gap-1 text-xs font-mono text-muted hover:text-accent transition-colors mb-6"
      >
        &larr; Back to feed
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Article Content - Left 2/3 */}
        <div className="lg:col-span-2">
          <div className="mb-4 flex items-center gap-2 text-xs font-mono text-muted">
            <span className="text-accent">{article.source.name}</span>
            <span>·</span>
            <span>
              {article.publishedAt
                ? new Date(article.publishedAt).toLocaleDateString("en-US", {
                    month: "long",
                    day: "numeric",
                    year: "numeric",
                  })
                : "Date unknown"}
            </span>
            <span>·</span>
            <span className="uppercase">{article.language}</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-bold leading-tight mb-4">
            {article.title}
          </h1>

          {article.author && (
            <p className="text-sm text-muted mb-4">By {article.author}</p>
          )}

          {categories.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-6">
              {categories.map((cat) => (
                <ViolenceTag key={cat} type={cat} />
              ))}
            </div>
          )}

          <div className="border-t border-border pt-6">
            <div className="prose prose-invert prose-sm max-w-none">
              {article.content.split("\n\n").map((paragraph, i) => (
                <p key={i} className="text-sm leading-relaxed text-foreground/80 mb-4">
                  {paragraph}
                </p>
              ))}
            </div>
          </div>

          <div className="mt-8 pt-4 border-t border-border">
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs font-mono text-accent hover:underline"
            >
              View original article &rarr;
            </a>
          </div>
        </div>

        {/* Analysis Panel - Right 1/3 */}
        <div className="lg:col-span-1">
          <div className="sticky top-24 bg-card border border-border rounded-lg p-5">
            {article.analysis ? (
              <AnalysisPanel analysis={article.analysis} />
            ) : (
              <div className="text-center py-8">
                <p className="text-muted font-mono text-sm">
                  Analysis pending
                </p>
                <p className="text-muted/60 font-mono text-xs mt-2">
                  This article has not been analyzed yet.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
