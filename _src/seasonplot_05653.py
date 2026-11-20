# -*- coding: utf-8 -*-
"""0.56.53 Fused Glass season views: the season's plot and the show's next airing (user, 2026-11-19: "Season Banner
List is missing Season plot, next episode airing info", also Showcase, Square wall, Compact list, Season list combined
1 / 2 / 3, Low list, Flix). Seasons mostly have no plot of their own, so the plot boxes stayed empty.
Every plot box of a Fused library view list (Container(N).ListItem.Plot, N the view's own list) now reads
$VAR[FG_SPlot_N]:
- a season: first line "S3 E7 airs Wednesday 25 November" in the accent colour (helper 0.3.115 publishes aeon.sn.next for the
  season in focus, aeon.sn.dbid says which), then the season's plot, else the show's plot (Container.ShowPlot);
- anything else: its plot, as before.
Run after the view generators (fg_lib*.py). Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Fused.xml')
MARK = '<!-- 0.56.53 season plot + next airing -->'
VIEWS = (510, 511, 512, 517, 518, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529)


def variables(n):
    c = 'Container(%d).ListItem.' % n
    return ('\t<variable name="FG_SPlot_%d">'
            '<value condition="String.IsEqual(%sDBType,season) + !String.IsEmpty(Window(Home).Property(aeon.sn.next)) + '
            'String.IsEqual(Window(Home).Property(aeon.sn.dbid),%sDBID)">[COLOR fg_mark]$INFO[Window(Home).Property(aeon.sn.next)][/COLOR][CR]$VAR[FG_SPlotB_%d]</value>'
            '<value>$VAR[FG_SPlotB_%d]</value></variable>\n'
            '\t<variable name="FG_SPlotB_%d">'
            '<value condition="String.IsEqual(%sDBType,season) + String.IsEmpty(%sPlot)">$INFO[Container.ShowPlot]</value>'
            '<value>$INFO[%sPlot]</value></variable>\n' % (n, c, c, n, n, n, c, c, c))


def main():
    s = io.open(P, encoding='utf-8').read()
    if MARK in s:
        print('season plot: already there')
        return
    total = 0
    out = []
    for n in VIEWS:
        head = '<include name="FG_V%d_View">' % n
        if head not in s:
            continue
        a = s.index(head)
        b = s.find('<include name=', a + 10)
        b = len(s) if b < 0 else b
        seg, k = re.subn(r'(<control type="textbox">(?:(?!</control>).)*?<label>)\$INFO\[Container\(%d\)\.ListItem\.Plot\](</label>)' % n,
                         r'\g<1>$VAR[FG_SPlot_%d]\g<2>' % n, s[a:b], flags=re.S)
        if k:
            s = s[:a] + seg + s[b:]
            out.append('%d:%d' % (n, k))
            total += k
            i = s.rindex('</includes>')
            s = s[:i] + variables(n) + s[i:]
    i = s.rindex('</includes>')
    s = s[:i] + '\t' + MARK + '\n' + s[i:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('season plot: %d boxes (%s)' % (total, ' '.join(out)))


if __name__ == '__main__':
    main()
