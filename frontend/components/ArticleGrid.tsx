import { Article } from "@/lib/types";
import { ArticleCard } from "./ArticleCard";

export function ArticleGrid({ articles }: { articles: Article[] }) {
  if (!articles.length) {
    return (
      <div className="flex flex-col items-center justify-center py-32 gap-3">
        <span className="font-mono text-4xl text-zinc-700">—</span>
        <p className="font-mono text-sm text-zinc-600 uppercase tracking-widest">
          No articles yet
        </p>
        <p className="font-mono text-xs text-zinc-700">
          The scraper runs daily at 06:00 UTC
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      {articles.map((a) => (
        <ArticleCard key={a.id} article={a} />
      ))}
    </div>
  );
}
