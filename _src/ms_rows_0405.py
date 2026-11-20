# -*- coding: utf-8 -*-
"""0.40.5: two On / Off rows, copied from the Fused Glass row 9546 (Home menu icons) with its focus bar:
  - Backgrounds, row 8 (y 681), id 9737, Aeon / Glass: Band under the Home menu (Skin.HasSetting(aeon.homeband))
  - Look, row 10 (y 821), id 9528, Fused Glass: Toasts from the clock pill (Skin.HasSetting(aeon.toastpill))
Both off by default. Help texts 32473 / 32475. Run once from the skin folder."""
import io
import re
import xml.etree.ElementTree as ET

P = '1080i/SkinSettings.xml'
s = io.open(P, encoding='utf-8').read()
assert 'id="9737"' not in s and 'id="9528"' not in s


def block_at(text, start):
    depth = 0
    for m in re.finditer(r'<control\b[^>]*?(/?)>|</control>', text[start:]):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return text[start:start + m.end()]
        elif not m.group(1):
            depth += 1
    raise ValueError('unclosed block')


def blocks(rid):
    f = s.index('<visible>Control.HasFocus(%d)' % rid)
    f = s.rindex('<control type="group">', 0, f)
    c = s.index('<param name="id" value="%d"/>' % rid)
    r = s.rindex('<control type="group">', 0, c)
    return (f, block_at(s, f)), (r, block_at(s, r))


(_, tfocus), (_, trow) = blocks(9546)
assert '<top>751</top>' in tfocus and '<top>751</top>' in trow


def make(rid, top, vis, setting, label, icon, up, down, back):
    f = tfocus.replace('Control.HasFocus(9546) + $EXP[Aeon_FGlass]', 'Control.HasFocus(%d) + %s' % (rid, vis))
    f = f.replace('<top>751</top>', '<top>%d</top>' % top, 1)
    r = trow.replace('<visible>$EXP[Aeon_FGlass]</visible>', '<visible>%s</visible>' % vis, 1).replace('<top>751</top>', '<top>%d</top>' % top, 1)
    r = r.replace('9546', str(rid)).replace('aeon.hm.icons', setting)
    r = r.replace('$ADDON[skin.aeon.fuse 32425]', label).replace('aeon/icons/home.png', icon)
    assert '9546' not in f + r and 'hm.icons' not in r
    r = r.replace('<onup>9542</onup>', '<onup>%s</onup>' % up).replace('<ondown>9521</ondown>', '<ondown>%s</ondown>' % down)
    r = r.replace('<onback>9551</onback>', '<onback>%s</onback>' % back).replace('SetFocus(9551)', 'SetFocus(%s)' % back)
    return f + '\n\t\t\t' + r


# 1. Backgrounds: after row 9736 (its row group); 9736 down / 9730 up reach the new row outside Fused Glass
(_, _), (r36, row36) = blocks(9736)
back36 = re.search(r'<onback>(\d+)</onback>', row36).group(1)
band = make(9737, 681, '!$EXP[Aeon_FGlass]', 'aeon.homeband', '$ADDON[skin.aeon.fuse 32472]', 'aeon/icons/home.png', '9736', '9730', back36)
at = r36 + len(row36)
s = s[:at] + ('\n\t\t\t<!-- 0.40.5: a band under the Home menu, over the spotlight pictures (aeon.homeband, Aeon / Glass, off) -->\n\t\t\t'
              + band) + s[at:]
b = s.index('<control type="button" id="9736">')
e = s.index('</control>', b)
old = s[b:e]
assert '<ondown>9730</ondown>' in old
s = s[:b] + old.replace('<ondown>9730</ondown>', '<ondown condition="!$EXP[Aeon_FGlass]">9737</ondown><ondown condition="$EXP[Aeon_FGlass]">9730</ondown>', 1) + s[e:]
b = s.index('<control type="button" id="9730">')
e = s.index('</control>', b)
old = s[b:e]
assert '<onup>9736</onup>' in old
s = s[:b] + old.replace('<onup>9736</onup>', '<onup condition="!$EXP[Aeon_FGlass]">9737</onup><onup condition="$EXP[Aeon_FGlass]">9736</onup>', 1) + s[e:]

# 2. Look: after row 9546 (Fused Glass); 9546 down / 9521 up reach it in Fused Glass
(_, _), (r46, row46) = blocks(9546)
toast = make(9528, 821, '$EXP[Aeon_FGlass]', 'aeon.toastpill', '$ADDON[skin.aeon.fuse 32474]', 'aeon/icons/clock.png', '9546', '9521', '9551')
at = r46 + len(row46)
s = s[:at] + ('\n\t\t\t<!-- 0.40.5: notifications grow out of the clock pill (aeon.toastpill, Fused Glass, off) -->\n\t\t\t' + toast) + s[at:]
b = s.index('<control type="button" id="9546">')
e = s.index('</control>', b)
old = s[b:e]
assert '<ondown>9521</ondown>' in old
s = s[:b] + old.replace('<ondown>9521</ondown>', '<ondown>9528</ondown>', 1) + s[e:]
b = s.index('<control type="button" id="9521">')
e = s.index('</control>', b)
old = s[b:e]
a = '<onup condition="$EXP[Aeon_FGlass]">9546</onup>'
assert a in old
s = s[:b] + old.replace(a, '<onup condition="$EXP[Aeon_FGlass]">9528</onup>', 1) + s[e:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
ET.parse(P)

H = '1080i/Includes_Settings.xml'
h = io.open(H, encoding='utf-8').read()
anchor = '\t\t<value condition="Control.HasFocus(9738)">$ADDON[skin.aeon.fuse 32465]</value>\n'
assert anchor in h
h = h.replace(anchor, anchor + '\t\t<value condition="Control.HasFocus(9737)">$ADDON[skin.aeon.fuse 32473]</value>\n'
                               '\t\t<value condition="Control.HasFocus(9528)">$ADDON[skin.aeon.fuse 32475]</value>\n', 1)
io.open(H, 'w', encoding='utf-8', newline='\n').write(h)
ET.parse(H)
print('rows 9737 and 9528 added')
