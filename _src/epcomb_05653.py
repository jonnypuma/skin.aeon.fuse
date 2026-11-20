# -*- coding: utf-8 -*-
"""0.56.53 Episode combined (Aeon_V538_View, Includes_Fused.xml), the right panel (user, 2026-11-19: "the chapters and
subtitles chips are slightly clipped on the bottom. the other mediainfo chips cut off, there is space for two rows
under the plot"). chipline2 had put the sidecar chips on the status line (32 high, the chips 36) and the media chips
line (top 520) ran out at the panel's edge. Now:
- the status line keeps the version / ring / Unwatched only (its sidecar chips and their twin line go);
- the plot moves up into the old chips line's place (top 520) and is 112 high (three lines) instead of 156;
- the media chips line goes under the plot (top 640), the sidecar chips get a line of their own under it (682).
Run after chipline2_05653.py and edition_05653.py. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'Includes_Fused.xml')
MARK = '<!-- 0.56.53 episode combined: chips under the plot -->'
MOVED = '<!-- 0.56.53 sidecar chips, line 2 -->'
BTN = re.compile(r'\s*<control type="button">(?:(?!<control).)*?</control>', re.S)


def main():
    s = io.open(P, encoding='utf-8').read()
    if MARK in s:
        print('episode combined: already there')
        return
    a = s.index('<include name="Aeon_V538_View">')
    b = s.find('<include name=', a + 10)
    b = len(s) if b < 0 else b
    seg = s[a:b]
    m = ss.masked(seg)
    chips = None
    # the status lines at 478: the first holds the moved chips, the second is the twin line made of them only
    lines = [x.start() for x in re.finditer(r'<control type="grouplist"><left>0</left><top>478</top>', seg)]
    for start in reversed(lines):
        end = ss.ctl_end(m, start)
        x = seg[start:end]
        if MOVED not in x:
            continue
        i = x.index(MOVED)
        j = i + len(MOVED)
        k = j
        while True:
            mm = BTN.match(x, k)
            if not mm or 'aeon.mi.path' not in mm.group(0):
                break
            k = mm.end()
        part = x[j:k]
        rest = (x[:i] + x[k:]).strip()
        only_chips = re.sub(r'<control type="grouplist">.*?<usecontrolcoords>true</usecontrolcoords>(?:<visible>.*?</visible>)*',
                            '', rest, count=1, flags=re.S).replace('</control>', '', 1).strip() == ''
        if only_chips:
            seg = seg[:start] + seg[end:]                 # the twin line: gone
        else:
            chips = part
            seg = seg[:start] + x[:i] + x[k:] + seg[end:]
        m = ss.masked(seg)
    # whatever moved chips are left on a status line go too (the loop above can miss the first line)
    while MOVED in seg:
        i = seg.index(MOVED)
        k = i + len(MOVED)
        while True:
            mm = BTN.match(seg, k)
            if not mm or 'aeon.mi.path' not in mm.group(0):
                break
            k = mm.end()
        if chips is None:
            chips = seg[i + len(MOVED):k]
        seg = seg[:i] + seg[k:]
    seg, n1 = re.subn(r'(<control type="textbox"><left>0</left><top>572</top><width>580</width><height>)156(</height>)',
                      r'\g<1>112\g<2>', seg)
    seg = seg.replace('<control type="textbox"><left>0</left><top>572</top><width>580</width><height>112</height>',
                      '<control type="textbox"><left>0</left><top>520</top><width>580</width><height>112</height>')
    seg, n2 = re.subn(r'(<control type="grouplist">\s*<left>0</left><top>)520(</top><width>580</width><height>36</height>)',
                      r'\g<1>640\g<2>', seg)
    if chips:
        line = ('%s<control type="grouplist"><left>0</left><top>682</top><width>580</width><height>36</height>'
                '<orientation>horizontal</orientation><itemgap>8</itemgap><usecontrolcoords>true</usecontrolcoords>%s</control>'
                % (MARK, chips))
        j = seg.index('<top>640</top>')
        st = seg.rfind('<control type="grouplist">', 0, j)
        e = ss.ctl_end(ss.masked(seg), st)
        seg = seg[:e] + line + seg[e:]
    else:
        seg = seg.replace('<top>640</top>', '<top>640</top>' + MARK, 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s[:a] + seg + s[b:])
    print('episode combined: plot boxes %d, chips line %d moved, sidecar line %s' % (n1, n2, 'added' if chips else 'none'))


if __name__ == '__main__':
    main()


# ---- 0.56.53 round 2 (user: "after HDR chip to show format, container on a new line ... move the chapter and
# subtitle chips to after S3 E4 at the top under the episode thumb")
MARK2 = '<!-- 0.56.53 episode combined round 2 -->'
SECOND = ('vcodec', 'container', 'bitrate')
TOP = ('subs', 'chapters')


def _line(seg, m, top):
    x = re.search(r'<control type="grouplist">\s*<left>0</left><top>%d</top>' % top, seg)
    return x.start(), ss.ctl_end(m, x.start())


def round2():
    s = io.open(P, encoding='utf-8').read()
    if MARK2 in s:
        print('episode combined round 2: already there')
        return
    a = s.index('<include name="Aeon_V538_View">')
    b = s.find('<include name=', a + 10)
    b = len(s) if b < 0 else b
    seg = s[a:b]
    m = ss.masked(seg)
    l1 = _line(seg, m, 640)
    l2 = _line(seg, m, 682)
    kids1 = ss.children(m, *l1)
    kids2 = ss.children(m, *l2)
    key = lambda x: (re.search(r'Skin\.HasSetting\(aeon\.chip\.(\w+)\)\]', x) or [None, None])[1]
    move1 = [(c0, c1) for c0, c1 in kids1 if key(seg[c0:c1]) in SECOND]
    to_top = [(c0, c1) for c0, c1 in kids2 if key(seg[c0:c1]) in TOP]
    second = ''.join(seg[c0:c1] for c0, c1 in move1)
    top = ''.join(seg[c0:c1] for c0, c1 in to_top)
    top = top.replace('<height>36</height>', '<height>30</height>').replace('<font>lb_small_20_bold</font>', '<font>lb_cap_16</font>')
    # rebuild back to front so the offsets stay right: line 2 (drop the top chips, codec / container / bitrate first)
    for c0, c1 in reversed(to_top):
        seg = seg[:c0] + seg[c1:]
    first_child = ss.children(ss.masked(seg), *_line(seg, ss.masked(seg), 682))
    ins = first_child[0][0] if first_child else _line(seg, ss.masked(seg), 682)[1] - len('</control>')
    seg = seg[:ins] + MARK2 + second + seg[ins:]
    m = ss.masked(seg)
    l1 = _line(seg, m, 640)
    for c0, c1 in reversed([(c0, c1) for c0, c1 in ss.children(m, *l1) if key(seg[c0:c1]) in SECOND]):
        seg = seg[:c0] + seg[c1:]
    # the S3 E1 line: the kicker, sized to its text, then the subtitles and chapters chips
    k = re.search(r'<control type="label"><left>0</left><top>344</top><width>580</width><height>30</height>(.*?)</control>', seg, re.S)
    kicker = '<control type="label"><width min="10" max="420">auto</width><height>30</height>%s</control>' % k.group(1)
    line = ('<control type="grouplist"><left>0</left><top>344</top><width>580</width><height>30</height>'
            '<orientation>horizontal</orientation><itemgap>12</itemgap><usecontrolcoords>true</usecontrolcoords>%s%s</control>'
            % (kicker, top))
    seg = seg[:k.start()] + line + seg[k.end():]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s[:a] + seg + s[b:])
    print('episode combined round 2: %d chips to line 2, %d chips to the S3 E1 line' % (len(move1), len(to_top)))


if __name__ == '__main__':
    round2()
