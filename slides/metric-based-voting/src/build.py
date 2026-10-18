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
  <p class="ref" style="bottom:128px;font-size:32px">Nimrod Talmon · joint work with Eyal Briman</p>
  <p class="ref">Ben-Gurion University of the Negev · October 26, 2026</p>
  <img class="deco" src="../assets/img/deco-network.svg" alt="">
</section>'''

slides = [TITLE]
S = slides.append

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
  <aside>Rounds 1–4. Picking a rule is hard even for a careful community.</aside>
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
  <aside>Rounds 3 and 4 are not strategyproof. Utilitarian moving phantoms: add phantom ballots whose positions move with a single parameter; strategyproof and maximizes L1 welfare.</aside>
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

HOW_NOTES = [
    'Start from the metrics: what counts. Here: helping the planet, fees (money), energy.',
    'Each voter says how much each metric matters.',
    'The rule turns the ballots into one weight per metric. This is the object we study: rules that aggregate weights first, metric by metric. (Optimism Round 4 did it the other way: a median per project, then rescaling. Under the mean the order does not matter; under the median it does.)',
    'Each project has a public value on each metric.',
    'Each project gets the weighted sum: its values times the weights. Colors show which metric earned what.',
]
for k in range(1, 6):
    S(f'''<section class="slide light">
  <h2>How it works</h2>
  <div style="margin-block:auto">{how_it_works(k)}</div>
  <aside>{HOW_NOTES[k-1]}</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>What a ballot looks like</h2>
  <div style="margin-block:auto">{ballot_formats()}</div>
</section>''')

for show in (False, True):
    S(f'''<section class="slide light">
  <h2>From ballots to one weight: mean or median?</h2>
  <div style="margin-block:auto">{mean_median_vis(show)}</div>
  <aside>{"Mean: what composite indices typically use. Median: what social choice usually recommends." if show else "Three voters on one metric. How do we get one weight?"}</aside>
</section>''')

S('''<section class="slide dark">
  <h2>Next: mean vs. median, on three fronts</h2>
  <div class="cards">
    <div class="card top"><h3>Lying</h3><p>Neither is safe</p></div>
    <div class="card top"><h3>Hitting a target</h3><p>Depends on the ballot</p></div>
    <div class="card top"><h3>Copying metrics</h3><p>Mean often immune</p></div>
  </div>
  <aside>Lying: no metric-by-metric rule is strategyproof. Hitting a target: which rule is harder to steer depends on the ballot type. Copying metrics: under the mean, copies cannot change any score with cumulative or plurality ballots; the median can be moved.</aside>
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
  <aside>Everyone states a temperature; the thermostat sets the mean.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Cat says 32°: the mean moves</h2>
  <div style="margin-block:auto">{thermo_pair('mean', True)}</div>
  <aside>The mean rewards exaggerating. No surprise.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Cat says 32°: the median does not</h2>
  <div style="margin-block:auto">{thermo_pair('median', True)}</div>
  <aside>On one dimension, nobody gains by lying to the median.</aside>
</section>''')

S('''<section class="slide accent center">
  <h1 class="q">So a median per metric is safe too?</h1>
</section>''')

S(f'''<section class="slide light">
  <h2>A project worth 1 on Planet and on Energy</h2>
  <div style="margin-block:auto">{ann_table(False)}</div>
  <aside>Ann truthfully cares only about Planet, so she wants this project's score to be 1. Medians are 0 and 0, score 0.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>A project worth 1 on Planet and on Energy</h2>
  <div style="margin-block:auto">{ann_table(True)}</div>
  <aside>Ann says Energy matters too. The Energy median becomes 1, the score becomes 1: exactly what she wanted.</aside>
</section>''')

S(f'''<section class="slide dark">
  <h2>Why</h2>
  <p class="big">Ann cares about the score, not about each weight</p>
  <p class="big muted">She lost on Planet, so she bought it back on Energy</p>
  <p class="big hl" style="margin-top:auto;margin-bottom:auto">No sensible metric-by-metric rule is safe from this</p>
  {deco('scale', cls='deco sm')}
  <aside>Theorem: no rule on fractional ballots is value-blind, metric-wise separable, metric-neutral, anonymous, unanimous, and strategyproof.</aside>
</section>''')

S('''<section class="slide accent center">
  <h1 class="q">Lying can pay.<br>How hard is it to find the lie?</h1>
  <aside>Exact score reachability: given a target scorecard, can some ballot produce it? Also an auditor's and a designer's question.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Searching for the right lie</h2>
  <div style="margin-block:auto">{search_vis()}</div>
  <div class="cols" style="margin:0;gap:40px">
    <p>One smooth region: <b>easy</b> to search</p>
    <p>Scattered islands: a <b>hard</b> puzzle</p>
  </div>
  <aside>Mean: finding the ballot is a linear program. Median with cumulative ballots: NP-hard. (Median with fractional ballots is still easy.)</aside>
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
  <p class="hl big" style="align-self:flex-start;visibility:hidden">The median doubled Fees</p>
  <aside>Cumulative ballots; the rest of each voter's budget is on other metrics.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Add a copy. Same opinions.</h2>
  <div style="margin-block:auto">{clone_vis(True)}</div>
  <p class="hl big" style="align-self:flex-start">The median doubled Fees</p>
  <aside>Each voter splits the same Fees weight across the two copies. The mean is unchanged by any such split; the median can change. The copy has the same values, so a fee-heavy project gains twice.</aside>
</section>''')

S(f'''<section class="slide light">
  <h2>Four levers, four ballot types</h2>
  <div style="margin-block:auto">{landscape_vis()}</div>
  <p class="hl big" style="align-self:flex-start">Which rule is harder to steer depends on the ballot</p>
  <aside>Exact score reachability. Easy: polynomial time. Hard: NP-hard (worst case). No effect: copying cannot change any score. Shared hardness holds already with one voter.</aside>
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
