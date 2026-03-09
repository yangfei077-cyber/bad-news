export type ViolenceCategory =
  | "direct"
  | "structural"
  | "cultural"
  | "identity"
  | "meta";

export interface AnalysisOutput {
  violence_categories: ViolenceCategory[];
  galtung_mapping: {
    direct: boolean;
    structural: boolean;
    cultural: boolean;
  };
  identity_violence: boolean;
  meta_violence: boolean;
  primal_race_analysis: string;
  co_conspiracy_analysis: string;
  existential_war_framing: string;
  severity_score: number;
  summary_en: string;
  summary_zh: string;
}

export interface ArticleWithAnalysis {
  id: string;
  title: string;
  url: string;
  language: string;
  content: string;
  excerpt: string | null;
  author: string | null;
  imageUrl: string | null;
  publishedAt: string | null;
  scrapedAt: string;
  source: {
    id: string;
    name: string;
    language: string;
  };
  analysis: {
    violenceCategories: string;
    galtungDirect: boolean;
    galtungStructural: boolean;
    galtungCultural: boolean;
    identityViolence: boolean;
    metaViolence: boolean;
    primalRaceAnalysis: string;
    coConspiracyAnalysis: string | null;
    existentialWarFraming: string | null;
    severityScore: number;
    summaryEn: string;
    summaryZh: string;
  } | null;
}
