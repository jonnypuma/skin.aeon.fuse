# -*- coding: utf-8 -*-
"""0.40.2: Skin settings > Look > Library options: Strip | Box (Skin.HasSetting(aeon.libpanel.box); Strip by default).
The side strip stays the Library panel / View settings; Box opens them as the big box of the Aeon menu style.
Row 9547 at y 751, shown in the Aeon theme with its own menus ($EXP[Aeon_MS]); the slot is Fused Glass's row 9546
otherwise. Copies row 9524 (Library side strip, a two-pill toggle). Run once from the skin folder."""
import io
import re
import xml.etree.ElementTree as ET

P = '1080i/SkinSettings.xml'
s = io.open(P, encoding='utf-8').read()
assert 'id="9547"' not in s


def block_at(text, start):
    """the <control ...> block starting at start, found by counting nested controls"""
    depth = 0
    for m in re.finditer(r'<control\b[^>]*?(/?)>|</control>', text[start:]):
        tok = m.group(0)
        if tok.startswith('</'):
            depth -= 1
            if depth == 0:
                return text[start:start + m.end()]
        elif not m.group(1):
            depth += 1
    raise ValueError('unclosed block')


# the focus bar group and the row group of 9524
fstart = s.index('<control type="group">\n\t\t\t\t<left>-119</left>\n\t\t\t\t<top>471</top>\n\t\t\t\t<visible>Control.HasFocus(9524)</visible>')
focus = block_at(s, fstart)
chrome = s.index('<param name="id" value="9524"/>')
rstart = s.rindex('<control type="group">', 0, chrome)
row = block_at(s, rstart)
assert '<control type="button" id="9524">' in row and 'Control.HasFocus(9524)' in focus

nfocus = focus.replace('<top>471</top>', '<top>751</top>').replace('9524', '9547')
nrow = (row.replace('<top>471</top>', '<top>751</top>\n\t\t\t\t<visible>$EXP[Aeon_MS]</visible>', 1)
        .replace('9524', '9547')
        .replace('aeon.vsbwhite', 'aeon.libpanel.box')
        .replace('$LOCALIZE[31748]', '$ADDON[skin.aeon.fuse 32458]')
        .replace('$LOCALIZE[31665]', '$ADDON[skin.aeon.fuse 32459]')
        .replace('$LOCALIZE[31666]', '$ADDON[skin.aeon.fuse 32460]')
        .replace('aeon/icons/sidebar.png', 'aeon/icons/layers.png'))
nrow = re.sub(r'<onup>[^<]*</onup>\s*<ondown>[^<]*</ondown>\s*<onback>[^<]*</onback>',
              '<onup>9542</onup>\n\t\t\t\t\t<ondown>9521</ondown>\n\t\t\t\t\t<onback>9551</onback>', nrow, 1)
nrow = nrow.replace('SetFocus(9600)', 'SetFocus(9551)')
assert '<onup>9542</onup>' in nrow
anchor = s.index('\t\t\t<!-- Home menu: only the focused item\'s name, the others as icons (0.38.0, Fused Glass) -->')
s = (s[:anchor] + '\t\t\t<!-- Library options (0.40.2, Aeon theme with its own menus): the side strip, or the big box of the menu style -->\n'
     '\t\t\t' + nfocus + '\n\t\t\t' + nrow + '\n' + s[anchor:])

# navigation: 9542 (Fonts) down and 9521 (top of the page) up reach the new row in the Aeon theme
old_down = '<ondown condition="$EXP[Aeon_FGlass]">9546</ondown>\n\t\t\t\t\t<ondown condition="!$EXP[Aeon_FGlass]">9521</ondown>'
assert s.count(old_down) == 1
s = s.replace(old_down, '<ondown condition="$EXP[Aeon_FGlass]">9546</ondown>\n\t\t\t\t\t<ondown condition="$EXP[Aeon_MS]">9547</ondown>\n'
                        '\t\t\t\t\t<ondown condition="!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]">9521</ondown>')
b = s.index('<control type="button" id="9521">')
e = s.index('</control>', b)
btn = s[b:e]
ups = re.findall(r'<onup[^>]*>[^<]*</onup>', btn)
print('9521 onup before:', ups)
new_ups = ('<onup condition="$EXP[Aeon_FGlass]">9546</onup><onup condition="$EXP[Aeon_MS]">9547</onup>'
           '<onup condition="!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]">9542</onup>')
btn2 = btn
for u in ups:
    btn2 = btn2.replace(u, '', 1)
btn2 = btn2.replace('<include>Dlg_SkinRowButton</include>', '<include>Dlg_SkinRowButton</include>\n\t\t\t\t\t' + new_ups, 1)
s = s[:b] + btn2 + s[e:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
ET.parse(P)

H = '1080i/Includes_Settings.xml'
h = io.open(H, encoding='utf-8').read()
anchor = '\t\t<value condition="Control.HasFocus(9524)">$LOCALIZE[31577]</value>\n'
assert anchor in h and 'Control.HasFocus(9547)' not in h
h = h.replace(anchor, anchor + '\t\t<value condition="Control.HasFocus(9547)">$ADDON[skin.aeon.fuse 32461]</value>\n')
io.open(H, 'w', encoding='utf-8', newline='\n').write(h)
ET.parse(H)
print('row 9547 added')
