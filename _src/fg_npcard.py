"""0.39.7 Music now playing page (MusicVisualisation, Aeon_NowPlaying), Fused Glass: the card and the cover get the round
corners of the other Fused cards (r28; large covers use r28 too, fg/m596x596).
- card (140..960 x 190..890): frosted r28 with the hairline edge instead of the square tinted block and its two edge
  lines; the song's progress is one bar revealed from the left inside the same shape (was 35 stacked 20 px bars).
- cover (1040..1740, 700 px): new mask fg/m700x700.png (r28), scalediffuse false; the lyrics shade over it the same.
Other themes keep the square look. Run from the skin folder: python _src/fg_npcard.py"""
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw   # noqa: E402

S = 8
big = Image.new('L', (700 * S, 700 * S), 0)
ImageDraw.Draw(big).rounded_rectangle((0, 0, 700 * S - 1, 700 * S - 1), radius=28 * S, fill=255)
m = Image.new('RGBA', (700, 700), (255, 255, 255, 0))
m.putalpha(big.resize((700, 700), Image.BOX))
m.save(os.path.join('media', 'fg', 'm700x700.png'), optimize=True)
print('wrote fg/m700x700.png')

p = os.path.join('1080i', 'Includes_Aeon_Music.xml')
s = io.open(p, encoding='utf-8').read()
FG = '<visible>$EXP[Aeon_FGlass]</visible>'
NFG = '<visible>!$EXP[Aeon_FGlass]</visible>'


def once(old, new):
    global s
    assert s.count(old) == 1, old[:90]
    s = s.replace(old, new)


# a. the card
once('''			<control type="image">
				<left>0</left>
				<top>0</top>
				<width>aeon_np_w</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="88101010">common/white.png</texture>
			</control>''', '''			<control type="image">
				<left>0</left>
				<top>0</top>
				<width>aeon_np_w</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="88101010">common/white.png</texture>
				%s
			</control>
			<!-- Fused Glass (0.39.7): a frosted r28 card; the song's progress revealed from the left inside the same shape -->
			<control type="image"><width>aeon_np_w</width><height>aeon_np_h</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture>%s</control>
			<control type="progress"><width>aeon_np_w</width><height>aeon_np_h</height><reveal>true</reveal><texturebg border="28" colordiffuse="00ffffff">fg/r28.png</texturebg><midtexture border="28" colordiffuse="24ffffff">fg/r28.png</midtexture><info>Player.Progress</info>%s</control>
			<control type="image"><width>aeon_np_w</width><height>aeon_np_h</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture>%s</control>''' % (NFG, FG, FG, FG))
# b. the 35-bar progress: other themes only
once('''			<control type="group">
				<animation effect="fade" end="19" time="0" condition="true">Conditional</animation>''', '''			<control type="group">
				%s
				<animation effect="fade" end="19" time="0" condition="true">Conditional</animation>''' % NFG)
# c. the edge lines: other themes only
once('''				<left>0</left>
				<top>0</top>
				<width>1</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="30ffffff">common/white.png</texture>''', '''				<left>0</left>
				<top>0</top>
				<width>1</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="30ffffff">common/white.png</texture>
				%s''' % NFG)
once('''				<left>aeon_np_w</left>
				<top>0</top>
				<width>1</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="30ffffff">common/white.png</texture>''', '''				<left>aeon_np_w</left>
				<top>0</top>
				<width>1</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="30ffffff">common/white.png</texture>
				%s''' % NFG)
# d. the lyrics shade over the cover
once('''			<control type="image">
				<width>aeon_np_h</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="d8000000">common/white.png</texture>
			</control>''', '''			<control type="image">
				<width>aeon_np_h</width>
				<height>aeon_np_h</height>
				<texture colordiffuse="d8000000">common/white.png</texture>
				%s
			</control>
			<control type="image"><width>aeon_np_h</width><height>aeon_np_h</height><texture border="28" colordiffuse="d8000000">fg/r28.png</texture>%s</control>''' % (NFG, FG))
# e. the cover: a rounded copy for Fused Glass
old = '''			<aspectratio>scale</aspectratio>
			<fadetime>400</fadetime>
			<texture background="true">$VAR[Aeon_NP_Cover]</texture>'''
assert s.count(old) == 1
a = s.index(old)
c0 = s.rindex('\t\t<control type="image">', 0, a)
c1 = s.index('\n\t\t</control>', a) + len('\n\t\t</control>')
block = s[c0:c1]
plain = block.replace('<texture background="true">$VAR[Aeon_NP_Cover]</texture>',
                      '<texture background="true">$VAR[Aeon_NP_Cover]</texture>\n\t\t\t' + NFG)
rounded = block.replace('<aspectratio>scale</aspectratio>', '<aspectratio scalediffuse="false">scale</aspectratio>') \
               .replace('<texture background="true">$VAR[Aeon_NP_Cover]</texture>',
                        '<texture background="true" diffuse="fg/m700x700.png">$VAR[Aeon_NP_Cover]</texture>\n\t\t\t' + FG)
s = s[:c0] + plain + '\n\t\t<!-- Fused Glass (0.39.7): the cover with the round corners of the large covers (r28) -->\n' + rounded + s[c1:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
