#!/usr/bin/env python3
"""Builds slides/who-gets-to-submit/index.html (inline SVG visuals, one interactive slide).

Talk at the ISAC yearly seminar (Shenkar, Nov 2026): credit systems for submissions,
based on "Who Gets to Submit?" (Rosenfeld, Stone, Milojevic, Talmon).
Static charts are simulated here (fixed seed), with the paper's rules (junk/gate rules kept for reference):
  perfect-round bonus : T' = max(1, T - R + [all T used and R == 0])
  forgive noise       : credible iff R <= rho*m + 1, rho = 1/4 + eps/2
                        T' = max(1, T + [credible and m == T] - [not credible])
  + stricter bonus    : bonus only if R <= eps*m + 2*sqrt(m*eps*(1-eps)); dock as above
"""
import math
import os
import random

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'index.html')
OR, DK, GR, GL, CARD, PALE, LT = '#F7941D', '#26282C', '#5F6368', '#B9BCC1', '#FDFDFB', '#FCE8D2', '#F3F3F1'
GREEN, RED = '#3E9B4F', '#D64545'
FONT = 'font-family="Heebo, Arial, sans-serif"'
EPS = 0.2


# ---------- simulation ----------
def step(rule, T, k, f, eps, rng):
    """One round. k = good papers available (None = unlimited), f = junk share of a full slate."""
    m = T if k is None else min(T, k)
    if f > 0:
        m = T
    R = 0
    for _ in range(m):
        junk = rng.random() < f
        R += (rng.random() < 1 - eps) if junk else (rng.random() < eps)
    rho = 0.25 + eps / 2
    if rule == 'bonus':
        return max(1, T - R + (1 if (m == T and R == 0) else 0))
    cred = R <= rho * m + 1
    if rule == 'forgive':
        return max(1, T + (1 if (cred and m == T) else 0) - (0 if cred else 1))
    gate = R <= eps * m + 2 * math.sqrt(m * eps * (1 - eps))
    return max(1, T + (1 if (gate and m == T) else 0) - (0 if cred else 1))


def mean_path(rule, rounds, k=None, f=0.0, eps=EPS, T0=1, runs=300, seed=1):
    rng = random.Random(seed)
    acc = [0.0] * (rounds + 1)
    for _ in range(runs):
        T = T0
        acc[0] += T
        for t in range(1, rounds + 1):
            T = step(rule, T, k, f, eps, rng)
            acc[t] += T
    return [a / runs for a in acc]


# ---------- svg helpers ----------
def svg(w, h, body, style='', extra=''):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT} style="{style}" {extra}>{body}</svg>'


def text(x, y, s, size=30, fill=DK, anchor='middle', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{s}</text>'


def head(cx, cy, r, fill):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx-1.6*r} {cy+2.6*r} a{1.6*r} {1.6*r} 0 0 1 {3.2*r} 0 Z" fill="{fill}"/>')


def arrow(x1, y1, x2, y2, color=GR, w=6):
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 20 * math.cos(a), y2 - 20 * math.sin(a)
    p1 = (bx + 12 * math.sin(a), by - 12 * math.cos(a))
    p2 = (bx - 12 * math.sin(a), by + 12 * math.cos(a))
    return (f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')


def paper(x, y, s=1.0, fill=CARD, stroke=DK):
    """A sheet of paper, top-left at (x, y), 60x78 at s=1."""
    w, h, c = 60 * s, 78 * s, 16 * s
    o = (f'<path d="M{x} {y} h{w-c} l{c} {c} v{h-c} h{-w} Z" fill="{fill}" stroke="{stroke}" stroke-width="{3*s:.1f}" stroke-linejoin="round"/>'
         f'<path d="M{x+w-c} {y} v{c} h{c}" fill="none" stroke="{stroke}" stroke-width="{3*s:.1f}" stroke-linejoin="round"/>')
    for j in range(3):
        o += f'<line x1="{x+10*s}" y1="{y+(30+14*j)*s}" x2="{x+w-12*s}" y2="{y+(30+14*j)*s}" stroke="{stroke}" stroke-width="{2.5*s:.1f}" opacity=".5"/>'
    return o


def coin(cx, cy, r=22):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#E2B42B" stroke="#B08A1A" stroke-width="3"/>'
            + text(cx, cy + r * .38, '1', r * 1.05, DK, weight=800))


def check(cx, cy, r, color=GREEN):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<path d="M{cx-r*.45} {cy} l{r*.32} {r*.36} l{r*.62} {-r*.7}" fill="none" stroke="#fff" '
            f'stroke-width="{r/4:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r, color=RED):
    d = r * .38
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<path d="M{cx-d} {cy-d} L{cx+d} {cy+d} M{cx+d} {cy-d} L{cx-d} {cy+d}" stroke="#fff" stroke-width="{r/4:.1f}" stroke-linecap="round"/>')


def chart(W, H, series, xmax, ymax, xlab='round', ylab='credits', refs=(), yticks=None, xticks=None, legend=True):
    """Line chart. series = [(values, color, width, dash, label)], refs = [(y, label)]."""
    X0, X1, Y0, Y1 = 130, W - 30, H - 110, 60
    X = lambda t: X0 + t / xmax * (X1 - X0)
    Y = lambda v: Y0 - min(v, ymax) / ymax * (Y0 - Y1)
    o = f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{DK}" stroke-width="3"/>'
    o += f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-20}" stroke="{DK}" stroke-width="3"/>'
    for y, lab in refs:
        o += f'<line x1="{X0}" y1="{Y(y):.1f}" x2="{X1}" y2="{Y(y):.1f}" stroke="{GL}" stroke-width="3" stroke-dasharray="12 9"/>'
        o += text(X1, Y(y) + 38, lab, 28, GR, 'end', weight=700)
    for v in (yticks or [0, ymax]):
        o += text(X0 - 16, Y(v) + 10, str(v), 28, GR, 'end')
    for t in (xticks or [0, xmax]):
        o += text(X(t), Y0 + 40, str(t), 28, GR)
    o += text((X0 + X1) / 2, Y0 + 86, xlab, 32, DK, weight=700)
    o += text(46, (Y0 + Y1) / 2, ylab, 32, DK, weight=700, extra=f'transform="rotate(-90 46 {(Y0 + Y1) / 2})"')
    ly = Y1 - 10
    for vals, col, w, dash, lab in series:
        pts = ' '.join(f'{X(t):.1f},{Y(v):.1f}' for t, v in enumerate(vals) if t <= xmax)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d}/>'
        if legend and lab:
            o += f'<line x1="{X0+40}" y1="{ly}" x2="{X0+100}" y2="{ly}" stroke="{col}" stroke-width="{w}"{d}/>'
            o += text(X0 + 116, ly + 10, lab, 30, DK, 'start', weight=700)
            ly += 48
    return svg(W, H, o)


# ---------- data (verified; see notes in the session) ----------
# AAAI main-track papers reviewed (well-formed / valid), official counts only:
# 2015-2019 proceedings prefaces (ojs.aaai.org), 2021 chairs' report (arXiv 2202.12273, Phase-1 full papers),
# 2025 AAAI-26 pilot slides ("active submissions"), 2026 AI-review pilot paper (arXiv 2604.13940, full review).
# 2020 and 2022-2024 have no official count and are skipped.
AAAI_SERIES = [(2015, 1991), (2016, 2132), (2017, 2571), (2018, 3800), (2019, 7095),
               (2021, 7133), (2025, 11263), (2026, 22977)]
AAAI_NOTE = 'official counts only; some years missing'
# verified on official calls: IJCAI-ECAI 2026 (cap 8, USD 100 fee), AAAI-27 (cap 10),
# ERC 2027 reapplication rules, PVLDB vol. 19 (12-month resubmission wait),
# AAMAS 2027 / ICML 2026 / IJCAI 2027 reciprocal-reviewer rules
RATION_EX = ['IJCAI: 8 · AAAI: 10', 'ERC · PVLDB: 1 year', 'AAMAS · ICML · IJCAI', 'IJCAI: $100 a paper']


# ---------- visuals ----------
def aaai_vis():
    W, H = 820, 640
    if not AAAI_SERIES:
        return svg(W, H, '')
    y0, y1 = AAAI_SERIES[0][0], AAAI_SERIES[-1][0]
    top = max(v for _, v in AAAI_SERIES)
    ymax = 35000 if top > 30000 else 30000
    X0, X1, Y0, Y1 = 150, W - 40, H - 120, 90
    X = lambda y: X0 + (y - y0) / (y1 - y0) * (X1 - X0)
    Y = lambda v: Y0 - v / ymax * (Y0 - Y1)
    o = text(20, 40, 'AAAI papers reviewed per year', 36, DK, 'start', weight=800)
    o += f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{DK}" stroke-width="3"/>'
    o += f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-10}" stroke="{DK}" stroke-width="3"/>'
    for v in range(0, ymax + 1, 10000):
        o += text(X0 - 16, Y(v) + 10, f'{v//1000}k' if v else '0', 28, GR, 'end')
    for y in (2015, 2020, 2026):
        o += text(X(y), Y0 + 42, str(y), 28, GR)
    pts = ' '.join(f'{X(y):.1f},{Y(v):.1f}' for y, v in AAAI_SERIES)
    o += f'<polyline points="{pts}" fill="none" stroke="{OR}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>'
    for y, v in AAAI_SERIES:
        o += f'<circle cx="{X(y):.1f}" cy="{Y(v):.1f}" r="9" fill="{OR}"/>'
    (ya, va), (yb, vb) = AAAI_SERIES[0], AAAI_SERIES[-1]
    o += text(X(ya) + 6, Y(va) - 24, f'{va/1000:.0f}k', 32, DK, 'start', weight=800)
    o += text(X(yb) - 10, Y(vb) - 24, f'{vb/1000:.0f}k', 32, DK, 'end', weight=800)
    if AAAI_NOTE:
        o += text(X0, Y0 + 96, AAAI_NOTE, 24, GR, 'start')
    return svg(W, H, o)


def ration_vis():
    W, H = 1664, 520
    items = [('Caps', 'at most N papers'), ('Embargoes', 'rejected? wait'),
             ('Review to submit', 'submit, then review'), ('Fees', 'pay per paper')]
    o = ''
    for k, (name, sub) in enumerate(items):
        x = k * 424
        cx = x + 200
        o += f'<rect x="{x}" y="10" width="400" height="500" rx="22" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
        o += f'<rect x="{x}" y="10" width="400" height="10" rx="5" fill="{OR}"/>'
        if k == 0:
            for j in range(3):
                o += paper(cx - 95 + j * 60, 90, 1.1)
            o += f'<line x1="{cx-120}" y1="215" x2="{cx+120}" y2="215" stroke="{OR}" stroke-width="10" stroke-linecap="round"/>'
        elif k == 1:
            o += (f'<circle cx="{cx}" cy="155" r="80" fill="none" stroke="{DK}" stroke-width="8"/>'
                  f'<line x1="{cx}" y1="155" x2="{cx}" y2="105" stroke="{DK}" stroke-width="8" stroke-linecap="round"/>'
                  f'<line x1="{cx}" y1="155" x2="{cx+38}" y2="175" stroke="{OR}" stroke-width="8" stroke-linecap="round"/>')
        elif k == 2:
            o += paper(cx - 120, 105, 1.2) + arrow(cx - 30, 150, cx + 40, 150, OR, 7) + head(cx + 90, 120, 26, DK)
        else:
            o += (f'<circle cx="{cx}" cy="155" r="80" fill="{PALE}" stroke="{OR}" stroke-width="8"/>'
                  + text(cx, 190, '$', 100, DK, weight=800))
        o += text(cx, 330, name, 44, DK, weight=800)
        o += text(cx, 390, sub, 32, GR)
        if RATION_EX[k]:
            o += text(cx, 460, RATION_EX[k], 30, OR, weight=800)
    return svg(W, H, o)


def goal_vis():
    W, H = 640, 260
    o = ''
    for j in range(5):
        o += paper(30 + j * 70, 30, 0.95, '#E6F2E8', GREEN) + check(70 + j * 70, 120, 20)
    o += paper(450, 30, 0.95, '#EDEDEB', GR) + check(490, 120, 20)
    o += text(200, 210, 'many good', 32, GREEN, weight=800)
    o += text(480, 210, 'few bad', 32, GR, weight=800)
    return svg(W, H, o)


def setting_vis():
    W, H = 1664, 600
    G, B = ('#E6F2E8', GREEN), ('#EDEDEB', GR)
    o = head(110, 170, 52, DK) + text(110, 370, 'author', 34, GR, weight=700)
    for j, g in enumerate([G, G, B, G]):
        o += paper(230 + j * 46, 100 + (j % 2) * 10, 1.1, *g)
    o += text(335, 270, 'good or bad', 30, GR, weight=700)
    for j in range(3):
        o += coin(285 + j * 52, 330)
    o += text(337, 396, 'credits', 30, GR, weight=700)
    o += arrow(470, 180, 700, 180, OR, 7)
    o += text(585, 150, 'costs 1 credit', 30, DK, weight=700)
    o += text(585, 222, 'per paper', 30, DK, weight=700)
    o += (f'<rect x="720" y="100" width="300" height="170" rx="22" fill="{CARD}" stroke="{DK}" stroke-width="4"/>'
          + text(870, 175, 'venue', 44, DK, weight=800) + text(870, 228, 'reviews, noisily', 30, GR))
    o += arrow(1040, 185, 1120, 185, GR, 6)
    # accept / reject piles, each with one mistake
    rows = [(check, 95, [G, G, G, B]), (cross, 215, [B, B, B, G])]
    for icon, y, papers in rows:
        o += icon(1170, y + 32, 30)
        for j, g in enumerate(papers):
            o += paper(1230 + j * 62, y, 0.85, *g)
        o += (f'<rect x="{1230 + 3*62 - 10}" y="{y-10}" width="71" height="86" rx="10" fill="none" '
              f'stroke="{OR}" stroke-width="4" stroke-dasharray="8 6"/>')
    o += text(1610, 205, 'noise', 30, OR, 'end', weight=800)
    # policy: decisions -> next round's credits
    o += (f'<rect x="560" y="420" width="1080" height="150" rx="22" fill="{PALE}" stroke="{OR}" stroke-width="4"/>'
          + text(1100, 482, 'Policy (what we design):', 36, DK, weight=800)
          + text(1100, 532, 'this round’s accepts and rejects → each author’s credits next round', 30, DK))
    o += arrow(1370, 320, 1370, 412, OR, 7)
    o += (f'<polyline points="552,495 337,495 337,425" fill="none" stroke="{OR}" stroke-width="7" stroke-linejoin="round"/>'
          f'<polygon points="337,410 323,434 351,434" fill="{OR}"/>')
    return svg(W, H, o)


def perfect_bars_vis():
    W, H = 720, 560
    vals = [(1, .8), (5, .8 ** 5), (10, .8 ** 10), (20, .8 ** 20)]
    Y0, top = 430, 90
    o = text(20, 40, 'Chance that all are accepted', 34, DK, 'start', weight=800)
    for j, (m, p) in enumerate(vals):
        x = 70 + j * 160
        h = p * (Y0 - top)
        o += f'<rect x="{x}" y="{Y0-h:.1f}" width="110" height="{max(h, 3):.1f}" rx="10" fill="{GR}"/>'
        o += text(x + 55, Y0 - h - 14, f'{round(100*p)}%', 34, DK, weight=800)
        o += text(x + 55, Y0 + 42, str(m), 32, GR, weight=700)
    o += f'<line x1="50" y1="{Y0}" x2="700" y2="{Y0}" stroke="{DK}" stroke-width="3"/>'
    o += text(375, Y0 + 96, 'good papers submitted', 32, DK, weight=700)
    return svg(W, H, o)


def checklist_vis():
    W, H = 560, 420
    rows = ['More good papers,', 'more credits', 'Always at least one', 'Slow periods: almost free']
    o = check(30, 50, 26) + text(76, 62, rows[0], 36, DK, 'start', weight=700) + text(76, 108, rows[1], 36, DK, 'start', weight=700)
    o += check(30, 200, 26) + text(76, 212, rows[2], 36, DK, 'start', weight=700)
    o += check(30, 320, 26) + text(76, 332, 'Slow periods:', 36, DK, 'start', weight=700) + text(76, 378, 'almost free', 36, DK, 'start', weight=700)
    return svg(W, H, o)


# ---------- static charts ----------
NO_NOISE = mean_path('bonus', 15, k=8, eps=0.0, runs=1)
BONUS_K20 = mean_path('bonus', 60, k=20, runs=300, seed=2)
FORGIVE_K20 = mean_path('forgive', 60, k=20, runs=300, seed=3)

slides = []
S = slides.append

TITLE = '''
<section class="slide dark center">
  <p class="eyebrow">ISAC Yearly Seminar · Shenkar</p>
  <h1>Who Gets to Submit?</h1>
  <p class="big">Designing credit systems for peer review</p>
  <p class="ref" style="bottom:128px;font-size:32px">Nimrod Talmon · with Ariel Rosenfeld, Peter Stone and Staša Milojević</p>
  <p class="ref">Ben-Gurion University of the Negev · November 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>'''
S(TITLE)

S(f'''<section class="slide light">
  <h2>Writing got cheap; reviewing, much less</h2>
  <div class="cols">
    <div>{aaai_vis()}</div>
    <div class="rows ruled">
      <div class="row"><span class="n">1</span><p>AI helps: at AAAI-26, each paper got an AI review</p></div>
      <div class="row"><span class="n">2</span><p>Still, we want human gatekeepers</p></div>
      <div class="row"><span class="n">3</span><p>Overload makes reviews noisier</p></div>
    </div>
  </div>
</section>''')

for reveal in (False, True):
    S(f'''<section class="slide light">
  <h2>Venues already ration submissions</h2>
  <p class="sub" style="color:var(--orange);font-weight:700{'' if reveal else ';visibility:hidden'}">All of these are credit systems</p>
  <div style="margin-block:auto">{ration_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <h2>So let's design one properly</h2>
  <div class="cards">
    <div class="card top">
      <p class="label">The goal</p>
      <p>Accept as many good papers as possible, and as few bad ones</p>
      {goal_vis()}
    </div>
    <div class="card top">
      <p class="label">Fair to authors</p>
      <div class="rows ruled tight">
        <div class="row"><span class="n">1</span><p>More good papers, more credits</p></div>
        <div class="row"><span class="n">2</span><p>Always at least one credit</p></div>
        <div class="row"><span class="n">3</span><p>Slow periods are free</p></div>
      </div>
    </div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <h2>The simplest setting</h2>
  <p class="paper">Paper: “Who Gets to Submit?” · with Rosenfeld, Stone and Milojević · NeurIPS 2026 Workshop on AI-Native Academia</p>
  <p class="sub">One venue · one author per paper</p>
  <p class="sub">Each author can write some good papers per round, and any number of bad ones</p>
  <div style="margin-top:auto">{setting_vis()}</div>
</section>''')

for reveal in (False, True):
    hid = '' if reveal else ' style="visibility:hidden"'
    S(f'''<section class="slide light">
  <p class="eyebrow"{hid}>The perfect-round bonus</p>
  <h2>If we assume no noise, then a solution exists</h2>
  <p class="sub"{hid}>Each accepted paper returns its credit; if all are accepted, then +1 bonus</p>
  <div style="margin-block:auto{'' if reveal else ';visibility:hidden'}">{chart(1600, 560, [(NO_NOISE, OR, 8, '', '')], 15, 10,
      refs=[(8, 'can write: 8')], yticks=[0, 5, 10], xticks=[0, 5, 10, 15])}</div>
</section>''')

S(f'''<section class="slide light">
  <h2>But with noise, it breaks</h2>
  <p class="sub">Reviewers err, say, 1 time in 5: the more you send, the rarer a perfect round</p>
  <div class="cols">
    <div>{perfect_bars_vis()}</div>
    <div>{chart(860, 560, [(BONUS_K20, GR, 8, '', 'perfect-round bonus')], 60, 25,
        refs=[(20, 'can write: 20')], yticks=[0, 10, 20], xticks=[0, 30, 60])}</div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <h2>The fix: forgive what noise explains</h2>
  <p class="sub">Only rejections beyond what noise plausibly causes cost a credit</p>
  <div class="cols">
    <div style="flex:1.7">{chart(1040, 560, [(FORGIVE_K20, OR, 8, '', 'forgive noise'), (BONUS_K20, GR, 8, '', 'perfect-round bonus')], 60, 25,
        refs=[(20, 'can write: 20')], yticks=[0, 10, 20], xticks=[0, 30, 60])}</div>
    <div>{checklist_vis()}</div>
  </div>
</section>''')

S('''<section class="slide light">
  <h2>Where this goes</h2>
  <p class="sub">From one venue and one author per paper, toward the real system</p>
  <div class="cards three" style="margin-block:auto">
    <div class="card top"><p class="label">Data-based modeling</p><p>Fit authors, noise and load to real submission records</p></div>
    <div class="card top"><p class="label">Model relaxations</p><p>Several authors per paper, several venues, credits for reviewing</p></div>
    <div class="card top"><p class="label">More settings</p><p>Pull requests, bug bounties, app stores</p></div>
  </div>
</section>''')

S(TITLE)

STYLE = '''<style>
.paper { font-size: 30px; color: var(--gray); margin-top: -24px; }
.sub { font-size: 44px; margin-top: -16px; }
.paper + .sub { margin-top: -28px; }
.sub + .sub { margin-top: -36px; }
.card .label { font-size: 36px; }
.rows.tight .row { padding: 22px 0; }
.rows.tight .row .n { width: 60px; font-size: 52px; }
.card svg { width: 100%; height: auto; }
.cards.three .card { min-height: 380px; }
.cards.three .card .label { font-size: 44px; color: var(--dark); }
.cards.three .card p:not(.label) { font-size: 40px; }
</style>'''

html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Who Gets to Submit? · Nimrod Talmon</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@300..900&display=swap">
<link rel="stylesheet" href="../assets/deck.css">
''' + STYLE + '''
</head>
<body>
<div id="stage">
''' + '\n'.join(f'<!-- {k+1} -->{s}' for k, s in enumerate(slides)) + '''
</div>
<script src="../assets/deck.js"></script>
</body>
</html>
'''
open(OUT, 'w').write(html)
print(len(slides), 'slides')
