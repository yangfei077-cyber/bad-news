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

const SORT_OPTIONS = [
  { value: "", label: "Latest" },
  { value: "severity", label: "Severity" },
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

  const currentType = searchParams.get("violence_type") || "";
  const currentLang = searchParams.get("language") || "";
  const currentSort = searchParams.get("sort") || "";

  const pillBase =
    "px-3.5 py-1.5 rounded-full text-xs font-medium border transition-all cursor-pointer";
  const pillActive = "bg-accent text-white border-accent";
  const pillInactive =
    "bg-white text-muted border-border hover:border-stone-300 hover:text-foreground";

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        {VIOLENCE_TYPES.map((t) => (
          <button
            key={t.value}
            onClick={() => updateParam("violence_type", t.value)}
            className={`${pillBase} ${currentType === t.value ? pillActive : pillInactive}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {LANGUAGES.map((l) => (
          <button
            key={l.value}
            onClick={() => updateParam("language", l.value)}
            className={`${pillBase} ${currentLang === l.value ? pillActive : pillInactive}`}
          >
            {l.label}
          </button>
        ))}

        <span className="w-px h-5 bg-border mx-1" />

        {SORT_OPTIONS.map((s) => (
          <button
            key={s.value}
            onClick={() => updateParam("sort", s.value)}
            className={`${pillBase} ${currentSort === s.value ? pillActive : pillInactive}`}
          >
            {s.label}
          </button>
        ))}
      </div>

      <div className="relative">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-light"
          xmlns="http://www.w3.org/2000/svg"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.3-4.3" />
        </svg>
        <input
          type="text"
          placeholder="Search architecture..."
          defaultValue={searchParams.get("search") || ""}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              updateParam("search", (e.target as HTMLInputElement).value);
            }
          }}
          className="w-full bg-white border border-border text-foreground text-sm pl-9 pr-4 py-2.5 rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent placeholder:text-muted-light"
        />
      </div>
    </div>
  );
}
