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


# ---------- the 2D example (s4, s5): five members, today at the bottom ----------
VOTES = [(5 + 3.5 * math.cos(math.radians(90 + 72 * k)), 5.5 + 3.5 * math.sin(math.radians(90 + 72 * k))) for k in range(5)]
TODAY2 = (5, 1)
COMP = (5, 6.6)


def gains(p):
    return [math.dist(v, TODAY2) - math.dist(v, p) for v in VOTES]


def score(p):
    return sorted(gains(p), reverse=True)[2]


def plane(size, body_fn, axes=True):
    U = size / 10
    P = lambda x, y: (40 + x * U, 10 + (10 - y) * U)
    b = ''
    if axes:
        b += (f'<line x1="40" y1="{10+size}" x2="{40+size}" y2="{10+size}" stroke="{DK}" stroke-width="4"/>'
              f'<line x1="40" y1="{10+size}" x2="40" y2="10" stroke="{DK}" stroke-width="4"/>')
        b += text(40 + size / 2, size + 56, 'membership fee', 30, GR, weight=700)
        b += text(22, 10 + size / 2, 'commission rate', 30, GR, weight=700, extra=f'transform="rotate(-90 22 {10+size/2})"')
    b += body_fn(P)
    return svg(size + 60, size + 70, b)


def member(P, v, fill, cls=''):
    x, y = P(*v)
    c = f' class="{cls}"' if cls else ''
    return f'<g{c}>{head(x, y - 10, 17, fill)}</g>'


def today_mark(P, at, label='today', cls=''):
    x, y = P(*at)
    c = f' class="{cls}"' if cls else ''
    return (f'<g{c}><rect x="{x-15}" y="{y-15}" width="30" height="30" fill="{GR}"/>'
            + text(x, y + 48, label, 28, GR, weight=700) + '</g>')


def approach_vis():
    sup = [k for k, g in enumerate(gains(COMP)) if g > 0]

    def body(P):
        b = today_mark(P, TODAY2)
        b += ''.join(member(P, v, DK, 'a1') for v in VOTES)
        b += ''.join(member(P, VOTES[k], GREEN, 'a3') for k in sup)
        x, y = P(*COMP)
        b += f'<g class="a2"><circle cx="{x}" cy="{y}" r="24" fill="{OR}" stroke="{DK}" stroke-width="4"/></g>'
        b += f'<g class="a3">' + text(x, y + 62, 'adopted', 32, OR, weight=800) + '</g>'
        return b
    return plane(560, body)


def scoring_plane():
    def body(P):
        b = today_mark(P, TODAY2)
        b += ''.join(member(P, v, DK) for v in VOTES)
        for lab, pt, cls in (('A', VOTES[0], 'a1'), ('B', COMP, 'a2')):
            x, y = P(*pt)
            b += (f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="24" fill="{OR}" stroke="{DK}" stroke-width="4"/>'
                  + text(x + 60, y + 14, lab, 40, DK, weight=800) + '</g>')
        return b
    return plane(460, body, axes=False)


def gain_bars(p, lab, win):
    W, H = 600, 270
    g = sorted(gains(p), reverse=True)
    base, U = 150, 16
    b = f'<line x1="20" y1="{base}" x2="580" y2="{base}" stroke="{DK}" stroke-width="3"/>'
    for k, v in enumerate(g):
        x = 50 + k * 105
        hh = abs(v) * U
        y = base - hh if v > 0 else base
        b += f'<rect x="{x}" y="{y:.1f}" width="80" height="{hh:.1f}" rx="6" fill="{OR if k == 2 else GL}"/>'
    b += text(50 + 2 * 105 + 40, base - g[2] * U - 14, f'{g[2]:.1f}', 34, DK, weight=800)
    b += text(300, 258, f'{lab}: score {g[2]:.1f}' + (' ✓' if win else ''), 40, OR if win else DK, weight=800)
    return svg(W, H, b)


# ---------- the constitution as a page ----------
ENTRIES = [('rate', 'Commission rate', 'a number', 'difference', '½'),
           ('budget', 'Budget', 'a split', 'Euclidean distance', '½'),
           ('board', 'Board', 'a set of members', 'members that differ', '½'),
           ('constitution', 'This constitution', 'its own entries', 'per entry', '⅔')]


def page_vis():
    rows = ''
    for k, (ic, name, opt, dist, maj) in enumerate(ENTRIES):
        on = ' on' if k == len(ENTRIES) - 1 else ''
        rows += (f'<div class="entry{on}"><div class="eic">{icon(ic)}</div><div><p class="en">{name}</p>'
                 f'<p class="ed">{opt} · {dist} · majority {maj}</p></div></div>')
    return f'<div class="page"><p class="ptitle">Constitution</p>{rows}</div>'


# ---------- gap closed by the pairwise heuristic (paper, Table 2, 2D Euclidean, "Combined") ----------
GAP = [(5, 27), (21, 76), (51, 94)]


def gap_vis():
    W, H = 1500, 400
    b = ''
    for k, (n, p) in enumerate(GAP):
        y = 30 + k * 130
        b += text(250, y + 58, f'{n} members', 40, DK, 'end', weight=700)
        b += f'<rect x="290" y="{y}" width="1000" height="84" rx="12" fill="{GL}"/>'
        b += f'<rect x="290" y="{y}" width="{p*10}" height="84" rx="12" fill="{OR}"/>'
        b += text(290 + p * 10 + 20, y + 58, f'{p}%', 44, DK, 'start', weight=800)
    return svg(W, H, b)


def qr_svg(url, size=380):
    import qrcode
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    d = ''.join(f'M{x} {y}h1v1h-1z' for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return (f'<svg viewBox="0 0 {n} {n}" width="{size}" height="{size}" shape-rendering="crispEdges" '
            f'aria-label="QR code"><path d="{d}" fill="{DK}"/></svg>')


# ---------- slides ----------
TITLE = """
<section class="slide dark center">
  <p class="eyebrow">Paper · ADT 2026</p>
  <h1>Constitutional Governance<br>in Metric Spaces</h1>
  <p class="ref" style="bottom:128px;font-size:32px">Ehud Shapiro and Nimrod Talmon</p>
  <p class="ref">LSE and Weizmann Institute · Ben-Gurion University · November 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>"""

PW = 'https://peoplesweb.org/'
slides = [TITLE]
S = slides.append

S(f"""<section class="slide dark split">
  <div class="col">
    <h1>The Grassroots Project</h1>
    <p class="big"><a href="{PW}">peoplesweb.org</a></p>
  </div>
  <a class="qr" href="{PW}">{qr_svg(PW)}<span>peoplesweb.org</span></a>
</section>""")

S(f"""<section class="slide light">
  <p class="eyebrow">The problem</p>
  <h2>Grassroots community governance</h2>
  <p class="paper">A community decides many kinds of things, each a different kind of object</p>
  {kinds_vis()}
</section>""")

S(f"""<section class="slide light">
  <p class="eyebrow">The approach</p>
  <h2>Example: setting two numbers</h2>
  <p class="paper">A fee and a rate: each option is a point in the plane</p>
  <div class="cols">
    <div class="rows ruled steps">
      <div class="row a1"><span class="n">1</span><p>Each member votes for their ideal point</p></div>
      <div class="row a2"><span class="n">2</span><p>Anyone may add proposals</p></div>
      <div class="row a3"><span class="n">3</span><p>Adopt the best one a majority prefers to today</p></div>
    </div>
    <div style="flex:none">{approach_vis()}</div>
  </div>
</section>""")

S(f"""<section class="slide light">
  <p class="eyebrow">Which proposal is best?</p>
  <h2>The median member decides</h2>
  <p class="paper">My gain: how much closer the proposal is to me than today. Score: the middle gain.</p>
  <div class="cols">
    <div style="flex:none">{scoring_plane()}</div>
    <div class="bars"><div class="a1">{gain_bars(VOTES[0], 'A, a member’s point', False)}</div>
      <div class="a2">{gain_bars(COMP, 'B, a compromise', True)}</div></div>
  </div>
</section>""")

S(f"""<section class="slide light">
  <p class="eyebrow">The constitution</p>
  <h2>For each decision: options, distance, majority</h2>
  <p class="paper">The constitution is one of its own entries, amended with a higher majority</p>
  {page_vis()}
</section>""")

S(f"""<section class="slide light">
  <p class="eyebrow">Simulations</p>
  <h2>A simple algorithm closes most of the gap</h2>
  <p class="paper">Gray: how much better the best possible point is than the best member's point.<br>Orange: what an algorithm that blends two proposals recovers.</p>
  <div style="margin-block:auto">{gap_vis()}</div>
</section>""")

S("""<section class="slide light">
  <p class="eyebrow">Guarantees</p>
  <h2>What else we show</h2>
  <div class="cards">
    <div class="card top"><p class="label">No cycles</p><p>Everything is compared with today</p></div>
    <div class="card top"><p class="label">Fast</p><p>Polynomial time in all settings</p></div>
    <div class="card top"><p class="label">Honest</p><p>On a line, voting your ideal point is best</p></div>
  </div>
</section>""")

slides.append(TITLE)

STYLE = """<style>
.paper { font-size: 34px; color: var(--gray); margin-top: -24px; }
.kinds { display: flex; gap: 20px; margin-block: auto; }
.kind { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; background: var(--card);
  border: 1px solid var(--gray-light); border-radius: 16px; padding: 24px 8px; }
.kind:last-child { border: 4px solid var(--orange); }
.kind p { font-size: 32px; font-weight: 700; text-align: center; }
.steps { margin-block: auto; }
.steps .row p { font-size: 40px; }
.steps { flex: 1 !important; }
.slide .cols { gap: 64px; }
.qr { flex: none; text-decoration: none; border: 3px solid var(--orange); }
.bars { display: flex; flex-direction: column; gap: 16px; }
.card .label { font-size: 56px; color: var(--dark) !important; }
.card p { font-size: 40px; }
.card { min-height: 0; }
.page { margin-block: auto 0; align-self: center; width: 1240px; background: #fff; border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,.18); padding: 20px 64px; display: flex; flex-direction: column; gap: 4px; }
.ptitle { font-family: Georgia, serif; font-size: 46px; font-weight: 700; text-align: center; margin-bottom: 8px; }
.entry { display: flex; align-items: center; gap: 28px; padding: 6px 0; border-top: 1px solid var(--gray-light); }
.eic svg { width: 88px; height: 88px; display: block; }
.en { font-size: 44px; font-weight: 800; }
.ed { font-size: 36px; color: var(--gray); }
.entry.on .en { color: var(--orange); }
/* builds: play once when the slide is shown */
@keyframes fin { from { opacity: 0; } to { opacity: 1; } }
@keyframes fout { from { opacity: 1; } to { opacity: 0; } }
@keyframes lit { from { opacity: .25; } to { opacity: 1; } }
.slide.active .a1, .slide.active .a2, .slide.active .a3 { animation: fin .7s ease both; }
.slide.active .row.a1, .slide.active .row.a2, .slide.active .row.a3 { animation-name: lit; }
.slide.active .a1 { animation-delay: .4s; }
.slide.active .a2 { animation-delay: 3s; }
.slide.active .a3 { animation-delay: 5.5s; }
.slide.active .a3out { animation: fout .7s ease 5.5s both; }
body.static .slide * { animation-duration: 0s !important; animation-delay: 0s !important; }
</style>"""

SCRIPT = """<script>
// automated exports (PDF backup) show each slide's final state
if (navigator.webdriver) document.body.classList.add('static');
</script>"""

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
