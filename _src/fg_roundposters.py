"""0.45.1 Fused Glass: posters with rounded corners everywhere (the set spotlight's films on Home, the versions / set
panes, other single-line poster images that had none). Each such image line gets a Fused Glass copy with a rounded mask
(radius 16, 12 under 120 px wide) and the old line is kept for the other themes. Run from the skin folder; safe to run
again."""
import io
import os
import re

from PIL import Image, ImageDraw

FILES = ['Includes_Aeon_Home.xml', 'Includes_Aeon_Video.xml', 'Includes_Aeon_Views2.xml']
POSTER = re.compile(r'Art\((?:set\.)?poster\)|Poster\]')
made = 0
masks = set()
for name in FILES:
    p = os.path.join('1080i', name)
    lines = io.open(p, encoding='utf-8').read().split('\n')
    out = []
    for line in lines:
        s = line.strip()
        if (s.startswith('<control type="image">') and s.endswith('</control>') and '<texture' in s and POSTER.search(s)
                and 'diffuse=' not in s and 'Aeon_FGlass' not in s and 'aspectratio>keep' not in s):
            w = re.search(r'<width>(\d+)</width>', s)
            h = re.search(r'<height>(\d+)</height>', s)
            if w and h:
                w, h = int(w.group(1)), int(h.group(1))
                r = 12 if w < 120 else 16
                masks.add((w, h, r))
                vis = re.search(r'<visible>([^<]*)</visible>', s)
                old = line.replace('<visible>%s</visible>' % vis.group(1), '<visible>[%s] + !$EXP[Aeon_FGlass]</visible>' % vis.group(1)) if vis \
                    else line.replace('</control>', '<visible>!$EXP[Aeon_FGlass]</visible></control>')
                new = line.replace('<aspectratio>scale</aspectratio>', '<aspectratio scalediffuse="false">scale</aspectratio>')
                new = re.sub(r'<texture( background="true")?>', lambda m: '<texture%s diffuse="fg/m%dx%d.png">' % (m.group(1) or '', w, h), new, count=1)
                new = new.replace('<visible>%s</visible>' % vis.group(1), '<visible>[%s] + $EXP[Aeon_FGlass]</visible>' % vis.group(1)) if vis \
                    else new.replace('</control>', '<visible>$EXP[Aeon_FGlass]</visible></control>')
                out += [old, new]
                made += 1
                continue
        out.append(line)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
for w, h, r in masks:
    path = os.path.join('media', 'fg', 'm%dx%d.png' % (w, h))
    if os.path.exists(path):
        continue
    im = Image.new('L', (w * 2, h * 2), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], r * 2, fill=255)
    o = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    o.putalpha(im.resize((w, h), Image.LANCZOS))
    o.save(path, optimize=True)
import xml.etree.ElementTree as ET
for name in FILES:
    ET.parse(os.path.join('1080i', name))
print('rounded copies', made, 'masks', sorted(masks))
