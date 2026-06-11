# 🥁 USIU Career Fair — Interactive Booth Suite

> An interactive career fair booth experience for **USIU-Africa**, built with Streamlit and Supabase. Students engage through four games, win real rewards, and every interaction is logged for end-of-day auditing via a Power BI dashboard.


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://career-fair-akinator-2yzgvbty5yfhurjutd3nux.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?logo=supabase&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Games](#games)
  - [Akinator — Guess My Degree](#1-akinator--guess-my-degree)
  - [Spot the CV Mistakes](#2-spot-the-cv-mistakes)
  - [USIU Trivia](#3-usiu-trivia)
  - [Solvo Global Trivia](#4-solvo-global-trivia)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Local Setup](#local-setup)
- [Deployment](#deployment)
- [Analytics Dashboard](#analytics-dashboard)
- [Mascot — Kofi](#mascot--kofi)

---

## Overview

This project replaces the traditional "scan a QR code" approach to career fair booth engagement. Instead of passive lead capture, students play games, compete for real rewards, and naturally share their details through the claim process. The booth operator receives a full reward audit log and engagement analytics out of the box.

**The experience in brief:**

1. Student approaches the booth and picks a game on a shared device
2. They play — games are 1–3 minutes each
3. Top performers win a USIU wristband (CV game, USIU Trivia) or a Solvo water bottle (Solvo Trivia)
4. Winners enter their name and student ID to claim their reward
5. A unique reward code is generated and logged to Supabase
6. Booth staff confirm and hand over the reward

---

## Games

### 1. Akinator — Guess My Degree

> *"Answer a few questions and I'll guess your degree."*

A **Bayesian question engine** that narrows down USIU-Africa's 40 programmes through behaviour-based questions. The algorithm uses **Expected Information Gain (EIG)** to pick the most discriminating question at each step, converging in 5–10 questions on average.

**Key specs:**
- 40 programmes across all 5 USIU-Africa schools
- 58 behavioural questions (personality, interests, work style)
- Confidence threshold: 56% to make a guess
- Min questions: 5 · Max questions: 10 (13 in extended mode)
- Online Bayesian learning: every session updates model weights in Supabase
- Local JSON fallback when Supabase is unreachable

**Files:** `usiu_akinator.py`, `knowledge_base.py`, `bayes_engine.py`, `db.py`

---

### 2. Spot the CV Mistakes

> *"You have 30 seconds. Find the 5 errors in this CV."*

Students tap on errors in a fabricated CV belonging to **Alex Mutua**. Errors span both ATS red flags and recruiter pet peeves — teaching real CV skills while keeping it competitive.

**The 5 errors:**
| # | Error | Category |
|---|---|---|
| 1 | Email typo (`@gmal.com`) | Hard fact error |
| 2 | Photo on CV | ATS / recruiter red flag |
| 3 | Weak objective statement | Soft error |
| 4 | Inconsistent date formatting | Formatting error |
| 5 | Passive language in experience | Language quality |

**Reward:**
| Score | Reward |
|---|---|
| 3 / 5 | Congratulations — no prize |
| 4 / 5 or 5 / 5 | **USIU Wristband** |

**Files:** `cv_game.py`

---

### 3. USIU Trivia

> *"8 questions about your university. Get 7 or 8 right and win a wristband."*

A multiple-choice trivia game about USIU-Africa. Questions are drawn randomly from a **17-question pool** each session and answer options are shuffled — so no two games feel the same.

**Question topics:** founding year, location, motto, vision, WSCUC accreditation, Vice-Chancellor, Chancellor, number of schools, Chandaria School of Business, nationalities on campus, alumni count, and more.

**Scoring:**
| Score | Outcome |
|---|---|
| 0 – 6 / 8 | Game over — correct answers revealed |
| 7 / 8 or 8 / 8 | 🎓 Claim a **USIU Wristband** |

**Files:** `trivia_game.py`

---

### 4. Solvo Global Trivia

> *"8 questions about Solvo and Oasis. Get 7 or 8 right and win a water bottle."*

A branded trivia game built on request for **Solvo Global** and their Kenya partner **Oasis Outsourcing**. Questions are drawn from a **16-question pool** spanning company knowledge, staff recognition, BPO/HR definitions, and a career fair event fact.

**Question categories:**
| Category | Count | Topics |
|---|---|---|
| About Solvo | 2 | What Solvo does · Founder |
| Staff recognition | 4 | Purity · Nalliah · Lilian · Munyuu (phonetic distractors used as wrong options) |
| About Oasis | 3 | What Oasis does · Location (Nairobi) · Services |
| Definitions | 6 | Recruitment · Outsourcing · Remote work · Nearshore staffing · Talent acquisition · Back office |
| Career fair fact | 1 | Event start date |

**Scoring:**
| Score | Outcome |
|---|---|
| 0 – 6 / 8 | Game over — correct answers revealed |
| 7 / 8 or 8 / 8 | 💧 Claim a **Solvo Water Bottle** |

**Files:** `solvo_game.py`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io) — Python-based web UI |
| Games | Self-contained HTML/CSS/JS components via `st.components.v1.html` |
| Backend / DB | [Supabase](https://supabase.com) — hosted PostgreSQL (West EU / Ireland region) |
| Mascot | Custom SVG character (Kofi) — hand-coded, fully animated |
| Dashboard | [Power BI Desktop + Service](https://powerbi.microsoft.com) — PostgreSQL direct connection, hourly refresh |
| Deployment | [Streamlit Cloud](https://streamlit.io/cloud) |

---

## Project Structure

```
Career_fair/
│
├── usiu_akinator.py        # Main app — routing, landing page (2×2 game grid), all pages
├── knowledge_base.py       # 40 USIU programmes, 58 questions, school definitions
├── bayes_engine.py         # Bayesian scoring engine + EIG question selection
├── db.py                   # Supabase persistence layer + local JSON fallback
├── kofi.py                 # Kofi mascot SVG — kofi_html(state) → HTML string
│
├── cv_game.py              # CV Spot-the-Error game (self-contained HTML component)
├── trivia_game.py          # USIU Trivia — wristband reward (self-contained HTML component)
├── solvo_game.py           # Solvo Global Trivia — water bottle reward (partner game)
│
├── simulator.py            # Bayesian engine validation simulator
├── supabase_setup.sql      # All table DDL — run once in Supabase SQL Editor
│
├── learning_bayes.json     # Local fallback for Bayesian learning counts
└── requirements.txt        # Python dependencies (streamlit, pandas, numpy, supabase)
```

---

## Database Schema

All data lives in **Supabase PostgreSQL** under the `public` schema. Run `supabase_setup.sql` in the Supabase SQL Editor to create the tables.

### `winners` — Reward audit log

Shared by all three reward games. Every reward claim writes one row.

| Column | Type | Description |
|---|---|---|
| `id` | bigserial PK | Auto-incrementing row ID |
| `name` | text | Player's full name |
| `student_id` | text | Student / staff ID (optional) |
| `game` | text | `'cv_errors'` · `'trivia'` · `'solvo'` |
| `score` | int4 | CV: errors found (4–5) · Trivia/Solvo: questions correct (7–8) |
| `time_left` | int4 | Seconds remaining at end (CV only; null for trivia and Solvo) |
| `reward_ksh` | int4 | Always `0` — no cash prizes. Retained for schema compatibility |
| `reward_code` | text UNIQUE | Auto-generated code — see prefix table below |
| `claimed` | bool | Default `false` — update to `true` when reward is physically handed out |
| `created_at` | timestamptz | Auto-set to `now()` in UTC |

**Reward code prefixes:**
| Prefix | Game | Reward |
|---|---|---|
| `USIU-WRIS-` | cv_errors · trivia | USIU Wristband |
| `SOLV-WBTL-` | solvo | Solvo Water Bottle |

### `game_log` — Akinator session log

| Column | Type | Description |
|---|---|---|
| `id` | bigserial PK | — |
| `type` | text | Game variant identifier |
| `guess` | text | Programme the Akinator guessed |
| `correct` | text | Whether the guess was correct |
| `confidence` | int4 | Model confidence at guess time (0–100) |
| `n_questions` | int4 | Questions asked before guessing |
| `path` | text | Comma-separated question path |
| `created_at` | timestamptz | Auto-set to `now()` |

### `learning_data` — Bayesian learning counts

Stores per-attribute per-response counts. Updated after each Akinator session.

---

## Local Setup

### Prerequisites
- Python 3.10+
- A [Supabase](https://supabase.com) project (free tier works)

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/rhkhabure/Career-fair-akinator.git
cd Career-fair-akinator
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up Supabase secrets**

Create `.streamlit/secrets.toml` in the project root:
```toml
[supabase]
url = "https://YOUR_PROJECT_ID.supabase.co"
key = "your_anon_public_key"
```

> ⚠️ Never commit `secrets.toml` to version control. It is already listed in `.gitignore`.

**4. Initialise the database**

Run `supabase_setup.sql` in your Supabase project's SQL Editor (Dashboard → SQL Editor → New query).

**5. Run the app**
```bash
cd Career_fair
streamlit run usiu_akinator.py
```

The app opens at `http://localhost:8501`.

---

## Deployment

The app is deployed on **Streamlit Cloud** from the `main` branch, pointing to `Career_fair/usiu_akinator.py`.

**To redeploy after changes:**
Push to `main` — Streamlit Cloud auto-detects and rebuilds (usually under 2 minutes).

**To add secrets in Streamlit Cloud:**
App → Settings → Secrets → paste the `[supabase]` block from your local `secrets.toml`.

---

## Analytics Dashboard

A **Power BI** dashboard connects directly to the Supabase PostgreSQL backend for hourly-refreshed analytics.

**Connection details:**
- Connector: PostgreSQL (native Power BI connector)
- Server: `db.YOUR_PROJECT_ID.supabase.co:5432`
- Database: `postgres`
- Tables imported: `public.winners`, `public.game_log`
- SSL: add `sslmode=require` in the Advanced Options field

**Dashboard pages:**
1. **Overview** — KPI cards (total players, wristbands given, water bottles given, game splits), rewards bar chart, hourly traffic column chart
2. **Reward Audit** — full sortable table with game, name, reward type, code, claimed status; filterable by game, date, and claimed flag

**Power Query calculated columns** (add in Transform Data before building visuals):
```
reward_type  =
  if Text.StartsWith([reward_code], "USIU-WRIS") then "Wristband"
  else if Text.StartsWith([reward_code], "SOLV-WBTL") then "Water Bottle"
  else "Other"

game_label   =
  if [game] = "cv_errors" then "CV Mistakes"
  else if [game] = "trivia" then "USIU Trivia"
  else "Solvo Trivia"

hour_of_day  = Time.Hour(DateTime.From([created_at]))
// Add 3 hours for EAT: Time.Hour(DateTime.From([created_at]) + #duration(0,3,0,0))

date_only    = DateTime.Date(DateTime.From([created_at]))
```

**Key DAX measures:**
```dax
Total Players        = COUNTROWS('public winners')
Wristbands Given     = COUNTROWS(FILTER('public winners', LEFT([reward_code],9) = "USIU-WRIS"))
Water Bottles Given  = COUNTROWS(FILTER('public winners', LEFT([reward_code],9) = "SOLV-WBTL"))
CV Game Plays        = CALCULATE(COUNTROWS('public winners'), [game] = "cv_errors")
Trivia Plays         = CALCULATE(COUNTROWS('public winners'), [game] = "trivia")
Solvo Plays          = CALCULATE(COUNTROWS('public winners'), [game] = "solvo")
Rewards Claimed      = CALCULATE(COUNTROWS('public winners'), [claimed] = TRUE())
Claim Rate %         = DIVIDE([Rewards Claimed], [Total Players], 0)
Akinator Games       = COUNTROWS('public game_log')
Total Booth Interactions = [Akinator Games] + [Total Players]
```

---

## Mascot — Kofi

Kofi is a fully hand-coded SVG character who reacts to game events. He lives in `kofi.py` and is called via `kofi_html(state)` which returns a self-contained HTML string.

**States:**
| State | When used |
|---|---|
| `idle` | Landing page |
| `thinking` | Questions being answered |
| `confident` | Akinator confidence ≥ 45% |
| `correct` | Right answer, win screen |
| `wrong` | Wrong answer, low score |

**SVG implementation notes:**
- All game instances use a **permanent zero-size sprite SVG** at the top of the document body holding all `<defs>` (kente pattern, clip-paths). This ensures `url(#...)` references resolve correctly even after multiple `innerHTML` re-insertions — a browser behaviour where dynamically re-inserted SVG content sometimes fails to re-register its own definitions.
- Each game uses unique ID suffixes to prevent collisions: CV game (`-t/-c/-w`), USIU Trivia (`-tt/-tc/-tw`), Solvo Trivia (`-svt/-svc/-svw`).
- Animations use `@keyframes` with `transform-box: fill-box; transform-origin: center` for reliable cross-browser rendering.

---

## Notes

- The `claimed` column defaults to `false` and is never automatically set to `true` by the games. Booth staff must update this manually in Supabase Table Editor when a reward is physically handed out.
- `created_at` is stored in **UTC**. Nairobi is **EAT = UTC+3**. Apply the +3 hour offset in Power Query when building the `hour_of_day` traffic chart.
- The Supabase anon key embedded in the game JS is safe to expose — Row Level Security restricts it to INSERT-only on the `winners` table. It cannot read, update, or delete existing records.
- `reward_ksh` is always `0` in the current version (all cash prizes were removed and replaced with physical merch). The column is retained for schema compatibility with the Power BI model.

---

*Built for the USIU-Africa PACS Career Fair · June 2025*
*Extended live on-site for Solvo Global / Oasis Outsourcing · June 2026*
