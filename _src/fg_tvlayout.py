"""0.39.5 Live TV windows (Channels, Recordings, Timers, Search: Misc_PVRList):
- The list card is as wide as the area tabs card above it (102 .. 1334, was 100 .. 1224); the list 1190 wide (was
  1080), its scroll bar at the card's right edge.
- The info panel beside it is narrower (x 1380, 440 wide, ending under the clock box; was 1264 / 560) and the channel
  icon is much smaller (150 px, was 300), the text under it moved up by the difference. New constants
  misc_pvr_panel_x / misc_pvr_panel_w (list_panel_x / _w stay for the TV channel guide dialog).
- Options row, Fused Glass: the radio buttons (Filter, Show hidden, Group items, Show deleted, Hide disabled:
  Misc_SubNavRadio) and the Recordings watched filter (button 10) are frosted pills with the round white focus like
  Group / Sort / Order; the radio mark sits 16 px inside the pill's right end.
Run in 1080i."""
import io
import re

p = 'Constants.xml'
c = io.open(p, encoding='utf-8').read()
if 'misc_pvr_panel_x' not in c:
    c = c.replace('\t<constant name="list_panel_w">560</constant>\n',
                  '\t<constant name="list_panel_w">560</constant>\n'
                  '\t<constant name="misc_pvr_panel_x">1380</constant>     <!-- Live TV windows: info panel beside the list card (0.39.5) -->\n'
                  '\t<constant name="misc_pvr_panel_w">440</constant>\n', 1)
    assert 'misc_pvr_panel_x' in c
io.open(p, 'w', encoding='utf-8', newline='').write(c)

p = 'Includes_Misc.xml'
s = io.open(p, encoding='utf-8').read()

# list card + list + scroll bar
a = s.index('\t<include name="Misc_PVRList">')
b = s.index('\n\t</include>', a)
blk = s[a:b]
old = '''				<left>100</left>
				<top>230</top>
				<width>1124</width>
				<height>830</height>
				<include>AG_Card</include>'''
assert old in blk
blk = blk.replace(old, old.replace('<left>100</left>', '<left>102</left>').replace('<width>1124</width>', '<width>1232</width>'))
assert blk.count('<width>list_w</width>') == 1
blk = blk.replace('<width>list_w</width>', '<width>1190</width>')
blk = blk.replace('<param name="width" value="1080"/>', '<param name="width" value="1190"/>')
assert '<param name="left" value="1196"/>' in blk
blk = blk.replace('<param name="left" value="1196"/>', '<param name="left" value="1306"/>')
s = s[:a] + blk + s[b:]

# info panel
a = s.index('\t<include name="Misc_PVRInfoPanel">')
b = s.index('\n\t</include>', a)
blk = s[a:b].replace('list_panel_x', 'misc_pvr_panel_x').replace('list_panel_w', 'misc_pvr_panel_w')
old = '''				<width>misc_pvr_panel_w</width>
				<height>300</height>
				<aspectratio align="left" aligny="top">keep</aspectratio>'''
assert old in blk
blk = blk.replace(old, '''				<width>150</width>
				<height>150</height>
				<aspectratio align="left" aligny="top">keep</aspectratio>''')
for t0, t1 in ((320, 170), (352, 202), (396, 246), (436, 286), (456, 306)):
    n = blk.count('<top>%d</top>' % t0)
    assert n == 1, (t0, n)
    blk = blk.replace('<top>%d</top>' % t0, '<top>%d</top>' % t1)
# the plot gets the room the icon gave back (bottom stays at 686)
i = blk.index('<top>306</top>')
j = blk.index('<height>230</height>', i)
assert j - i < 200
blk = blk[:j] + '<height>380</height>' + blk[j + len('<height>230</height>'):]
s = s[:a] + blk + s[b:]

# options row: radio buttons as pills
a = s.index('\t<include name="Misc_SubNavRadio">')
b = s.index('\n\t</include>', a)
blk = s[a:b]
blk = blk.replace('<param name="visible">true</param>', '<param name="visible">true</param>\n\t\t<param name="radiox">0</param>', 1)
old = '''				<textoffsetx>12</textoffsetx>
				<include>Aeon_TexRowFocus</include>
				<texturenofocus />'''
assert old in blk
blk = blk.replace(old, '''				<include>FG_SubNavRadioX</include>
				<include>FG_SubNavFocus</include>
				<include>FG_SubNavNoFocus</include>''')
blk = blk.replace('<radiowidth>18</radiowidth>', '<radiowidth>18</radiowidth>\n\t\t\t\t<radioposx>$PARAM[radiox]</radioposx>', 1)
s = s[:a] + blk + s[b:]
# each radio: the mark 16 px inside the right end (width - 18 - 16)
def radiox(m):
    w = int(m.group(2))
    return m.group(0) + '\n\t\t\t<param name="radiox" value="%d"/>' % (w - 34)
s, n = re.subn(r'(<include content="Misc_SubNavRadio">(?:\s*<param name="(?:id|label)" value="[^"]*"/>)*\s*<param name="width" value="(\d+)"/>)', radiox, s)
assert n == 6, n
s = s.replace('<include content="Misc_SubNavRadio">\n\t\t\t<param', '<include content="Misc_SubNavRadio">\n\t\t\t<param', 1)
# Recordings watched filter
old = '''			<description>Watched filter (Kodi sets the label)</description>
			<width>auto</width>
			<height>subnav_h</height>
			<font>cap_20</font>
			<textcolor>$VAR[AG_Ink2]</textcolor>
			<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>
			<textoffsetx>12</textoffsetx>
			<include>Aeon_TexRowFocus</include>
			<texturenofocus />'''
assert old in s
s = s.replace(old, old.replace('''			<textoffsetx>12</textoffsetx>
			<include>Aeon_TexRowFocus</include>
			<texturenofocus />''', '''			<include>FG_SubNavRadioX</include>
			<include>FG_SubNavFocus</include>
			<include>FG_SubNavNoFocus</include>'''))
io.open(p, 'w', encoding='utf-8', newline='').write(s)

for f in ('MyPVRRecordings.xml', 'MyPVRTimers.xml'):
    x = io.open(f, encoding='utf-8').read()
    x = x.replace('list_panel_x', 'misc_pvr_panel_x').replace('list_panel_w', 'misc_pvr_panel_w')
    io.open(f, 'w', encoding='utf-8', newline='').write(x)

p = 'Includes_Fused.xml'
t = io.open(p, encoding='utf-8').read()
if 'FG_SubNavRadioX' not in t:
    t = t.replace('\t<include name="FG_SubNavFocus">', '''	<!-- options-row radios / buttons: text inset 20 inside the Fused pill (12 elsewhere, as before) -->
	<include name="FG_SubNavRadioX">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_SubNavRadioX_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">FG_SubNavRadioX_old</include>
	</include>
	<include name="FG_SubNavRadioX_fg"><textoffsetx>20</textoffsetx></include>
	<include name="FG_SubNavRadioX_old"><textoffsetx>12</textoffsetx></include>
	<include name="FG_SubNavFocus">''', 1)
    assert 'FG_SubNavRadioX' in t
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('ok')
