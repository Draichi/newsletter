import { createClient } from "@supabase/supabase-js";
import { NextRequest, NextResponse } from "next/server";

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const slug = searchParams.get("source");

  let query = supabase
    .from("articles")
    .select(
      "id, url, source_name, source_slug, title, summary, published_at, scraped_at, image_url"
    )
    .not("summary", "is", null)
    .order("scraped_at", { ascending: false })
    .limit(60);

  if (slug) {
    query = query.eq("source_slug", slug);
  }

  const { data, error } = await query;

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json(data, {
    headers: {
      "Cache-Control": "public, s-maxage=1800, stale-while-revalidate=3600",
    },
  });
}
