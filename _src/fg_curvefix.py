"""0.39.6 curvature fixes from _src/fg_curvature_audit.py (rule: [[feedback-curvature]]):
- 60 px pills drawn with r28 (2 px flat at each end) -> r30: the Power card's focused row (its 44 px icon disc, inset
  8, is then concentric: 30 - 8 = 22) and the TV area tabs card (its 44 px tab pills, inset 8: 30 - 8 = 22).
- "In library" pill 30 px tall with r14 -> r15 (new fg/r15.png); seek bubble 36 px tall with r16 -> r18.
- Pills drawn at another height than their texture had their round ends squashed: the 40 px A-Z / count bubbles
  used the 44 px pill (Aeon_TexPill40 -> aeon/pill_40.png), a 36 px pill used pill_40 (-> new aeon/pill_36.png),
  the 4 px focus marks used the 6 px fg/pillh.png (-> new fg/pill4.png).
- Settings strip (1160 / 1166), Fused Glass: the focused row's white bar started on the panel's left edge and ended
  40 px short of its right edge. It sits 8 px inside the panel on both sides now (16 .. 444) with r24 corners,
  concentric with the panel's r32 (32 - 8); the lists are 452 wide to hold it.
Run in 1080i."""
import io
import re


def edit(path, pairs, count=None):
    s = io.open(path, encoding='utf-8').read()
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, (path, old[:80], c, n)
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('Includes_Aeon_Home.xml', [
    ('<width>536</width><height>60</height><texture border="28" colordiffuse="2effffff">fg/r28.png</texture>',
     '<width>536</width><height>60</height><texture border="30" colordiffuse="2effffff">fg/r30.png</texture>', 1)])

s = io.open('Includes_Misc.xml', encoding='utf-8').read()
a = s.index('\t<include name="Misc_PVRFrame">')
b = s.index('\n\t</include>', a)
blk = s[a:b]
for old, new in (('<width>1232</width><height>60</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture>',
                  '<width>1232</width><height>60</height><texture border="30" colordiffuse="fg_frost">fg/r30.png</texture>'),
                 ('<width>1232</width><height>60</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture>',
                  '<width>1232</width><height>60</height><texture border="30" colordiffuse="fg_edge">fg/e30.png</texture>')):
    assert blk.count(old) == 1, old
    blk = blk.replace(old, new)
s = s[:a] + blk + s[b:]
io.open('Includes_Misc.xml', 'w', encoding='utf-8', newline='').write(s)

edit('Includes_Fused.xml', [
    ('<texturenofocus border="15" colordiffuse="f2ffffff">fg/r14.png</texturenofocus>',
     '<texturenofocus border="15" colordiffuse="f2ffffff">fg/r15.png</texturenofocus>', 1),
    ('<texturefocus border="15" colordiffuse="f2ffffff">fg/r14.png</texturefocus>',
     '<texturefocus border="15" colordiffuse="f2ffffff">fg/r15.png</texturefocus>', 1)])
edit('DialogFullScreenInfo.xml', [
    ('<width>120</width><height>36</height><texture border="18" colordiffuse="f2ffffff">fg/r16.png</texture>',
     '<width>120</width><height>36</height><texture border="18" colordiffuse="f2ffffff">fg/r18.png</texture>', 1)])

# 40 px bubbles: a 40 px pill
for f in ('Includes_Aeon_Video.xml', 'Includes_Aeon_Views2.xml'):
    x = io.open(f, encoding='utf-8').read()
    x, n = re.subn(r'(<height>40</height><texture border="20,0,20,0" colordiffuse="[^"]*">)\$VAR\[Aeon_TexPill\]', r'\1$VAR[Aeon_TexPill40]', x)
    assert n >= 2, (f, n)
    io.open(f, 'w', encoding='utf-8', newline='').write(x)
    print(f, n, 'bubbles')
g = io.open('Includes_Aeon_Glass.xml', encoding='utf-8').read()
if 'Aeon_TexPill40' not in g:
    old = '''	<variable name="Aeon_TexPill">
		<value condition="Skin.HasSetting(aeon.vglass)">aeon/pill_44.png</value>
		<value>common/aeon_flat_pill.png</value>
	</variable>'''
    assert old in g
    g = g.replace(old, old + '''
	<!-- 0.39.6: 40 px tall pills (A-Z / count bubbles) use a 40 px pill: drawn from the 44 px one, the ends were squashed -->
	<variable name="Aeon_TexPill40">
		<value condition="Skin.HasSetting(aeon.vglass)">aeon/pill_40.png</value>
		<value>common/aeon_flat_pill.png</value>
	</variable>''')
    io.open('Includes_Aeon_Glass.xml', 'w', encoding='utf-8', newline='').write(g)

edit('Includes_Views_Video.xml', [
    ('<texture border="18,0,18,0" colordiffuse="$VAR[AG_Surface]">aeon/pill_40.png</texture>',
     '<texture border="18,0,18,0" colordiffuse="$VAR[AG_Surface]">aeon/pill_36.png</texture>', 1)])

# 4 px marks
for f in ('Includes_Aeon_Home.xml', 'Includes_Fused.xml', 'Custom_1168_Planner.xml'):
    x = io.open(f, encoding='utf-8').read()
    x, n = re.subn(r'(<height>4</height><texture border="2,0,2,0"[^>]*>)fg/pillh\.png', r'\1fg/pill4.png', x)
    io.open(f, 'w', encoding='utf-8', newline='').write(x)
    print(f, n, 'marks')

# settings strip: the focused row's bar inside the panel, concentric
p = 'Includes_Aeon_Menu.xml'
m = io.open(p, encoding='utf-8').read()
old = '<control type="image"><left>0</left><top>0</top><width>420</width><height>80</height><texture colordiffuse="$VAR[Aeon_StripFocusBox]">fg/striprow420x80.png</texture>'
assert m.count(old) == 1
m = m.replace(old, '<control type="image"><left>16</left><top>8</top><width>428</width><height>64</height><texture border="24" colordiffuse="$VAR[Aeon_StripFocusBox]">fg/r24.png</texture>')
io.open(p, 'w', encoding='utf-8', newline='').write(m)
for f in ('Custom_1160_LibraryPanel.xml', 'Custom_1166_ViewSettings.xml'):
    x = io.open(f, encoding='utf-8').read()
    n1 = x.count('<left>0</left><top>108</top><width>420</width><height>864</height>')
    x = x.replace('<left>0</left><top>108</top><width>420</width><height>864</height>', '<left>0</left><top>108</top><width>452</width><height>864</height>')
    n2 = x.count('layout width="420" height="80"')
    x = x.replace('layout width="420" height="80"', 'layout width="452" height="80"')
    io.open(f, 'w', encoding='utf-8', newline='').write(x)
    print(f, 'lists', n1, 'layouts', n2)
print('ok')
