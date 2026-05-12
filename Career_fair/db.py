"""
db.py
-----
Supabase persistence layer for the USIU Akinator.

All load/save operations go through this module.
Falls back to local JSON files automatically when:
  - Running locally without secrets configured
  - Supabase is temporarily unreachable

Supabase tables required (run the SQL in README_SUPABASE.md):
  learning_data  – stores attr|response counts (the Bayesian model)
  game_log       – stores every completed game (for analytics)
"""

import json
import os
from typing import Dict, List

import streamlit as st

# ─────────────────────────────────────────────────────────────
# Local fallback paths (used when Supabase is not configured)
# ─────────────────────────────────────────────────────────────
LOCAL_LEARNING_FILE = "learning_bayes.json"


# ─────────────────────────────────────────────────────────────
# Supabase client  (singleton, cached for the whole server process)
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def _get_supabase_client():
    """
    Returns a Supabase client, or None if credentials are not configured.
    Uses st.cache_resource so only one client is created per server instance.
    """
    try:
        from supabase import create_client
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception:
        return None


def _supabase():
    """Shorthand to get client. Returns None if not configured."""
    return _get_supabase_client()


def is_supabase_configured() -> bool:
    return _supabase() is not None


# ─────────────────────────────────────────────────────────────
# Learning counts  (the Bayesian model)
# ─────────────────────────────────────────────────────────────

def load_learning_counts() -> Dict[str, Dict[str, int]]:
    """
    Load all attr|response counts from Supabase.
    Falls back to local JSON file if Supabase is not available.
    """
    client = _supabase()

    if client:
        try:
            # Fetch all rows — table is small (<5000 rows) so one call is fine
            result = client.table("learning_data").select("key, success, trials").execute()
            counts = {}
            for row in result.data:
                counts[row["key"]] = {
                    "success": int(row["success"]),
                    "trials":  int(row["trials"]),
                }
            return counts
        except Exception as e:
            st.warning(f"⚠️ Supabase load failed, using local fallback. ({e})")

    # ── Local fallback ────────────────────────────────────────
    if os.path.exists(LOCAL_LEARNING_FILE):
        try:
            with open(LOCAL_LEARNING_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    k: {"success": int(v.get("success", 0)),
                        "trials":  int(v.get("trials", 0))}
                    for k, v in data.items()
                }
        except Exception:
            pass
    return {}


def save_learning_counts(counts: Dict[str, Dict[str, int]]):
    """
    Save all counts to Supabase via upsert (insert or update on conflict).
    Also mirrors to the local file for debugging / local use.
    Runs in small batches to stay within Supabase free-tier limits.
    """
    client = _supabase()

    if client:
        try:
            rows = [
                {"key": k, "success": v["success"], "trials": v["trials"]}
                for k, v in counts.items()
            ]
            # Batch upsert — Supabase free tier handles ~500 rows/request fine
            BATCH = 200
            for i in range(0, len(rows), BATCH):
                client.table("learning_data").upsert(
                    rows[i : i + BATCH],
                    on_conflict="key",
                ).execute()
        except Exception as e:
            st.warning(f"⚠️ Supabase save failed, writing locally only. ({e})")

    # ── Always mirror to local file (useful for local dev + debugging) ──
    try:
        with open(LOCAL_LEARNING_FILE, "w", encoding="utf-8") as f:
            json.dump(counts, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def atomic_increment(attr: str, response: str, delta_success: int, delta_trials: int):
    """
    Increment a single attr|response pair atomically using an RPC call.
    This avoids the read-modify-write race condition when two games
    finish simultaneously.

    Falls back to a full save if the RPC is not available.
    """
    client = _supabase()
    key = f"{attr}|{response}"

    if client:
        try:
            # Call the Postgres function defined in README_SUPABASE.md
            client.rpc("increment_learning", {
                "p_key":           key,
                "p_delta_success": delta_success,
                "p_delta_trials":  delta_trials,
            }).execute()
            return
        except Exception:
            pass  # fall through to full save


def save_game_result(entry: dict):
    """
    Append a completed game record to the game_log table.
    entry should have keys: type, guess, correct (optional),
    confidence, n_questions, path (list of [attr, response] pairs).
    """
    client = _supabase()

    if client:
        try:
            client.table("game_log").insert({
                "type":        entry.get("type"),
                "guess":       entry.get("guess"),
                "correct":     entry.get("correct"),
                "confidence":  entry.get("confidence"),
                "n_questions": entry.get("n_questions"),
                "path":        json.dumps(entry.get("path", [])),
            }).execute()
            return
        except Exception as e:
            st.warning(f"⚠️ Could not log game to Supabase. ({e})")

    # ── Local fallback log ────────────────────────────────────
    try:
        with open("path_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────
# Analytics helpers (used by the sidebar diagnostics panel)
# ─────────────────────────────────────────────────────────────

def fetch_game_stats() -> dict:
    """
    Returns a summary dict:
      total_games, correct_games, accuracy, avg_questions, avg_confidence
    """
    client = _supabase()
    if not client:
        return {}

    try:
        result = client.table("game_log").select(
            "type, confidence, n_questions"
        ).execute()
        rows = result.data
        if not rows:
            return {}

        total     = len(rows)
        correct   = sum(1 for r in rows if r["type"] == "SUCCESS")
        avg_q     = sum(r["n_questions"] or 0 for r in rows) / total
        avg_conf  = sum(r["confidence"]  or 0 for r in rows) / total

        return {
            "total_games":   total,
            "correct_games": correct,
            "accuracy":      round(correct / total * 100, 1),
            "avg_questions": round(avg_q, 1),
            "avg_confidence": round(avg_conf, 1),
        }
    except Exception:
        return {}


def fetch_confusion_pairs(limit: int = 10) -> List[dict]:
    """
    Returns the most common (guessed, correct) pairs from game_log.
    """
    client = _supabase()
    if not client:
        return []

    try:
        result = client.table("game_log").select(
            "guess, correct"
        ).eq("type", "FAIL").execute()

        from collections import Counter
        pairs = Counter()
        for r in result.data:
            g = r.get("guess") or ""
            c = r.get("correct") or ""
            if g and c and g != c:
                pairs[(g, c)] += 1

        return [
            {"guessed": g, "correct": c, "count": n}
            for (g, c), n in pairs.most_common(limit)
        ]
    except Exception:
        return []
