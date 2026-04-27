import { Article } from "@/lib/types";
import { DateBadge } from "./DateBadge";

export function ArticleCard({ article }: { article: Article }) {
  const date = article.published_at ?? article.scraped_at;

  return (
    <article className="group border border-zinc-800 rounded-sm p-5 hover:border-zinc-600 transition-colors duration-200 flex flex-col gap-3">
      <div className="flex items-center justify-between gap-2">
        <span className="font-mono text-xs uppercase tracking-widest text-amber-400 truncate">
          {article.source_name}
        </span>
        <DateBadge date={date} />
      </div>

      <h2 className="font-serif text-xl font-bold leading-snug text-zinc-50">
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-amber-300 transition-colors duration-150"
        >
          {article.title}
        </a>
      </h2>

      {article.summary && (
        <p className="font-mono text-sm text-zinc-400 leading-relaxed line-clamp-4">
          {article.summary}
        </p>
      )}

      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="font-mono text-xs text-zinc-600 hover:text-amber-400 transition-colors duration-150 mt-auto"
      >
        Read original →
      </a>
    </article>
  );
}
