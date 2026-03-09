-- CreateTable
CREATE TABLE "Source" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "language" TEXT NOT NULL,
    "category" TEXT,
    "scrapeConfig" TEXT,
    "enabled" BOOLEAN NOT NULL DEFAULT true,
    "lastScraped" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Source_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Article" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "sourceId" TEXT NOT NULL,
    "language" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "excerpt" TEXT,
    "author" TEXT,
    "imageUrl" TEXT,
    "publishedAt" TIMESTAMP(3),
    "scrapedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Article_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Analysis" (
    "id" TEXT NOT NULL,
    "articleId" TEXT NOT NULL,
    "violenceCategories" TEXT NOT NULL,
    "galtungDirect" BOOLEAN NOT NULL DEFAULT false,
    "galtungStructural" BOOLEAN NOT NULL DEFAULT false,
    "galtungCultural" BOOLEAN NOT NULL DEFAULT false,
    "identityViolence" BOOLEAN NOT NULL DEFAULT false,
    "metaViolence" BOOLEAN NOT NULL DEFAULT false,
    "primalRaceAnalysis" TEXT NOT NULL,
    "coConspiracyAnalysis" TEXT,
    "existentialWarFraming" TEXT,
    "severityScore" INTEGER NOT NULL,
    "summaryEn" TEXT NOT NULL,
    "summaryZh" TEXT NOT NULL,
    "modelVersion" TEXT NOT NULL,
    "analyzedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Analysis_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Source_name_key" ON "Source"("name");

-- CreateIndex
CREATE UNIQUE INDEX "Article_url_key" ON "Article"("url");

-- CreateIndex
CREATE INDEX "Article_language_idx" ON "Article"("language");

-- CreateIndex
CREATE INDEX "Article_publishedAt_idx" ON "Article"("publishedAt");

-- CreateIndex
CREATE INDEX "Article_sourceId_idx" ON "Article"("sourceId");

-- CreateIndex
CREATE UNIQUE INDEX "Analysis_articleId_key" ON "Analysis"("articleId");

-- CreateIndex
CREATE INDEX "Analysis_severityScore_idx" ON "Analysis"("severityScore");

-- CreateIndex
CREATE INDEX "Analysis_analyzedAt_idx" ON "Analysis"("analyzedAt");

-- AddForeignKey
ALTER TABLE "Article" ADD CONSTRAINT "Article_sourceId_fkey" FOREIGN KEY ("sourceId") REFERENCES "Source"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Analysis" ADD CONSTRAINT "Analysis_articleId_fkey" FOREIGN KEY ("articleId") REFERENCES "Article"("id") ON DELETE CASCADE ON UPDATE CASCADE;
