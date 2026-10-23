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

    def line_dots(y, a):
        x0, x1 = 480, 1100
        o = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
        for p in (0, a, .5, 1 - a, 1):
            o += f'<circle cx="{x0+p*(x1-x0):.1f}" cy="{y}" r="20" fill="{DK}"/>'
        return o

    def committee(y, n):
        return ''.join(f'<circle cx="{500+52*k}" cy="{y}" r="17" fill="{OR}"/>' for k in range(n))

    b += text(20, 40, 'It depends on the population', 36, GR, 'start', weight=800)
    b += row(115, 'Polarized', line_dots(115, .05), False)
    b += row(215, 'Moderate', line_dots(215, .4), True)
    b += text(20, 330, 'New: more simulations; same main message, in more detail', 36, GR, 'start', weight=800)
    b += text(20, 375, 'e.g., in some populations, committee size matters too', 32, GR, 'start')
    b += row(435, 'Small committee', committee(435, 3), False)
    b += row(535, 'Large committee', committee(535, 11), True)
    return svg(W, H, b)


def mirror_vis():
    W, H = 1640, 520
    cy = 260
    b = (f'<ellipse cx="270" cy="{cy}" rx="180" ry="240" fill="{PALE}" stroke="{GOLD}" stroke-width="18"/>'
         f'<ellipse cx="270" cy="{cy}" rx="148" ry="206" fill="none" stroke="{GOLD}" stroke-width="3"/>'
         + text(270, cy + 58, '?', 170, GOLD, weight=800))
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


CURVES = [  # (OPT(b) - 1/2) / (OPT(12) - 1/2), b = 1..12: planted-cluster experiment of the paper,
    # rerun with its code and settings (n=100, m=12, 4 clusters, 50 reps, seed 20260909)
    ('#FBC07A', [0.807, 0.940, 0.984, 0.997, 0.998, 0.999, 0.999, 1.0, 1.0, 1.0, 1.0, 1.0]),   # Euclidean
    ('#F7941D', [0.796, 0.875, 0.927, 0.969, 0.975, 0.980, 0.985, 0.989, 0.992, 0.995, 0.998, 1.0]),  # Gaussian
    ('#B35F00', [0.779, 0.881, 0.944, 0.995, 0.997, 0.997, 0.998, 0.999, 0.999, 1.0, 1.0, 1.0])]  # Mallows


def gain_vis():
    W, H = 1640, 560
    X0, X1, Y0, Y1 = 260, 1500, 470, 40
    X = lambda b: X0 + (b - 1) / 11 * (X1 - X0)
    Y = lambda v: Y0 - v * (Y0 - Y1)
    o = f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{DK}" stroke-width="3"/>'
    o += f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-10}" stroke="{DK}" stroke-width="3"/>'
    o += f'<line x1="{X(4)}" y1="{Y0}" x2="{X(4)}" y2="{Y1-10}" stroke="{GL}" stroke-width="3" stroke-dasharray="10 8"/>'
    o += text(X(4) + 16, Y(0.08), '4 groups of topics', 30, GR, 'start', weight=700)
    # theorem: b areas keep at least b/12 of the above-coin-flip accuracy
    o += f'<line x1="{X(1)}" y1="{Y(1/12):.1f}" x2="{X(12)}" y2="{Y(1)}" stroke="{DK}" stroke-width="5" stroke-dasharray="14 10"/>'
    o += text(X(9.3), Y(0.6), 'theorem: never below this line', 30, DK, 'start', weight=700)
    for v, lab in ((0, '0%'), (1, '100%')):
        o += text(X0 - 18, Y(v) + 10, lab, 30, GR, 'end')
    for b in (1, 4, 12):
        o += text(X(b), Y0 + 44, str(b), 32, GR)
    o += text((X0 + X1) / 2, Y0 + 86, 'number of areas', 34, DK, weight=700)
    o += text(70, (Y0 + Y1) / 2, 'accuracy above a coin flip', 34, DK, weight=700, extra=f'transform="rotate(-90 70 {(Y0 + Y1) / 2})"')
    o += text(70 + 40, (Y0 + Y1) / 2, '(share of the best possible)', 26, GR, extra=f'transform="rotate(-90 110 {(Y0 + Y1) / 2})"')
    o += text(X(7.5), Y(0.86), 'experiments: one line per kind of population', 30, OR, weight=700)
    for col, c in CURVES:
        pts = ' '.join(f'{X(b+1):.1f},{Y(v):.1f}' for b, v in enumerate(c))
        o += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
        o += ''.join(f'<circle cx="{X(b+1):.1f}" cy="{Y(v):.1f}" r="7" fill="{col}"/>' for b, v in enumerate(c))
    return svg(W, H, o)


def nope_vis():
    W, H = 440, 220
    return svg(W, H, text(220, 128, '1 person, 1 vote', 52, DK, weight=800)
               + f'<line x1="20" y1="170" x2="420" y2="50" stroke="{OR}" stroke-width="14" stroke-linecap="round"/>')


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
  <p class="ref" style="bottom:128px;font-size:32px">Nimrod Talmon · with Eyal Briman and Davide Grossi</p>
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
  <div style="margin-block:auto">{findings_vis()}</div>
</section>''')

S(divider('Variant 1', 'Topic-based delegation',
          '“Topic Bundling for Epistemic Committee Design”',
          'with Davide Grossi and Eyal Briman · 🤞 AAMAS 2027'))

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
  <h2>A few areas go a long way</h2>
  <p class="paper">More areas never lower accuracy; experiments (12 topics in 4 groups) do far better than the guarantee</p>
  <div style="margin-block:auto">{gain_vis()}</div>
</section>''')

S(divider('Variant 2', 'Sortition on top of delegation', 'Sampled liquid democracy',
          'with Eyal Briman · ' + OVEN + ' in the oven'))

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · the problem</p>
  <h2>Representatives must vote on everything</h2>
  <p class="paper">Some may be busy, absent, or vote without attention</p>
  <div style="margin-block:auto">{forest_vis('problem')}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · the approach</p>
  <h2>Draw a small panel</h2>
  <p class="paper">Large representatives are drawn more often; drawn votes are scaled up to stand for the others</p>
  <div style="margin-block:auto">{forest_vis('panel')}</div>
</section>''')

S('''<section class="slide light center">
  <p class="big">Like a poll: a random sample tracks the whole</p>
  <h1 class="huge" style="color:var(--orange)">≈ 160</h1>
  <p class="big">panel members match a 60/40 full vote at least 95% of the time</p>
  <p class="big" style="font-weight:700">whatever the population size</p>
</section>''')

S('''<section class="slide light">
  <p class="eyebrow">Variant 2 · two knobs</p>
  <h2>Panel size, and how much delegations count</h2>
  <p class="paper">Example: representatives hold 8, 4, 2, 1, 1 citizens and are right 80, 70, 65, 60, 60% of the time</p>
  <div class="interactive knobs">
    <div class="kcol">
      <div class="klab">Panel size <b id="kbv"></b> <span class="keys"><i>1</i>◀ ▶<i>2</i></span></div>
      <input type="range" id="kb" min="1" max="5" step="1" value="5">
      <div class="klab">How much delegations count <b id="ksv"></b> <span class="keys"><i>3</i>◀ ▶<i>4</i></span></div>
      <input type="range" id="ks" min="0" max="1" step="0.05" value="1">
      <div class="khint"><span>0: everyone counts 1</span><span>1: full delegation weight</span></div>
      <svg id="kbars" viewBox="0 0 700 250" width="700" height="250"></svg>
    </div>
    <div class="kcol">
      <p class="kacc">Accuracy <b id="kacc"></b></p>
      <svg id="kmap" viewBox="0 0 820 600" width="580" height="424"></svg>
    </div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2</p>
  <h2>The price of counting delegations less</h2>
  <div class="cards">
    <div class="card top">{nope_vis()}</div>
    <div class="card top">{clones_vis()}<p class="ctitle">Fake identities pay</p></div>
    <div class="card top">{small_vis()}<p class="ctitle">Small accuracy gains</p></div>
  </div>
</section>''')

S('''<section class="slide dark">
  <p class="eyebrow">Towards D5.3</p>
  <h2>Let's discuss</h2>
  <div class="rows ruled">
    <div class="row"><span class="n">1</span><p>What suggestions do we want to give?</p></div>
    <div class="row"><span class="n">2</span><p>What would we want implemented?</p></div>
    <div class="row"><span class="n">3</span><p>Other variants worth studying?</p></div>
  </div>
</section>''')

slides.append(TITLE)

STYLE = '''<style>
.paper { font-size: 34px; color: var(--gray); margin-top: -24px; }
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
  const W = [8, 4, 2, 1, 1], P = [0.8, 0.7, 0.65, 0.6, 0.6], n = 5;
  const OR = '#F7941D', GR = '#5F6368', DK = '#26282C';
  function incl(s, k) {
    const e = W.map(w => Math.pow(w, s));
    if (k >= n - 1e-9) return [e, e.map(() => 1)];
    const capped = new Set();
    let thr;
    for (;;) {
      const rest = [...Array(n).keys()].filter(i => !capped.has(i));
      thr = rest.reduce((a, i) => a + e[i], 0) / (k - capped.size);
      const big = rest.filter(i => e[i] >= thr);
      if (!big.length) break;
      capped.add(big.reduce((a, i) => (e[i] > e[a] ? i : a), big[0]));
    }
    return [e, e.map(x => Math.min(1, x / thr))];
  }
  function acc(s, k) {
    const [e, pi] = incl(s, k);
    let tot = 0;
    for (let c = 0; c < 32; c++) {
      let pc = 1;
      for (let i = 0; i < n; i++) pc *= (c >> i & 1) ? P[i] : 1 - P[i];
      for (let z = 0; z < 32; z++) {
        let pz = 1, sc = 0;
        for (let i = 0; i < n; i++) {
          if (z >> i & 1) { pz *= pi[i]; sc += (e[i] / pi[i]) * ((c >> i & 1) ? 1 : -1); }
          else pz *= 1 - pi[i];
        }
        if (pz === 0) continue;
        tot += pc * pz * (sc > 1e-9 ? 1 : Math.abs(sc) <= 1e-9 ? 0.5 : 0);
      }
    }
    return tot;
  }
  const kb = document.getElementById('kb'), ks = document.getElementById('ks');
  const bars = document.getElementById('kbars'), map = document.getElementById('kmap');
  const NX = 41, NY = 5, X0 = 110, X1 = 800, Y0 = 470, Y1 = 20;
  // rows = panel sizes 1..5; colors are normalized within each row, so the best
  // "how much delegations count" for each panel size stands out
  const rows = [];
  for (let b = 0; b < NY; b++) {
    const r = [];
    for (let a = 0; a < NX; a++) r.push(acc(a / (NX - 1), b + 1));
    rows.push(r);
  }
  const STOPS = [[250, 240, 222], [247, 148, 29], [122, 52, 8]];
  const mix = (t) => {
    const [c0, c1, u] = t < .5 ? [STOPS[0], STOPS[1], t * 2] : [STOPS[1], STOPS[2], t * 2 - 1];
    return 'rgb(' + c0.map((x, j) => Math.round(x + (c1[j] - x) * u)).join(',') + ')';
  };
  const cw = (X1 - X0) / NX, ch = (Y0 - Y1) / NY;
  const T = (x, y, s, size, fill, anchor, weight, extra) =>
    `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor || 'middle'}" font-weight="${weight || 400}" font-family="Heebo, Arial, sans-serif" ${extra || ''}>${s}</text>`;
  let h = '';
  rows.forEach((r, b) => {
    const lo = Math.min(...r), hi = Math.max(...r), best = r.indexOf(hi);
    r.forEach((v, a) => {
      h += `<rect x="${(X0 + a * cw).toFixed(1)}" y="${(Y0 - (b + 1) * ch).toFixed(1)}" width="${(cw + .6).toFixed(1)}" height="${(ch + .6).toFixed(1)}" fill="${mix((v - lo) / (hi - lo))}"/>`;
    });
    const bx = Math.min(X0 + (best + .5) * cw, X1 - 18), by = Y0 - (b + .5) * ch;
    h += T(bx, by + 14, '★', 40, '#fff', 'middle', 700);
    h += T(X0 - 16, by + 10, String(b + 1), 30, GR, 'end');
  });
  h += `<rect x="${X0}" y="${Y1}" width="${X1 - X0}" height="${Y0 - Y1}" fill="none" stroke="${GR}" stroke-width="2"/>`;
  h += T(X0, Y0 + 40, '0', 30, GR) + T(X1, Y0 + 40, '1', 30, GR) + T((X0 + X1) / 2, Y0 + 80, 'how much delegations count', 32, GR, 'middle', 700);
  h += T(44, (Y0 + Y1) / 2, 'panel size', 32, GR, 'middle', 700, `transform="rotate(-90 44 ${(Y0 + Y1) / 2})"`);
  h += T(X1, Y0 + 124, 'per row: darker = more accurate · ★ = best', 28, GR, 'end');
  h += '<circle id="kdot" r="22" fill="none" stroke="' + DK + '" stroke-width="6"/>';
  map.innerHTML = h;
  const dot = map.querySelector('#kdot');
  function update() {
    const k = parseFloat(kb.value), s = parseFloat(ks.value);
    document.getElementById('kbv').textContent = k >= 5 ? '5 (everyone)' : String(k);
    document.getElementById('ksv').textContent = s.toFixed(2);
    const [e, pi] = incl(s, k);
    let g = '';
    const unit = 20, base = 200;
    for (let i = 0; i < n; i++) {
      const x = 40 + i * 130, hh = e[i] * unit;
      g += `<rect x="${x}" y="${base - hh}" width="80" height="${hh}" rx="8" fill="${i ? GR : OR}"/>`;
      g += T(x + 40, base - hh - 12, e[i].toFixed(1), 28, DK, 'middle', 700);
      g += T(x + 40, base + 34, Math.round(100 * pi[i]) + '%', 26, GR);
    }
    g += T(700, 24, 'bar: weight', 26, GR, 'end') + T(700, 58, '%: chance to be drawn', 26, GR, 'end');
    bars.innerHTML = g;
    document.getElementById('kacc').textContent = (100 * acc(s, k)).toFixed(1) + '%';
    dot.setAttribute('cx', X0 + s * (X1 - X0));
    dot.setAttribute('cy', Y0 - (k - .5) * ch);
  }
  kb.addEventListener('input', update); ks.addEventListener('input', update);
  // mouse use should not keep focus on a slider
  [kb, ks].forEach(el => el.addEventListener('change', () => el.blur()));
  map.addEventListener('click', (ev) => {
    const r = map.getBoundingClientRect(), sx = (ev.clientX - r.left) / r.width * 820, sy = (ev.clientY - r.top) / r.height * 600;
    if (sx < X0 || sx > X1 || sy < Y1 || sy > Y0) return;
    ks.value = ((sx - X0) / (X1 - X0)).toFixed(2);
    kb.value = String(Math.min(5, 1 + Math.floor((Y0 - sy) / ch)));
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
