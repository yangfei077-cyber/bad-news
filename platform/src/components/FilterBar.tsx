"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";

const VIOLENCE_TYPES = [
  { value: "", label: "All Types" },
  { value: "direct", label: "Direct" },
  { value: "structural", label: "Structural" },
  { value: "cultural", label: "Cultural" },
  { value: "identity", label: "Identity" },
  { value: "meta", label: "Meta" },
];

const LANGUAGES = [
  { value: "", label: "All Languages" },
  { value: "EN", label: "English" },
  { value: "ZH", label: "中文" },
];

const SEVERITY_OPTIONS = [
  { value: "", label: "Any Severity" },
  { value: "3", label: "3+" },
  { value: "5", label: "5+" },
  { value: "7", label: "7+" },
  { value: "9", label: "9+" },
];

export function FilterBar() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const updateParam = useCallback(
    (key: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      params.delete("page");
      router.push(`/?${params.toString()}`);
    },
    [router, searchParams]
  );

  const selectClass =
    "bg-card border border-border text-foreground text-xs font-mono px-3 py-2 rounded focus:outline-none focus:border-accent appearance-none cursor-pointer";

  return (
    <div className="flex flex-wrap items-center gap-3 py-4 border-b border-border">
      <span className="text-muted text-xs font-mono uppercase tracking-widest mr-2">
        Filter
      </span>

      <select
        value={searchParams.get("violence_type") || ""}
        onChange={(e) => updateParam("violence_type", e.target.value)}
        className={selectClass}
      >
        {VIOLENCE_TYPES.map((t) => (
          <option key={t.value} value={t.value}>
            {t.label}
          </option>
        ))}
      </select>

      <select
        value={searchParams.get("language") || ""}
        onChange={(e) => updateParam("language", e.target.value)}
        className={selectClass}
      >
        {LANGUAGES.map((l) => (
          <option key={l.value} value={l.value}>
            {l.label}
          </option>
        ))}
      </select>

      <select
        value={searchParams.get("min_severity") || ""}
        onChange={(e) => updateParam("min_severity", e.target.value)}
        className={selectClass}
      >
        {SEVERITY_OPTIONS.map((s) => (
          <option key={s.value} value={s.value}>
            {s.label}
          </option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Search..."
        defaultValue={searchParams.get("search") || ""}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            updateParam("search", (e.target as HTMLInputElement).value);
          }
        }}
        className="bg-card border border-border text-foreground text-xs font-mono px-3 py-2 rounded focus:outline-none focus:border-accent placeholder:text-muted w-48"
      />
    </div>
  );
}
