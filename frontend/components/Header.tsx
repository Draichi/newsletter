export function Header() {
  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <header className="border-b border-zinc-800 px-4 py-8 mb-2">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col sm:flex-row sm:items-baseline gap-2 sm:gap-5">
          <h1 className="font-serif text-5xl sm:text-6xl font-black tracking-tight text-zinc-50">
            SIGNAL BRIEF
          </h1>
          <span className="font-mono text-xs text-zinc-500 uppercase tracking-widest self-end pb-1">
            Daily Intelligence Digest
          </span>
        </div>
        <p className="font-mono text-xs text-zinc-600 mt-2 uppercase tracking-wider">
          {today}
        </p>
      </div>
    </header>
  );
}
