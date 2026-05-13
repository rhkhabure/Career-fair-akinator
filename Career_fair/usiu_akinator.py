"""
usiu_akinator.py  — USIU Career Fair Akinator
Redesigned with USIU brand colours, course cards, and butterfly celebration.
"""

import streamlit as st
import pandas as pd
from typing import Any, Dict, List, Tuple

from knowledge_base import programs, questions, school_questions
from bayes_engine import (
    init_log_scores, update_log_scores, log_scores_to_probs,
    top_candidates, confidence_of_top, estimate_eig_bayes,
    compute_attr_boosts, build_program_priors,
    record_success, record_failure,
    CONFUSION_PREFIX, PROGRAM_FREQ_PREFIX,
)
from db import (
    load_learning_counts, save_learning_counts, save_game_result,
    fetch_game_stats, fetch_confusion_pairs, is_supabase_configured,
)

# ─────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.56
MIN_QUESTIONS        = 5
MAX_QUESTIONS        = 10
MAX_QUESTIONS_EXT    = 13

st.set_page_config(
    page_title="USIU Akinator 🦉",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# USIU Brand colours & global CSS
# Primary: Crimson  #B31B1B
# Secondary: Gold   #F5A623
# Accent: Deep navy #0D1B2A
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ───────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Page background ───────────────────────────────────── */
.stApp {
    background: linear-gradient(145deg, #0D1B2A 0%, #1a2a3a 100%);
    min-height: 100vh;
}

/* ── Sidebar ───────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #111e2b !important;
    border-right: 1px solid #1e3044;
}

/* ── Headings ──────────────────────────────────────────── */
h1 { color: #FFFFFF !important; font-weight: 800 !important; }
h2, h3 { color: #F5A623 !important; font-weight: 700 !important; }
p, li, label { color: #d0dde8 !important; }

/* ── Progress bar ──────────────────────────────────────── */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #B31B1B, #F5A623) !important;
    border-radius: 10px;
}
div[data-testid="stProgress"] > div {
    background: #1e3044 !important;
    border-radius: 10px;
}

/* ── Radio buttons ─────────────────────────────────────── */
div[data-testid="stRadio"] label {
    background: #1a2e42 !important;
    border: 1px solid #2a4060 !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    margin: 4px 0 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    color: #d0dde8 !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #F5A623 !important;
    background: #1e3650 !important;
    color: #F5A623 !important;
}

/* ── Primary button (Play / Correct) ───────────────────── */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #B31B1B, #cc2222) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 0.6rem 1.8rem !important;
    box-shadow: 0 4px 15px rgba(179,27,27,0.4) !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(179,27,27,0.55) !important;
}

/* ── Secondary button ───────────────────────────────────── */
div[data-testid="stButton"] button[kind="secondary"] {
    background: #1a2e42 !important;
    color: #d0dde8 !important;
    border: 1px solid #2a4060 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color: #F5A623 !important;
    color: #F5A623 !important;
}

/* ── Expander ───────────────────────────────────────────── */
details {
    background: #152333 !important;
    border: 1px solid #1e3044 !important;
    border-radius: 12px !important;
}
details summary {
    color: #a0b4c8 !important;
    font-size: 0.9rem !important;
}

/* ── Success box ────────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
}

/* ── Divider ────────────────────────────────────────────── */
hr { border-color: #1e3044 !important; }

/* ── Metric ─────────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: #152333;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #1e3044;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Course card metadata  — emoji icon + school colour
# Drop a real image file named e.g. "img_software_engineering.png"
# into your repo and it will be used automatically.
# ─────────────────────────────────────────────────────────────
COURSE_META: Dict[str, Dict] = {
    # Chandaria
    "International Business Administration": {"icon": "🌍", "color": "#B31B1B"},
    "Accounting":                            {"icon": "📊", "color": "#B31B1B"},
    "Finance":                               {"icon": "💹", "color": "#B31B1B"},
    "Hotel & Restaurant Management":         {"icon": "🏨", "color": "#B31B1B"},
    "Business Administration (MBA)":         {"icon": "💼", "color": "#B31B1B"},
    "Global Leadership & Management":        {"icon": "🧭", "color": "#B31B1B"},
    "Global Banking and Finance":            {"icon": "🏦", "color": "#B31B1B"},
    "Global Business Management":            {"icon": "🌐", "color": "#B31B1B"},
    "Health Leadership and Management":      {"icon": "🏥", "color": "#B31B1B"},
    "Management and Organizational Development": {"icon": "🔄", "color": "#B31B1B"},
    "Doctor of Business Administration":     {"icon": "🎓", "color": "#B31B1B"},
    # Humanities & Social Sciences
    "International Relations":               {"icon": "🕊️", "color": "#1a6b3c"},
    "Psychology":                            {"icon": "🧠", "color": "#1a6b3c"},
    "Criminal Justice Studies":              {"icon": "⚖️", "color": "#1a6b3c"},
    "Sociology":                             {"icon": "👥", "color": "#1a6b3c"},
    "Criminal and Transitional Justice":     {"icon": "🔏", "color": "#1a6b3c"},
    "Clinical Psychology":                   {"icon": "🛋️", "color": "#1a6b3c"},
    "Counseling Psychology":                 {"icon": "💬", "color": "#1a6b3c"},
    "International Relations (MA)":          {"icon": "🗺️", "color": "#1a6b3c"},
    "Marriage and Family Therapy":           {"icon": "❤️", "color": "#1a6b3c"},
    "PhD International Relations":           {"icon": "📜", "color": "#1a6b3c"},
    "Doctor of Psychology (Clinical)":       {"icon": "🔬", "color": "#1a6b3c"},
    # Science & Technology
    "Applied Computer Technology":           {"icon": "🖥️", "color": "#1a4a8a"},
    "Information Systems & Technology":      {"icon": "🗄️", "color": "#1a4a8a"},
    "Data Science & Analytics":              {"icon": "📈", "color": "#1a4a8a"},
    "Artificial Intelligence & Robotics":    {"icon": "🤖", "color": "#1a4a8a"},
    "Software Engineering":                  {"icon": "⚙️", "color": "#1a4a8a"},
    "Information Security":                  {"icon": "🔐", "color": "#1a4a8a"},
    "Information Systems and Technology":    {"icon": "🌐", "color": "#1a4a8a"},
    # Pharmacy & Health Sciences
    "Bachelor of Pharmacy":                  {"icon": "💊", "color": "#6b1a6b"},
    "Nursing":                               {"icon": "🩺", "color": "#6b1a6b"},
    "Epidemiology & Biostatistics":          {"icon": "📋", "color": "#6b1a6b"},
    "Analytical Chemistry":                  {"icon": "🧪", "color": "#6b1a6b"},
    "Applied Biochemistry":                  {"icon": "🧬", "color": "#6b1a6b"},
    "Clinical Pharmacology and Therapeutics":{"icon": "🔭", "color": "#6b1a6b"},
    # Creative Arts
    "Journalism":                            {"icon": "📰", "color": "#7a5c00"},
    "Animation":                             {"icon": "🎨", "color": "#7a5c00"},
    "Film Production & Directing":           {"icon": "🎬", "color": "#7a5c00"},
    "Communication Studies":                 {"icon": "📡", "color": "#7a5c00"},
}

def _course_image_html(name: str, level: str, school: str, conf_pct: int) -> str:
    """Render a styled course card. Swap to <img> if a real photo file exists."""
    import os
    meta = COURSE_META.get(name, {"icon": "🎓", "color": "#B31B1B"})
    icon  = meta["icon"]
    color = meta["color"]

    # Check for a real image file (e.g. img_software_engineering.png)
    slug     = name.lower().replace(" ", "_").replace("&", "and").replace("(", "").replace(")", "")
    img_file = f"img_{slug}.png"
    if os.path.exists(img_file):
        img_tag = f'<img src="{img_file}" style="width:100%;height:180px;object-fit:cover;border-radius:14px 14px 0 0;">'
    else:
        img_tag = f"""
        <div style="
            width:100%; height:180px;
            background: linear-gradient(135deg, {color}cc, {color}55);
            border-radius:14px 14px 0 0;
            display:flex; align-items:center; justify-content:center;
            font-size:5rem;
        ">{icon}</div>"""

    return f"""
    <div style="
        border-radius:14px;
        border: 2px solid {color}88;
        overflow:hidden;
        box-shadow: 0 8px 32px {color}44;
        margin-bottom: 1rem;
    ">
        {img_tag}
        <div style="padding:16px 20px; background:#152333;">
            <div style="font-size:1.35rem; font-weight:800; color:#fff; margin-bottom:4px;">{name}</div>
            <div style="font-size:0.85rem; color:#a0b4c8; margin-bottom:10px;">{level} · {school}</div>
            <div style="
                display:inline-block;
                background: linear-gradient(90deg, #B31B1B, #F5A623);
                color:white; font-weight:700; font-size:0.9rem;
                padding: 4px 14px; border-radius:20px;
            ">Confidence: {conf_pct}%</div>
        </div>
    </div>"""

# ─────────────────────────────────────────────────────────────
# Butterfly + glitter celebration
# ─────────────────────────────────────────────────────────────
def show_celebration():
    st.components.v1.html("""
    <style>
    @keyframes flyUp {
        0%   { transform: translate(0, 0) rotate(0deg) scale(1);   opacity:1; }
        50%  { transform: translate(var(--dx), -45vh) rotate(var(--rot)) scale(1.2); opacity:0.9; }
        100% { transform: translate(calc(var(--dx)*1.6), -100vh) rotate(calc(var(--rot)*2)) scale(0.6); opacity:0; }
    }
    @keyframes wingFlap {
        0%, 100% { transform: scaleX(1); }
        50%       { transform: scaleX(0.4); }
    }
    @keyframes glitter {
        0%   { transform: translate(0,0) rotate(0deg); opacity:1; }
        100% { transform: translate(var(--gx), var(--gy)) rotate(720deg); opacity:0; }
    }
    .butterfly {
        position:fixed;
        font-size: var(--size);
        animation: flyUp var(--dur) ease-in forwards;
        pointer-events:none;
        z-index:9999;
        left: var(--left);
        bottom: -5vh;
    }
    .butterfly-inner { animation: wingFlap 0.35s ease-in-out infinite; }
    .glitter {
        position:fixed;
        width:8px; height:8px;
        border-radius:50%;
        background: var(--gc);
        animation: glitter var(--gdur) ease-out forwards;
        pointer-events:none;
        z-index:9998;
        left: var(--gl); bottom: var(--gb);
    }
    </style>
    <script>
    (function(){
        const BUTTERFLIES = ['🦋','🦋','🦋','🌸','🌺','✨','🌟'];
        const COLORS = ['#F5A623','#B31B1B','#ffffff','#FFE066','#ff88cc','#88ddff','#aaffcc'];
        const body   = document.body;

        // Butterflies
        for(let i=0;i<22;i++){
            const el = document.createElement('div');
            el.className='butterfly';
            const left = Math.random()*95;
            const dx   = (Math.random()-0.5)*60;
            const rot  = (Math.random()-0.5)*720;
            const dur  = 2.2 + Math.random()*2.5;
            const size = (1.4 + Math.random()*1.8)+'rem';
            el.style.cssText=`--left:${left}vw;--dx:${dx}vw;--rot:${rot}deg;--dur:${dur}s;--size:${size};animation-delay:${Math.random()*1.2}s`;
            el.innerHTML=`<div class="butterfly-inner">${BUTTERFLIES[Math.floor(Math.random()*BUTTERFLIES.length)]}</div>`;
            body.appendChild(el);
            setTimeout(()=>el.remove(),(dur+1.5)*1000);
        }

        // Glitter
        for(let i=0;i<60;i++){
            const el=document.createElement('div');
            el.className='glitter';
            const gx=(Math.random()-0.5)*120;
            const gy=30+Math.random()*80;
            const gdur=0.8+Math.random()*1.4;
            const gc=COLORS[Math.floor(Math.random()*COLORS.length)];
            const gl=Math.random()*98;
            const gb=Math.random()*40;
            el.style.cssText=`--gx:${gx}vw;--gy:-${gy}vh;--gdur:${gdur}s;--gc:${gc};--gl:${gl}vw;--gb:${gb}vh;animation-delay:${Math.random()*0.6}s`;
            body.appendChild(el);
            setTimeout(()=>el.remove(),(gdur+0.8)*1000);
        }
    })();
    </script>
    """, height=0)


# ─────────────────────────────────────────────────────────────
# Data
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
def fresh_candidates(log_prior):
    return init_log_scores(df.copy(), log_prior)

def recompute_candidates(path, log_prior, attr_boost):
    cands = fresh_candidates(log_prior)
    for attr, response in path:
        cands = update_log_scores(cands, attr, response, attr_boost)
    return cands

# ─────────────────────────────────────────────────────────────
# Question selection
# ─────────────────────────────────────────────────────────────
def question_splits_candidates(candidates, qid):
    tags = questions.get(qid, {}).get("tags", [qid])
    for tag in tags:
        w  = candidates[candidates["attributes"].apply(lambda a: tag in a)]
        wo = candidates[candidates["attributes"].apply(lambda a: tag not in a)]
        if len(w) > 0 and len(wo) > 0:
            return True
    return False

def get_attr_for_qid(qid):
    tags = questions.get(qid, {}).get("tags", [])
    return tags[0] if tags else qid

def infer_top_school(candidates):
    cp = log_scores_to_probs(candidates)
    sp = {}
    for _, row in cp.iterrows():
        s = row.get("school", "")
        sp[s] = sp.get(s, 0.0) + row["prob"]
    if not sp:
        return ""
    top = max(sp, key=sp.get)
    return top if sp[top] >= 0.65 else ""

def get_pending_followup(asked_qids, history_pairs):
    for qid, response in reversed(history_pairs):
        fu = questions.get(qid, {}).get("followups", {})
        for key in (response, "default"):
            for fq in fu.get(key, []):
                if fq and fq not in asked_qids and fq in questions:
                    return fq
    return None

def select_next_question(candidates, asked_qids, history_pairs, attr_boost):
    pending = get_pending_followup(asked_qids, history_pairs)
    if pending:
        return pending

    eig_scores = {}
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
# Session init / reset
# ─────────────────────────────────────────────────────────────
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
    st.session_state.just_correct    = False
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
    st.session_state.just_correct    = False
    st.session_state._needs_rerun    = False
    st.session_state.page            = "landing"
    for k in [k for k in st.session_state.keys()
              if k.startswith("q_") or k == "correction_select"]:
        del st.session_state[k]


# ═════════════════════════════════════════════════════════════
# LANDING PAGE
# ═════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem 1.5rem;">
        <div style="font-size:5rem; margin-bottom:0.5rem;">🦉</div>
        <h1 style="font-size:2.4rem; margin-bottom:0.4rem;">USIU Career Fair Akinator</h1>
        <p style="font-size:1.1rem; color:#a0b4c8; max-width:480px; margin:0 auto 2rem;">
            Think of your <strong style="color:#F5A623;">degree programme</strong> at USIU-Africa.<br>
            I'll try to guess it in <strong style="color:#F5A623;">10 questions or fewer!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([2, 1, 2])
    with col_m:
        if st.button("▶ Play", type="primary", use_container_width=True):
            _reset_game()
            st.session_state.page = "questions"
            st.rerun()


# ═════════════════════════════════════════════════════════════
# ANSWER CALLBACK
# ═════════════════════════════════════════════════════════════
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


# ═════════════════════════════════════════════════════════════
# QUESTIONS PAGE
# ═════════════════════════════════════════════════════════════
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

        # Progress bar
        prog = q_index / st.session_state.max_questions
        st.progress(prog, text=f"Question {q_index + 1} of {st.session_state.max_questions}")

        # Question text
        st.markdown(f"""
        <div style="
            background: #152333;
            border-left: 4px solid #B31B1B;
            border-radius: 0 14px 14px 0;
            padding: 1.2rem 1.5rem;
            margin: 1rem 0;
        ">
            <span style="color:#a0b4c8; font-size:0.8rem; font-weight:600; letter-spacing:1px;">
                QUESTION {q_index + 1}
            </span>
            <div style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-top:6px;">
                {q_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Current thinking expander
        with st.expander("🔍 My current thinking…", expanded=False):
            top3 = top_candidates(st.session_state.candidates, n=3)
            for _, row in top3.iterrows():
                pct  = int(row["prob"] * 100)
                meta = COURSE_META.get(row["name"], {"icon": "🎓", "color": "#B31B1B"})
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                    <span style="font-size:1.2rem;">{meta['icon']}</span>
                    <div style="flex:1;">
                        <div style="color:#fff; font-weight:600; font-size:0.9rem;">
                            {row['name']} <span style="color:#a0b4c8; font-weight:400;">({row['level']})</span>
                        </div>
                        <div style="background:#1e3044; border-radius:6px; height:6px; margin-top:4px;">
                            <div style="background:linear-gradient(90deg,#B31B1B,#F5A623);
                                        width:{pct}%; height:6px; border-radius:6px;"></div>
                        </div>
                    </div>
                    <span style="color:#F5A623; font-weight:700; font-size:0.9rem;">{pct}%</span>
                </div>
                """, unsafe_allow_html=True)

        # Answer radio
        key = f"q_{q_index}"
        if key not in st.session_state:
            st.session_state[key] = None

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


# ═════════════════════════════════════════════════════════════
# GUESS PAGE
# ═════════════════════════════════════════════════════════════
if st.session_state.page == "guess":
    if st.session_state.candidates is None or st.session_state.candidates.empty:
        st.session_state.candidates = fresh_candidates(st.session_state.log_prior)

    top3 = top_candidates(st.session_state.candidates, n=3)
    best = top3.iloc[0]
    st.session_state.final_guess = best["name"]
    conf_pct = int(best["prob"] * 100)

    # Fire celebration if just confirmed correct
    if st.session_state.get("just_correct"):
        show_celebration()
        st.markdown("""
        <div style="text-align:center; padding:1rem 0;">
            <div style="font-size:2rem;">🎉</div>
            <div style="color:#F5A623; font-size:1.2rem; font-weight:700;">
                Yes! Got it right!
            </div>
            <div style="color:#a0b4c8; font-size:0.9rem;">Thanks for playing.</div>
        </div>
        """, unsafe_allow_html=True)

    # Guess header
    st.markdown("""
    <div style="text-align:center; margin-bottom:1rem;">
        <span style="font-size:2rem;">🎯</span>
        <h2 style="display:inline; margin-left:8px;">My guess is…</h2>
    </div>
    """, unsafe_allow_html=True)

    # Course card
    st.markdown(
        _course_image_html(best["name"], best["level"], best["school"], conf_pct),
        unsafe_allow_html=True
    )

    # Runner-up
    if len(top3) > 1:
        runner = top3.iloc[1]
        r_meta = COURSE_META.get(runner["name"], {"icon": "🎓"})
        st.markdown(f"""
        <div style="
            background:#152333; border:1px solid #1e3044;
            border-radius:10px; padding:10px 16px;
            display:flex; align-items:center; gap:10px; margin-bottom:1rem;
        ">
            <span style="font-size:1.2rem;">{r_meta['icon']}</span>
            <div>
                <span style="color:#a0b4c8; font-size:0.8rem;">Runner-up</span><br>
                <span style="color:#d0dde8; font-weight:600;">{runner['name']}</span>
                <span style="color:#a0b4c8;"> ({runner['level']})</span>
                <span style="color:#F5A623; font-weight:700; margin-left:8px;">{int(runner['prob']*100)}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Correct / Wrong buttons
    if not st.session_state.get("just_correct") and not st.session_state.show_correction:
        col1, col2 = st.columns(2)
        if col1.button("✅ Yes, correct!", type="primary", use_container_width=True):
            counts = st.session_state.learning_counts
            counts = record_success(counts, st.session_state.final_guess, st.session_state.asked)
            save_learning_counts(counts)
            st.session_state.learning_counts = counts
            st.session_state.attr_boost = compute_attr_boosts(counts)
            save_game_result({
                "type": "SUCCESS", "guess": st.session_state.final_guess,
                "correct": st.session_state.final_guess, "confidence": conf_pct,
                "n_questions": len(st.session_state.asked_qids),
                "path": [list(p) for p in st.session_state.asked],
            })
            st.session_state.just_correct = True
            st.rerun()

        if col2.button("❌ No, wrong guess", use_container_width=True):
            st.session_state.show_correction = True
            st.rerun()

    # Correction flow
    if st.session_state.show_correction:
        st.markdown('<div style="color:#F5A623; font-weight:600; margin-bottom:6px;">What is your actual programme?</div>', unsafe_allow_html=True)
        correct_program = st.selectbox(
            "Select your programme:",
            sorted(df["name"].unique()),
            key="correction_select",
            label_visibility="collapsed",
        )
        if st.button("Confirm & submit", type="primary"):
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
                "type": "FAIL", "guess": st.session_state.final_guess,
                "correct": correct_program, "confidence": conf_pct,
                "n_questions": len(st.session_state.asked_qids),
                "path": [list(p) for p in st.session_state.asked],
            })
            st.session_state.show_correction = False
            st.markdown(f"""
            <div style="background:#1a2e42; border:1px solid #2a4060; border-radius:10px; padding:12px 16px; margin:8px 0;">
                <span style="color:#a0b4c8;">Got it — noted as </span>
                <strong style="color:#F5A623;">{correct_program}</strong>
                <span style="color:#a0b4c8;">. I'll learn from this! 🤔</span>
            </div>
            """, unsafe_allow_html=True)

    # Play again
    st.divider()
    col_l2, col_m2, col_r2 = st.columns([2, 1, 2])
    with col_m2:
        if st.button("🔄 Play Again", use_container_width=True):
            _reset_game()
            st.session_state.page = "landing"
            st.rerun()


# ═════════════════════════════════════════════════════════════
# SIDEBAR  — diagnostics
# ═════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 16px;">
        <span style="font-size:1.2rem; font-weight:700; color:#fff;">🛠 Diagnostics</span>
    </div>
    """, unsafe_allow_html=True)

    storage_status = "☁️ Supabase" if is_supabase_configured() else "💾 Local file"
    st.caption(f"Storage: **{storage_status}**")

    if st.checkbox("Show live stats"):
        stats = fetch_game_stats()
        if stats:
            col_a, col_b = st.columns(2)
            col_a.metric("Total games", stats.get("total_games", 0))
            col_b.metric("Accuracy",    f"{stats.get('accuracy', 0)}%")
            col_a.metric("Avg Q's",     stats.get("avg_questions", "—"))
            col_b.metric("Avg conf.",   f"{stats.get('avg_confidence', 0)}%")
        else:
            st.info("No game stats yet.")

        confusions = fetch_confusion_pairs(limit=8)
        if confusions:
            st.markdown("**Top mistakes:**")
            for row in confusions:
                st.write(f"**{row['guessed']}** → **{row['correct']}** ({row['count']}×)")

        st.markdown("**Top attribute signals:**")
        boosts = sorted(st.session_state.attr_boost.items(), key=lambda x: -abs(x[1]))[:8]
        for attr, boost in boosts:
            sign = "▲" if boost > 0 else "▼"
            st.write(f"{sign} `{attr}`: {boost:+.2f}")
