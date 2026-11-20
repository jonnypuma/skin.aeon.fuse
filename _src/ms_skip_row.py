# -*- coding: utf-8 -*-
"""0.40.3: Skin settings > Behaviour > Skippy: skip button style = Box pair | Clock dock (row 9738 at y 891, Aeon theme,
Skin.String(aeon.skippy.aeonstyle): '' box pair, clock). The slot is Fused Glass's row 9739 (Skip button on the player
card) otherwise; this copies that row. Run once from the skin folder."""
import io
import re
import xml.etree.ElementTree as ET

P = '1080i/SkinSettings.xml'
s = io.open(P, encoding='utf-8').read()
assert 'id="9738"' not in s


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


fstart = s.index('<visible>Control.HasFocus(9739)')
fstart = s.rindex('<control type="group">', 0, fstart)
focus = block_at(s, fstart)
chrome = s.index('<param name="id" value="9739"/>')
rstart = s.rindex('<control type="group">', 0, chrome)
row = block_at(s, rstart)
assert '<control type="button" id="9739">' in row and 'Control.HasFocus(9739)' in focus
CARD_TAB = '[String.IsEmpty(Skin.String(aeon.skippy.cardstyle)) | String.IsEqual(Skin.String(aeon.skippy.cardstyle),tab)]'
PAIR = 'String.IsEmpty(Skin.String(aeon.skippy.aeonstyle))'
nfocus = focus.replace('9739', '9738').replace('$EXP[Aeon_FGlass]', '!Skin.HasSetting(aeon.vglass)', 1) if '$EXP[Aeon_FGlass] + System' in focus else focus.replace('9739', '9738')
nrow = row.replace('<visible>$EXP[Aeon_FGlass] + System.AddonIsEnabled(service.skippy)</visible>',
                   '<visible>!Skin.HasSetting(aeon.vglass) + System.AddonIsEnabled(service.skippy)</visible>', 1)
assert nrow != row
nrow = (nrow.replace('9739', '9738').replace(CARD_TAB, PAIR)
        .replace('Skin.SetString(aeon.skippy.cardstyle,glass)', 'Skin.SetString(aeon.skippy.aeonstyle,clock)')
        .replace('String.IsEqual(Skin.String(aeon.skippy.cardstyle),glass)', 'String.IsEqual(Skin.String(aeon.skippy.aeonstyle),clock)')
        .replace('Skin.Reset(aeon.skippy.cardstyle)', 'Skin.Reset(aeon.skippy.aeonstyle)')
        .replace('$ADDON[skin.aeon.fuse 32427]', '$ADDON[skin.aeon.fuse 32462]')
        .replace('$ADDON[skin.aeon.fuse 32428]', '$ADDON[skin.aeon.fuse 32463]')
        .replace('$ADDON[skin.aeon.fuse 32429]', '$ADDON[skin.aeon.fuse 32464]'))
assert 'cardstyle' not in nrow, 'left-over cardstyle'
s = s[:fstart] + ('<!-- Skippy, Aeon theme (0.40.3): the skin\'s skip button as a box pair (bottom right) or docked to the clock box -->\n\t\t\t'
                  + nfocus + '\n\t\t\t' + nrow + '\n\t\t\t') + s[fstart:]

# navigation: 9729 down / 9720 up reach the Aeon row in the Aeon theme
old = '<ondown condition="$EXP[Aeon_FGlass]">9739</ondown><ondown condition="!$EXP[Aeon_FGlass]">9720</ondown>'
b = s.index('<control type="button" id="9729">')
e = s.index('</control>', b)
btn = s[b:e]
btn2 = re.sub(r'<ondown condition="\$EXP\[Aeon_FGlass\]">9739</ondown>\s*<ondown condition="!\$EXP\[Aeon_FGlass\]">9720</ondown>',
              '<ondown condition="$EXP[Aeon_FGlass]">9739</ondown><ondown condition="!Skin.HasSetting(aeon.vglass)">9738</ondown>'
              '<ondown condition="Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass]">9720</ondown>', btn)
assert btn2 != btn
s = s[:b] + btn2 + s[e:]
b = s.index('<control type="button" id="9720">')
e = s.index('</control>', b)
btn = s[b:e]
btn2 = btn.replace('<onup condition="System.AddonIsEnabled(service.skippy) + !$EXP[Aeon_FGlass]">9729</onup>',
                   '<onup condition="System.AddonIsEnabled(service.skippy) + !Skin.HasSetting(aeon.vglass)">9738</onup>'
                   '<onup condition="System.AddonIsEnabled(service.skippy) + Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass]">9729</onup>')
assert btn2 != btn
s = s[:b] + btn2 + s[e:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
ET.parse(P)

H = '1080i/Includes_Settings.xml'
h = io.open(H, encoding='utf-8').read()
anchor = '\t\t<value condition="Control.HasFocus(9739)">$ADDON[skin.aeon.fuse 32430]</value>\n'
assert anchor in h
h = h.replace(anchor, anchor + '\t\t<value condition="Control.HasFocus(9738)">$ADDON[skin.aeon.fuse 32465]</value>\n')
io.open(H, 'w', encoding='utf-8', newline='\n').write(h)
ET.parse(H)
print('row 9738 added')
