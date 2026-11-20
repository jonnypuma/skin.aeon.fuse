"""0.56.46 Fused Glass style, the Add-ons window's list (FGS_AddonRow / FGS_View50, Includes_Views.xml), the user,
2026-11-18: "the highlight bar in Fused Glass overlaps the scrollbar and outer edge of the addon label and version
cell. also the highlight bar should just have an upper and lower line, not be a rectangle".
The focused row had a top line, a bottom line and a right edge (on the scrollbar at 1556), all inside the focus
animation (Pop zooms the row to 101.2 %, 7 px past both ends). Now: the top and bottom lines only, outside the
animation, and every row rule stops 6 px before the scrollbar (1190 of the 1200 wide list); the white bar on the
divider keeps its animation. Run from the skin folder. Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Views.xml')
MARK = '<!-- 0.56.46 fgs_addonrow -->'


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('fgs_addonrow: already done')
        return
    s = t.index('<include name="FGS_AddonRow">')
    e = t.index('</include>', t.index('</definition>', s))
    blk = t[s:e]
    old_group = ('\t\t\t<control type="group">\n'
                 '\t\t\t\t<visible>$PARAM[focused] + Control.HasFocus(50)</visible>\n'
                 '\t\t\t\t<include>FGS_RowAnim</include>\n'
                 '\t\t\t\t<control type="image"><left>0</left><top>-1</top><width>1200</width><height>1</height><texture colordiffuse="44ffffff">common/white.png</texture></control>\n'
                 '\t\t\t\t<control type="image"><left>0</left><top>99</top><width>1200</width><height>1</height><texture colordiffuse="44ffffff">common/white.png</texture></control>\n'
                 '\t\t\t\t<control type="image"><left>1199</left><top>0</top><width>1</width><height>100</height><texture colordiffuse="44ffffff">common/white.png</texture></control>\n'
                 '\t\t\t\t<control type="image"><left>448</left><top>0</top><width>5</width><height>100</height><texture>common/white.png</texture></control>\n'
                 '\t\t\t</control>\n')
    assert old_group in blk, 'focused group'
    new_group = ('\t\t\t' + MARK + ' the focus: a line above and below (still), the white bar on the divider (animated)\n'
                 '\t\t\t<control type="group">\n'
                 '\t\t\t\t<visible>$PARAM[focused] + Control.HasFocus(50)</visible>\n'
                 '\t\t\t\t<control type="image"><left>0</left><top>-1</top><width>1190</width><height>1</height><texture colordiffuse="44ffffff">common/white.png</texture></control>\n'
                 '\t\t\t\t<control type="image"><left>0</left><top>99</top><width>1190</width><height>1</height><texture colordiffuse="44ffffff">common/white.png</texture></control>\n'
                 '\t\t\t</control>\n'
                 '\t\t\t<control type="group">\n'
                 '\t\t\t\t<visible>$PARAM[focused] + Control.HasFocus(50)</visible>\n'
                 '\t\t\t\t<include>FGS_RowAnim</include>\n'
                 '\t\t\t\t<control type="image"><left>448</left><top>0</top><width>5</width><height>100</height><texture>common/white.png</texture></control>\n'
                 '\t\t\t</control>\n')
    blk = blk.replace(old_group, new_group)
    rule = '<control type="image"><left>0</left><top>99</top><width>1200</width><height>1</height><texture colordiffuse="12ffffff">common/white.png</texture></control>'
    assert blk.count(rule) == 1, 'row rule'
    blk = blk.replace(rule, rule.replace('<width>1200</width>', '<width>1190</width>'))
    t = t[:s] + blk + t[e:]
    first = ('<control type="image"><left>360</left><top>250</top><width>1200</width><height>1</height><texture colordiffuse="44ffffff">common/white.png</texture>'
             '<visible>Control.HasFocus(50) + Integer.IsEqual(Container(50).Position,0)</visible></control>')
    assert t.count(first) == 1, 'first row line'
    t = t.replace(first, first.replace('<width>1200</width>', '<width>1190</width>'))
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('fgs_addonrow: lines only, clear of the scrollbar')


if __name__ == '__main__':
    main()
