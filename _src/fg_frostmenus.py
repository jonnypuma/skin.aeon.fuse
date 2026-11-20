# -*- coding: utf-8 -*-
"""0.56.12 Menu theme in Fused Glass: Dark | Glass | Frost (Skin.String(aeon.fgmenu): '' / glass / frost).

The user (2026-11-16), on the mockup canvas RfMMKDTnbQCAG46Y3hpn9j (skin.glass/mockups/fg-glass-menu/menu-tint):
"A. Darker will be the new Glass theme, and you will add B. Frost as a third option."
- Glass: the cards a step darker, halfway from the old Glass to the Dark fill (fg_material.py writes the values).
- Frost (new): Glass's see-through menus (FG_GlassMenus is true for Glass and Frost) on a light cool tint, over a
  blurred picture. Kodi cannot blur what is on the screen, so the blur is the helper's blurred backdrop:
  - settings windows: Aeon_Backdrop shows the blurred copy of the settings backdrop (Window(Home).Property(
    aeon.bgfan.blur), script.aeon.helper 0.3.93) while it matches aeon.bgfan;
  - dialogs over a library window (videos, music, Planner): the window lays the blurred copy of its backdrop
    (aeon.blur) over itself while a menu dialog is open (include FG_FrostBehind, the last control of the window),
    under a lighter dim, so the frosted panel shows the blurred picture through its tint.
  Information pages and windows without a blurred backdrop show the frost tint alone.
Run from the skin folder, then python _src/fg_material.py and python _src/ok_only.py. Safe to run again."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
FUSED = os.path.join(D, 'Includes_Fused.xml')
AEON = os.path.join(D, 'Includes_Aeon.xml')
GLASS = os.path.join(D, 'Includes_Aeon_Glass.xml')
SET = os.path.join(D, 'SkinSettings.xml')
A = '$ADDON[skin.aeon.fuse %d]'
FG = 'Skin.HasSetting(aeon.fglass)'
MENU = 'Skin.String(aeon.fgmenu)'
EQ = lambda v: 'String.IsEqual(%s,%s)' % (MENU, v)
DIALOGS = ('contextmenu', 'selectdialog', 'yesnodialog', 'okdialog', 'textviewer', 'numericinput', 'virtualkeyboard',
           'filebrowser', 'sliderdialog', 'addonsettings', 'smartplaylisteditor', 'mediasource', '1161')


def read(p):
    return io.open(p, encoding='utf-8').read()


def write(p, t):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


# ---------------------------------------------------------------- expressions and the layer behind dialogs
f = read(FUSED)
old = '<expression name="FG_GlassMenus">%s + %s</expression>' % (FG, EQ('glass'))
new = '<expression name="FG_GlassMenus">%s + [%s | %s]</expression>' % (FG, EQ('glass'), EQ('frost'))
if old in f:
    f = f.replace(old, new)
assert new in f
if 'name="FG_FrostMenus"' not in f:
    win = ' | '.join('Window.IsVisible(%s)' % d for d in DIALOGS)
    block = ('\n\t<!-- 0.56.12 Menu theme Frost (_src/fg_frostmenus.py): Glass\'s see-through menus on a light cool tint over a\n'
             '\t     blurred picture. FG_FrostPic: the library window has its blurred backdrop (aeon.blur) to lay behind a\n'
             '\t     dialog; FG_FrostBehind (the last control of the library windows) shows it while a menu dialog is open. -->\n'
             '\t<expression name="FG_FrostMenus">%s + %s</expression>\n'
             '\t<expression name="FG_FrostPic">$EXP[FG_FrostMenus] + !String.IsEmpty(Window(Home).Property(aeon.blur)) + '
             '[Window.IsActive(videos) | Window.IsActive(music) | Window.IsActive(1168)]</expression>\n'
             '\t<include name="FG_FrostBehind">\n'
             '\t\t<control type="image">\n'
             '\t\t\t<left>0</left><top>0</top><width>1920</width><height>1080</height>\n'
             '\t\t\t<aspectratio>scale</aspectratio>\n'
             '\t\t\t<texture background="true" colordiffuse="e6ffffff">$INFO[Window(Home).Property(aeon.blur)]</texture>\n'
             '\t\t\t<animation type="Visible"><effect type="fade" start="0" end="100" time="200"/></animation>\n'
             '\t\t\t<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>\n'
             '\t\t\t<visible>$EXP[FG_FrostPic] + [%s]</visible>\n'
             '\t\t</control>\n'
             '\t</include>' % (FG, EQ('frost'), win))
    f = f.replace(new, new + block, 1)
write(FUSED, f)

# the library windows: the layer last, over the view and under the dialogs
for name in ('MyVideoNav.xml', 'MyMusicNav.xml', 'Custom_1168_Planner.xml'):
    p = os.path.join(D, name)
    t = read(p)
    if '<include>FG_FrostBehind</include>' not in t:
        assert t.count('\t</controls>') == 1, name
        t = t.replace('\t</controls>', '\t\t<include>FG_FrostBehind</include>\n\t</controls>')
        write(p, t)

# the dim behind dialogs: lighter over the blurred picture
a = read(AEON)
dim = '\t<variable name="AG_DimDialog">\n\t\t<value condition="$EXP[FG_GlassMenus]">5908090c</value>\n'
if 'FG_FrostPic' not in a.split('name="AG_DimDialog"')[1][:400]:
    assert dim in a
    a = a.replace(dim, '\t<variable name="AG_DimDialog">\n\t\t<value condition="$EXP[FG_FrostPic]">26080a0e</value>\n'
                  '\t\t<value condition="$EXP[FG_GlassMenus]">5908090c</value>\n')
write(AEON, a)

# ---------------------------------------------------------------- the settings backdrop blurred with Frost
g = read(GLASS)
FROSTBG = ('$EXP[FG_FrostMenus] + !String.IsEmpty(Window(Home).Property(aeon.bgfan.blur)) + '
           'String.IsEqual(Window(Home).Property(aeon.bgfan.blursrc),Window(Home).Property(aeon.bgfan))')
sharp = ('\t\t\t\t<texture background="true" colordiffuse="$VAR[Aeon_BackdropAlpha]">$INFO[Window(Home).Property(aeon.bgfan)]</texture>\n'
         '\t\t\t\t<visible>!Skin.HasSetting(aeon.nobackdrop) + !String.IsEmpty(Window(Home).Property(aeon.bgfan))</visible>\n'
         '\t\t\t</control>\n')
if 'aeon.bgfan.blur' not in g:
    assert g.count(sharp) == 1
    g = g.replace(sharp, sharp.replace('</visible>', ' + ![%s]</visible>' % FROSTBG) +
                  '\t\t\t<!-- 0.56.12 Menu theme Frost: the blurred copy (script.aeon.helper 0.3.93) -->\n'
                  '\t\t\t<control type="image">\n'
                  '\t\t\t\t<left>-40</left><top>-40</top><width>2000</width><height>1160</height>\n'
                  '\t\t\t\t<aspectratio>scale</aspectratio>\n'
                  '\t\t\t\t<fadetime>400</fadetime>\n'
                  '\t\t\t\t<texture background="true" colordiffuse="$VAR[Aeon_BackdropAlpha]">$INFO[Window(Home).Property(aeon.bgfan.blur)]</texture>\n'
                  '\t\t\t\t<visible>!Skin.HasSetting(aeon.nobackdrop) + %s</visible>\n'
                  '\t\t\t</control>\n' % FROSTBG)
write(GLASS, g)

# ---------------------------------------------------------------- Skin settings: Menu theme Dark | Glass | Frost
s = read(SET)
i = re.search(r'<!-- Fused Glass \(0\.5[0-9.]+\): Dark \(default\) \| Glass', s).start()
j = s.index('\t\t\t</control>', i)
TRACK_L, TRACK_R = 500, 864
cells = [('', A % 32573, 124), ('glass', 'Glass', 116), ('frost', A % 32547, 116)]
sel = {'': '[!%s + !%s]' % (EQ('glass'), EQ('frost')), 'glass': '[%s]' % EQ('glass'), 'frost': '[%s]' % EQ('frost')}
o = ['<!-- Fused Glass (0.56.12): Dark (default) | Glass | Frost, aeon.fgmenu (_src/fg_frostmenus.py) -->']
for focus, col in (('!Control.HasFocus(9748)', '22ffffff'), ('Control.HasFocus(9748)', '26000000')):
    o.append('<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="%s">'
             '$VAR[Aeon_MenuTexPill]</texture><visible>%s + %s</visible></control>' % (TRACK_L, TRACK_R - TRACK_L, col, FG, focus))
x = TRACK_L + 4
for key, label, w in cells:
    c = sel[key]
    for focus, fill, bold, plain in (('!Control.HasFocus(9748)', '$VAR[Aeon_Accent]', '$VAR[Aeon_AccentText]', '99ffffff'),
                                     ('Control.HasFocus(9748)', '$VAR[Aeon_OnBarFill]', '$VAR[Aeon_SegSelTxt]', '$VAR[Aeon_SegUnselF]')):
        o.append('<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="%s">'
                 '$VAR[Aeon_MenuTexPill]</texture><visible>%s + %s + %s</visible></control>' % (x, w, fill, FG, c, focus))
        o.append('<control type="label"><left>%d</left><top>13</top><width>%d</width><height>44</height><align>center</align><font>st_ui_22_bold</font>'
                 '<textcolor>%s</textcolor><label>%s</label><visible>%s + %s + %s</visible></control>' % (x, w, bold, label, FG, c, focus))
        o.append('<control type="label"><left>%d</left><top>13</top><width>%d</width><height>44</height><align>center</align><font>st_ui_22</font>'
                 '<textcolor>%s</textcolor><label>%s</label><visible>%s + !%s + %s</visible></control>' % (x, w, plain, label, FG, c, focus))
    x += w
s = s[:i] + '\n\t\t\t\t'.join(o) + '\n' + s[j:]
# the click: Dark -> Glass -> Frost -> Dark
clicks = re.compile(r'\t*<onclick condition="Skin.HasSetting\(aeon.fglass\) \+ (?:!)?String.IsEqual\(Skin.String\(aeon.fgmenu\),\w+\)(?: \+ [^"]*)?">'
                    r'Skin.(?:Reset|SetString)\(aeon.fgmenu(?:,\w+)?\)</onclick>\n')
b = s.index('<control type="button" id="9748">')
e = s.index('</control>', b)
btn = clicks.sub('', s[b:e])
btn = btn.replace('\t\t\t\t\t<onclick condition="!Skin.HasSetting(aeon.fglass)">RunScript(script.aeon.helper,menutheme)</onclick>\n',
                  '\t\t\t\t\t<onclick condition="!Skin.HasSetting(aeon.fglass)">RunScript(script.aeon.helper,menutheme)</onclick>\n'
                  '\t\t\t\t\t<onclick condition="%s + %s">Skin.SetString(aeon.fgmenu,frost)</onclick>\n'
                  '\t\t\t\t\t<onclick condition="%s + %s">Skin.Reset(aeon.fgmenu)</onclick>\n'
                  '\t\t\t\t\t<onclick condition="%s + !%s + !%s">Skin.SetString(aeon.fgmenu,glass)</onclick>\n'
                  % (FG, EQ('glass'), FG, EQ('frost'), FG, EQ('glass'), EQ('frost')))
assert btn.count('aeon.fgmenu') == 3 + 4, btn
s = s[:b] + btn + s[e:]
write(SET, s)

for p in (FUSED, AEON, GLASS, SET, os.path.join(D, 'MyVideoNav.xml'), os.path.join(D, 'MyMusicNav.xml'), os.path.join(D, 'Custom_1168_Planner.xml')):
    ET.parse(p)
print('ok')
