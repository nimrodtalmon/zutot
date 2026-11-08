#!/usr/bin/env python3
"""Builds slides/who-gets-to-submit/index.html (inline SVG visuals, one interactive slide).

Talk at the ISAC yearly seminar (Shenkar, Nov 2026): credit systems for submissions,
based on "Who Gets to Submit?" (Rosenfeld, Stone, Milojevic, Talmon).
Static charts are simulated here (fixed seed), with the paper's rules:
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


# ---------- visuals ----------
def squeeze_vis():
    W, H = 820, 640
    bars = [('NeurIPS', [('2020', 9467), ('2025', 21575)]), ('AAAI', [('2025', 15000), ('2026', 30000)])]
    labels = {9467: '9.5k', 21575: '21.6k', 15000: '~15k', 30000: '30k+'}
    Y0, top = 520, 80
    scale = (Y0 - top) / 30000
    o = text(20, 40, 'Submissions per year', 36, DK, 'start', weight=800)
    for g, (venue, pair) in enumerate(bars):
        gx = 90 + g * 380
        for j, (yr, v) in enumerate(pair):
            x = gx + j * 150
            h = v * scale
            o += f'<rect x="{x}" y="{Y0-h:.1f}" width="120" height="{h:.1f}" rx="10" fill="{GR if j == 0 else OR}"/>'
            o += text(x + 60, Y0 - h - 16, labels[v], 34, DK, weight=800)
            o += text(x + 60, Y0 + 42, yr, 30, GR)
        o += text(gx + 135, Y0 + 96, venue, 36, DK, weight=800)
    o += f'<line x1="60" y1="{Y0}" x2="800" y2="{Y0}" stroke="{DK}" stroke-width="3"/>'
    return svg(W, H, o)


def ration_vis():
    W, H = 1664, 470
    items = [('Caps', 'at most N papers'), ('Embargoes', 'rejected? wait'),
             ('Review to submit', 'submit, then review'), ('Fees', 'pay per paper')]
    o = ''
    for k, (name, sub) in enumerate(items):
        x = k * 424
        cx = x + 200
        o += f'<rect x="{x}" y="10" width="400" height="450" rx="22" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
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
    return svg(W, H, o)


def goal_vis():
    W, H = 640, 260
    o = ''
    for j in range(5):
        o += paper(30 + j * 70, 30, 0.95, '#E6F2E8', GREEN)
        o += check(70 + j * 70, 120, 20)
    o += paper(440, 30, 0.95, '#EDEDEB', GR) + cross(480, 120, 20)
    o += text(200, 210, 'many good', 32, GREEN, weight=800)
    o += text(470, 210, 'few weak', 32, GR, weight=800)
    return svg(W, H, o)


def setting_vis():
    W, H = 1664, 580
    o = head(150, 200, 52, DK)
    o += text(150, 400, 'author', 34, GR, weight=700)
    for j, good in enumerate([1, 1, 0, 1]):
        o += paper(290 + j * 46, 130 + (j % 2) * 10, 1.1, '#E6F2E8' if good else '#EDEDEB', GREEN if good else GR)
    o += text(390, 300, 'good or weak', 30, GR, weight=700)
    for j in range(3):
        o += coin(330 + j * 52, 360)
    o += text(380, 430, 'credits', 30, GR, weight=700)
    o += arrow(530, 200, 820, 200, OR, 7)
    o += text(675, 170, 'each paper: 1 credit', 30, DK, weight=700)
    o += (f'<rect x="840" y="110" width="330" height="180" rx="22" fill="{CARD}" stroke="{DK}" stroke-width="4"/>'
          + text(1005, 190, 'venue', 44, DK, weight=800) + text(1005, 245, 'reviews (noisily)', 30, GR))
    o += arrow(1190, 200, 1310, 200, GR, 6)
    o += check(1370, 160, 30) + cross(1370, 245, 30)
    o += text(1490, 172, 'accept', 30, DK, 'start', weight=700) + text(1490, 257, 'reject', 30, DK, 'start', weight=700)
    o += f'<path d="M1370 300 C1370 470, 380 470, 380 460" fill="none" stroke="{OR}" stroke-width="7" stroke-dasharray="14 10"/>'
    o += f'<polygon points="380,452 366,480 394,480" fill="{OR}"/>'
    o += text(875, 555, 'after each round, the venue refills credits based on the decisions', 32, DK, weight=700)
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


def agenda_vis():
    W, H = 1664, 300
    boxes = [('Data', 'real submission records'), ('Theory', 'which wishes fit together'), ('Simulation', 'a sandbox for venues')]
    o = ''
    for k, (name, sub) in enumerate(boxes):
        x = k * 572
        o += f'<rect x="{x}" y="20" width="500" height="230" rx="24" fill="{CARD}" stroke="{GL}" stroke-width="3"/>'
        o += text(x + 250, 120, name, 56, DK, weight=800) + text(x + 250, 185, sub, 32, GR)
        if k < 2:
            o += arrow(x + 512, 135, x + 562, 135, OR)
    return svg(W, H, o)


# ---------- static charts ----------
NO_NOISE = mean_path('bonus', 15, k=8, eps=0.0, runs=1)
BONUS_K20 = mean_path('bonus', 60, k=20, runs=300, seed=2)
FORGIVE_K20 = mean_path('forgive', 60, k=20, runs=300, seed=3)
HEAVY = mean_path('forgive', 60, f=0.4, T0=60, runs=300, seed=4)
LIGHT_F = mean_path('forgive', 500, f=0.2, runs=150, seed=5)
LIGHT_G = mean_path('gate', 500, f=0.2, runs=150, seed=6)

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
    <div>{squeeze_vis()}</div>
    <div class="rows ruled">
      <div class="row"><span class="n">1</span><p>AI reviews help: at AAAI-26, every paper got one</p></div>
      <div class="row"><span class="n">2</span><p>Still, we want human gatekeepers: judgment, taste</p></div>
      <div class="row"><span class="n">3</span><p>Overload makes reviews noisier</p></div>
    </div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <h2>Venues already ration submissions</h2>
  <p class="sub">Each of these is a crude credit system</p>
  <div style="margin-block:auto">{ration_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <h2>Let's design the credit system properly</h2>
  <div class="cards">
    <div class="card top">
      <p class="label">The goal</p>
      <p>Accept as many good papers as possible, and as few weak ones</p>
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
  <p class="sub">One venue · one author per paper · each paper is good or weak</p>
  <div style="margin-block:auto">{setting_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">The perfect-round bonus</p>
  <h2>If we assume no noise, then a solution exists</h2>
  <p class="sub">Each accepted paper returns its credit; if all are accepted, then +1 bonus</p>
  <div style="margin-block:auto">{chart(1600, 560, [(NO_NOISE, OR, 8, '', '')], 15, 10,
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
  <h2>Try it</h2>
  <p class="sub">One author, average of 200 runs</p>
  <div class="interactive knobs">
    <div class="kcol">
      <div class="klab">Reviewer error <b id="kev"></b> <span class="keys"><i>1</i>◀ ▶<i>2</i></span></div>
      <input type="range" id="ke" min="0" max="4" step="1" value="3">
      <div class="klab" style="margin-top:40px">Good papers per round <b id="kkv"></b> <span class="keys"><i>3</i>◀ ▶<i>4</i></span></div>
      <input type="range" id="kk" min="0" max="3" step="1" value="2">
      <div class="klegend"><span class="sw" style="background:#F7941D"></span>forgive noise</div>
      <div class="klegend"><span class="sw" style="background:#5F6368;height:5px"></span>perfect-round bonus</div>
    </div>
    <svg id="kplot" viewBox="0 0 900 560" width="900" height="560"></svg>
  </div>
</section>''')

S(f'''<section class="slide light">
  <h2>Heavy junk drains; light junk stops growing</h2>
  <p class="sub">For light junk: earning a bonus needs a stricter test than losing a credit</p>
  <div class="cols">
    <div>{chart(800, 560, [(HEAVY, OR, 8, '', 'forgive noise')], 60, 60, xlab='round · 40% junk',
        yticks=[0, 30, 60], xticks=[0, 30, 60])}</div>
    <div>{chart(800, 560, [(LIGHT_F, GR, 7, '14 10', 'forgive noise'), (LIGHT_G, OR, 8, '', '+ stricter bonus')], 500, 400,
        xlab='round · 20% junk', yticks=[0, 200, 400], xticks=[0, 250, 500])}</div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <h2>Where this goes</h2>
  <p class="sub">From one venue and one author per paper, toward the real system</p>
  <div style="margin-top:20px">{agenda_vis()}</div>
  <div class="chips" style="margin-top:40px">
    <span class="chip">co-authors share credits</span><span class="chip">many venues</span>
    <span class="chip">credits for reviewing</span><span class="chip on">beyond science: pull requests · app stores</span>
  </div>
</section>''')

S(TITLE)

STYLE = '''<style>
.paper { font-size: 30px; color: var(--gray); margin-top: -24px; }
.sub { font-size: 44px; margin-top: -16px; }
.paper + .sub { margin-top: -28px; }
.card .label { font-size: 36px; }
.rows.tight .row { padding: 22px 0; }
.rows.tight .row .n { width: 60px; font-size: 52px; }
.card svg { width: 100%; height: auto; }
.knobs { display: flex; gap: 72px; align-items: center; margin-block: auto; }
.kcol { display: flex; flex-direction: column; gap: 10px; width: 640px; }
.klab { font-size: 36px; font-weight: 700; display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.klab b { color: var(--orange); }
.keys { margin-left: auto; font-size: 26px; font-weight: 700; color: var(--gray); display: flex; align-items: center; gap: 6px; }
.keys i { font-style: normal; width: 40px; height: 40px; border-radius: 50%; border: 3px solid var(--gray-light);
  display: inline-flex; align-items: center; justify-content: center; font-size: 24px; color: var(--dark); }
.knobs input[type=range] { width: 640px; height: 36px; accent-color: var(--orange); cursor: pointer; }
.klegend { font-size: 32px; font-weight: 700; display: flex; align-items: center; gap: 16px; margin-top: 18px; }
.klegend + .klegend { margin-top: 0; }
.sw { width: 60px; height: 8px; border-radius: 4px; display: inline-block; }
</style>'''

SCRIPT = '''<script>
(function () {
  const ERR = [0, 0.05, 0.1, 0.2, 0.3], KS = [5, 10, 20, 30], ROUNDS = 60, RUNS = 200;
  const OR = '#F7941D', GR = '#5F6368', DK = '#26282C', GL = '#B9BCC1';
  let seed = 7;
  const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
  function path(rule, k, eps) {
    const acc = new Array(ROUNDS + 1).fill(0), rho = 0.25 + eps / 2;
    for (let r = 0; r < RUNS; r++) {
      let T = 1; acc[0] += T;
      for (let t = 1; t <= ROUNDS; t++) {
        const m = Math.min(T, k);
        let R = 0;
        for (let j = 0; j < m; j++) if (rnd() < eps) R++;
        if (rule === 'bonus') T = Math.max(1, T - R + ((m === T && R === 0) ? 1 : 0));
        else { const cred = R <= rho * m + 1; T = Math.max(1, T + ((cred && m === T) ? 1 : 0) - (cred ? 0 : 1)); }
        acc[t] += T;
      }
    }
    return acc.map(a => a / RUNS);
  }
  const ke = document.getElementById('ke'), kk = document.getElementById('kk'), plot = document.getElementById('kplot');
  const X0 = 130, X1 = 870, Y0 = 450, Y1 = 40, YMAX = 35;
  const X = t => X0 + t / ROUNDS * (X1 - X0), Y = v => Y0 - Math.min(v, YMAX) / YMAX * (Y0 - Y1);
  const T = (x, y, s, size, fill, anchor, weight, extra) =>
    `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor || 'middle'}" font-weight="${weight || 400}" font-family="Heebo, Arial, sans-serif" ${extra || ''}>${s}</text>`;
  function update() {
    const eps = ERR[+ke.value], k = KS[+kk.value];
    document.getElementById('kev').textContent = eps === 0 ? 'none' : `1 in ${Math.round(1 / eps)}`;
    document.getElementById('kkv').textContent = String(k);
    seed = 7;
    const a = path('forgive', k, eps), b = path('bonus', k, eps);
    let h = `<line x1="${X0}" y1="${Y0}" x2="${X1}" y2="${Y0}" stroke="${DK}" stroke-width="3"/>`;
    h += `<line x1="${X0}" y1="${Y0}" x2="${X0}" y2="${Y1 - 20}" stroke="${DK}" stroke-width="3"/>`;
    h += `<line x1="${X0}" y1="${Y(k)}" x2="${X1}" y2="${Y(k)}" stroke="${GL}" stroke-width="3" stroke-dasharray="12 9"/>`;
    h += T(X1, Y(k) + 38, 'can write: ' + k, 28, GR, 'end', 700);
    [0, 10, 20, 30].forEach(v => { h += T(X0 - 16, Y(v) + 10, v, 28, GR, 'end'); });
    [0, 30, 60].forEach(t => { h += T(X(t), Y0 + 40, t, 28, GR); });
    h += T((X0 + X1) / 2, Y0 + 86, 'round', 32, DK, 'middle', 700);
    h += T(46, (Y0 + Y1) / 2, 'credits', 32, DK, 'middle', 700, `transform="rotate(-90 46 ${(Y0 + Y1) / 2})"`);
    // orange first, gray (thinner) on top, so both stay visible when they coincide
    [[a, OR, 8], [b, GR, 5]].forEach(([p, c, w]) => {
      h += `<polyline points="${p.map((v, t) => X(t).toFixed(1) + ',' + Y(v).toFixed(1)).join(' ')}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"/>`;
    });
    plot.innerHTML = h;
  }
  ke.addEventListener('input', update); kk.addEventListener('input', update);
  [ke, kk].forEach(el => el.addEventListener('change', () => el.blur()));
  // keys 1/2 and 3/4 move the sliders (arrows stay for slides)
  const slide = ke.closest('.slide');
  document.addEventListener('keydown', (e) => {
    if (!slide.classList.contains('active') || e.metaKey || e.ctrlKey || e.altKey) return;
    const stepIt = (el, d) => { el.value = String(Math.max(+el.min, Math.min(+el.max, +el.value + d))); update(); };
    if (e.key === '1') stepIt(ke, -1); else if (e.key === '2') stepIt(ke, 1);
    else if (e.key === '3') stepIt(kk, -1); else if (e.key === '4') stepIt(kk, 1);
  });
  update();
})();
</script>'''

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
''' + SCRIPT + '''
</body>
</html>
'''
open(OUT, 'w').write(html)
print(len(slides), 'slides')
