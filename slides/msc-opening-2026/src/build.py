#!/usr/bin/env python3
"""Builds slides/msc-opening-2026/index.html (Hebrew, RTL; shares ../assets/deck.css and deck.js)."""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'index.html')
OR, DK, GR, GL, PALE = '#F7941D', '#26282C', '#5F6368', '#B9BCC1', '#FCE8D2'

# ---------- icons (24x24, stroked) ----------
ICONS = {
    'cap': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    'bulb': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14a5 5 0 0 1 5 5"/>',
    'badge': '<rect x="5" y="3" width="14" height="18" rx="2"/><circle cx="12" cy="10" r="2.5"/><path d="M8.5 17a3.5 3.5 0 0 1 7 0"/>',
    'tree': '<circle cx="12" cy="5" r="2"/><path d="M12 7v5M5 17v-3c0-1 1-2 2-2h10c1 0 2 1 2 2v3M12 12v5"/><circle cx="5" cy="19" r="2"/><circle cx="12" cy="19" r="2"/><circle cx="19" cy="19" r="2"/>',
    'layers': '<path d="M12 3 2 8l10 5 10-5z"/><path d="M2 13l10 5 10-5"/><path d="M2 18l10 5 10-5"/>',
    'box': '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M3 8l3-5h12l3 5M10 12h4"/>',
    'route': '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h8a3 3 0 0 0 0-6H8a3 3 0 0 1 0-6h8"/>',
    'cart': '<path d="M2 4h3l2.5 11h11L21 8H6"/><circle cx="9" cy="19.5" r="1.5"/><circle cx="18" cy="19.5" r="1.5"/>',
    'coins': '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3 3 7 3s7-1.3 7-3V6"/><path d="M5 12v6c0 1.7 3 3 7 3s7-1.3 7-3v-6"/>',
    'list': '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
    'check': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 12l2 2 4-4"/>',
    'search': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
    'pen': '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 7l3 3"/>',
    'screen': '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M12 16v4M8 20h8"/>',
    'book': '<path d="M4 4h6a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h6z"/>',
    'help': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5v.4"/><path d="M12 17h.01"/>',
    'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    'upload': '<path d="M12 15V4M7 9l5-5 5 5M4 20h16"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'medal': '<circle cx="12" cy="15" r="5"/><path d="M8 3l4 7 4-7"/>',
    'file': '<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4M9 13h6M9 17h6"/>',
    'refresh': '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v5h-5"/>',
    'flag': '<path d="M5 21V4h12l-2 4 2 4H5"/>',
    'beach': '<path d="M12 4a8 8 0 0 0-8 8h16a8 8 0 0 0-8-8z"/><path d="M12 12v7M4 21h16"/>',
    'g': '<path d="M19 12a7 7 0 1 1-2-5"/><path d="M12.5 12H19"/>',
    'atom': '<circle cx="12" cy="12" r="1.2"/><ellipse cx="12" cy="12" rx="9" ry="3.6"/><ellipse cx="12" cy="12" rx="9" ry="3.6" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="3.6" transform="rotate(120 12 12)"/>',
    'mug': '<path d="M5 6h10v13a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/><path d="M15 9h2a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-2M8.5 10v7M11.5 10v7"/>',
    'desert': '<circle cx="16" cy="8" r="3"/><path d="M2 19c4-4 6-4 10 0s6 4 10 0"/>',
}


def ic(name, size=88, bg=OR, fg='#fff'):
    """Icon in a filled circle, as inline SVG."""
    return (f'<svg class="ic" viewBox="-6 -6 36 36" width="{size}" height="{size}" aria-hidden="true">'
            f'<circle cx="12" cy="12" r="18" fill="{bg}"/>'
            f'<g fill="none" stroke="{fg}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            f'{ICONS[name]}</g></svg>')


def big_icon(name, size=420):
    """Large decorative icon on a pale disc."""
    return (f'<svg viewBox="-6 -6 36 36" width="{size}" height="{size}" aria-hidden="true">'
            f'<circle cx="12" cy="12" r="18" fill="{PALE}"/>'
            f'<g fill="none" stroke="{OR}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" '
            f'transform="translate(3.6 3.6) scale(.7)">{ICONS[name]}</g></svg>')


def hd(title, icon):
    return f'<h2 class="hd">{ic(icon)}<span>{title}</span></h2>'


def ltr(s):
    return f'<span dir="ltr">{s}</span>'


# ---------- slide 2: career path ----------
def career():
    stops = [('תל אביב', 'beach'), ('גוגל', 'g'), ('מכון ויצמן', 'atom'),
             ('ברלין', 'mug'), ('מכון ויצמן', 'atom'), ('בן-גוריון', 'desert')]
    W, H, r = 1660, 330, 54
    xs = [W - 110 - k * (W - 220) / 5 for k in range(6)]
    ys = [110 if k % 2 == 0 else 190 for k in range(6)]
    b = ''
    for k in range(5):
        b += (f'<line x1="{xs[k]}" y1="{ys[k]}" x2="{xs[k+1]}" y2="{ys[k+1]}" stroke="{GL}" '
              f'stroke-width="5" stroke-dasharray="14 12"/>')
    for k, (lab, icon) in enumerate(stops):
        last = k == 5
        b += f'<circle cx="{xs[k]}" cy="{ys[k]}" r="{r}" fill="{OR if last else DK}"/>'
        b += (f'<g transform="translate({xs[k]-27} {ys[k]-27}) scale(2.25)" fill="none" stroke="#fff" '
              f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>')
        b += (f'<text x="{xs[k]}" y="{ys[k]+r+48}" font-size="34" text-anchor="middle" fill="{DK}" '
              f'font-weight="{800 if last else 400}">{lab}</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Heebo, Arial, sans-serif">{b}</svg>'


# ---------- slide 6: credits bars ----------
SEG = {'core': (DK, '#fff'), 'spec': (GR, '#fff'), 'clu': (GL, DK), 'el': (PALE, DK), 'th': (OR, DK)}


def credit_bar(label, segs):
    out = f'<div class="cbar"><div class="clab">{label}</div><div class="segs">'
    for n, name, kind in segs:
        bg, fg = SEG[kind]
        out += f'<div class="seg" style="flex:{n};background:{bg};color:{fg}"><b>{n}</b><span>{name}</span></div>'
    return out + '</div></div>'


# ---------- slide 8: timeline ----------
def timeline():
    steps = [('שנת ההשלמות', 'סיום קורסי השלמה', 'book'),
             ('סוף סמסטר א\'', 'מנחה ונושא', 'users'),
             ('סוף שנה א\'', 'הצעת מחקר', 'file'),
             ('כל סמסטר', 'דו"ח התקדמות', 'refresh'),
             ('סוף שנה ב\'', 'הגשת תזה / סמינר מסכם', 'flag')]
    out = '<div class="tl">'
    for k, (when, what, icon) in enumerate(steps):
        last = k == len(steps) - 1
        out += (f'<div class="tstep{" on" if last else ""}">{ic(icon, 150, OR if last else DK)}'
                f'<b>{when}</b><span>{what}</span></div>')
    return out + '</div>'


EXTRA_CSS = '''
html[dir=rtl] .slide { text-align: right; }
html[dir=rtl] .slide.dark::before, html[dir=rtl] .slide.light::before { left: auto; right: 128px; }
html[dir=rtl] .deco { right: auto; left: 128px; }
.slide.middle { text-align: center !important; }
.slide.middle::before { display: none; }
.hd { display: flex; align-items: center; gap: 28px; }
.hd .ic { flex: none; }
.orange { color: var(--orange); }
.mail { font-size: 44px; font-weight: 800; color: var(--orange); }
.pills { display: flex; gap: 24px; }
.pills span { flex: 1; text-align: center; font-size: 36px; font-weight: 800; background: var(--orange-pale);
  border-radius: 14px; padding: 20px 0; }
.box { background: var(--orange-pale); border-radius: 16px; padding: 28px 40px; font-size: 48px; font-weight: 800; }
.split2 { display: flex; gap: 40px; margin-block: auto; align-items: stretch; }
.split2 > * { flex: 1; }
.people { display: flex; flex-direction: column; gap: 14px; }
.person { display: flex; align-items: center; gap: 24px; background: var(--card); border: 1px solid var(--gray-light);
  border-radius: 14px; padding: 12px 24px; }
.person b { display: block; font-size: 36px; line-height: 1.2; }
.person span { font-size: 28px; color: var(--gray); }
.panel { background: var(--dark); color: var(--light); border-radius: 16px; padding: 36px 44px;
  display: flex; flex-direction: column; gap: 6px; }
.panel h3 { color: var(--orange); font-size: 40px; margin-bottom: 14px; }
.panel .kv { display: flex; justify-content: space-between; gap: 24px; font-size: 32px; padding: 14px 0;
  border-top: 1px solid var(--gray); }
.panel .kv b { font-weight: 700; }
.panel .kv span { color: var(--gray-light); }
.tracks { display: flex; flex-direction: column; gap: 18px; }
.track { background: var(--dark2); border-radius: 12px; padding: 24px 32px; font-size: 38px; }
.spec { display: flex; align-items: center; gap: 28px; background: var(--card); border: 1px solid var(--gray-light);
  border-radius: 16px; padding: 32px 36px; flex: 1; }
.spec.hot { background: var(--orange-pale); border: none; }
.spec b { font-size: 44px; display: block; }
.spec span { font-size: 28px; color: var(--gray); }
.cbars { display: flex; flex-direction: column; gap: 48px; margin-block: auto; }
.cbar { display: flex; align-items: center; gap: 40px; }
.clab { width: 220px; flex: none; font-size: 44px; font-weight: 800; }
.segs { flex: 1; display: flex; gap: 6px; height: 170px; }
.seg { border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; padding: 0 6px; gap: 4px; overflow: hidden; }
.seg b { font-size: 60px; line-height: 1; }
.seg span { font-size: 24px; font-weight: 700; line-height: 1.15; }
.note { font-size: 34px; color: var(--gray); background: var(--card); border: 1px solid var(--gray-light);
  border-radius: 14px; padding: 22px 32px; }
.cols3 { display: flex; gap: 32px; margin-block: auto; align-items: stretch; }
.col { flex: 1; border-radius: 16px; padding: 40px; display: flex; flex-direction: column; gap: 22px; }
.col.dk { background: var(--dark); color: var(--light); }
.col.lt { background: var(--card); border: 1px solid var(--gray-light); }
.col h3 { font-size: 44px; color: var(--orange); }
.col.lt h3 { color: var(--dark); }
.col p { font-size: 34px; line-height: 1.3; }
.col p + p { padding-top: 22px; border-top: 1px solid var(--gray-light); }
.col.dk p + p { border-top-color: var(--gray); }
.tl { display: flex; margin-block: auto; position: relative; }
.tl::before { content: ""; position: absolute; top: 75px; left: 10%; right: 10%; height: 6px;
  background: var(--gray-light); border-radius: 3px; }
.tstep { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center; position: relative; }
.tstep b { font-size: 40px; margin-top: 12px; }
.tstep span { font-size: 32px; color: var(--gray); }
.tstep.on b { color: var(--orange); }
.shop { display: flex; gap: 96px; align-items: center; margin-block: auto; }
.shop .rows2 { flex: 1; display: flex; flex-direction: column; gap: 30px; }
.shop .r { display: flex; align-items: center; gap: 32px; }
.shop .r b { font-size: 42px; display: block; line-height: 1.2; }
.shop .r span { font-size: 32px; color: var(--gray); }
.shop .side { flex: none; display: flex; flex-direction: column; align-items: center; gap: 36px; }
.shop .side p { font-size: 40px; font-weight: 800; text-align: center; }
.submit { display: flex; flex-direction: column; align-items: center; gap: 10px; margin-block: auto; font-weight: 800; }
.submit .s1 { font-size: 80px; color: var(--gray); }
.submit .s2 { font-size: 120px; }
.submit .s3 { font-size: 220px; color: var(--orange); line-height: 1.1; }
table.reg { border-collapse: separate; border-spacing: 0 10px; width: 100%; margin-block: auto; font-size: 36px; }
table.reg th { background: var(--dark); color: var(--light); font-size: 32px; padding: 20px 32px; text-align: right; }
table.reg th:first-child { border-radius: 0 12px 12px 0; }
table.reg th:last-child { border-radius: 12px 0 0 12px; }
table.reg td { background: var(--card); padding: 22px 32px; border-top: 1px solid var(--gray-light);
  border-bottom: 1px solid var(--gray-light); }
table.reg td:first-child { font-weight: 800; border-right: 1px solid var(--gray-light); border-radius: 0 12px 12px 0; }
table.reg td:last-child { color: var(--gray); border-left: 1px solid var(--gray-light); border-radius: 12px 0 0 12px; }
table.reg td.num { font-weight: 700; }
.rules { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-block: auto; }
.rule { display: flex; align-items: center; gap: 28px; background: var(--card); border: 1px solid var(--gray-light);
  border-radius: 14px; padding: 22px 30px; font-size: 36px; line-height: 1.25; }
.rule.hot { background: var(--orange-pale); border: none; }
.cat { display: flex; gap: 96px; align-items: center; margin-block: auto; }
.cat-text { flex: 1; display: flex; flex-direction: column; gap: 48px; }
.qr { text-decoration: none; border: 3px solid var(--orange); }
.qr span { font-size: 30px; }
.who { display: flex; gap: 32px; }
.who .person { flex: 1; padding: 24px 32px; }
.person.big b { font-size: 44px; }
.person.big span { font-size: 32px; }
.rules.one { grid-template-columns: 1fr; }
.cbars.simple .seg span { font-size: 36px; }
.cbars.simple .seg b { font-size: 72px; }
.rules.one .rule { font-size: 44px; padding: 26px 36px; }
'''

# ---------- slides ----------
TITLE = f'''<section class="slide dark middle">
  <div style="align-self:center">{ic('cap', 190)}</div>
  <h1>מפגש פתיחה תשפ"ז</h1>
  <p class="big orange">תואר שני · הנדסת תעשייה וניהול</p>
  <p class="big orange" style="font-size:48px">פרופ' נמרוד טלמון</p>
  <p class="muted" style="margin-top:40px;font-size:34px">אוניברסיטת בן-גוריון בנגב · אוקטובר 2026</p>
</section>'''

slides = [TITLE]
S = slides.append

S(f'''<section class="slide light">
  {hd('מי אני', 'user')}
  <div>
    <h3>פרופ' נמרוד טלמון</h3>
    <p class="muted">יו"ר ועדת הוראה לתואר שני</p>
    <p class="mail">{ltr('IEMGrad@bgu.ac.il')}</p>
  </div>
  <div class="pills"><span>דמוקרטיה דיגיטלית</span><span>{ltr('Cooperative AI')}</span><span>ממשל בבלוקצ'יין</span></div>
  <div style="margin-top:-12px">{career()}</div>
</section>''')

S(f'''<section class="slide light">
  {hd('ברוכים הבאים', 'bulb')}
  <div style="margin-block:auto;display:flex;flex-direction:column;gap:24px;max-width:1020px">
    <p class="big muted">תואר שני זה קודם כל</p>
    <h1 class="huge orange" style="font-size:220px">מחקר</h1>
    <p class="box">מחקר זה כיף, ויותר כיף לעשות את זה ביחד</p>
  </div>
  <div style="position:absolute;left:150px;top:300px">{big_icon('bulb', 460)}</div>
  <div style="position:absolute;left:470px;top:620px">{ic('users', 170)}</div>
</section>''')


CATALOG = 'https://www.bgu.ac.il/media/admboseg/364-2027.pdf'


def qr_svg(url, size=420):
    import qrcode
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    d = ''.join(f'M{x} {y}h1v1h-1z' for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return (f'<svg viewBox="0 0 {n} {n}" width="{size}" height="{size}" shape-rendering="crispEdges" '
            f'aria-label="QR code"><path d="{d}" fill="{DK}"/></svg>')


S(f'''<section class="slide light">
  {hd('השנתון', 'book')}
  <div class="cat">
    <div class="cat-text">
      <h1 class="q">הכל כתוב בשנתון.<br><span class="orange">תקראו אותו.</span></h1>
      <div class="chips">
        <span class="chip">התמחויות</span><span class="chip">מבנה התוכנית</span><span class="chip">קורסים</span>
        <span class="chip">נהלים</span><span class="chip">מסלולים</span>
      </div>
      <p class="muted">שאלות? <span class="mail">{ltr('IEMGrad@bgu.ac.il')}</span></p>
    </div>
    <a class="qr" href="{CATALOG}">{qr_svg(CATALOG)}<span>שנתון המחלקה, תשפ"ז</span></a>
  </div>
</section>''')


def contact(name, role, icon):
    return f'<div class="person big">{ic(icon, 96)}<div><b>{name}</b><span>{role}</span></div></div>'


S(f'''<section class="slide light">
  {hd('למי פונים', 'chat')}
  <div class="who">
    {contact("פרופ' נמרוד טלמון", 'יו"ר ועדת הוראה לתואר שני', 'user')}
    {contact("ג'ני רוקביצין", 'עוזרת רמ"ן לענייני מוסמכים', 'check')}
  </div>
  <div>
    <h3 style="margin-bottom:24px">רכזי ההתמחויות והמגמות</h3>
    <div class="chips">
      <span class="chip">פרופ' רועי זיוון</span><span class="chip">פרופ' נמרוד טלמון</span><span class="chip">ד"ר יואב קרנר</span>
      <span class="chip">פרופ' ליאור פינק</span><span class="chip">פרופ' בעז לרנר</span><span class="chip">פרופ' אבינועם בורובסקי</span>
    </div>
  </div>
  <p class="muted">הרשימה המלאה, עם תפקידים: נספח א' בשנתון</p>
</section>''')

S(f'''<section class="slide light">
  {hd('התמחויות ומסלולים', 'tree')}
  <div class="split2">
    <div class="panel" style="gap:18px">
      <div style="display:flex;align-items:center;gap:24px">{ic('layers', 80)}<div><h3 style="margin:0;color:var(--light)">הנדסת תעשייה</h3><span class="orange" style="font-size:32px;font-weight:700">שלוש מגמות</span></div></div>
      <div class="tracks">
        <div class="track">מערכות נבונות</div>
        <div class="track">חקר ביצועים ואלגוריתמיקה</div>
        <div class="track">סטטיסטיקה שימושית</div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:24px">
      <div class="spec">{ic('screen', 84)}<div><b>מערכות מידע</b></div></div>
      <div class="spec">{ic('search', 84)}<div><b>מדעי הנתונים</b></div></div>
      <div class="spec">{ic('bulb', 84)}<div><b>הנדסת בינה-טכנולוגיה</b></div></div>
    </div>
  </div>
  <div class="pills"><span style="flex:none;background:none;padding-inline:0">בכל התמחות, שני מסלולים:</span><span>עם תזה</span><span>בלי תזה</span></div>
</section>''')

S(f'''<section class="slide light">
  {hd('מבנה התוכנית: 36 נק"ז', 'layers')}
  <div class="cbars simple">
    {credit_bar('עם תזה', [(24, '8 קורסים', 'core'), (12, 'תזה', 'th')])}
    {credit_bar('בלי תזה', [(33, '11 קורסים', 'core'), (3, 'סמינר מסכם', 'th')])}
  </div>
  <p class="muted">איזה קורסים, לפי כל התמחות: בשנתון</p>
</section>''')


S(f'''<section class="slide light">
  {hd('ציר זמן', 'route')}
  {timeline()}
</section>''')


def srow(icon, title, sub):
    return f'<div class="r">{ic(icon, 88, DK)}<div><b>{title}</b><span>{sub}</span></div></div>'


S(f'''<section class="slide light">
  {hd('שופינג למנחה', 'cart')}
  <div class="shop">
    <div class="rows2">
      {srow('search', "סמסטר א' = שופינג", 'זה הזמן להכיר את המעבדות ואת הנושאים')}
      {srow('chat', 'דברו עם כמה חברי סגל', 'הדלת פתוחה, פשוט שלחו מייל')}
      {srow('users', 'שאלו את הסטודנטים במעבדה', 'איך זה באמת')}
      {srow('pen', 'סטודיו למחקר', 'המקום לשאול הכל, ולהפוך את המחקר ליותר טוב, כיף ומועיל')}
      {srow('screen', 'סמינרי המחלקה', 'חובה, אבל גם החלון הכי טוב למה שקורה פה')}
    </div>
    <div class="side">{big_icon('cart', 400)}<p>נושא מעניין + מנחה שנעים לעבוד איתו</p></div>
  </div>
</section>''')

S(f'''<section class="slide light">
  {hd('מלגות', 'coins')}
  <p class="muted">להיות אקטיביים · לבחון בפריזמה רחבה · לעקוב אחרי פרסומים</p>
  <div class="submit"><span class="s1">להגיש…</span><span class="s2">להגיש…</span><span class="s3">ולהגיש!</span></div>
</section>''')

rules = [('upload', 'כל חריגה מהתוכנית: אישור מראש', False),
         ('screen', 'בקשות: מערכת הטפסים באתר הפקולטה (דורש VPN)', False),
         ('check', 'לומדה למניעת הטרדה מינית: לכולם, גם למי שעשה בתואר ראשון', False),
         ('users', 'סמינרי המחלקה: חובה', False)]
S(f'''<section class="slide light">
  {hd('כמה דגשים', 'check')}
  <div class="rules one">
    {''.join(f'<div class="rule{" hot" if hot else ""}">{ic(i, 80, DK)}<span>{t}</span></div>' for i, t, hot in rules)}
  </div>
  <p class="muted">וכל השאר: בשנתון</p>
</section>''')

S(f'''<section class="slide dark middle">
  <h1 class="huge">בהצלחה!</h1>
  <p class="big orange">מחקר זה כיף, ויותר כיף לעשות את זה ביחד</p>
  <p class="big muted" style="margin-top:40px">שאלות?</p>
  <p class="mail" style="font-size:56px">{ltr('IEMGrad@bgu.ac.il')}</p>
</section>''')


html = '''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>מפגש פתיחה תשפ"ז · נמרוד טלמון</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@300..900&display=swap">
<link rel="stylesheet" href="../assets/deck.css">
<style>''' + EXTRA_CSS + '''</style>
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
