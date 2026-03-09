"use client";

import { GaltungTriangle } from "./GaltungTriangle";
import { ViolenceTag, SeverityBadge } from "./ViolenceTag";

interface AnalysisData {
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
  modelVersion: string;
  analyzedAt: string | Date;
}

function parseCategories(raw: string): string[] {
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function AnalysisSection({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <h4 className="text-[11px] font-mono uppercase tracking-widest text-muted mb-2">
        {title}
      </h4>
      <div className="text-sm leading-relaxed text-foreground/80">
        {children}
      </div>
    </div>
  );
}

export function AnalysisPanel({ analysis }: { analysis: AnalysisData }) {
  const categories = parseCategories(analysis.violenceCategories);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="font-serif text-lg font-bold text-accent">
          Framework Analysis
        </h3>
        <SeverityBadge score={analysis.severityScore} />
      </div>

      <div className="flex flex-col items-center py-5 bg-stone-50 rounded-xl border border-border">
        <GaltungTriangle
          direct={analysis.galtungDirect}
          structural={analysis.galtungStructural}
          cultural={analysis.galtungCultural}
        />
        <p className="text-[10px] font-mono text-muted mt-2 uppercase tracking-widest">
          Galtung&apos;s Violence Triangle
        </p>
      </div>

      <div>
        <h4 className="text-[11px] font-mono uppercase tracking-widest text-muted mb-2">
          Violence Types
        </h4>
        <div className="flex flex-wrap gap-1.5">
          {categories.map((cat) => (
            <ViolenceTag key={cat} type={cat} />
          ))}
          {analysis.identityViolence && <ViolenceTag type="identity" />}
          {analysis.metaViolence && <ViolenceTag type="meta" />}
        </div>
      </div>

      <AnalysisSection title="Primal Race Analysis">
        <p>{analysis.primalRaceAnalysis}</p>
      </AnalysisSection>

      {analysis.coConspiracyAnalysis && (
        <AnalysisSection title="Co-conspiracy Structure">
          <p>{analysis.coConspiracyAnalysis}</p>
        </AnalysisSection>
      )}

      {analysis.existentialWarFraming && (
        <AnalysisSection title="Existential War Framing">
          <p>{analysis.existentialWarFraming}</p>
        </AnalysisSection>
      )}

      <div className="space-y-4 pt-5 border-t border-border">
        <AnalysisSection title="Summary (EN)">
          <p>{analysis.summaryEn}</p>
        </AnalysisSection>
        <AnalysisSection title="Summary (ZH)">
          <p>{analysis.summaryZh}</p>
        </AnalysisSection>
      </div>

      <div className="pt-4 border-t border-border">
        <p className="text-[10px] font-mono text-muted-light">
          Model: {analysis.modelVersion} &middot; Analyzed:{" "}
          {new Date(analysis.analyzedAt).toLocaleString()}
        </p>
      </div>
    </div>
  );
}
