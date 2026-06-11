"""
solvo_game.py — Solvo Global Trivia  (Career Fair partner game)

Pool of 12 questions about Solvo Global; 8 drawn at random each session.
Answer options are shuffled every game.
Scoring: 7/8 or 8/8 wins a Solvo water bottle.
Supabase: writes to the shared `winners` table (game='solvo').
"""

import json
from kofi import kofi_html as _kh

# ─────────────────────────────────────────────────────────────
# Question pool  (12 questions — 8 drawn at random each game)
# correct is always the first option; JS shuffles all four.
# ─────────────────────────────────────────────────────────────
QUESTIONS = [
    # ── About Solvo ───────────────────────────────────────────────────────────
    {"q": "What does Solvo do?",
     "options": [
         "Connects US companies with skilled remote professionals in Latin America",
         "Provides office furniture and equipment to businesses",
         "Designs websites and mobile apps for startups",
         "Offers financial loans to small businesses"],
     "correct": "Connects US companies with skilled remote professionals in Latin America"},

    {"q": "Who is the Founder and CEO of Solvo?",
     "options": ["George Newberry", "Michael Torres", "Carlos Mendez", "David Rodriguez"],
     "correct": "George Newberry"},

    # ── Staff recognition ─────────────────────────────────────────────────────
    # Correct answer is one of the real staff (Lilian / Purity / Nalliah / Munyuu).
    # Wrong options are phonetically similar but not real names.
    {"q": "Which of these is the name of one of the Solvo booth staff members?",
     "options": ["Purity", "Clarity", "Charity", "Sincerity"],
     "correct": "Purity"},

    {"q": "Which of these is the name of one of the Solvo booth staff members?",
     "options": ["Nalliah", "Naliah", "Nalika", "Naliwa"],
     "correct": "Nalliah"},

    {"q": "Which of these is the name of one of the Solvo booth staff members?",
     "options": ["Lilian", "Liliana", "Livia", "Linnea"],
     "correct": "Lilian"},

    {"q": "Which of these is the name of one of the Solvo booth staff members?",
     "options": ["Munyuu", "Munyua", "Munyuki", "Munyore"],
     "correct": "Munyuu"},

    # ── About Oasis Outsourcing (Solvo's Kenya partner) ───────────────────────
    {"q": "What does Oasis Outsourcing do?",
     "options": [
         "A BPO company providing data annotation, customer support, and outsourced HR services",
         "A Kenyan bank offering loans to small businesses",
         "A software company that builds mobile apps for startups",
         "A logistics company handling East African shipping"],
     "correct": "A BPO company providing data annotation, customer support, and outsourced HR services"},


    {"q": "When did the USIU-Africa Career Fair 2026 officially start?",
     "options": ["June 9th", "June 15th", "June 3rd", "June 20th"],
     "correct": "June 9th"},

    # ── Definition questions (Solvo's core work) ──────────────────────────────
    {"q": "What is recruitment?",
     "options": [
         "The process of finding, attracting, and hiring qualified candidates for job openings",
         "The process of training and upskilling existing employees",
         "The process of managing employee salaries and benefits",
         "The process of creating company HR policies"],
     "correct": "The process of finding, attracting, and hiring qualified candidates for job openings"},

    {"q": "What is outsourcing?",
     "options": [
         "Hiring external professionals or companies to handle specific business functions",
         "Moving an entire company's offices to another country",
         "Replacing all employees with automated systems",
         "Selling a division of your business to a competitor"],
     "correct": "Hiring external professionals or companies to handle specific business functions"},

    {"q": "What does a remote worker do?",
     "options": [
         "Works outside a traditional office, typically from home or another location",
         "Only works on weekends and public holidays",
         "Travels internationally for every project",
         "Works exclusively on a factory floor"],
     "correct": "Works outside a traditional office, typically from home or another location"},

    {"q": "What is nearshore staffing?",
     "options": [
         "Hiring talent from a nearby country to access skills at a lower cost",
         "Hiring only workers who live near the company's office",
         "Staffing a company's coastal or waterfront operations",
         "Hiring exclusively local, in-office workers"],
     "correct": "Hiring talent from a nearby country to access skills at a lower cost"},

    {"q": "What is talent acquisition?",
     "options": [
         "The strategic process of identifying, attracting, and onboarding skilled professionals",
         "Buying another company to gain its employees",
         "Developing internal training programmes for existing staff",
         "Automating repetitive tasks in a business"],
     "correct": "The strategic process of identifying, attracting, and onboarding skilled professionals"},

    {"q": "What is back office support?",
     "options": [
         "Administrative and operational tasks that keep a business running behind the scenes",
         "IT support for a company's website and apps",
         "Customer-facing sales and front desk services",
         "Security and facilities management for an office"],
     "correct": "Administrative and operational tasks that keep a business running behind the scenes"},
]


# ─────────────────────────────────────────────────────────────
# SVG helpers  (same pattern as trivia_game.py)
# ─────────────────────────────────────────────────────────────

def _extract(state):
    h = _kh(state)
    s = h.find("<svg"); e = h.rfind("</svg>") + 6
    return h[s:e]

def _rename(svg, suffix):
    return (svg
        .replace('class="kg"',              f'class="kg-{suffix}"')
        .replace('id="kpkm"',               f'id="kpkm-{suffix}"')
        .replace('url(#kpkm)',              f'url(#kpkm-{suffix})')
        .replace('id="krcm"',               f'id="krcm-{suffix}"')
        .replace('clip-path="url(#krcm)"',  f'clip-path="url(#krcm-{suffix})"')
    )

def _split_defs(svg):
    ds = svg.find("<defs>"); de = svg.find("</defs>") + 7
    if ds == -1: return "", svg
    return svg[ds:de], svg[:ds] + svg[de:]

def _kf():
    h = _kh("thinking")
    raw = h[h.find("<style>")+7:h.find("</style>")]
    parts = raw.split("@keyframes ")[1:]
    return "\n".join("@keyframes " + tok[:tok.find("}}")+2] for tok in parts)


# ─────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────

def solvo_game_html(supabase_url="", supabase_key=""):
    """Return a self-contained HTML string for the Solvo trivia game."""

    svg_think = _rename(_extract("thinking"), "svt")
    svg_right = _rename(_extract("correct"),  "svc")
    svg_wrong = _rename(_extract("wrong"),    "svw")

    defs_t, body_t = _split_defs(svg_think)
    defs_c, body_c = _split_defs(svg_right)
    defs_w, body_w = _split_defs(svg_wrong)

    sprite = (
        "<svg style='position:absolute;width:0;height:0;overflow:hidden;' aria-hidden='true'>"
        f"{defs_t}{defs_c}{defs_w}"
        "</svg>"
    )

    kf_css   = _kf()
    js_think = json.dumps(body_t)
    js_right = json.dumps(body_c)
    js_wrong = json.dumps(body_w)
    q_json   = json.dumps(QUESTIONS)

    kofi_css = kf_css + """
.kg-svt{animation:kft  3.8s  ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.kg-svc{animation:kfb  0.55s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.kg-svw{animation:kfs  3s    ease-in-out infinite;transform-box:fill-box;transform-origin:center;}
.kwv{animation:kwv 2.6s ease-in-out infinite;}
"""

    # ── Teal colour theme for Solvo ─────────────────────────────
    css = """
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:#0D1B2A;color:#d0dde8;
  font-family:'Segoe UI',Arial,sans-serif;font-size:14px;}
.scr{display:none;padding:14px 18px;}.scr.on{display:block;}
.wrap{max-width:500px;margin:0 auto;text-align:center;}
.kofi-md{max-width:230px;margin:0 auto;}
.kofi-sm{width:72px;flex-shrink:0;}
.sp{font-size:12px;font-style:italic;color:#00c8b8;padding:2px 12px 8px;min-height:28px;text-align:center;}
.r-title{font-size:1.45rem;font-weight:700;color:#fff;margin:0 0 4px;}
.r-sub{font-size:13px;color:#a0b4c8;margin:0 0 14px;line-height:1.5;}
.rules{background:#0d2235;border-radius:10px;padding:12px 16px;text-align:left;margin:10px 0 16px;}
.rule{display:flex;gap:10px;margin-bottom:7px;font-size:12.5px;color:#d0dde8;}
.ri{font-size:16px;min-width:22px;}
.start-btn{width:100%;max-width:280px;padding:14px;background:#009B8D;color:#fff;
  font-size:1.05rem;font-weight:700;border:none;border-radius:12px;cursor:pointer;
  box-shadow:0 4px 16px rgba(0,155,141,.4);transition:all .2s;}
.start-btn:hover{opacity:.9;transform:translateY(-1px);}
.q-hd{display:flex;align-items:center;gap:10px;margin-bottom:10px;}
.q-prog{font-size:12px;color:#a0b4c8;font-weight:500;white-space:nowrap;}
.score-cur{background:#0d2235;border:1px solid #2a4060;border-radius:16px;
  padding:3px 12px;font-size:12px;font-weight:600;color:#00c8b8;}
.q-text{font-size:1.05rem;font-weight:700;color:#fff;line-height:1.45;
  background:#0d2235;border-left:4px solid #009B8D;padding:12px 16px;
  border-radius:0 10px 10px 0;margin-bottom:12px;text-align:left;}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;}
.opt{padding:10px 14px;background:#0d2235;border:1.5px solid #2a4060;
  border-radius:10px;cursor:pointer;font-size:13px;color:#d0dde8;text-align:left;
  transition:all .15s;line-height:1.35;}
.opt:hover:not(.disabled){background:#1a3a4a;border-color:#00c8b8;color:#fff;}
.opt.correct{background:#0f2a1a;border-color:#6ee7b7;color:#6ee7b7;font-weight:600;}
.opt.wrong-sel{background:#2a0f0f;border-color:#f87171;color:#f87171;}
.opt.show-ans{background:#0f2a1a;border-color:#6ee7b7;color:#6ee7b7;}
.opt.disabled{cursor:default;opacity:.65;}
.fb-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:8px;
  font-size:13px;font-weight:600;margin-bottom:8px;}
.fb-ok{background:#0f2a1a;color:#6ee7b7;border:1px solid #2a5a3a;}
.fb-no{background:#2a0f0f;color:#f87171;border:1px solid #5a2a2a;}
.score-big{font-size:3.2rem;font-weight:800;color:#00c8b8;line-height:1;}
.score-lbl{font-size:13px;color:#a0b4c8;margin-bottom:10px;}
.score-msg{font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:10px;}
.miss-box{background:#0d1f2b;border-radius:10px;padding:12px;text-align:left;
  margin:10px 0;max-height:220px;overflow-y:auto;}
.miss-ttl{font-size:10px;font-weight:700;color:#00c8b8;letter-spacing:.9px;
  text-transform:uppercase;margin-bottom:8px;}
.miss-item{font-size:12px;color:#d0dde8;margin-bottom:6px;line-height:1.4;}
.miss-q{color:#a0b4c8;margin-bottom:2px;}
.miss-a{color:#6ee7b7;font-weight:600;}
.claim-btn{width:100%;max-width:260px;padding:14px;background:#009B8D;color:#fff;
  font-size:1.05rem;font-weight:700;border:none;border-radius:12px;cursor:pointer;
  transition:all .2s;box-shadow:0 4px 16px rgba(0,155,141,.4);}
.claim-btn:hover:not(:disabled){opacity:.9;transform:translateY(-1px);}
.rwd-banner{background:linear-gradient(135deg,#0a2535,#0d1f2b);
  border:1.5px solid #00c8b8;border-radius:10px;padding:12px 16px;margin:12px 0;}
.rwd-ksh{font-size:1.4rem;font-weight:800;color:#00c8b8;margin-bottom:3px;}
.rwd-note{font-size:11.5px;color:#80c8c0;}
.cf input{width:100%;padding:9px 12px;margin:5px 0;background:#0d1f2b;
  border:1px solid #2a4060;border-radius:8px;color:#d0dde8;font-size:13px;outline:none;}
.cf input:focus{border-color:#009B8D;}
.cl-btn{width:100%;padding:11px;margin-top:8px;background:#00c8b8;color:#0a2535;
  font-size:14px;font-weight:700;border:none;border-radius:10px;cursor:pointer;}
.cl-btn:disabled{opacity:.5;cursor:not-allowed;}
.code-box{background:#0d1f2b;border:2px solid #009B8D;border-radius:10px;
  padding:16px;margin:10px 0;}
.code-lbl{font-size:11px;color:#a0b4c8;margin-bottom:4px;}
.code-val{font-size:1.6rem;font-weight:800;color:#00c8b8;letter-spacing:3px;font-family:monospace;}
.code-hint{font-size:11.5px;color:#6ee7b7;margin-top:6px;}
.again-btn{width:100%;max-width:260px;padding:10px;background:#0d2235;color:#d0dde8;
  border:1px solid #2a4060;border-radius:10px;font-size:14px;cursor:pointer;
  margin-top:12px;transition:all .2s;}
.again-btn:hover{border-color:#009B8D;color:#00c8b8;}
.prize-card{background:#0d2235;border-radius:12px;padding:14px 20px;text-align:center;margin-top:8px;}
""" + kofi_css

    html = (
        "<!DOCTYPE html><html lang='en'><head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{css}</style></head><body>"
        f"{sprite}"

        # ── JS constants ─────────────────────────────────────────
        "<script>"
        f"const _ST={js_think},_SC={js_right},_SW={js_wrong};"
        "function kofiSVG(k){{return k==='t'?_ST:k==='c'?_SC:_SW;}}"
        f"const QPOOL={q_json};"
        f"const SB_URL='{supabase_url}',SB_KEY='{supabase_key}';"
        "</script>"

        # ══════════════════════ PHASE 1 — READY ══════════════════
        "<div id='s-ready' class='scr on'>"
        "<div class='wrap'>"
        "<div class='kofi-md' id='rk'></div>"
        "<div class='sp' id='rk-sp'>Think you know Solvo Global? Let&#8217;s find out&#8230;</div>"
        "<h1 class='r-title'>Solvo Trivia</h1>"
        "<p class='r-sub'>8 questions about Solvo Global.<br>"
        "Score 7 or 8 out of 8 and win a water bottle!</p>"
        "<div class='rules'>"
        "<div class='rule'><span class='ri'>❓</span><span><strong>8 questions</strong>, multiple choice</span></div>"
        "<div class='rule'><span class='ri'>✅</span><span>Get <strong>7/8 or 8/8</strong> to win a reward</span></div>"
        "<div class='rule'><span class='ri'>💧</span><span>Win a <strong>Solvo water bottle</strong> for your score!</span></div>"
        "</div>"
        "<button class='start-btn' onclick='startGame()'>💧 Start Trivia!</button>"
        "</div></div>"

        # ══════════════════════ PHASE 2 — QUESTION ═══════════════
        "<div id='s-q' class='scr'>"
        "<div class='q-hd'>"
        "<div class='kofi-sm' id='qk'></div>"
        "<div style='flex:1;'>"
        "<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;'>"
        "<span class='q-prog' id='qprog'>Question 1 of 8</span>"
        "<span class='score-cur' id='qscore'>0 correct</span>"
        "</div>"
        "<div style='background:#1a3040;border-radius:4px;height:5px;overflow:hidden;'>"
        "<div id='qbar' style='height:5px;background:linear-gradient(90deg,#009B8D,#00c8b8);"
        "border-radius:4px;transition:width .4s;width:0;'></div>"
        "</div>"
        "</div></div>"
        "<div class='sp' id='qk-sp'></div>"
        "<div class='q-text' id='q-text'></div>"
        "<div class='opts' id='q-opts'></div>"
        "<div id='q-fb' style='display:none;'></div>"
        "</div>"

        # ══════════════════════ PHASE 3 — SCORE ══════════════════
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

        # ══════════════════════ PHASE 4 — CLAIM ══════════════════
        "<div id='s-claim' class='scr'>"
        "<div class='wrap'>"
        "<div class='kofi-md' id='spk'></div>"
        "<div class='sp' id='spk-sp'>You&#8217;ve earned it! Claim your water bottle. &#128167;</div>"
        "<div class='prize-card'>"
        "<div style='font-size:2.5rem;margin-bottom:8px;'>&#128167;</div>"
        "<div style='font-size:1.3rem;font-weight:800;color:#00c8b8;margin-bottom:4px;'>Solvo Water Bottle!</div>"
        "<div class='sp'>Enter your details so booth staff can hand over your reward.</div>"
        "<div class='rwd-banner'>"
        "<div class='rwd-ksh'>&#128167; Solvo Water Bottle</div>"
        "<div class='rwd-note'>Enter your details below to claim</div>"
        "</div>"
        "<div class='cf' id='cf-div'>"
        "<input type='text' id='pname' placeholder='Full name *' autocomplete='off'>"
        "<input type='text' id='pid' placeholder='Student / Staff ID (optional)' autocomplete='off'>"
        "<button class='cl-btn' id='cl-btn' onclick='submitClaim()'>Claim Water Bottle &#8594;</button>"
        "</div>"
        "<div id='cf-done' style='display:none;'>"
        "<div class='code-box'>"
        "<div class='code-lbl'>Your reward code</div>"
        "<div class='code-val' id='rcode'></div>"
        "<div class='code-hint'>Show this to Solvo booth staff to collect your water bottle &#127881;</div>"
        "</div></div>"
        "</div>"
        "<button class='again-btn' id='sp-again' style='display:none;margin-top:10px;' onclick='resetGame()'>&#128260; Play Again</button>"
        "</div></div>"

        # ══════════════════════ JAVASCRIPT ═══════════════════════
        "<script>"
        r"""
let gQuestions=[], gIdx=0, gScore=0, gMissed=[], finalScore=0;

function show(id){document.querySelectorAll('.scr').forEach(s=>s.classList.remove('on'));document.getElementById(id).classList.add('on');}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}

function startGame(){
  const pool=shuffle([...QPOOL]).slice(0,8);
  gQuestions=pool.map(q=>{
    const opts=shuffle([...q.options]);
    return {...q,shuffled:opts,correctIdx:opts.indexOf(q.correct)};
  });
  gIdx=0;gScore=0;gMissed=[];
  document.getElementById('qk').innerHTML=kofiSVG('t');
  showQ();show('s-q');
}

function showQ(){
  const q=gQuestions[gIdx];
  document.getElementById('qprog').textContent=`Question ${gIdx+1} of 8`;
  document.getElementById('qscore').textContent=`${gScore} correct`;
  document.getElementById('qbar').style.width=(gIdx/8*100)+'%';
  document.getElementById('q-text').textContent=q.q;
  const L=['A','B','C','D'];
  document.getElementById('q-opts').innerHTML=q.shuffled.map((o,i)=>
    `<button class="opt" onclick="pick(${i})">${L[i]}) ${o}</button>`
  ).join('');
  document.getElementById('q-fb').style.display='none';
  document.getElementById('qk').innerHTML=kofiSVG('t');
  document.getElementById('qk-sp').textContent='';
}

function pick(i){
  const q=gQuestions[gIdx];
  const ok=i===q.correctIdx;
  if(ok)gScore++;else gMissed.push({q:q.q,ans:q.correct});
  document.querySelectorAll('.opt').forEach((el,idx)=>{
    el.classList.add('disabled');
    if(idx===q.correctIdx)el.classList.add('show-ans');
    else if(idx===i&&!ok)el.classList.add('wrong-sel');
  });
  const fb=document.getElementById('q-fb');
  fb.style.display='block';
  fb.className='fb-bar '+(ok?'fb-ok':'fb-no');
  fb.textContent=ok?'✓ Correct!':'✗ The correct answer was: '+q.correct;
  document.getElementById('qk').innerHTML=kofiSVG(ok?'c':'w');
  document.getElementById('qk-sp').textContent=ok?'Nailed it! 🎯':'Hmm, not quite. Keep going!';
  setTimeout(()=>{gIdx++;if(gIdx<8)showQ();else showScore();},1700);
}

function showScore(){
  finalScore=gScore;
  document.getElementById('sc-n').textContent=gScore;
  const sk=document.getElementById('sk');
  const sp=document.getElementById('sk-sp');
  const msg=document.getElementById('sc-msg');
  if(gScore>=7){
    sk.innerHTML=kofiSVG('c');
    sp.textContent=gScore===8?'PERFECT! Solvo is impressed! 🎉':'7 out of 8 — you know your stuff! 🎯';
    msg.textContent=gScore===8?'Flawless. You truly know Solvo!':'Excellent! You\'ve earned a water bottle!';
    document.getElementById('sc-btns').innerHTML=
      `<button class="claim-btn" onclick="goClaim()">💧 Claim Your Water Bottle!</button>`;
  } else {
    sk.innerHTML=kofiSVG('w');
    sp.textContent='Good effort — check what you missed and try again! 📚';
    const msgs={6:'So close! 6/8.',5:'5/8 — study those Solvo facts!',4:'4/8 — keep learning!'};
    msg.textContent=msgs[gScore]||`${gScore}/8 — keep studying!`;
    if(gMissed.length){
      document.getElementById('miss-box').style.display='block';
      document.getElementById('miss-list').innerHTML=gMissed.map(m=>
        `<div class="miss-item"><div class="miss-q">${m.q}</div><div class="miss-a">✓ ${m.ans}</div></div>`
      ).join('');
    }
    document.getElementById('sc-btns').innerHTML=
      `<button class="again-btn" onclick="resetGame()">🔄 Try Again</button>`;
  }
  show('s-score');
}

function goClaim(){
  document.getElementById('spk').innerHTML=kofiSVG('c');
  document.getElementById('spk-sp').textContent='You\'ve earned it! Claim your water bottle. 💧';
  document.getElementById('cf-div').style.display='block';
  document.getElementById('cf-done').style.display='none';
  document.getElementById('sp-again').style.display='none';
  document.getElementById('pname').value='';
  document.getElementById('pid').value='';
  document.getElementById('pname').style.borderColor='';
  show('s-claim');
}

function genCode(){
  const c='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let s='';for(let i=0;i<6;i++)s+=c[Math.floor(Math.random()*c.length)];
  return'SOLV-WBTL-'+s;
}

async function submitClaim(){
  const name=document.getElementById('pname').value.trim();
  if(!name){document.getElementById('pname').style.borderColor='#f87171';return;}
  const sid=document.getElementById('pid').value.trim();
  const code=genCode();
  const btn=document.getElementById('cl-btn');
  btn.textContent='Saving…';btn.disabled=true;
  if(SB_URL&&SB_KEY){
    try{
      await fetch(SB_URL+'/rest/v1/winners',{
        method:'POST',
        headers:{'Content-Type':'application/json',
                 'apikey':SB_KEY,'Authorization':'Bearer '+SB_KEY,
                 'Prefer':'return=minimal'},
        body:JSON.stringify({name,student_id:sid||null,game:'solvo',
                             score:finalScore,time_left:null,
                             reward_ksh:0,reward_code:code,
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
  document.getElementById('miss-box').style.display='none';
  document.getElementById('miss-list').innerHTML='';
  document.getElementById('rk').innerHTML=kofiSVG('t');
  show('s-ready');
}

document.getElementById('rk').innerHTML=kofiSVG('t');
"""
        "</script></body></html>"
    )
    return html
