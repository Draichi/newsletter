import Link from "next/link";

const SOURCES = [
  { name: "All", slug: "" },
  { name: "Dark Reading", slug: "darkreading" },
  { name: "The Record", slug: "therecord" },
  { name: "Securelist", slug: "securelist" },
  { name: "Bellingcat", slug: "bellingcat" },
  { name: "Check Point", slug: "checkpoint-research" },
  { name: "SentinelOne", slug: "sentinelone-labs" },
  { name: "SANS ISC", slug: "sans-isc" },
  { name: "The Cradle", slug: "thecradle" },
  { name: "C4ISRNET", slug: "c4isrnet" },
  { name: "TechXplore", slug: "techxplore" },
  { name: "Grey Dynamics", slug: "greydynamics" },
  { name: "DCiber", slug: "dciber" },
  { name: "Pepe Escobar", slug: "muckrack-escobar" },
  { name: "Threat Intel", slug: "threatintel-rss" },
];

export function SourceFilter({ activeSlug }: { activeSlug?: string }) {
  return (
    <nav
      aria-label="Filter by source"
      className="flex flex-wrap gap-2 mb-8 pb-6 border-b border-zinc-800"
    >
      {SOURCES.map(({ name, slug }) => {
        const isActive = (activeSlug ?? "") === slug;
        const href = slug ? `/?source=${slug}` : "/";
        return (
          <Link
            key={slug}
            href={href}
            className={`px-3 py-1 font-mono text-xs uppercase tracking-wider rounded-sm border transition-colors duration-150 ${
              isActive
                ? "bg-amber-400 text-zinc-950 border-amber-400 font-bold"
                : "border-zinc-700 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200"
            }`}
          >
            {name}
          </Link>
        );
      })}
    </nav>
  );
}
