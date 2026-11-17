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
        b += ''.join(member(P, v, GREEN if k in sup else DK) for k, v in enumerate(VOTES))
        x, y = P(*COMP)
        b += f'<circle cx="{x}" cy="{y}" r="24" fill="{OR}" stroke="{DK}" stroke-width="4"/>'
        b += text(x, y + 62, 'adopted', 32, OR, weight=800)
        return b
    return plane(560, body)


def legend():
    def item(sym, lab):
        return f'<div class="li">{sym}<span>{lab}</span></div>'
    hd = lambda c: svg(48, 48, head(24, 14, 10, c))
    return ('<div class="legend">'
            + item(hd(DK), 'a member’s ideal point')
            + item(hd(GREEN), 'prefers the proposal to today')
            + item(svg(48, 48, f'<circle cx="24" cy="24" r="17" fill="{OR}" stroke="{DK}" stroke-width="3"/>'), 'a proposal (a compromise)')
            + item(svg(48, 48, f'<rect x="12" y="12" width="24" height="24" fill="{GR}"/>'), 'today')
            + '</div>')


def mini_plane(pt, lab):
    def body(P):
        b = today_mark(P, TODAY2)
        b += ''.join(member(P, v, DK) for v in VOTES)
        x, y = P(*pt)
        b += (f'<circle cx="{x}" cy="{y}" r="22" fill="{OR}" stroke="{DK}" stroke-width="4"/>'
              + text(x + 52, y + 14, lab, 40, DK, weight=800))
        return b
    return plane(300, body, axes=False)


def gain_bars(p, win):
    W, H = 520, 300
    g = sorted(gains(p), reverse=True)
    base, U = 150, 16
    b = f'<line x1="10" y1="{base}" x2="510" y2="{base}" stroke="{DK}" stroke-width="3"/>'
    for k, v in enumerate(g):
        x = 30 + k * 98
        hh = abs(v) * U
        y = base - hh if v > 0 else base
        b += f'<rect x="{x}" y="{y:.1f}" width="76" height="{hh:.1f}" rx="6" fill="{OR if k == 2 else GL}"/>'
    b += text(30 + 2 * 98 + 38, base - g[2] * U - 14, f'{g[2]:.1f}', 34, DK, weight=800)
    b += text(260, 270, 'gains, sorted; middle one is the score', 26, GR)
    return svg(W, H, b)


def score_card(pt, lab, name, win):
    s = score(pt)
    return (f'<div class="card top sc{" win" if win else ""}"><p class="label">{lab}: {name}</p>'
            f'<div class="scrow">{mini_plane(pt, lab)}{gain_bars(pt, win)}</div>'
            f'<p class="scv">score {s:.1f}{" ✓" if win else ""}</p></div>')


# ---------- the constitution as a page ----------
ENTRIES = [('rate', 'Commission rate', 'a number', 'absolute difference', '½'),
           ('budget', 'Budget', 'a split', 'Euclidean distance', '½'),
           ('board', 'Board', 'a set of members', 'members that differ', '½'),
           ('constitution', 'This constitution', 'its own entries', 'per entry', '⅔')]


def page_vis():
    rows = '<div class="entry hdr"><span></span><span></span><span>options</span><span>distance</span><span>majority</span></div>'
    for k, (ic, name, opt, dist, maj) in enumerate(ENTRIES):
        on = ' on' if k == len(ENTRIES) - 1 else ''
        rows += (f'<div class="entry{on}"><div class="eic">{icon(ic)}</div><span class="en">{name}</span>'
                 f'<span>{opt}</span><span>{dist}</span><span class="em">{maj}</span></div>')
    return f'<div class="page"><p class="ptitle">Constitution</p>{rows}</div>'


# ---------- pairwise blends (heuristic P), and its effect at 51 members (paper, Table 2, 2D Euclidean, "Combined") ----------
def pairs_vis():
    def body(P):
        b = ''
        for i in range(5):
            for j in range(i + 1, 5):
                (x1, y1), (x2, y2) = P(*VOTES[i]), P(*VOTES[j])
                b += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GL}" stroke-width="3" stroke-dasharray="8 8"/>'
        for i in range(5):
            for j in range(i + 1, 5):
                m = ((VOTES[i][0] + VOTES[j][0]) / 2, (VOTES[i][1] + VOTES[j][1]) / 2)
                x, y = P(*m)
                b += f'<circle cx="{x}" cy="{y}" r="11" fill="{OR}"/>'
        b += today_mark(P, TODAY2)
        b += ''.join(member(P, v, DK) for v in VOTES)
        return b
    return plane(520, body, axes=False)


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


# layers of the grassroots architecture, as named in the paper's outlook
LAYERS = [('Federation', 'communities of communities'),
          ('Governance', 'this paper: any decision, polynomial time'),
          ('Consensus', 'on members’ own phones')]


def layers_vis():
    out = ''
    for name, sub in LAYERS:
        on = ' on' if name == 'Governance' else ''
        out += f'<div class="layer{on}"><b>{name}</b><span>{sub}</span></div>'
    return f'<div class="layers">{out}</div>'


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

S(f"""<section class="slide dark">
  <div class="cols apps">
    <div class="lcol">
      <h1>The Grassroots Project</h1>
      <a class="qr" href="{PW}">{qr_svg(PW, 580)}<span>peoplesweb.org</span></a>
    </div>
    <img class="appmap" src="img/grassroots-apps.png" alt="Map of grassroots apps and how they relate">
  </div>
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
    <div class="lcol">
      <div class="rows ruled steps">
        <div class="row"><span class="n">1</span><p>Each member votes for their ideal point</p></div>
        <div class="row"><span class="n">2</span><p>Anyone may add proposals</p></div>
        <div class="row"><span class="n">3</span><p>Adopt the best one a majority prefers to today</p></div>
      </div>
      {legend()}
    </div>
    <div style="flex:none">{approach_vis()}</div>
  </div>
</section>""")

S(f"""<section class="slide light">
  <p class="eyebrow">Which proposal is best?</p>
  <h2>The median member decides</h2>
  <p class="paper">My gain: how much closer the proposal is to me than today. Score: the middle gain.</p>
  <div class="cards">
    {score_card(VOTES[0], 'A', 'a member’s point', False)}
    {score_card(COMP, 'B', 'a compromise', True)}
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
  <h2>Blending pairs closes most of the gap</h2>
  <p class="paper">Gap: how much better the best possible point is than the best member’s point</p>
  <div class="cols">
    <div style="flex:none">{pairs_vis()}</div>
    <div class="bignum"><p class="small muted">Try the blend of every pair of proposals</p>
      <h1 class="huge" style="color:var(--orange)">94%</h1><p class="big">of the gap closed, with 51 members</p>
      <p class="src">Proposals may also come from deliberation, optimization, or AI</p></div>
  </div>
</section>""")

GOOD = [('General', 'Officers, budgets, bylaws, …'),
        ('Unified', 'One rule for all decisions'),
        ('Polynomial time', 'Even where optima are NP-hard'),
        ('Self-amending', 'The constitution, by the same rule')]
good = ''.join(f'<div class="card top"><p class="label">{t}</p><p>{d}</p></div>' for t, d in GOOD)
S(f"""<section class="slide light">
  <p class="eyebrow">The vision</p>
  <h2>A governance layer for grassroots communities</h2>
  <div class="cols">
    <div class="good">{good}</div>
    <a class="qr" style="flex:none" href="{PW}">{qr_svg(PW, 360)}<span>peoplesweb.org</span></a>
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
.slide .cols { gap: 64px; }
.lcol { flex: 1; display: flex; flex-direction: column; gap: 48px; }
.steps { margin-block: 0; }
.steps .row p { font-size: 40px; }
.legend { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 24px; }
.li { display: flex; align-items: center; gap: 12px; font-size: 30px; color: var(--gray); }
.li svg { flex: none; }
.qr { flex: none; text-decoration: none; border: 3px solid var(--orange); }
.qr span { font-size: 34px; }
.gp { gap: 64px; }
.apps { align-items: stretch; height: 100%; }
.apps .lcol { justify-content: space-between; align-items: flex-start; }
.apps h1 { font-size: 80px; white-space: nowrap; }
.apps .qr { margin: 0; align-self: flex-start; }
.apps .qr span { font-size: 48px; }
.appmap { flex: none; height: 860px; border-radius: 16px; }
.gp h1 { white-space: nowrap; }
.sc { padding: 28px 32px; gap: 8px; min-height: 0; }
.sc .label { font-size: 40px; color: var(--dark) !important; }
.scrow { display: flex; align-items: center; gap: 8px; }
.scrow svg:first-child { width: 270px; height: auto; flex: none; }
.scrow svg:last-child { width: 440px; height: auto; flex: none; }
.sc { flex: 1 1 0; min-width: 0; }
.scv { font-size: 44px !important; font-weight: 800; text-align: center; }
.sc.win { border: 4px solid var(--orange) !important; }
.sc.win .scv { color: var(--orange); }
.page { margin-block: auto 0; align-self: center; width: 1560px; background: #fff; border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,.18); padding: 16px 56px 20px; display: flex; flex-direction: column; }
.ptitle { font-family: Georgia, serif; font-size: 46px; font-weight: 700; text-align: center; }
.entry { display: grid; grid-template-columns: 100px 380px 360px 400px 1fr; align-items: center;
  padding: 4px 0; border-top: 1px solid var(--gray-light); font-size: 36px; }
.entry.hdr { border-top: none; font-size: 28px; font-weight: 700; color: var(--gray); }
.eic svg { width: 84px; height: 84px; display: block; }
.en { font-size: 40px; font-weight: 800; }
.em { font-weight: 800; }
.entry.on .en, .entry.on .em { color: var(--orange); }
.good { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.good .card { min-height: 0; padding: 32px 36px; }
.good .label { font-size: 48px; color: var(--dark) !important; }
.good p { font-size: 34px; white-space: nowrap; }
.src { font-size: 34px; color: var(--gray); margin-top: 40px; padding-top: 24px; border-top: 2px solid var(--gray-light); }
.bignum { display: flex; flex-direction: column; gap: 8px; }
.layers { flex: 1; display: flex; flex-direction: column; gap: 16px; }
.layer { display: flex; align-items: baseline; gap: 32px; padding: 32px 40px; border-radius: 16px;
  background: var(--card); border: 1px solid var(--gray-light); }
.layer b { font-size: 48px; width: 300px; flex: none; }
.layer span { font-size: 34px; color: var(--gray); }
.layer.on { background: var(--orange); border: none; }
.layer.on span { color: var(--dark); }
</style>"""

SCRIPT = ""

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
