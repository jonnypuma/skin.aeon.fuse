# -*- coding: utf-8 -*-
"""0.56.53 the level scroll bars of the sideways library rows are reachable (user, 2026-11-20: "the library views you
added a horizontal scrollbar to, i cannot navigate to those scrollbars"). Down from the row goes to its bar; on the bar
Up goes back to the row, Down on to where the row's Down went before (Flix: the letter strip; 529: the season panels);
the letter strips' Right (it pointed at the old upright bar) goes nowhere. Run after libbars_05653.py. Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Fused.xml')
ROWS = (('528', '5280050', '5280001'), ('529', '5290050', '5290001'), ('5181', '5180051', '5180001'))


def main():
    s = io.open(P, encoding='utf-8').read()
    n = 0
    for cid, bar, strip in ROWS:
        m = re.search(r'<control type="\w+" id="%s">' % cid, s)
        k = s.index('<itemlayout', m.end())
        head = s[m.end():k]
        if '<!-- barnav -->' in head:
            continue
        downs = ''.join(re.findall(r'<ondown[^>]*>[^<]*</ondown>', head))
        head2 = re.sub(r'<ondown[^>]*>[^<]*</ondown>', '', head)
        head2 = '<!-- barnav --><ondown>%s</ondown>' % bar + head2
        s = s[:m.end()] + head2 + s[k:]
        i = s.index('<control type="scrollbar" id="%s">' % bar)
        e = s.index('</control>', i)
        x = s[i:e]
        x = re.sub(r'<onup>[^<]*</onup>', '<onup>%s</onup>' % cid, x, count=1)
        x = re.sub(r'<ondown>[^<]*</ondown>', downs.replace('<ondown>noop</ondown>', '') or '<ondown>noop</ondown>', x, count=1)
        s = s[:i] + x + s[e:]
        j = s.find('<control type="list" id="%s">' % strip)
        if j > 0:
            je = s.index('<itemlayout', j)
            s = s[:j] + s[j:je].replace('<onright>%s</onright>' % bar, '<onright>noop</onright>', 1) + s[je:]
        n += 1
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('level bars reachable: %d rows' % n)



def only_when_scrolling():
    """Down goes to the bar only while the row scrolls (a one-page row hides its bar): otherwise where it went before"""
    s = io.open(P, encoding='utf-8').read()
    for cid, bar, _ in ROWS:
        m = re.search(r'<control type="\w+" id="%s">' % cid, s)
        k = s.index('<itemlayout', m.end())
        head = s[m.end():k]
        if 'barnav2' in head:
            continue
        i = s.index('<control type="scrollbar" id="%s">' % bar)
        e = s.index('</control>', i)
        sc = '[Container(%s).HasNext | Container(%s).HasPrevious]' % (cid, cid)
        alt = ''
        for c, tgt in re.findall(r'<ondown([^>]*)>([^<]*)</ondown>', s[i:e]):
            cc = re.search(r'condition="([^"]*)"', c)
            alt += '<ondown condition="!%s%s">%s</ondown>' % (sc, (' + ' + cc.group(1)) if cc else '', tgt)
        head = head.replace('<!-- barnav --><ondown>%s</ondown>' % bar,
                            '<!-- barnav --><!-- barnav2 --><ondown condition="%s">%s</ondown>%s' % (sc, bar, alt), 1)
        s = s[:m.end()] + head + s[k:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)



def track_glow():
    """with thousands of items the bar's thumb is a few px: while the bar has the focus its whole track lights up in
    the accent (fg_mark at 60 %), so the focus shows"""
    s = io.open(P, encoding='utf-8').read()
    for cid, bar, _ in ROWS:
        i = s.index('<control type="scrollbar" id="%s">' % bar)
        if '<!-- trackglow %s -->' % bar in s[max(0, i - 400):i]:
            continue
        e = s.index('</control>', i)
        g = re.search(r'<left>(-?\d+)</left><top>(-?\d+)</top><width>(\d+)</width><height>(\d+)</height>', s[i:e])
        glow = ('<!-- trackglow %s --><control type="image"><left>%s</left><top>%s</top><width>%s</width><height>%s</height>'
                '<texture border="2" colordiffuse="99e8b04b">fg/r8.png</texture><visible>Control.HasFocus(%s)</visible></control>'
                % (bar, g.group(1), g.group(2), g.group(3), g.group(4), bar))
        s = s[:i] + glow + s[i:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    main()
    only_when_scrolling()
    track_glow()
