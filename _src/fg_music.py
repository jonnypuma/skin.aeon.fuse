"""Fused Glass, music views (0.32.0). Run once from 1080i.
- Focused text in the album / song lists is dark ink on the white pill (Aeon_VInkF / Aeon_VInk2F / Aeon_VRatingF had
  white for Glass, which Fused inherited: the focused row read white on white).
- Album list / song list rows (Aeon_V_SongRow, 532 / 533): the pill inset in the row, no divider, the cover rounded.
- Cover showcase (531): covers rounded, the focus a ring inside the cover instead of the white frame, and a frosted
  stand-in where an album has no cover (the frame showed as a plain white square).
- Album list side cover and biography panel (532): rounded, frosted.
- Music List (513): the list and the artist / album column as two frosted cards, the cover rounded, the pill inset."""
import io

F = '$EXP[Aeon_FGlass]'
SD = '<aspectratio scalediffuse="false">scale</aspectratio>'


def patch(path, pairs, many=()):
    s = io.open(path, encoding='utf-8').read()
    for i, (a, b) in enumerate(pairs):
        assert s.count(a) == 1 or (i in many and s.count(a) > 1), (path, a[:110], s.count(a))
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


if __name__ == '__main__':
    done = '<variable name="Aeon_VInkF">\n\t\t<value condition="Skin.HasSetting(aeon.fglass)">'
    if done not in io.open('Includes_Aeon_Sub.xml', encoding='utf-8').read():
      patch('Includes_Aeon_Sub.xml', [
        ('\t<variable name="Aeon_VInkF">\n', '\t<variable name="Aeon_VInkF">\n\t\t<value condition="Skin.HasSetting(aeon.fglass)">ff0f1115</value>\n'),
        ('\t<variable name="Aeon_VInk2F">\n', '\t<variable name="Aeon_VInk2F">\n\t\t<value condition="Skin.HasSetting(aeon.fglass)">b30f1115</value>\n'),
        ('\t<variable name="Aeon_VRatingF">\n', '\t<variable name="Aeon_VRatingF">\n\t\t<value condition="Skin.HasSetting(aeon.fglass)">ff0f1115</value>\n'),
        # album list side bio panel
        ('<control type="image"><left>0</left><top>0</top><width>280</width><height>584</height><texture colordiffuse="90101010">common/white.png</texture></control>',
         '<control type="image"><left>0</left><top>0</top><width>280</width><height>584</height><texture colordiffuse="90101010">common/white.png</texture><visible>!%s</visible></control>'
         '<control type="image"><left>0</left><top>0</top><width>280</width><height>584</height><texture border="24" colordiffuse="fg_frost">fg/r24.png</texture><visible>%s</visible></control>'
         '<control type="image"><left>0</left><top>0</top><width>280</width><height>584</height><texture border="24" colordiffuse="fg_edge">fg/e24.png</texture><visible>%s</visible></control>' % (F, F, F)),
    ])
    v = 'Includes_Aeon_Views2.xml'
    patch(v, [
        # song / album rows
        ('<control type="image"><left>0</left><top>0</top><width>1440</width><height>92</height><texture border="16" colordiffuse="$VAR[Aeon_RowFocusCol]">fg/r16.png</texture>',
         '<control type="image"><left>8</left><top>4</top><width>1424</width><height>84</height><texture border="16" colordiffuse="$VAR[Aeon_RowFocusCol]">fg/r16.png</texture>'),
        ('<control type="image"><left>0</left><top>91</top><width>1440</width><height>1</height><texture colordiffuse="22ffffff">common/white.png</texture></control>\n'
         '\t\t\t<control type="image"><left>20</left><top>10</top><width>72</width><height>72</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture></control>',
         '<control type="image"><left>0</left><top>91</top><width>1440</width><height>1</height><texture colordiffuse="22ffffff">common/white.png</texture><visible>!%s</visible></control>\n'
         '\t\t\t<control type="image"><left>20</left><top>10</top><width>72</width><height>72</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture><visible>!%s</visible></control>\n'
         '\t\t\t<control type="image"><left>20</left><top>10</top><width>72</width><height>72</height>%s<texture background="true" diffuse="fg/m72x72.png">$VAR[Aeon_V_Cover]</texture><visible>%s</visible></control>' % (F, F, SD, F)),
        # cover showcase
        ('''					<control type="image"><left>30</left><top>220</top><width>280</width><height>280</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture></control>
					<control type="image"><left>30</left><top>220</top><width>280</width><height>280</height><texture colordiffuse="88000000">common/white.png</texture></control>
				</itemlayout>
				<focusedlayout width="560" height="640">
					<control type="image"><left>30</left><top>60</top><width>500</width><height>500</height><texture colordiffuse="$VAR[Aeon_Accent]">common/white.png</texture><visible>Control.HasFocus(531)</visible></control>
					<control type="image"><left>38</left><top>68</top><width>484</width><height>484</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture></control>
				</focusedlayout>''',
         '''					<control type="image"><left>30</left><top>220</top><width>280</width><height>280</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture><visible>!{F}</visible></control>
					<control type="image"><left>30</left><top>220</top><width>280</width><height>280</height><texture colordiffuse="88000000">common/white.png</texture><visible>!{F}</visible></control>
					<control type="image"><left>30</left><top>220</top><width>280</width><height>280</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture><visible>{F}</visible></control>
					<control type="image"><left>30</left><top>220</top><width>280</width><height>280</height>{SD}<texture background="true" diffuse="fg/m280x280.png">$VAR[Aeon_V_Cover]</texture><visible>{F}</visible></control>
					<control type="image"><left>30</left><top>220</top><width>280</width><height>280</height><texture border="16" colordiffuse="88000000">fg/r16.png</texture><visible>{F}</visible></control>
				</itemlayout>
				<focusedlayout width="560" height="640">
					<control type="image"><left>30</left><top>60</top><width>500</width><height>500</height><texture colordiffuse="$VAR[Aeon_Accent]">common/white.png</texture><visible>Control.HasFocus(531) + !{F}</visible></control>
					<control type="image"><left>38</left><top>68</top><width>484</width><height>484</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture><visible>!{F}</visible></control>
					<control type="image"><left>38</left><top>68</top><width>484</width><height>484</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture><visible>{F}</visible></control>
					<control type="image"><left>38</left><top>68</top><width>484</width><height>484</height>{SD}<texture background="true" diffuse="fg/m484x484.png">$VAR[Aeon_V_Cover]</texture><visible>{F}</visible></control>
					<control type="image"><left>38</left><top>68</top><width>484</width><height>484</height><texture border="16" colordiffuse="ffffffff">fg/ri16.png</texture><visible>Control.HasFocus(531) + {F}</visible></control>
				</focusedlayout>'''.replace('{F}', F).replace('{SD}', SD)),
        # album list side cover
        ('<control type="image"><left>1540</left><top>108</top><width>280</width><height>280</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture></control>',
         '<control type="image"><left>1540</left><top>108</top><width>280</width><height>280</height><aspectratio>scale</aspectratio><texture background="true">$VAR[Aeon_V_Cover]</texture><visible>!%s</visible></control>'
         '<control type="image"><left>1540</left><top>108</top><width>280</width><height>280</height>%s<texture background="true" diffuse="fg/m280x280.png">$VAR[Aeon_V_Cover]</texture><visible>%s</visible></control>' % (F, SD, F)),
    ], many=(3,))
    m = 'Includes_Aeon_MusicLib.xml'
    patch(m, [
        ('''			<control type="image"><left>0</left><top>107</top><width>1820</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture></control>
			<!-- right column: the artist's picture (album: cover), its facts under it -->
			<control type="image">
				<left>1200</left><top>108</top><width>620</width><height>864</height>
				<texture colordiffuse="x_deep_cc">common/white.png</texture>
			</control>
			<control type="image">
				<left>1200</left><top>108</top><width>620</width><height>620</height>
				<aspectratio>scale</aspectratio>
				<fadetime>350</fadetime>
				<texture background="true">$VAR[AeonM_Cover]</texture>
			</control>''',
         '''			<control type="image"><left>0</left><top>107</top><width>1820</width><height>1</height><texture colordiffuse="30ffffff">common/white.png</texture><visible>!{F}</visible></control>
			<!-- right column: the artist's picture (album: cover), its facts under it -->
			<control type="image">
				<left>1200</left><top>108</top><width>620</width><height>864</height>
				<texture colordiffuse="x_deep_cc">common/white.png</texture>
				<visible>!{F}</visible>
			</control>
			<!-- Fused Glass: the list and this column as two frosted cards -->
			<control type="group">
				<visible>{F}</visible>
				<control type="image"><left>12</left><top>116</top><width>1176</width><height>612</height><texture border="28" colordiffuse="fg_frostb">fg/r28.png</texture></control>
				<control type="image"><left>12</left><top>116</top><width>1176</width><height>612</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
				<control type="image"><left>1212</left><top>116</top><width>596</width><height>856</height><texture border="28" colordiffuse="fg_frostb">fg/r28.png</texture></control>
				<control type="image"><left>1212</left><top>116</top><width>596</width><height>856</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
			</control>
			<control type="image">
				<left>1200</left><top>108</top><width>620</width><height>620</height>
				<aspectratio>scale</aspectratio>
				<fadetime>350</fadetime>
				<texture background="true">$VAR[AeonM_Cover]</texture>
				<visible>!{F}</visible>
			</control>
			<control type="image">
				<left>1212</left><top>116</top><width>596</width><height>596</height>
				{SD}
				<fadetime>350</fadetime>
				<texture background="true" diffuse="fg/m596x596.png">$VAR[AeonM_Cover]</texture>
				<visible>{F}</visible>
			</control>'''.replace('{F}', F).replace('{SD}', SD)),
        ('''			<!-- grey band behind header + list -->
			<control type="image">
				<left>0</left>
				<top>108</top>
				<width>1200</width>
				<height>620</height>
				<texture colordiffuse="88202020">common/white.png</texture>
			</control>''',
         '''			<!-- grey band behind header + list -->
			<control type="image">
				<left>0</left>
				<top>108</top>
				<width>1200</width>
				<height>620</height>
				<texture colordiffuse="88202020">common/white.png</texture>
				<visible>!%s</visible>
			</control>''' % F),
        ('''				<width>1200</width>
				<height>100</height>
				<texture border="16" colordiffuse="$VAR[Aeon_RowFocusCol]">fg/r16.png</texture>''',
         '''				<width>1160</width>
				<height>88</height>
				<texture border="16" colordiffuse="$VAR[Aeon_RowFocusCol]">fg/r16.png</texture>'''),
    ])
    # the pill inset: left 20, top 6 (the control above lost its left / top 0 lines in the replace)
    s = io.open(m, encoding='utf-8').read()
    old = '''			<control type="image">
				<left>0</left>
				<top>0</top>
				<width>1160</width>
				<height>88</height>'''
    assert s.count(old) == 1
    s = s.replace(old, old.replace('<left>0</left>', '<left>20</left>').replace('<top>0</top>', '<top>6</top>'))
    io.open(m, 'w', encoding='utf-8', newline='').write(s)
    print('music ok')
