"use client";

const TAG_CONFIG: Record<string, { label: string; color: string }> = {
  direct: {
    label: "Direct Violence",
    color: "bg-red-50 text-red-700 border-red-200",
  },
  structural: {
    label: "Structural Violence",
    color: "bg-amber-50 text-amber-700 border-amber-200",
  },
  cultural: {
    label: "Cultural Violence",
    color: "bg-yellow-50 text-yellow-700 border-yellow-200",
  },
  identity: {
    label: "Identity Violence",
    color: "bg-purple-50 text-purple-700 border-purple-200",
  },
  meta: {
    label: "Meta-Violence",
    color: "bg-sky-50 text-sky-700 border-sky-200",
  },
};

export function ViolenceTag({ type }: { type: string }) {
  const config = TAG_CONFIG[type] || {
    label: type,
    color: "bg-stone-100 text-stone-600 border-stone-200",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 text-[11px] font-medium rounded-full border ${config.color}`}
    >
      {config.label}
    </span>
  );
}

export function SeverityBadge({ score }: { score: number }) {
  let color = "text-green-600";
  if (score >= 8) color = "text-red-600";
  else if (score >= 6) color = "text-amber-600";
  else if (score >= 4) color = "text-yellow-600";

  return (
    <div className="flex flex-col items-center">
      <span className="text-[10px] font-mono uppercase tracking-wider text-muted-light mb-0.5">
        Score
      </span>
      <span className={`font-serif text-2xl font-bold ${color}`}>
        {score.toFixed(1)}
      </span>
    </div>
  );
}
