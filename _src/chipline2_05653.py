# -*- coding: utf-8 -*-
"""0.56.53 the sidecar chips (sidechips_05653.py) on a second line (user, 2026-11-19: "Yes, second line"; one line ran
out of room with many chips on). For each chip row that has them:
- the row is in a vertical grouplist: the sidecar chips become a horizontal grouplist of their own right after the
  row (same width / height / gap / alignment), so what follows moves down;
- the row has a fixed top: they go to the end of the line next to it (a grouplist of the same parent whose top is
  30-60 px away: the ratings line in the spotlights, widgets and cards);
- otherwise a new line of their own 44 px below the row (the Aeon views' fourth chip line, the big Home spotlight).
The marker comment stays after the chip row (sidechips_05653.py sees the row as done). Video codec, container and bitrate stay on the first line, beside the resolution (user). RUN AFTER sidechips_05653.py.
Repeatable (moved chips carry MOVED)."""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402

D = os.path.join(HERE, '..', '1080i')
MARK = '<!-- 0.56.53 sidecar chips -->'
MOVED = '<!-- 0.56.53 sidecar chips, line 2 -->'
FIRST = ('vcodec', 'container', 'bitrate')
BTN = re.compile(r'\s*<control type="button">(?:(?!<control).)*?</control>', re.S)


def clones_after(s, i):
    """(start, end) of the sidecar chip buttons right after the marker at i"""
    j = i + len(MARK)
    e = j
    while True:
        m = BTN.match(s, e)
        if not m or 'aeon.mi.path' not in m.group(0):
            return j, e
        e = m.end()


def tag(seg, name):
    m = re.search(r'<%s>([^<]*)</%s>' % (name, name), seg)
    return m.group(1) if m else None


def head(s, m, start):
    """the text of a control from its opening tag to its first child control"""
    gt = s.index('>', start) + 1
    nxt = re.compile(r'<control[ >]').search(m, gt)
    return s[start:nxt.start() if nxt else gt]


def one(s):
    m = ss.masked(s)
    for x in re.finditer(re.escape(MARK), s):
        i = x.start()
        a, b = clones_after(s, i)
        if a == b:
            continue
        # container and bitrate stay on the first line, beside the resolution (user, 2026-11-19)
        parts = [y.group(0) for y in BTN.finditer(s, a, b)]
        kept = ''.join(x for x in parts if any('aeon.chip.%s)' % k in x for k in FIRST))
        moved = ''.join(x for x in parts if not any('aeon.chip.%s)' % k in x for k in FIRST))
        if not moved:
            continue
        stack = []
        for y in re.finditer(r'<control[ >][^>]*>|</control>', m[:i]):
            if y.group(0).startswith('</'):
                stack.pop()
            else:
                stack.append(y.start())
        row = stack[-1]
        par = stack[-2] if len(stack) > 1 else None
        chips = moved
        rhead = head(s, m, row)
        if par is not None and 'grouplist' in s[par:par + 40] and tag(head(s, m, par), 'orientation') == 'vertical':
            rend = ss.ctl_end(m, row)
            h = re.sub(r'\s*<top>[^<]*</top>', '', rhead)
            h = re.sub(r'\s*<left>[^<]*</left>', '', h)
            h = re.sub(r'\s*<visible>.*?</visible>', '', h, flags=re.S)
            h = re.sub(r'\s*<description>.*?</description>', '', h, flags=re.S)
            line = MOVED + h.rstrip() + chips + '</control>'
            s = s[:a] + kept + s[b:rend] + line + s[rend:]
            return s, 'vertical'
        top = tag(rhead, 'top')
        best = None
        if par is None:          # the row is a top-level control of an include: its siblings are the include's
            inc = s.rfind('<include name="', 0, i)
            nxt = s.find('<include name="', i)
            nxt = len(s) if nxt < 0 else nxt
            kids, k = [], s.index('>', inc) + 1
            while True:
                y = re.compile(r'<control[ >]').search(m, k, nxt)
                if not y:
                    break
                e = ss.ctl_end(m, y.start())
                kids.append((y.start(), e))
                k = e
        else:
            kids = ss.children(m, par, ss.ctl_end(m, par))
        for c0, c1 in kids:
            if c0 == row or not s.startswith('<control type="grouplist"', c0):
                continue
            t = tag(head(s, m, c0), 'top')
            if top and t and top.lstrip('-').isdigit() and t.lstrip('-').isdigit() and 30 <= abs(int(t) - int(top)) <= 60 and (best is None or abs(int(t) - int(top)) < best[0]):
                best = (abs(int(t) - int(top)), c0, c1)
        if not best:             # no line next to it: a new line 44 px below the row (same place, slid down)
            rend = ss.ctl_end(m, row)
            h = re.sub(r'\s*<visible>.*?</visible>', '', rhead, flags=re.S)
            h = re.sub(r'\s*<description>.*?</description>', '', h, flags=re.S)
            line = (MOVED + h.rstrip() + '<animation effect="slide" start="0,0" end="0,44" time="0" condition="true">'
                    'Conditional</animation>' + chips + '</control>')
            s = s[:a] + kept + s[b:rend] + line + s[rend:]
            return s, 'below'
        _d, c0, c1 = best
        close = s.rindex('</control>', c0, c1)
        # a line that shows only on a condition (ratings on): a twin line in its place for when it is hidden
        shead = head(s, m, c0)
        sv = re.search(r'<visible>(.*?)</visible>', shead, re.S)
        twin = ''
        if sv:
            th = shead.replace(sv.group(0), '<visible>![%s]</visible>' % sv.group(1), 1)
            twin = MOVED + th.rstrip() + chips + '</control>'
        if c0 > i:
            close -= (b - a - len(kept))
            c1 -= (b - a - len(kept))
        s = s[:a] + kept + s[b:]
        s = s[:close] + MOVED + chips + s[close:c1] + twin + s[c1:]
        return s, 'next line'
    return s, None


PLOT = ('<control type="textbox"><left>120</left><top>348</top><width>760</width><height>72</height>')
PLOT_SHIFT = ('<animation effect="slide" start="0,0" end="0,44" time="0" condition="Skin.HasSetting(aeon.mi.sidecar) + '
              'String.IsEqual(Window(Home).Property(aeon.mi.path),Container(9441).ListItem.FileNameAndPath)">Conditional'
              '</animation><!-- 0.56.53 under the sidecar chip line -->')


def shift_plot():
    """the big Home spotlight (9441): its plot goes 44 px down while the sidecar chip line under the chips can show"""
    p = os.path.join(D, 'Includes_Aeon_Home.xml')
    s = io.open(p, encoding='utf-8').read()
    if PLOT_SHIFT in s or s.count(PLOT) != 1:
        return
    i = s.index(PLOT) + len(PLOT)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s[:i] + PLOT_SHIFT + s[i:])
    print('big spotlight plot: shifted under the sidecar line')


COND510 = ('Skin.HasSetting(aeon.mi.sidecar) + '
           'String.IsEqual(Window(Home).Property(aeon.mi.path),Container(510).ListItem.FileNameAndPath)')


def card510():
    """the Fused Glass List view card (510): its chips sit on the card's bottom edge, so the sidecar line goes 44 px
    above them, and the plot is 44 px shorter while that line can show (a twin of each plot box)"""
    p = os.path.join(D, 'Includes_Fused.xml')
    s = io.open(p, encoding='utf-8').read()
    if '0.56.53 card 510' in s:
        return
    a = s.index('<include name="FG_V510_View">') if '<include name="FG_V510_View">' in s else 0
    b = s.find('<include name=', a + 10)
    b = len(s) if b < 0 else b
    seg = s[a:b]
    old = '<animation effect="slide" start="0,0" end="0,44" time="0" condition="true">Conditional</animation>'
    i = seg.find(old)
    while i >= 0 and 'Container(510).ListItem.FileNameAndPath' not in seg[i:i + 3000]:
        i = seg.find(old, i + 1)
    if i < 0:
        print('card 510: sidecar line not found')
        return
    seg = seg[:i] + old.replace('0,44', '0,-44') + seg[i + len(old):]
    n = 0

    def twin(m):
        nonlocal n
        x = m.group(0)
        h = int(re.search(r'<height>(\d+)</height>', x).group(1))
        short = re.sub(r'<height>\d+</height>', '<height>%d</height>' % (h - 44), x, count=1)
        n += 1
        return (x.replace('</control>', '<visible>![%s]</visible></control>' % COND510, 1)
                + '<!-- 0.56.53 card 510: shorter while the sidecar line shows -->'
                + short.replace('</control>', '<visible>%s</visible></control>' % COND510, 1))
    seg = re.sub(r'<control type="textbox"><left>747</left><top>(?:858|826)</top>(?:(?!<control).)*?'
                 r'Container\(510\)\.ListItem\.Plot(?:(?!<control).)*?</control>', twin, seg, flags=re.S)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s[:a] + seg + s[b:])
    print('card 510: line above the chips, %d plot boxes shortened' % n)


def main():
    shift_plot()
    for p in sorted(glob.glob(os.path.join(D, '*.xml'))):
        s = io.open(p, encoding='utf-8').read()
        if MARK not in s:
            continue
        counts = {}
        for _ in range(200):
            s, how = one(s)
            if not how:
                break
            counts[how] = counts.get(how, 0) + 1
        if counts:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
            print('%-28s %s' % (os.path.basename(p), counts))
    card510()
    widen_strips()


STRIPS = ('FG_V520_View', 'FG_V521_View', 'FG_V523_View', 'FG_V525_View', 'FG_V526_View')


def widen_strips():
    """the five Fused Glass views with the info strip along the bottom (Poster wall, Landscape wall, Showcase, Square
    wall, Cards): their chip lines were 560 px (the left column); under the plot and the studio logo the strip is free
    to its right edge, so every line of that column but the top one (the ratings, beside the clear logo) gets 1656 px"""
    p = os.path.join(D, 'Includes_Fused.xml')
    s = io.open(p, encoding='utf-8').read()
    n = 0
    for name in STRIPS:
        a = s.index('<include name="%s">' % name)
        b = s.find('<include name=', a + 10)
        b = len(s) if b < 0 else b
        seg = s[a:b]
        pat = re.compile(r'<control type="grouplist"><left>120</left><top>(\d+)</top><width>560</width>')
        tops = sorted(set(int(x) for x in pat.findall(seg)))
        if len(tops) < 2:
            continue
        keep = tops[0]

        def wide(m):
            nonlocal n
            if int(m.group(1)) == keep:
                return m.group(0)
            n += 1
            return m.group(0).replace('<width>560</width>', '<width>1656</width>')
        seg = pat.sub(wide, seg)
        s = s[:a] + seg + s[b:]
    if n:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
        print('strip views: %d chip lines widened to 1656 px' % n)


if __name__ == '__main__':
    main()
