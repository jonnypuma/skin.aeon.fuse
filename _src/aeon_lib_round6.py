# -*- coding: utf-8 -*-
"""0.56.20 Aeon library views, round 6 (chain step 15, after aeon_lib_round5.py). The user (2026-11-17):
- List view (510): "move the List title view up to the top above title label" - the view name ("LIST: TITLE") leaves
  the bar under the list and sits at the top of the info pane, over the title line;
- (PC, Aeon Glass) "look at that diamond due to different color of the highlight bar": the focused row's pointer tip
  was a white square turned 45 degrees laid over the bar's end. In Aeon the bar is white too, so the tip blended in; in
  Aeon Glass the bar is the accent at 29 % and the white square showed as a diamond. The tip is now a triangle that
  starts where the bar ends, in the bar's own colour and texture opacity (aeon/row_tip_*_flat|glass.png, made here);
  Fused Glass keeps its white tip on its white focus bar. Three rows: the List row (Aeon_Row, left tip to the version /
  set pane), Aeon_EpRow and Aeon_SeasonRow (right tips).
Runs once (marker)."""
import io
import os
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
GL = os.path.join('1080i', 'Includes_Aeon_Glass.xml')
MARK = '0.56.20 aeon_lib_round6'


def swap(t, old, new, count=1):
    n = t.count(old)
    assert n == count, (old[:120], n, count)
    return t.replace(old, new)


def tips():
    """left-pointing 54 x 108 (the List row) and right-pointing 48 x 96 (episode / season rows), flat and glass"""
    out = os.path.join('media', 'aeon')
    for name, (w, h), pts in (('l', (54, 108), lambda W, H: [(0, H / 2.0), (W, 0), (W, H)]),
                              ('r', (48, 96), lambda W, H: [(0, 0), (W, H / 2.0), (0, H)])):
        for kind, alpha in (('flat', 255), ('glass', 74)):
            s = 8
            big = Image.new('L', (w * s, h * s), 0)
            ImageDraw.Draw(big).polygon(pts(w * s, h * s), fill=alpha)
            mask = big.resize((w, h), Image.LANCZOS)
            im = Image.new('RGBA', (w, h), (255, 255, 255, 0))
            im.putalpha(mask)
            im.save(os.path.join(out, 'row_tip_%s_%s.png' % (name, kind)))


def main():
    v = io.open(VID, encoding='utf-8').read()
    if MARK in v:
        print('already')
        return
    tips()
    g = io.open(GL, encoding='utf-8').read()
    if 'name="Aeon_RowTipTexL"' not in g:              # Includes_Aeon_Glass.xml is not restored by a chain rebuild
        g = swap(g, '\t<variable name="Aeon_RowFocusCol">',
             '\t<!-- %s: the focused row\'s pointer tip, the bar\'s texture opacity (aeon_row_glass is white at 74) -->\n'
             '\t<variable name="Aeon_RowTipTexL">\n\t\t<value condition="Skin.HasSetting(aeon.vglass)">aeon/row_tip_l_glass.png</value>\n\t\t<value>aeon/row_tip_l_flat.png</value>\n\t</variable>\n'
             '\t<variable name="Aeon_RowTipTexR">\n\t\t<value condition="Skin.HasSetting(aeon.vglass)">aeon/row_tip_r_glass.png</value>\n\t\t<value>aeon/row_tip_r_flat.png</value>\n\t</variable>\n'
             '\t<variable name="Aeon_RowFocusCol">' % MARK)
    # 1. the List row's left tip (to the version / set pane): the bar starts at 54
    old = ('\t\t\t<control type="image">\n\t\t\t\t<left>16</left>\n\t\t\t\t<top>16</top>\n\t\t\t\t<width>76</width>\n\t\t\t\t<height>76</height>\n'
           '\t\t\t\t<texture colordiffuse="lib_aeon_white">common/white.png</texture>\n'
           '\t\t\t\t<animation effect="rotate" start="45" end="45" center="auto" time="0" condition="true">Conditional</animation>\n'
           '\t\t\t\t<visible>$PARAM[focused] + $EXP[Aeon_HasLeftPane]</visible>\n\t\t\t</control>')
    new = ('\t\t\t<!-- %s: the tip in the bar\'s colour and opacity (a white diamond showed on Aeon Glass\'s accent bar) -->\n'
           '\t\t\t<control type="image"><left>0</left><top>0</top><width>54</width><height>aeon_row_h</height><texture colordiffuse="$VAR[Aeon_RowFocusCol_L]">$VAR[Aeon_RowTipTexL]</texture><visible>$PARAM[focused] + $EXP[Aeon_HasLeftPane] + !$EXP[Aeon_FGlass]</visible></control>\n'
           '\t\t\t<control type="image"><left>0</left><top>0</top><width>54</width><height>aeon_row_h</height><texture colordiffuse="lib_aeon_white">aeon/row_tip_l_flat.png</texture><visible>$PARAM[focused] + $EXP[Aeon_HasLeftPane] + $EXP[Aeon_FGlass]</visible></control>' % MARK)
    v = swap(v, old, new)
    # 2. / 3. right tips of the episode and season rows (bars 1040 and 1043 wide, 100 high)
    for left, bar in (('1006', 1040), ('1009', 1043)):
        old = ('\t\t\t<control type="image">\n\t\t\t\t<left>%s</left>\n\t\t\t\t<top>16</top>\n\t\t\t\t<width>68</width>\n\t\t\t\t<height>68</height>\n'
               '\t\t\t\t<texture colordiffuse="aeon_white">common/white.png</texture>\n'
               '\t\t\t\t<animation effect="rotate" start="45" end="45" center="auto" time="0" condition="true">Conditional</animation>\n'
               '\t\t\t\t<visible>$PARAM[focused]</visible>\n\t\t\t</control>' % left)
        new = ('\t\t\t<!-- %s: the tip in the bar\'s colour and opacity -->\n'
               '\t\t\t<control type="image"><left>%d</left><top>2</top><width>48</width><height>96</height><texture colordiffuse="$VAR[Aeon_RowFocusCol]">$VAR[Aeon_RowTipTexR]</texture><visible>$PARAM[focused] + !$EXP[Aeon_FGlass]</visible></control>\n'
               '\t\t\t<control type="image"><left>%d</left><top>2</top><width>48</width><height>96</height><texture colordiffuse="aeon_white">aeon/row_tip_r_flat.png</texture><visible>$PARAM[focused] + $EXP[Aeon_FGlass]</visible></control>' % (MARK, bar, bar))
        v = swap(v, old, new)
    # 4. the List view's name: from the bar under the list to the top of the info pane, over the title line (y 50)
    v = swap(v, '\t\t\t<!-- 0.56.13 aeon_lib510: the info panel rule over the rows: kicker and plot (Aeon, Glass) -->\n',
             '\t\t\t<!-- %s: the view\'s name over the title line ("move the List title view up to the top") -->\n'
             '\t\t\t<control type="label"><left>760</left><top>12</top><width>1010</width><height>30</height><aligny>center</aligny><font>lb_small_20</font><textcolor>99ffffff</textcolor><selectedcolor>99ffffff</selectedcolor><label>[UPPERCASE]$VAR[Aeon_ViewHead]: [B]$VAR[Aeon_SortName][/B][/UPPERCASE]</label><visible>!$EXP[Aeon_FGlass] + Control.IsVisible(510)</visible></control>\n'
             '\t\t\t<!-- 0.56.13 aeon_lib510: the info panel rule over the rows: kicker and plot (Aeon, Glass) -->\n' % MARK)
    w = io.open(V2, encoding='utf-8').read()
    a = w.index('<include name="Aeon_V_Bar510">')
    b = w.index('</include>', a)
    s = w[a:b]
    line = [l for l in s.split('\n') if '<left>1180</left><top>1030</top>' in l and 'Aeon_ViewHead' in l]
    assert len(line) == 1, len(line)
    s = s.replace(line[0] + '\n', '\t\t\t<!-- %s: the view\'s name moved to the top of the info pane -->\n' % MARK)
    w = w[:a] + s + w[b:]
    for p, t in ((VID, v), (V2, w), (GL, g)):
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        ET.parse(p)
    print('ok')


if __name__ == '__main__':
    main()
