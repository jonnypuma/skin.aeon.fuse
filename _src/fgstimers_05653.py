# -*- coding: utf-8 -*-
"""0.56.53 TV Timers as the week in lanes of time (canvas round 7, idea B; user: "build timer concept B"), Fused Glass
style, TV Timers only (Timer rules and the radio pages keep today's page; MyPVRTimers.xml serves all four).

Kodi's list 50 stays the focus holder (off the eye under the page): Up / Down walk the timers in Kodi's order and the
block of the focused row is lit white; Up goes to the TV tabs (103), Right / Down to the actions. The page: the count,
when the next one starts and how much is set to record; the hours of the span; five lanes (today first) with up to
three timers each, placed and sized by their time (red = recording, gold = reminder (the user's IPTV source cannot record), violet = series, faded when
disabled); a gold line for now; the actions as cells: New timer (Kodi's Add timer row), Edit (the focused row),
Activate / Deactivate (Kodi's timer menu), Delete (helper, asks first), Hide disabled (Kodi's toggle 8).
Data: helper 0.3.122 resources/lib/tmweek.py (aeon.tm.*). Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

DAYS, PER_DAY = 5, 3
WIDTHS = list(range(10, 101, 6))
X0, SPAN = 300, 1520.0
LANE0, LANE_H = 244, 104
P = 'Window(Home).Property(aeon.tm.%s)'
MODE = '$EXP[FGS] + Window.IsActive(TVTimers)'
ADD = '$ADDON[skin.aeon.fuse %d]'


def prop(k):
    return P % k


def block(key):
    f = 'String.IsEqual(%s,%s) + Control.HasFocus(50)' % (prop('focus'), key)
    k = lambda kind: 'String.IsEqual(%s,%s)' % (prop(key + '.k'), kind)
    out = ('<control type="group"><left>%d</left><top>0</top><visible>!String.IsEmpty(%s)</visible>' % (X0, prop(key + '.t')) +
           ''.join('<animation effect="slide" end="%.1f,0" time="0" condition="String.IsEqual(%s,%d)">Conditional</animation>'
                   % (x * SPAN / 100, prop(key + '.x'), x) for x in range(1, 100)) +
           '<animation effect="fade" end="45" time="0" condition="String.IsEqual(%s,1)">Conditional</animation>' % prop(key + '.off'))
    for w in WIDTHS:
        px = int(round(w * SPAN / 100)) - 6
        out += '<control type="group"><visible>String.IsEqual(%s,%d)</visible>' % (prop(key + '.w'), w)
        r12 = lambda diffuse, vis, tex='fg/r12.png': fw.img(0, 0, px, 72, tex, diffuse, vis).replace('<texture colordiffuse', '<texture border="12" colordiffuse')
        out += r12('40e05a4f', '%s + ![%s]' % (k('rec'), f))
        out += r12('2e8c6af2', '%s + ![%s]' % (k('series'), f))
        out += r12('33e8b04b', '%s + ![%s]' % (k('remind'), f))
        out += fw.img(0, 10, 4, 52, 'common/white.png', 'ffe05a4f', '%s + ![%s]' % (k('rec'), f))
        out += fw.img(0, 10, 4, 52, 'common/white.png', 'ff8c6af2', '%s + ![%s]' % (k('series'), f))
        out += fw.img(0, 10, 4, 52, 'common/white.png', 'ffe8b04b', '%s + ![%s]' % (k('remind'), f))
        out += ('<control type="image"><left>-36</left><top>-30</top><width>%d</width><height>132</height>%s<visible>%s + $EXP[FGS_ShadowOn]</visible></control>'
                % (px + 72, fw.SHADOW, f))
        out += r12('ffffffff', f)
        for ink, ink2, vis in (('ffffffff', '99ffffff', '![%s]' % f), ('ff0b0d11', 'b30b0d11', f)):
            out += fw.label(14, 8, px - 24, 30, '$INFO[%s]' % prop(key + '.t'), 'st_small_20_bold', ink, vis=vis, extra='<scroll>false</scroll>')
            out += fw.label(14, 38, px - 24, 26, '$INFO[%s]' % prop(key + '.s'), 'st_small_20', ink2, vis=vis)
        out += '</control>'
    return out + '</control>'


def page():
    out = ('<include name="FGS_TimersWeek"><control type="group"><visible>Window.IsActive(TVTimers)</visible>'
           # the week's own page under the TV tabs: the frame's background fades into it
           )
    # header: how many, when the next one starts, how much is set to record
    out += ('<control type="grouplist"><left>120</left><top>134</top><width>1000</width><height>60</height><orientation>horizontal</orientation>'
            '<itemgap>16</itemgap><usecontrolcoords>true</usecontrolcoords><visible>!String.IsEqual(%s,0)</visible>' % prop('count') +
            '<control type="label"><width>auto</width><height>60</height><aligny>center</aligny><font>st_display_40</font><textcolor>fg_mark</textcolor>'
            '<label>$INFO[%s]</label></control>'
            '<control type="label"><width>auto</width><height>60</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor>'
            '<label>%s</label></control></control>' % (prop('count'), ADD % 32812))
    out += fw.label(120, 134, 1000, 60, ADD % 32816, 'st_ui_28_bold', 'ffffffff', vis='String.IsEqual(%s,0)' % prop('count'))
    out += fw.label(1120, 134, 700, 60, '$INFO[%s]$INFO[%s,  ·  ,]' % (prop('next'), prop('rec')), 'st_small_20', 'a6ffffff', 'right')
    # the hours of the span and their faint lines
    for i in range(7):
        x = X0 + int(i * SPAN / 6)
        out += fw.label(x - (60 if i == 6 else 0), 206, 60, 30, '$INFO[%s]' % prop('h%d' % (i + 1)), 'st_small_20', '73ffffff', 'right' if i == 6 else 'left')
        out += fw.img(x, LANE0, 1, LANE_H * DAYS, 'common/white.png', '0fffffff')
    # the lanes
    for d in range(1, DAYS + 1):
        y = LANE0 + (d - 1) * LANE_H
        out += fw.line(120, y, 1700)
        out += fw.label(120, y + 18, 170, 26, '[UPPERCASE]$INFO[%s][/UPPERCASE]' % prop('d%d.w' % d), 'st_cap_14', 'fg_mark' if d == 1 else '99ffffff')
        out += fw.label(120, y + 44, 170, 44, '$INFO[%s]' % prop('d%d.n' % d), 'st_ui_28_bold', 'ffffffff' if d < 3 else 'b3ffffff')
        out += '<control type="group"><top>%d</top>' % (y + 16) + ''.join(block('d%db%d' % (d, b)) for b in range(1, PER_DAY + 1)) + '</control>'
    out += fw.line(120, LANE0 + LANE_H * DAYS, 1700)
    # now, as a gold line in today's lane
    out += ('<control type="group"><left>%d</left><top>%d</top><visible>!String.IsEmpty(%s)</visible>' % (X0 - 1, LANE0, prop('now')) +
            ''.join('<animation effect="slide" end="%.1f,0" time="0" condition="String.IsEqual(%s,%d)">Conditional</animation>'
                    % (x * SPAN / 100, prop('now'), x) for x in range(1, 100)) +
            fw.img(0, 0, 2, LANE_H, 'common/white.png', 'fg_mark') + '</control>')
    # nothing set
    out += fw.label(X0, LANE0, int(SPAN), LANE_H * DAYS, ADD % 32815, 'st_ui_24_semibold', '8cffffff', 'center', 'String.IsEqual(%s,0)' % prop('count'))
    # the actions
    nav = '<onup>50</onup>'
    on = '!String.IsEmpty(%s)' % prop('focus')
    cells = (fw.cell('9051', 340, '[COLOR fg_mark]+[/COLOR]  $LOCALIZE[19056]', nav, ('SetFocus(50,0,absolute)', 'SendClick(50)'), font='st_cap_16')
             + fw.cell('9052', 340, '$LOCALIZE[21435]', nav, ('SendClick(50)',), font='st_cap_16').replace('<onup>50</onup>', '<onup>50</onup><enable>%s</enable>' % on, 1)
             + fw.cell('9053', 340, '$VAR[FGS_TmToggle]', nav, ('SetFocus(50)', 'Action(ContextMenu)'), font='st_cap_16').replace('<onup>50</onup>', '<onup>50</onup><enable>%s</enable>' % on, 1)
             + fw.cell('9054', 340, '$LOCALIZE[117]', nav, ('RunScript(script.aeon.helper,tmweek,delete)',), font='st_cap_16').replace('<onup>50</onup>', '<onup>50</onup><enable>%s</enable>' % on, 1)
             + fw.cell('9055', 340, '$LOCALIZE[19077]', nav, ('SendClick(8)', 'SetProperty(aeon.tm.refresh,$INFO[System.Time(hh:mm:ss)],home)'), font='st_cap_16'))
    out += (fw.line(120, 889, 1700) + fw.line(120, 960, 1700) + fw.line(120, 890, 1, 70) +
            '<control type="grouplist" id="9050"><left>120</left><top>890</top><width>1700</width><height>70</height><orientation>horizontal</orientation>'
            '<itemgap>0</itemgap><onleft>9055</onleft><onright>9051</onright><onup>50</onup>%s</control>' % cells +
            fw.img(1776, 919, 12, 12, 'fg/circle.png', 'fg_mark', 'String.IsEqual(%s,1)' % prop('hide')) +
            fw.img(1776, 919, 12, 12, 'fg/circle.png', '40ffffff', '!String.IsEqual(%s,1)' % prop('hide')))
    out += '</control></include>'
    out += ('<variable name="FGS_TmToggle"><value condition="String.IsEqual(%s,1)">$LOCALIZE[843]</value><value>$LOCALIZE[844]</value></variable>' % prop('foff'))
    return out


def patch():
    p = os.path.join(fw.D, 'MyPVRTimers.xml')
    s = io.open(p, encoding='utf-8').read()
    # open on the first timer / rule (row 0 is Kodi's Add row); the window is not active yet while onload runs, so no
    # window test, and an alarm so the list has its items first
    line = ('\t<onload condition="$EXP[FGS] + String.IsEmpty(Window(Home).Property(aeon.pvrnav))">'
            'AlarmClock(fgstmfocus,SetFocus(50,1,absolute),00:00,silent)</onload>\n')
    s = '\n'.join(x for x in s.split('\n') if 'SetFocus(50,1,absolute)' not in x)
    s = s.replace('\t<onload>ClearProperty(aeon.pvrnav,home)</onload>', line + '\t<onload>ClearProperty(aeon.pvrnav,home)</onload>', 1)
    assert 'fgstmfocus' in s
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    if 'FGS_TimersWeek' not in s:
        s = s.replace('\t</controls>\n</window>', '\t\t<include condition="$EXP[FGS]">FGS_TimersWeek</include>\n\t</controls>\n</window>', 1)
        assert 'FGS_TimersWeek' in s
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    p = os.path.join(fw.D, 'Includes_Misc.xml')
    s = io.open(p, encoding='utf-8').read()
    a = s.index('<include name="Misc_PVRList">')
    b = s.index('</include>', s.index('<include>Misc_PVRInfoPanel</include>', a))
    seg = s[a:b]
    if 'TVTimers' not in seg:
        seg = seg.replace('<onup>9001</onup>', '<onup condition="%s">103</onup><onup condition="![%s]">9001</onup>' % (MODE, MODE), 1)
        seg = seg.replace('<ondown>50</ondown>', '<ondown condition="%s">9050</ondown><ondown condition="![%s]">50</ondown>' % (MODE, MODE), 1)
        seg = seg.replace('<onright>60</onright>', '<onright condition="%s">9050</onright><onright condition="![%s]">60</onright>' % (MODE, MODE), 1)
        assert seg.count('TVTimers') == 6
        s = s[:a] + seg + s[b:]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def hide_classic():
    """Timers / Timer rules in the Fused Glass style draw on the normal background: today's list (with its card and info
    panel), the next-timer line and the sort row slide out of view; list 50 keeps the focus, radio 8 its clicks"""
    modes = '[$EXP[FGS] + [Window.IsActive(TVTimers) | Window.IsActive(TVTimerRules)]]'
    anim = '<animation effect="slide" end="0,-3000" time="0" condition="%s">Conditional</animation>' % modes
    tab, nl = chr(9), chr(10)
    p = os.path.join(fw.D, 'MyPVRTimers.xml')
    s = io.open(p, encoding='utf-8').read()
    if 'end="0,-3000"' not in s:
        a = s.index(tab * 2 + '<include content="Misc_PVRList">')
        b = s.index(tab * 2 + '<include condition="$EXP[FGS]">FGS_TimersWeek</include>')
        s = s[:a] + tab * 2 + '<control type="group">' + anim + nl + s[a:b] + tab * 2 + '</control>' + nl + s[b:]
        io.open(p, 'w', encoding='utf-8', newline=nl).write(s)
    p = os.path.join(fw.D, 'Includes_Misc.xml')
    s = io.open(p, encoding='utf-8').read()
    i = s.index('<include name="Misc_PVRSubNav">')
    j = s.index('<control type="grouplist" id="9001">', i)
    k = s.index('</animation>', j) + len('</animation>')
    if 'end="0,-3000"' not in s[j:k + 300]:
        s = s[:k] + nl + tab * 4 + anim + s[k:]
        io.open(p, 'w', encoding='utf-8', newline=nl).write(s)


def tabs():
    """Down from the Timers tab: the timers (the sort / filter row sits under the week page)"""
    p = os.path.join(fw.D, 'Includes_Fused.xml')
    s = io.open(p, encoding='utf-8').read()
    i = s.index('<control type="button" id="103">')
    j = s.index('</control>', i)
    seg = s[i:j]
    if 'TVTimers)">9100' not in seg:
        seg = seg.replace('<ondown condition="Control.IsVisible(9001)">9001</ondown>',
                          '<ondown condition="%s">9100</ondown><ondown condition="Control.IsVisible(9001) + ![%s]">9001</ondown>' % (MODE, MODE), 1)
        assert 'TVTimers)">9100' in seg
        s = s[:i] + seg + s[j:]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def main():
    patch()
    tabs()
    hide_classic()
    fw.put('TimersWeek', page())
    print('fgs timers week: page written')


if __name__ == '__main__':
    main()
