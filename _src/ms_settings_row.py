# -*- coding: utf-8 -*-
"""0.40.0: Skin settings > Appearance > Menu theme (row 9748). In the Aeon theme it offers the four menu styles and Fuse
(Mosaic | Ledger | Bridge | Tab slab | Fuse, Bridge when nothing is set); in Glass it keeps Glass | Fuse.
Values of Skin.String(aeon.menutheme): '' Bridge (or Glass's own menus), mosaic, ledger, tabslab, fused.
Run once from the skin folder: python _src/ms_settings_row.py"""
import io
import re

P = '1080i/SkinSettings.xml'
s = io.open(P, encoding='utf-8').read()
start = s.index('<param name="id" value="9748"/>')
gs = s.rindex('<control type="group">', 0, start)
ge = s.index('\n\t\t\t</control>\n', start) + 1    # the row group's closing tag (exactly three tabs)
row = s[gs:ge]
assert row.count('<control type="button" id="9748">') == 1

# 1. the button: Left / Right step through the options of the theme in use
old_btn = re.search(r'<onclick>RunScript\(script\.aeon\.helper,menutheme\)</onclick>.*?</control>', row, re.S).group(0)
ORDER = ['mosaic', 'ledger', 'bridge', 'tabslab', 'fused']
IS = {
    'mosaic': 'String.IsEqual(Skin.String(aeon.menutheme),mosaic)',
    'ledger': 'String.IsEqual(Skin.String(aeon.menutheme),ledger)',
    'tabslab': 'String.IsEqual(Skin.String(aeon.menutheme),tabslab)',
    'fused': 'String.IsEqual(Skin.String(aeon.menutheme),fused)',
}
IS['bridge'] = '![%s | %s | %s | %s]' % (IS['mosaic'], IS['ledger'], IS['tabslab'], IS['fused'])
AEON = '!Skin.HasSetting(aeon.vglass)'
GLASS = 'Skin.HasSetting(aeon.vglass)'
# 0.51.0: settings change with OK only (Left goes back to the category list, Right does nothing)
btn = ['<onclick>RunScript(script.aeon.helper,menutheme)</onclick>', '<onleft>SetFocus(9600)</onleft>']
btn_xml = '\n\t\t\t\t\t'.join(btn) + '\n\t\t\t\t</control>'
row = row.replace(old_btn, btn_xml)

# 2. Glass keeps its two pills: every existing pill control gets the Glass condition
seg_start = row.index('<control type="image"><left>612</left>')
pills = row[seg_start:]
pills = re.sub(r'<visible>(.*?)</visible>', lambda m: '<visible>%s + [%s]</visible>' % (GLASS, m.group(1)), pills)


# 3. the Aeon theme's five pills, in the same pattern (track, then per option: fill + label, focused and not)
def pill_set():
    cells = [('mosaic', '$ADDON[skin.aeon.fuse 32452]', 98), ('ledger', '$ADDON[skin.aeon.fuse 32453]', 92),
             ('bridge', '$ADDON[skin.aeon.fuse 32454]', 92), ('tabslab', '$ADDON[skin.aeon.fuse 32455]', 106),
             ('fused', 'Fuse', 78)]
    total = sum(w for _, _, w in cells)
    x = 896 - total
    out = ['<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="22ffffff">$VAR[Aeon_MenuTexPill]</texture><visible>%s + !Control.HasFocus(9748)</visible></control>' % (x - 4, total + 8, AEON),
           '<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="26000000">$VAR[Aeon_MenuTexPill]</texture><visible>%s + Control.HasFocus(9748)</visible></control>' % (x - 4, total + 8, AEON)]
    for v, label, w in cells:
        on = '%s + [%s]' % (AEON, IS[v])
        off = '%s + ![%s]' % (AEON, IS[v])
        geo = '<left>%d</left><top>13</top><width>%d</width><height>44</height>' % (x, w)
        out.append('<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[Aeon_Accent]">$VAR[Aeon_MenuTexPill]</texture><visible>%s + !Control.HasFocus(9748)</visible></control>' % (geo, on))
        out.append('<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[Aeon_OnBarFill]">$VAR[Aeon_MenuTexPill]</texture><visible>%s + Control.HasFocus(9748)</visible></control>' % (geo, on))
        out.append('<control type="label">%s<align>center</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_AccentText]</textcolor><label>%s</label><visible>%s + !Control.HasFocus(9748)</visible></control>' % (geo, label, on))
        out.append('<control type="label">%s<align>center</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_SegSelTxt]</textcolor><label>%s</label><visible>%s + Control.HasFocus(9748)</visible></control>' % (geo, label, on))
        out.append('<control type="label">%s<align>center</align><font>st_ui_22</font><textcolor>99ffffff</textcolor><label>%s</label><visible>%s + !Control.HasFocus(9748)</visible></control>' % (geo, label, off))
        out.append('<control type="label">%s<align>center</align><font>st_ui_22</font><textcolor>$VAR[Aeon_SegUnselF]</textcolor><label>%s</label><visible>%s + Control.HasFocus(9748)</visible></control>' % (geo, label, off))
        x += w
    return '\n\t\t\t\t'.join(out)


row = row[:seg_start] + pills.rstrip() + '\n\t\t\t\t<!-- Aeon theme: the four menu styles and Fuse -->\n\t\t\t\t' + pill_set() + '\n'
s = s[:gs] + row + s[ge:]
s = s.replace('<!-- Menu theme: the skin theme\'s own menus (Aeon or Glass), or Fuse, the setup wizard\'s rounded cards (aeon.menutheme) -->',
              '<!-- Menu theme (aeon.menutheme): in the Aeon theme one of its four menu styles (Mosaic, Ledger, Bridge - the default -\n'
              '\t\t\t     Tab slab; _src/ms_menus.py) or Fuse, the setup wizard\'s rounded cards; in Glass its own menus or Fuse -->')
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)

# 4. the help line under the settings
H = '1080i/Includes_Settings.xml'
h = io.open(H, encoding='utf-8').read()
anchor = '\t\t<value condition="Control.HasFocus(9744)">$LOCALIZE[31579]</value>\n'
assert anchor in h and 'Control.HasFocus(9748)' not in h
h = h.replace(anchor, anchor + '\t\t<value condition="Control.HasFocus(9748) + !Skin.HasSetting(aeon.vglass)">$ADDON[skin.aeon.fuse 32456]</value>\n'
                                '\t\t<value condition="Control.HasFocus(9748)">$ADDON[skin.aeon.fuse 32457]</value>\n')
io.open(H, 'w', encoding='utf-8', newline='\n').write(h)
print('row', len(row), 'chars')
