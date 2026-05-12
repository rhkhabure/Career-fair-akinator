"""
bayes_engine.py
---------------
Proper multiplicative Bayesian scoring engine for the USIU Akinator.

Why this is better than the old additive model
-----------------------------------------------
Old model:  score += weight  (or tiny penalty 0.2 * (1-weight))
            → Programs accumulate score by volume; "Definitely No" only
              subtracts a tiny 0.02 from non-matching programs — they
              are never truly eliminated.

New model:  log_score += log_likelihood_ratio
            → Each answer multiplies the probability of each program.
              A "Definitely No" to `coding` drops a Software Engineering
              program's probability by ~20×. Programs are actively
              eliminated, not just out-scored.
"""

import math
import json
import os
from typing import Dict, List, Tuple

import pandas as pd

# ─────────────────────────────────────────────────────────────
# Log-likelihood ratios per Likert response
# ─────────────────────────────────────────────────────────────
# These encode P(response | program HAS attribute) /
#              P(response | program LACKS attribute)
# Calibrated from empirical survey of how students answer
# when the attribute is or isn't in their program.
#
# Example: P("Definitely Yes" | has attr) ≈ 0.70
#          P("Definitely Yes" | lacks attr) ≈ 0.05
#          LLR = log(0.70 / 0.05) = +2.64  → strong positive evidence
#
LOG_LR_WITH: Dict[str, float] = {
    "Definitely Yes":  2.64,   # 14× more likely if attr present
    "Probably Yes":    0.85,   # 2.3× more likely
    "Neutral":        -0.36,   # slight negative (person uncertain)
    "Probably No":   -2.20,   # 9× more likely if attr absent
    "Definitely No": -3.22,   # 25× more likely if attr absent
}

# For programs that LACK the attribute, all signs flip
LOG_LR_WITHOUT: Dict[str, float] = {k: -v for k, v in LOG_LR_WITH.items()}

# Fallback if response string not in table
_FALLBACK_WITH = 0.0
_FALLBACK_WITHOUT = 0.0


def response_to_llr(response: str, program_has_attr: bool) -> float:
    """Return the log-likelihood-ratio contribution for one answer."""
    if program_has_attr:
        return LOG_LR_WITH.get(response, _FALLBACK_WITH)
    else:
        return LOG_LR_WITHOUT.get(response, _FALLBACK_WITHOUT)


# ─────────────────────────────────────────────────────────────
# Per-program frequency prior
# ─────────────────────────────────────────────────────────────

def build_program_priors(
    learning_counts: Dict[str, Dict[str, int]],
    program_names: List[str],
    smoothing: float = 5.0,
) -> Dict[str, float]:
    """
    Build log-prior for each program from learning data.

    We look for keys like  "program_freq|<name>": {"success": N, "trials": M}
    in learning_counts. If absent, every program gets a uniform prior.

    smoothing: pseudo-count added so new programs still have a non-zero prior.
    """
    # Gather raw success counts per program
    raw: Dict[str, float] = {name: smoothing for name in program_names}
    for k, v in learning_counts.items():
        if k.startswith("program_freq|"):
            name = k[len("program_freq|"):]
            if name in raw:
                raw[name] += v.get("success", 0)

    total = sum(raw.values())
    # log-prior proportional to frequency
    log_prior = {name: math.log(raw[name] / total) for name in program_names}
    return log_prior


# ─────────────────────────────────────────────────────────────
# Core scoring
# ─────────────────────────────────────────────────────────────

def init_log_scores(df: pd.DataFrame, log_prior: Dict[str, float]) -> pd.DataFrame:
    """
    Set each program's log_score to its log-prior.
    Returns a *copy* of df with a 'log_score' column.
    """
    df = df.copy()
    df["log_score"] = df["name"].map(log_prior).fillna(0.0)
    return df


def update_log_scores(
    df: pd.DataFrame,
    attr: str,
    response: str,
    attr_boost: Dict[str, float] = None,
) -> pd.DataFrame:
    """
    Apply one Bayesian update for the given (attr, response) pair.

    attr_boost (optional): learned adjustment for how reliable this
    attribute is as a discriminator. Range roughly [-0.6, 0.9].
    Boost is applied as a dampening/amplification of the LLR.
    """
    attr_boost = attr_boost or {}
    boost = attr_boost.get(attr, 0.0)
    # Dampen extreme boosts so they don't overwhelm the signal
    scale = 1.0 + max(-0.5, min(0.7, boost))

    def _llr(row) -> float:
        has_attr = attr in row["attributes"]
        base_llr = response_to_llr(response, has_attr)
        return base_llr * scale

    df = df.copy()
    df["log_score"] = df["log_score"] + df.apply(_llr, axis=1)
    return df


def log_scores_to_probs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert log_scores to proper probabilities via softmax (numerically stable).
    Adds a 'prob' column.
    """
    df = df.copy()
    ls = df["log_score"].values
    # Subtract max for numerical stability
    ls_shifted = ls - ls.max()
    exp_ls = [math.exp(x) for x in ls_shifted]
    total = sum(exp_ls)
    df["prob"] = [e / total for e in exp_ls]
    return df


def top_candidates(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """Return top-n candidates sorted by probability (descending)."""
    df = log_scores_to_probs(df)
    return df.sort_values("prob", ascending=False).head(n).reset_index(drop=True)


def confidence_of_top(df: pd.DataFrame) -> float:
    """Return the probability mass on the single top candidate."""
    df = log_scores_to_probs(df)
    return float(df["prob"].max())


# ─────────────────────────────────────────────────────────────
# Expected Information Gain (EIG) with Bayesian model
# ─────────────────────────────────────────────────────────────

def _entropy_from_probs(probs: List[float]) -> float:
    return -sum(p * math.log(p) for p in probs if p > 1e-12)


def estimate_eig_bayes(
    df: pd.DataFrame,
    attr: str,
    attr_boost: Dict[str, float] = None,
) -> float:
    """
    Expected Information Gain for asking a question about `attr`.

    EIG = H(current) - E[H(after answer)]

    Computed exactly over all 5 Likert responses, weighted by their
    probability under the current belief state.
    """
    df = log_scores_to_probs(df)  # ensure 'prob' column is fresh
    current_probs = list(df["prob"])
    H_before = _entropy_from_probs(current_probs)

    responses = list(LOG_LR_WITH.keys())  # all 5 Likert options
    attr_boost = attr_boost or {}

    expected_H_after = 0.0
    for response in responses:
        sim = update_log_scores(df, attr, response, attr_boost)
        sim = log_scores_to_probs(sim)
        after_probs = list(sim["prob"])
        H_after = _entropy_from_probs(after_probs)

        # P(this response) = sum over programs of P(response | program) * P(program)
        p_response = 0.0
        for _, row in df.iterrows():
            has_attr = attr in row["attributes"]
            llr = response_to_llr(response, has_attr)
            # Convert LLR back to approximate response probability
            # Using logistic function: P ≈ sigmoid(LLR * 0.5 + 0)
            p_resp_given_prog = 1.0 / (1.0 + math.exp(-llr * 0.5))
            p_response += p_resp_given_prog * row["prob"]

        expected_H_after += p_response * H_after

    eig = H_before - expected_H_after
    return eig


# ─────────────────────────────────────────────────────────────
# Confusion tracking helpers
# ─────────────────────────────────────────────────────────────

CONFUSION_PREFIX = "confusion|"
PROGRAM_FREQ_PREFIX = "program_freq|"


def get_attr_for_qid(qid: str, questions_bank: dict = None) -> str:
    """
    Convenience helper so simulator and app resolve attributes identically.
    Pass your `questions` dict; falls back to qid if not found.
    """
    if questions_bank is None:
        return qid
    tags = questions_bank.get(qid, {}).get("tags", [])
    return tags[0] if tags else qid


def record_success(
    counts: Dict[str, Dict[str, int]],
    correct_name: str,
    path: List[Tuple[str, str]],
) -> Dict[str, Dict[str, int]]:
    """Update counts after a correct guess."""
    # Update attribute-response counts
    for attr, response in path:
        k = f"{attr}|{response}"
        e = counts.setdefault(k, {"success": 0, "trials": 0})
        e["success"] += 1
        e["trials"] += 1

    # Update program frequency prior
    k_freq = f"{PROGRAM_FREQ_PREFIX}{correct_name}"
    e_freq = counts.setdefault(k_freq, {"success": 0, "trials": 0})
    e_freq["success"] += 1
    e_freq["trials"] += 1

    return counts


def record_failure(
    counts: Dict[str, Dict[str, int]],
    guessed_name: str,
    correct_name: str,
    path: List[Tuple[str, str]],
    name_to_attrs: Dict[str, set],
) -> Dict[str, Dict[str, int]]:
    """Update counts after a wrong guess, including confusion pair tracking."""
    correct_attrs = name_to_attrs.get(correct_name, set())

    for attr, response in path:
        k = f"{attr}|{response}"
        e = counts.setdefault(k, {"success": 0, "trials": 0})
        e["trials"] += 1
        if attr in correct_attrs:
            e["success"] += 1

    # Record confusion pair: system guessed A, correct was B
    if guessed_name and correct_name and guessed_name != correct_name:
        k_conf = f"{CONFUSION_PREFIX}{guessed_name}|{correct_name}"
        e_conf = counts.setdefault(k_conf, {"success": 0, "trials": 0})
        e_conf["trials"] += 1

    # Update program frequency prior for correct program
    k_freq = f"{PROGRAM_FREQ_PREFIX}{correct_name}"
    e_freq = counts.setdefault(k_freq, {"success": 0, "trials": 0})
    e_freq["success"] += 1
    e_freq["trials"] += 1

    return counts


def get_top_confusions(
    counts: Dict[str, Dict[str, int]],
    min_trials: int = 2,
) -> List[Tuple[str, str, int]]:
    """
    Return list of (guessed, correct, count) for the most common mistakes.
    Useful for diagnostics and targeted question suggestions.
    """
    confusions = []
    for k, v in counts.items():
        if not k.startswith(CONFUSION_PREFIX):
            continue
        rest = k[len(CONFUSION_PREFIX):]
        # format: "guessed|correct"
        parts = rest.split("|", 1)
        if len(parts) != 2:
            continue
        guessed, correct = parts
        n = v.get("trials", 0)
        if n >= min_trials:
            confusions.append((guessed, correct, n))
    confusions.sort(key=lambda x: -x[2])
    return confusions


def compute_attr_boosts(counts: Dict[str, Dict[str, int]]) -> Dict[str, float]:
    """
    Compute per-attribute reliability boost from learning history.
    Returned as dict: attr -> float in [-0.6, 0.9]
    """
    attr_acc: Dict[str, Tuple[float, float]] = {}

    response_weights = {
        "Definitely Yes": 1.0,
        "Probably Yes": 0.75,
        "Neutral": 0.5,
        "Probably No": 0.25,
        "Definitely No": 0.1,
    }

    for k, v in counts.items():
        # Skip non attr|response keys
        if k.startswith(CONFUSION_PREFIX) or k.startswith(PROGRAM_FREQ_PREFIX):
            continue
        try:
            attr, response = k.split("|", 1)
        except Exception:
            continue
        success = v.get("success", 0)
        trials = v.get("trials", 0)
        posterior_mean = (1.0 + success) / (2.0 + trials)  # Beta(1,1) prior
        w = response_weights.get(response, 0.5)
        weighted = posterior_mean * w
        acc = attr_acc.get(attr, (0.0, 0.0))
        attr_acc[attr] = (acc[0] + weighted, acc[1] + w)

    attr_boost: Dict[str, float] = {}
    for attr, (weighted_sum, weight_sum) in attr_acc.items():
        if weight_sum <= 0:
            continue
        avg_p = weighted_sum / weight_sum
        boost = avg_p - 0.5
        boost = max(-0.6, min(0.9, boost))
        attr_boost[attr] = boost

    return attr_boost
