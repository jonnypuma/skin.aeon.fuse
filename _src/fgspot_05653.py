# -*- coding: utf-8 -*-
"""0.56.53 the Home menu's option dialogs in Fused Glass style (user, 2026-11-19, box: "spotlight submenus not in
fused glass style", "missing horizontal lines"): Spotlight (1163), Planner spotlight (1169), Live TV (1170) and
Widget screen options (1162) had the plain classic page (flat ground, rows at 140, white bar) in every theme.

Each window's controls become includes picked when the window loads:
- Spot<id>_Classic: the controls as they were (every look but Fused Glass style);
- Spot<id>_FGS: the Skin settings design: backdrop, "Aeon Fuse  <dialog>" header and clock pill, one frame 120-1820 /
  108-960 with a title band (the dialog's title and what it does, rule at 191), rows of the settings grid (70 high from
  191) flush with the frame's lines, each with the settings rows' line at its top (hidden on the focused row), the
  style's grey focus bar and its ink, the value right-aligned 24 px inside the right line.
Repeatable (the controls are taken from Spot<id>_Classic once it exists)."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
WINDOWS = {1162: 'Custom_1162_SpotlightOptions.xml', 1163: 'Custom_1163_Spotlight.xml',
           1169: 'Custom_1169_PlannerSpotlight.xml', 1170: 'Custom_1170_LiveTV.xml'}
L, R, T, B, BAND, PITCH = 120, 1820, 108, 960, 191, 70
FRAME = 'FGS_FrameCol'
RR = R - 20                               # 0.56.53 the rows end at the scroll bar gutter (1800-1820)


def rule(x, y, w, h=1):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="$VAR[%s]">common/white.png</texture></control>' % (x, y, w, h, FRAME))


def row_of(top):
    return (top - 220) // 80 if top >= 220 and (top - 220) % 80 == 0 else None


def fgs(body):
    b = body
    b = re.sub(r'<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height>'
               r'<texture colordiffuse="\$VAR\[AG_Ground\]">common/white.png</texture></control>', '', b, count=1)
    title = re.search(r'<control type="label"><left>140</left><top>70</top>.*?<label>(.*?)</label></control>', b, re.S)
    desc = re.search(r'<control type="label"><left>140</left><top>126</top>.*?<label>(.*?)</label></control>', b, re.S)
    b = b.replace(title.group(0), '').replace(desc.group(0), '')
    # the classic separators (1 px under some rows): the rows draw their own
    b = re.sub(r'<control type="image"><left>140</left><top>\d+</top><width>\d+</width><height>1</height>.*?</control>', '', b, flags=re.S)
    for a, c in (('hm_ui_24_bold', 'st_ui_24_bold'), ('hm_ui_24_semibold', 'st_ui_24_semibold'),
                 ('hm_small_20_semibold', 'st_small_20_semibold'), ('hm_small_20', 'st_small_20')):
        b = b.replace('<font>%s</font>' % a, '<font>%s</font>' % c)
    b = b.replace('<include>Aeon_TexRowFocus</include>', '<include>FGS_BtnFocus</include>')
    b = b.replace('$VAR[Aeon_OnBarInk]', '$VAR[FGS_Aeon_OnBarInk]')
    rows = {}                                   # row -> [button ids]

    def geo(m):
        left, top, width, height = (int(m.group(k)) for k in (1, 2, 3, 4))
        r = row_of(top)
        if r is None or height != 64:
            return m.group(0)
        nt = BAND + r * PITCH
        if left == 140:                          # the row's button: frame line to frame line
            left, width = L + 1, RR - L - 1
        elif left == 164:                        # its name, 24 px in
            left = L + 25
        else:                                    # its value, right-aligned 24 px inside the right line
            left = RR - 24 - width
        return '<left>%d</left>%s<top>%d</top>%s<width>%d</width>%s<height>%d</height>' % (
            left, m.group(5), nt, m.group(6), width, m.group(7), PITCH)
    b = re.sub(r'<left>(-?\d+)</left>(?P<s1>\s*)<top>(-?\d+)</top>(?P<s2>\s*)<width>(\d+)</width>(?P<s3>\s*)<height>(\d+)</height>',
               lambda m: geo(_M(m)), b)
    for m in re.finditer(r'<control type="button" id="(\d+)">\s*<left>%d</left>\s*<top>(\d+)</top>' % (L + 1), b):
        rows.setdefault((int(m.group(2)) - BAND) // PITCH, []).append(m.group(1))
    lines = ''.join('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>1</height>'
                    '<texture colordiffuse="12ffffff">common/white.png</texture><visible>!%s</visible></control>'
                    % (L + 1, BAND + r * PITCH, RR - L - 1, '[%s]' % ' | '.join('Control.HasFocus(%s)' % i for i in ids))
                    for r, ids in sorted(rows.items()))
    head = re.sub(r'\[/?UPPERCASE\]', '', title.group(1)).split('  -  ')[0]
    top = ('<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="$VAR[AG_Ground]">common/white.png</texture></control>'
           '<control type="group"><visible>$EXP[Aeon_VGlass]</visible><include>Aeon_Backdrop</include></control>')
    top += rule(L, T, R - L + 1) + rule(L, B, R - L + 1) + rule(L, T, 1, B - T) + rule(RR, T, 1, B - T) + rule(R, T, 1, B - T) + rule(L + 1, BAND, R - L - 1)
    top += ('<include content="Aeon_MenuHeader"><param name="lead" value="Aeon Fuse"/><param name="label" value="%s"/></include>'
            '<include>Aeon_ClockBox</include>' % head)
    top += ('<control type="label"><left>%d</left><top>116</top><width>%d</width><height>40</height><aligny>center</aligny>'
            '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>%s</label></control>'
            '<control type="label"><left>%d</left><top>154</top><width>%d</width><height>30</height><aligny>center</aligny>'
            '<font>st_small_20</font><textcolor>99ffffff</textcolor><label>%s</label></control>'
            % (L + 24, R - L - 48, title.group(1), L + 24, R - L - 48, desc.group(1)))
    return '<!-- 0.56.53 fgspot -->' + top + lines + b


class _M(object):
    """the regex match with the spacing groups numbered 5-7 for geo()"""
    def __init__(self, m):
        self.m = m

    def group(self, k):
        if k == 0:
            return self.m.group(0)
        return {1: self.m.group(1), 2: self.m.group(3), 3: self.m.group(5), 4: self.m.group(7),
                5: self.m.group('s1'), 6: self.m.group('s2'), 7: self.m.group('s3')}[k]


def put(t, name, content):
    if '<include name="%s">' % name in t:
        i = t.index('<include name="%s">' % name)
        j = t.index('<!-- end %s -->' % name, i) + len('<!-- end %s -->' % name)
        return t[:i] + '<include name="%s">%s</include>\n\t<!-- end %s -->' % (name, content, name) + t[j:]
    k = t.rindex('</includes>')
    return t[:k] + '\t<include name="%s">%s</include>\n\t<!-- end %s -->\n' % (name, content, name) + t[k:]


def main():
    inc = os.path.join(D, 'Includes_Fused.xml')
    t = io.open(inc, encoding='utf-8').read()
    for wid, name in sorted(WINDOWS.items()):
        p = os.path.join(D, name)
        s = io.open(p, encoding='utf-8').read()
        a = s.index('<controls>') + len('<controls>')
        e = s.rindex('</controls>')
        cn = 'Spot%d_Classic' % wid
        if '<include name="%s">' % cn in t:
            i = t.index('<include name="%s">' % cn)
            body = t[i + len('<include name="%s">' % cn):t.index('</include>\n\t<!-- end %s -->' % cn, i)]
        else:
            body = s[a:e]
        t = put(t, cn, body)
        t = put(t, 'Spot%d_FGS' % wid, fgs(body))
        s = (s[:a] + '\n\t\t<include condition="$EXP[Aeon_FGlass] + $EXP[FGS]">Spot%d_FGS</include>'
             '\n\t\t<include condition="![$EXP[Aeon_FGlass] + $EXP[FGS]]">%s</include>\n\t' % (wid, cn) + s[e:])
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
        print('window %d: Fused Glass style layout written' % wid)
    io.open(inc, 'w', encoding='utf-8', newline='\n').write(t)


if __name__ == '__main__':
    main()
