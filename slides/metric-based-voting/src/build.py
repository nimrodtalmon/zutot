#!/usr/bin/env python3
"""Builds slides/metric-based-voting/index.html (inline SVG visuals)."""
import statistics as st

import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'index.html')
OR, DK, GR, GL, CARD, PALE, LT = '#F7941D', '#26282C', '#5F6368', '#B9BCC1', '#FDFDFB', '#FCE8D2', '#F3F3F1'
FONT = 'font-family="Heebo, Arial, sans-serif"'

# ---------- running example ----------
METRICS = ['Users', 'Fees', 'Open source']
PROJECTS = ['Wallet', 'Bridge', 'DEX']
VAL = [[.9, .3, .6], [.4, .9, .2], [.6, .6, .9]]
BALLOTS = [[.6, .2, .2], [.2, .6, .2], [.3, .2, .5]]
MCOL = [OR, '#FBC17A', GL]


def svg(w, h, body, style=''):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT} style="{style}">{body}</svg>'


def text(x, y, s, size=30, fill=DK, anchor='middle', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def head(cx, cy, r, fill):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx-1.6*r} {cy+2.6*r} a{1.6*r} {1.6*r} 0 0 1 {3.2*r} 0 Z" fill="{fill}"/>')


def arrow(x1, y, x2, color=OR):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2-14}" y2="{y}" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M{x2} {y} l-22 -13 v26 z" fill="{color}"/>')


def bars(x, y, vals, w=34, gap=10, h=150, cols=MCOL, frame=True, ghost=None):
    out = ''
    for k, v in enumerate(vals):
        bx = x + k * (w + gap)
        if frame:
            out += f'<rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="5" fill="none" stroke="{GL}" stroke-width="2"/>'
        if v > 0:
            out += f'<rect x="{bx}" y="{y+h-v*h}" width="{w}" height="{v*h}" rx="5" fill="{cols[k % len(cols)]}"/>'
    return out


# ---------- slide visuals ----------
def how_it_works():
    W, H = 1660, 640
    b = ''
    T, S = 46, 32
    # data matrix
    x0, y0, c = 130, 200, 100
    b += text(x0 + 1.5 * c, 60, 'Data', T, DK, weight=800)
    b += text(x0 + 1.5 * c, 108, 'public', S, GR)
    for j, m in enumerate(METRICS):
        b += f'<rect x="{x0+j*c+10}" y="{y0-34}" width="{c-20}" height="14" rx="7" fill="{MCOL[j]}"/>'
    for i, p in enumerate(PROJECTS):
        b += text(x0 - 16, y0 + i * c + c / 2 + 11, p, S, GR, 'end')
        for j in range(3):
            v = VAL[i][j]
            b += f'<rect x="{x0+j*c+5}" y="{y0+i*c+5}" width="{c-10}" height="{c-10}" rx="12" fill="{MCOL[j]}" fill-opacity="{0.15+0.85*v:.2f}"/>'
            b += text(x0 + j * c + c / 2, y0 + i * c + c / 2 + 12, f'{v:.1f}'.lstrip('0'), 34, DK, weight=700)
    b += arrow(455, 350, 525)
    # ballots
    bx = 560
    b += text(bx + 115, 60, 'Ballots', T, DK, weight=800)
    b += text(bx + 115, 108, 'what matters', S, GR)
    for v in range(3):
        yy = 165 + v * 150
        b += head(bx + 24, yy + 42, 18, GR)
        b += bars(bx + 80, yy, BALLOTS[v], w=40, gap=10, h=120)
    b += arrow(830, 350, 900)
    # aggregate
    agg = [st.median(col) for col in zip(*BALLOTS)]
    ax = 935
    b += text(ax + 80, 60, 'Weights', T, DK, weight=800)
    b += text(ax + 80, 108, 'one per metric', S, GR)
    b += bars(ax, 215, agg, w=50, gap=14, h=260)
    b += arrow(1150, 350, 1220)
    # scores
    sc = [sum(a * v for a, v in zip(agg, VAL[i])) for i in range(3)]
    sx = 1360
    b += text(sx + 130, 60, 'Scores', T, DK, weight=800)
    b += text(sx + 130, 108, 'weighted sums', S, GR)
    for i, p in enumerate(PROJECTS):
        yy = 215 + i * 100
        b += text(sx - 16, yy + 44, p, S, GR, 'end')
        b += f'<rect x="{sx}" y="{yy}" width="{sc[i]*560:.0f}" height="64" rx="10" fill="{DK}"/>'
    return svg(W, H, b)


def ballot_formats():
    W, H = 1660, 520
    b = ''
    panels = [('Fractional', 'any weight', [.8, .3, 1, .5], 'f'),
              ('Cumulative', 'split a budget', [.4, .3, .2, .1], 'c'),
              ('Approval', 'in or out', [1, 1, 0, 1], 'a'),
              ('Plurality', 'pick one', [0, 1, 0, 0], 'p')]
    for k, (name, sub, vals, kind) in enumerate(panels):
        x = 40 + k * 410
        b += f'<rect x="{x}" y="20" width="380" height="480" rx="18" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
        b += f'<rect x="{x}" y="20" width="380" height="10" rx="5" fill="{OR}"/>'
        b += text(x + 190, 95, name, 40, DK, weight=800)
        b += text(x + 190, 140, sub, 30, GR)
        b += bars(x + 70, 200, vals, w=46, gap=18, h=220, cols=[OR])
        if kind == 'c':
            b += text(x + 190, 470, '= 100%', 28, GR, weight=700)
        if kind == 'a':
            for j, v in enumerate(vals):
                b += text(x + 70 + j * 64 + 23, 470, '✓' if v else '✗', 32, DK if v else GL, weight=700)
    return svg(W, H, b)


def numline(lo, hi, dots, marks, W=1600, H=360, unit='', ticks=None, fmt=None):
    """dots: (value, label, kind) kind in dot|on|ghost; marks: (value, label, color, shape)."""
    fmt = fmt or (lambda v: f'{v:g}{unit}')
    X = lambda v: 80 + (v - lo) / (hi - lo) * (W - 160)
    y = 170
    b = f'<line x1="60" y1="{y}" x2="{W-60}" y2="{y}" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
    for t in (ticks or []):
        b += f'<line x1="{X(t)}" y1="{y-10}" x2="{X(t)}" y2="{y+10}" stroke="{GL}" stroke-width="3"/>'
        b += text(X(t), y + 46, fmt(t), 28, GL)
    for v, lab, kind in dots:
        if kind == 'ghost':
            b += f'<circle cx="{X(v)}" cy="{y}" r="20" fill="none" stroke="{GL}" stroke-width="4" stroke-dasharray="6 6"/>'
            continue
        fill = OR if kind == 'on' else DK
        b += f'<circle cx="{X(v)}" cy="{y}" r="22" fill="{fill}"/>'
        b += text(X(v), y - 46, lab, 32, DK, weight=700)
    for v, lab, color, shape in marks:
        if shape == 'tri':
            b += f'<path d="M{X(v)} {y+74} l-22 36 h44 z" fill="{color}"/>'
        else:
            b += f'<path d="M{X(v)} {y+70} l22 24 l-22 24 l-22 -24 z" fill="{color}"/>'
        b += text(X(v), y + 158, lab, 34, color, weight=800)
    return svg(W, H, b)


def ann_table(lie):
    rows = [('Ann', [1, 1 if lie else 0]), ('Ben', [0, 1]), ('Cat', [0, 0])]
    med = [st.median(c) for c in zip(*[r[1] for r in rows])]
    W, H = 1100, 470
    b = ''
    cx = [420, 600, 860]
    for x, h in zip(cx, ['metric A', 'metric B', 'score']):
        b += text(x, 50, h, 32, GR, weight=700)
    for i, (nm, v) in enumerate(rows + [('Median', med)]):
        y = 80 + i * 92
        b += text(40, y + 52, nm, 36, DK, 'start', weight=800 if nm in ('Ann', 'Median') else 400)
        if nm == 'Ann':
            b += text(150, y + 52, '(lie)' if lie else '(truth)', 30, OR if lie else GR, 'start', weight=700)
        for j, val in enumerate(v):
            hot = (lie and nm == 'Ann' and j == 1)
            b += f'<rect x="{cx[j]-75}" y="{y}" width="150" height="74" rx="12" fill="{OR if hot else CARD}" stroke="{GL}" stroke-width="{0 if hot else 2}"/>'
            b += text(cx[j], y + 50, f'{val:g}', 36, DK, weight=700)
        if nm in ('Ann', 'Median'):
            s = 1 if nm == 'Ann' else med[0] + med[1]
            lab = 'wants 1' if nm == 'Ann' else f'{s:g}'
            fill = OR if nm == 'Median' else PALE
            b += f'<rect x="{cx[2]-110}" y="{y}" width="220" height="74" rx="12" fill="{fill}"/>'
            b += text(cx[2], y + 50, lab, 36, DK, weight=800)
    return svg(W, H, b)


def clone_vis(after):
    W, H = 1600, 520
    b = ''
    before = [.4, .2, .2]
    split = [(.2, .2), (.2, 0), (0, .2)]
    names = ['Ann', 'Ben', 'Cat']
    hmax = 300
    base = 400

    def column(x, vals, title, dashed=False):
        o = text(x + 150, 60, title, 34, DK, weight=800)
        o += f'<rect x="{x}" y="80" width="300" height="{base-60}" rx="14" fill="none" stroke="{GL}" stroke-width="3" {"stroke-dasharray=\"14 10\"" if dashed else ""}/>'
        for k, v in enumerate(vals):
            bx = x + 30 + k * 85
            if v > 0:
                o += f'<rect x="{bx}" y="{base - v*hmax/0.4*0.75}" width="70" height="{v*hmax/0.4*0.75}" rx="8" fill="{DK}"/>'
            o += text(bx + 35, base + 44, names[k], 30, GR)
            o += text(bx + 35, base - v * hmax / 0.4 * 0.75 - 12, f'{v:g}', 30, DK, weight=700)
        m = st.median(vals)
        y = base - m * hmax / 0.4 * 0.75
        o += f'<line x1="{x+10}" y1="{y}" x2="{x+290}" y2="{y}" stroke="{OR}" stroke-width="6" stroke-dasharray="4 10" stroke-linecap="round"/>'
        o += text(x + 150, base + 100, f'median {m:g}', 32, OR, weight=800)
        return o, m

    if not after:
        o, m = column(160, before, 'Fees')
        b += o
        b += text(1150, 220, 'Fees weight', 34, GR)
        b += text(1150, 290, f'median: {m:g}', 52, OR, weight=800)
        b += text(1150, 360, f'mean: {sum(before)/3:.2f}', 40, DK, weight=700)
    else:
        o1, m1 = column(60, [s[0] for s in split], 'Fees')
        o2, m2 = column(420, [s[1] for s in split], 'Fees (log)', dashed=True)
        b += o1 + o2
        b += text(1210, 220, 'Fees weight, in total', 34, GR)
        b += text(1210, 290, f'median: {m1:g} + {m2:g} = {m1+m2:g}', 52, OR, weight=800)
        b += text(1210, 360, f'mean: {sum(before)/3:.2f}  (unchanged)', 40, DK, weight=700)
    return svg(W, H, b)


def search_vis():
    W, H = 1660, 560
    b = ''
    # left: smooth region
    b += f'<rect x="20" y="20" width="790" height="520" rx="22" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
    b += f'<path d="M150 380 C120 230 260 130 420 150 C590 170 690 260 640 390 C600 480 330 500 220 460 C180 445 160 420 150 380 Z" fill="{PALE}" stroke="{OR}" stroke-width="5"/>'
    b += f'<path d="M260 400 C330 360 420 320 490 270" fill="none" stroke="{DK}" stroke-width="5" stroke-dasharray="2 14" stroke-linecap="round"/>'
    b += f'<circle cx="260" cy="400" r="12" fill="{DK}"/>'
    b += star(500, 262, 30)
    b += text(415, 90, 'Mean', 44, DK, weight=800)
    # right: islands
    b += f'<rect x="850" y="20" width="790" height="520" rx="22" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
    import random
    random.seed(4)
    for _ in range(26):
        x, y, r = random.randint(930, 1560), random.randint(150, 500), random.randint(14, 34)
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PALE}" stroke="{OR}" stroke-width="4"/>'
    b += star(1330, 300, 30)
    b += text(1245, 90, 'Median, budget ballots', 44, DK, weight=800)
    return svg(W, H, b)


def star(cx, cy, r):
    import math
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append(f'{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{DK}"/>'


def crowd_vis():
    W, H = 1500, 560
    data = [(5, .353), (11, .195), (21, .103)]
    b = ''
    base = 470
    for k, (n, g) in enumerate(data):
        x = 140 + k * 460
        h = g / .4 * 380
        b += f'<rect x="{x}" y="{base-h}" width="240" height="{h}" rx="14" fill="{OR}"/>'
        b += text(x + 120, base - h - 24, f'{round(g*100)}%', 52, DK, weight=800)
        # little crowd
        cols = min(n, 11)
        for q in range(n):
            r, c = divmod(q, cols)
            b += f'<circle cx="{x + 120 - (cols-1)*11 + c*22}" cy="{base + 40 + r*24}" r="8" fill="{GR}"/>'
        b += text(x + 120, base + 40 + ((n - 1) // cols + 1) * 24 + 26, f'{n} voters', 28, GR)
    return svg(W, H + 60, b)


# ---------- slides ----------
def deco(name, dark=False, cls='deco'):
    return f'<img class="{cls}" src="img/{name}{"-dark" if dark else ""}.svg" alt="">'


TITLE = '''
<section class="slide dark center">
  <p class="eyebrow">MidChain DeFi Conference</p>
  <h1>Metric-Based Voting</h1>
  <p class="big muted">Designing Rules for Ecosystem Resource Allocation</p>
  <p class="ref" style="bottom:128px;font-size:32px">Nimrod Talmon · joint work with Eyal Briman</p>
  <p class="ref">Ben-Gurion University of the Negev · October 26, 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>'''

slides = [TITLE]
S = slides.append

S(f'''<section class="slide light center">
  <h1 class="q">A pot of money,<br>many projects.<br>Who gets what?</h1>
  {deco('pot')}
</section>''')

S(f'''<section class="slide dark">
  <h2>Optimism Retro Funding</h2>
  <p class="big">Over $100M in four rounds, and a new voting rule every round</p>
  <div class="chips" style="margin-block:auto">
    <span class="chip">Quadratic</span><span class="arrow">→</span>
    <span class="chip">Mean</span><span class="arrow">→</span>
    <span class="chip">Quorum median</span><span class="arrow">→</span>
    <span class="chip on">Capped median</span>
  </div>
  <p class="ref">Briman, Talmon, Kreitenweis, Idrees 2025</p>
  <aside>Rounds 1–4. Picking a rule is hard even for a careful community.</aside>
</section>''')

S(f'''<section class="slide accent center">
  <h1 class="q">Which rule is the right one?</h1>
  <p class="big">This is what social choice studies</p>
  {deco('scale', True, 'deco sm')}
</section>''')

S(f'''<section class="slide light">
  <h2>We looked at Optimism's rules</h2>
  <div class="rows ruled">
    <div class="row"><span class="k">Found</span><p>The median rules invite strategic voting</p></div>
    <div class="row"><span class="k">Suggested</span><p>Moving phantoms: no gain from lying</p></div>
  </div>
  <p class="ref">Freeman, Pennock, Peters, Wortman Vaughan 2019 · Briman, Talmon, Kreitenweis, Idrees 2025</p>
  {deco('magnifier', cls='deco sm')}
  <aside>Rounds 3 and 4 are not strategyproof. Utilitarian moving phantoms: strategyproof and maximizes L1 welfare.</aside>
</section>''')

S(f'''<section class="slide dark">
  <h2>Round 4: vote on metrics, not on projects</h2>
  <div class="cards">
    <div class="card top"><span class="num">108</span><span class="label">voters</span></div>
    <div class="card top"><span class="num">16</span><span class="label">metrics</span></div>
    <div class="card top"><span class="num">230</span><span class="label">projects</span></div>
    <div class="card top"><span class="num">10M</span><span class="label">OP</span></div>
  </div>
  <p class="muted">Voters weighted metrics; onchain data scored the projects</p>
</section>''')

S(f'''<section class="slide light">
  <h2>Not only crypto</h2>
  <div class="cards">
    <div class="card top"><h3>OECD Better Life Index</h3><p>Rank countries: you weight 11 topics (income, health, …)</p></div>
    <div class="card top"><h3>ERC grants</h3><p>Excellence = ambition, feasibility, the PI</p></div>
  </div>
  {deco('globe', cls='deco sm')}
</section>''')

S('''<section class="slide dark center">
  <p class="eyebrow">The model</p>
  <h1>Metric-based voting</h1>
</section>''')

S(f'''<section class="slide light">
  <h2>How it works</h2>
  <div style="margin-block:auto">{how_it_works()}</div>
  <aside>Running example: three projects, three metrics, three voters. Here the weights are the per-metric median.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>What a ballot looks like</h2>
  <div style="margin-block:auto">{ballot_formats()}</div>
</section>''')

S(f'''<section class="slide light">
  <h2>Mean or median, metric by metric</h2>
  <p class="muted">Three voters on the Users metric</p>
  <div style="margin-block:auto">{numline(0, 1, [(.9, 'Ann', 'dot'), (.1, 'Ben', 'dot'), (.3, 'Cat', 'dot')],
                                         [(sum([.9, .1, .3]) / 3, 'mean', DK, 'tri'), (.3, 'median', OR, 'dia')], ticks=[0, .5, 1])}</div>
  <aside>Mean: what composite indices typically use. Median: what social choice usually recommends.</aside>
</section>''')

S(f'''<section class="slide dark center">
  <p class="eyebrow">Strategic voting</p>
  <h1>Can a voter gain by lying?</h1>
  {deco('ballot')}
</section>''')

TH = [16, 20, 24, 28, 32]
S(f'''<section class="slide light">
  <h2>The office thermostat</h2>
  <div style="margin-block:auto">{numline(15, 33, [(18, 'Ann', 'dot'), (22, 'Ben', 'dot'), (26, 'Cat', 'dot')], [(22, 'mean 22°', DK, 'tri')], ticks=TH, unit='°')}</div>
  {deco('thermo', cls='deco sm')}
</section>''')

S(f'''<section class="slide light">
  <h2>Cat says 32°</h2>
  <div style="margin-block:auto">{numline(15, 33, [(18, 'Ann', 'dot'), (22, 'Ben', 'dot'), (26, '', 'ghost'), (32, 'Cat', 'on')], [(24, 'mean 24°', DK, 'tri')], ticks=TH, unit='°')}</div>
  <p class="muted">The mean rewards exaggerating. No surprise.</p>
</section>''')

S(f'''<section class="slide light">
  <h2>The median does not move</h2>
  <div style="margin-block:auto">{numline(15, 33, [(18, 'Ann', 'dot'), (22, 'Ben', 'dot'), (26, '', 'ghost'), (32, 'Cat', 'on')], [(22, 'median 22°', OR, 'dia')], ticks=TH, unit='°')}</div>
  <p class="muted">On one dimension, nobody gains by lying to the median</p>
</section>''')

S('''<section class="slide accent center">
  <h1 class="q">So a median per metric is safe too?</h1>
</section>''')

S(f'''<section class="slide light">
  <h2>One project, worth 1 on metric A and on metric B</h2>
  <div style="margin-block:auto">{ann_table(False)}</div>
  <aside>Truthfully: medians 0 and 0, score 0. Ann wants score 1.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>One project, worth 1 on metric A and on metric B</h2>
  <div style="margin-block:auto">{ann_table(True)}</div>
  <aside>Ann says B matters too. Median of B becomes 1, the score becomes 1: exactly what she wanted.</aside>
</section>''')

S(f'''<section class="slide dark">
  <h2>Why</h2>
  <p class="big">Ann cares about the score, not about each weight</p>
  <p class="big muted">She lost on A, so she bought it back on B</p>
  <p class="big hl" style="margin-top:auto;margin-bottom:auto">No sensible metric-by-metric rule is safe from this</p>
  {deco('scale', cls='deco sm')}
  <aside>Theorem: no rule on fractional ballots is value-blind, metric-wise separable, metric-neutral, anonymous, unanimous, and strategyproof.</aside>
</section>''')

S(f'''<section class="slide dark center">
  <p class="eyebrow">The platform's choices</p>
  <h1>Duplicate metrics</h1>
  <p class="big muted">Round 4: gas fees, and also log gas fees</p>
  {deco('clone', cls='deco sm')}
  <aside>Both on 94 of 108 ballots.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Three voters, one Fees metric</h2>
  <div style="margin-block:auto">{clone_vis(False)}</div>
  <aside>Budget ballots; the rest of each voter's budget is on other metrics.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Add a copy. Same opinions.</h2>
  <div style="margin-block:auto">{clone_vis(True)}</div>
  <p class="hl big" style="align-self:flex-start">The median doubled Fees</p>
  <aside>Each voter splits the same Fees weight across the two copies. Mean is unchanged by any such split; median can change.</aside>
</section>''')

S('''<section class="slide accent center">
  <h1 class="q">Can someone hit a target scorecard?</h1>
  <p class="big">By choosing a ballot, the metrics, or the copies</p>
  <aside>Exact score reachability: an auditor's and a designer's question.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Searching for the lever</h2>
  <div style="margin-block:auto">{search_vis()}</div>
  <div class="cols" style="margin:0;gap:40px">
    <p>One smooth region: <b>easy</b> to search</p>
    <p>Scattered islands: a <b>hard</b> puzzle</p>
  </div>
  <aside>Mean with continuous ballots: a linear program. Median with budget ballots: every lever is NP-hard.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Good news: lying pays less in a crowd</h2>
  <div style="margin-block:auto;align-self:center">{crowd_vis()}</div>
  <p class="muted">How much of the gap to her ideal a liar can close (typical case)</p>
  <aside>Synthetic data, fractional ballots, mean rule; the median is nearly identical.</aside>
</section>''')

S(f'''<section class="slide accent center">
  <h1 class="q">Metric-based voting is effective,<br>but not easy to do right</h1>
  {deco('bulb', True, 'deco sm')}
</section>''')

slides.append(TITLE)

html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Metric-Based Voting · Nimrod Talmon</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@300..900&display=swap">
<link rel="stylesheet" href="../assets/deck.css">
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
