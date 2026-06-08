# 🥁 USIU Career Fair — Interactive Booth Suite

> An interactive career fair booth experience for **USIU-Africa**, built with Streamlit and Supabase. Students engage through three games, win real cash rewards, and every interaction is logged for end-of-day auditing via a Power BI dashboard.

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
  - [USIU Trivia + Spin to Win](#3-usiu-trivia--spin-to-win)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Local Setup](#local-setup)
- [Deployment](#deployment)
- [Analytics Dashboard](#analytics-dashboard)
- [Mascot — Kofi](#mascot--kofi)

---

## Overview

This project replaces the traditional "scan a QR code" approach to career fair booth engagement. Instead of passive lead capture, students play games, compete for real prizes, and naturally share information through the claim process. The booth operator gets a full reward audit log and engagement analytics out of the box.

**The experience in brief:**

1. Student approaches the booth and picks a game on a shared device
2. They play — games are 1–3 minutes each
3. Top performers unlock a **Spin to Win** wheel (Trivia) or cash/reward tiers (CV)
4. Winners submit their name and student ID to claim their reward
5. A unique reward code is generated and logged to Supabase
6. Booth staff confirm and mark rewards as claimed in real time

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
- Online Bayesian learning: every session updates the model weights in Supabase
- Local JSON fallback when Supabase is unreachable

**Files:** `usiu_akinator.py`, `knowledge_base.py`, `bayes_engine.py`, `db.py`

---

### 2. Spot the CV Mistakes

> *"You have 30 seconds. Find the 5 errors in this CV."*

Students tap/click on errors in a fabricated CV belonging to **Alex Mutua**. Errors span both ATS red flags and recruiter pet peeves — teaching real CV skills while keeping it competitive.

**The 5 errors:**
| # | Error | Category |
|---|---|---|
| 1 | Email typo (`@gmal.com`) | Hard fact error |
| 2 | Photo on CV | ATS / recruiter red flag |
| 3 | Weak objective statement | Soft error |
| 4 | Inconsistent date formatting | Formatting error |
| 5 | Passive language in experience | Language quality |

**Reward tiers:**
| Score | Reward |
|---|---|
| 3 / 5 | Congratulations — no prize |
| 4 / 5 | **Ksh 50** |
| 5 / 5 | **Ksh 100** |

**Files:** `cv_game.py`

---

### 3. USIU Trivia + Spin to Win

> *"8 questions about your university. Get 7 or 8 right and spin the wheel."*

A timed multiple-choice trivia game about USIU-Africa. Questions are drawn randomly from a **17-question pool** each session, and answer options are shuffled — so no two games feel the same.

**Question topics include:** founding year, location, motto, vision, WSCUC accreditation, Vice-Chancellor, Chancellor, number of schools, Chandaria School of Business, nationalities on campus, alumni count, and more.

**Scoring:**
| Score | Outcome |
|---|---|
| 0 – 6 / 8 | Game over — correct answers revealed |
| 7 / 8 or 8 / 8 | 🎰 Unlocks the Spin to Win wheel |

**Spin wheel — 8 equal segments (12.5% each):**

| Prize | Qty | Probability |
|---|---|---|
| Ksh 100 | 1 | 12.5% |
| Ksh 50 | 2 | 25% |
| Ksh 20 | 2 | 25% |
| Wristband | 1 | 12.5% |
| Second Chance | 1 | 12.5% |
| Nothing | 1 | 12.5% |

*Second Chance grants an immediate re-spin. Nothing results are not logged to Supabase.*

**Files:** `trivia_game.py`

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
├── usiu_akinator.py        # Main app — routing, landing page, all page sections
├── knowledge_base.py       # 40 USIU programmes, 58 questions, school definitions
├── bayes_engine.py         # Bayesian scoring engine + EIG question selection
├── db.py                   # Supabase persistence layer + local JSON fallback
├── kofi.py                 # Kofi mascot SVG — kofi_html(state) → HTML string
│
├── cv_game.py              # CV Spot-the-Error game (self-contained HTML component)
├── trivia_game.py          # USIU Trivia + Spin to Win (self-contained HTML component)
│
├── simulator.py            # Bayesian engine validation simulator
├── supabase_setup.sql      # All table DDL — run once in Supabase SQL Editor
│
├── learning_bayes.json     # Local fallback for Bayesian learning counts
└── requirements.txt        # Python dependencies
```

```
requirements.txt
├── streamlit
├── pandas
├── numpy
└── supabase
```

---

## Database Schema

All data lives in **Supabase PostgreSQL** under the `public` schema. Run `supabase_setup.sql` in the Supabase SQL Editor to create the tables.

### `winners` — Reward audit log

Shared by both CV and Trivia games. Every reward claim writes one row.

| Column | Type | Description |
|---|---|---|
| `id` | bigserial PK | Auto-incrementing row ID |
| `name` | text | Player's full name (from claim form) |
| `student_id` | text | Student / staff ID (optional) |
| `game` | text | `'cv_errors'` or `'trivia'` |
| `score` | int4 | CV: errors found (1–5) · Trivia: questions correct (7–8) |
| `time_left` | int4 | Seconds remaining at end (CV only; null for Trivia) |
| `reward_ksh` | int4 | Cash amount (20 / 50 / 100) or 0 for wristband |
| `reward_code` | text UNIQUE | Auto-generated code e.g. `USIU-KSH5-MN3XRK` |
| `claimed` | bool | Default `false` — update to `true` when reward is physically handed out |
| `created_at` | timestamptz | Auto-set to `now()` in UTC |

**Reward code prefixes** (used for type detection in Power BI):
- `USIU-KSH1-` → Ksh 100
- `USIU-KSH5-` → Ksh 50
- `USIU-KSH2-` → Ksh 20
- `USIU-WRIS-` → Wristband

### `game_log` — Akinator session log

| Column | Type | Description |
|---|---|---|
| `id` | bigserial PK | — |
| `type` | text | Game variant identifier |
| `guess` | text | Programme the Akinator guessed |
| `correct` | text | Whether the guess was correct |
| `confidence` | int4 | Model confidence at time of guess (0–100) |
| `n_questions` | int4 | Number of questions asked before guessing |
| `path` | text | Comma-separated question path taken |
| `created_at` | timestamptz | Auto-set to `now()` |

### `learning_data` — Bayesian learning counts

Stores per-attribute per-response counts that the Bayesian engine learns from. Updated after each Akinator session.

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
1. Push changes to `main`
2. Streamlit Cloud auto-detects and rebuilds (usually < 2 minutes)

**To add secrets in Streamlit Cloud:**
- App → Settings → Secrets → paste the `[supabase]` block from your local `secrets.toml`

---

## Analytics Dashboard

A **Power BI** dashboard connects directly to the Supabase PostgreSQL backend for hourly-refreshed analytics.

**Connection details:**
- Connector: PostgreSQL (native Power BI connector)
- Server: `db.YOUR_PROJECT_ID.supabase.co:5432`
- Database: `postgres`
- Tables: `public.winners`, `public.game_log`
- SSL: `sslmode=require` (add in Advanced Options)

**Dashboard pages:**
1. **Overview** — KPI cards (total players, cash distributed, wristbands, game split), rewards bar chart, game-split donut, hourly traffic column chart
2. **Reward Audit** — full sortable table with game, name, reward, code, claimed status; filterable by game, date, and claimed flag

**Power Query calculated columns** (add before building visuals):
```
reward_type  = if Text.StartsWith([reward_code],"USIU-WRIS") then "Wristband"
                else if [reward_ksh]=100 then "Ksh 100"
                else if [reward_ksh]=50  then "Ksh 50"
                else "Ksh 20"

game_label   = if [game]="cv_errors" then "CV Mistakes" else "USIU Trivia"

hour_of_day  = Time.Hour(DateTime.From([created_at]))    -- adjust +3 for EAT

date_only    = DateTime.Date(DateTime.From([created_at]))
```

---

## Mascot — Kofi

Kofi is a fully hand-coded SVG character who reacts to game events. He lives in `kofi.py` and is called via `kofi_html(state)` which returns a self-contained HTML string.

**States:**
| State | When used |
|---|---|
| `idle` | Landing page |
| `thinking` | Questions being answered, waiting for spin |
| `confident` | Akinator confidence ≥ 45% |
| `correct` | Right answer, winning spin result, high score |
| `wrong` | Wrong answer, low score, Nothing spin |

**SVG implementation notes:**
- All Kofi instances share a **permanent zero-size sprite SVG** at the top of the document body that holds all `<defs>` (kente pattern, clip-paths). This ensures `url(#...)` pattern references resolve correctly even after multiple `innerHTML` re-insertions.
- Each game instance uses unique ID suffixes (`-tt`, `-tc`, `-tw`) to prevent collisions when multiple states are in the DOM simultaneously.
- Animations use `@keyframes` with `transform-box: fill-box; transform-origin: center` for reliable cross-browser rendering.

---

## Notes

- The `claimed` column in `winners` defaults to `false` and is never automatically set to `true` by the games. Booth staff must update this manually in Supabase (Table Editor → find row → toggle `claimed`) when a reward is physically handed out, or build a separate admin tool for bulk updates.
- `created_at` is stored in **UTC**. Nairobi is **EAT = UTC+3**. Add 3 hours when displaying times in Power BI for local accuracy.
- The Supabase anon key used in the JS claim forms is safe to expose — it is INSERT-only by Row Level Security (RLS) policy. It cannot read, update, or delete existing records.

---

*Built for the USIU-Africa PACS Career Fair · June 2025*
