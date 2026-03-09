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

export function AnalysisPanel({ analysis }: { analysis: AnalysisData }) {
  const categories = parseCategories(analysis.violenceCategories);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-mono uppercase tracking-widest text-accent">
          Framework Analysis
        </h3>
        <SeverityBadge score={analysis.severityScore} />
      </div>

      {/* Galtung Triangle */}
      <div className="flex flex-col items-center py-4 bg-background rounded-lg border border-border">
        <GaltungTriangle
          direct={analysis.galtungDirect}
          structural={analysis.galtungStructural}
          cultural={analysis.galtungCultural}
        />
        <p className="text-[10px] font-mono text-muted mt-2 uppercase tracking-widest">
          Galtung&apos;s Violence Triangle
        </p>
      </div>

      {/* Violence Categories */}
      <div>
        <h4 className="text-xs font-mono text-muted uppercase tracking-widest mb-2">
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

      {/* Primal Race Analysis */}
      <div>
        <h4 className="text-xs font-mono text-muted uppercase tracking-widest mb-2">
          Primal Race Analysis
        </h4>
        <p className="text-sm leading-relaxed">{analysis.primalRaceAnalysis}</p>
      </div>

      {/* Co-conspiracy Analysis */}
      {analysis.coConspiracyAnalysis && (
        <div>
          <h4 className="text-xs font-mono text-muted uppercase tracking-widest mb-2">
            Co-conspiracy Structure
          </h4>
          <p className="text-sm leading-relaxed">
            {analysis.coConspiracyAnalysis}
          </p>
        </div>
      )}

      {/* Existential War Framing */}
      {analysis.existentialWarFraming && (
        <div>
          <h4 className="text-xs font-mono text-muted uppercase tracking-widest mb-2">
            Existential War Framing
          </h4>
          <p className="text-sm leading-relaxed">
            {analysis.existentialWarFraming}
          </p>
        </div>
      )}

      {/* Summaries */}
      <div className="space-y-4 pt-4 border-t border-border">
        <div>
          <h4 className="text-xs font-mono text-muted uppercase tracking-widest mb-2">
            Summary (EN)
          </h4>
          <p className="text-sm leading-relaxed">{analysis.summaryEn}</p>
        </div>
        <div>
          <h4 className="text-xs font-mono text-muted uppercase tracking-widest mb-2">
            Summary (ZH)
          </h4>
          <p className="text-sm leading-relaxed">{analysis.summaryZh}</p>
        </div>
      </div>

      {/* Model Info */}
      <div className="pt-4 border-t border-border">
        <p className="text-[10px] font-mono text-muted">
          Model: {analysis.modelVersion} | Analyzed:{" "}
          {new Date(analysis.analyzedAt).toLocaleString()}
        </p>
      </div>
    </div>
  );
}
