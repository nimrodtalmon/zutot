#!/usr/bin/env python3
"""Builds slides/metric-based-voting/index.html (inline SVG visuals)."""
import math
import os
import statistics as st

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'index.html')
OR, DK, GR, GL, CARD, PALE, LT = '#F7941D', '#26282C', '#5F6368', '#B9BCC1', '#FDFDFB', '#FCE8D2', '#F3F3F1'
FONT = 'font-family="Heebo, Arial, sans-serif"'

# ---------- running example: three color-coded metrics ----------
GREEN, GOLD, BLUE = '#3E9B4F', '#E2B42B', '#3A7BC8'
LIE = '#D64545'
METRICS = ['Planet', 'Fees', 'Energy']
KINDS = ['leaf', 'coin', 'bolt']
MCOL = [GREEN, GOLD, BLUE]
PROJECTS = ['Wallet', 'Bridge', 'DEX']
VAL = [[.9, .3, .6], [.4, .9, .2], [.6, .6, .9]]
VOTERS = ['Ann', 'Ben', 'Cat']
BALLOTS = [[.6, .2, .2], [.2, .6, .2], [.3, .2, .5]]


def svg(w, h, body, style=''):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT} style="{style}">{body}</svg>'


def text(x, y, s, size=30, fill=DK, anchor='middle', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def head(cx, cy, r, fill):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx-1.6*r} {cy+2.6*r} a{1.6*r} {1.6*r} 0 0 1 {3.2*r} 0 Z" fill="{fill}"/>')


def ghost(cx, cy, r, color=OR):
    """A friendly phantom: dome top, wavy hem, two eyes."""
    top, bot = cy - r, cy + 1.3 * r
    hem = ' '.join(f'q{r/4:.1f} {r/3 if k % 2 == 0 else -r/3:.1f} {r/2:.1f} 0' for k in range(4))
    return (f'<path d="M{cx-r} {bot} V{cy} a{r} {r} 0 0 1 {2*r} 0 V{bot} '
            f'{" ".join(f"q{-r/4:.1f} {-r/3 if k % 2 == 0 else r/3:.1f} {-r/2:.1f} 0" for k in range(4))} Z" '
            f'fill="{PALE}" stroke="{color}" stroke-width="4" stroke-dasharray="8 6"/>'
            f'<circle cx="{cx-r/3}" cy="{cy-r/6}" r="{r/7}" fill="{DK}"/>'
            f'<circle cx="{cx+r/3}" cy="{cy-r/6}" r="{r/7}" fill="{DK}"/>')


def icon(kind, cx, cy, r, color):
    """Metric badge: colored disc with a white glyph (leaf / coin / bolt)."""
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
    if kind == 'leaf':
        a = .55 * r
        o += (f'<path d="M{cx-a} {cy+a} C{cx-a} {cy-.2*r} {cx-.1*r} {cy-a} {cx+a} {cy-a} '
              f'C{cx+a} {cy+.2*r} {cx+.1*r} {cy+a} {cx-a} {cy+a} Z" fill="#fff"/>'
              f'<line x1="{cx-a}" y1="{cy+a}" x2="{cx+.25*r}" y2="{cy-.25*r}" stroke="{color}" stroke-width="{r/9:.1f}" stroke-linecap="round"/>')
    elif kind == 'coin':
        o += text(cx, cy + .38 * r, '$', 1.1 * r, '#fff', weight=800)
    else:
        pts = [(.12, -.62), (-.36, .08), (-.02, .08), (-.14, .62), (.36, -.1), (.02, -.1)]
        o += f'<polygon points="{" ".join(f"{cx+x*r:.1f},{cy+y*r:.1f}" for x, y in pts)}" fill="#fff"/>'
    return o


def arrow(x1, y, x2, color=OR):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2-14}" y2="{y}" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M{x2} {y} l-22 -13 v26 z" fill="{color}"/>')


def bars(x, y, vals, w=34, gap=10, h=150, cols=MCOL, frame=True):
    out = ''
    for k, v in enumerate(vals):
        bx = x + k * (w + gap)
        if frame:
            out += f'<rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="5" fill="none" stroke="{GL}" stroke-width="2"/>'
        if v > 0:
            out += f'<rect x="{bx}" y="{y+h-v*h}" width="{w}" height="{v*h}" rx="5" fill="{cols[k % len(cols)]}"/>'
    return out


def face(cx, cy, r, happy):
    mouth = (f'M{cx-.45*r} {cy+.25*r} q{.45*r} {.4*r} {.9*r} 0' if happy
             else f'M{cx-.45*r} {cy+.5*r} q{.45*r} {-.4*r} {.9*r} 0')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{OR if happy else CARD}" stroke="{DK}" stroke-width="4"/>'
            f'<circle cx="{cx-.33*r}" cy="{cy-.2*r}" r="{.1*r}" fill="{DK}"/>'
            f'<circle cx="{cx+.33*r}" cy="{cy-.2*r}" r="{.1*r}" fill="{DK}"/>'
            f'<path d="{mouth}" fill="none" stroke="{DK}" stroke-width="5" stroke-linecap="round"/>')


def hide(on, body):
    return body if on else f'<g opacity="0">{body}</g>'


# ---------- slide visuals ----------
def pot_vis():
    """A pile of coins, dashed arrows to four project tiles, each with a question mark."""
    W, H = 820, 560
    b = ''
    for s, (sx, n) in enumerate([(70, 6), (150, 9), (230, 4)]):
        for k in range(n):
            y = 470 - k * 22
            b += (f'<ellipse cx="{sx}" cy="{y+10}" rx="56" ry="18" fill="#D97F0F"/>'
                  f'<ellipse cx="{sx}" cy="{y}" rx="56" ry="18" fill="{OR}" stroke="{PALE}" stroke-width="2"/>')
    tiles = [(640, 90), (700, 230), (700, 370), (640, 510)]
    for k, (tx, ty) in enumerate(tiles):
        b += (f'<path d="M300 {300} C 430 {300} 480 {ty} {tx-80} {ty}" fill="none" stroke="{GL}" '
              f'stroke-width="5" stroke-dasharray="4 12" stroke-linecap="round"/>')
        b += f'<rect x="{tx-70}" y="{ty-46}" width="140" height="92" rx="18" fill="{CARD}" stroke="{DK}" stroke-width="4"/>'
        b += text(tx, ty + 22, '?', 60, OR, weight=800)
    return svg(W, H, b)


def fishbone(x, y, s=1, color=DK):
    """Fish skeleton: something smells funny."""
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{color}" stroke-width="6" stroke-linecap="round" fill="none">'
            f'<path d="M0 0 l26 -22 q22 22 0 44 z" fill="{color}"/>'
            f'<line x1="26" y1="0" x2="120" y2="0"/>'
            + ''.join(f'<line x1="{x0}" y1="-20" x2="{x0+8}" y2="20"/>' for x0 in (48, 72, 96)) +
            f'<path d="M120 0 l24 -20 v40 z" fill="{color}"/></g>')


def phantoms_vis():
    W, H = 1460, 250
    b = f'<line x1="40" y1="190" x2="{W-40}" y2="190" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
    for x in (220, 520, 1060):
        b += head(x, 110, 26, DK)
    for x in (360, 820):
        b += ghost(x, 118, 40)
    return svg(W, H, b)


def how_it_works(step):
    """step 1..5: Metrics, Ballots, Weights, Data, Scores (later columns hidden).
    Reads as: metrics -> ballots -> weights x data = scores."""
    W, H = 1660, 570
    T, S = 46, 30
    agg = [st.median(c) for c in zip(*BALLOTS)]
    sc = [[agg[j] * VAL[i][j] for j in range(3)] for i in range(3)]
    y0, c = 200, 96
    cols = []
    # 1 metrics
    b = text(115, 50, 'Metrics', T, DK, weight=800) + text(115, 96, 'what counts', S, GR)
    for j, m in enumerate(METRICS):
        y = 250 + 100 * j
        b += icon(KINDS[j], 40, y, 30, MCOL[j]) + text(86, y + 11, m, 34, DK, 'start', weight=700)
    cols.append(b)
    # 2 ballots
    bx = 360
    b = text(bx + 92, 50, 'Ballots', T, DK, weight=800) + text(bx + 92, 96, 'what matters', S, GR)
    for v in range(3):
        yy = 168 + v * 136
        b += head(bx + 20, yy + 40, 16, GR)
        b += bars(bx + 62, yy, BALLOTS[v], w=36, gap=10, h=110)
    cols.append(b)
    # 3 weights
    ax = 680
    b = text(ax + 80, 50, 'Weights', T, DK, weight=800) + text(ax + 80, 96, 'one per metric', S, GR)
    b += bars(ax, 215, agg, w=46, gap=12, h=270)
    cols.append(b)
    # 4 data
    x0 = 1010
    b = text(x0 + 1.5 * c, 50, 'Data', T, DK, weight=800) + text(x0 + 1.5 * c, 96, 'public', S, GR)
    for j in range(3):
        b += icon(KINDS[j], x0 + j * c + c / 2, y0 - 34, 22, MCOL[j])
    for i, p in enumerate(PROJECTS):
        b += text(x0 - 14, y0 + i * c + c / 2 + 11, p, S, GR, 'end')
        for j in range(3):
            v = VAL[i][j]
            b += f'<rect x="{x0+j*c+5}" y="{y0+i*c+5}" width="{c-10}" height="{c-10}" rx="12" fill="{MCOL[j]}" fill-opacity="{0.12+0.7*v:.2f}"/>'
            b += text(x0 + j * c + c / 2, y0 + i * c + c / 2 + 12, f'{v:.1f}'.lstrip('0'), 32, DK, weight=700)
    cols.append(b)
    # 5 scores, stacked by metric, aligned with the data rows
    sx, scale = 1370, 285 / max(sum(r) for r in sc)
    b = text(sx + 140, 50, 'Scores', T, DK, weight=800) + text(sx + 140, 96, 'weighted sums', S, GR)
    for i in range(3):
        yy, x = y0 + i * c + 12, sx
        for j in range(3):
            w = sc[i][j] * scale
            b += f'<rect x="{x:.1f}" y="{yy}" width="{w:.1f}" height="{c-24}" fill="{MCOL[j]}"/>'
            x += w
    cols.append(b)
    joins = [arrow(240, 350, 330), arrow(570, 350, 660),
             text(855, 372, '×', 72, OR, weight=800), text(1328, 370, '=', 72, OR, weight=800)]
    body = ''
    for k, col in enumerate(cols):
        body += hide(k < step, col)
        if k < 4:
            body += hide(k + 1 < step, joins[k])
    return svg(W, H, body)


def ballot_formats():
    W, H = 1660, 540
    b = ''
    panels = [('Plurality', 'pick one', [0, 1, 0], ''),
              ('Approval', 'in or out', [1, 0, 1], ''),
              ('Cumulative', 'split 100%', [.5, .3, .2], '= 100%'),
              ('Fractional', 'any weight', [.8, .4, 1], '')]
    for k, (name, sub, vals, foot) in enumerate(panels):
        x = 40 + k * 410
        b += f'<rect x="{x}" y="20" width="380" height="500" rx="18" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
        b += f'<rect x="{x}" y="20" width="380" height="10" rx="5" fill="{OR}"/>'
        b += text(x + 190, 95, name, 40, DK, weight=800)
        b += text(x + 190, 140, sub, 30, GR)
        b += bars(x + 82, 190, vals, w=56, gap=24, h=220)
        for j in range(3):
            b += icon(KINDS[j], x + 82 + j * 80 + 28, 450, 20, MCOL[j])
        if foot:
            b += text(x + 190, 505, foot, 26, GR, weight=700)
    return svg(W, H, b)


def mean_median_vis(show):
    """Three voters' Planet weights, then the two aggregates."""
    W, H = 1600, 600
    vals = [.9, .1, .3]
    base, hh = 500, 340
    b = ''
    b += icon('leaf', 150, 40, 30, GREEN) + text(196, 52, 'Planet', 38, DK, 'start', weight=800)
    for k, (nm, v) in enumerate(zip(VOTERS, vals)):
        x = 120 + k * 200
        b += f'<rect x="{x}" y="{base-hh}" width="110" height="{hh}" rx="10" fill="none" stroke="{GL}" stroke-width="2"/>'
        b += f'<rect x="{x}" y="{base-v*hh}" width="110" height="{v*hh}" rx="10" fill="{GREEN}"/>'
        b += text(x + 55, base - v * hh - 16, f'{v:g}', 34, DK, weight=700)
        b += text(x + 55, base + 50, nm, 32, GR)
    b += arrow(760, 330, 860)
    agg = [('mean', sum(vals) / 3, DK), ('median', st.median(vals), OR)]
    tag = (f'<rect x="950" y="0" width="450" height="64" rx="32" fill="{PALE}"/>'
           + text(1175, 44, 'Both used in practice', 32, DK, weight=800))
    b += hide(show, tag)
    for k, (nm, v, col) in enumerate(agg):
        x = 960 + k * 280
        b += f'<rect x="{x}" y="{base-hh}" width="150" height="{hh}" rx="10" fill="none" stroke="{GL}" stroke-width="3" stroke-dasharray="12 10"/>'
        b += text(x + 75, base + 50, nm, 36, col if show else GR, weight=800)
        if show:
            b += f'<rect x="{x}" y="{base-v*hh}" width="150" height="{v*hh}" rx="10" fill="{col}"/>'
            b += text(x + 75, base - v * hh - 16, f'{v:.2f}'.rstrip('0').rstrip('.'), 40, col, weight=800)
        else:
            b += text(x + 75, base - hh / 2 + 20, '?', 64, GL, weight=800)
    return svg(W, H, b)


def thermo_pair(rule, lie_shown):
    """Two stacked number lines: everyone truthful, and Cat saying 32°."""
    W, H = 1600, 640
    lo, hi = 15, 33
    X = lambda v: 280 + (v - lo) / (hi - lo) * (W - 340)
    b = ''
    for r, (label, cat) in enumerate([('Truth', 26), ('Cat lies', 32)]):
        y = 150 + r * 320
        row = text(40, y + 12, label, 36, DK if r == 0 else LIE, 'start', weight=800)
        row += f'<line x1="{X(lo)-20}" y1="{y}" x2="{X(hi)+20}" y2="{y}" stroke="{GL}" stroke-width="6" stroke-linecap="round"/>'
        for t in (16, 20, 24, 28, 32):
            row += f'<line x1="{X(t)}" y1="{y-10}" x2="{X(t)}" y2="{y+10}" stroke="{GL}" stroke-width="3"/>'
            row += text(X(t), y + 46, f'{t}°', 26, GL)
        if r == 1:
            row += f'<circle cx="{X(26)}" cy="{y}" r="20" fill="none" stroke="{GL}" stroke-width="4" stroke-dasharray="6 6"/>'
        for v, nm in [(18, 'Ann'), (22, 'Ben'), (cat, 'Cat')]:
            row += f'<circle cx="{X(v)}" cy="{y}" r="22" fill="{LIE if (r == 1 and nm == "Cat") else DK}"/>'
            row += text(X(v), y - 42, nm, 32, DK, weight=700)
        if rule:
            vals = [18, 22, cat]
            m = sum(vals) / 3 if rule == 'mean' else st.median(vals)
            col = DK if rule == 'mean' else OR
            if rule == 'mean':
                row += f'<path d="M{X(m)} {y+70} l-22 36 h44 z" fill="{col}"/>'
            else:
                row += f'<path d="M{X(m)} {y+68} l22 24 l-22 24 l-22 -24 z" fill="{col}"/>'
            row += text(X(m), y + 150, f'{rule} {m:g}°', 34, col, weight=800)
        b += hide(r == 0 or lie_shown, row)
    return svg(W, H, b)


def ann_table(lie):
    rows = [('Ann', [1, 1 if lie else 0]), ('Ben', [0, 1]), ('Cat', [0, 0])]
    med = [st.median(c) for c in zip(*[r[1] for r in rows])]
    W, H = 1300, 600
    b = ''
    cx = [420, 610, 870]
    b += icon('leaf', cx[0] - 52, 52, 22, GREEN) + text(cx[0] - 20, 62, 'Planet', 30, DK, 'start', weight=700)
    b += icon('bolt', cx[1] - 52, 52, 22, BLUE) + text(cx[1] - 20, 62, 'Energy', 30, DK, 'start', weight=700)
    b += text(cx[2], 62, 'score', 30, GR, weight=700)
    for i, (nm, v) in enumerate(rows):
        y = 90 + i * 92
        b += text(40, y + 50, nm, 36, DK, 'start', weight=800 if nm == 'Ann' else 400)
        if nm == 'Ann':
            b += text(140, y + 50, '(lie)' if lie else '(truth)', 30, LIE if lie else GR, 'start', weight=700)
            b += f'<rect x="{cx[2]-110}" y="{y}" width="220" height="74" rx="12" fill="{PALE}"/>'
            b += text(cx[2], y + 50, 'wants 1', 34, DK, weight=800)
        for j, val in enumerate(v):
            hot = lie and nm == 'Ann' and j == 1
            b += f'<rect x="{cx[j]-75}" y="{y}" width="150" height="74" rx="12" fill="{LIE if hot else CARD}" stroke="{GL}" stroke-width="{0 if hot else 2}"/>'
            b += text(cx[j], y + 50, f'{val:g}', 36, '#fff' if hot else DK, weight=700)
    # median row, set apart by a rule
    y = 90 + 3 * 92 + 40
    b += f'<line x1="30" y1="{y-26}" x2="{cx[2]+110}" y2="{y-26}" stroke="{DK}" stroke-width="5" stroke-linecap="round"/>'
    b += text(40, y + 50, 'Median', 36, DK, 'start', weight=800)
    for j in range(2):
        b += f'<rect x="{cx[j]-75}" y="{y}" width="150" height="74" rx="12" fill="{PALE}"/>'
        b += text(cx[j], y + 50, f'{med[j]:g}', 36, DK, weight=800)
    s = med[0] + med[1]
    b += f'<rect x="{cx[2]-110}" y="{y}" width="220" height="74" rx="12" fill="{OR}"/>'
    b += text(cx[2], y + 50, f'{s:g}', 36, DK, weight=800)
    b += face(1150, y + 20, 56, s == 1)
    b += text(1150, y + 120, 'Ann', 30, GR, weight=700)
    return svg(W, H, b)


def search_vis():
    W, H = 1660, 560
    b = ''
    b += f'<rect x="20" y="20" width="790" height="520" rx="22" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
    b += f'<path d="M150 380 C120 230 260 130 420 150 C590 170 690 260 640 390 C600 480 330 500 220 460 C180 445 160 420 150 380 Z" fill="{PALE}" stroke="{OR}" stroke-width="5"/>'
    b += f'<path d="M260 400 C330 360 420 320 490 270" fill="none" stroke="{DK}" stroke-width="5" stroke-dasharray="2 14" stroke-linecap="round"/>'
    b += f'<circle cx="260" cy="400" r="12" fill="{DK}"/>'
    b += star(500, 262, 30)
    b += text(415, 90, 'Mean', 44, DK, weight=800)
    b += f'<rect x="850" y="20" width="790" height="520" rx="22" fill="{CARD}" stroke="{GL}" stroke-width="2"/>'
    import random
    random.seed(4)
    for _ in range(26):
        x, y, r = random.randint(930, 1560), random.randint(150, 500), random.randint(14, 34)
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PALE}" stroke="{OR}" stroke-width="4"/>'
    b += star(1330, 300, 30)
    b += text(1245, 90, 'Median, cumulative ballots', 44, DK, weight=800)
    return svg(W, H, b)


def star(cx, cy, r):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append(f'{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{DK}"/>'


def clone_vis(after):
    """Fees weights before/after adding a copy; the fee-heavy DEX on the side."""
    W, H = 1600, 540
    names = VOTERS
    before = [.4, .2, .2]
    split = [(.2, .2), (.2, 0), (0, .2)]
    base, unit = 400, 560
    b = ''

    def column(x, vals, title, dashed=False):
        o = text(x + 150, 50, title, 34, DK, weight=800)
        dash = 'stroke-dasharray="14 10"' if dashed else ''
        o += f'<rect x="{x}" y="70" width="300" height="{base-50}" rx="14" fill="none" stroke="{GL}" stroke-width="3" {dash}/>'
        for k, v in enumerate(vals):
            bx = x + 30 + k * 85
            if v > 0:
                o += f'<rect x="{bx}" y="{base - v*unit}" width="70" height="{v*unit}" rx="8" fill="{GOLD}"/>'
            o += text(bx + 35, base + 44, names[k], 30, GR)
            o += text(bx + 35, base - v * unit - 12, f'{v:g}', 30, DK, weight=700)
        m = st.median(vals)
        y = base - m * unit
        o += f'<line x1="{x+10}" y1="{y}" x2="{x+290}" y2="{y}" stroke="{DK}" stroke-width="6" stroke-dasharray="4 10" stroke-linecap="round"/>'
        o += text(x + 150, base + 100, f'median {m:g}', 32, OR, weight=800)
        return o, m

    if after:
        o1, m1 = column(40, [s[0] for s in split], 'Fees')
        o2, m2 = column(400, [s[1] for s in split], 'Fees (log)', dashed=True)
        b += o1 + o2
        m = m1 + m2
    else:
        o1, m = column(40, before, 'Fees')
        b += o1
    tx = 860
    b += icon('coin', tx + 26, 60, 26, GOLD) + text(tx + 66, 72, 'Fees weight' + (', in total' if after else ''), 34, GR, 'start')
    b += text(tx, 150, f'median: {"0.2 + 0.2 = " if after else ""}{m:g}', 50, OR, 'start', weight=800)
    b += text(tx, 210, f'mean: {sum(before)/3:.2f}' + ('  (unchanged)' if after else ''), 38, DK, 'start', weight=700)
    # DEX, strong on fees
    y = 330
    b += text(tx, y, 'DEX, strong on fees:', 34, DK, 'start', weight=800)
    b += text(tx, y + 46, 'its score from fees', 30, GR, 'start')
    sc = m * .9
    b += f'<rect x="{tx}" y="{y+76}" width="{sc*1500:.0f}" height="64" rx="10" fill="{GOLD}"/>'
    if after:
        ox = tx + .18 * 1500
        b += f'<line x1="{ox}" y1="{y+62}" x2="{ox}" y2="{y+154}" stroke="{DK}" stroke-width="4" stroke-dasharray="8 8"/>'
        b += text(ox, y + 190, 'was 0.18', 28, GR, weight=700)
    b += text(tx + sc * 1500 + 20, y + 122, f'{sc:.2f}', 38, DK, 'start', weight=800)
    return svg(W, H, b)


def landscape_vis():
    """The paper's classification table, as colored tiles."""
    T = {
        'Plurality': [('P', 'P'), ('H', 'P'), ('H', 'P'), ('I', 'P')],
        'Approval': [('H', 'H')] * 4,
        'Cumulative': [('P', 'H'), ('P', 'H'), ('H', 'H'), ('I', 'H')],
        'Fractional': [('P', 'P'), ('P', 'P'), ('H', 'H'), ('H', 'H')],
    }  # (mean, median) per lever: RC, PM, MS, MR
    levers = ['Change a ballot', 'Edit ballots', 'Pick metrics', 'Copy metrics']
    W, H = 1660, 580
    x0, cw, gap, ggap = 270, 160, 8, 26
    b = ''
    gx = lambda g: x0 + g * (2 * cw + gap + ggap)
    for g, lv in enumerate(levers):
        b += text(gx(g) + cw + gap / 2, 40, lv, 32, DK, weight=800)
        b += text(gx(g) + cw / 2, 88, 'mean', 26, GR, weight=700)
        b += text(gx(g) + cw + gap + cw / 2, 88, 'median', 26, OR, weight=700)
    for r, (dom, cells) in enumerate(T.items()):
        y = 112 + r * 116
        b += text(x0 - 30, y + 62, dom, 34, DK, 'end', weight=700)
        for g, pair in enumerate(cells):
            for k, c in enumerate(pair):
                x = gx(g) + k * (cw + gap)
                fill, fg, lab = {'P': (CARD, GR, 'easy'), 'H': (DK, LT, 'hard'), 'I': (OR, DK, 'no effect')}[c]
                stroke = f'stroke="{GL}" stroke-width="2"' if c == 'P' else ''
                b += f'<rect x="{x}" y="{y}" width="{cw}" height="96" rx="12" fill="{fill}" {stroke}/>'
                b += text(x + cw / 2, y + 58, lab, 30, fg, weight=700)
    return svg(W, H, b)


# ---------- part 1 visuals: food security ----------
SOFTRED, SOFTGREEN = '#FBE3E3', '#E2F2E5'
DASHED = 'stroke-dasharray="10 8"'


def house(x, y, s, on, w=10):
    col = OR if on else GL
    return (f'<path d="M{x} {y+.45*s} L{x+.5*s} {y} L{x+s} {y+.45*s} V{y+s} H{x} Z" fill="{OR if on else "none"}" '
            f'stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<rect x="{x+.38*s}" y="{y+.6*s}" width="{.24*s}" height="{.4*s}" rx="{s/30:.0f}" fill="{DK if on else GL}"/>')


def houses_small():
    return svg(390, 100, ''.join(house(10 + k * 95, 10, 80, k == 0, 6) for k in range(4)))


def box(cx, cy, label, w=270, h=84, fill=CARD, stroke=DK, fg=DK, dash='', size=30):
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="4" {dash}/>'
            + text(cx, cy + size * .36, label, size, fg, weight=700))


def link(x1, y1, x2, y2, color, w=6, dash=''):
    mx = (x1 + x2) / 2
    return (f'<path d="M{x1} {y1} C{mx} {y1} {mx} {y2} {x2-18} {y2}" fill="none" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round" {dash}/>'
            f'<path d="M{x2} {y2} l-22 -12 v24 z" fill="{color}"/>')


def virus(cx, cy, r):
    o = ''
    for k in range(8):
        a = k * math.pi / 4
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + 1.45 * r * math.cos(a), cy + 1.45 * r * math.sin(a)
        o += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{OR}" stroke-width="8" stroke-linecap="round"/>'
        o += f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="12" fill="{OR}"/>'
    return o + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PALE}" stroke="{OR}" stroke-width="8"/>'


def roadblock(cx, cy, r):
    w, h = 2.2 * r, .5 * r
    o = ''.join(f'<rect x="{cx+dx-8}" y="{cy-.2*r}" width="16" height="{1.2*r}" rx="6" fill="{DK}"/>' for dx in (-.8 * r, .8 * r))
    o += f'<rect x="{cx-w/2}" y="{cy-h/2-.3*r}" width="{w}" height="{h}" rx="10" fill="{CARD}" stroke="{DK}" stroke-width="5"/>'
    seg = (w - 10) / 5
    for k in range(0, 5, 2):
        o += f'<rect x="{cx-w/2+5+k*seg:.0f}" y="{cy-h/2-.3*r+5:.0f}" width="{seg:.0f}" height="{h-10:.0f}" fill="{LIE}"/>'
    return o


def crisis_vis():
    """Pandemic, war -> a supply chain with a broken link."""
    W, H = 1660, 340
    b = virus(150, 140, 70) + text(150, 310, 'pandemic', 36, DK, weight=800)
    b += roadblock(450, 150, 90) + text(450, 310, 'war', 36, DK, weight=800)
    b += f'<path d="M640 150 h70" stroke="{OR}" stroke-width="10" stroke-linecap="round"/><path d="M740 150 l-34 -22 v44 z" fill="{OR}"/>'
    xs = [900, 1150, 1400]
    for k, x in enumerate(xs):
        b += f'<circle cx="{x}" cy="150" r="50" fill="{CARD}" stroke="{DK}" stroke-width="6"/>'
    b += f'<line x1="950" y1="150" x2="1100" y2="150" stroke="{DK}" stroke-width="8"/>'
    b += f'<line x1="1200" y1="150" x2="1260" y2="150" stroke="{LIE}" stroke-width="8" stroke-linecap="round"/>'
    b += f'<line x1="1290" y1="150" x2="1350" y2="150" stroke="{LIE}" stroke-width="8" stroke-linecap="round"/>'
    b += f'<path d="M1262 118 l26 64" stroke="{LIE}" stroke-width="8" stroke-linecap="round"/>'
    b += text(1150, 310, 'supply chains break', 36, DK, weight=800)
    return svg(W, H, b)


def network_vis():
    """Seeds, eggs and meat moving between farmers, distributors, the grocery; consumers and waste are sinks."""
    W, H, bw = 1680, 600, 270
    N = {'seedf': ('Seed farmer', 145, 270), 'chick': ('Chicken farmer', 480, 140),
         'seedd': ('Seed distributor', 480, 420), 'eggd': ('Egg distributor', 815, 50),
         'butch': ('Butcher', 815, 195), 'groc': ('Grocery', 1150, 300),
         'cons': ('Consumers', 1530, 190), 'waste': ('Waste', 1530, 420)}
    SEED, EGG, MEAT = GREEN, GOLD, LIE
    E = [('seedf', 'chick', SEED), ('seedf', 'seedd', SEED), ('seedd', 'groc', SEED),
         ('chick', 'eggd', EGG), ('chick', 'butch', MEAT), ('eggd', 'groc', EGG),
         ('butch', 'groc', MEAT), ('groc', 'cons', GR), ('groc', 'waste', GL)]
    sinks = {'cons', 'waste'}
    b = ''
    for a, c, col in E:
        _, xa, ya = N[a]
        _, xc, yc = N[c]
        b += link(xa + bw / 2, ya, xc - bw / 2, yc, col, dash='stroke-dasharray="4 12"' if c in sinks else '')
    for k, (lab, x, y) in N.items():
        if k in sinks:
            b += box(x, y, lab, bw, fill=LT, stroke=GR, fg=GR, dash=DASHED)
        else:
            b += box(x, y, lab, bw)
    for k, (lab, col) in enumerate([('seeds', SEED), ('eggs', EGG), ('meat', MEAT)]):
        x = 520 + k * 240
        b += f'<line x1="{x}" y1="560" x2="{x+70}" y2="560" stroke="{col}" stroke-width="8" stroke-linecap="round"/>'
        b += text(x + 90, 571, lab, 30, GR, 'start', weight=700)
    return svg(W, H, b)


def check(cx, cy, r, color=GREEN):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<path d="M{cx-.45*r} {cy} l{.3*r} {.32*r} l{.6*r} {-.62*r}" fill="none" stroke="#fff" '
            f'stroke-width="{r/4:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def record_vis():
    """One hand-off as a record, and the four steps it goes through."""
    W, H = 1660, 500
    b = f'<rect x="20" y="20" width="700" height="460" rx="22" fill="{CARD}" stroke="{DK}" stroke-width="4"/>'
    b += f'<rect x="20" y="20" width="700" height="12" rx="6" fill="{OR}"/>'
    rows = [('seller', 'Dairy farm'), ('buyer', 'Grocery'), ('batch', '#4417'), ('date', 'March 3'), ('amount', '200 liters')]
    for k, (f, v) in enumerate(rows):
        y = 105 + k * 82
        b += text(70, y, f, 34, GR, 'start', weight=700) + text(300, y, v, 38, DK, 'start', weight=800)
        if k:
            b += f'<line x1="60" y1="{y-50}" x2="680" y2="{y-50}" stroke="{GL}" stroke-width="2"/>'
    steps = ['proposed', 'confirmed', 'shipped', 'received']
    x0, dx, y = 900, 230, 250
    b += f'<line x1="{x0}" y1="{y}" x2="{x0+3*dx}" y2="{y}" stroke="{GL}" stroke-width="8" stroke-linecap="round"/>'
    for k, s in enumerate(steps):
        b += check(x0 + k * dx, y, 40, OR)
        b += text(x0 + k * dx, y + 100, s, 32, DK, weight=700)
    b += text(x0 + 1.5 * dx, 120, 'signed by both sides, on-chain', 34, GR, weight=700)
    return svg(W, H, b)


def pill(cx, cy, label, w=240, fill=CARD, stroke=DK):
    return (f'<rect x="{cx-w/2}" y="{cy-35}" width="{w}" height="70" rx="35" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
            + head(cx - w / 2 + 40, cy - 12, 12, GR) + text(cx + 18, cy + 11, label, 30, DK, weight=700))


def cylinder(cx, cy, rx, h, fill=PALE, stroke=OR):
    ry = rx * .3
    return (f'<path d="M{cx-rx} {cy-h/2} V{cy+h/2} a{rx} {ry} 0 0 0 {2*rx} 0 V{cy-h/2}" fill="{fill}" stroke="{stroke}" stroke-width="5"/>'
            f'<ellipse cx="{cx}" cy="{cy-h/2}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="5"/>')


def lock(cx, cy, s, color=DK):
    return (f'<path d="M{cx-.3*s} {cy} v{-.25*s} a{.3*s} {.3*s} 0 0 1 {.6*s} 0 v{.25*s}" fill="none" stroke="{color}" stroke-width="{s/9:.0f}"/>'
            f'<rect x="{cx-.45*s}" y="{cy}" width="{.9*s}" height="{.65*s}" rx="{s/10:.0f}" fill="{color}"/>')


def trust_vis():
    """Competing firms write to one log; the regulator reads it; nobody rewrites it; prices stay off-chain."""
    W, H = 1660, 560
    b = ''
    writers = [('Farm', 290), ('Importer', 560), ('Dairy', 830), ('Retailer', 1100)]
    blocks = [200 + k * 175 for k in range(6)]
    cy = 270
    for lab, x in writers:
        b += f'<line x1="{x}" y1="105" x2="{x}" y2="{cy-62}" stroke="{GL}" stroke-width="5" stroke-dasharray="4 10" stroke-linecap="round"/>'
        b += f'<path d="M{x} {cy-50} l-12 -20 h24 z" fill="{GL}"/>'
    for k, x in enumerate(blocks):
        if k:
            b += f'<line x1="{x-55}" y1="{cy}" x2="{x}" y2="{cy}" stroke="{DK}" stroke-width="6"/>'
        b += f'<rect x="{x}" y="{cy-45}" width="120" height="90" rx="14" fill="{OR if k == 5 else CARD}" stroke="{DK}" stroke-width="4"/>'
    for lab, x in writers:
        b += pill(x, 70, lab, 230)
    b += text(1280, 82, 'competitors write', 34, GR, 'start', weight=700)
    b += lock(1300, cy - 20, 50) + text(1350, cy + 12, 'nobody rewrites', 34, GR, 'start', weight=700)
    mx = 650
    b += f'<line x1="{mx}" y1="{430}" x2="{mx}" y2="{cy+62}" stroke="{GL}" stroke-width="5" stroke-dasharray="4 10" stroke-linecap="round"/>'
    b += f'<path d="M{mx} {cy+50} l-12 20 h24 z" fill="{GL}"/>'
    b += pill(mx, 470, 'Regulator', 260, PALE, OR)
    b += text(mx + 160, 482, 'reads', 34, GR, 'start', weight=700)
    b += cylinder(1330, 460, 60, 70, LT, GR) + text(1410, 450, 'prices, contracts:', 30, GR, 'start', weight=700)
    b += text(1410, 490, 'off-chain', 30, GR, 'start', weight=700)
    return svg(W, H, b)


BATCHES = (('A', 40, 3), ('B', 30, 7), ('C', 30, 13))
PER_DAY = 8
BCOL = {'A': '#1F4E8C', 'B': BLUE, 'C': '#9DC0E8'}


def milk_series(expiry=True):
    """The depletion algorithm: drop expired batches, record stock per batch, use the first-to-expire first."""
    bs = {n: [q, e] for n, q, e in BATCHES}
    out, day = [], 0
    while True:
        lost = {}
        if expiry:
            for n, (q, e) in bs.items():
                if e <= day and q > 0:
                    lost[n] = q
                    bs[n][0] = 0
        out.append((day, {n: q for n, (q, _) in bs.items()}, lost))
        if sum(q for q, _ in bs.values()) == 0:
            return out
        need = PER_DAY
        for n in sorted(bs, key=lambda n: bs[n][1]):
            take = min(need, bs[n][0])
            bs[n][0] -= take
            need -= take
        day += 1


def carton(cx, cy, s, color, letter):
    return (f'<path d="M{cx-.4*s} {cy-.3*s} L{cx-.25*s} {cy-.6*s} H{cx+.25*s} L{cx+.4*s} {cy-.3*s} V{cy+.6*s} H{cx-.4*s} Z" '
            f'fill="{color}" stroke="{DK}" stroke-width="4" stroke-linejoin="round"/>'
            + text(cx, cy + .32 * s, letter, .5 * s, '#fff', weight=800))


def milk_vis():
    W, H = 1660, 560
    ser = milk_series()
    b = text(40, 50, 'in stock', 32, GR, 'start', weight=700)
    for k, (n, q, e) in enumerate(BATCHES):
        y = 140 + k * 125
        b += carton(80, y, 90, BCOL[n], n)
        b += text(150, y - 4, f'{q} liters', 34, DK, 'start', weight=800)
        b += text(150, y + 38, f'good until day {e}', 28, GR, 'start')
    b += text(40, 530, f'we drink {PER_DAY} a day', 34, DK, 'start', weight=800)
    base, unit, bw, gap, x0 = 470, 3.6, 62, 30, 560
    b += text(x0, 50, 'liters left, day by day', 32, GR, 'start', weight=700)
    for d, left, lost in ser:
        x = x0 + d * (bw + gap)
        y = base
        for n, _, _ in BATCHES:
            if left[n]:
                b += f'<rect x="{x}" y="{y-left[n]*unit}" width="{bw}" height="{left[n]*unit}" fill="{BCOL[n]}"/>'
                y -= left[n] * unit
        for n, q in lost.items():
            b += f'<rect x="{x}" y="{y-q*unit}" width="{bw}" height="{q*unit}" fill="none" stroke="{LIE}" stroke-width="4" stroke-dasharray="8 6"/>'
            b += text(x + bw / 2, y - q * unit - 16, 'expired', 28, LIE, weight=800)
        b += text(x + bw / 2, base + 40, str(d), 28, GR)
    end = ser[-1][0]
    xe = x0 + end * (bw + gap) + bw / 2
    b += f'<line x1="{x0-10}" y1="{base}" x2="{xe+bw}" y2="{base}" stroke="{GL}" stroke-width="4"/>'
    b += text(xe, base - 24, 'out', 34, OR, weight=800)
    b += text(x0 + 5 * (bw + gap), base + 84, 'day', 30, GR, weight=700)
    return svg(W, H, b), end, milk_series(False)[-1][0]


def banana(cx, cy, r):
    return (f'<path d="M{cx-r} {cy-.35*r} Q{cx} {cy+.9*r} {cx+r} {cy-.35*r}" fill="none" stroke="{GOLD}" '
            f'stroke-width="{.42*r:.0f}" stroke-linecap="round"/>'
            f'<line x1="{cx+r}" y1="{cy-.35*r}" x2="{cx+1.1*r}" y2="{cy-.55*r}" stroke="#7A5C12" stroke-width="{.18*r:.0f}" stroke-linecap="round"/>')


def sack(cx, cy, r):
    return (f'<path d="M{cx-.55*r} {cy-.6*r} Q{cx-r} {cy+.2*r} {cx-.8*r} {cy+.9*r} H{cx+.8*r} Q{cx+r} {cy+.2*r} {cx+.55*r} {cy-.6*r} Z" '
            f'fill="{CARD}" stroke="{DK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M{cx-.55*r} {cy-.6*r} l{.2*r} {-.35*r} h{.7*r} l{.2*r} {.35*r}" fill="none" stroke="{DK}" stroke-width="5" stroke-linejoin="round"/>'
            + text(cx, cy + .45 * r, 'FLOUR', .36 * r, GR, weight=800))


def bread_vis():
    """Zoom into one node of the network: what is in its warehouse, and what it can bake from it."""
    W, H = 1660, 560
    b = ''
    b += link(250, 150, 410, 280, GR) + link(250, 410, 410, 280, GR)
    b += text(262, 128, 'flour', 26, GR, 'start', weight=700) + text(262, 452, 'bananas', 26, GR, 'start', weight=700)
    b += box(140, 150, 'Mill', 220, 70, size=28) + box(140, 410, 'Importer', 220, 70, size=28)
    b += box(520, 280, 'Bakery', 220, 80, fill=PALE, stroke=OR, size=30)
    px0, px1 = 720, 1640
    b += (f'<path d="M630 242 L{px0} 20 M630 318 L{px0} 540" stroke="{OR}" stroke-width="3" stroke-dasharray="8 8"/>'
          f'<rect x="{px0}" y="20" width="{px1-px0}" height="520" rx="24" fill="{CARD}" stroke="{OR}" stroke-width="5"/>')
    b += text(px0 + 40, 80, 'inside the bakery', 32, GR, 'start', weight=700)
    b += text(1120, 80, 'enough for', 32, GR, 'start', weight=700)
    rows = [(200, 'sack', '300 cups', '2 per loaf', 150, GR), (390, 'banana', '6 bananas', '3 per loaf', 2, OR)]
    scale = 380 / 150
    for y, ic, have, per, loaves, col in rows:
        b += sack(px0 + 80, y, 52) if ic == 'sack' else banana(px0 + 80, y, 50)
        b += text(px0 + 160, y - 2, have, 38, DK, 'start', weight=800)
        b += text(px0 + 160, y + 40, per, 30, GR, 'start')
        w = max(loaves * scale, 14)
        b += f'<rect x="1120" y="{y-32}" width="{w:.0f}" height="64" rx="10" fill="{col}"/>'
        if loaves > 20:
            b += text(1120 + w - 18, y + 12, f'{loaves} loaves', 34, '#fff', 'end', weight=800)
        else:
            b += text(1120 + w + 22, y + 12, f'{loaves} loaves', 38, OR, 'start', weight=800)
    return svg(W, H, b)


def cascade_vis(step):
    """step 0: the network; 1: Russia cut, the loss travels downstream; 2: another supplier covers it."""
    W, H, bw = 1680, 520, 300
    N = {'ru': ('Russian supplier', 170, 110), 'el': ('Other supplier', 170, 400),
         'imp': ('Fruit importer', 640, 110), 'whs': ('Wholesaler', 640, 400),
         'bak': ('Bakery', 1110, 110), 'groc': ('Grocery', 1500, 300)}
    E = [('ru', 'imp', 'bananas'), ('imp', 'bak', 'bananas'), ('bak', 'groc', 'banana bread'),
         ('el', 'whs', ''), ('whs', 'groc', '')]
    hit = {'imp', 'bak'} if step == 1 else set()
    b = ''
    for a, c, lab in E:
        _, xa, ya = N[a]
        _, xc, yc = N[c]
        red = step >= 1 and a in ('ru', 'imp', 'bak') and (step == 1 or a == 'ru')
        b += link(xa + bw / 2, ya, xc - bw / 2, yc, LIE if red else GR,
                  dash='stroke-dasharray="14 10"' if red else '')
        if lab and ya == yc:
            b += text((xa + xc) / 2, ya - 18, lab, 28, LIE if red else GR, weight=700)
        elif lab:
            b += text(xa + bw / 2 + 24, ya - 30, lab, 28, LIE if red else GR, 'start', weight=700)
    if step == 2:
        _, xa, ya = N['el']
        _, xc, yc = N['imp']
        b += link(xa + bw / 2, ya, xc - bw / 2, yc, GREEN, w=8)
        b += text((xa + xc) / 2 + 30, (ya + yc) / 2 + 10, 'bananas', 28, GREEN, 'start', weight=800)
    for k, (lab, x, y) in N.items():
        if k == 'ru' and step >= 1:
            b += box(x, y, lab, bw, fill=SOFTRED, stroke=LIE, fg=GR)
            cx, cy = x + bw / 2 - 6, y - 40
            b += (f'<circle cx="{cx}" cy="{cy}" r="26" fill="{LIE}"/>'
                  f'<path d="M{cx-10} {cy-10} l20 20 M{cx+10} {cy-10} l-20 20" stroke="#fff" stroke-width="6" stroke-linecap="round"/>')
        elif k in hit:
            b += box(x, y, lab, bw, fill=SOFTRED, stroke=LIE)
        elif step == 2 and k in ('imp', 'bak'):
            b += box(x, y, lab, bw, fill=SOFTGREEN, stroke=GREEN)
        else:
            b += box(x, y, lab, bw)
    if step == 1:
        b += text(1110, 200, 'no bananas', 32, LIE, weight=800)
    return svg(W, H, b)


def whatif_vis():
    """A dashboard: switch off a source, compare today with the what-if."""
    W, H = 1600, 440
    b = f'<rect x="20" y="20" width="1560" height="400" rx="26" fill="{CARD}" stroke="{DK}" stroke-width="4"/>'
    for k, (lab, on) in enumerate([('Imports from A', False), ('Region B', True), ('Supplier C', True)]):
        y = 110 + k * 110
        b += text(80, y + 12, lab, 32, DK, 'start', weight=700)
        b += f'<rect x="380" y="{y-26}" width="96" height="52" rx="26" fill="{GREEN if on else GL}"/>'
        b += f'<circle cx="{454 if on else 402}" cy="{y}" r="20" fill="#fff"/>'
    b += f'<line x1="560" y1="60" x2="560" y2="380" stroke="{GL}" stroke-width="3"/>'
    X = lambda d: 640 + d * 72
    Y = lambda v: 360 - v * 2.6
    today = [100, 98, 97, 95, 94, 93, 91, 90, 89, 88, 86]
    whatif = [100, 92, 83, 74, 66, 57, 49, 41, 32, 24, 16]
    for ser, col, dash in [(today, DK, ''), (whatif, OR, 'stroke-dasharray="16 10"')]:
        pts = ' '.join(f'{X(d)},{Y(v)}' for d, v in enumerate(ser))
        b += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" {dash}/>'
    b += text(X(10) + 20, Y(86) + 10, 'today', 32, DK, 'start', weight=800)
    b += text(X(10) + 20, Y(16) + 10, 'what if', 32, OR, 'start', weight=800)
    b += f'<line x1="620" y1="{Y(0)}" x2="{X(10)}" y2="{Y(0)}" stroke="{GL}" stroke-width="3"/>'
    return svg(W, H, b)


# ---------- slides ----------
def deco(name, dark=False, cls='deco'):
    return f'<img class="{cls}" src="img/{name}{"-dark" if dark else ""}.svg" alt="">'


def logo(name, h=72, style=''):
    """Organization logo, if its file was dropped into img/ (logo-<name>.svg or .png)."""
    for ext in ('svg', 'png'):
        if os.path.exists(os.path.join(HERE, '..', 'img', f'logo-{name}.{ext}')):
            return f'<img src="img/logo-{name}.{ext}" alt="" style="height:{h}px;{style}">'
    return ''


TITLE = '''
<section class="slide dark center">
  <p class="eyebrow">MidChain DeFi Conference</p>
  <h1>Metric-Based Voting</h1>
  <p class="big muted">Designing Rules for Ecosystem Resource Allocation</p>
  <p class="hl">…and first: food security on a blockchain</p>
  <p class="ref" style="bottom:128px;font-size:32px">Nimrod Talmon</p>
  <p class="ref">Ben-Gurion University of the Negev · October 26, 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>'''

slides = [TITLE]
S = slides.append

# ===== Part 1: food security on a blockchain (~10 min) =====
S('''<section class="slide dark center">
  <p class="eyebrow">Part 1</p>
  <h1>Food security<br>on a blockchain</h1>
  <p class="ref" style="bottom:128px;font-size:32px">with Bar Hoter, Moran Koren, Dorit Nitzan, Stav Shapira (+ Adir Even and Max Gluhov)</p>
  <p class="ref">Supported by the Israeli Ministry of Science and Technology</p>
</section>''')

S(f'''<section class="slide light">
  <h2>Pandemics and wars break food supply chains</h2>
  <div style="margin-block:auto">{crisis_vis()}</div>
  <div style="display:flex;align-items:center;gap:36px">
    {houses_small()}
    <p class="muted" style="font-size:40px">Also today: 1 in 4 households in Israel is food insecure</p>
  </div>
  <p class="ref">National Insurance Institute of Israel, Food Security Report 2024 (published 2025)</p>
</section>''')

S('''<section class="slide light">
  <h2>Goal: see the whole food system, live</h2>
  <div class="flow">
    <div class="step"><b style="font-size:56px">1 · Record</b><span style="font-size:40px">every hand-off,<br>on-chain</span></div>
    <span class="arrow" style="font-size:72px">→</span>
    <div class="step" style="flex:1.6"><b style="font-size:56px">2 · Ask</b>
      <span style="font-size:40px">How long will it last?<br>What can we still make?<br>What if a source is cut?</span></div>
  </div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">1 · Record</p>
  <h2>Food moves along a network of hand-offs</h2>
  <div style="margin-block:auto">{network_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">1 · Record</p>
  <h2>Every hand-off is a record</h2>
  <div style="margin-block:auto">{record_vis()}</div>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">1 · Record</p>
  <h2>Why on-chain, for food?</h2>
  <div style="margin-block:auto">{trust_vis()}</div>
  <p class="ref">And the Ministry of Science asked for it</p>
</section>''')

MILK, MILK_OUT, MILK_NOEXP = milk_vis()
S(f'''<section class="slide light">
  <p class="eyebrow">2 · Ask</p>
  <h2>How long will the milk last?</h2>
  <div style="margin-block:auto 0">{MILK}</div>
  <p class="hl big" style="align-self:flex-start;margin-block:0 auto">Expiry counts: out on day {MILK_OUT}, not day {MILK_NOEXP}</p>
</section>''')

S(f'''<section class="slide light">
  <p class="eyebrow">2 · Ask</p>
  <h2>What can each producer still make?</h2>
  <div style="margin-block:auto 0">{bread_vis()}</div>
  <p class="hl big" style="align-self:flex-start;margin-block:0 auto">The scarcest input decides</p>
</section>''')

for k in range(3):
    S(f'''<section class="slide light">
  <p class="eyebrow">2 · Ask</p>
  <h2>What if we lose Russia?</h2>
  <div style="margin-block:auto 0">{cascade_vis(k)}</div>
  <p class="hl big" style="align-self:flex-start;margin-block:0 auto;{"" if k == 2 else "visibility:hidden"}">Bananas from elsewhere: the bakery is covered</p>
</section>''')

S('''<section class="slide dark">
  <h2>Where it stands</h2>
  <div style="display:flex;gap:40px;align-items:flex-start;margin-block:auto 0">
    <div style="display:flex;flex-direction:column;gap:16px">
      <div class="shot"><img src="img/food-nutrition.png" alt="" style="height:320px"></div>
      <p class="muted small">Nutrition per person, by city</p></div>
    <div style="display:flex;flex-direction:column;gap:16px">
      <div class="shot"><img src="img/food-flows.jpg" alt="" style="height:320px"></div>
      <p class="muted small">Who supplies bananas to whom</p></div>
  </div>
  <p style="margin-block:0 auto">Prototype on an Ethereum testnet, with synthetic data</p>
  <p class="ref">Hoter, Koren, Nitzan, Shapira, Talmon · IEEE ISCC 2025</p>
</section>''')

S(f'''<section class="slide light">
  <h2>Now: a real BI with a what-if simulator</h2>
  <div style="margin-block:auto 0">{whatif_vis()}</div>
  <p class="hl big" style="align-self:flex-start;margin-block:0 auto">Interested? Let's talk, and stay in touch for updates</p>
</section>''')

# ===== Part 2: metric-based voting =====
S('''<section class="slide dark center">
  <p class="eyebrow">Part 2</p>
  <h1>Metric-based voting</h1>
  <p class="ref" style="bottom:128px;font-size:32px">with Eyal Briman</p>
</section>''')

S(f'''<section class="slide light center">
  <h1 class="q">A pot of money,<br>many projects.<br>Who gets what?</h1>
  <div style="position:absolute;right:110px;top:50%;transform:translateY(-50%)">{pot_vis()}</div>
</section>''')

BUBBLE = f'''<span style="position:absolute;left:50%;bottom:calc(100% + 34px);transform:translateX(-30%);
  display:flex;align-items:center;gap:22px;white-space:nowrap;background:var(--light);color:var(--dark);
  font-size:40px;font-weight:700;padding:18px 32px;border-radius:28px">
  {svg(150, 50, fishbone(4, 25, 1), "display:block")}Smells funny…
  <span style="position:absolute;left:30%;top:100%;border:18px solid transparent;border-top-color:var(--light)"></span>
</span>'''

S(f'''<section class="slide dark">
  <h2 style="display:flex;align-items:center;gap:32px">{logo('op', 80)}Optimism Retro Funding</h2>
  <p class="big">Over $100M in four rounds, and a new voting rule every round</p>
  <div class="chips" style="margin-block:auto">
    <span class="chip">Quadratic</span><span class="arrow">→</span>
    <span class="chip">Mean</span><span class="arrow">→</span>
    <span class="chip">Quorum median</span><span class="arrow">→</span>
    <span style="position:relative"><span class="chip on">Capped median</span>{BUBBLE}</span>
  </div>
  <p class="ref">Briman, Talmon, Kreitenweis, Idrees 2025</p>
</section>''')

S(f'''<section class="slide accent center">
  <h1 class="q">Which rule is the right one?</h1>
  <p class="big">This is what social choice studies</p>
  {deco('scale', True, 'deco sm')}
</section>''')

S(f'''<section class="slide light">
  <h2>We looked at Optimism's rules</h2>
  <div class="rows ruled" style="margin-block:auto 0">
    <div class="row"><span class="k">Found</span><p>The median rules invite strategic voting</p></div>
    <div class="row"><span class="k">Suggested</span><p>Moving phantoms: artificial voters so that lying never pays</p></div>
  </div>
  <div style="margin-block:0 auto">{phantoms_vis()}</div>
  <p class="ref">Freeman, Pennock, Peters, Wortman Vaughan 2019 · Briman, Talmon, Kreitenweis, Idrees 2025</p>
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
    <div class="card top"><h3 style="display:flex;align-items:center;gap:20px">{logo('oecd', 56)}OECD Better Life Index</h3>
      <p><b>Rank countries:</b> weight 11 topics</p></div>
    <div class="card top"><h3 style="display:flex;align-items:center;gap:20px">{logo('erc', 56)}ERC</h3>
      <p><b>Rank grants:</b> ambition, feasibility, PI</p></div>
  </div>
  {deco('globe', cls='deco sm')}
</section>''')

S('''<section class="slide dark center">
  <p class="eyebrow">The model</p>
  <h1>Metric-based voting</h1>
</section>''')

for k in range(1, 6):
    S(f'''<section class="slide light">
  <h2>How it works</h2>
  <div style="margin-block:auto">{how_it_works(k)}</div>
</section>''')

S(f'''<section class="slide light">
  <h2>What a ballot looks like</h2>
  <div style="margin-block:auto">{ballot_formats()}</div>
</section>''')

for show in (False, True):
    S(f'''<section class="slide light">
  <h2>From ballots to one weight: mean or median?</h2>
  <div style="margin-block:auto">{mean_median_vis(show)}</div>
</section>''')

S('''<section class="slide dark">
  <h2>Next: mean vs. median, on three fronts</h2>
  <div class="cards">
    <div class="card top"><h3>Lying</h3><p>Neither is safe</p></div>
    <div class="card top"><h3>Hitting a target</h3><p>Depends on the ballot</p></div>
    <div class="card top"><h3>Copying metrics</h3><p>Mean often immune</p></div>
  </div>
</section>''')

S(f'''<section class="slide dark center">
  <p class="eyebrow">Strategic voting</p>
  <h1>Can a voter gain by lying?</h1>
  {deco('ballot')}
</section>''')

S(f'''<section class="slide light">
  <h2>The office thermostat</h2>
  <div style="margin-block:auto">{thermo_pair('mean', False)}</div>
  {deco('thermo', cls='deco sm')}
</section>''')

S(f'''<section class="slide light">
  <h2>Cat says 32°: the mean moves</h2>
  <div style="margin-block:auto">{thermo_pair('mean', True)}</div>
</section>''')

S(f'''<section class="slide light">
  <h2>Cat says 32°: the median does not</h2>
  <div style="margin-block:auto">{thermo_pair('median', True)}</div>
</section>''')

S('''<section class="slide accent center">
  <h1 class="q">So a median per metric is safe too?</h1>
</section>''')

S(f'''<section class="slide light">
  <h2>A project worth 1 on Planet and on Energy</h2>
  <div style="margin-block:auto">{ann_table(False)}</div>
</section>''')

S(f'''<section class="slide light">
  <h2>A project worth 1 on Planet and on Energy</h2>
  <div style="margin-block:auto">{ann_table(True)}</div>
</section>''')

S(f'''<section class="slide dark">
  <h2>Why</h2>
  <p class="big">Ann cares about the score, not about each weight</p>
  <p class="big muted">She lost on Planet, so she bought it back on Energy</p>
  <p class="big hl" style="margin-top:auto;margin-bottom:auto">No sensible metric-by-metric rule is safe from this</p>
  {deco('scale', cls='deco sm')}
</section>''')

S('''<section class="slide accent center">
  <h1 class="q">Lying can pay.<br>How hard is it to find the lie?</h1>
</section>''')

S(f'''<section class="slide light">
  <h2>Searching for the right lie</h2>
  <div style="margin-block:auto">{search_vis()}</div>
  <div class="cols" style="margin:0;gap:40px">
    <p>One smooth region: <b>easy</b> to search</p>
    <p>Scattered islands: a <b>hard</b> puzzle</p>
  </div>
</section>''')

S(f'''<section class="slide dark center">
  <p class="eyebrow">The platform's choices</p>
  <h1>Duplicate metrics</h1>
  <p class="big muted">Round 4: gas fees, and also log gas fees</p>
  {deco('clone', cls='deco sm')}
</section>''')

S(f'''<section class="slide light">
  <h2>Three voters, one Fees metric</h2>
  <div style="margin-block:auto">{clone_vis(False)}</div>
  <p class="hl big" style="align-self:flex-start;visibility:hidden">The median doubled Fees</p>
</section>''')

S(f'''<section class="slide light">
  <h2>Add a copy. Same opinions.</h2>
  <div style="margin-block:auto">{clone_vis(True)}</div>
  <p class="hl big" style="align-self:flex-start">The median doubled Fees</p>
</section>''')

S(f'''<section class="slide light">
  <h2>Four levers, four ballot types</h2>
  <div style="margin-block:auto">{landscape_vis()}</div>
  <p class="hl big" style="align-self:flex-start">Which rule is harder to steer depends on the ballot</p>
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
