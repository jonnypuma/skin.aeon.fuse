"""0.46.0: the view picker's mock-up for Episode combined (538): header, season pills, season poster, the episode rows
in a card (the focused one white, a yellow progress line), the episode in focus on the right."""
import io
import xml.etree.ElementTree as ET

P = r'C:\Users\gideo\AppData\Roaming\Kodi\addons\skin.aeon.fuse\1080i\Includes_Aeon_Picker.xml'


def img(x, y, w, h, col, tex='common/white.png'):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="%s">%s</texture></control>' % (x, y, w, h, col, tex))


parts = [img(14, 14, 64, 6, '55ffffff'), img(14, 26, 104, 14, 'ccffffff')]
parts += [img(14 + k * 34, 48, 30, 10, 'ffffffff' if k == 2 else '33ffffff') for k in range(4)]
parts.append(img(14, 66, 46, 68, '88ffffff'))                     # season poster
parts.append(img(68, 64, 122, 124, '1fffffff'))                   # the episodes card
for k in range(4):
    y = 70 + k * 29
    if k == 1:
        parts.append(img(70, y - 3, 118, 28, 'ffffffff'))         # the row in focus: white
        ink = 'ff0f1115'
    else:
        ink = 'ccffffff'
    parts.append(img(74, y, 30, 17, '88ffffff' if k != 1 else '660f1115'))
    if k == 0:
        parts.append(img(74, y + 15, 20, 2, 'ffe8b04b'))          # yellow progress line
    parts.append(img(110, y + 2, 62, 5, ink))
    parts.append(img(110, y + 10, 40, 4, '880f1115' if k == 1 else '66ffffff'))
parts.append(img(196, 64, 62, 35, '88ffffff'))                    # the episode in focus
parts.append(img(196, 98, 30, 2, 'ffe8b04b'))
parts.append(img(196, 106, 52, 7, 'ccffffff'))
parts += [img(196 + k * 21, 118, 18, 7, '44ffffff') for k in range(3)]
parts += [img(196, 132 + k * 9, 60 - k * 8, 3, '55ffffff') for k in range(4)]
GROUP = ('\t\t\t<!-- 0.46.0 Episode combined (538) -->\n\t\t\t<control type="group"><visible>String.IsEqual(ListItem.Property(pk),epcomb)</visible>'
         + ''.join(parts) + '</control>\n')

t = io.open(P, encoding='utf-8').read()
if 'Episode combined (538)' not in t:
    lines = t.split('\n')
    k = next(i for i, l in enumerate(lines) if 'String.IsEqual(ListItem.Label2,$LOCALIZE[31293])' in l)
    lines.insert(k + 1, GROUP.rstrip('\n'))
    t = '\n'.join(lines)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
ET.parse(P)
# the picker item says which view it is: a condition cannot read $ADDON[...] strings, so Label2 was no use (and the
# phase 4 mock-up never showed for that reason)
V = r'C:\Users\gideo\AppData\Roaming\Kodi\addons\skin.aeon.fuse\1080i\Custom_1165_VideoViews.xml'
v = io.open(V, encoding='utf-8').read()
if 'property name="pk">epcomb' not in v:
    v = v.replace('<icon>538</icon><onclick>', '<icon>538</icon><property name="pk">epcomb</property><onclick>', 1)
    io.open(V, 'w', encoding='utf-8', newline='\n').write(v)
ET.parse(V)
print('ok')
