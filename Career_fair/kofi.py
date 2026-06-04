"""
kofi.py — Kofi the Griot-Scholar, USIU Akinator mascot.

Usage:
    from kofi import kofi_html
    st.components.v1.html(kofi_html("thinking"), height=280, scrolling=False)

States: idle | thinking | confident | correct | wrong
"""


def _eyes(state):
    if state in ("idle", "thinking"):
        if state == "thinking":
            p1, p2 = "cx='313' cy='122'", "cx='361' cy='122'"
            rb = "Q364 101 373 107", "3"
        else:
            p1, p2 = "cx='316' cy='120'", "cx='364' cy='120'"
            rb = "Q364 104 373 109", "2.5"
        return f"""
        <circle cx="316" cy="120" r="9" fill="white"/>
        <circle cx="364" cy="120" r="9" fill="white"/>
        <circle {p1} r="5.5" fill="#1a1a1a"/>
        <circle {p2} r="5.5" fill="#1a1a1a"/>
        <circle cx="315" cy="118" r="1.8" fill="white"/>
        <circle cx="363" cy="118" r="1.8" fill="white"/>
        <path d="M307 109 Q316 104 325 109" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M355 107 {rb[0]}" fill="none" stroke="#1a1a1a" stroke-width="{rb[1]}" stroke-linecap="round"/>"""
    if state == "confident":
        return """
        <circle cx="316" cy="116" r="10" fill="white"/>
        <circle cx="364" cy="116" r="10" fill="white"/>
        <circle cx="317" cy="116" r="6.5" fill="#1a1a1a"/>
        <circle cx="365" cy="116" r="6.5" fill="#1a1a1a"/>
        <circle cx="319" cy="114" r="2" fill="white"/>
        <circle cx="367" cy="114" r="2" fill="white"/>
        <path d="M307 105 Q316 100 325 105" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M355 105 Q364 100 373 105" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round"/>"""
    if state == "correct":
        return """
        <path d="M305 122 Q316 112 327 122" fill="#1a1a1a"/>
        <path d="M353 122 Q364 112 375 122" fill="#1a1a1a"/>
        <path d="M304 110 Q316 104 328 110" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round"/>
        <path d="M352 110 Q364 104 376 110" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round"/>"""
    return """
        <circle cx="316" cy="118" r="10" fill="white"/>
        <circle cx="364" cy="118" r="10" fill="white"/>
        <circle cx="316" cy="119" r="6" fill="#1a1a1a"/>
        <circle cx="364" cy="119" r="6" fill="#1a1a1a"/>
        <circle cx="318" cy="117" r="2" fill="white"/>
        <circle cx="366" cy="117" r="2" fill="white"/>
        <path d="M306 104 Q316 98 326 104" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round"/>
        <path d="M354 104 Q364 98 374 104" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round"/>"""


def _mouth(state):
    if state == "idle":
        return """<path d="M326 162 Q340 170 354 162" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round"/>"""
    if state == "thinking":
        return """<path d="M328 158 Q340 164 352 158" fill="none" stroke="#1a1a1a" stroke-width="2" stroke-linecap="round"/>"""
    if state == "confident":
        return """
        <path d="M320 156 Q340 172 360 156" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round"/>
        <ellipse cx="340" cy="162" rx="16" ry="8" fill="white"/>"""
    if state == "correct":
        return """
        <path d="M308 154 Q340 184 372 154" fill="#1a1a1a"/>
        <ellipse cx="340" cy="164" rx="28" ry="15" fill="white"/>
        <path d="M308 154 Q340 184 372 154" fill="none" stroke="#1a1a1a" stroke-width="2.5"/>"""
    return """
        <path d="M322 158 Q340 172 358 158" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round"/>
        <ellipse cx="340" cy="163" rx="14" ry="6.5" fill="white"/>"""


def _rarm(state):
    if state in ("idle", "thinking"):
        return """
        <path d="M408 216 Q424 240 428 268" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <ellipse cx="430" cy="276" rx="17" ry="12" fill="#7A4F2E"/>
        <ellipse cx="430" cy="266" rx="14" ry="18" fill="#7A4F2E"/>"""
    if state == "confident":
        return """
        <path d="M410 212 Q434 232 450 248" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <path d="M448 246 Q466 256 480 264" fill="none" stroke="#7A4F2E" stroke-width="13" stroke-linecap="round"/>
        <ellipse cx="484" cy="270" rx="15" ry="10" fill="#7A4F2E"/>"""
    if state == "correct":
        return """
        <path d="M414 208 Q440 186 452 160" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <ellipse cx="454" cy="150" rx="13" ry="18" fill="#7A4F2E"/>"""
    return """
        <path d="M414 216 Q440 205 452 220" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <path d="M450 218 Q458 202 450 186" fill="none" stroke="#7A4F2E" stroke-width="13" stroke-linecap="round"/>
        <ellipse cx="448" cy="180" rx="12" ry="16" fill="#7A4F2E"/>"""


def _larm_drum_fx(state):
    drum_think = """
        <path d="M272 216 Q250 248 238 280" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <ellipse cx="236" cy="288" rx="17" ry="12" fill="#7A4F2E"/>
        <ellipse cx="214" cy="278" rx="26" ry="10" fill="#5a3018"/>
        <ellipse cx="214" cy="276" rx="22" ry="8" fill="#c8a070"/>
        <path d="M188 278 Q195 296 202 310 L226 310 Q233 296 240 278Z" fill="#6B3F24"/>
        <rect x="202" y="310" width="24" height="14" rx="4" fill="#5a3018"/>
        <path d="M202 324 Q195 338 188 354 L240 354 Q233 338 226 324Z" fill="#6B3F24"/>
        <ellipse cx="214" cy="354" rx="26" ry="10" fill="#5a3018"/>
        <ellipse cx="214" cy="356" rx="22" ry="8" fill="#a07840"/>
        <line x1="194" y1="278" x2="205" y2="324" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <line x1="214" y1="288" x2="214" y2="324" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <line x1="234" y1="278" x2="223" y2="324" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>"""
    if state == "idle":
        return drum_think + """<ellipse cx="214" cy="276" rx="30" ry="13" fill="#F5A623" opacity="0.14"/>"""
    if state == "thinking":
        return drum_think + """
        <ellipse cx="214" cy="276" rx="32" ry="14" fill="#F5A623" opacity="0.18"/>
        <g class="kwv">
            <path d="M200 266 Q214 258 228 266" fill="none" stroke="#F5A623" stroke-width="1.8" opacity="0.55"/>
            <path d="M196 256 Q214 246 232 256" fill="none" stroke="#F5A623" stroke-width="1.5" opacity="0.38"/>
            <path d="M194 246 Q214 235 234 246" fill="none" stroke="#F5A623" stroke-width="1.2" opacity="0.22"/>
            <circle cx="214" cy="238" r="3" fill="#F5A623" opacity="0.35"/>
        </g>"""
    if state == "confident":
        return """
        <path d="M270 212 Q248 242 236 266" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <ellipse cx="234" cy="274" rx="17" ry="12" fill="#7A4F2E"/>
        <ellipse cx="212" cy="260" rx="26" ry="10" fill="#5a3018"/>
        <ellipse cx="212" cy="258" rx="22" ry="8" fill="#c8a070"/>
        <path d="M186 260 Q193 278 200 292 L224 292 Q231 278 238 260Z" fill="#6B3F24"/>
        <rect x="200" y="292" width="24" height="14" rx="4" fill="#5a3018"/>
        <path d="M200 306 Q193 320 186 336 L238 336 Q231 320 224 306Z" fill="#6B3F24"/>
        <ellipse cx="212" cy="336" rx="26" ry="10" fill="#5a3018"/>
        <ellipse cx="212" cy="338" rx="22" ry="8" fill="#a07840"/>
        <line x1="192" y1="260" x2="203" y2="306" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <line x1="212" y1="270" x2="212" y2="306" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <line x1="232" y1="260" x2="221" y2="306" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <ellipse cx="212" cy="258" rx="40" ry="19" fill="#F5A623" opacity="0.28"/>
        <ellipse cx="212" cy="258" rx="28" ry="13" fill="#F5A623" opacity="0.2"/>
        <text x="484" y="115" font-size="30" fill="#F5A623" opacity="0.85" font-family="sans-serif">!</text>
        <circle cx="468" cy="88" r="5" fill="#F5A623" opacity="0.55"/>
        <circle cx="488" cy="76" r="3.5" fill="#F5A623" opacity="0.38"/>"""
    if state == "correct":
        return """
        <path d="M266 208 Q238 184 224 156" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <ellipse cx="222" cy="146" rx="13" ry="18" fill="#7A4F2E"/>
        <ellipse cx="204" cy="138" rx="26" ry="10" fill="#5a3018"/>
        <ellipse cx="204" cy="136" rx="22" ry="8" fill="#c8a070"/>
        <path d="M178 138 Q185 152 192 162 L216 162 Q223 152 230 138Z" fill="#6B3F24"/>
        <rect x="192" y="162" width="24" height="10" rx="3" fill="#5a3018"/>
        <path d="M192 172 Q185 182 178 194 L230 194 Q223 182 216 172Z" fill="#6B3F24"/>
        <ellipse cx="204" cy="194" rx="26" ry="10" fill="#5a3018"/>
        <ellipse cx="204" cy="196" rx="22" ry="8" fill="#a07840"/>
        <line x1="184" y1="138" x2="195" y2="172" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <line x1="204" y1="148" x2="204" y2="172" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <line x1="224" y1="138" x2="213" y2="172" stroke="#c8a070" stroke-width="1.8" opacity="0.6"/>
        <circle cx="204" cy="136" r="62" fill="#F5A623" opacity="0.12"/>
        <circle cx="204" cy="136" r="44" fill="#F5A623" opacity="0.26"/>
        <circle cx="204" cy="136" r="28" fill="#F5A623" opacity="0.52"/>
        <circle cx="196" cy="128" r="9"  fill="white"   opacity="0.35"/>
        <circle cx="204" cy="136" r="76" fill="none" stroke="#F5A623" stroke-width="2.5" opacity="0.32"/>
        <circle cx="204" cy="136" r="92" fill="none" stroke="#F5A623" stroke-width="2"   opacity="0.18"/>
        <text x="464" y="172" font-size="26" fill="#F5A623" font-family="sans-serif">&#9834;</text>
        <text x="492" y="228" font-size="20" fill="#6ee7b7" font-family="sans-serif">&#9835;</text>
        <text x="512" y="162" font-size="18" fill="#F5A623" font-family="sans-serif">&#9733;</text>
        <text x="484" y="122" font-size="16" fill="#ffdd66" font-family="sans-serif">&#9733;</text>
        <circle cx="470" cy="107" r="5" fill="#F5A623" opacity="0.7"/>"""
    # wrong
    return """
        <path d="M266 216 Q240 205 228 220" fill="none" stroke="#7A4F2E" stroke-width="15" stroke-linecap="round"/>
        <path d="M230 218 Q222 202 230 186" fill="none" stroke="#7A4F2E" stroke-width="13" stroke-linecap="round"/>
        <ellipse cx="232" cy="180" rx="12" ry="16" fill="#7A4F2E"/>
        <ellipse cx="210" cy="338" rx="26" ry="10" fill="#3a2010" opacity="0.65"/>
        <ellipse cx="210" cy="336" rx="22" ry="8" fill="#7a5030" opacity="0.6"/>
        <path d="M184 338 Q191 352 198 364 L222 364 Q229 352 236 338Z" fill="#4a2a10" opacity="0.6"/>
        <rect x="198" y="364" width="24" height="12" rx="3" fill="#3a2010" opacity="0.65"/>
        <path d="M198 376 Q191 388 184 400 L236 400 Q229 388 222 376Z" fill="#4a2a10" opacity="0.6"/>
        <ellipse cx="210" cy="400" rx="26" ry="10" fill="#3a2010" opacity="0.65"/>
        <line x1="190" y1="338" x2="201" y2="376" stroke="#7a5030" stroke-width="1.5" opacity="0.3"/>
        <line x1="210" y1="346" x2="210" y2="376" stroke="#7a5030" stroke-width="1.5" opacity="0.3"/>
        <line x1="230" y1="338" x2="219" y2="376" stroke="#7a5030" stroke-width="1.5" opacity="0.3"/>
        <ellipse cx="394" cy="104" rx="6" ry="9" fill="#88aacc" opacity="0.72"/>
        <circle  cx="394" cy="96"  r="5.5"        fill="#88aacc" opacity="0.72"/>
        <text x="428" y="142" font-size="15" fill="#f87171" opacity="0.6" font-family="sans-serif">?!</text>"""


# ─────────────────────────────────────────────────────────────
SPEECH = {
    "idle":      "Think of your USIU programme&#8230; &#x1F941;",
    "thinking":  "The drum is speaking&#8230; let me feel it&#8230;",
    "confident": "I can feel it in the rhythm! &#x1F525;",
    "correct":   "Ayeee! The griot always knows! &#x1F3B5;",
    "wrong":     "Hmm&#8230; the drum had a different story!",
}

_ANIM = {
    "idle":      ("kff", "4s"),
    "thinking":  ("kft", "3.8s"),
    "confident": ("kff", "2.5s"),
    "correct":   ("kfb", "0.55s"),
    "wrong":     ("kfs", "3s"),
}

_SHARED = """
    <circle cx="340" cy="265" r="175" fill="#0D1A0A" opacity="0.88"/>
    <circle cx="340" cy="265" r="171" fill="none" stroke="#F5A623" stroke-width="0.8" opacity="0.22"/>
    <path d="M268 204 Q248 198 228 202 L185 412 L495 412 L452 202 Q432 198 412 204 Q380 212 340 218 Q300 212 268 204Z" fill="#B31B1B"/>
    <rect x="185" y="202" width="310" height="210" fill="url(#kpkm)" clip-path="url(#krcm)"/>
    <path d="M228 202 L185 412" fill="none" stroke="#F5A623" stroke-width="2" opacity="0.5"/>
    <path d="M452 202 L495 412" fill="none" stroke="#F5A623" stroke-width="2" opacity="0.5"/>
    <path d="M185 412 L495 412" fill="none" stroke="#F5A623" stroke-width="2.5" opacity="0.6"/>
    <path d="M290 204 Q315 198 340 202 Q365 198 390 204" fill="none" stroke="#F5A623" stroke-width="5" stroke-linecap="round"/>
    <circle cx="302" cy="204" r="4"   fill="#F5A623"/>
    <circle cx="320" cy="200" r="4.5" fill="#F5A623"/>
    <circle cx="340" cy="199" r="5.5" fill="#F5A623"/>
    <circle cx="360" cy="200" r="4.5" fill="#F5A623"/>
    <circle cx="378" cy="204" r="4"   fill="#F5A623"/>
    <rect x="322" y="178" width="36" height="26" rx="4" fill="#7A4F2E"/>
    <circle cx="340" cy="122" r="57" fill="#7A4F2E"/>
    <ellipse cx="284" cy="128" rx="11" ry="14" fill="#6B3F24"/>
    <ellipse cx="396" cy="128" rx="11" ry="14" fill="#6B3F24"/>
    <ellipse cx="284" cy="128" rx="6"  ry="9"  fill="#5a3018"/>
    <ellipse cx="396" cy="128" rx="6"  ry="9"  fill="#5a3018"/>
    <ellipse cx="340" cy="68" rx="58" ry="18" fill="#B31B1B"/>
    <path d="M284 68 Q286 53 296 40 Q340 30 384 40 Q394 53 396 68Z" fill="#B31B1B"/>
    <path d="M288 66 Q292 51 304 39 Q340 28 376 39 Q388 51 392 66Z" fill="#2D6A4F"/>
    <path d="M294 60 Q300 46 312 36 Q340 26 368 36 Q380 46 386 60Z" fill="#F5A623"/>
    <path d="M302 52 Q310 40 322 32 Q340 24 358 32 Q370 40 378 52Z" fill="#1a1a1a"/>
    <path d="M314 41 Q322 30 340 24 Q358 30 366 41Z"                 fill="#B31B1B"/>
    <circle cx="340" cy="23" r="9" fill="#F5A623"/>
    <circle cx="340" cy="23" r="5" fill="#B31B1B"/>
    <ellipse cx="340" cy="142" rx="7"  ry="5.5" fill="#6B3F24"/>
    <ellipse cx="310" cy="152" rx="13" ry="7"   fill="#9B4020" opacity="0.3"/>
    <ellipse cx="370" cy="152" rx="13" ry="7"   fill="#9B4020" opacity="0.3"/>"""


def kofi_html(state: str = "thinking") -> str:
    """Return self-contained HTML with Kofi in the given animation state."""
    state = state if state in _ANIM else "thinking"
    an, ad = _ANIM[state]
    speech = SPEECH.get(state, "")
    css = (
        f"body{{margin:0;padding:0;background:transparent;overflow:hidden;"
        f"font-family:'Segoe UI',Arial,sans-serif;}}"
        f"@keyframes kff{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}"
        f"@keyframes kft{{0%,100%{{transform:rotate(0)}}30%{{transform:rotate(-2deg)}}70%{{transform:rotate(1.5deg)}}}}"
        f"@keyframes kfb{{0%,100%{{transform:translateY(0)}}20%{{transform:translateY(-20px)}}"
        f"50%{{transform:translateY(-8px)}}75%{{transform:translateY(-16px)}}}}"
        f"@keyframes kfs{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(4px)}}}}"
        f"@keyframes kwv{{0%,100%{{transform:translateY(0);opacity:.5}}50%{{transform:translateY(-10px);opacity:.9}}}}"
        f".kg{{animation:{an} {ad} ease-in-out infinite;}}"
        f".kwv{{animation:kwv 2.6s ease-in-out infinite;}}"
    )
    body = f"{_SHARED}{_eyes(state)}{_mouth(state)}{_rarm(state)}{_larm_drum_fx(state)}"
    sdiv = (f'<div style="text-align:center;color:#c8a060;font-size:12px;'
            f'font-style:italic;padding:2px 12px 0;">{speech}</div>') if speech else ""
    return (
        f'<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<style>{css}</style></head><body>'
        f'<svg width="100%" viewBox="148 10 360 415" xmlns="http://www.w3.org/2000/svg">'
        f'<defs>'
        f'<pattern id="kpkm" x="0" y="0" width="20" height="28" patternUnits="userSpaceOnUse">'
        f'<rect width="20" height="28" fill="#B31B1B"/>'
        f'<rect x="0" y="0" width="20" height="6" fill="#F5A623"/>'
        f'<rect x="0" y="13" width="20" height="6" fill="#2D6A4F"/>'
        f'<rect x="0" y="6" width="6" height="7" fill="#1a1a1a"/>'
        f'<rect x="14" y="6" width="6" height="7" fill="#1a1a1a"/>'
        f'</pattern>'
        f'<clipPath id="krcm">'
        f'<path d="M268 204 Q248 198 228 202 L185 412 L495 412 L452 202 '
        f'Q432 198 412 204 Q380 212 340 218 Q300 212 268 204Z"/>'
        f'</clipPath></defs>'
        f'<g class="kg">{body}</g>'
        f'</svg>{sdiv}</body></html>'
    )
