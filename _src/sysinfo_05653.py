# -*- coding: utf-8 -*-
"""0.56.53 System information in Fused Glass style, to the Skin settings page spec (user, 2026-11-20: "kodi system
info menu has loads of issues"; box shot: the sections' focus was the rounded white pill of the other looks, 68 high,
the CPU line ran past the frame):
- the sections (95, 94, 96-101) are rows of the settings grid: 121-480 (inside the line), 70 high from 191, the style's
  bar with the dark fill (FGS_CatTex), capitals as the Categories column of Skin settings;
- the open section, while the focus is on the right, is marked as Skin settings' open category: the style's dimmed bar
  (fgs_bar at 40) at its 70 row, its name in the parent ink (the other looks keep their markers);
- the meters' labels end inside the right column (276 wide, as the bars under them).
The facts (labels 2-13, not focusable) keep their 50 px lines. Repeatable."""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '1080i')
P = os.path.join(D, 'SettingsSystemInfo.xml')
FUSED = os.path.join(D, 'Includes_Fused.xml')
SECTIONS = (('95', '20037'), ('94', '13277'), ('96', '13279'), ('97', '13280'), ('98', '13281'), ('99', '19191'), ('100', '12389'), ('101', '12396'))
LOOK = ('\t<!-- 0.56.53 System information sections in Fused Glass style: rows of the settings grid -->\n'
        '\t<include name="FGS_SysCatLook"><width>359</width><height>70</height><font>uc_st_ui_24_bold</font>'
        '<textcolor>$VAR[FGS_CatText]</textcolor><focusedcolor>$VAR[FGS_Aeon_CatFocInk]</focusedcolor>'
        '<disabledcolor>44ffffff</disabledcolor><textoffsetx>24</textoffsetx><aligny>center</aligny><include>FGS_CatTex</include></include>'
        '<include name="FGS_W276"><width>276</width></include><include name="FGS_W328_Else"><width>328</width></include>\n')


def main():
    s = io.open(P, encoding='utf-8').read()
    if '<!-- 0.56.53 sysinfo -->' not in s:
        s = s.replace('<include content="Misc_RowLook" condition="$EXP[FGS]"><param name="width" value="361"/></include>',
                      '<include condition="$EXP[FGS]">FGS_SysCatLook</include>')
        i = s.index('<control type="grouplist" id="9000">')
        e = s.index('<control type="button"', i)
        s = s[:i] + s[i:e].replace('<animation effect="slide" start="0,0" end="0,23" time="0" condition="$EXP[FGS]">',
                                   '<animation effect="slide" start="0,0" end="1,23" time="0" condition="$EXP[FGS]">', 1) + s[e:]
        # the old open-section markers: not in the style
        s = re.sub(r'(<visible>!ControlGroup\(9000\)\.HasFocus \+ String\.IsEqual\(Window\.Property\(aeon\.sysinfo\),\d+\))(</visible>)',
                   r'\1 + !$EXP[FGS]\2', s)
        marks = []
        for k, (sid, lab) in enumerate(SECTIONS):
            marks.append('<control type="group"><left>121</left><top>%d</top>'
                         '<visible>$EXP[FGS] + !ControlGroup(9000).HasFocus + String.IsEqual(Window.Property(aeon.sysinfo),%s)</visible>'
                         '<control type="image"><left>0</left><top>0</top><width>359</width><height>70</height>'
                         '<texture border="20" colordiffuse="40ffffff">fg/fgs_bar.png</texture></control>'
                         '<control type="label"><left>24</left><top>0</top><width>320</width><height>70</height><aligny>center</aligny>'
                         '<font>uc_st_ui_24_bold</font><textcolor>$VAR[FGS_Aeon_ParentInk]</textcolor><label>$LOCALIZE[%s]</label></control>'
                         '</control>' % (191 + 70 * k, sid, lab))
        anchor = '<!-- the open section keeps a grey bar while the highlight is on the page to its right -->'
        s = s.replace(anchor, anchor + '\n\t\t<!-- 0.56.53 sysinfo --><!-- the style: the dimmed bar on the 70 grid -->' + ''.join(marks), 1)
        # the meters' labels inside the column
        for lab in ('$LOCALIZE[31809]  $INFO[System.Memory(used.percent)]', 'CPU  $INFO[System.CPUUsage]'):
            j = s.index('<label>%s</label>' % lab)
            k = s.rfind('<width>328</width>', 0, j)
            s = s[:k] + '<include condition="$EXP[FGS]">FGS_W276</include><include condition="!$EXP[FGS]">FGS_W328_Else</include>' + s[k + len('<width>328</width>'):]
        io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
        print('system info: sections, markers, meters')
    t = io.open(FUSED, encoding='utf-8').read()
    if '<include name="FGS_SysCatLook">' not in t:
        k = t.index('\t<include name="FGS_RowTex">')
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t[:k] + LOOK + t[k:])


if __name__ == '__main__':
    main()
