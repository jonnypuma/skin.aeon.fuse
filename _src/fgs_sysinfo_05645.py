# -*- coding: utf-8 -*-
"""0.56.45 Fused Glass style: System info (SettingsSystemInfo.xml) in the settings grid (the user, 2026-11-18: "versions
manager modal and system information window has not been created in Fused Glass style yet").

As Skin settings in the style: no cards; one ruled frame 120-1820 x 108-960 with a title row (rule at 191) and two
dividers (481, 1500): Categories | the open section (its name) | Hardware. The section rows fill the first column (361
wide, from 191); the facts (labels 2-13, 971 wide from 505) each sit over a faint rule while they have text; the
privacy policy (30) and the contribute page (102) take the same place; the build lines close the middle column; memory
and CPU fill the right column. Kodi's ids stay single (one control per id): the style moves and sizes them
(Conditional slides, load-time width includes), the frame, titles and rules are the style's own. Other looks unchanged.
Run from the skin folder. Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'SettingsSystemInfo.xml')
MARK = '<!-- 0.56.45 fgs_sysinfo -->'
FGS = '$EXP[FGS]'
SECTIONS = [(95, 20037), (94, 13277), (96, 13279), (97, 13280), (98, 13281), (99, 19191), (100, 12389), (101, 12396)]


def slide(x, y):
    return '<animation effect="slide" start="0,0" end="%d,%d" time="0" condition="%s">Conditional</animation>' % (x, y, FGS)


def width(normal, fgs):
    return ('<include content="Param_W" condition="%s"><param name="w" value="%d"/></include>'
            '<include content="Param_W" condition="!%s"><param name="w" value="%d"/></include>' % (FGS, fgs, FGS, normal))


def line(x, y, w, h, col='$VAR[FGS_FrameCol]', vis=FGS):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="%s">common/white.png</texture><visible>%s</visible></control>' % (x, y, w, h, col, vis))


def frame():
    title = ('<control type="label"><left>%d</left><top>108</top><width>%d</width><height>83</height><aligny>center</aligny>'
             '<font>st_ui_30_semibold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label><visible>%s</visible></control>')
    o = ['\t\t' + MARK,
         '\t\t' + line(120, 108, 1700, 1), '\t\t' + line(120, 960, 1700, 1), '\t\t' + line(120, 108, 1, 853),
         '\t\t' + line(1820, 108, 1, 853), '\t\t' + line(481, 108, 1, 853), '\t\t' + line(1500, 108, 1, 853),
         '\t\t' + line(120, 191, 1700, 1),
         '\t\t' + title % (144, 320, '$LOCALIZE[31847]', FGS),
         '\t\t' + title % (505, 970, '$VAR[Aeon_SysInfoSection]', FGS),
         '\t\t' + title % (1524, 280, '$LOCALIZE[13281]', FGS)]
    # a faint rule under each fact that has text (not on the privacy policy / contribute pages)
    for k in range(12):
        o.append('\t\t' + line(481, 241 + 50 * k, 1019, 1, '12ffffff',
                               '%s + !String.IsEmpty(Control.GetLabel(%d)) + !Control.IsVisible(30) + !Control.IsVisible(102)' % (FGS, k + 2)))
    return '\n'.join(o) + '\n'


def section_var():
    o = ['\t<variable name="Aeon_SysInfoSection">']
    for cid, sid in SECTIONS:
        o.append('\t\t<value condition="String.IsEqual(Window(10007).Property(aeon.sysinfo),%d)">$LOCALIZE[%d]</value>' % (cid, sid))
    o.append('\t\t<value>$LOCALIZE[%d]</value>' % SECTIONS[0][1])
    return '\n'.join(o + ['\t</variable>'])


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('fgs_sysinfo: already done')
        return
    # cards: not in the style
    for old in ('<visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible></control>',):
        assert old in t
    t = t.replace('<visible>!$EXP[Aeon_VGlass] | $EXP[Aeon_FGlass]</visible>', '<visible>[!$EXP[Aeon_VGlass] | $EXP[Aeon_FGlass]] + !$EXP[FGS]</visible>')
    # the frame, titles and fact rules: before the sections
    anchor = '\t\t<!-- ====== sections -->'
    t = t.replace(anchor, frame() + anchor, 1)
    # sections: from the title row, the first column's width
    s = t.index('<control type="grouplist" id="9000">')
    e = t.index('</control>\n\t\t<!-- the open section', s) if '<!-- the open section' in t else t.index('<!-- ====== section content')
    blk = t[s:e]
    blk = blk.replace('<width>420</width>', width(420, 361), 1)
    blk = blk.replace('<orientation>vertical</orientation>', '<orientation>vertical</orientation>\n\t\t\t' + slide(0, 23), 1)
    blk = blk.replace('<include content="Misc_RowLook"><param name="width" value="420"/></include>',
                      '<include content="Misc_RowLook" condition="!%s"><param name="width" value="420"/></include>'
                      '<include content="Misc_RowLook" condition="%s"><param name="width" value="361"/></include>' % (FGS, FGS))
    t = t[:s] + blk + t[e:]
    # the open section's bar: down with the rows, the first column's width
    t = re.sub(r'(<left>page_margin</left><top>\d+</top>)(\n\t\t\t<visible>!ControlGroup\(9000\).HasFocus)', r'\1' + slide(0, 23) + r'\2', t)
    t = re.sub(r'(<control type="image"><left>0</left><top>0</top><width>420</width><height>68</height><texture[^>]*>[^<]*</texture>)',
               r'\1<animation effect="zoom" start="100,100" end="85.95,100" center="0,0" time="0" condition="%s">Conditional</animation>' % FGS, t)
    # the facts, the privacy policy, the contribute page: to the middle column, 971 wide
    s = t.index('<!-- ====== section content -->')
    e = t.index('<!-- ====== footer')
    blk = t[s:e]
    blk = blk.replace('<left>580</left>\n\t\t\t<top>200</top>\n\t\t\t<width>800</width>\n\t\t\t<height>600</height>\n\t\t\t<orientation>vertical</orientation>',
                      '<left>580</left>\n\t\t\t<top>200</top>\n\t\t\t' + width(800, 971) + '\n\t\t\t<height>600</height>\n\t\t\t<orientation>vertical</orientation>\n\t\t\t' + slide(-75, -9), 1)
    blk = re.sub(r'<control type="label" id="(\d+)"><width>800</width>', lambda m: '<control type="label" id="%s">%s' % (m.group(1), width(800, 971)), blk)
    blk = blk.replace('<description>Privacy policy</description>', '<description>Privacy policy</description>\n\t\t\t' + slide(-75, -9), 1)
    blk = blk.replace('<description>Contribute page (Kodi toggles it)</description>', '<description>Contribute page (Kodi toggles it)</description>\n\t\t\t' + slide(-75, -9), 1)
    blk = blk.replace('<param name="left" value="1366"/>', '<param name="left" value="1366"/>\n\t\t\t<param name="visible" value="Control.IsVisible(30)"/>', 1) if False else blk
    t = t[:s] + blk + t[e:]
    # footer: the rule goes (the frame has one), the build lines close the middle column, memory / CPU to the right
    rule = re.search(r'\t\t<include content="AG_Rule">\n\t\t\t<param name="left" value="580"/>\n\t\t\t<param name="top" value="840"/>.*?</include>\n', t, re.S)
    assert rule, 'footer rule'
    t = t[:rule.start()] + ('\t\t<control type="group"><visible>!%s</visible>\n' % FGS) + rule.group(0) + '\t\t</control>\n' + \
        '\t\t' + line(481, 852, 1019, 1, '$VAR[FGS_FrameCol]') + '\n' + t[rule.end():]
    t = t.replace('<control type="group">\n\t\t\t<left>1416</left>\n\t\t\t<top>208</top>',
                  '<control type="group">\n\t\t\t<left>1416</left>\n\t\t\t<top>208</top>\n\t\t\t' + slide(108, 7), 1)
    t = re.sub(r'(<control type="progress">\n\t\t\t\t<left>0</left>\n\t\t\t\t<top>\d+</top>\n\t\t\t\t<width>328</width>)',
               r'\1\n\t\t\t\t<animation effect="zoom" start="100,100" end="84.15,100" center="0,0" time="0" condition="%s">Conditional</animation>' % FGS, t)
    t = t.replace('<control type="grouplist">\n\t\t\t<left>580</left>\n\t\t\t<top>856</top>',
                  '<control type="grouplist">\n\t\t\t<left>580</left>\n\t\t\t<top>856</top>\n\t\t\t' + slide(-75, -8), 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    # the section name for the middle title (variables live in include files)
    sub = os.path.join(os.path.dirname(P), 'Includes_Aeon_Sub.xml')
    x = io.open(sub, encoding='utf-8').read()
    if 'name="Aeon_SysInfoSection"' not in x:
        i = x.index('\t<variable name="Aeon_VOS_ratings">')
        x = x[:i] + '\t<!-- 0.56.45 fgs_sysinfo: the open section of System info -->\n' + section_var() + '\n' + x[i:]
        io.open(sub, 'w', encoding='utf-8', newline='\n').write(x)
    print('fgs_sysinfo: System info in the settings grid')


if __name__ == '__main__':
    main()
