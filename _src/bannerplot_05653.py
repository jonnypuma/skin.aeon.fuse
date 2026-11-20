# -*- coding: utf-8 -*-
"""0.56.53 Fused Glass Banner list (FG_V522_View), a season in focus: the airing line and the plot move from the
bottom of the info column (two lines, user 2026-11-19: "how little of the plot you see and there's a huge space on
the right side for it") into the empty right half beside the logo / name / year lines: left 1196, top 604 (under the kicker), to the
card's inner edge (1772) and bottom (1000). Films, shows and sets keep the column plot. Run after seasonplot and
mediagate. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'Includes_Fused.xml')
MARK = '<!-- 0.56.53 season plot on the right -->'
SEASON = 'String.IsEqual(Container(522).ListItem.DBType,season)'


def main():
    s = io.open(P, encoding='utf-8').read()
    if MARK in s:
        print('banner plot: already there')
        return
    a = s.index('<include name="FG_V522_View">')
    b = s.find('<include name=', a + 10)
    seg = s[a:b]
    gl = seg.index('<control type="grouplist"><left>776</left><top>552</top>')
    m = ss.masked(seg)
    e = ss.ctl_end(m, gl)
    col = seg[gl:e]
    old = re.search(r'<control type="textbox"><width>996</width><height>108</height>(?:(?!</control>).)*?\$VAR\[FG_SPlot_522\](?:(?!</control>).)*?</control>', col, re.S).group(0)
    col = col.replace(old, old.replace('</control>', '<visible>!%s</visible></control>' % SEASON, 1), 1)
    right = ('%s<control type="textbox"><left>1196</left><top>604</top><width>576</width><height>396</height>'
             '<font>lb_body_24</font><textcolor>d9ffffff</textcolor><label>$VAR[FG_SPlot_522]</label>'
             '<autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll><visible>%s + $EXP[Aeon_VOPlot]</visible></control>'
             % (MARK, SEASON))
    seg = seg[:gl] + col + right + seg[e:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s[:a] + seg + s[b:])
    print('banner plot: season plot on the right')


if __name__ == '__main__':
    main()
