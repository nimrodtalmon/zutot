#!/usr/bin/env python3
"""Builds slides/constitutional-governance/index.html (ADT 2026 talk; inline SVG visuals, one interactive slide)."""
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


# ---------- slide 3: kinds of decisions ----------
def icon(kind):
    W = H = 180
    b = ''
    if kind == 'officers':
        for k, x in enumerate([40, 90, 140]):
            b += head(x, 70, 18, OR if k == 1 else GR)
    elif kind == 'rate':
        b += f'<line x1="20" y1="110" x2="160" y2="110" stroke="{DK}" stroke-width="5" stroke-linecap="round"/>'
        for x in [20, 55, 90, 125, 160]:
            b += f'<line x1="{x}" y1="100" x2="{x}" y2="120" stroke="{DK}" stroke-width="4"/>'
        b += f'<polygon points="110,96 98,72 122,72" fill="{OR}"/>' + text(110, 60, '%', 34, DK, weight=800)
    elif kind == 'budget':
        b += (f'<rect x="20" y="70" width="70" height="56" fill="{OR}"/>'
              f'<rect x="90" y="70" width="45" height="56" fill="{GR}"/>'
              f'<rect x="135" y="70" width="25" height="56" fill="{GL}"/>')
    elif kind == 'priorities':
        for k, w in enumerate([130, 95, 60]):
            y = 40 + k * 40
            b += text(30, y + 22, str(k + 1), 28, DK, weight=800)
            b += f'<rect x="50" y="{y}" width="{w}" height="28" rx="6" fill="{OR if k == 0 else GR}"/>'
    elif kind == 'board':
        for k in range(6):
            x, y = 45 + (k % 3) * 45, 55 + (k // 3) * 60
            on = k in (0, 2, 4)
            b += f'<circle cx="{x}" cy="{y}" r="15" fill="{OR if on else GL}"/>'
    elif kind == 'bylaws':
        b += f'<rect x="45" y="25" width="90" height="125" rx="8" fill="{CARD}" stroke="{DK}" stroke-width="5"/>'
        for k, w in enumerate([60, 60, 40, 60, 50]):
            b += f'<line x1="60" y1="{50+k*20}" x2="{60+w}" y2="{50+k*20}" stroke="{GR}" stroke-width="5" stroke-linecap="round"/>'
    elif kind == 'constitution':
        b += f'<rect x="45" y="25" width="90" height="125" rx="8" fill="{PALE}" stroke="{OR}" stroke-width="6"/>'
        for k, w in enumerate([60, 60, 40]):
            b += f'<line x1="60" y1="{50+k*20}" x2="{60+w}" y2="{50+k*20}" stroke="{GR}" stroke-width="5" stroke-linecap="round"/>'
        b += f'<circle cx="112" cy="122" r="16" fill="{OR}"/>'
    return svg(W, H, b)


KINDS = [('officers', 'Officers'), ('rate', 'A rate'), ('budget', 'A budget'), ('priorities', 'Priorities'),
         ('board', 'A board'), ('bylaws', 'Bylaws'), ('constitution', 'The constitution')]


def kinds_vis():
    cards = ''.join(f'<div class="kind">{icon(k)}<p>{lab}</p></div>' for k, lab in KINDS)
    return f'<div class="kinds">{cards}</div>'


# ---------- slide 4: one decision on a line ----------
VOTES_1D = [5, 14, 16, 18, 25]
TODAY = 10


def line_vis():
    W, H = 1640, 330
    x0, x1, lo, hi = 80, 1560, 0, 30
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    y = 220
    b = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{DK}" stroke-width="5" stroke-linecap="round"/>'
    for v in range(0, 31, 5):
        b += f'<line x1="{X(v)}" y1="{y-12}" x2="{X(v)}" y2="{y+12}" stroke="{DK}" stroke-width="4"/>'
        b += text(X(v), y + 52, f'{v}%', 30, GR)
    # today
    b += f'<rect x="{X(TODAY)-16}" y="{y-16}" width="32" height="32" fill="{GR}"/>'
    b += text(X(TODAY), y - 40, 'today', 32, GR, weight=700)
    for v in VOTES_1D:
        b += head(X(v), 70, 22, OR if v == 16 else DK)
    b += text(X(16), 30, 'median member', 30, DK, weight=800)
    b += (f'<line x1="{X(16)}" y1="{y-70}" x2="{X(16)}" y2="{y-20}" stroke="{OR}" stroke-width="6"/>'
          f'<circle cx="{X(16)}" cy="{y}" r="18" fill="{OR}"/>')
    b += text(X(16) + 30, y - 30, 'adopted', 32, OR, 'start', weight=800)
    return svg(W, H, b)


# ---------- slide 8: gap closed by the pairwise heuristic (paper, Table 2, 2D Euclidean, "Combined") ----------
GAP = [(5, 27), (21, 76), (51, 94)]


def gap_vis():
    W, H = 1100, 560
    x0, y0, y1 = 170, 460, 60
    Y = lambda p: y0 - p / 100 * (y0 - y1)
    b = ''
    for p in (0, 50, 100):
        b += f'<line x1="{x0}" y1="{Y(p)}" x2="1060" y2="{Y(p)}" stroke="{GL}" stroke-width="2"/>'
        b += text(x0 - 20, Y(p) + 10, f'{p}%', 30, GR, 'end')
    for k, (n, p) in enumerate(GAP):
        x = 260 + k * 290
        b += f'<rect x="{x}" y="{Y(p)}" width="160" height="{y0-Y(p)}" rx="10" fill="{OR}"/>'
        b += text(x + 80, Y(p) - 18, f'{p}%', 40, DK, weight=800)
        b += text(x + 80, y0 + 44, str(n), 34, DK, weight=700)
    b += text(615, y0 + 94, 'number of members', 32, GR, weight=700)
    b += text(40, 260, 'share of the gap closed', 32, GR, weight=700, extra='transform="rotate(-90 40 260)"')
    return svg(W, H, b)


# ---------- slides ----------
TITLE = '''
<section class="slide dark center">
  <p class="eyebrow">Paper · ADT 2026</p>
  <h1>Constitutional Governance<br>in Metric Spaces</h1>
  <p class="ref" style="bottom:128px;font-size:32px">Ehud Shapiro and Nimrod Talmon</p>
  <p class="ref">LSE and Weizmann Institute · Ben-Gurion University · November 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>'''

slides = [TITLE]
S = slides.append

S('''<section class="slide dark middle">
  <h1>The Grassroots Project</h1>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">The problem</p>
  <h2>A community decides many kinds of things</h2>
  <p class="paper">Each is a different kind of object, and there is no single process for all of them</p>
  {kinds_vis()}
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">How a decision is made</p>
  <h2>Example: five members set a rate; today it is 10%</h2>
  <div class="rows ruled steps">
    <div class="row"><span class="n">1</span><p>Each member votes for their ideal point</p></div>
    <div class="row"><span class="n">2</span><p>Anyone may add a compromise that a majority prefers to today</p></div>
    <div class="row"><span class="n">3</span><p>Score: how much the median member gains; best one wins, else today stays</p></div>
  </div>
  <div>{line_vis()}</div>
</section>''')

ROWS = [('Officers', 'a candidate, or vacant', 'same or not', '½'),
        ('A rate', 'a number', 'difference', '½'),
        ('A budget', 'a split', 'Euclidean', '½'),
        ('Priorities', 'a ranking', 'swaps', '½'),
        ('A board', 'a set of people', 'people that differ', '½'),
        ('Bylaws', 'a text', 'edits', '½'),
        ('The constitution', 'these parameters', 'per parameter', '⅔')]
rows = ''.join(f'<tr{" class=on" if k == len(ROWS) - 1 else ""}><th class="rh">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
               for k, (a, b, c, d) in enumerate(ROWS))
S(f'''<section class="slide light">
  <p class="eyebrow">The constitution</p>
  <h2>For each kind of decision, it sets the rules</h2>
  <p class="paper">The constitution is amended the same way, with a higher majority</p>
  <table class="t ct"><tr><th class="rh"></th><th>Options</th><th>Distance</th><th>Majority (e.g.)</th></tr>{rows}</table>
</section>''')

S('''<section class="slide light">
  <p class="eyebrow">Live</p>
  <h2>A compromise can beat every member's point</h2>
  <p class="paper">Two issues at once: options are points in the plane. Drag the orange proposal.</p>
  <div class="interactive demo">
    <svg id="dplane" viewBox="0 0 640 640" width="600" height="600"></svg>
    <div class="dcol">
      <p class="dlab">Score (median member's gain)</p>
      <p class="dnum" id="dscore"></p>
      <p class="dlab"><span class="sw g"></span> prefers it to today: <b id="dsup"></b> of 5</p>
      <p class="dlab muted">Best member's own point: <b id="dpeak"></b></p>
    </div>
  </div>
</section>''')

S('''<section class="slide light">
  <p class="eyebrow">What we show</p>
  <h2>Guarantees</h2>
  <div class="cards">
    <div class="card top"><p class="label">Always a decision</p><p>Proposals are compared with today, not with each other: no cycles</p></div>
    <div class="card top"><p class="label">Polynomial time</p><p>In all seven settings, also where the classic optimum is NP-hard (rankings, boards, bylaws)</p></div>
    <div class="card top"><p class="label">On a line</p><p>The median member's point is optimal, and honest voting is a dominant strategy</p></div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">What we show · beyond a line</p>
  <h2>A simple compromise closes most of the gap</h2>
  <p class="paper">Simulations in 2D: blend two existing proposals, keep the best blend</p>
  <div style="margin-block:auto;align-self:center">{gap_vis()}</div>
</section>''')

slides.append(TITLE)

STYLE = '''<style>
.paper { font-size: 34px; color: var(--gray); margin-top: -24px; }
.kinds { display: flex; gap: 20px; margin-block: auto; }
.kind { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; background: var(--card);
  border: 1px solid var(--gray-light); border-radius: 16px; padding: 24px 8px; }
.kind:last-child { border: 4px solid var(--orange); }
.card .label { font-size: 44px; color: var(--dark) !important; }
.card p { font-size: 40px; }
.kind p { font-size: 32px; font-weight: 700; text-align: center; }
.steps { margin-block: 0; }
.steps .row { padding: 10px 0; }
.steps .row .n { font-size: 52px; }
.steps .row p { font-size: 40px; }
table.ct { margin-block: auto; font-size: 34px; border-spacing: 10px 6px; margin-top: -16px; }
table.ct th.rh { font-size: 36px; padding-right: 32px; }
table.ct td { padding: 6px 22px; font-weight: 400; }
table.ct td:last-child { font-weight: 800; }
table.ct tr.on td { background: var(--orange-pale); border-color: var(--orange); }
table.ct tr.on th { color: var(--orange); }
.demo { display: flex; gap: 72px; align-items: center; margin-block: auto; }
#dplane { cursor: grab; touch-action: none; }
.dcol { display: flex; flex-direction: column; gap: 20px; }
.dlab { font-size: 38px; font-weight: 700; display: flex; align-items: center; gap: 14px; }
.dlab b { color: var(--orange); }
.dnum { font-size: 140px; font-weight: 800; color: var(--orange); line-height: 1; }
.sw { width: 30px; height: 30px; border-radius: 50%; display: inline-block; }
.sw.g { background: #3E9B4F; }
</style>'''

# the 2D demo: five members on a pentagon, today at the bottom; generalised median at threshold 1/2
SCRIPT = '''<script>
(function () {
  const svg = document.getElementById('dplane');
  const U = 60, OFF = 20;                        // plane [0,10]^2 -> 600px, y up
  const P = (x, y) => [OFF + x * U, OFF + (10 - y) * U];
  const V = [0, 1, 2, 3, 4].map(k => { const a = (90 + 72 * k) * Math.PI / 180; return [5 + 3.5 * Math.cos(a), 5.5 + 3.5 * Math.sin(a)]; });
  const S0 = [5, 1];
  const d = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
  const gains = p => V.map(v => d(v, S0) - d(v, p));
  const score = p => gains(p).slice().sort((a, b) => b - a)[2];
  const peak = Math.max(...V.map(score));
  let q = V.find(v => score(v) === peak).slice();   // start at the best member's own point
  const T = (x, y, s, sz, f, w) => `<text x="${x}" y="${y}" font-size="${sz}" fill="${f}" text-anchor="middle" font-weight="${w}" font-family="Heebo, Arial, sans-serif">${s}</text>`;
  function draw() {
    const g = gains(q);
    let h = `<rect x="${OFF}" y="${OFF}" width="600" height="600" rx="12" fill="#FDFDFB" stroke="#B9BCC1" stroke-width="2"/>`;
    const [sx, sy] = P(...S0);
    h += `<rect x="${sx - 16}" y="${sy - 16}" width="32" height="32" fill="#5F6368"/>` + T(sx, sy + 50, 'today', 30, '#5F6368', 700);
    V.forEach((v, k) => {
      const [x, y] = P(...v), on = g[k] > 0, c = on ? '#3E9B4F' : '#B9BCC1';
      h += `<circle cx="${x}" cy="${y - 10}" r="18" fill="${c}"/><path d="M${x - 29} ${y + 37} a29 29 0 0 1 58 0 Z" fill="${c}"/>`;
    });
    const [qx, qy] = P(...q);
    h += `<circle cx="${qx}" cy="${qy}" r="26" fill="#F7941D" stroke="#26282C" stroke-width="4"/>`;
    svg.innerHTML = h;
    const sc = score(q);
    document.getElementById('dscore').textContent = sc > 0 ? sc.toFixed(1) : 'not adopted';
    document.getElementById('dscore').style.fontSize = sc > 0 ? '' : '72px';
    document.getElementById('dsup').textContent = g.filter(x => x > 0).length;
  }
  document.getElementById('dpeak').textContent = peak.toFixed(1);
  let drag = false;
  const at = ev => { const r = svg.getBoundingClientRect();
    const x = ((ev.clientX - r.left) / r.width * 640 - OFF) / U, y = 10 - ((ev.clientY - r.top) / r.height * 640 - OFF) / U;
    q = [Math.max(0, Math.min(10, x)), Math.max(0, Math.min(10, y))]; draw(); };
  svg.addEventListener('pointerdown', ev => { drag = true; svg.setPointerCapture(ev.pointerId); at(ev); });
  svg.addEventListener('pointermove', ev => { if (drag) at(ev); });
  svg.addEventListener('pointerup', () => { drag = false; });
  draw();
})();
</script>'''

html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Constitutional Governance in Metric Spaces · Nimrod Talmon</title>
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
