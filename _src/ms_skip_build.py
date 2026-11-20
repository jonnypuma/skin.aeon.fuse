# -*- coding: utf-8 -*-
"""0.40.3: the skin's own Skippy skip button in the Aeon theme (mockups/skip-button-aeon): a palette tile with the skip
glyph + the label cell (name, time left, how much has played). Box pair (default): bottom right, flush with the screen
edge; above the player controls when they are open. Clock dock: tile, label cell and the clock box in one row at the
top right. The skip dialog (Custom_1167) holds the focus, so its cell is lit (white, dark ink); in the player controls the
same boxes show dark until Up from the seek bar focuses them (button 88). Run once from the skin folder.
ms_skip_bar.py then swapped the progress controls drawn here for track + per-cent bar images (a progress control
cannot read the window property)."""
import io
import xml.etree.ElementTree as ET

W1 = 'f0ffffff'


def cells(name, h, w, g):
    """an include: tile h x h + label cell w x h; param lit = condition for the focused look"""
    lab = '[UPPERCASE]$LOCALIZE[31964] $INFO[Window(Home).Property(Skippy.Segment.Type)][/UPPERCASE]'
    rem = '$INFO[Window(Home).Property(Skippy.Segment.Remaining)]'
    prog = 'Window(Home).Property(Skippy.Segment.Progress)'
    o = ['\t<include name="%s">' % name, '\t\t<param name="lit">true</param>', '\t\t<definition>']
    o.append('\t\t\t<control type="image"><left>0</left><top>0</top><width>%d</width><height>%d</height><texture colordiffuse="$VAR[Aeon_BoxCol]">common/white.png</texture></control>' % (h, h))
    o.append('\t\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/next.png</texture></control>' % (g, g, h - 2 * g, h - 2 * g))
    for lit in (True, False):
        v = '$PARAM[lit]' if lit else '![$PARAM[lit]]'
        bg = 'aeon_white' if lit else 'x_deep'
        ink = 'aeon_onbar' if lit else W1
        ink2 = 'aeon_onbar_99' if lit else 'a0ffffff'
        line = 'aeon_onbar_99' if lit else 'ccffffff'
        track = '22000000' if lit else '22ffffff'
        o.append('\t\t\t<control type="group"><visible>%s</visible>' % v)
        o.append('\t\t\t\t<control type="image"><left>%d</left><top>0</top><width>%d</width><height>%d</height><texture colordiffuse="%s">common/white.png</texture></control>' % (h, w, h, bg))
        o.append('\t\t\t\t<control type="label"><left>%d</left><top>0</top><width>%d</width><height>%d</height><aligny>center</aligny><font>pl_ui_24_bold</font><textcolor>%s</textcolor><label>%s</label></control>' % (h + 28, w - 28 - 100, h, ink, lab))
        o.append('\t\t\t\t<control type="label"><left>%d</left><top>0</top><width>80</width><height>%d</height><align>right</align><aligny>center</aligny><font>pl_small_20_semibold</font><textcolor>%s</textcolor><label>%s</label></control>' % (h + w - 28 - 80, h, ink2, rem))
        o.append('\t\t\t\t<control type="progress"><left>%d</left><top>%d</top><width>%d</width><height>6</height><texturebg colordiffuse="%s">common/aeon_line_6.png</texturebg><midtexture colordiffuse="%s">common/aeon_line_6.png</midtexture><info>%s</info></control>' % (h, h - 6, w, track, line, prog))
        o.append('\t\t\t</control>')
    o += ['\t\t</definition>', '\t</include>']
    return '\n'.join(o) + '\n'


# 1. shared pieces and the two expressions (Includes_Fused.xml, beside the Fused Glass skip button)
F = '1080i/Includes_Fused.xml'
f = io.open(F, encoding='utf-8').read()
assert 'Aeon_SkipPair' not in f
anchor = '\t<expression name="FG_SkipGlass">'
block = ('\t<!-- Aeon theme skip button (0.40.3, Skin settings > Behaviour > Skippy: skip button style): Box pair or Clock dock -->\n'
         '\t<expression name="Aeon_SkipClock">!Skin.HasSetting(aeon.vglass) + String.IsEqual(Skin.String(aeon.skippy.aeonstyle),clock)</expression>\n'
         '\t<expression name="Aeon_SkipPair">!Skin.HasSetting(aeon.vglass) + !String.IsEqual(Skin.String(aeon.skippy.aeonstyle),clock)</expression>\n'
         + cells('Aeon_SkipCells96', 96, 360, 28) + cells('Aeon_SkipCells108', 108, 420, 32))
f = f.replace(anchor, block + anchor, 1)
# the button's own texture: the white block stays Glass's; Fused Glass and the Aeon theme draw their own boxes
old = ('\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_SkipBtnTex_fg</include>\n'
       '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">FG_SkipBtnTex_old</include>')
assert old in f
f = f.replace(old, '\t\t<include condition="Skin.HasSetting(aeon.fglass) | !Skin.HasSetting(aeon.vglass)">FG_SkipBtnTex_fg</include>\n'
                   '\t\t<include condition="Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">FG_SkipBtnTex_old</include>')
io.open(F, 'w', encoding='utf-8', newline='\n').write(f)
ET.parse(F)

# 2. the skip dialog
D = '1080i/Custom_1167_SkippySkip.xml'
d = io.open(D, encoding='utf-8').read()
n = d.count('<visible>!$EXP[Aeon_FGlass]</visible>')
assert n == 4, n
d = d.replace('<visible>!$EXP[Aeon_FGlass]</visible>', '<visible>Skin.HasSetting(aeon.vglass) + !$EXP[Aeon_FGlass]</visible>')
i = d.rindex('\t</controls>')
aeon = '''		<!-- Aeon theme (0.40.3): the box pair at the bottom right, or the row of tile, label cell and clock box at the top right -->
		<control type="group">
			<left>1464</left><top>834</top>
			<visible>$EXP[Aeon_SkipPair]</visible>
			<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="120,0" end="0,0" time="300" tween="cubic" easing="out"/><effect type="fade" start="0" end="100" time="200"/></animation>
			<animation type="WindowClose"><effect type="fade" start="100" end="0" time="200"/></animation>
			<include content="Aeon_SkipCells96"><param name="lit" value="true"/></include>
		</control>
		<control type="group">
			<visible>$EXP[Aeon_SkipClock]</visible>
			<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="0,-108" end="0,0" time="300" tween="cubic" easing="out"/><effect type="fade" start="0" end="100" time="200"/></animation>
			<animation type="WindowClose"><effect type="fade" start="100" end="0" time="200"/></animation>
			<control type="group">
				<left>1292</left><top>0</top>
				<include content="Aeon_SkipCells108"><param name="lit" value="true"/></include>
			</control>
			<include>Aeon_ClockBoxAeon</include>
		</control>
'''
d = d[:i] + aeon + d[i:]
io.open(D, 'w', encoding='utf-8', newline='\n').write(d)
ET.parse(D)

# 3. the player controls: the same boxes, dark until Up from the seek bar focuses them
O = '1080i/Includes_Aeon_OSD.xml'
o = io.open(O, encoding='utf-8').read()
old_up = '<onup condition="$EXP[Aeon_FGlass] + $EXP[FG_SkipAsk]">SetFocus(88)</onup>\n\t\t\t<onup condition="![$EXP[Aeon_FGlass] + $EXP[FG_SkipAsk]]">Action(Info,fullscreenvideo)</onup>'
assert old_up in o
o = o.replace(old_up, '<onup condition="[$EXP[Aeon_FGlass] | !Skin.HasSetting(aeon.vglass)] + $EXP[FG_SkipAsk]">SetFocus(88)</onup>\n'
                      '\t\t\t<onup condition="![[$EXP[Aeon_FGlass] | !Skin.HasSetting(aeon.vglass)] + $EXP[FG_SkipAsk]]">Action(Info,fullscreenvideo)</onup>')
old_vis = '\t\t\t<visible>$EXP[Aeon_FGlass] + $EXP[FG_SkipAsk]</visible>\n'
assert o.count(old_vis) == 1
o = o.replace(old_vis, '\t\t\t<visible>$EXP[FG_SkipAsk] + [$EXP[Aeon_FGlass] | !Skin.HasSetting(aeon.vglass)]</visible>\n')
for old, new in (('<visible>!$EXP[FG_SkipGlass]</visible>', '<visible>$EXP[Aeon_FGlass] + !$EXP[FG_SkipGlass]</visible>'),
                 ('<visible>$EXP[FG_SkipGlass]</visible>', '<visible>$EXP[Aeon_FGlass] + $EXP[FG_SkipGlass]</visible>')):
    a = o.index('<control type="button" id="88">')
    k = o.rindex(old, 0, a)
    o = o[:k] + new + o[k + len(old):]
a = o.index('\t\t\t<control type="button" id="88">')
o = o[:a] + '''			<!-- Aeon theme (0.40.3): box pair above the controls, or tile and label cell beside the clock box -->
			<control type="group">
				<left>1464</left><top>672</top>
				<visible>$EXP[Aeon_SkipPair]</visible>
				<include content="Aeon_SkipCells96"><param name="lit" value="Control.HasFocus(88)"/></include>
			</control>
			<control type="group">
				<left>1292</left><top>0</top>
				<visible>$EXP[Aeon_SkipClock]</visible>
				<include content="Aeon_SkipCells108"><param name="lit" value="Control.HasFocus(88)"/></include>
			</control>
''' + o[a:]
io.open(O, 'w', encoding='utf-8', newline='\n').write(o)
ET.parse(O)
print('skip button built')
