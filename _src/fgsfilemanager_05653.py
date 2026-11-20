# -*- coding: utf-8 -*-
"""0.56.53 Kodi's File manager in Fused Glass style (user, 2026-11-20: every standard menu on the one page spec; box
shot: two rounded cards with the white pill of the other looks).

The window's controls after the header become EventLog-style includes: FM_Classic (as they were, every look but the
style) and FGS_FileManager, the Skin settings page spec with two panes:
- frame 120-1820 x 108-960, title band 108-191 per pane: the pane's path (label 101 / 102, Kodi writes it) and
  "n of total"; lines at 120 | left pane 121-949 | 950 gutter 970 | right pane 971-1799 | 1800 gutter 1820;
- the files as 70 rows: the icon (40), the name, label2 (size / date) at the right, the check (fg_mark) on marked
  items; a line on top of each row; the focused row the style's bar with the focus shadow and white ink; the other
  pane's current row the dimmed bar (as the open category in Skin settings);
- the walk as before: Right list 20 > bar 60 (when it scrolls) > list 21 > bar 61, Left back; Up / Down wrap; Back on a
  bar returns to its list. The bars are square, in the gutters.
Repeatable."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '1080i')
P = os.path.join(D, 'FileManager.xml')
FUSED = os.path.join(D, 'Includes_Fused.xml')
L, R, T, B, BAND, ROW, GUT = 120, 1820, 108, 960, 191, 70, 20
MID = 950                                       # the left pane's right line; its gutter 950-970


def rule(x, y, w, h):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture></control>' % (x, y, w, h))


def row(lid, w, focused):
    out = ['<control type="image"><left>0</left><top>0</top><width>%d</width><height>1</height>'
           '<texture colordiffuse="12ffffff">common/white.png</texture>%s</control>'
           % (w, '<visible>!Control.HasFocus(%s)</visible>' % lid if focused else '')]
    ink, ink2 = 'ccffffff', '66ffffff'
    if focused:
        out.append('<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>150</height>'
                   '<texture border="56" colordiffuse="$VAR[FG_ShadowColM]">fg/sh16.png</texture>'
                   '<visible>Control.HasFocus(%s) + $EXP[FGS_ShadowOn]</visible></control>' % (w + 80, lid))
        out.append('<control type="image"><left>0</left><top>0</top><width>%d</width><height>70</height>'
                   '<texture border="20">fg/fgs_bar.png</texture><visible>Control.HasFocus(%s)</visible>'
                   '<include>FGS_RowAnim</include></control>' % (w, lid))
        out.append('<control type="image"><left>0</left><top>0</top><width>%d</width><height>70</height>'
                   '<texture border="20" colordiffuse="40ffffff">fg/fgs_bar.png</texture><visible>!Control.HasFocus(%s) + !String.IsEmpty(ListItem.Label)</visible></control>' % (w, lid))
    out.append('<control type="image"><left>24</left><top>15</top><width>40</width><height>40</height><aspectratio>keep</aspectratio>'
               '<texture background="true" colordiffuse="b3ffffff">$INFO[ListItem.Icon]</texture></control>')
    for vis, col in (('!ListItem.IsSelected', ink), ('ListItem.IsSelected', 'fg_mark')):
        c = col
        out.append('<control type="label"><left>84</left><top>0</top><width>%d</width><height>70</height><aligny>center</aligny>'
                   '<font>st_ui_24_semibold</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label]</label>%s<visible>%s</visible></control>'
                   % (w - 330, c, '<scroll>true</scroll>' if focused else '', vis))
    out.append('<control type="label"><left>%d</left><top>0</top><width>200</width><height>70</height><align>right</align><aligny>center</aligny>'
               '<font>st_small_20</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label2]</label></control>' % (w - 224, ink2))
    out.append('<control type="image"><left>%d</left><top>23</top><width>24</width><height>24</height>'
               '<texture colordiffuse="fg_mark">markers/check.png</texture><visible>ListItem.IsSelected</visible></control>' % (w - 260))
    return ''.join(out)


def pane(x0, x1, lid, sid, head, count, nav, snav, top=BAND, extra=''):
    """one pane: its heading and count in the title band, the list from top, the square bar in its gutter at x1"""
    w = x1 - x0
    out = [head % (x0 + 24, w - 260) if '%d' in head else head,
           count % (x1 - 224) if '%d' in count else count]
    out.append('<control type="list" id="%s"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<onup>%s</onup><ondown>%s</ondown>%s<pagecontrol>%s</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>%s'
               '<itemlayout width="%d" height="70">%s</itemlayout><focusedlayout width="%d" height="70">%s</focusedlayout></control>'
               % (lid, x0, top, w, B - top - 1, lid, lid, nav, sid, extra, w, row(lid, w, False), w, row(lid, w, True)))
    out.append('<control type="scrollbar" id="%s"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus /><orientation>vertical</orientation>'
               '<showonepage>false</showonepage>%s<onback>%s</onback></control>' % (sid, x1 + 1, top + 1, GUT - 1, B - top - 1, snav, lid))
    return ''.join(out)


HEAD_ID = ('<control type="label" id="%s"><left>%%d</left><top>120</top><width>%%d</width><height>60</height><aligny>center</aligny>'
           '<font>st_ui_24_semibold</font><textcolor>$VAR[AG_Ink]</textcolor></control>')
HEAD_TXT = ('<control type="label"><left>%%d</left><top>120</top><width>%%d</width><height>60</height><aligny>center</aligny>'
            '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>')
COUNT_POS = ('<control type="label"><left>%%d</left><top>120</top><width>200</width><height>60</height><align>right</align><aligny>center</aligny>'
             '<font>st_small_20</font><textcolor>80ffffff</textcolor>'
             '<label>$INFO[Container(%s).CurrentItem]$INFO[Container(%s).NumItems, $ADDON[skin.aeon.fuse 32285] ,]</label></control>')
COUNT_ID = ('<control type="label" id="%s"><left>%%d</left><top>120</top><width>200</width><height>60</height><align>right</align><aligny>center</aligny>'
            '<font>st_small_20</font><textcolor>80ffffff</textcolor></control>')


def page():
    out = ['<!-- 0.56.53 fgsfilemanager: the Skin settings page spec, two panes -->']
    out += [rule(L, T, R - L + 1, 1), rule(L, B, R - L + 1, 1), rule(L + 1, BAND, R - L - 1, 1)]
    out += [rule(x, T, 1, B - T) for x in (L, MID, MID + GUT, R - GUT, R)]
    lnav = ('<onleft>noop</onleft><onright condition="Container(20).HasNext | Container(20).HasPrevious">60</onright>'
            '<onright condition="!Container(20).HasNext + !Container(20).HasPrevious">21</onright>')
    rnav = ('<onleft condition="Container(20).HasNext | Container(20).HasPrevious">60</onleft>'
            '<onleft condition="!Container(20).HasNext + !Container(20).HasPrevious">20</onleft>'
            '<onright condition="Container(21).HasNext | Container(21).HasPrevious">61</onright>'
            '<onright condition="!Container(21).HasNext + !Container(21).HasPrevious">noop</onright>')
    out.append(pane(L + 1, MID, '20', '60', HEAD_ID % '101', COUNT_POS % ('20', '20'), lnav, '<onleft>20</onleft><onright>21</onright>'))
    out.append(pane(MID + GUT + 1, R - GUT, '21', '61', HEAD_ID % '102', COUNT_POS % ('21', '21'), rnav, '<onleft>21</onleft><onright>noop</onright>'))
    return '\n\t\t'.join(out)


def put(t, name, content):
    body = '\t<include name="%s">\n\t\t%s\n\t</include>\n\t<!-- end %s -->\n' % (name, content, name)
    if '<include name="%s">' % name in t:
        i = t.index('\t<include name="%s">' % name)
        j = t.index('<!-- end %s -->' % name, i) + len('<!-- end %s -->\n' % name)
        return t[:i] + body + t[j:]
    k = t.index('\t<include name="FGS_RowTex">')
    return t[:k] + body + t[k:]


def main():
    s = io.open(P, encoding='utf-8').read()
    t = io.open(FUSED, encoding='utf-8').read()
    a = s.index('</include>', s.index('<include content="AG_TopBar">')) + len('</include>')
    e = s.rindex('</controls>')
    if '<include name="FM_Classic">' in t:
        i = t.index('<include name="FM_Classic">')
        classic = t[i + len('<include name="FM_Classic">'):t.index('</include>\n\t<!-- end FM_Classic -->', i)].strip('\n\t')
    else:
        classic = s[a:e].strip('\n\t')
    t = put(t, 'FM_Classic', classic)
    t = put(t, 'FGS_FileManager', page())
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    s = (s[:a] + '\n\t\t<include condition="!$EXP[FGS]">FM_Classic</include>'
         '\n\t\t<include condition="$EXP[FGS]">FGS_FileManager</include><!-- 0.56.53 fgsfilemanager -->\n\t' + s[e:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('file manager: classic + style layouts')


if __name__ == '__main__':
    main()
