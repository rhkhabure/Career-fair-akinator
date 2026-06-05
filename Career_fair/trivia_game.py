"""
trivia_game.py — USIU Trivia + Spin to Win  (Career Fair game 3)

Pool of 17 questions; 8 randomly selected and option-shuffled per game.
Scoring: 7/8 or 8/8 unlocks the Spin to Win wheel.
Wheel prizes (8 segments): Ksh 100, Ksh 50 ×2, Ksh 20 ×2, Wristband,
                            Second Chance, Nothing
Supabase: writes to the shared `winners` table (game='trivia').
"""

import json
from kofi import kofi_html as _kh

# ─────────────────────────────────────────────────────────────
# Question pool  (17 questions — 8 drawn at random each game)
# correct is always the first option; JS shuffles all four.
# ─────────────────────────────────────────────────────────────
QUESTIONS = [
    {"q": "What year was USIU-Africa established in Nairobi?",
     "options": ["1969", "1965", "1972", "1978"],
     "correct": "1969"},
    {"q": "Where is USIU-Africa's main campus located in Nairobi?",
     "options": ["Kasarani, off Thika Road", "Westlands", "Karen", "Kilimani"],
     "correct": "Kasarani, off Thika Road"},
    {"q": "What is USIU-Africa's official motto?",
     "options": ["Education To Take You Places", "Lighting the Way",
                 "Excellence in Africa", "The Global University"],
     "correct": "Education To Take You Places"},
    {"q": "What is the full name of USIU-Africa's business school?",
     "options": ["Chandaria School of Business", "Nairobi Business School",
                 "Kenya Graduate School", "Wambugu School of Commerce"],
     "correct": "Chandaria School of Business"},
    {"q": "What is USIU-Africa's vision statement?",
     "options": [
         "To be a premier institution of academic excellence with a global perspective",
         "The Global University in Africa",
         "Education for the African Century",
         "Excellence with a Global Focus"],
     "correct": "To be a premier institution of academic excellence with a global perspective"},
    {"q": "Which US accreditation body recognises USIU-Africa at degree level?",
     "options": ["WSCUC (Western Association of Schools and Colleges)",
                 "HLC", "SACSCOC", "MSCHE"],
     "correct": "WSCUC (Western Association of Schools and Colleges)"},
    {"q": "Who is the current Vice-Chancellor of USIU-Africa?",
     "options": ["Prof. Mwenda Ntarangwi", "Prof. Freida Brown",
                 "Prof. Juliana Namada", "Prof. Margee Ensign"],
     "correct": "Prof. Mwenda Ntarangwi"},
    {"q": "Who is the current Chancellor of USIU-Africa?",
     "options": ["Ambassador Dennis Awori", "Manu Chandaria",
                 "Dr. Kevit Desai", "Prof. Eileen Wilson-Oyelaran"],
     "correct": "Ambassador Dennis Awori"},
    {"q": "How many schools does USIU-Africa currently have?",
     "options": ["5", "3", "4", "6"],
     "correct": "5"},
    {"q": "Which of these is NOT one of USIU-Africa's schools?",
     "options": ["School of Engineering",
                 "Chandaria School of Business",
                 "School of Pharmacy and Health Sciences",
                 "School of Communication, Cinematic & Creative Arts"],
     "correct": "School of Engineering"},
    {"q": "Approximately how many nationalities are represented at USIU-Africa?",
     "options": ["70+", "20+", "40+", "100+"],
     "correct": "70+"},
    {"q": "In what year did USIU-Africa receive its formal Charter from the Kenyan government?",
     "options": ["1999", "1990", "2001", "2005"],
     "correct": "1999"},
    {"q": "USIU-Africa is described as the most diverse university in which region?",
     "options": ["East and Central Africa", "All of Africa",
                 "Sub-Saharan Africa", "East Africa only"],
     "correct": "East and Central Africa"},
    {"q": "Approximately how many programmes does USIU-Africa offer across all levels?",
     "options": ["38", "15", "25", "50"],
     "correct": "38"},
    {"q": "In which US city was the original United States International University founded?",
     "options": ["San Diego", "Los Angeles", "San Francisco", "Seattle"],
     "correct": "San Diego"},
    {"q": "What type of institution is USIU-Africa?",
     "options": ["Private secular university", "Public government university",
                 "Faith-based private university", "International consortium"],
     "correct": "Private secular university"},
    {"q": "Approximately how many alumni does USIU-Africa have globally?",
     "options": ["25,000+", "5,000+", "10,000+", "50,000+"],
     "correct": "25,000+"},
]

# ─────────────────────────────────────────────────────────────
# Spin wheel  (8 equal segments, 45° each, starting top = -90°)
# ─────────────────────────────────────────────────────────────
SEGMENTS = [
    {"label": "Ksh 100",      "color": "#F5A623",
     "speech": "THE DRUM BOOMS! Ksh 100 — the griot has spoken! 🎵🎵",
     "ksh": 100, "type": "cash"},
    {"label": "Ksh 50",       "color": "#B31B1B",
     "speech": "Ayeee! 50 shillings! The drum never lies! 🥁",
     "ksh": 50,  "type": "cash"},
    {"label": "Wristband",    "color": "#1a4a8a",
     "speech": "Rock the USIU colours! A wristband for a true scholar! 🎓",
     "ksh": 0,   "type": "wristband"},
    {"label": "Ksh 20",       "color": "#D85030",
     "speech": "The drum spoke — Ksh 20 is yours! Every shilling counts! 🥁",
     "ksh": 20,  "type": "cash"},
    {"label": "2nd Chance",   "color": "#2D6A4F",
     "speech": "The drum gives you ANOTHER spin! The griot demands it! 🔄",
     "ksh": 0,   "type": "retry"},
    {"label": "Ksh 20",       "color": "#C04020",
     "speech": "The drum spoke — Ksh 20 coming your way! 🥁",
     "ksh": 20,  "type": "cash"},
    {"label": "Nothing",      "color": "#445566",
     "speech": "The drum is quiet this time… but 7/8 on USIU trivia? That IS the prize. 🎓",
     "ksh": 0,   "type": "nothing"},
    {"label": "Ksh 50",       "color": "#9a1515",
     "speech": "Ayeee! Another 50 bob! The griot is generous today! 🥁",
     "ksh": 50,  "type": "cash"},
]


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _extract(state):
    h = _kh(state)
    s = h.find("<svg"); e = h.rfind("</svg>") + 6
    svg = h[s:e]
    return svg

def _split_defs(svg):
    """Separate <defs>…</defs> from the rest of the SVG string."""
    ds = svg.find("<defs>")
    de = svg.find("</defs>") + 7
    if ds == -1:
        return "", svg
    return svg[ds:de], svg[:ds] + svg[de:]

def _rename(svg, suffix):
    return (svg
        .replace('class="kg"',   f'class="kg-{suffix}"')
        .replace('id="kpkm"',    f'id="kpkm-{suffix}"')
        .replace('url(#kpkm)',   f'url(#kpkm-{suffix})')
        .replace('id="krcm"',    f'id="krcm-{suffix}"')
        .replace('clip-path="url(#krcm)"', f'clip-path="url(#krcm-{suffix})"')
    )

def _kf():
    """Extract keyframe CSS from kofi_html (all @keyframes blocks)."""
    h = _kh("thinking")
    raw = h[h.find("<style>")+7:h.find("</style>")]
    parts = raw.split("@keyframes ")[1:]
    kfs = []
    for tok in parts:
        close = tok.find("}}")
        kfs.append("@keyframes " + tok[:close+2])
    return "\n".join(kfs)


# ─────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────

def trivia_game_html(supabase_url="", supabase_key=""):
    """Return a self-contained HTML string for the trivia + spin-to-win game."""

    svg_think = _rename(_extract("thinking"), "tt")
    svg_right = _rename(_extract("correct"),  "tc")
    svg_wrong = _rename(_extract("wrong"),    "tw")

    # Split each SVG into <defs> and body; pool all defs in one always-visible
    # sprite SVG so url(#…) references are always resolvable regardless of which
    # Kofi state was last inserted via innerHTML.
    defs_t, body_t = _split_defs(svg_think)
    defs_c, body_c = _split_defs(svg_right)
    defs_w, body_w = _split_defs(svg_wrong)

    sprite = (
        "<svg style='position:absolute;width:0;height:0;overflow:hidden;' aria-hidden='true'>"
        f"{defs_t}{defs_c}{defs_w}"
        "</svg>"
    )

    kf_css   = _kf()
    js_think = json.dumps(body_t)   # body-only (no defs) — refs sprite IDs
    js_right = json.dumps(body_c)
    js_wrong = json.dumps(body_w)
    q_json   = json.dumps(QUESTIONS)
    seg_json = json.dumps(SEGMENTS)

    kofi_css = kf_css + """
.kg-tt{animation:kft  3.8s  ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.kg-tc{animation:kfb  0.55s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.kg-tw{animation:kfs  3s    ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.kwv{animation:kwv 2.6s ease-in-out infinite;}
"""

    css = """
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:#0D1B2A;color:#d0dde8;
  font-family:'Segoe UI',Arial,sans-serif;font-size:14px;}
.scr{display:none;padding:14px 18px;}.scr.on{display:block;}
.wrap{max-width:500px;margin:0 auto;text-align:center;}
.kofi-md{max-width:230px;margin:0 auto;}
.kofi-sm{width:72px;flex-shrink:0;}
.sp{font-size:12px;font-style:italic;color:#c8a060;padding:2px 12px 8px;min-height:28px;text-align:center;}
.r-title{font-size:1.45rem;font-weight:700;color:#fff;margin:0 0 4px;}
.r-sub{font-size:13px;color:#a0b4c8;margin:0 0 14px;line-height:1.5;}
.rules{background:#152333;border-radius:10px;padding:12px 16px;text-align:left;margin:10px 0 16px;}
.rule{display:flex;gap:10px;margin-bottom:7px;font-size:12.5px;color:#d0dde8;}
.ri{font-size:16px;min-width:22px;}
.start-btn{width:100%;max-width:280px;padding:14px;background:#B31B1B;color:#fff;
  font-size:1.05rem;font-weight:700;border:none;border-radius:12px;cursor:pointer;
  box-shadow:0 4px 16px rgba(179,27,27,.4);transition:all .2s;}
.start-btn:hover{opacity:.9;transform:translateY(-1px);}
.q-hd{display:flex;align-items:center;gap:10px;margin-bottom:10px;}
.q-prog{font-size:12px;color:#a0b4c8;font-weight:500;white-space:nowrap;}
.score-cur{background:#152333;border:1px solid #2a4060;border-radius:16px;
  padding:3px 12px;font-size:12px;font-weight:600;color:#F5A623;}
.q-text{font-size:1.05rem;font-weight:700;color:#fff;line-height:1.45;
  background:#152333;border-left:4px solid #B31B1B;padding:12px 16px;
  border-radius:0 10px 10px 0;margin-bottom:12px;text-align:left;}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;}
.opt{padding:10px 14px;background:#152333;border:1.5px solid #2a4060;
  border-radius:10px;cursor:pointer;font-size:13px;color:#d0dde8;text-align:left;
  transition:all .15s;line-height:1.35;}
.opt:hover:not(.disabled){background:#1e3044;border-color:#F5A623;color:#fff;}
.opt.correct{background:#0f2a1a;border-color:#6ee7b7;color:#6ee7b7;font-weight:600;}
.opt.wrong-sel{background:#2a0f0f;border-color:#f87171;color:#f87171;}
.opt.show-ans{background:#0f2a1a;border-color:#6ee7b7;color:#6ee7b7;}
.opt.disabled{cursor:default;opacity:.65;}
.fb-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:8px;
  font-size:13px;font-weight:600;margin-bottom:8px;}
.fb-ok{background:#0f2a1a;color:#6ee7b7;border:1px solid #2a5a3a;}
.fb-no{background:#2a0f0f;color:#f87171;border:1px solid #5a2a2a;}
.score-big{font-size:3.2rem;font-weight:800;color:#F5A623;line-height:1;}
.score-lbl{font-size:13px;color:#a0b4c8;margin-bottom:10px;}
.score-msg{font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:10px;}
.miss-box{background:#0f1d2b;border-radius:10px;padding:12px;text-align:left;
  margin:10px 0;max-height:220px;overflow-y:auto;}
.miss-ttl{font-size:10px;font-weight:700;color:#F5A623;letter-spacing:.9px;
  text-transform:uppercase;margin-bottom:8px;}
.miss-item{font-size:12px;color:#d0dde8;margin-bottom:6px;line-height:1.4;}
.miss-q{color:#a0b4c8;margin-bottom:2px;}
.miss-a{color:#6ee7b7;font-weight:600;}
.spin-btn{width:100%;max-width:260px;padding:14px;background:#F5A623;color:#0a1520;
  font-size:1.05rem;font-weight:700;border:none;border-radius:12px;cursor:pointer;
  transition:all .2s;box-shadow:0 4px 16px rgba(245,166,35,.4);}
.spin-btn:hover:not(:disabled){opacity:.9;transform:translateY(-1px);}
.spin-btn:disabled{opacity:.45;cursor:not-allowed;}
.wheel-wrap{position:relative;width:300px;height:300px;margin:0 auto;}
.ptr{position:absolute;top:-4px;left:50%;transform:translateX(-50%);
  z-index:10;font-size:24px;color:#F5A623;line-height:1;}
.prize-card{background:#152333;border-radius:12px;padding:14px 20px;
  text-align:center;margin-top:8px;}
.prize-name{font-size:1.6rem;font-weight:800;margin-bottom:4px;}
.rwd-banner{background:linear-gradient(135deg,#0f2a1a,#0a1e12);
  border:1.5px solid #6ee7b7;border-radius:10px;padding:12px 16px;margin:12px 0;}
.rwd-ksh{font-size:1.55rem;font-weight:800;color:#6ee7b7;margin-bottom:3px;}
.rwd-note{font-size:11.5px;color:#a0c8a0;}
.cf input{width:100%;padding:9px 12px;margin:5px 0;background:#0f1d2b;
  border:1px solid #2a4060;border-radius:8px;color:#d0dde8;font-size:13px;outline:none;}
.cf input:focus{border-color:#F5A623;}
.cl-btn{width:100%;padding:11px;margin-top:8px;background:#6ee7b7;color:#0a2010;
  font-size:14px;font-weight:700;border:none;border-radius:10px;cursor:pointer;}
.cl-btn:disabled{opacity:.5;cursor:not-allowed;}
.code-box{background:#0f1d2b;border:2px solid #F5A623;border-radius:10px;padding:16px;margin:10px 0;}
.code-lbl{font-size:11px;color:#a0b4c8;margin-bottom:4px;}
.code-val{font-size:1.75rem;font-weight:800;color:#F5A623;letter-spacing:3px;font-family:monospace;}
.code-hint{font-size:11.5px;color:#6ee7b7;margin-top:6px;}
.again-btn{width:100%;max-width:260px;padding:10px;background:#1a2e42;color:#d0dde8;
  border:1px solid #2a4060;border-radius:10px;font-size:14px;cursor:pointer;
  margin-top:12px;transition:all .2s;}
.again-btn:hover{border-color:#F5A623;color:#F5A623;}
""" + kofi_css

    html = (
        "<!DOCTYPE html><html lang='en'><head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{css}</style></head><body>"
        f"{sprite}"   # permanent defs — always in DOM, always resolvable

        # ── Kofi SVG JS constants ──────────────────────────────────────
        "<script>"
        f"const _ST={js_think},_SC={js_right},_SW={js_wrong};"
        "function kofiSVG(k){{return k==='t'?_ST:k==='c'?_SC:_SW;}}"
        f"const QPOOL={q_json};"
        f"const SEGS={seg_json};"
        f"const SB_URL='{supabase_url}',SB_KEY='{supabase_key}';"
        "</script>"

        # ══════════════════════════════ PHASE 1 — READY ═══════════════
        "<div id='s-ready' class='scr on'>"
        "<div class='wrap'>"
        "<div class='kofi-md' id='rk'></div>"
        "<div class='sp' id='rk-sp'>Think you know USIU-Africa? Let's find out&#8230;</div>"
        "<h1 class='r-title'>USIU Trivia</h1>"
        "<p class='r-sub'>8 questions about your university.<br>"
        "Score 7 or 8 out of 8 and spin to win!</p>"
        "<div class='rules'>"
        "<div class='rule'><span class='ri'>❓</span><span><strong>8 questions</strong>, multiple choice</span></div>"
        "<div class='rule'><span class='ri'>✅</span><span>Get <strong>7/8 or 8/8</strong> to unlock the spin wheel</span></div>"
        "<div class='rule'><span class='ri'>🎰</span><span>Spin to win <strong>Ksh 20, 50, 100</strong> or a <strong>wristband</strong></span></div>"
        "<div class='rule'><span class='ri'>🔄</span><span>Land on <em>Second Chance</em> and spin again!</span></div>"
        "</div>"
        "<button class='start-btn' onclick='startGame()'>🥁 Start Trivia!</button>"
        "</div></div>"

        # ══════════════════════════════ PHASE 2 — QUESTION ════════════
        "<div id='s-q' class='scr'>"
        "<div class='q-hd'>"
        "<div class='kofi-sm' id='qk'></div>"
        "<div style='flex:1;'>"
        "<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;'>"
        "<span class='q-prog' id='qprog'>Question 1 of 8</span>"
        "<span class='score-cur' id='qscore'>0 correct</span>"
        "</div>"
        "<div style='background:#1e3044;border-radius:4px;height:5px;overflow:hidden;'>"
        "<div id='qbar' style='height:5px;background:linear-gradient(90deg,#B31B1B,#F5A623);"
        "border-radius:4px;transition:width .4s;width:0;'></div>"
        "</div>"
        "</div></div>"
        "<div class='sp' id='qk-sp'></div>"
        "<div class='q-text' id='q-text'></div>"
        "<div class='opts' id='q-opts'></div>"
        "<div id='q-fb' style='display:none;'></div>"
        "</div>"

        # ══════════════════════════════ PHASE 3 — SCORE ═══════════════
        "<div id='s-score' class='scr'>"
        "<div class='wrap'>"
        "<div class='kofi-md' id='sk'></div>"
        "<div class='sp' id='sk-sp'></div>"
        "<div style='display:flex;align-items:baseline;justify-content:center;gap:10px;margin:8px 0 2px;'>"
        "<div class='score-big' id='sc-n'>0</div>"
        "<div style='font-size:1.2rem;color:#a0b4c8;font-weight:600;'>/ 8</div>"
        "</div>"
        "<div class='score-lbl'>questions correct</div>"
        "<div class='score-msg' id='sc-msg'></div>"
        "<div class='miss-box' id='miss-box' style='display:none;'>"
        "<div class='miss-ttl'>Correct answers for the ones you missed</div>"
        "<div id='miss-list'></div>"
        "</div>"
        "<div id='sc-btns' style='margin-top:14px;'></div>"
        "</div></div>"

        # ══════════════════════════════ PHASE 4 — SPIN ════════════════
        "<div id='s-spin' class='scr'>"
        "<div class='wrap'>"
        "<div class='kofi-md' id='spk'></div>"
        "<div class='sp' id='spk-sp'>The drum decides your fate&#8230;</div>"
        "<div class='wheel-wrap'>"
        "<div class='ptr'>&#9660;</div>"
        "<svg id='tw' width='300' height='300' viewBox='-150 -150 300 300' style='overflow:visible;'>"
        "<g id='twheel'>"
        "<path d='M0,0 L0,-140 A140,140,0,0,1,99,-99 Z' fill='#F5A623'/>"
        "<path d='M0,0 L99,-99 A140,140,0,0,1,140,0 Z' fill='#B31B1B'/>"
        "<path d='M0,0 L140,0 A140,140,0,0,1,99,99 Z' fill='#1a4a8a'/>"
        "<path d='M0,0 L99,99 A140,140,0,0,1,0,140 Z' fill='#D85030'/>"
        "<path d='M0,0 L0,140 A140,140,0,0,1,-99,99 Z' fill='#2D6A4F'/>"
        "<path d='M0,0 L-99,99 A140,140,0,0,1,-140,0 Z' fill='#C04020'/>"
        "<path d='M0,0 L-140,0 A140,140,0,0,1,-99,-99 Z' fill='#445566'/>"
        "<path d='M0,0 L-99,-99 A140,140,0,0,1,0,-140 Z' fill='#9a1515'/>"
        "<line x1='0' y1='0' x2='0' y2='-140' stroke='#0a1520' stroke-width='1.5'/>"
        "<line x1='0' y1='0' x2='99' y2='-99' stroke='#0a1520' stroke-width='1.5'/>"
        "<line x1='0' y1='0' x2='140' y2='0' stroke='#0a1520' stroke-width='1.5'/>"
        "<line x1='0' y1='0' x2='99' y2='99' stroke='#0a1520' stroke-width='1.5'/>"
        "<line x1='0' y1='0' x2='0' y2='140' stroke='#0a1520' stroke-width='1.5'/>"
        "<line x1='0' y1='0' x2='-99' y2='99' stroke='#0a1520' stroke-width='1.5'/>"
        "<line x1='0' y1='0' x2='-140' y2='0' stroke='#0a1520' stroke-width='1.5'/>"
        "<line x1='0' y1='0' x2='-99' y2='-99' stroke='#0a1520' stroke-width='1.5'/>"
        "<circle r='22' fill='#0a1520'/><circle r='18' fill='#1a2e3a'/>"
        "<text y='6' text-anchor='middle' fill='#F5A623' font-size='9' font-weight='600'>SPIN</text>"
        "<g transform='rotate(22.5) translate(0,-88)' fill='white' font-size='9.5' font-weight='600' text-anchor='middle'><text>Ksh 100</text></g>"
        "<g transform='rotate(67.5) translate(0,-88)' fill='white' font-size='9.5' font-weight='600' text-anchor='middle'><text>Ksh 50</text></g>"
        "<g transform='rotate(112.5) translate(0,-86)' fill='white' font-size='8.5' font-weight='600' text-anchor='middle'><text>Wristband</text></g>"
        "<g transform='rotate(157.5) translate(0,-88)' fill='white' font-size='9.5' font-weight='600' text-anchor='middle'><text>Ksh 20</text></g>"
        "<g transform='rotate(202.5) translate(0,-82)' fill='white' font-size='8' font-weight='600' text-anchor='middle'><text>2nd Chance</text></g>"
        "<g transform='rotate(247.5) translate(0,-88)' fill='white' font-size='9.5' font-weight='600' text-anchor='middle'><text>Ksh 20</text></g>"
        "<g transform='rotate(292.5) translate(0,-86)' fill='white' font-size='9' font-weight='600' text-anchor='middle'><text>Nothing</text></g>"
        "<g transform='rotate(337.5) translate(0,-88)' fill='white' font-size='9.5' font-weight='600' text-anchor='middle'><text>Ksh 50</text></g>"
        "</g>"
        "<circle r='142' fill='none' stroke='#2a3a4a' stroke-width='3'/>"
        "</svg>"
        "</div>"
        "<button class='spin-btn' id='sp-btn' onclick='doSpin()'>🥁 Spin the wheel!</button>"
        "<div id='prize-card' class='prize-card' style='display:none;'>"
        "<div class='prize-name' id='prize-name'></div>"
        "<div class='sp' id='prize-sp'></div>"
        "<div id='claim-section' style='display:none;'>"
        "<div class='rwd-banner'><div class='rwd-ksh' id='rwd-ksh'></div>"
        "<div class='rwd-note'>Enter your details below to claim</div></div>"
        "<div class='cf' id='cf-div'>"
        "<input type='text' id='pname' placeholder='Full name *' autocomplete='off'>"
        "<input type='text' id='pid' placeholder='Student / Staff ID (optional)' autocomplete='off'>"
        "<button class='cl-btn' id='cl-btn' onclick='submitClaim()'>Claim Reward &#8594;</button>"
        "</div>"
        "<div id='cf-done' style='display:none;'>"
        "<div class='code-box'>"
        "<div class='code-lbl'>Your reward code</div>"
        "<div class='code-val' id='rcode'></div>"
        "<div class='code-hint'>Show this to booth staff to receive your reward &#127881;</div>"
        "</div></div></div>"
        "<div id='nothing-sec' style='display:none;'>"
        "<p style='font-size:12.5px;color:#a0b4c8;font-style:italic;margin:8px 0;'>"
        "Your USIU knowledge is the real prize. Go study that extra chapter! &#127891;"
        "</p></div>"
        "<button class='again-btn' id='sp-again' style='display:none;' onclick='resetGame()'>&#128260; Play Again</button>"
        "</div>"
        "</div></div>"

        # ══════════════════════════════ JAVASCRIPT ════════════════════
        "<script>"
        r"""
let gQuestions=[], gIdx=0, gScore=0, gCorrectIdx=[], gMissed=[];
let wheelRot=0, spinning=false, finalScore=0;

function show(id){document.querySelectorAll('.scr').forEach(s=>s.classList.remove('on'));document.getElementById(id).classList.add('on');}

function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}

function startGame(){
  const pool=shuffle([...QPOOL]).slice(0,8);
  gQuestions=pool.map(q=>{
    const opts=shuffle([...q.options]);
    return {...q,shuffled:opts,correctIdx:opts.indexOf(q.correct)};
  });
  gIdx=0;gScore=0;gMissed=[];gCorrectIdx=[];
  document.getElementById('qk').innerHTML=kofiSVG('t');
  showQ();
  show('s-q');
}

function showQ(){
  const q=gQuestions[gIdx];
  document.getElementById('qprog').textContent=`Question ${gIdx+1} of 8`;
  document.getElementById('qscore').textContent=`${gScore} correct`;
  document.getElementById('qbar').style.width=(gIdx/8*100)+'%';
  document.getElementById('q-text').textContent=q.q;
  const labels=['A','B','C','D'];
  document.getElementById('q-opts').innerHTML=q.shuffled.map((o,i)=>
    `<button class="opt" onclick="pick(${i})">${labels[i]}) ${o}</button>`
  ).join('');
  document.getElementById('q-fb').style.display='none';
  document.getElementById('qk').innerHTML=kofiSVG('t');
  document.getElementById('qk-sp').textContent='';
}

function pick(i){
  const q=gQuestions[gIdx];
  const correct=i===q.correctIdx;
  if(correct)gScore++;else gMissed.push({q:q.q,ans:q.correct});
  document.querySelectorAll('.opt').forEach((el,idx)=>{
    el.classList.add('disabled');
    if(idx===q.correctIdx)el.classList.add('show-ans');
    else if(idx===i&&!correct)el.classList.add('wrong-sel');
  });
  const fb=document.getElementById('q-fb');
  fb.style.display='block';
  fb.className='fb-bar '+(correct?'fb-ok':'fb-no');
  fb.textContent=correct?'✓ Correct!':'✗ The correct answer was: '+q.correct;
  document.getElementById('qk').innerHTML=kofiSVG(correct?'c':'w');
  document.getElementById('qk-sp').textContent=correct?'Ayeee! 🥁':'Hmm… not quite.';
  setTimeout(()=>{
    gIdx++;
    if(gIdx<8)showQ();
    else showScore();
  },1700);
}

function showScore(){
  finalScore=gScore;
  const sk=document.getElementById('sk');
  const sp=document.getElementById('sk-sp');
  const msg=document.getElementById('sc-msg');
  document.getElementById('sc-n').textContent=gScore;
  if(gScore>=7){
    sk.innerHTML=kofiSVG('c');
    sp.textContent=gScore===8?'PERFECT SCORE! The griot is amazed! 🎵':'7 out of 8 — outstanding! 🥁';
    msg.textContent=gScore===8?'Flawless. You truly know your university!':'Excellent! You\'ve earned the spin!';
    const btns=document.getElementById('sc-btns');
    btns.innerHTML=`<button class="spin-btn" onclick="goSpin()">🎰 Spin the Wheel!</button>`;
  } else {
    sk.innerHTML=kofiSVG('w');
    sp.textContent='Good effort — check what you missed and try again! 📚';
    const msgs={6:'So close! 6/8.',5:'5/8 — study those facts!',4:'4/8 — keep learning!',0:'0/8 — that\'s a start!'};
    msg.textContent=msgs[gScore]||`${gScore}/8 — keep studying!`;
    if(gMissed.length){
      const mb=document.getElementById('miss-box');
      mb.style.display='block';
      document.getElementById('miss-list').innerHTML=gMissed.map(m=>
        `<div class="miss-item"><div class="miss-q">${m.q}</div><div class="miss-a">✓ ${m.ans}</div></div>`
      ).join('');
    }
    document.getElementById('sc-btns').innerHTML=
      `<button class="again-btn" onclick="resetGame()">🔄 Try Again</button>`;
  }
  show('s-score');
}

function goSpin(){
  document.getElementById('spk').innerHTML=kofiSVG('t');
  document.getElementById('spk-sp').textContent='The drum decides your fate…';
  document.getElementById('prize-card').style.display='none';
  document.getElementById('sp-btn').disabled=false;
  document.getElementById('sp-btn').textContent='🥁 Spin the wheel!';
  document.getElementById('sp-again').style.display='none';
  show('s-spin');
}

function doSpin(){
  if(spinning)return;
  spinning=true;
  document.getElementById('sp-btn').disabled=true;
  const seg=Math.floor(Math.random()*8);
  const base=337.5-seg*45;
  const spins=5+Math.floor(Math.random()*4);
  const delta=((base-(wheelRot%360))+360)%360;
  wheelRot+=spins*360+delta;
  const el=document.getElementById('twheel');
  el.style.transition='transform 4.5s cubic-bezier(0.17,0.67,0.12,1)';
  el.style.transform=`rotate(${wheelRot}deg)`;
  setTimeout(()=>{spinning=false;handlePrize(SEGS[seg]);},4700);
}

function handlePrize(seg){
  const card=document.getElementById('prize-card');
  const pn=document.getElementById('prize-name');
  const ps=document.getElementById('prize-sp');
  pn.textContent=seg.label;
  pn.style.color=seg.color;
  ps.textContent='🥁 '+seg.speech;
  card.style.display='block';
  document.getElementById('claim-section').style.display='none';
  document.getElementById('nothing-sec').style.display='none';
  document.getElementById('sp-again').style.display='none';
  document.getElementById('cf-done').style.display='none';
  document.getElementById('cf-div').style.display='block';
  if(seg.type==='retry'){
    document.getElementById('spk').innerHTML=kofiSVG('t');
    document.getElementById('spk-sp').textContent='Spin again — the griot demands it! 🔄';
    document.getElementById('sp-btn').disabled=false;
    document.getElementById('sp-btn').textContent='🔄 Spin again!';
  } else if(seg.type==='nothing'){
    document.getElementById('spk').innerHTML=kofiSVG('w');
    document.getElementById('nothing-sec').style.display='block';
    document.getElementById('sp-again').style.display='inline-block';
  } else {
    const ksh=seg.ksh;
    document.getElementById('spk').innerHTML=kofiSVG('c');
    document.getElementById('claim-section').style.display='block';
    const rwd=ksh>0?`Ksh ${ksh} credit reward!`:`${seg.label} reward!`;
    document.getElementById('rwd-ksh').textContent=rwd;
    document.getElementById('cl-btn').textContent=
      ksh>0?`Claim Ksh ${ksh} →`:'Claim Wristband →';
    document.getElementById('cl-btn').dataset.ksh=ksh;
    document.getElementById('cl-btn').dataset.type=seg.type;
    document.getElementById('cl-btn').dataset.label=seg.label;
  }
}

function genCode(label){
  const c='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let s='';for(let i=0;i<6;i++)s+=c[Math.floor(Math.random()*c.length)];
  const pfx=label.replace(/[^A-Z0-9]/gi,'').substring(0,4).toUpperCase();
  return`USIU-${pfx}-${s}`;
}

async function submitClaim(){
  const name=document.getElementById('pname').value.trim();
  if(!name){document.getElementById('pname').style.borderColor='#f87171';return;}
  const sid=document.getElementById('pid').value.trim();
  const btn=document.getElementById('cl-btn');
  const ksh=parseInt(btn.dataset.ksh||'0');
  const label=btn.dataset.label||'prize';
  const code=genCode(label);
  btn.textContent='Saving…';btn.disabled=true;
  if(SB_URL&&SB_KEY){
    try{
      await fetch(SB_URL+'/rest/v1/winners',{
        method:'POST',
        headers:{'Content-Type':'application/json',
                 'apikey':SB_KEY,'Authorization':'Bearer '+SB_KEY,
                 'Prefer':'return=minimal'},
        body:JSON.stringify({name,student_id:sid||null,game:'trivia',
                             score:finalScore,time_left:null,
                             reward_ksh:ksh,reward_code:code,
                             claimed:false})
      });
    }catch(e){console.warn('Supabase save failed:',e);}
  }
  document.getElementById('cf-div').style.display='none';
  document.getElementById('rcode').textContent=code;
  document.getElementById('cf-done').style.display='block';
  document.getElementById('sp-again').style.display='inline-block';
}

function resetGame(){
  wheelRot=0;spinning=false;
  const el=document.getElementById('twheel');
  el.style.transition='none';
  el.style.transform='rotate(0deg)';
  document.getElementById('miss-box').style.display='none';
  document.getElementById('miss-list').innerHTML='';
  document.getElementById('pname').value='';
  document.getElementById('pid').value='';
  document.getElementById('pname').style.borderColor='';
  document.getElementById('rk').innerHTML=kofiSVG('t');
  show('s-ready');
}

document.getElementById('rk').innerHTML=kofiSVG('t');
"""
        "</script></body></html>"
    )

    return html
