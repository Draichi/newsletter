# Signal Brief

A daily news aggregator focused on cybersecurity, threat intelligence, and geopolitical analysis. A GitHub Action scrapes 13 news sites + 1 RSS feed every day, summarizes articles with Gemini Flash 1.5, and displays them on a dark newspaper-style website.

**Stack:** Python · Next.js 14 · Supabase · Vercel · GitHub Actions

---

## How it works

1. GitHub Action runs daily at 06:00 UTC
2. Python scraper fetches the latest articles from each source
3. New articles are batched into a single Gemini Flash 1.5 API call for summarization
4. Summarized articles are upserted into Supabase (deduped by URL)
5. The Next.js frontend reads from Supabase and renders the articles

---

## Prerequisites

- Python 3.12+
- Node.js 18+
- A [Supabase](https://supabase.com) project (free tier is enough)
- A [Gemini API key](https://aistudio.google.com/app/apikey) (free, no credit card required)
- A [Vercel](https://vercel.com) account for frontend deployment

---

## 1. Database setup

In your Supabase project, go to **SQL Editor** and run the contents of `supabase-schema.sql`. This creates the `articles` table, indexes, and Row Level Security policies.

---

## 2. Running the scraper locally

```bash
cd scraper
pip install -r requirements.txt
```

Create a `.env` file inside `scraper/`:

```bash
GEMINI_API_KEY=your_gemini_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
```

Load the variables and run:

```bash
export $(cat .env | xargs)
python main.py
```

You should see logs like:

```
2026-04-27T06:00:01 INFO Scraping: Dark Reading
2026-04-27T06:00:03 INFO   Dark Reading: 3 scraped, 3 new
...
2026-04-27T06:00:45 INFO Total new articles to summarize: 38
2026-04-27T06:01:10 INFO Upserted 38 articles to Supabase
```

---

## 3. Running the frontend locally

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

Start the dev server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

> The page will be empty until you run the scraper at least once to populate the database.

---

## 4. GitHub Actions setup

Push the repository to GitHub. Then go to **Settings → Secrets and variables → Actions** and add the following secrets:

| Secret | Where to find it |
|---|---|
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| `SUPABASE_URL` | Supabase → Settings → API → Project URL |
| `SUPABASE_ANON_KEY` | Supabase → Settings → API → anon public |
| `VERCEL_DEPLOY_HOOK` | *(optional)* Vercel → Project → Settings → Git → Deploy Hooks |

The workflow runs automatically every day at 06:00 UTC. To trigger it manually, go to **Actions → Daily News Scrape & Summarize → Run workflow**.

---

## 5. Deploying the frontend to Vercel

1. Import the repository in Vercel
2. Set the **Root Directory** to `frontend`
3. Add the following environment variables in **Project Settings → Environment Variables**:

| Variable | Value | Scope |
|---|---|---|
| `SUPABASE_URL` | `https://your-project.supabase.co` | Server only |
| `SUPABASE_SERVICE_ROLE_KEY` | service_role key from Supabase | Server only |
| `NEXT_PUBLIC_SUPABASE_URL` | same URL | All |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | anon key from Supabase | All |
| `NEXT_PUBLIC_BASE_URL` | `https://your-app.vercel.app` | All |

4. Deploy. Vercel auto-detects Next.js and builds accordingly.

> `SUPABASE_SERVICE_ROLE_KEY` must **never** have the `NEXT_PUBLIC_` prefix — it has full database access and must stay server-side only.

---

## Supabase key locations

Go to your Supabase project → **Settings → API**:

- **Project URL** → `SUPABASE_URL`
- **anon public** → `SUPABASE_ANON_KEY`
- **service_role** (click Reveal) → `SUPABASE_SERVICE_ROLE_KEY`

---

## Tuning scrapers

The CSS selectors in `scraper/config.py` may need adjustments as sites redesign. After the first run, check the logs for any source reporting `0 scraped` — those selectors need updating.

If a site blocks the scraper with a 403, it falls back automatically to `cloudscraper`. For persistent blocks, check if the site offers an RSS feed and switch the config `type` to `"rss"`.

---

## Project structure

```
daily-news-summary/
├── .github/workflows/daily-scrape.yml   # cron job
├── scraper/
│   ├── main.py          # entry point
│   ├── config.py        # per-site CSS selector configs
│   ├── scraper.py       # HTML scraping engine
│   ├── rss_reader.py    # RSS feed reader
│   ├── summarizer.py    # Gemini Flash 1.5 summarization
│   ├── db.py            # Supabase upsert logic
│   └── requirements.txt
├── frontend/            # Next.js 14 app
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── api/articles/route.ts
│   └── components/
│       ├── Header.tsx
│       ├── SourceFilter.tsx
│       ├── ArticleGrid.tsx
│       ├── ArticleCard.tsx
│       └── DateBadge.tsx
├── supabase-schema.sql
└── news-websites.txt
```
