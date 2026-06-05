"""
cv_game.py — 'Spot the CV Mistakes' game for the USIU Career Fair booth.

Usage:
    from cv_game import cv_game_html
    st.components.v1.html(
        cv_game_html(supabase_url, supabase_key),
        height=860, scrolling=True
    )

Three phases
------------
ready   Kofi intro + rules card + START button
game    30-second timer, CV with 5 clickable error zones, small Kofi sidebar
result  Large Kofi (state depends on score) + breakdown + claim form

Scoring
-------
5 / 5  →  Kofi BOOM, Ksh 100 claim form
4 / 5  →  Kofi celebrate, Ksh 50 claim form
3 / 5  →  Kofi congratulates, explains all missed errors, parting remark
< 3    →  Kofi teaches, full error breakdown, parting remark

Supabase
--------
Writes directly to the `winners` table from JavaScript (no Streamlit round-trip).
Falls back gracefully if SB_URL / SB_KEY are empty — shows the reward code anyway.
"""

from kofi import kofi_html as _kh


# ── helpers ──────────────────────────────────────────────────────────────────

def _extract(state: str) -> tuple[str, str]:
    """Return (svg_html, keyframe_css) from kofi_html for a given state."""
    h = _kh(state)
    # CSS: keyframes only — we rebuild .kg rules ourselves per-state
    style_start = h.find("<style>") + 7
    style_end   = h.find("</style>")
    raw_css     = h[style_start:style_end]
    # Keep only @keyframe blocks and .kwv (sound-wave class)
    lines = raw_css.split(";")
    kf_css = []
    in_kf  = False
    for tok in raw_css.split("@keyframes ")[1:]:   # split on each @keyframes
        name = tok.split("{")[0].strip()
        close = tok.find("}}")
        body  = tok[:close + 2]
        kf_css.append(f"@keyframes {body}")
    kwv = ".kwv{animation:kwv 2.6s ease-in-out infinite;}"
    full_kf = "\n".join(kf_css) + "\n" + kwv

    # SVG element
    s_start = h.find("<svg")
    s_end   = h.rfind("</svg>") + 6
    svg     = h[s_start:s_end]
    return svg, full_kf


def _rename_kg(svg: str, suffix: str) -> str:
    """Rename the .kg class AND all defs IDs in a Kofi SVG to avoid
    ID collisions when multiple instances share the same HTML document."""
    return (svg
        .replace('class="kg"',       f'class="kg-{suffix}"')
        .replace('id="kpkm"',        f'id="kpkm-{suffix}"')
        .replace('url(#kpkm)',       f'url(#kpkm-{suffix})')
        .replace('id="krcm"',        f'id="krcm-{suffix}"')
        .replace('clip-path="url(#krcm)"', f'clip-path="url(#krcm-{suffix})"')
    )

def _split_defs(svg: str) -> tuple[str, str]:
    """Separate <defs>…</defs> from the visual body of an SVG string."""
    ds = svg.find("<defs>")
    de = svg.find("</defs>") + 7
    if ds == -1:
        return "", svg
    return svg[ds:de], svg[:ds] + svg[de:]


# ── public API ────────────────────────────────────────────────────────────────

def cv_game_html(supabase_url: str = "", supabase_key: str = "") -> str:
    """Return a self-contained HTML string for the CV game."""

    import json

    svg_think,  kf_css = _extract("thinking")
    svg_right,  _      = _extract("correct")
    svg_wrong,  _      = _extract("wrong")

    # Give every instance unique defs IDs so url(#...) references never collide
    svg_think = _rename_kg(svg_think, "t")
    svg_right = _rename_kg(svg_right, "c")
    svg_wrong = _rename_kg(svg_wrong, "w")

    # Sprite SVG: permanent home for all <defs> — always in DOM, never display:none
    # so url(#...) refs resolve correctly even after multiple innerHTML re-insertions.
    defs_t, body_t = _split_defs(svg_think)
    defs_c, body_c = _split_defs(svg_right)
    defs_w, body_w = _split_defs(svg_wrong)
    sprite = (
        "<svg style='position:absolute;width:0;height:0;overflow:hidden;' aria-hidden='true'>"
        f"{defs_t}{defs_c}{defs_w}"
        "</svg>"
    )

    # Encode body-only SVGs (no defs) as JS string literals
    js_think = json.dumps(body_t)
    js_right = json.dumps(body_c)
    js_wrong = json.dumps(body_w)

    # Build combined Kofi animation CSS for all three states
    kofi_anim_css = kf_css + """
.kg-t{ animation: kft  3.8s  ease-in-out infinite; transform-box:fill-box; transform-origin:center; }
.kg-c{ animation: kfb  0.55s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }
.kg-w{ animation: kfs  3s    ease-in-out infinite; transform-box:fill-box; transform-origin:center; }
"""

    html = (
        "<!DOCTYPE html><html lang='en'><head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>"

        # ── base ──
        "*{box-sizing:border-box;} "
        "html,body{margin:0;padding:0;background:#0D1B2A;color:#d0dde8;"
        "font-family:'Segoe UI',Arial,sans-serif;font-size:14px;} "

        # ── screens ──
        ".scr{display:none;padding:14px 18px;} "
        ".scr.on{display:block;} "

        # ── ready screen ──
        ".ready-wrap{max-width:460px;margin:0 auto;text-align:center;} "
        ".kofi-mid{max-width:240px;margin:0 auto;} "
        ".kofi-speech{font-size:12px;font-style:italic;color:#c8a060;"
        "margin-top:-6px;padding:0 12px 10px;} "
        ".r-title{font-size:1.45rem;font-weight:700;color:#fff;margin-bottom:4px;} "
        ".r-sub{font-size:13px;color:#a0b4c8;margin-bottom:14px;line-height:1.5;} "
        ".rules{background:#152333;border-radius:10px;padding:12px 16px;"
        "text-align:left;margin:10px 0 16px;} "
        ".rule{display:flex;gap:10px;margin-bottom:7px;font-size:12.5px;color:#d0dde8;} "
        ".ri{font-size:16px;min-width:22px;} "
        ".start-btn{width:100%;max-width:280px;padding:14px;"
        "background:#B31B1B;color:#fff;font-size:1.05rem;font-weight:700;"
        "border:none;border-radius:12px;cursor:pointer;"
        "box-shadow:0 4px 16px rgba(179,27,27,.4);transition:all .2s;} "
        ".start-btn:hover{opacity:.9;transform:translateY(-1px);} "

        # ── game screen ──
        ".g-top{display:flex;align-items:center;gap:10px;margin-bottom:8px;} "
        ".kofi-sm{width:75px;flex-shrink:0;} "
        ".timer-row{display:flex;align-items:center;gap:10px;margin-bottom:6px;} "
        "#timer-num{font-size:22px;font-weight:700;color:#F5A623;min-width:44px;} "
        "#timer-num.danger{color:#f87171;animation:blink .5s step-end infinite;} "
        "@keyframes blink{0%,100%{opacity:1}50%{opacity:.35}} "
        ".t-track{background:#1e3044;border-radius:6px;height:7px;flex:1;overflow:hidden;} "
        ".t-fill{height:100%;background:linear-gradient(90deg,#B31B1B,#F5A623);"
        "border-radius:6px;transition:width .25s linear;} "
        ".s-badge{background:#152333;border:1px solid #2a4060;border-radius:20px;"
        "padding:4px 14px;font-size:13px;font-weight:600;color:#F5A623;white-space:nowrap;} "
        ".instr{font-size:11.5px;color:#a0b4c8;font-style:italic;line-height:1.45;} "

        # ── CV document ──
        ".cv-doc{background:#fff;color:#111;border-radius:10px;overflow:hidden;"
        "box-shadow:0 4px 24px rgba(0,0,0,.45);max-width:600px;margin:0 auto;"
        "font-size:12.5px;line-height:1.55;} "
        ".cv-hd{background:#1a2a3a;padding:14px 18px;} "
        ".cv-name{font-size:18px;font-weight:700;color:#fff;margin-bottom:3px;} "
        ".cv-ct{font-size:11px;color:#8ab0cc;display:flex;flex-wrap:wrap;gap:8px;align-items:center;} "
        ".cv-sep{color:#3a5060;} "
        ".cv-photo{float:right;width:54px;height:66px;background:#2a3f54;"
        "border:1px solid #3a5060;border-radius:3px;margin-left:12px;"
        "display:flex;align-items:center;justify-content:center;"
        "font-size:10px;color:#6a8aaa;text-align:center;line-height:1.3;cursor:pointer;} "
        ".cv-sec{padding:9px 18px;border-top:1px solid #e8e8e8;} "
        ".cv-sh{font-size:9.5px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;"
        "color:#1a4a7a;margin-bottom:5px;} "
        ".cv-jh{display:flex;justify-content:space-between;align-items:baseline;gap:8px;} "
        ".cv-jt{font-weight:700;font-size:12.5px;color:#111;} "
        ".cv-jd{font-size:11px;color:#5a7a8a;white-space:nowrap;} "
        ".cv-js{font-size:11.5px;color:#4a4a4a;margin-bottom:3px;} "
        ".cv-b{font-size:12px;color:#2a2a2a;padding-left:12px;position:relative;margin-bottom:2px;} "
        ".cv-b::before{content:'•';position:absolute;left:0;} "
        ".cv-pill{display:inline-block;background:#f0f4f8;border:1px solid #dce4ec;"
        "border-radius:3px;padding:2px 7px;font-size:11px;color:#2a3a4a;margin:2px 2px 2px 0;} "

        # ── error zones ──
        ".ez{cursor:pointer;border-radius:3px;outline:2px dashed transparent;"
        "outline-offset:2px;transition:background .12s,outline .12s;} "
        ".ezb{cursor:pointer;border-radius:3px;display:block;"
        "outline:2px dashed transparent;outline-offset:2px;transition:background .12s,outline .12s;} "
        ".ezp{cursor:pointer;border-radius:3px;"
        "outline:2px dashed transparent;outline-offset:1px;} "
        ".ez:hover,.ezb:hover,.ezp:hover{"
        "background:rgba(245,166,35,.12);outline-color:#F5A62388;} "
        ".ez.found,.ezb.found,.ezp.found{"
        "background:rgba(110,231,183,.2);outline-color:#6ee7b7;cursor:default;} "
        ".ez.missed,.ezb.missed,.ezp.missed{"
        "background:rgba(248,113,113,.15);outline-color:#f87171;} "

        # ── result screen ──
        ".res-card{background:#152333;border-radius:14px;padding:20px;"
        "max-width:480px;margin:0 auto;text-align:center;} "
        ".kofi-big{max-width:280px;margin:0 auto;} "
        ".res-score{font-size:3rem;font-weight:800;color:#F5A623;line-height:1;} "
        ".res-sub{font-size:13px;color:#a0b4c8;margin-bottom:10px;} "
        ".res-msg{font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:8px;} "
        ".miss-box{background:#0f1d2b;border-radius:10px;padding:12px;"
        "text-align:left;margin:10px 0;} "
        ".miss-ttl{font-size:10px;font-weight:700;color:#F5A623;"
        "letter-spacing:.9px;text-transform:uppercase;margin-bottom:8px;} "
        ".miss-item{display:flex;gap:8px;margin-bottom:8px;"
        "font-size:12px;color:#d0dde8;line-height:1.45;} "
        ".miss-lbl{font-weight:700;color:#f87171;white-space:nowrap;min-width:90px;} "
        ".rwd-banner{background:linear-gradient(135deg,#0f2a1a,#0a1e12);"
        "border:1.5px solid #6ee7b7;border-radius:10px;padding:12px 16px;margin:12px 0;} "
        ".rwd-ksh{font-size:1.55rem;font-weight:800;color:#6ee7b7;margin-bottom:3px;} "
        ".rwd-note{font-size:11.5px;color:#a0c8a0;} "
        ".cf input{width:100%;padding:9px 12px;margin:5px 0;"
        "background:#0f1d2b;border:1px solid #2a4060;border-radius:8px;"
        "color:#d0dde8;font-size:13px;outline:none;} "
        ".cf input:focus{border-color:#F5A623;} "
        ".cl-btn{width:100%;padding:11px;margin-top:8px;background:#6ee7b7;"
        "color:#0a2010;font-size:14px;font-weight:700;border:none;"
        "border-radius:10px;cursor:pointer;transition:opacity .2s;} "
        ".cl-btn:hover{opacity:.9;} "
        ".cl-btn:disabled{opacity:.5;cursor:not-allowed;} "
        ".code-box{background:#0f1d2b;border:2px solid #F5A623;border-radius:10px;"
        "padding:16px;margin:10px 0;} "
        ".code-lbl{font-size:11px;color:#a0b4c8;margin-bottom:4px;} "
        ".code-val{font-size:1.75rem;font-weight:800;color:#F5A623;"
        "letter-spacing:3px;font-family:monospace;} "
        ".code-hint{font-size:11.5px;color:#6ee7b7;margin-top:6px;} "
        ".parting{font-size:12px;color:#a0b4c8;font-style:italic;margin-top:12px;} "
        ".again-btn{width:100%;max-width:260px;padding:10px;"
        "background:#1a2e42;color:#d0dde8;border:1px solid #2a4060;"
        "border-radius:10px;font-size:14px;cursor:pointer;margin-top:12px;"
        "transition:all .2s;} "
        ".again-btn:hover{border-color:#F5A623;color:#F5A623;} "

        + kofi_anim_css +

        "</style></head><body>"
        f"{sprite}"   # permanent defs sprite — always resolvable

        # ══════════════════════════════ SVG STRINGS AS JS CONSTS ══════════════
        # Injected as JSON-encoded JS constants — never inside display:none.
        # url(#...) refs inside SVG need their <defs> to be in a rendered context;
        # hidden divs can suppress this, causing pattern/clipPath to render blank.
        "<script>"
        f"const _SVG_T={js_think};"
        f"const _SVG_C={js_right};"
        f"const _SVG_W={js_wrong};"
        "function kofiSVG(slot){"
        "  if(slot==='k-think')return _SVG_T;"
        "  if(slot==='k-right')return _SVG_C;"
        "  if(slot==='k-wrong')return _SVG_W;"
        "  return '';}"
        "</script>"

        # ══════════════════════════════ PHASE 1 — READY ═══════════════════
        "<div id='s-ready' class='scr on'>"
        "<div class='ready-wrap'>"
        "<div class='kofi-mid' id='rk'></div>"
        "<div class='kofi-speech'>This CV has 5 problems... can you find them all?</div>"
        "<h1 class='r-title'>Spot the CV Mistakes</h1>"
        "<p class='r-sub'>Tap every error before the 30 seconds run out.<br>Find 4 or 5 and win real credit!</p>"
        "<div class='rules'>"
        "<div class='rule'><span class='ri'>⏱️</span><span>You have <strong>30 seconds</strong></span></div>"
        "<div class='rule'><span class='ri'>👆</span><span>Tap anything that looks wrong on the CV</span></div>"
        "<div class='rule'><span class='ri'>💡</span><span>ATS red flags and recruiter pet-peeves both count</span></div>"
        "<div class='rule'><span class='ri'>🏆</span>"
        "<span>Find <strong>4 / 5</strong> → Ksh 50 &nbsp;·&nbsp; Find <strong>5 / 5</strong> → Ksh 100</span></div>"
        "</div>"
        "<button class='start-btn' onclick='startGame()'>🥁 Start — Let&rsquo;s go!</button>"
        "</div></div>"

        # ══════════════════════════════ PHASE 2 — GAME ════════════════════
        "<div id='s-game' class='scr'>"

        "<div class='timer-row'>"
        "<span id='tnum'>0:30</span>"
        "<div class='t-track'><div id='tfill' class='t-fill' style='width:100%'></div></div>"
        "<span id='sbadge' class='s-badge'>0 / 5</span>"
        "</div>"

        "<div class='g-top'>"
        "<div class='kofi-sm' id='gk'></div>"
        "<div class='instr'>Tap anything that would stop this CV passing an ATS system or a recruiter's first glance.</div>"
        "</div>"

        # ── THE CV ───────────────────────────────────────────────────────
        "<div class='cv-doc'>"

        # Header
        "<div class='cv-hd'>"
        "<div class='cv-photo ezp' id='e2' onclick='tap(event,\"e2\")'>Photo<br>📷</div>"
        "<div class='cv-name'>Alex Mutua</div>"
        "<div class='cv-ct'>"
        "<span class='ez' id='e1' onclick='tap(event,\"e1\")'>alex.mutua@gmal.com</span>"
        "<span class='cv-sep'>|</span><span>+254 712 345 678</span>"
        "<span class='cv-sep'>|</span><span>Nairobi, Kenya</span>"
        "<span class='cv-sep'>|</span><span>linkedin.com/in/alexmutua</span>"
        "</div></div>"

        # Objective
        "<div class='cv-sec'>"
        "<div class='cv-sh'>Objective</div>"
        "<div class='ezb' id='e3' onclick='tap(event,\"e3\")'>"
        "Looking for any job that suits my qualifications and where I can grow professionally."
        "</div></div>"

        # Education
        "<div class='cv-sec'>"
        "<div class='cv-sh'>Education</div>"
        "<div class='cv-jh'>"
        "<span class='cv-jt'>Bachelor of Business Administration</span>"
        "<span class='cv-jd'>Sep 2020 – May 2024</span>"
        "</div>"
        "<div class='cv-js'>United States International University – Africa (USIU-Africa)</div>"
        "<div class='cv-b'>GPA: 3.4 / 4.0 &nbsp;·&nbsp; Marketing Strategy, Consumer Behaviour, Digital Media</div>"
        "</div>"

        # Experience
        "<div class='cv-sec'>"
        "<div class='cv-sh'>Work Experience</div>"
        "<div style='margin-bottom:10px;'>"
        "<div class='cv-jh'>"
        "<span class='cv-jt'>Marketing Intern — Safaricom PLC</span>"
        "<span class='ez cv-jd' id='e4' onclick='tap(event,\"e4\")'>January 2023 – Present</span>"
        "</div>"
        "<div class='cv-js'>Nairobi &nbsp;·&nbsp; Digital Marketing Team</div>"
        "<div class='cv-b'>Managed company social media channels, growing total followers by 18% in Q3 2023.</div>"
        "<div class='cv-b ezb' id='e5' onclick='tap(event,\"e5\")'>"
        "Responsible for creating weekly performance reports and ensuring timely submission to line managers."
        "</div>"
        "<div class='cv-b'>Assisted in planning and executing the Safaricom Youth Summit digital campaign.</div>"
        "</div>"

        "<div>"
        "<div class='cv-jh'>"
        "<span class='cv-jt'>Sales Assistant — Naivas Supermarket</span>"
        "<span class='cv-jd'>01/2022 – 12/2022</span>"
        "</div>"
        "<div class='cv-js'>Westlands, Nairobi</div>"
        "<div class='cv-b'>Assisted customers with product queries and processed daily sales transactions.</div>"
        "<div class='cv-b'>Achieved top-5 staff rating for customer satisfaction three months consecutively.</div>"
        "</div></div>"

        # Skills
        "<div class='cv-sec'>"
        "<div class='cv-sh'>Skills &amp; Tools</div>"
        "<div>"
        "<span class='cv-pill'>Microsoft Office Suite</span>"
        "<span class='cv-pill'>Google Analytics</span>"
        "<span class='cv-pill'>Canva</span>"
        "<span class='cv-pill'>Social Media Marketing</span>"
        "<span class='cv-pill'>Hootsuite</span>"
        "<span class='cv-pill'>Basic HTML/CSS</span>"
        "</div></div>"

        # References
        "<div class='cv-sec' style='padding-bottom:14px;'>"
        "<div class='cv-sh'>References</div>"
        "<div style='font-size:12px;color:#4a4a4a;'>Available upon request.</div>"
        "</div></div>"  # end .cv-doc

        "</div>"  # end #s-game

        # ══════════════════════════════ PHASE 3 — RESULT ══════════════════
        "<div id='s-result' class='scr'>"
        "<div class='res-card'>"
        "<div class='kofi-big' id='reskf'></div>"
        "<div class='kofi-speech' id='res-speech'></div>"
        "<div style='display:flex;align-items:center;justify-content:center;"
        "gap:10px;margin:10px 0 2px;'>"
        "<div class='res-score' id='res-n'>0</div>"
        "<div style='font-size:1.1rem;color:#a0b4c8;font-weight:600;'>/ 5</div>"
        "</div>"
        "<div class='res-sub'>errors found</div>"
        "<div class='res-msg' id='res-msg'></div>"

        # Missed breakdown
        "<div class='miss-box' id='miss-box' style='display:none;'>"
        "<div class='miss-ttl'>What you missed</div>"
        "<div id='miss-list'></div>"
        "</div>"

        # Reward section (score ≥ 4)
        "<div id='rwd-sec' style='display:none;'>"
        "<div class='rwd-banner'>"
        "<div class='rwd-ksh' id='rwd-ksh'></div>"
        "<div class='rwd-note'>Enter your details below to claim your credit</div>"
        "</div>"
        "<div class='cf' id='cf-div'>"
        "<input type='text' id='pname' placeholder='Full name *' autocomplete='off'>"
        "<input type='text' id='pid'   placeholder='Student / Staff ID (optional)' autocomplete='off'>"
        "<button class='cl-btn' id='cl-btn' onclick='submitClaim()'>Claim Reward →</button>"
        "</div>"
        "<div id='cf-done' style='display:none;'>"
        "<div class='code-box'>"
        "<div class='code-lbl'>Your reward code</div>"
        "<div class='code-val' id='rcode'></div>"
        "<div class='code-hint'>Show this to booth staff to receive your credit 🎉</div>"
        "</div>"
        "</div></div>"  # end #rwd-sec

        "<div class='parting' id='parting'></div>"
        "<br>"
        "<button class='again-btn' onclick='resetGame()'>🔄 Play Again</button>"
        "</div></div>"  # end .res-card, #s-result

        # ══════════════════════════════ JAVASCRIPT ════════════════════════
        "<script>"
        f"const SB_URL='{supabase_url}',SB_KEY='{supabase_key}';"
        r"""
const ERRORS={
  e1:{label:'Email typo',
      exp:"'gmal.com' instead of 'gmail.com' — this email hard-bounces and the recruiter never hears from you."},
  e2:{label:'Photo on CV',
      exp:'Photos cause most modern ATS scanners to reject or misparse the CV. They also invite unconscious bias at the screening stage.'},
  e3:{label:'Weak objective',
      exp:"'Any job' signals zero research. Replace with a targeted sentence: \"Marketing graduate seeking to grow digital revenue at a consumer-facing brand.\""},
  e4:{label:'Inconsistent date format',
      exp:"One job says 'January 2023', the other says '01/2022'. Pick one format and apply it throughout — inconsistency reads as careless."},
  e5:{label:'Passive language',
      exp:"'Responsible for creating…' is weak. Lead with action verbs: 'Created and delivered weekly performance reports, enabling the team to track KPIs in real time.'"}
};

let found=new Set(),timeLeft=30,active=false,timerID=null,finalN=0;

function show(id){
  document.querySelectorAll('.scr').forEach(s=>s.classList.remove('on'));
  document.getElementById(id).classList.add('on');
}

function startGame(){
  found.clear();timeLeft=30;active=true;finalN=0;
  document.getElementById('tnum').textContent='0:30';
  document.getElementById('tnum').classList.remove('danger');
  document.getElementById('tfill').style.width='100%';
  document.getElementById('sbadge').textContent='0 / 5';
  Object.keys(ERRORS).forEach(id=>{
    const el=document.getElementById(id);
    if(el){el.classList.remove('found','missed');}
  });
  // Put thinking Kofi in game column
  document.getElementById('gk').innerHTML=kofiSVG('k-think');
  show('s-game');
  timerID=setInterval(tick,1000);
}

function tick(){
  timeLeft--;
  const s=timeLeft%60,m=Math.floor(timeLeft/60);
  document.getElementById('tnum').textContent=m+':'+(s<10?'0':'')+s;
  document.getElementById('tfill').style.width=(timeLeft/30*100)+'%';
  if(timeLeft<=8) document.getElementById('tnum').classList.add('danger');
  if(timeLeft<=0) endGame();
}

function tap(evt,id){
  if(!active||found.has(id))return;
  evt.stopPropagation();
  found.add(id);
  document.getElementById(id).classList.add('found');
  document.getElementById('sbadge').textContent=found.size+' / 5';
  if(found.size>=5)endGame();
}

function endGame(){
  if(!active)return;
  active=false;clearInterval(timerID);finalN=found.size;
  Object.keys(ERRORS).forEach(id=>{
    if(!found.has(id)){
      const el=document.getElementById(id);
      if(el)el.classList.add('missed');
    }
  });
  showResult();
}

function showResult(){
  const n=finalN;
  // Kofi state
  const rk=document.getElementById('reskf');
  let speech='';
  if(n>=4){rk.innerHTML=kofiSVG('k-right');speech='Ayeee! '+(n>=5?'Perfect score! The griot sees ALL! 🎵':'4 out of 5 — Kofi is impressed! 🥁');}
  else{rk.innerHTML=kofiSVG('k-wrong');speech=n>=3?'Good effort — a few slipped through though…':"Keep practising — these are common traps! 📋";}
  document.getElementById('res-speech').textContent=speech;
  document.getElementById('res-n').textContent=n;

  const msgs={5:'Perfect! You caught every error.',4:'Excellent! 4 of 5 found.',
               3:'Good eye! 3 found — reward is just one away.',
               2:'Just 2 this time — but now you know what to look for.',
               1:'Only 1 found — check out what you missed below.',
               0:'No errors found — but you will know them all now!'};
  document.getElementById('res-msg').textContent=msgs[n]||'';

  // Missed breakdown
  const missed=Object.entries(ERRORS).filter(([id])=>!found.has(id));
  if(missed.length&&n<5){
    document.getElementById('miss-box').style.display='block';
    document.getElementById('miss-list').innerHTML=missed.map(
      ([,e])=>`<div class="miss-item"><span class="miss-lbl">${e.label}:</span><span>${e.exp}</span></div>`
    ).join('');
  }

  // Reward
  if(n>=4){
    const ksh=n>=5?100:50;
    document.getElementById('rwd-sec').style.display='block';
    document.getElementById('rwd-ksh').textContent='Ksh '+ksh+' credit reward!';
    document.getElementById('cl-btn').textContent='Claim Ksh '+ksh+' →';
    document.getElementById('cl-btn').dataset.ksh=ksh;
  }

  // Parting remark
  const partings=[
    "Remember to audit your own CV against these same errors before your next application! 🎓",
    "A polished CV opens doors — go fix yours before the next opportunity. 📄",
    "Every USIU graduate should know these five traps before entering the job market. 💼"
  ];
  document.getElementById('parting').textContent=partings[n%3];

  show('s-result');
}

function genCode(ksh){
  const c='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let s='';for(let i=0;i<6;i++)s+=c[Math.floor(Math.random()*c.length)];
  return'USIU-'+(ksh>=100?'100K':'50K')+'-'+s;
}

async function submitClaim(){
  const name=document.getElementById('pname').value.trim();
  if(!name){
    document.getElementById('pname').style.borderColor='#f87171';
    document.getElementById('pname').placeholder='Name is required ✕';
    return;
  }
  const sid=document.getElementById('pid').value.trim();
  const ksh=parseInt(document.getElementById('cl-btn').dataset.ksh||'50');
  const code=genCode(ksh);
  const btn=document.getElementById('cl-btn');
  btn.textContent='Saving…';btn.disabled=true;
  if(SB_URL&&SB_KEY){
    try{
      await fetch(SB_URL+'/rest/v1/winners',{
        method:'POST',
        headers:{'Content-Type':'application/json',
                 'apikey':SB_KEY,'Authorization':'Bearer '+SB_KEY,
                 'Prefer':'return=minimal'},
        body:JSON.stringify({name,student_id:sid||null,game:'cv_errors',
                             score:finalN,time_left:timeLeft,
                             reward_ksh:ksh,reward_code:code,claimed:false})
      });
    }catch(e){console.warn('Supabase save failed:',e);}
  }
  document.getElementById('cf-div').style.display='none';
  document.getElementById('rcode').textContent=code;
  document.getElementById('cf-done').style.display='block';
}

function resetGame(){
  document.getElementById('miss-box').style.display='none';
  document.getElementById('miss-list').innerHTML='';
  document.getElementById('rwd-sec').style.display='none';
  document.getElementById('cf-div').style.display='block';
  document.getElementById('cf-done').style.display='none';
  document.getElementById('pname').value='';
  document.getElementById('pid').value='';
  document.getElementById('pname').style.borderColor='';
  document.getElementById('pname').placeholder='Full name *';
  document.getElementById('reskf').innerHTML='';
  show('s-ready');
}

// Init: put thinking Kofi on ready screen
document.getElementById('rk').innerHTML=kofiSVG('k-think');
"""
        "</script></body></html>"
    )

    return html
