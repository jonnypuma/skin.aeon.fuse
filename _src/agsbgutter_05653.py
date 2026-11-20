# -*- coding: utf-8 -*-
"""0.56.53 the scroll bar gutter in every standard window that draws its bar through AG_Scrollbar (user, 2026-11-20:
"you have to make scrollbar gutter for all of Kodi's standard menus too now"): in Fused Glass style the include draws
AG_ScrollbarFGS instead - a 20 px column between two lines centred on the old 6 px bar (lines at left-7 and left+13),
the square bar (19 wide, FGS_SBTex) between them, the same id, navigation and visibility. Other looks keep the round
6 px bar. Lists that ran into the column are narrowed per window after a box shot. Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Dialogs.xml')
FGS = '''	<!-- 0.56.53 the scroll bar gutter (Fused Glass style): two lines 20 apart around the old bar, the square bar between -->
	<include name="AG_ScrollbarFGS">
		<param name="onleft">noop</param>
		<param name="onright">noop</param>
		<param name="onback">noop</param>
		<param name="visible">true</param>
		<param name="showonepage">true</param>
		<definition>
			<control type="group">
				<left>$PARAM[left]</left>
				<top>$PARAM[top]</top>
				<visible>$PARAM[visible]</visible>
				<control type="image"><left>-7</left><top>0</top><width>1</width><height>$PARAM[height]</height><texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture></control>
				<control type="image"><left>13</left><top>0</top><width>1</width><height>$PARAM[height]</height><texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture></control>
				<control type="scrollbar" id="$PARAM[id]">
					<showonepage>$PARAM[showonepage]</showonepage>
					<left>-6</left>
					<top>0</top>
					<width>19</width>
					<height>$PARAM[height]</height>
					<include>FGS_SBTex</include>
					<textureslidernib /><textureslidernibfocus />
					<onleft>$PARAM[onleft]</onleft>
					<onright>$PARAM[onright]</onright>
					<onback>$PARAM[onback]</onback>
					<orientation>vertical</orientation>
				</control>
			</control>
		</definition>
	</include>
'''


def main():
    t = io.open(P, encoding='utf-8').read()
    if '<include name="AG_ScrollbarFGS">' in t:
        print('already')
        return
    i = t.index('\t<include name="AG_Scrollbar">')
    # AG_Scrollbar: in the style hand everything to AG_ScrollbarFGS
    d = t.index('<definition>', i) + len('<definition>')
    hand = ('\n\t\t\t<include content="AG_ScrollbarFGS" condition="$EXP[FGS]"><param name="id" value="$PARAM[id]"/>'
            '<param name="left" value="$PARAM[left]"/><param name="top" value="$PARAM[top]"/><param name="height" value="$PARAM[height]"/>'
            '<param name="onleft" value="$PARAM[onleft]"/><param name="onright" value="$PARAM[onright]"/><param name="onback" value="$PARAM[onback]"/>'
            '<param name="visible" value="$PARAM[visible]"/><param name="showonepage" value="$PARAM[showonepage]"/></include>'
            '\n\t\t\t<include content="AG_ScrollbarRound" condition="!$EXP[FGS]"><param name="id" value="$PARAM[id]"/>'
            '<param name="left" value="$PARAM[left]"/><param name="top" value="$PARAM[top]"/><param name="height" value="$PARAM[height]"/>'
            '<param name="onleft" value="$PARAM[onleft]"/><param name="onright" value="$PARAM[onright]"/><param name="onback" value="$PARAM[onback]"/>'
            '<param name="visible" value="$PARAM[visible]"/><param name="showonepage" value="$PARAM[showonepage]"/></include>')
    e = t.index('</definition>', d)
    old_body = t[d:e]
    head = t[i:d].replace('<include name="AG_Scrollbar">', '<include name="AG_ScrollbarRound">', 1)
    rnd = head + old_body + '</definition>\n\t</include>\n'
    j = t.index('</include>', e) + len('</include>\n')
    new = t[i:d] + hand + '\n\t\t</definition>\n\t</include>\n' + rnd + FGS
    t = t[:i] + new + t[j:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('AG_Scrollbar: gutter in the style')


if __name__ == '__main__':
    main()
