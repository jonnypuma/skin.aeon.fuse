# -*- coding: utf-8 -*-
"""0.40.3: the Aeon skip button's segment line. A progress control cannot read Window(Home).Property(Skippy.Segment.Progress)
(Kodi asks the property for a number and gets none, so the line stayed empty); the line is now a track image plus a
bar image per whole per cent, media/aeon/skipbar/0..100.png (white on the left N per cent, 420 x 6), coloured with
colordiffuse like the old midtexture. Run once from the skin folder."""
import io
import os
import re
import xml.etree.ElementTree as ET

from PIL import Image

# 1. the bar images
D = 'media/aeon/skipbar'
os.makedirs(D, exist_ok=True)
W, H = 420, 6
for n in range(101):
    im = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    fill = round(W * n / 100.0)
    if fill:
        im.paste((255, 255, 255, 255), (0, 0, fill, H))
    im.save(os.path.join(D, '%d.png' % n), optimize=True)

# 2. the two includes: progress control -> track image + bar image
F = '1080i/Includes_Fused.xml'
f = io.open(F, encoding='utf-8').read()
a = f.index('<include name="Aeon_SkipCells96">')
b = f.index('</include>', f.index('<include name="Aeon_SkipCells108">')) + len('</include>')
part = f[a:b]
PROP = 'Window(Home).Property(Skippy.Segment.Progress)'
pat = re.compile(r'<control type="progress"><left>(\d+)</left><top>(\d+)</top><width>(\d+)</width><height>6</height>'
                 r'<texturebg colordiffuse="([^"]+)">common/aeon_line_6.png</texturebg>'
                 r'<midtexture colordiffuse="([^"]+)">common/aeon_line_6.png</midtexture><info>' + re.escape(PROP) + r'</info></control>')


def repl(m):
    left, top, width, track, line = m.groups()
    box = '<left>%s</left><top>%s</top><width>%s</width><height>6</height>' % (left, top, width)
    return ('<control type="image">%s<texture colordiffuse="%s">common/white.png</texture></control>\n\t\t\t\t'
            '<control type="image">%s<texture colordiffuse="%s">aeon/skipbar/$INFO[%s].png</texture>'
            '<visible>!String.IsEmpty(%s)</visible></control>' % (box, track, box, line, PROP, PROP))


new, n = pat.subn(repl, part)
assert n == 4, n
f = f[:a] + new + f[b:]
io.open(F, 'w', encoding='utf-8', newline='\n').write(f)
ET.parse(F)
print('skip line: 101 bar images, %d progress controls replaced' % n)
