"""
usiu_akinator.py — USIU Career Fair Akinator
Mascot: Kofi the Griot-Scholar (kofi.py)
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
)
from db import (
    load_learning_counts, save_learning_counts, save_game_result,
    fetch_game_stats, fetch_confusion_pairs, is_supabase_configured,
)
from kofi import kofi_html
from cv_game import cv_game_html

# ─────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.56
MIN_QUESTIONS        = 5
MAX_QUESTIONS        = 10
MAX_QUESTIONS_EXT    = 13

st.set_page_config(
    page_title="USIU Akinator 🥁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# Global CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(145deg,#0D1B2A 0%,#1a2a3a 100%); min-height:100vh; }
section[data-testid="stSidebar"] { background:#111e2b !important; border-right:1px solid #1e3044; }
h1 { color:#FFFFFF !important; font-weight:800 !important; }
h2, h3 { color:#F5A623 !important; font-weight:700 !important; }
p, li, label { color:#d0dde8 !important; }
div[data-testid="stProgress"] > div > div {
    background:linear-gradient(90deg,#B31B1B,#F5A623) !important; border-radius:10px; }
div[data-testid="stProgress"] > div { background:#1e3044 !important; border-radius:10px; }
div[data-testid="stRadio"] label {
    background:#1a2e42 !important; border:1px solid #2a4060 !important;
    border-radius:10px !important; padding:10px 18px !important;
    margin:4px 0 !important; cursor:pointer !important;
    transition:all 0.2s !important; color:#d0dde8 !important; }
div[data-testid="stRadio"] label:hover {
    border-color:#F5A623 !important; background:#1e3650 !important; color:#F5A623 !important; }
div[data-testid="stButton"] button[kind="primary"] {
    background:linear-gradient(135deg,#B31B1B,#cc2222) !important;
    color:white !important; border:none !important; border-radius:12px !important;
    font-weight:700 !important; font-size:1.05rem !important;
    padding:0.6rem 1.8rem !important;
    box-shadow:0 4px 15px rgba(179,27,27,.4) !important; transition:all .2s !important; }
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform:translateY(-2px) !important; box-shadow:0 6px 20px rgba(179,27,27,.55) !important; }
div[data-testid="stButton"] button[kind="secondary"] {
    background:#1a2e42 !important; color:#d0dde8 !important;
    border:1px solid #2a4060 !important; border-radius:12px !important;
    font-weight:600 !important; transition:all .2s !important; }
div[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color:#F5A623 !important; color:#F5A623 !important; }
details { background:#152333 !important; border:1px solid #1e3044 !important; border-radius:12px !important; }
details summary { color:#a0b4c8 !important; font-size:.9rem !important; }
hr { border-color:#1e3044 !important; }
div[data-testid="stMetric"] {
    background:#152333; border-radius:10px; padding:10px; border:1px solid #1e3044; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Course card
# ─────────────────────────────────────────────────────────────
COURSE_META: Dict[str, Dict] = {
    "International Business Administration": {"icon":"🌍","color":"#B31B1B"},
    "Accounting":                            {"icon":"📊","color":"#B31B1B"},
    "Finance":                               {"icon":"💹","color":"#B31B1B"},
    "Hotel & Restaurant Management":         {"icon":"🏨","color":"#B31B1B"},
    "Business Administration (MBA)":         {"icon":"💼","color":"#B31B1B"},
    "Global Leadership & Management":        {"icon":"🧭","color":"#B31B1B"},
    "Global Banking and Finance":            {"icon":"🏦","color":"#B31B1B"},
    "Global Business Management":           {"icon":"🌐","color":"#B31B1B"},
    "Health Leadership and Management":      {"icon":"🏥","color":"#B31B1B"},
    "Management and Organizational Development": {"icon":"🔄","color":"#B31B1B"},
    "Doctor of Business Administration":     {"icon":"🎓","color":"#B31B1B"},
    "International Relations":               {"icon":"🕊️","color":"#1a6b3c"},
    "Psychology":                            {"icon":"🧠","color":"#1a6b3c"},
    "Criminal Justice Studies":              {"icon":"⚖️","color":"#1a6b3c"},
    "Sociology":                             {"icon":"👥","color":"#1a6b3c"},
    "Criminal and Transitional Justice":     {"icon":"🔏","color":"#1a6b3c"},
    "Clinical Psychology":                   {"icon":"🛋️","color":"#1a6b3c"},
    "Counseling Psychology":                 {"icon":"💬","color":"#1a6b3c"},
    "International Relations (MA)":          {"icon":"🗺️","color":"#1a6b3c"},
    "Marriage and Family Therapy":           {"icon":"❤️","color":"#1a6b3c"},
    "PhD International Relations":           {"icon":"📜","color":"#1a6b3c"},
    "Doctor of Psychology (Clinical)":       {"icon":"🔬","color":"#1a6b3c"},
    "Applied Computer Technology":           {"icon":"🖥️","color":"#1a4a8a"},
    "Information Systems & Technology":      {"icon":"🗄️","color":"#1a4a8a"},
    "Data Science & Analytics":              {"icon":"📈","color":"#1a4a8a"},
    "Artificial Intelligence & Robotics":    {"icon":"🤖","color":"#1a4a8a"},
    "Software Engineering":                  {"icon":"⚙️","color":"#1a4a8a"},
    "Information Security":                  {"icon":"🔐","color":"#1a4a8a"},
    "Information Systems and Technology":    {"icon":"🌐","color":"#1a4a8a"},
    "Bachelor of Pharmacy":                  {"icon":"💊","color":"#6b1a6b"},
    "Nursing":                               {"icon":"🩺","color":"#6b1a6b"},
    "Epidemiology & Biostatistics":          {"icon":"📋","color":"#6b1a6b"},
    "Analytical Chemistry":                  {"icon":"🧪","color":"#6b1a6b"},
    "Applied Biochemistry":                  {"icon":"🧬","color":"#6b1a6b"},
    "Clinical Pharmacology and Therapeutics":{"icon":"🔭","color":"#6b1a6b"},
    "Journalism":                            {"icon":"📰","color":"#7a5c00"},
    "Animation":                             {"icon":"🎨","color":"#7a5c00"},
    "Film Production & Directing":           {"icon":"🎬","color":"#7a5c00"},
    "Communication Studies":                 {"icon":"📡","color":"#7a5c00"},
}

def _course_card_html(name: str, level: str, school: str, conf_pct: int) -> str:
    import os
    meta  = COURSE_META.get(name, {"icon":"🎓","color":"#B31B1B"})
    icon  = meta["icon"]
    color = meta["color"]
    slug  = name.lower().replace(" ","_").replace("&","and").replace("(","").replace(")","")
    img_file = f"img_{slug}.png"
    if os.path.exists(img_file):
        banner = f'<img src="{img_file}" style="width:100%;height:160px;object-fit:cover;border-radius:12px 12px 0 0;">'
    else:
        banner = (
            f'<div style="width:100%;height:160px;'
            f'background:linear-gradient(135deg,{color}cc,{color}44);'
            f'border-radius:12px 12px 0 0;display:flex;align-items:center;'
            f'justify-content:center;font-size:4.5rem;">{icon}</div>'
        )
    return (
        f'<!DOCTYPE html><html><head>'
        f'<style>body{{margin:0;padding:0;background:transparent;'
        f'font-family:"Segoe UI",Arial,sans-serif;}}</style></head><body>'
        f'<div style="border-radius:12px;border:2px solid {color}88;overflow:hidden;'
        f'box-shadow:0 6px 24px {color}44;">'
        f'{banner}'
        f'<div style="padding:14px 18px;background:#152333;">'
        f'<div style="font-size:1.25rem;font-weight:800;color:#fff;margin-bottom:3px;">{name}</div>'
        f'<div style="font-size:0.82rem;color:#a0b4c8;margin-bottom:10px;">{level} · {school}</div>'
        f'<span style="background:linear-gradient(90deg,#B31B1B,#F5A623);color:#fff;'
        f'font-weight:700;font-size:0.88rem;padding:4px 14px;border-radius:20px;">'
        f'Confidence: {conf_pct}%</span>'
        f'</div></div></body></html>'
    )

# ─────────────────────────────────────────────────────────────
# Celebration  (butterflies + glitter via st.markdown)
# ─────────────────────────────────────────────────────────────
def show_celebration():
    st.balloons()
    st.markdown("""
<style>
@keyframes bflyUp{0%{opacity:1;transform:translate(0,0)rotate(0)scale(1)}
  50%{opacity:.9;transform:translate(var(--dx),-45vh)rotate(var(--rot))scale(1.2)}
  100%{opacity:0;transform:translate(calc(var(--dx)*1.6),-105vh)rotate(calc(var(--rot)*2))scale(.5)}}
@keyframes bWing{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.3)}}
@keyframes sparkle{0%{opacity:1;transform:translate(0,0)rotate(0)}
  100%{opacity:0;transform:translate(var(--sx),var(--sy))rotate(720deg)}}
.bfly{position:fixed;bottom:-6vh;left:var(--bl);font-size:var(--bs);
  pointer-events:none;z-index:99999;
  animation:bflyUp var(--bd) ease-in forwards var(--bdelay);}
.bfly-inner{display:inline-block;animation:bWing .35s ease-in-out infinite;}
.spark{position:fixed;width:9px;height:9px;border-radius:50%;background:var(--sc);
  pointer-events:none;z-index:99998;left:var(--sl);bottom:var(--sb);
  animation:sparkle var(--sd) ease-out forwards var(--sdelay);}
</style>
<script>
(function(){
  const E=['🦋','🦋','🦋','🌸','🌺','✨','🌟','💛','🥁'];
  const C=['#F5A623','#B31B1B','#fff','#FFE066','#ff88cc','#88ddff','#aaffcc','#ffaa44','#2D6A4F'];
  for(let i=0;i<24;i++){
    const e=document.createElement('div'); e.className='bfly';
    const bl=Math.random()*94,dx=(Math.random()-.5)*55,rot=(Math.random()-.5)*700;
    const bd=2.3+Math.random()*2.4,bs=(1.3+Math.random()*1.9)+'rem',bdelay=Math.random()*1.3+'s';
    e.style.cssText=`--bl:${bl}vw;--dx:${dx}vw;--rot:${rot}deg;--bd:${bd}s;--bs:${bs};--bdelay:${bdelay}`;
    e.innerHTML=`<div class="bfly-inner">${E[Math.floor(Math.random()*E.length)]}</div>`;
    document.body.appendChild(e);
    setTimeout(()=>e.remove(),(bd+parseFloat(bdelay)+1.5)*1000);
  }
  for(let i=0;i<70;i++){
    const s=document.createElement('div'); s.className='spark';
    const sx=(Math.random()-.5)*130+'vw',sy='-'+(35+Math.random()*75)+'vh';
    const sd=.8+Math.random()*1.5,sc=C[Math.floor(Math.random()*C.length)];
    const sl=Math.random()*97+'vw',sb=Math.random()*35+'vh',sdelay=Math.random()*.7+'s';
    s.style.cssText=`--sx:${sx};--sy:${sy};--sd:${sd}s;--sc:${sc};--sl:${sl};--sb:${sb};--sdelay:${sdelay}`;
    document.body.appendChild(s);
    setTimeout(()=>s.remove(),(sd+parseFloat(sdelay)+.8)*1000);
  }
})();
</script>
""", unsafe_allow_html=True)

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
        if (candidates["attributes"].apply(lambda a: tag in a).any() and
                candidates["attributes"].apply(lambda a: tag not in a).any()):
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
            best_pool = max(pool_eig, key=pool_eig.get)
            best_global = max(eig_scores, key=eig_scores.get)
            if eig_scores[best_pool] >= 0.8 * eig_scores[best_global]:
                return best_pool
    return max(eig_scores, key=eig_scores.get)

# ─────────────────────────────────────────────────────────────
# Session init / reset
# ─────────────────────────────────────────────────────────────
def _init_session():
    counts    = load_learning_counts()
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
    counts    = load_learning_counts()
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
# LANDING PAGE — game selector
# ═════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    _, k_col, _ = st.columns([1, 2, 1])
    with k_col:
        st.components.v1.html(kofi_html("idle"), height=430, scrolling=False)

    st.markdown("""
    <div style="text-align:center; padding:.3rem 1rem 1.2rem;">
        <h1 style="font-size:2rem; margin-bottom:.3rem;">USIU Career Fair</h1>
        <p style="font-size:1rem; color:#a0b4c8; margin:0;">
            Choose a game and hand the screen to a student
        </p>
    </div>
    """, unsafe_allow_html=True)

    g_left, g_right = st.columns(2, gap="medium")

    with g_left:
        st.markdown("""
        <div style="background:#152333;border:2px solid #B31B1B55;border-radius:16px;
                    padding:1.4rem;text-align:center;min-height:150px;">
            <div style="font-size:2.2rem;margin-bottom:8px;">🎯</div>
            <div style="font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:6px;">
                Guess My Degree
            </div>
            <div style="font-size:0.82rem;color:#a0b4c8;line-height:1.45;">
                Think of your programme at USIU-Africa. Kofi will guess it in 10 questions or fewer!
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶ Play Akinator", type="primary", use_container_width=True, key="btn_ak"):
            _reset_game()
            st.session_state.page = "questions"
            st.rerun()

    with g_right:
        st.markdown("""
        <div style="background:#152333;border:2px solid #F5A62355;border-radius:16px;
                    padding:1.4rem;text-align:center;min-height:150px;">
            <div style="font-size:2.2rem;margin-bottom:8px;">📄</div>
            <div style="font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:6px;">
                Spot CV Mistakes
            </div>
            <div style="font-size:0.82rem;color:#a0b4c8;line-height:1.45;">
                Find 5 errors in a CV before 30 seconds run out. Find 4+ and win Ksh 50–100!
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶ Play CV Game", use_container_width=True, key="btn_cv"):
            st.session_state.page = "cv_game"
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

        # Pick Kofi state based on current confidence
        conf_now   = confidence_of_top(st.session_state.candidates)
        kofi_state = "confident" if (q_index >= MIN_QUESTIONS and conf_now >= 0.45) else "thinking"

        # ── Two-column layout: Kofi left, question right ──────
        col_k, col_q = st.columns([2, 3], gap="medium")

        with col_k:
            # Kofi fills the full left column height
            st.components.v1.html(kofi_html(kofi_state), height=430, scrolling=False)

        with col_q:
            # Progress bar
            st.progress(
                q_index / st.session_state.max_questions,
                text=f"Question {q_index + 1} of {st.session_state.max_questions}"
            )

            # Question card
            st.markdown(f"""
            <div style="background:#152333;border-left:4px solid #B31B1B;
                        border-radius:0 14px 14px 0;padding:1.1rem 1.4rem;margin:.6rem 0;">
                <span style="color:#a0b4c8;font-size:.75rem;font-weight:600;letter-spacing:1px;">
                    QUESTION {q_index + 1}
                </span>
                <div style="color:#fff;font-size:1.1rem;font-weight:700;margin-top:5px;
                            line-height:1.45;">
                    {q_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Current thinking expander
            with st.expander("🥁 Kofi's current thinking…", expanded=False):
                top3 = top_candidates(st.session_state.candidates, n=3)
                for _, row in top3.iterrows():
                    pct  = int(row["prob"] * 100)
                    meta = COURSE_META.get(row["name"], {"icon":"🎓","color":"#B31B1B"})
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                        <span style="font-size:1.1rem;">{meta['icon']}</span>
                        <div style="flex:1;">
                            <div style="color:#fff;font-weight:600;font-size:.85rem;">
                                {row['name']}
                                <span style="color:#a0b4c8;font-weight:400;"> ({row['level']})</span>
                            </div>
                            <div style="background:#1e3044;border-radius:6px;height:5px;margin-top:4px;">
                                <div style="background:linear-gradient(90deg,#B31B1B,#F5A623);
                                            width:{pct}%;height:5px;border-radius:6px;"></div>
                            </div>
                        </div>
                        <span style="color:#F5A623;font-weight:700;font-size:.85rem;">{pct}%</span>
                    </div>
                    """, unsafe_allow_html=True)

            # Answer radio
            key = f"q_{q_index}"
            if key not in st.session_state:
                st.session_state[key] = None

            st.radio(
                "Your answer:",
                qmeta.get("responses", ["Definitely Yes","Probably Yes","Neutral","Probably No","Definitely No"]),
                index=None, key=key,
                on_change=handle_answer, args=(qid, q_index),
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

    # ── Two-column: Kofi left, result right ──────────────────
    col_k2, col_r = st.columns([2, 3], gap="medium")

    with col_k2:
        if st.session_state.get("just_correct"):
            st.components.v1.html(kofi_html("correct"),    height=430, scrolling=False)
        elif st.session_state.show_correction:
            st.components.v1.html(kofi_html("wrong"),      height=430, scrolling=False)
        else:
            st.components.v1.html(kofi_html("confident"),  height=430, scrolling=False)

    with col_r:
        if st.session_state.get("just_correct"):
            show_celebration()
            st.markdown("""
            <div style="padding:.5rem 0 1rem;">
                <div style="font-size:1.5rem;font-weight:700;color:#F5A623;">
                    🥁 BOOM — got it right!
                </div>
                <div style="color:#a0b4c8;font-size:.9rem;">Thanks for playing.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="margin-bottom:.6rem;">
                <span style="font-size:1.6rem;">🎯</span>
                <h2 style="display:inline;margin-left:8px;">My guess is…</h2>
            </div>
            """, unsafe_allow_html=True)

        # Course card
        st.components.v1.html(
            _course_card_html(best["name"], best["level"], best["school"], conf_pct),
            height=260, scrolling=False
        )

        # Runner-up
        if len(top3) > 1:
            runner = top3.iloc[1]
            r_meta = COURSE_META.get(runner["name"], {"icon":"🎓"})
            st.markdown(f"""
            <div style="background:#152333;border:1px solid #1e3044;border-radius:10px;
                        padding:9px 14px;display:flex;align-items:center;
                        gap:10px;margin-bottom:.8rem;">
                <span style="font-size:1.1rem;">{r_meta['icon']}</span>
                <div>
                    <span style="color:#a0b4c8;font-size:.75rem;">Runner-up</span><br>
                    <span style="color:#d0dde8;font-weight:600;">{runner['name']}</span>
                    <span style="color:#a0b4c8;"> ({runner['level']})</span>
                    <span style="color:#F5A623;font-weight:700;margin-left:8px;">{int(runner['prob']*100)}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Correct / Wrong buttons
        if not st.session_state.get("just_correct") and not st.session_state.show_correction:
            c1, c2 = st.columns(2)
            if c1.button("✅ Yes, correct!", type="primary", use_container_width=True):
                counts = st.session_state.learning_counts
                counts = record_success(counts, st.session_state.final_guess, st.session_state.asked)
                save_learning_counts(counts)
                st.session_state.learning_counts = counts
                st.session_state.attr_boost = compute_attr_boosts(counts)
                save_game_result({
                    "type":"SUCCESS","guess":st.session_state.final_guess,
                    "correct":st.session_state.final_guess,"confidence":conf_pct,
                    "n_questions":len(st.session_state.asked_qids),
                    "path":[list(p) for p in st.session_state.asked],
                })
                st.session_state.just_correct = True
                st.rerun()
            if c2.button("❌ No, wrong guess", use_container_width=True):
                st.session_state.show_correction = True
                st.rerun()

        if st.session_state.show_correction:
            st.markdown(
                '<div style="color:#F5A623;font-weight:600;margin-bottom:6px;">'
                'What is your actual programme?</div>',
                unsafe_allow_html=True)
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
                    "type":"FAIL","guess":st.session_state.final_guess,
                    "correct":correct_program,"confidence":conf_pct,
                    "n_questions":len(st.session_state.asked_qids),
                    "path":[list(p) for p in st.session_state.asked],
                })
                st.session_state.show_correction = False
                st.markdown(f"""
                <div style="background:#1a2e42;border:1px solid #2a4060;border-radius:10px;
                            padding:12px 16px;margin:8px 0;">
                    <span style="color:#a0b4c8;">Kofi says: "I hear you — noted as </span>
                    <strong style="color:#F5A623;">{correct_program}</strong>
                    <span style="color:#a0b4c8;">. The drum will remember." 🥁</span>
                </div>
                """, unsafe_allow_html=True)

    st.divider()
    col_l2, col_m2, col_r2 = st.columns([2, 1, 2])
    with col_m2:
        if st.button("🔄 Play Again", use_container_width=True):
            _reset_game()
            st.session_state.page = "landing"
            st.rerun()


# ═════════════════════════════════════════════════════════════
# CV GAME PAGE
# ═════════════════════════════════════════════════════════════
if st.session_state.page == "cv_game":
    # Pull Supabase credentials for the JS client in the iframe
    sb_url = sb_key = ""
    if is_supabase_configured():
        try:
            sb_url = st.secrets["supabase"]["url"]
            sb_key = st.secrets["supabase"]["key"]
        except Exception:
            pass

    st.components.v1.html(
        cv_game_html(sb_url, sb_key),
        height=860,
        scrolling=True,
    )

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    if st.button("← Back to menu", key="cv_back"):
        st.session_state.page = "landing"
        st.rerun()


# ═════════════════════════════════════════════════════════════
# SIDEBAR  — diagnostics
# ═════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="padding:8px 0 16px;font-size:1.1rem;font-weight:700;color:#fff;">🥁 Diagnostics</div>',
                unsafe_allow_html=True)
    st.caption(f"Storage: **{'☁️ Supabase' if is_supabase_configured() else '💾 Local'}**")

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
            st.write(f"{'▲' if boost>0 else '▼'} `{attr}`: {boost:+.2f}")
