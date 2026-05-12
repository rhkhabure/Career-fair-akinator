"""
usiu_akinator.py
----------------
USIU Career Fair Akinator — Streamlit app.

Persistence: all learning data is stored in Supabase (see db.py).
Falls back to local JSON files when running without Supabase credentials.
"""

import streamlit as st
import pandas as pd
import math
from typing import Any, Dict, List, Tuple

from knowledge_base import programs, questions, school_questions
from bayes_engine import (
    init_log_scores,
    update_log_scores,
    log_scores_to_probs,
    top_candidates,
    confidence_of_top,
    estimate_eig_bayes,
    compute_attr_boosts,
    build_program_priors,
    record_success,
    record_failure,
    get_top_confusions,
    CONFUSION_PREFIX,
    PROGRAM_FREQ_PREFIX,
)
from db import (
    load_learning_counts,
    save_learning_counts,
    save_game_result,
    fetch_game_stats,
    fetch_confusion_pairs,
    is_supabase_configured,
)

# ─────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.56
MIN_QUESTIONS        = 5
MAX_QUESTIONS        = 10
MAX_QUESTIONS_EXT    = 13

# ─────────────────────────────────────────────────────────────
# Base dataframe
# ─────────────────────────────────────────────────────────────
df            = pd.DataFrame(programs)
df["score"]   = 0.0
PROGRAM_NAMES = list(df["name"].unique())
NAME_TO_ATTRS: Dict[str, set] = {
    row["name"]: set(row["attributes"]) for _, row in df.iterrows()
}

# ─────────────────────────────────────────────────────────────
# Scoring helpers
# ─────────────────────────────────────────────────────────────
def fresh_candidates(log_prior: Dict[str, float]) -> pd.DataFrame:
    return init_log_scores(df.copy(), log_prior)


def recompute_candidates(
    path: List[Tuple[str, str]],
    log_prior: Dict[str, float],
    attr_boost: Dict[str, float],
) -> pd.DataFrame:
    cands = fresh_candidates(log_prior)
    for attr, response in path:
        cands = update_log_scores(cands, attr, response, attr_boost)
    return cands


# ─────────────────────────────────────────────────────────────
# Question selection
# ─────────────────────────────────────────────────────────────
def question_splits_candidates(candidates: pd.DataFrame, qid: str) -> bool:
    tags = questions.get(qid, {}).get("tags", [qid])
    for tag in tags:
        w  = candidates[candidates["attributes"].apply(lambda a: tag in a)]
        wo = candidates[candidates["attributes"].apply(lambda a: tag not in a)]
        if len(w) > 0 and len(wo) > 0:
            return True
    return False


def get_attr_for_qid(qid: str) -> str:
    tags = questions.get(qid, {}).get("tags", [])
    return tags[0] if tags else qid


def infer_top_school(candidates: pd.DataFrame) -> str:
    cands_prob = log_scores_to_probs(candidates)
    school_prob: Dict[str, float] = {}
    for _, row in cands_prob.iterrows():
        s = row.get("school", "")
        school_prob[s] = school_prob.get(s, 0.0) + row["prob"]
    if not school_prob:
        return ""
    top = max(school_prob, key=school_prob.get)
    return top if school_prob[top] >= 0.65 else ""


def get_pending_followup(asked_qids: List[str], history_pairs: List[Tuple[str, str]]) -> str:
    for qid, response in reversed(history_pairs):
        followup = questions.get(qid, {}).get("followups", {})
        for key in (response, "default"):
            for fq in followup.get(key, []):
                if fq and fq not in asked_qids and fq in questions:
                    return fq
    return None


def select_next_question(
    candidates: pd.DataFrame,
    asked_qids: List[str],
    history_pairs: List[Tuple[str, str]],
    attr_boost: Dict[str, float],
) -> Any:
    pending = get_pending_followup(asked_qids, history_pairs)
    if pending:
        return pending

    eig_scores: Dict[str, float] = {}
    for qid in questions:
        if qid in asked_qids or not question_splits_candidates(candidates, qid):
            continue
        attr = get_attr_for_qid(qid)
        eig_scores[qid] = estimate_eig_bayes(candidates, attr, attr_boost)

    if not eig_scores:
        for qid in questions:
            if qid not in asked_qids:
                return qid
        return None

    top_school = infer_top_school(candidates)
    if top_school:
        pool_eig = {q: eig_scores[q] for q in school_questions.get(top_school, []) if q in eig_scores}
        if pool_eig:
            best_pool   = max(pool_eig, key=pool_eig.get)
            best_global = max(eig_scores, key=eig_scores.get)
            if eig_scores[best_pool] >= 0.8 * eig_scores[best_global]:
                return best_pool

    return max(eig_scores, key=eig_scores.get)


# ─────────────────────────────────────────────────────────────
# Streamlit UI
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="USIU Career Fair Akinator 🦉", layout="centered")


def _init_session():
    counts     = load_learning_counts()
    attr_boost = compute_attr_boosts(counts)
    log_prior  = build_program_priors(counts, PROGRAM_NAMES)
    st.session_state.page            = "landing"
    st.session_state.learning_counts = counts
    st.session_state.attr_boost      = attr_boost
    st.session_state.log_prior       = log_prior
    st.session_state.candidates      = fresh_candidates(log_prior)
    st.session_state.asked           = []
    st.session_state.asked_qids      = []
    st.session_state.history_pairs   = []
    st.session_state.final_guess     = None
    st.session_state.show_correction = False
    st.session_state.max_questions   = MAX_QUESTIONS
    st.session_state._needs_rerun    = False


if "page" not in st.session_state:
    _init_session()

if st.session_state.get("_needs_rerun", False):
    st.session_state._needs_rerun = False
    st.rerun()


def _reset_game():
    counts     = load_learning_counts()
    attr_boost = compute_attr_boosts(counts)
    log_prior  = build_program_priors(counts, PROGRAM_NAMES)
    st.session_state.learning_counts = counts
    st.session_state.attr_boost      = attr_boost
    st.session_state.log_prior       = log_prior
    st.session_state.candidates      = fresh_candidates(log_prior)
    st.session_state.asked           = []
    st.session_state.asked_qids      = []
    st.session_state.history_pairs   = []
    st.session_state.final_guess     = None
    st.session_state.show_correction = False
    st.session_state.max_questions   = MAX_QUESTIONS
    st.session_state._needs_rerun    = False
    st.session_state.page            = "landing"
    for k in [k for k in st.session_state.keys()
              if k.startswith("q_") or k == "correction_select"]:
        del st.session_state[k]


# ── Landing ───────────────────────────────────────────────────
if st.session_state.page == "landing":
    st.title("🦉 USIU Career Fair Akinator")
    try:
        st.image("owl_placeholder.png", width=180)
    except Exception:
        pass
    st.markdown(
        "Think of your **degree programme** at USIU-Africa…  \n"
        "I'll try to guess it in **10 questions or fewer!**"
    )
    if st.button("▶ Play", type="primary"):
        _reset_game()
        st.session_state.page = "questions"
        st.rerun()


# ── Answer callback ───────────────────────────────────────────
def handle_answer(qid: str, q_index: int):
    key      = f"q_{q_index}"
    response = st.session_state.get(key)
    if response is None or q_index != len(st.session_state.asked_qids):
        return

    attr = get_attr_for_qid(qid)
    st.session_state.candidates = update_log_scores(
        st.session_state.candidates, attr, response, st.session_state.attr_boost
    )
    st.session_state.asked.append((attr, response))
    st.session_state.asked_qids.append(qid)
    st.session_state.history_pairs.append((qid, response))

    n_asked = len(st.session_state.asked_qids)
    conf    = confidence_of_top(st.session_state.candidates)

    if n_asked >= MIN_QUESTIONS and conf >= CONFIDENCE_THRESHOLD:
        st.session_state.page = "guess"
    elif n_asked >= st.session_state.max_questions:
        if conf < 0.45 and st.session_state.max_questions == MAX_QUESTIONS:
            st.session_state.max_questions = MAX_QUESTIONS_EXT
        else:
            st.session_state.page = "guess"

    st.session_state._needs_rerun = True


# ── Questions ─────────────────────────────────────────────────
if st.session_state.page == "questions":
    qid = select_next_question(
        st.session_state.candidates,
        st.session_state.asked_qids,
        st.session_state.history_pairs,
        st.session_state.attr_boost,
    )

    if qid is None or len(st.session_state.asked_qids) >= st.session_state.max_questions:
        st.session_state.page = "guess"
        st.rerun()
    else:
        q_index = len(st.session_state.asked_qids)
        qmeta   = questions.get(qid, {})
        q_text  = qmeta.get("text", f"Question about {qid}")

        st.progress(
            q_index / st.session_state.max_questions,
            text=f"Question {q_index + 1} of {st.session_state.max_questions}"
        )
        st.subheader(f"Q{q_index + 1}: {q_text}")

        with st.expander("🔍 My current thinking…", expanded=False):
            top3 = top_candidates(st.session_state.candidates, n=3)
            for _, row in top3.iterrows():
                pct = int(row["prob"] * 100)
                st.markdown(f"**{row['name']}** ({row['level']}) — `{pct}%`")
                st.progress(row["prob"])

        key = f"q_{q_index}"
        if key not in st.session_state:
            st.session_state[key] = None

        if qmeta.get("type") == "multi":
            st.selectbox(
                "Your answer:",
                qmeta.get("responses", ["None"]),
                key=key,
                on_change=handle_answer,
                args=(qid, q_index),
            )
        else:
            st.radio(
                "Your answer:",
                qmeta.get("responses", ["Definitely Yes","Probably Yes","Neutral","Probably No","Definitely No"]),
                index=None,
                key=key,
                on_change=handle_answer,
                args=(qid, q_index),
            )

        if st.button("← Go Back", disabled=(q_index == 0)):
            if st.session_state.asked_qids:
                st.session_state.asked_qids.pop()
                st.session_state.asked.pop()
                st.session_state.history_pairs.pop()
                st.session_state.candidates = recompute_candidates(
                    st.session_state.asked,
                    st.session_state.log_prior,
                    st.session_state.attr_boost,
                )
                prev_key = f"q_{len(st.session_state.asked_qids)}"
                if prev_key in st.session_state:
                    del st.session_state[prev_key]
                st.rerun()


# ── Guess ─────────────────────────────────────────────────────
if st.session_state.page == "guess":
    if st.session_state.candidates is None or st.session_state.candidates.empty:
        st.session_state.candidates = fresh_candidates(st.session_state.log_prior)

    top3 = top_candidates(st.session_state.candidates, n=3)
    best = top3.iloc[0]
    st.session_state.final_guess = best["name"]
    conf_pct = int(best["prob"] * 100)

    st.markdown("## 🎯 My guess is…")
    st.success(
        f"**{best['name']}**  \n"
        f"_{best['level']} · {best['school']}_  \n"
        f"Confidence: **{conf_pct}%**"
    )
    try:
        st.image("degree_placeholder.png", width=160)
    except Exception:
        pass

    if len(top3) > 1:
        runner = top3.iloc[1]
        st.caption(
            f"Runner-up: {runner['name']} ({runner['level']}) "
            f"— {int(runner['prob']*100)}%"
        )

    col1, col2 = st.columns(2)

    if col1.button("✅ Yes, correct!", type="primary"):
        st.balloons()
        st.markdown("🎉 Great! Thanks for playing.")
        counts = st.session_state.learning_counts
        counts = record_success(counts, st.session_state.final_guess, st.session_state.asked)
        save_learning_counts(counts)
        st.session_state.learning_counts = counts
        st.session_state.attr_boost = compute_attr_boosts(counts)
        save_game_result({
            "type":        "SUCCESS",
            "guess":       st.session_state.final_guess,
            "correct":     st.session_state.final_guess,
            "confidence":  conf_pct,
            "n_questions": len(st.session_state.asked_qids),
            "path":        [list(p) for p in st.session_state.asked],
        })
        st.session_state.show_correction = False

    if col2.button("❌ No, wrong guess"):
        st.session_state.show_correction = True

    if st.session_state.show_correction:
        correct_program = st.selectbox(
            "What's your actual programme?",
            sorted(df["name"].unique()),
            key="correction_select",
        )
        if st.button("Confirm & submit"):
            st.markdown("🤔 Thanks! I'll learn from this.")
            counts = st.session_state.learning_counts
            counts = record_failure(
                counts,
                guessed_name=st.session_state.final_guess,
                correct_name=correct_program,
                path=st.session_state.asked,
                name_to_attrs=NAME_TO_ATTRS,
            )
            save_learning_counts(counts)
            st.session_state.learning_counts = counts
            st.session_state.attr_boost = compute_attr_boosts(counts)
            save_game_result({
                "type":        "FAIL",
                "guess":       st.session_state.final_guess,
                "correct":     correct_program,
                "confidence":  conf_pct,
                "n_questions": len(st.session_state.asked_qids),
                "path":        [list(p) for p in st.session_state.asked],
            })
            st.session_state.show_correction = False

    st.divider()
    if st.button("🔄 Play Again"):
        _reset_game()
        st.session_state.page = "landing"
        st.rerun()


# ── Sidebar diagnostics ───────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛠 Diagnostics")
    storage_status = "☁️ Supabase" if is_supabase_configured() else "💾 Local file"
    st.caption(f"Storage: **{storage_status}**")

    if st.checkbox("Show live stats"):
        stats = fetch_game_stats()
        if stats:
            col_a, col_b = st.columns(2)
            col_a.metric("Total games", stats.get("total_games", 0))
            col_b.metric("Accuracy",    f"{stats.get('accuracy', 0)}%")
            col_a.metric("Avg questions",   stats.get("avg_questions", "—"))
            col_b.metric("Avg confidence",  f"{stats.get('avg_confidence', 0)}%")
        else:
            st.info("No game stats yet.")

        confusions = fetch_confusion_pairs(limit=8)
        if confusions:
            st.markdown("**Most common mistakes:**")
            for row in confusions:
                st.write(
                    f"Guessed **{row['guessed']}** → "
                    f"actually **{row['correct']}** ({row['count']}×)"
                )

        st.markdown("**Top attribute signals:**")
        boosts = sorted(
            st.session_state.attr_boost.items(), key=lambda x: -abs(x[1])
        )[:10]
        for attr, boost in boosts:
            sign = "▲" if boost > 0 else "▼"
            st.write(f"{sign} `{attr}`: {boost:+.2f}")
