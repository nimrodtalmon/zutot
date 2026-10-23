#!/usr/bin/env python3
"""Builds slides/variants-of-liquid-representation/index.html (inline SVG visuals)."""
import math
import os

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'index.html')
OR, DK, GR, GL, CARD, PALE, LT = '#F7941D', '#26282C', '#5F6368', '#B9BCC1', '#FDFDFB', '#FCE8D2', '#F3F3F1'
GREEN, GOLD, BLUE = '#3E9B4F', '#E2B42B', '#3A7BC8'
FONT = 'font-family="Heebo, Arial, sans-serif"'


def svg(w, h, body, style=''):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT} style="{style}">{body}</svg>'


def text(x, y, s, size=30, fill=DK, anchor='middle', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def head(cx, cy, r, fill):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx-1.6*r} {cy+2.6*r} a{1.6*r} {1.6*r} 0 0 1 {3.2*r} 0 Z" fill="{fill}"/>')


def arrow(x1, y1, x2, y2, color=OR, w=6):
    """Straight arrow from (x1,y1) to (x2,y2)."""
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 20 * math.cos(a), y2 - 20 * math.sin(a)
    p1 = (bx + 12 * math.sin(a), by - 12 * math.cos(a))
    p2 = (bx - 12 * math.sin(a), by + 12 * math.cos(a))
    return (f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')


def chip(cx, cy, label, fill, fg='#fff', w=220, size=30):
    return (f'<rect x="{cx-w/2}" y="{cy-28}" width="{w}" height="56" rx="28" fill="{fill}"/>'
            + text(cx, cy + 11, label, size, fg, weight=700))


def dice(cx, cy, s, color=DK):
    pips = [(-.25, -.25), (.25, .25), (0, 0), (-.25, .25), (.25, -.25)]
    return (f'<rect x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" rx="{s/6}" fill="{CARD}" stroke="{color}" stroke-width="5"/>'
            + ''.join(f'<circle cx="{cx+x*s:.1f}" cy="{cy+y*s:.1f}" r="{s/11:.1f}" fill="{color}"/>' for x, y in pips))


# ---------- visuals ----------
def wp5_vis():
    W, H = 1640, 420
    boxes = [('Compare', 'lottery vs delegation', 'done'), ('Vary', 'variants of delegation', 'now'),
             ('Recommend', 'design guidance', 'next')]
    b = ''
    for k, (name, sub, st) in enumerate(boxes):
        x = 20 + k * 560
        on = st == 'now'
        b += (f'<rect x="{x}" y="60" width="480" height="200" rx="24" fill="{OR if on else CARD}" '
              f'stroke="{OR if on else GL}" stroke-width="3"/>')
        b += text(x + 240, 150, name, 56, DK, weight=800)
        b += text(x + 240, 210, sub, 32, DK if on else GR)
        if k < 2:
            b += arrow(x + 495, 160, x + 545, 160, GR)
        if st == 'done':
            b += (f'<circle cx="{x+450}" cy="70" r="30" fill="{GREEN}"/>'
                  f'<path d="M{x+436} 70 l10 11 l20 -22" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    b += text(20 + 560 + 240, 340, '▲ we are here', 40, DK, weight=800)
    return svg(W, H, b)


def recall_vis():
    W, H = 1640, 520
    b = ''
    rows = [('Polarized', 0.05, 'lottery steadier', GR), ('Moderate', 0.4, 'delegation steadier', OR)]
    for r, (name, a, verdict, col) in enumerate(rows):
        y = 120 + r * 250
        b += text(20, y + 14, name, 44, DK, 'start', weight=800)
        x0, x1 = 360, 1180
        b += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
        for p in (0, a, .5, 1 - a, 1):
            b += f'<circle cx="{x0+p*(x1-x0):.1f}" cy="{y}" r="22" fill="{DK}"/>'
        b += chip(1420, y, verdict, col, '#fff' if col == GR else DK, w=380, size=34)
    return svg(W, H, b)


def committee_vis():
    W, H = 1640, 440
    x0, x1, xm, y = 60, 1580, 820, 250
    b = (f'<rect x="{x0}" y="{y-150}" width="{xm-x0}" height="150" rx="16" fill="{GL}" fill-opacity=".35"/>'
         f'<rect x="{xm}" y="{y-150}" width="{x1-xm}" height="150" rx="16" fill="{PALE}"/>')
    b += text((x0 + xm) / 2, y - 62, 'lottery more accurate', 44, DK, weight=800)
    b += text((xm + x1) / 2, y - 62, 'delegation more accurate', 44, DK, weight=800)
    b += arrow(x0, y + 40, x1, y + 40, DK)
    b += f'<line x1="{xm}" y1="{y-170}" x2="{xm}" y2="{y+70}" stroke="{OR}" stroke-width="6" stroke-dasharray="14 10"/>'
    b += text(xm, y + 130, '≈ √(2 × population)', 44, OR, weight=800)
    b += text(x1, y + 130, 'committee size', 36, GR, 'end')
    return svg(W, H, b)


TOPICS = [('Health', GREEN), ('Transport', BLUE), ('Budget', GOLD)]


def topic_vis():
    W, H = 1640, 560
    b = ''
    # standard LD
    b += text(330, 40, 'Standard', 40, GR, weight=700)
    b += head(110, 260, 34, DK)
    b += arrow(170, 290, 470, 290, GR)
    b += head(540, 260, 34, GR)
    b += text(330, 470, '1 delegation', 40, DK, weight=800)
    # divider
    b += f'<line x1="760" y1="40" x2="760" y2="500" stroke="{GL}" stroke-width="3" stroke-dasharray="6 10"/>'
    # topic-based
    b += text(1200, 40, 'Topic-based', 40, OR, weight=700)
    b += head(900, 260, 34, DK)
    ys = [130, 290, 450]
    for (name, col), yy in zip(TOPICS, ys):
        b += arrow(960, 290, 1400, yy, col)
        b += head(1470, yy - 30, 30, col)
        b += chip(1180, (290 + yy) / 2, name, col, '#fff', w=210, size=30)
    b += text(1200, 545, '3 delegations, 3 specialists', 40, DK, weight=800)
    return svg(W, H, b)


def chart_vis():
    """Schematic: best achievable accuracy vs number of delegation areas."""
    W, H = 1640, 620
    X0, X1, Y0, Y1 = 220, 1300, 540, 90
    m = 12
    X = lambda b: X0 + (b - 1) / (m - 1) * (X1 - X0)
    Y = lambda f: Y0 - f * (Y0 - Y1)
    vals = [.55, .76, .89, .97, .975, .98, .985, .99, .993, .996, .998, 1]
    b = ''
    b += f'<line x1="{X0}" y1="{Y0}" x2="{X1+40}" y2="{Y0}" stroke="{DK}" stroke-width="4"/>'
    b += f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-30}" stroke="{DK}" stroke-width="4"/>'
    b += f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{GL}" stroke-width="3" stroke-dasharray="8 8"/>'
    b += text(X0 - 20, Y1 + 10, 'one area', 28, GR, 'end') + text(X0 - 20, Y1 + 42, 'per topic', 28, GR, 'end')
    b += text(X0 - 20, Y0 + 10, 'coin flip', 28, GR, 'end')
    b += text((X0 + X1) / 2, Y0 + 60, 'number of delegation areas', 32, GR)
    # guarantee line b/m
    b += (f'<line x1="{X(1):.1f}" y1="{Y(1/m):.1f}" x2="{X(m):.1f}" y2="{Y(1):.1f}" stroke="{GR}" '
          f'stroke-width="5" stroke-dasharray="14 10"/>')
    b += text(X(8.2), Y(8.2 / m) + 50, 'guaranteed: at least this', 34, GR, 'start', weight=700)
    # curve
    pts = ' '.join(f'{X(k+1):.1f},{Y(v):.1f}' for k, v in enumerate(vals))
    b += f'<polyline points="{pts}" fill="none" stroke="{OR}" stroke-width="8" stroke-linejoin="round"/>'
    for k, v in enumerate(vals):
        b += f'<circle cx="{X(k+1):.1f}" cy="{Y(v):.1f}" r="9" fill="{OR}"/>'
    # cluster marker
    b += f'<line x1="{X(4):.1f}" y1="{Y0}" x2="{X(4):.1f}" y2="{Y(.97)+20:.1f}" stroke="{OR}" stroke-width="3" stroke-dasharray="6 8"/>'
    b += text(X(4), Y0 - 20, '4 clusters', 28, OR, weight=700)
    b += text(X(4) + 30, Y(.97) - 40, 'one area per cluster: most of the gain', 34, DK, 'start', weight=700)
    b += text(X(1) + 24, Y(.55) + 70, 'never goes down', 34, OR, 'start', weight=800)
    return svg(W, H, b)


def reps_vis():
    W, H = 1640, 420
    weights = [8, 1, 3, 1, 1, 5, 1, 2, 1, 1, 1, 4]
    drawn = {0, 2, 5, 8, 11}
    b = ''
    x = 60
    for k, w in enumerate(weights):
        r = 24 + 14 * math.sqrt(w)
        cx = x + r
        on = k in drawn
        b += (f'<circle cx="{cx:.1f}" cy="200" r="{r:.1f}" fill="{OR if on else CARD}" '
              f'stroke="{OR if on else GL}" stroke-width="5"/>')
        b += text(cx, 212, str(w), 34, DK, weight=700)
        x += 2 * r + 22
    b += f'<circle cx="80" cy="370" r="16" fill="{OR}"/>' + text(110, 382, 'drawn for this issue', 32, DK, 'start', weight=700)
    b += text(1580, 382, 'number = delegations held', 32, GR, 'end')
    return svg(W, H, b)


def knob_vis():
    W, H = 1640, 600
    groups = [('0', [1, 1, 1, 1, 1], 'lottery among', 'representatives'), ('½', [math.sqrt(8), 1, 1, 1, 1], '', ''),
              ('1', [8, 1, 1, 1, 1], 'standard', 'liquid democracy')]
    unit, base = 40, 360
    b = f'<line x1="270" y1="420" x2="1310" y2="420" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
    for k, (lab, vals, c1, c2) in enumerate(groups):
        gx = 120 + k * 520
        for j, v in enumerate(vals):
            bx = gx + j * 64
            b += f'<rect x="{bx}" y="{base-v*unit:.1f}" width="48" height="{v*unit:.1f}" rx="6" fill="{OR if j == 0 else GR}"/>'
        cx = gx + 150
        if lab == '½':
            b += f'<circle cx="{cx}" cy="420" r="30" fill="{OR}"/>'
        else:
            b += f'<circle cx="{cx}" cy="420" r="12" fill="{GR}"/>'
        b += text(cx, 500, lab, 52, DK, weight=800)
        if c1:
            b += text(cx, 550, c1, 32, GR) + text(cx, 590, c2, 32, GR)
    return svg(W, H, b)


def areas_vis():
    W, H = 1640, 560
    panels = [('1 area', 1), ('3 areas', 3), ('one per topic', 6)]
    cols = [GR, GREEN, BLUE, GOLD, '#8E5BB5', '#D64545']
    b = ''
    for k, (lab, n) in enumerate(panels):
        x = 40 + k * 540
        b += text(x + 230, 40, lab, 40, DK, weight=800)
        b += head(x + 50, 220, 30, DK)
        for j in range(n):
            yy = 220 if n == 1 else 70 + j * (310 / (n - 1))
            col = GR if n == 1 else cols[1 + j % 5] if n == 3 else cols[j % 6]
            b += arrow(x + 100, 240, x + 360, yy + 20, col, 5)
            b += head(x + 400, yy, 14 if n == 6 else 24, col)
    b += (f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{GL}"/>'
          f'<stop offset="1" stop-color="{OR}"/></linearGradient></defs>'
          f'<rect x="40" y="460" width="1560" height="10" rx="5" fill="url(#g)"/>')
    b += text(40, 530, 'fewer decisions per citizen', 36, DK, 'start', weight=700)
    b += text(1600, 530, 'better specialists', 36, DK, 'end', weight=700)
    return svg(W, H, b)


# ---------- slides ----------
TITLE = '''
<section class="slide dark center">
  <p class="eyebrow">PERYCLES · WP5</p>
  <h1>Variants of Liquid<br>Representation</h1>
  <p class="ref" style="bottom:128px;font-size:32px">Nimrod Talmon · with Eyal Briman and Davide Grossi</p>
  <p class="ref">Ben-Gurion University of the Negev · Rome, December 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>'''

slides = [TITLE]
S = slides.append

S(f'''<section class="slide light">
  <h2>WP5 in one picture</h2>
  <div style="margin-block:auto">{wp5_vis()}</div>
  <aside>T5.1 done (D5.1, February). Today: the variants of D5.2, due in December. Then we turn to design recommendations, D5.3 — that is where I want your input.</aside>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Recall · Lot or proxy?</p>
  <h2>A committee by lottery, or by delegation?</h2>
  <div style="margin-block:auto">{recall_vis()}</div>
  <p class="ref">Which one reproduces the everyone-votes outcome more steadily? It depends on the population.</p>
  <aside>Both mechanisms pick a committee and let it decide; we compare how close each gets to direct democracy. Five agents on a line: when the population is polarized, the lottery is steadier; when it is moderate, delegation is.</aside>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">New since D5.1</p>
  <h2>Larger committees can flip the answer</h2>
  <div style="margin-block:auto">{committee_vis()}</div>
  <p class="ref">Large populations of close-knit pairs</p>
  <aside>One new result: in large populations made of close-knit pairs, the lottery is more accurate for small committees and delegation for larger ones; the switch is around the square root of twice the population.</aside>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1</p>
  <h2>Delegate per topic</h2>
  <div style="margin-block:auto">{topic_vis()}</div>
  <aside>A citizen may trust different people on different topics. The platform groups topics into delegation areas, and citizens delegate once per area.</aside>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1</p>
  <h2>How many delegation areas?</h2>
  <div style="margin-block:auto">{areas_vis()}</div>
  <aside>Each extra area is another delegation decision for every citizen, but lets each area be decided by people who know it. How many areas are worth it?</aside>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1 · what we show</p>
  <h2>A few areas go a long way</h2>
  <div style="margin-block:auto">{chart_vis()}</div>
  <p class="ref">Schematic · with Davide Grossi</p>
  <aside>Splitting an area never lowers the best achievable accuracy. With b areas out of m topics, at least a b/m share of the gain is guaranteed. In experiments with clustered topics, one area per cluster recovers most of the gain (85 to 98 percent). Finding the best areas is computationally hard; greedy designs come with guarantees.</aside>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2</p>
  <h2>Representatives are busy: draw a panel</h2>
  <div style="margin-block:auto">{reps_vis()}</div>
  <aside>Delegation saves citizens' attention, but representatives must vote on every issue, some for many citizens. So on each issue we draw a small panel of representatives; big representatives are drawn more often, and every drawn vote is scaled up to compensate for those not drawn.</aside>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · two knobs</p>
  <h2>Panel size, and how much delegations count</h2>
  <div style="margin-block:auto">{knob_vis()}</div>
  <p class="ref">Five representatives: one holds eight citizens, four hold one each</p>
  <aside>Knob one: how many representatives are asked to vote. Knob two, the delegation strength: at one, a representative with eight delegations counts eight; at zero, everyone counts one; at one half, about 2.8.</aside>
</section>''')

S('''<section class="slide accent center">
  <h1 class="huge">≈ 160</h1>
  <p class="big">panel members match a 60/40 full vote at least 95% of the time</p>
  <p class="big" style="font-weight:700">whatever the population size</p>
  <aside>The panel size that suffices depends only on how close the vote is and on the error we accept, not on the number of citizens or representatives.</aside>
</section>''')

S('''<section class="slide light">
  <p class="eyebrow">Variant 2</p>
  <h2>The price of dampening</h2>
  <div class="cards">
    <div class="card top"><span class="num">0.35 vs 1</span><p>Citizens no longer count equally</p></div>
    <div class="card top"><span class="num">× 2</span><p>Four fake identities double the weight</p></div>
    <div class="card top"><span class="num">small</span><p>Accuracy gains we can prove</p></div>
  </div>
  <p class="ref">At strength one half, in the five-representative example · with Eyal Briman</p>
  <aside>At strength one half, each citizen behind the big representative weighs about 0.35, while a small representative weighs 1. Splitting into four identities doubles combined weight. An intermediate strength can beat both extremes in accuracy, but only under narrow conditions, and by about half a percentage point in our example.</aside>
</section>''')

S('''<section class="slide dark">
  <p class="eyebrow">Towards D5.3</p>
  <h2>Let's discuss</h2>
  <div class="rows ruled">
    <div class="row"><span class="n">1</span><p>What suggestions do we want to give?</p></div>
    <div class="row"><span class="n">2</span><p>To whom?</p></div>
    <div class="row"><span class="n">3</span><p>What would we want implemented?</p></div>
    <div class="row"><span class="n">4</span><p>Other variants worth studying?</p></div>
  </div>
</section>''')

slides.append(TITLE)

html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Variants of Liquid Representation · Nimrod Talmon</title>
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
