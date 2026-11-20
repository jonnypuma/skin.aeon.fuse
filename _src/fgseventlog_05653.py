# -*- coding: utf-8 -*-
"""0.56.53 Kodi's Event log in Fused Glass style (user, 2026-11-20: "kodi event log menu has to be rebuilt in fused
glass style too"): it had the rounded card and white bar of the other looks in every look.

The window's controls after the header become includes picked at load: EventLog_Classic (as they were, every look but
the style) and FGS_EventLog, the Skin settings page spec:
- frame 120-1820 x 108-960, title band 108-191: EVENT LOG over the options | the level filter's label over the events,
  the position (n / total) at the right; the columns split by one line (480), the scroll bar gutter 1800-1820;
- the options (9000: sort order 4, level 21, higher levels 22, clear 20, logging settings 501) as 70 rows of the grid
  from 191, 121-480, the style's bar with the dark fill;
- the events (50) as 70 rows 481-1799: the icon (54), the title over the description, the date at the right; a line on
  top of each row; the focused one the style's bar with the focus shadow and white ink; Right reaches the bar 60
  (square, in the gutter), Up from the first wraps to the last and Down from the last to the first;
- focus group 9100 keeps both (an empty log lands the focus on the options), the empty note in the events column.
Repeatable (the classic controls are taken from EventLog_Classic once it exists)."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '1080i')
P = os.path.join(D, 'EventLog.xml')
FUSED = os.path.join(D, 'Includes_Fused.xml')
L, R, T, B, BAND, ROW, COL, GUT = 120, 1820, 108, 960, 191, 70, 480, 20


def rule(x, y, w, h):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture></control>' % (x, y, w, h))


def row(focused):
    w = R - GUT - COL - 1
    out = ['<control type="image"><left>0</left><top>0</top><width>%d</width><height>1</height>'
           '<texture colordiffuse="12ffffff">common/white.png</texture>%s</control>'
           % (w, '<visible>!Control.HasFocus(50)</visible>' if focused else '')]
    ink, ink2 = 'ccffffff', '66ffffff'
    if focused:
        out.append('<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>150</height>'
                   '<texture border="56" colordiffuse="$VAR[FG_ShadowColM]">fg/sh16.png</texture>'
                   '<visible>Control.HasFocus(50) + $EXP[FGS_ShadowOn]</visible></control>' % (w + 80))
        out.append('<control type="image"><left>0</left><top>0</top><width>%d</width><height>70</height>'
                   '<texture border="20">fg/fgs_bar.png</texture><visible>Control.HasFocus(50)</visible>'
                   '<include>FGS_RowAnim</include></control>' % w)
        ink, ink2 = '$VAR[FGS_Aeon_OnBarInk]', 'ccffffff'
    out.append('<control type="image"><left>24</left><top>8</top><width>54</width><height>54</height><aspectratio>keep</aspectratio>'
               '<texture background="true">$INFO[ListItem.Icon]</texture></control>')
    out.append('<control type="label"><left>100</left><top>5</top><width>%d</width><height>34</height><aligny>center</aligny>'
               '<font>st_ui_24_semibold</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label]</label></control>' % (w - 440, ink))
    out.append('<control type="label"><left>100</left><top>37</top><width>%d</width><height>26</height><aligny>center</aligny>'
               '<font>st_small_20</font><textcolor>%s</textcolor><label>$INFO[ListItem.Property(Event.Description)]</label></control>' % (w - 124, ink2))
    out.append('<control type="label"><left>%d</left><top>5</top><width>300</width><height>34</height><align>right</align><aligny>center</aligny>'
               '<font>st_small_20</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label2]</label></control>' % (w - 324, ink2))
    return ''.join(out)


def option(kind, cid, extra):
    tex = '<include>FGS_RowTex</include>'
    radio = '<include>FGS_RadioTex</include><textwidth>240</textwidth>' if kind == 'radiobutton' else ''   # the name ends before the switch
    return ('<control type="%s" id="%s"><width>%d</width><height>70</height><font>uc_st_ui_24_semibold</font>'
            '<textcolor>ccffffff</textcolor><focusedcolor>$VAR[FGS_Aeon_OnBarInk]</focusedcolor><textoffsetx>24</textoffsetx>'
            '<aligny>center</aligny>%s%s%s</control>' % (kind, cid, COL - L - 1, tex, radio, extra))


def page():
    w = R - GUT - COL - 1
    out = ['<!-- 0.56.53 fgseventlog: the Skin settings page spec -->']
    out += [rule(L, T, R - L + 1, 1), rule(L, B, R - L + 1, 1), rule(L + 1, BAND, R - L - 1, 1)]
    out += [rule(x, T, 1, B - T) for x in (L, COL, R - GUT, R)]
    out.append('<control type="label"><left>%d</left><top>120</top><width>320</width><height>60</height><aligny>center</aligny>'
               '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]$LOCALIZE[31264][/UPPERCASE]</label></control>' % (L + 24))
    out.append('<control type="label"><left>%d</left><top>120</top><width>%d</width><height>60</height><aligny>center</aligny>'
               '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]$INFO[Control.GetLabel(21)][/UPPERCASE]</label></control>'
               % (COL + 25, w - 300))
    out.append('<control type="label"><left>%d</left><top>120</top><width>260</width><height>60</height><align>right</align><aligny>center</aligny>'
               '<font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[Container(50).CurrentItem]  /  $INFO[Container(50).NumItems]</label>'
               '<visible>Integer.IsGreater(Container(50).NumItems,0)</visible></control>' % (R - GUT - 24 - 260))
    opts = (option('togglebutton', '4', '<label>$LOCALIZE[31223] $LOCALIZE[584]</label><altlabel>$LOCALIZE[31223] $LOCALIZE[585]</altlabel>')
            + option('button', '21', '') + option('radiobutton', '22', '') + option('button', '20', '<label>$LOCALIZE[192]</label>')
            + option('button', '501', '<label>$LOCALIZE[5]</label><onclick>ActivateWindow(systemsettings,logging)</onclick>'))
    out.append('<control type="group" id="9100">'
               '<control type="list" id="50"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<onup>Action(LastPage)</onup><ondown>Action(FirstPage)</ondown><onleft>9000</onleft><onright>60</onright>'
               '<pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime><viewtype label="535">list</viewtype>'
               '<itemlayout width="%d" height="70">%s</itemlayout><focusedlayout width="%d" height="70">%s</focusedlayout></control>'
               '<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<orientation>vertical</orientation><itemgap>0</itemgap><onup>9000</onup><ondown>9000</ondown><onleft>noop</onleft>'
               '<onright>50</onright><onback>50</onback>%s</control></control>'
               % (COL + 1, BAND, w, B - BAND - 1, w, row(False), w, row(True), L + 1, BAND, COL - L - 1, ROW * 5, opts))
    out.append('<control type="scrollbar" id="60"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus /><orientation>vertical</orientation>'
               '<showonepage>false</showonepage><onleft>50</onleft><onright>noop</onright></control>' % (R - GUT + 1, BAND + 1, GUT - 1, B - BAND - 1))
    out.append('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>70</height><aligny>center</aligny>'
               '<font>st_ui_24_semibold</font><textcolor>66ffffff</textcolor><label>$LOCALIZE[31224]</label>'
               '<visible>Integer.IsEqual(Container(50).NumItems,0) + !Container.IsUpdating</visible></control>' % (COL + 25, BAND, w - 48))
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
    if '<include name="EventLog_Classic">' in t:
        i = t.index('<include name="EventLog_Classic">')
        classic = t[i + len('<include name="EventLog_Classic">'):t.index('</include>\n\t<!-- end EventLog_Classic -->', i)].strip('\n\t')
    else:
        classic = s[a:e].strip('\n\t')
    t = put(t, 'EventLog_Classic', classic)
    t = put(t, 'FGS_EventLog', page())
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    s = (s[:a] + '\n\t\t<include condition="!$EXP[FGS]">EventLog_Classic</include>'
         '\n\t\t<include condition="$EXP[FGS]">FGS_EventLog</include><!-- 0.56.53 fgseventlog -->\n\t' + s[e:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('event log: classic + style layouts')


if __name__ == '__main__':
    main()
