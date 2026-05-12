"""
simulator.py  (improved)
-----------------------
Validation simulator using the new Bayesian engine from bayes_engine.py.

Run:   python simulator.py
"""

import os
import json
import random
from typing import Dict, List, Tuple
from collections import Counter

import pandas as pd

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
    LOG_LR_WITH,
    PROGRAM_FREQ_PREFIX,
)

LEARNING_FILE        = "learning_bayes.json"
CONFIDENCE_THRESHOLD = 0.56
MIN_QUESTIONS        = 5
MAX_QUESTIONS        = 10
MAX_QUESTIONS_EXT    = 13
LIKERT               = list(LOG_LR_WITH.keys())

df            = pd.DataFrame(programs)
PROGRAM_NAMES = list(df["name"].unique())
NAME_TO_ATTRS = {row["name"]: set(row["attributes"]) for _, row in df.iterrows()}


def load_learning_counts():
    if os.path.exists(LEARNING_FILE):
        try:
            with open(LEARNING_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {k: {"success": int(v.get("success", 0)),
                            "trials":  int(v.get("trials", 0))}
                        for k, v in data.items()}
        except Exception:
            return {}
    return {}


def _splits(candidates, qid):
    tags = questions.get(qid, {}).get("tags", [qid])
    for tag in tags:
        w  = candidates[candidates["attributes"].apply(lambda a: tag in a)]
        wo = candidates[candidates["attributes"].apply(lambda a: tag not in a)]
        if len(w) > 0 and len(wo) > 0:
            return True
    return False


def _attr(qid):
    tags = questions.get(qid, {}).get("tags", [])
    return tags[0] if tags else qid


def _top_school(candidates):
    cp = log_scores_to_probs(candidates)
    sp: Dict[str, float] = {}
    for _, row in cp.iterrows():
        s = row.get("school", "")
        sp[s] = sp.get(s, 0.0) + row["prob"]
    if not sp:
        return ""
    ts = max(sp, key=sp.get)
    return ts if sp[ts] >= 0.65 else ""


def _followup(asked_qids, history_pairs):
    for qid, response in reversed(history_pairs):
        fu = questions.get(qid, {}).get("followups", {})
        for key in (response, "default"):
            for fq in fu.get(key, []):
                if fq and fq not in asked_qids and fq in questions:
                    return fq
    return None


def select_next_question(candidates, asked_qids, history_pairs, attr_boost):
    pending = _followup(asked_qids, history_pairs)
    if pending:
        return pending

    eig: Dict[str, float] = {}
    for qid in questions:
        if qid in asked_qids or not _splits(candidates, qid):
            continue
        eig[qid] = estimate_eig_bayes(candidates, _attr(qid), attr_boost)

    if not eig:
        for qid in questions:
            if qid not in asked_qids:
                return qid
        return None

    ts = _top_school(candidates)
    if ts:
        pool_eig = {q: eig[q] for q in school_questions.get(ts, []) if q in eig}
        if pool_eig:
            bpq = max(pool_eig, key=pool_eig.get)
            bgq = max(eig, key=eig.get)
            if eig.get(bpq, 0) >= 0.8 * eig.get(bgq, 1):
                return bpq

    return max(eig, key=eig.get)


def sim_response(has_attr, noise=0.10, yes_skew=0.40, neutral=0.20):
    if random.random() < noise:
        return random.choice(LIKERT)
    if has_attr:
        base = [yes_skew, 0.25, neutral, 0.10, 0.05]
    else:
        base = [0.05, 0.10, neutral, 0.30, max(0.01, 0.45 - neutral * 0.3)]
    s = sum(base)
    probs = [b / s for b in base]
    r = random.random(); cum = 0.0
    for k, p in zip(LIKERT, probs):
        cum += p
        if r <= cum:
            return k
    return LIKERT[-1]


def simulate_game(prog, log_prior, attr_boost, noise=0.10, yes_skew=0.40):
    prog_attrs    = set(prog["attributes"])
    asked_qids    = []
    asked         = []
    history_pairs = []
    candidates    = init_log_scores(df.copy(), log_prior)
    mq            = MAX_QUESTIONS
    extended      = False

    for _ in range(mq + 5):
        qid = select_next_question(candidates, asked_qids, history_pairs, attr_boost)
        if qid is None:
            break
        tags     = questions.get(qid, {}).get("tags", [qid])
        has_attr = any(t in prog_attrs for t in tags)
        response = sim_response(has_attr, noise, yes_skew)
        attr     = tags[0] if tags else qid
        candidates = update_log_scores(candidates, attr, response, attr_boost)
        asked_qids.append(qid)
        asked.append((attr, response))
        history_pairs.append((qid, response))
        n = len(asked_qids)
        conf = confidence_of_top(candidates)
        if n >= MIN_QUESTIONS and conf >= CONFIDENCE_THRESHOLD:
            break
        if n >= mq:
            if conf < 0.45 and not extended:
                mq = MAX_QUESTIONS_EXT
                extended = True
            else:
                break

    topdf = top_candidates(candidates, 3)
    return list(topdf["name"]), len(asked_qids), confidence_of_top(candidates)


def validate(attr_boost, log_prior, sims=50):
    rows = []
    confusion = Counter()
    for _, prog in df.iterrows():
        name  = prog["name"]
        t1, t3 = 0, 0
        qtot, ctot = 0, 0.0
        for _ in range(sims):
            guesses, nq, conf = simulate_game(prog, log_prior, attr_boost)
            if guesses and guesses[0] == name:
                t1 += 1
            if name in guesses:
                t3 += 1
            if guesses and guesses[0] != name:
                confusion[(guesses[0], name)] += 1
            qtot  += nq
            ctot  += conf
        rows.append({
            "programme":      name,
            "school":         prog["school"],
            "top1_acc":       round(t1 / sims, 3),
            "top3_acc":       round(t3 / sims, 3),
            "avg_questions":  round(qtot / sims, 1),
            "avg_confidence": round(ctot / sims, 3),
        })
    return pd.DataFrame(rows).sort_values("top1_acc", ascending=False).reset_index(drop=True), confusion


def run_pretraining(base_sims=200, noise=0.10, yes_skew=0.40, persist=True):
    counts     = load_learning_counts() or {}
    log_prior  = build_program_priors(counts, PROGRAM_NAMES)
    attr_boost = compute_attr_boosts(counts)

    school_counts = df["school"].value_counts().to_dict()
    mx  = max(school_counts.values())
    spm = {s: mx / c for s, c in school_counts.items()}
    avg = sum(spm.values()) / len(spm)
    spm = {s: v / avg for s, v in spm.items()}

    for _, prog in df.iterrows():
        n_sims = max(1, int(base_sims * spm.get(prog["school"], 1.0)))
        for _ in range(n_sims):
            guesses, _, _ = simulate_game(prog, log_prior, attr_boost, noise, yes_skew)
            guess = guesses[0] if guesses else ""
            if guess == prog["name"]:
                counts = record_success(counts, prog["name"], [(prog["name"], "pretrain")])
            else:
                counts = record_failure(counts, guess, prog["name"],
                                        [(prog["name"], "pretrain")], NAME_TO_ATTRS)

    if persist:
        with open(LEARNING_FILE, "w", encoding="utf-8") as f:
            json.dump(counts, f, ensure_ascii=False, indent=2)

    return counts, compute_attr_boosts(counts), build_program_priors(counts, PROGRAM_NAMES)


if __name__ == "__main__":
    print("Loading learning data…")
    counts     = load_learning_counts()
    attr_boost = compute_attr_boosts(counts)
    log_prior  = build_program_priors(counts, PROGRAM_NAMES)

    print(f"Validating ({len(df)} programmes, 50 sims each)…\n")
    results, confusion = validate(attr_boost, log_prior, sims=50)
    print(results.to_string(index=False))

    o1 = results["top1_acc"].mean()
    o3 = results["top3_acc"].mean()
    aq = results["avg_questions"].mean()
    print(f"\n{'='*65}")
    print(f"  Overall top-1: {o1:.1%}   top-3: {o3:.1%}   avg questions: {aq:.1f}")
    print(f"{'='*65}")
    print("\nTop confusion pairs:")
    for (guessed, correct), n in confusion.most_common(10):
        print(f"  Guessed '{guessed}' → Correct '{correct}'  ({n}×)")
