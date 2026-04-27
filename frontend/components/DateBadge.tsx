"use client";

export function DateBadge({ date }: { date: string }) {
  const d = new Date(date);
  if (isNaN(d.getTime())) return null;

  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffH = diffMs / (1000 * 60 * 60);

  let label: string;
  if (diffH < 1) {
    label = `${Math.floor(diffMs / 60000)}m ago`;
  } else if (diffH < 24) {
    label = `${Math.floor(diffH)}h ago`;
  } else {
    label = d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  }

  return (
    <time
      dateTime={d.toISOString()}
      className="font-mono text-xs text-zinc-500"
    >
      {label}
    </time>
  );
}
