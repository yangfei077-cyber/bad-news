"use client";

const TAG_CONFIG: Record<string, { label: string; className: string }> = {
  direct: {
    label: "Direct",
    className: "bg-red-900/40 text-red-400 border-red-800",
  },
  structural: {
    label: "Structural",
    className: "bg-orange-900/40 text-orange-400 border-orange-800",
  },
  cultural: {
    label: "Cultural",
    className: "bg-yellow-900/40 text-yellow-400 border-yellow-800",
  },
  identity: {
    label: "Identity",
    className: "bg-purple-900/40 text-purple-400 border-purple-800",
  },
  meta: {
    label: "Meta",
    className: "bg-cyan-900/40 text-cyan-400 border-cyan-800",
  },
};

export function ViolenceTag({ type }: { type: string }) {
  const config = TAG_CONFIG[type] || {
    label: type,
    className: "bg-zinc-800 text-zinc-400 border-zinc-700",
  };

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider border rounded ${config.className}`}
    >
      {config.label}
    </span>
  );
}

export function SeverityBadge({ score }: { score: number }) {
  let color = "text-green-400";
  if (score >= 8) color = "text-red-500";
  else if (score >= 6) color = "text-orange-400";
  else if (score >= 4) color = "text-yellow-400";

  return (
    <span className={`font-mono text-sm font-bold ${color}`}>
      {score}/10
    </span>
  );
}
