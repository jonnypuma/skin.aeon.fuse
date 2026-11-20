"""Skin settings option pickers: overlaps, English padding, English names that would be cut. Run in skin.aeon.fuse."""
import io, re, sys
sys.path.insert(0, '_src')
import pickers_flush_05618 as pf, pickers_fit_05618 as f  # noqa: E402
from PIL import ImageFont

nf = ImageFont.truetype('fonts/Figtree-Bold.ttf', 24)
sf = ImageFont.truetype('fonts/Figtree-Bold.ttf', 22)
en = f.strings('en_gb')
lines = io.open('1080i/SkinSettings.xml', encoding='utf-8').read().split('\n')
bad = cut = 0
pads = []
for p in pf.pickers(lines):
    s = sorted(p['segs'])
    for a, b in zip(s, s[1:]):
        if a[0] + a[1] > b[0]:
            bad += 1
            print('overlap', p['start'] + 1, a, b)
    m = re.search(r'Control\.HasFocus\((\d+)\)', lines[p['start']])
    rid = m.group(1) if m else None
    hit = [l for i, l in enumerate(lines) if rid and 'param name="id" value="%s"/>' % rid in l
           and 'Dlg_SkinRowChrome' in lines[i - 1] + l.split('<param', 1)[0]]
    if hit:
        nm = re.search(r'param name="label" value="([^"]*)"', hit[0]).group(1)
        w = re.search(r'namew" value="(\d+)"', hit[0])
        t = f.resolve(nm, en) or ''
        if w and nf.getlength(t) > int(w.group(1)):
            cut += 1
            print('english name cut', rid, t)
    gaps = []
    for i in range(p['start'], min(len(lines), p['start'] + 120)):
        g = pf.GEO.search(lines[i])
        m2 = re.search(r'<label>(.*?)</label>', lines[i])
        if g and m2 and (int(g.group(1)), int(g.group(3))) in p['segs'] and g.group(2) == p['track'][1]:
            t = f.resolve(m2.group(1), en)
            if t:
                gaps.append(((int(g.group(3)) - sf.getlength(t)) / 2, t))
    if gaps:
        pads.append((round(min(gaps)[0]), rid, min(gaps)[1]))
print('pickers', len(pf.pickers(lines)), 'overlaps', bad, 'english names cut', cut)
print('smallest English pads', sorted(pads)[:6])
