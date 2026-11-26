#!/usr/bin/env python3
"""Builds slides/variants-of-liquid-representation/index.html (inline SVG visuals, one interactive slide)."""
import math
import os

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'index.html')
OR, DK, GR, GL, CARD, PALE, LT = '#F7941D', '#26282C', '#5F6368', '#B9BCC1', '#FDFDFB', '#FCE8D2', '#F3F3F1'
GREEN, GOLD, BLUE = '#3E9B4F', '#E2B42B', '#3A7BC8'
FONT = 'font-family="Heebo, Arial, sans-serif"'



def svg(w, h, body, style='', extra=''):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT} style="{style}" {extra}>{body}</svg>'


def text(x, y, s, size=30, fill=DK, anchor='middle', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{s}</text>'


def head(cx, cy, r, fill, opacity=1):
    return (f'<g opacity="{opacity}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx-1.6*r} {cy+2.6*r} a{1.6*r} {1.6*r} 0 0 1 {3.2*r} 0 Z" fill="{fill}"/></g>')


def arrow(x1, y1, x2, y2, color=OR, w=6, dash=''):
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 20 * math.cos(a), y2 - 20 * math.sin(a)
    p1 = (bx + 12 * math.sin(a), by - 12 * math.cos(a))
    p2 = (bx - 12 * math.sin(a), by + 12 * math.cos(a))
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{d}/>'
            f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')


def chip(cx, cy, label, fill, fg='#fff', w=220, size=30):
    return (f'<rect x="{cx-w/2}" y="{cy-28}" width="{w}" height="56" rx="28" fill="{fill}"/>'
            + text(cx, cy + 11, label, size, fg, weight=700))


def box(cx, cy, label, w=300, h=96, fill=CARD, stroke=DK, size=36):
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
            + text(cx, cy + size * .36, label, size, DK, weight=800))


def dice(cx, cy, s, color=DK):
    pips = [(-.25, -.25), (.25, .25), (0, 0), (-.25, .25), (.25, -.25)]
    return (f'<rect x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" rx="{s/6}" fill="{CARD}" stroke="{color}" stroke-width="5"/>'
            + ''.join(f'<circle cx="{cx+x*s:.1f}" cy="{cy+y*s:.1f}" r="{s/11:.1f}" fill="{color}"/>' for x, y in pips))


def check(cx, cy, r, color=GREEN):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<path d="M{cx-r*.45} {cy} l{r*.32} {r*.36} l{r*.62} {-r*.7}" fill="none" stroke="#fff" '
            f'stroke-width="{r/4:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')



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
            b += check(x + 450, 70, 30)
    b += text(20 + 560 + 240, 340, '▲ we are here', 40, DK, weight=800)
    return svg(W, H, b)



def perarea_vis():
    W, H = 1640, 480
    b = head(300, 210, 40, DK)
    ys = [70, 240, 410]
    for (name, col), yy in zip(TOPICS, ys):
        b += arrow(370, 240, 1100, yy + 20, col)
        b += head(1190, yy - 10, 36, col)
        b += chip(760, (240 + yy + 20) / 2, name, col, '#fff', w=240, size=34)
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



TOPICS = [('Health', GREEN), ('Transport', BLUE), ('Budget', GOLD)]


# delegation forest: (x, subtree size, citizens per level)
FOREST = [(160, 6, [3, 2]), (520, 1, []), (800, 4, [2, 1]), (1110, 2, [1]), (1350, 1, [])]


def forest_vis(mode):
    W, H = 1640, 520
    drawn = {0, 2}
    b = ''
    for k, (x, w, levels) in enumerate(FOREST):
        on = mode != 'panel' or k in drawn
        op = 1 if on else .3
        g = ''
        prev = [x]
        for lv, cnt in enumerate(levels):
            y = 270 + lv * 130
            xs = [x + (j - (cnt - 1) / 2) * 90 for j in range(cnt)]
            for j, cx in enumerate(xs):
                px = prev[min(j, len(prev) - 1)]
                py = 120 if lv == 0 else 270 + (lv - 1) * 130
                g += f'<line x1="{cx}" y1="{y}" x2="{px}" y2="{py}" stroke="{GL}" stroke-width="4"/>'
            for cx in xs:
                g += f'<circle cx="{cx}" cy="{y}" r="18" fill="{GR}"/>'
            prev = xs
        r = 26 + 10 * math.sqrt(w)
        fill = OR if on else DK
        g += f'<circle cx="{x}" cy="120" r="{r:.1f}" fill="{fill}"/>' + text(x, 132, str(w), 34, '#fff' if fill == DK else DK, weight=800)
        b += f'<g opacity="{op}">{g}</g>'
    if mode == 'problem':
        for k in range(4):
            b += (f'<rect x="{1470+k*12}" y="{60+k*14}" width="130" height="170" rx="12" fill="{CARD}" stroke="{DK}" stroke-width="4"/>')
        b += text(1571, 165, 'issue', 30, DK, weight=700)
    else:
        b += dice(1530, 140, 110)
    return svg(W, H, b)




def tree_icon(cx, cy, color=DK):
    """Small delegation tree: three citizens pointing up to one representative."""
    o = ''
    for dx in (-36, 0, 36):
        o += arrow(cx + dx, cy + 40, cx + dx * .25, cy - 4, GR, 4)
        o += f'<circle cx="{cx+dx}" cy="{cy+48}" r="11" fill="{GR}"/>'
    o += f'<circle cx="{cx}" cy="{cy-18}" r="18" fill="{color}"/>'
    return o


def setting_vis():
    """Lottery and delegation each lead to their own decision; both are compared with direct democracy."""
    W, H = 1640, 560
    b = ''
    for k in range(12):
        b += f'<circle cx="{90 + 62 * (k % 3)}" cy="{180 + 62 * (k // 3)}" r="18" fill="{DK}"/>'
    b += text(152, 140, 'citizens', 32, GR)
    rows = [(110, 'lottery', [(22, 0), (22, 1), (22, 2)], 'equal weights'),
            (450, 'delegation', [(14, 0), (34, 1), (22, 2)], 'weighted')]
    for y, name, dots, sub in rows:
        b += arrow(260, 290 + (y - 280) * .25, 360, y, GR)
        b += dice(430, y, 74) if name == 'lottery' else tree_icon(430, y - 6)
        b += text(430, y + 80, name, 32, DK, weight=800)
        for r, j in dots:
            b += f'<circle cx="{560+70*j}" cy="{y}" r="{r}" fill="{OR}"/>'
        b += text(630, y + 70, sub, 28, GR)
        b += arrow(730, y, 820, y, GR)
        b += box(950, y, 'decision', 230, 90)
        b += f'<line x1="1065" y1="{y}" x2="1250" y2="{262 if y < 280 else 298}" stroke="{OR}" stroke-width="5" stroke-dasharray="10 8"/>'
    b += box(1420, 280, 'direct democracy', 340, 96, PALE, OR, 34)
    b += text(1262, 205, 'how close?', 30, OR, 'start', weight=800) + text(1262, 378, 'how close?', 30, OR, 'start', weight=800)
    return svg(W, H, b)


def findings_vis():
    W, H = 1640, 620
    b = ''

    def row(y, label, dots, deleg):
        o = text(20, y + 12, label, 40, DK, 'start', weight=700) + dots
        o += chip(1400, y, 'delegation more accurate' if deleg else 'lottery more accurate',
                  OR if deleg else GR, DK if deleg else '#fff', w=440, size=30)
        return o

    x0, x1 = 600, 1100
    X = lambda p: x0 + p * (x1 - x0)

    def line_dots(y, a, clusters):
        o = ''
        for lo, hi in clusters:
            o += (f'<rect x="{X(lo)-38:.1f}" y="{y-38}" width="{X(hi)-X(lo)+76:.1f}" height="76" rx="38" '
                  f'fill="{PALE}" stroke="{OR}" stroke-width="4"/>')
        o += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
        for p in (0, a, .5, 1 - a, 1):
            o += f'<circle cx="{X(p):.1f}" cy="{y}" r="20" fill="{DK}"/>'
        return o

    def committee(y, n):
        return ''.join(f'<circle cx="{x0+20+50*k}" cy="{y}" r="17" fill="{OR}"/>' for k in range(n))

    b += text(X(.5), 40, 'center', 28, GR, weight=700)
    b += f'<line x1="{X(.5)}" y1="52" x2="{X(.5)}" y2="250" stroke="{GL}" stroke-width="3" stroke-dasharray="8 8"/>'
    b += row(115, 'Clusters near the center', line_dots(115, .4, [(.4, .6)]), True)
    b += row(215, 'Clusters far from it', line_dots(215, .05, [(0, .05), (.95, 1)]), False)
    b += text(20, 350, 'Committee size can flip it', 36, GR, 'start', weight=800)
    b += row(435, 'Small committee', committee(435, 3), False)
    b += row(535, 'Large committee', committee(535, 11), True)
    return svg(W, H, b)


def mirror_vis():
    W, H = 1640, 520
    cx, cy = 320, 340  # spans exactly the three topic rows (chip tops 202 to bottoms 478)
    b = (f'<ellipse cx="{cx}" cy="{cy}" rx="102" ry="131" fill="{PALE}" stroke="{GOLD}" stroke-width="16"/>'
         f'<ellipse cx="{cx}" cy="{cy}" rx="80" ry="108" fill="none" stroke="{GOLD}" stroke-width="3"/>'
         f'<path d="M{cx-52} {cy-40} q8 -36 40 -52" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round"/>'
         + text(cx, cy + 40, '?', 116, GOLD, weight=800))
    xs = [960, 1210, 1460]
    ys = [230, 340, 450]
    for j, x in enumerate(xs):
        b += head(x, 90, 40, TOPICS[j][1])
    for i, (name, col) in enumerate(TOPICS):
        y = ys[i]
        b += chip(650, y, name, col, '#fff', w=240, size=34)
        for j, x in enumerate(xs):
            b += check(x, y, 28) if i == j else f'<line x1="{x-20}" y1="{y}" x2="{x+20}" y2="{y}" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
    return svg(W, H, b)


CURVES = [  # share of the gain from 1 area to one area per topic, b = 1..12 (paper, Fig. cluster budget)
    ('#FBC07A', [0.0, 0.697, 0.915, 0.98, 0.989, 0.994, 0.997, 0.998, 0.999, 1.0, 1.0, 1.0]),    # Euclidean
    ('#F7941D', [0.0, 0.386, 0.643, 0.848, 0.878, 0.903, 0.924, 0.943, 0.961, 0.976, 0.989, 1.0]),  # Gaussian
    ('#B35F00', [0.0, 0.461, 0.745, 0.979, 0.984, 0.988, 0.991, 0.994, 0.996, 0.998, 0.999, 1.0])]  # Mallows


def gain_vis():
    W, H = 1640, 560
    X0, X1, Y0, Y1 = 260, 1500, 470, 40
    X = lambda b: X0 + (b - 1) / 11 * (X1 - X0)
    Y = lambda v: Y0 - v * (Y0 - Y1)
    o = f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{DK}" stroke-width="3"/>'
    o += f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-10}" stroke="{DK}" stroke-width="3"/>'
    o += f'<line x1="{X(4)}" y1="{Y0}" x2="{X(4)}" y2="{Y1-10}" stroke="{GL}" stroke-width="3" stroke-dasharray="10 8"/>'
    o += text(X(4) + 16, Y(0.3), '12 topics in 4 groups', 30, GR, 'start', weight=700)
    for v, lab in ((0, '0%'), (1, '100%')):
        o += text(X0 - 18, Y(v) + 10, lab, 30, GR, 'end')
    for b in (1, 4, 12):
        o += text(X(b), Y0 + 44, str(b), 32, GR)
    o += text((X0 + X1) / 2, Y0 + 86, 'number of areas', 34, DK, weight=700)
    o += text(70, (Y0 + Y1) / 2, 'accuracy gain', 34, DK, weight=700, extra=f'transform="rotate(-90 70 {(Y0 + Y1) / 2})"')
    o += text(X(8), Y(0.8), 'one line per kind of population', 30, OR, weight=700)
    # inset: who is good at what (topics x people), expertise in clusters
    cx0, cy0, cs = 1150, 222, 32
    o += text(cx0 + 3 * cs, cy0 - 22, 'who is good at what', 28, GR, weight=700)
    for i in range(6):
        for j in range(6):
            on = i // 2 == j // 2
            o += (f'<rect x="{cx0 + j * cs + 2}" y="{cy0 + i * cs + 2}" width="{cs - 4}" height="{cs - 4}" rx="5" '
                  f'fill="{OR if on else LT}" stroke="{GL}" stroke-width="{0 if on else 1.5}"/>')
    o += text(cx0 - 14, cy0 + 3 * cs + 10, 'topics', 26, GR, 'end')
    o += text(cx0 + 3 * cs, cy0 + 6 * cs + 34, 'people', 26, GR)
    for col, c in CURVES:
        pts = ' '.join(f'{X(b+1):.1f},{Y(v):.1f}' for b, v in enumerate(c))
        o += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
        o += ''.join(f'<circle cx="{X(b+1):.1f}" cy="{Y(v):.1f}" r="7" fill="{col}"/>' for b, v in enumerate(c))
    return svg(W, H, o)


def nope_vis():
    W, H = 440, 220
    return svg(W, H, text(220, 128, '1 person, 1 vote', 52, DK, weight=800)
               + f'<line x1="20" y1="170" x2="420" y2="50" stroke="{OR}" stroke-width="14" stroke-linecap="round"/>')


def keep_vis():
    W, H = 520, 220
    return svg(W, H, text(230, 128, '1 person, 1 vote', 52, DK, weight=800) + check(470, 110, 36))


def best_vis():
    """Accuracy along the knob for three populations: best at 0, in between, at 1."""
    W, H = 520, 220
    x0, x1, yb = 30, 490, 200
    o = f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{DK}" stroke-width="3"/>'
    for col, pk, y0 in (('#FBC07A', 0, 40), ('#F7941D', .5, 70), ('#B35F00', 1, 100)):
        pts = []
        for j in range(41):
            t = j / 40
            pts.append(f'{x0 + t * (x1 - x0):.1f},{y0 + 90 * (t - pk) ** 2:.1f}')
        o += f'<polyline points="{' '.join(pts)}" fill="none" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
        o += text(x0 + pk * (x1 - x0), y0 - 8, '★', 40, col, weight=700)
    return svg(W, H, o)


def clones_vis():
    W, H = 440, 220
    b = head(70, 90, 30, DK) + arrow(130, 120, 200, 120, GR)
    for k in range(3):
        b += f'<g stroke="{DK}" stroke-width="3" stroke-dasharray="6 6" fill="none">'
        b += f'<circle cx="{260+70*k}" cy="90" r="26"/><path d="M{260+70*k-42} {178} a42 42 0 0 1 84 0 Z"/></g>'
    b += text(330, 215, 'more weight', 30, OR, weight=800)
    return svg(W, H, b)


def small_vis():
    W, H = 440, 220
    b = (f'<rect x="120" y="40" width="80" height="150" rx="8" fill="{GR}"/>'
         f'<rect x="240" y="34" width="80" height="156" rx="8" fill="{OR}"/>'
         f'<line x1="90" y1="190" x2="350" y2="190" stroke="{DK}" stroke-width="4"/>')
    b += text(330, 26, '+ a bit', 30, OR, weight=800)
    return svg(W, H, b)


# ---------- slides ----------
TITLE = '''
<section class="slide dark center">
  <p class="eyebrow">PERYCLES · WP5</p>
  <h1>Variants of Liquid<br>Representation</h1>
  <p class="ref" style="bottom:128px;font-size:32px">Nimrod Talmon · with Joel van der Boom, Eyal Briman, and Davide Grossi</p>
  <p class="ref">Ben-Gurion University of the Negev · Rome, December 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>'''


def divider(eyebrow, title, paper, who):
    return f'''<section class="slide dark center">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{title}</h1>
  <p class="big muted">Paper: {paper}</p>
  <p class="big">{who}</p>
</section>'''


OVEN = (f'<svg viewBox="0 0 64 64" width="64" height="64" style="vertical-align:-12px">'
        f'<path d="M22 8c-4 4 4 6 0 10M32 6c-4 4 4 6 0 10M42 8c-4 4 4 6 0 10" stroke="{OR}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        f'<rect x="6" y="22" width="52" height="38" rx="5" fill="none" stroke="#fff" stroke-width="4"/>'
        f'<line x1="6" y1="31" x2="58" y2="31" stroke="#fff" stroke-width="3"/>'
        f'<circle cx="14" cy="26.5" r="2" fill="#fff"/><circle cx="22" cy="26.5" r="2" fill="#fff"/>'
        f'<rect x="14" y="37" width="36" height="16" rx="3" fill="{OR}"/></svg>')

slides = [TITLE]
S = slides.append

S(f'''<section class="slide light">
  <h2>WP5: where we are</h2>
  <div style="margin-block:auto">{wp5_vis()}</div>
</section>''')

S(divider('Recall · D5.1', 'Lottery or delegation?',
          '“Lot or Proxy? Representation in Sortition and Liquid Democracy”',
          'with Eyal Briman and Davide Grossi · 🤞 AAMAS 2027'))

S(f'''<section class="slide light">
  <p class="eyebrow">Recall · D5.1</p>
  <h2>A committee by lottery, or by delegation?</h2>
  <div style="margin-block:auto">{setting_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Recall · D5.1</p>
  <h2>Which is more accurate?</h2>
  <p class="paper">Delegation picks representatives inside clusters</p>
  <div style="margin-block:auto">{findings_vis()}</div>
</section>''')

S(divider('Variant 1', 'Topic-based delegation',
          '“Topic Bundling for Epistemic Committee Design”',
          'with Eyal Briman and Davide Grossi · 🤞 AAMAS 2027'))

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1 · the problem</p>
  <h2>Mirror, mirror: who is my best delegate?</h2>
  <p class="paper">With one delegation for everything, no single delegate may be best on all topics</p>
  <div style="margin-block:auto">{mirror_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1 · the approach</p>
  <h2>Delegate per area</h2>
  <p class="paper">Our question: how fine should the areas be?</p>
  <div style="margin-block:auto">{perarea_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1</p>
  <h2>How many areas?</h2>
  <div style="margin-block:auto">{areas_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1 · what we show</p>
  <h2>As many areas as groups of topics</h2>
  <p class="paper">Group topics that share experts; the less expertise overlaps, the more splitting pays</p>
  <div style="margin-block:auto">{gain_vis()}</div>
</section>''')

S(divider('Variant 2', 'Sortition on top of delegation', '“Sampled Panels of Delegates in Liquid Democracy”',
          'with Joel van der Boom and Eyal Briman · ' + OVEN + ' in the oven'))

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · the problem</p>
  <h2>Representatives must vote on everything</h2>
  <p class="paper">Some may be busy, absent, or vote without attention</p>
  <div class="data">Data from six DAOs: even holders of over 1% of the voting power vote on only 45% of proposals, on average</div>
  <div style="margin-block:auto">{forest_vis('problem')}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · the approach</p>
  <h2>Draw a small panel</h2>
  <p class="paper">Each drawn vote is scaled up, so every voter keeps the same expected weight</p>
  <div style="margin-block:auto">{forest_vis('panel')}</div>
</section>''')

S('''<section class="slide light center">
  <p class="big">Aggressive sampling, same decision</p>
  <h1 class="huge" style="color:var(--orange)">≈ 150</h1>
  <p class="big">drawn delegates match a 60/40 vote 95% of the time</p>
  <p class="big" style="font-weight:700">at any population size</p>
</section>''')

S('''<section class="slide light">
  <p class="eyebrow">Variant 2 · two knobs</p>
  <h2>Panel size, and what support buys</h2>
  <p class="paper">Example: one representative of 5 citizens (right 80%), ten of 1 citizen each (right 60%)</p>
  <div class="interactive knobs">
    <div class="kcol">
      <div class="klab">Panel size <b id="kbv"></b> <span class="keys"><i>1</i>◀ ▶<i>2</i></span></div>
      <input type="range" id="kb" min="1" max="11" step="1" value="5">
      <div class="klab">Support buys chance (0) or weight (1) <b id="ksv"></b> <span class="keys"><i>3</i>◀ ▶<i>4</i></span></div>
      <input type="range" id="ks" min="0" max="1" step="0.05" value="0.5">
      <div class="khint"><span>0: big delegates drawn more often</span><span>1: their votes count more</span></div>
      <svg id="kbars" viewBox="0 0 700 270" width="700" height="270"></svg>
    </div>
    <div class="kcol">
      <p class="kacc">Accuracy <b id="kacc"></b></p>
      <svg id="kmap" viewBox="0 0 820 560" width="640" height="437"></svg>
    </div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · what we show</p>
  <h2>Fair on average; no setting always wins</h2>
  <div class="cards">
    <div class="card top">{keep_vis()}<p class="ctitle">Kept, on average</p></div>
    <div class="card top">{best_vis()}<p class="ctitle">Best setting depends on the population</p></div>
  </div>
</section>''')

S('''<section class="slide dark">
  <p class="eyebrow">Towards D5.3</p>
  <h2>Let's discuss</h2>
  <div class="rows ruled">
    <div class="row"><span class="n">1</span><p>What suggestions do we want to give?<span class="sub">lottery or delegation · how many areas · panel rules</span><span class="sub">and beyond: e.g., how sticky should delegations be?</span></p></div>
    <div class="row"><span class="n">2</span><p>Experiments: which variants, and where?<span class="sub">Wikipedia · Consenz · DAOs</span></p></div>
  </div>
</section>''')

slides.append(TITLE)

STYLE = '''<style>
.paper { font-size: 34px; color: var(--gray); margin-top: -24px; }
.data { position: absolute; top: 56px; right: 128px; width: 560px; font-size: 28px; line-height: 1.35; color: var(--gray);
  border: 2px solid var(--gray-light); border-radius: 18px; padding: 18px 24px; }
.sub { display: block; font-size: 32px; color: var(--gray-light); margin-top: 4px; }
.knobs { display: flex; gap: 56px; align-items: flex-start; margin-block: auto; }
.kcol { display: flex; flex-direction: column; gap: 8px; }
.klab { font-size: 36px; font-weight: 700; display: flex; align-items: center; gap: 14px; }
.klab b { color: var(--orange); }
.keys { margin-left: auto; font-size: 26px; font-weight: 700; color: var(--gray); display: flex; align-items: center; gap: 6px; }
.keys i { font-style: normal; width: 40px; height: 40px; border-radius: 50%; border: 3px solid var(--gray-light);
  display: inline-flex; align-items: center; justify-content: center; font-size: 24px; color: var(--dark); }
.knobs input[type=range] { width: 700px; height: 36px; accent-color: var(--orange); cursor: pointer; }
.khint { display: flex; justify-content: space-between; width: 700px; font-size: 26px; color: var(--gray); margin-top: -4px; }
.kacc { font-size: 48px; font-weight: 700; }
.kacc b { color: var(--orange); }
#kmap { cursor: crosshair; }
.card svg { width: 100%; height: auto; }
.ctitle { font-size: 40px !important; font-weight: 800; text-align: center; }
</style>'''

SCRIPT = '''<script>
(function () {
  // paper example (Prop. "explicit intermediate improvement"): one delegate with support W, competence p;
  // m delegates with support 1, competence q; panel of k; parameter b in [0, 1]
  const W = 5, m = 10, g = 11, p = 0.8, q = 0.6;
  const OR = '#F7941D', GR = '#5F6368', DK = '#26282C';
  const psi = (x) => (x > 1e-9 ? 1 : x < -1e-9 ? 0 : 0.5);
  const binom = (a, c) => { let r = 1; for (let i = 1; i <= c; i++) r = r * (a - c + i) / i; return r; };
  // chances to be drawn: proportional to support^(1-b), capped at 1, summing to k
  function incl(b, k) {
    if (k >= g) return [1, 1];
    const u = Math.pow(W, 1 - b);
    return (k - 1) * u <= m ? [k * u / (u + m), k / (u + m)] : [1, (k - 1) / m];
  }
  function C(l, r) {  // the big delegate is drawn, with l small ones; her relative weight is r
    let t = 0;
    for (let j = 0; j <= l; j++)
      t += binom(l, j) * Math.pow(q, j) * Math.pow(1 - q, l - j) * (p * psi(r + 2 * j - l) + (1 - p) * psi(-r + 2 * j - l));
    return t;
  }
  function M(k) {  // k small delegates, equal weights
    let t = 0;
    for (let j = 0; j <= k; j++) t += binom(k, j) * Math.pow(q, j) * Math.pow(1 - q, k - j) * psi(2 * j - k);
    return t;
  }
  function acc(b, k) {
    if (k >= g) return C(m, W);
    const [pH, pL] = incl(b, k), r = W * pL / pH;  // weight when drawn = support / chance
    return pH * C(k - 1, r) + (1 - pH) * M(k);
  }
  const kb = document.getElementById('kb'), ks = document.getElementById('ks');
  const bars = document.getElementById('kbars'), map = document.getElementById('kmap');
  // line chart: accuracy along the second knob, for the current panel size (fixed axis)
  const X0 = 130, X1 = 800, Y0 = 470, Y1 = 30, LO = 0.6, HI = 0.85, NX = 201;
  const X = (t) => X0 + t * (X1 - X0), Y = (v) => Y0 - (v - LO) / (HI - LO) * (Y0 - Y1);
  const T = (x, y, s, size, fill, anchor, weight, extra) =>
    `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor || 'middle'}" font-weight="${weight || 400}" font-family="Heebo, Arial, sans-serif" ${extra || ''}>${s}</text>`;
  let h = `<line x1="${X0}" y1="${Y0}" x2="${X1}" y2="${Y0}" stroke="${DK}" stroke-width="3"/>`;
  h += `<line x1="${X0}" y1="${Y0}" x2="${X0}" y2="${Y1}" stroke="${DK}" stroke-width="3"/>`;
  for (const v of [0.6, 0.7, 0.8]) h += T(X0 - 14, Y(v) + 10, Math.round(100 * v) + '%', 28, GR, 'end');
  const ld = acc(0, g);
  h += `<line x1="${X0}" y1="${Y(ld)}" x2="${X1}" y2="${Y(ld)}" stroke="${GR}" stroke-width="3" stroke-dasharray="10 8"/>`;
  h += T(X1, Y(ld) - 12, 'everyone votes', 26, GR, 'end');
  h += T(X0, Y0 + 40, '0', 30, GR) + T(X1, Y0 + 40, '1', 30, GR) + T((X0 + X1) / 2, Y0 + 80, 'support buys chance (0) or weight (1)', 32, GR, 'middle', 700);
  h += '<polyline id="kline" fill="none" stroke="' + OR + '" stroke-width="6" stroke-linejoin="round"/>';
  h += '<g id="kstar"></g><circle id="kdot" r="16" fill="' + DK + '"/>';
  map.innerHTML = h;
  const dot = map.querySelector('#kdot'), line = map.querySelector('#kline'), star = map.querySelector('#kstar');
  let lastK = -1;
  function drawLine(k) {
    const vs = [...Array(NX).keys()].map(i => acc(i / (NX - 1), k));
    line.setAttribute('points', vs.map((v, i) => `${X(i / (NX - 1)).toFixed(1)},${Y(v).toFixed(1)}`).join(' '));
    const hi = Math.max(...vs), lo = Math.min(...vs), bi = vs.indexOf(hi);
    star.innerHTML = hi - lo < 1e-9 ? '' : T(X(bi / (NX - 1)), Y(hi) - 14, '★', 44, OR, 'middle', 700);
  }
  function update() {
    const k = parseFloat(kb.value), s = parseFloat(ks.value);
    document.getElementById('kbv').textContent = k >= g ? g + ' (everyone)' : String(k);
    document.getElementById('ksv').textContent = s.toFixed(2);
    const pi = incl(s, k), e = [W / pi[0] * pi[1], 1];  // weight when drawn, relative to a small delegate
    let out = '';
    const unit = 30, base = 190;
    [['the big one', OR], ['each small one', GR]].forEach(([name, col], i) => {
      const x = 60 + i * 260, hh = e[i] * unit;
      out += `<rect x="${x}" y="${base - hh}" width="140" height="${hh}" rx="8" fill="${col}"/>`;
      out += T(x + 70, base - hh - 12, e[i].toFixed(1), 28, DK, 'middle', 700);
      out += T(x + 70, base + 34, Math.round(100 * pi[i]) + '%', 26, GR);
      out += T(x + 70, base + 66, name, 26, GR);
    });
    out += T(700, 24, 'bar: weight when drawn', 26, GR, 'end') + T(700, 58, '%: chance to be drawn', 26, GR, 'end');
    bars.innerHTML = out;
    document.getElementById('kacc').textContent = (100 * acc(s, k)).toFixed(1) + '%';
    if (k !== lastK) { drawLine(k); lastK = k; }
    dot.setAttribute('cx', X(s));
    dot.setAttribute('cy', Y(acc(s, k)));
  }
  kb.addEventListener('input', update); ks.addEventListener('input', update);
  // mouse use should not keep focus on a slider
  [kb, ks].forEach(el => el.addEventListener('change', () => el.blur()));
  map.addEventListener('click', (ev) => {
    const r = map.getBoundingClientRect(), sx = (ev.clientX - r.left) / r.width * 820, sy = (ev.clientY - r.top) / r.height * 560;
    if (sx < X0 || sx > X1 || sy < Y1 || sy > Y0) return;
    ks.value = ((sx - X0) / (X1 - X0)).toFixed(2);
    update();
  });
  // keys 1/2 move the panel-size slider, 3/4 the other one (arrows stay for slides)
  const slide = kb.closest('.slide');
  document.addEventListener('keydown', (e) => {
    if (!slide.classList.contains('active') || e.metaKey || e.ctrlKey || e.altKey) return;
    const step = (el, d) => { el.value = (parseFloat(el.value) + d * parseFloat(el.step)).toString(); update(); };
    if (e.key === '1') step(kb, -1); else if (e.key === '2') step(kb, 1);
    else if (e.key === '3') step(ks, -1); else if (e.key === '4') step(ks, 1);
  });
  update();
})();
</script>'''

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
