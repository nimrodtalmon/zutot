#!/usr/bin/env python3
"""Builds slides/variants-of-liquid-representation/index.html (inline SVG visuals, one interactive slide)."""
import math
import os

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'index.html')
OR, DK, GR, GL, CARD, PALE, LT = '#F7941D', '#26282C', '#5F6368', '#B9BCC1', '#FDFDFB', '#FCE8D2', '#F3F3F1'
GREEN, GOLD, BLUE = '#3E9B4F', '#E2B42B', '#3A7BC8'
FONT = 'font-family="Heebo, Arial, sans-serif"'

PAPER_LOP = '“Lot or Proxy? Representation in Sortition and Liquid Democracy” · with Eyal Briman'
PAPER_TOPIC = '“Topic Bundling for Epistemic Committee Design” · with Davide Grossi'
PAPER_SAMPLED = 'Sampled liquid democracy · with Eyal Briman'


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


def setting_vis():
    """Population -> lottery or delegation -> committee -> decision, compared with direct democracy."""
    W, H = 1640, 560
    b = ''
    pop = [(90 + 70 * (k % 3), 170 + 70 * (k // 3)) for k in range(12)]
    for x, y in pop:
        b += f'<circle cx="{x}" cy="{y}" r="20" fill="{DK}"/>'
    b += text(160, 140, 'citizens', 32, GR)
    # lottery branch
    b += arrow(290, 250, 400, 160, GR)
    b += dice(450, 150, 70)
    b += text(450, 80, 'lottery', 34, DK, weight=800)
    for k in range(3):
        b += f'<circle cx="{570+60*k}" cy="150" r="22" fill="{OR}"/>'
    b += text(630, 215, 'equal weights', 28, GR)
    # delegation branch
    b += arrow(290, 340, 400, 420, GR)
    b += arrow(420, 420, 500, 420, OR, 5)
    b += text(450, 520, 'delegation', 34, DK, weight=800)
    for k, r in enumerate((14, 34, 22)):
        b += f'<circle cx="{570+65*k}" cy="420" r="{r}" fill="{OR}"/>'
    b += text(635, 490, 'weighted', 28, GR)
    # decisions
    b += arrow(760, 150, 850, 260, GR) + arrow(760, 420, 850, 300, GR)
    b += box(980, 280, 'decision', 240)
    b += box(1450, 280, 'direct democracy', 340, 96, PALE, OR, 34)
    b += text(1188, 236, 'how close?', 32, OR, weight=800)
    b += f'<line x1="1110" y1="280" x2="1265" y2="280" stroke="{OR}" stroke-width="5" stroke-dasharray="8 8"/>'
    return svg(W, H, b)


def findings_vis():
    W, H = 1640, 640
    b = ''

    def row(y, label, dots, verdict, deleg):
        o = text(20, y + 12, label, 40, DK, 'start', weight=700)
        o += dots
        col = OR if deleg else GR
        o += chip(1430, y, verdict, col, DK if deleg else '#fff', w=360, size=32)
        return o

    def line_dots(y, a):
        x0, x1 = 480, 1150
        o = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
        for p in (0, a, .5, 1 - a, 1):
            o += f'<circle cx="{x0+p*(x1-x0):.1f}" cy="{y}" r="20" fill="{DK}"/>'
        return o

    def committee(y, n):
        return ''.join(f'<circle cx="{500+56*k}" cy="{y}" r="18" fill="{OR}"/>' for k in range(n))

    b += text(20, 40, 'It depends on the population', 36, GR, 'start', weight=800)
    b += row(115, 'Polarized', line_dots(115, .05), 'lottery closer', False)
    b += row(215, 'Moderate', line_dots(215, .4), 'delegation closer', True)
    b += text(20, 360, 'New: it also depends on the committee size', 36, GR, 'start', weight=800)
    b += f'<rect x="{20+790}" y="328" width="280" height="44" rx="22" fill="{PALE}"/>' + text(20 + 930, 359, 'close-knit pairs', 26, DK, weight=700)
    b += row(445, 'Small committee', committee(445, 3), 'lottery closer', False)
    b += row(545, 'Large committee', committee(545, 11), 'delegation closer', True)
    return svg(W, H, b)


TOPICS = [('Health', GREEN), ('Transport', BLUE), ('Budget', GOLD)]


def onedel_vis():
    W, H = 1640, 460
    b = head(200, 200, 40, DK)
    b += arrow(270, 230, 640, 230, GR)
    b += head(720, 200, 40, GR)
    for k, (name, col) in enumerate(TOPICS):
        y = 90 + k * 130
        b += chip(1060, y, name, col if k == 0 else GL, '#fff' if k == 0 else DK, w=260, size=34)
        b += check(1240, y, 26) if k == 0 else text(1240, y + 18, '?', 56, GR, weight=800)
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


def chart_vis():
    """Schematic: accuracy gain vs number of areas, 12 topics in 4 groups of related topics."""
    W, H = 1640, 680
    X0, X1, Y0, Y1 = 200, 1180, 560, 80
    m = 12
    X = lambda b: X0 + b / m * (X1 - X0)
    Y = lambda f: Y0 - f * (Y0 - Y1)
    vals = [.55, .76, .89, .97, .975, .98, .985, .99, .993, .996, .998, 1]
    b = text(W - 20, 30, 'schematic', 26, GR, 'end')
    b += f'<line x1="{X0}" y1="{Y0}" x2="{X1+30}" y2="{Y0}" stroke="{DK}" stroke-width="4"/>'
    b += f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1-30}" stroke="{DK}" stroke-width="4"/>'
    for t, lab in ((0, '0'), (4, '4'), (12, '12')):
        b += text(X(t), Y0 + 44, lab, 30, GR)
    b += text((X0 + X1) / 2, Y0 + 80, 'number of areas (12 topics)', 32, GR)
    b += text(X0 - 20, Y0 + 10, '0', 30, GR, 'end') + text(X0 - 20, Y1 + 10, 'max', 30, GR, 'end')
    b += text(70, (Y0 + Y1) / 2, 'accuracy gain', 32, GR, extra=f'transform="rotate(-90 70 {(Y0+Y1)/2})"')
    # guarantee
    b += (f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(m):.1f}" y2="{Y(1):.1f}" stroke="{GR}" '
          f'stroke-width="5" stroke-dasharray="14 10"/>')
    b += text(X(7.4), Y(7.4 / m) + 52, 'guaranteed', 34, GR, 'start', weight=700)
    # curve
    pts = ' '.join(f'{X(k+1):.1f},{Y(v):.1f}' for k, v in enumerate(vals))
    b += f'<polyline points="{pts}" fill="none" stroke="{OR}" stroke-width="8" stroke-linejoin="round"/>'
    for k, v in enumerate(vals):
        b += f'<circle cx="{X(k+1):.1f}" cy="{Y(v):.1f}" r="9" fill="{OR}"/>'
    b += f'<line x1="{X(4):.1f}" y1="{Y0}" x2="{X(4):.1f}" y2="{Y(.97)+16:.1f}" stroke="{OR}" stroke-width="3" stroke-dasharray="6 8"/>'
    b += text(X1 + 60, Y(1) + 12, 'never goes down', 34, OR, 'start', weight=800)
    b += text(X1 + 60, Y(.62), 'topics in 4 groups:', 32, DK, 'start', weight=700)
    b += text(X1 + 60, Y(.62) + 42, '4 areas give', 32, DK, 'start', weight=700)
    b += text(X1 + 60, Y(.62) + 84, 'most of the gain', 32, DK, 'start', weight=700)
    return svg(W, H, b)


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
        fill = OR if (mode == 'panel' and on) else DK
        g += f'<circle cx="{x}" cy="120" r="{r:.1f}" fill="{fill}"/>' + text(x, 132, str(w), 34, '#fff' if fill == DK else DK, weight=800)
        b += f'<g opacity="{op}">{g}</g>'
    if mode == 'problem':
        for k in range(4):
            b += (f'<rect x="{1470+k*12}" y="{60+k*14}" width="130" height="170" rx="12" fill="{CARD}" stroke="{DK}" stroke-width="4"/>')
        b += text(1571, 165, 'issue', 30, DK, weight=700)
        b += text(1535, 300, 'every', 30, GR, weight=700) + text(1535, 340, 'issue', 30, GR, weight=700)
    else:
        b += dice(1530, 140, 110)
        b += text(1530, 260, 'per issue', 30, GR, weight=700)
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
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Recall · D5.1</p>
  <h2>A committee by lottery, or by delegation?</h2>
  <p class="paper">Paper: {PAPER_LOP}</p>
  <div style="margin-block:auto">{setting_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Recall · D5.1</p>
  <h2>Which is closer to direct democracy?</h2>
  <div style="margin-block:auto">{findings_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1 · the problem</p>
  <h2>One delegate for everything?</h2>
  <p class="paper">A citizen may trust different people on different topics</p>
  <div style="margin-block:auto">{onedel_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 1 · the approach</p>
  <h2>Delegate per area</h2>
  <p class="paper">Paper: {PAPER_TOPIC}</p>
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
  <div style="margin-block:auto">{chart_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · the problem</p>
  <h2>Representatives must vote on everything</h2>
  <p class="paper">Some may be busy, absent, or vote without attention</p>
  <div style="margin-block:auto">{forest_vis('problem')}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">Variant 2 · the approach</p>
  <h2>Per issue, draw a small panel</h2>
  <p class="paper">Paper: {PAPER_SAMPLED}</p>
  <p class="paper" style="margin-top:-36px">Large representatives are drawn more often; drawn votes are scaled up to stand for the others</p>
  <div style="margin-block:auto">{forest_vis('panel')}</div>
</section>''')

S('''<section class="slide accent center">
  <p class="big">Like a poll: a random sample tracks the whole</p>
  <h1 class="huge">≈ 160</h1>
  <p class="big">panel members match a 60/40 full vote at least 95% of the time</p>
  <p class="big" style="font-weight:700">whatever the population size</p>
</section>''')

KNOBS = '''
<section class="slide light">
  <p class="eyebrow">Variant 2 · two knobs</p>
  <h2>Panel size, and how much delegations count</h2>
  <p class="paper">Example: one representative holds 8 citizens and is right 80% of the time; four hold 1 and are right 60%</p>
  <div class="interactive knobs">
    <div class="kcol">
      <label>Panel size <b id="kbv"></b></label>
      <input type="range" id="kb" min="1" max="5" step="0.1" value="5">
      <label>Delegation strength <b id="ksv"></b></label>
      <input type="range" id="ks" min="0" max="1" step="0.01" value="1">
      <p class="kacc">Accuracy <b id="kacc"></b></p>
      <svg id="kbars" viewBox="0 0 700 230" width="700" height="230"></svg>
    </div>
    <div class="kcol">
      <svg id="kmap" viewBox="0 0 820 600" width="640" height="468"></svg>
    </div>
  </div>
</section>'''
S(KNOBS)

S('''<section class="slide light">
  <p class="eyebrow">Variant 2</p>
  <h2>The price of dampening</h2>
  <div class="cards">
    <div class="card top"><h3>Unequal citizens</h3><p>Below strength 1, it is no longer one person, one vote</p></div>
    <div class="card top"><h3>Fake identities pay</h3><p>Below strength 1, splitting into several identities adds weight</p></div>
    <div class="card top"><h3>Small gains</h3><p>In-between strengths can beat both ends in accuracy, but only by a little</p></div>
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
.knobs { display: flex; gap: 64px; align-items: flex-start; margin-block: auto; }
.kcol { display: flex; flex-direction: column; gap: 8px; }
.knobs label { font-size: 36px; font-weight: 700; }
.knobs label b { color: var(--orange); margin-left: 12px; }
.knobs input[type=range] { width: 700px; height: 36px; accent-color: var(--orange); cursor: pointer; margin-bottom: 4px; }
.kacc { font-size: 44px; }
.kacc b { color: var(--orange); }
#kmap { cursor: crosshair; }
</style>'''

SCRIPT = '''<script>
(function () {
  const W = [8, 1, 1, 1, 1], P = [0.8, 0.6, 0.6, 0.6, 0.6], n = 5;
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
  // heatmap
  const NX = 50, NY = 40, X0 = 110, X1 = 800, Y0 = 470, Y1 = 20;
  const grid = [];
  let lo = 1, hi = 0;
  for (let a = 0; a < NX; a++) for (let b = 0; b < NY; b++) {
    const s = a / (NX - 1), k = 1 + 4 * b / (NY - 1), v = acc(s, k);
    grid.push([a, b, v]); lo = Math.min(lo, v); hi = Math.max(hi, v);
  }
  const mix = (t) => {
    const c0 = [243, 243, 241], c1 = [247, 148, 29];
    return 'rgb(' + c0.map((x, j) => Math.round(x + (c1[j] - x) * t)).join(',') + ')';
  };
  const cw = (X1 - X0) / NX, ch = (Y0 - Y1) / NY;
  let h = '';
  for (const [a, b, v] of grid)
    h += `<rect x="${(X0 + a * cw).toFixed(1)}" y="${(Y0 - (b + 1) * ch).toFixed(1)}" width="${(cw + .6).toFixed(1)}" height="${(ch + .6).toFixed(1)}" fill="${mix((v - lo) / (hi - lo))}"/>`;
  const T = (x, y, s, size, fill, anchor, weight, extra) =>
    `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor || 'middle'}" font-weight="${weight || 400}" font-family="Heebo, Arial, sans-serif" ${extra || ''}>${s}</text>`;
  h += `<rect x="${X0}" y="${Y1}" width="${X1 - X0}" height="${Y0 - Y1}" fill="none" stroke="${GR}" stroke-width="2"/>`;
  h += T(X0, Y0 + 40, '0', 28, GR) + T(X1, Y0 + 40, '1', 28, GR) + T((X0 + X1) / 2, Y0 + 80, 'delegation strength', 30, GR, 'middle', 700);
  h += T(X0 - 16, Y0 + 8, '1', 28, GR, 'end') + T(X0 - 16, Y1 + 20, '5', 28, GR, 'end');
  h += T(40, (Y0 + Y1) / 2, 'panel size', 30, GR, 'middle', 700, `transform="rotate(-90 40 ${(Y0 + Y1) / 2})"`);
  h += T(X1, Y0 + 120, `accuracy: ${(100 * lo).toFixed(0)}% (light) to ${(100 * hi).toFixed(1)}% (orange)`, 26, GR, 'end');
  h += '<circle id="kdot" r="16" fill="none" stroke="' + DK + '" stroke-width="6"/>';
  map.innerHTML = h;
  const dot = map.querySelector('#kdot');
  function update() {
    const k = parseFloat(kb.value), s = parseFloat(ks.value);
    document.getElementById('kbv').textContent = k >= 5 ? '5 (everyone)' : k.toFixed(1);
    document.getElementById('ksv').textContent = s.toFixed(2);
    const [e, pi] = incl(s, k);
    let g = '';
    const unit = 20, base = 190;
    for (let i = 0; i < n; i++) {
      const x = 40 + i * 130, hh = e[i] * unit;
      g += `<rect x="${x}" y="${base - hh}" width="80" height="${hh}" rx="8" fill="${i ? GR : OR}"/>`;
      g += T(x + 40, base - hh - 14, e[i].toFixed(1), 28, DK, 'middle', 700);
      g += T(x + 40, base + 32, Math.round(100 * pi[i]) + '%', 26, GR);
    }
    g += T(690, 24, 'bar: weight', 26, GR, 'end') + T(690, 58, '%: chance to be drawn', 26, GR, 'end');
    bars.innerHTML = g;
    document.getElementById('kacc').textContent = (100 * acc(s, k)).toFixed(1) + '%';
    dot.setAttribute('cx', X0 + s * (X1 - X0));
    dot.setAttribute('cy', Y0 - (k - 1) / 4 * (Y0 - Y1));
  }
  kb.addEventListener('input', update); ks.addEventListener('input', update);
  map.addEventListener('click', (ev) => {
    const r = map.getBoundingClientRect(), sx = (ev.clientX - r.left) / r.width * 820, sy = (ev.clientY - r.top) / r.height * 620;
    if (sx < X0 || sx > X1 || sy < Y1 || sy > Y0) return;
    ks.value = ((sx - X0) / (X1 - X0)).toFixed(2);
    kb.value = (1 + 4 * (Y0 - sy) / (Y0 - Y1)).toFixed(1);
    update();
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
