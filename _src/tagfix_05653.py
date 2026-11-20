# -*- coding: utf-8 -*-
"""0.56.53 the version tag on list rows (tagrows_05653.py), fixed (box, 2026-11-19, site shots): the title + tag pair is
a grouplist, and in a list row Kodi does not hand a grouplist's children the row's item: they read the focused item.
Every row of a film with versions showed the FOCUSED film's title and version ("DONNIE DARKO THEATRICAL CUT" on all).
- the focused row (Aeon $PARAM[focused] rows, Fused <focusedlayout>): the outline tag stays (focused item = its item);
- the other rows: no grouplist; the title label shows again for every row and carries the version inline, dimmed
  ("DONNIE DARKO   THEATRICAL CUT"), from $VAR[Aeon_VerInline] which reads the row's own item.
Run after tagrows_05653.py. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402
import tagrows_05653 as tr  # noqa: E402

D = os.path.join(HERE, '..', '1080i')
MARK = tr.MARK
NEG = '<visible>![%s]</visible>' % tr.TAG
INLINE = '$VAR[Aeon_VerInline]'
VAR = ('\t<variable name="Aeon_VerInline"><value condition="%s">[COLOR 8cffffff]   [UPPERCASE]$VAR[Aeon_VerStat][/UPPERCASE][/COLOR]</value></variable>\n'
       % tr.TAG)


def unwrap(seg, start):
    """the grouplist at start: removed; the label just before it: shown for every row, with the inline version"""
    m = ss.masked(seg)
    g = start + len(MARK)
    e = ss.ctl_end(m, g)
    lab_end = start
    lab_start = seg.rfind('<control type="label">', 0, start)
    lab = seg[lab_start:lab_end]
    assert NEG in lab, lab[:200]
    lab = lab.replace(NEG, '', 1)
    lab = re.sub(r'<label>(.*?)</label>', lambda x: '<label>%s%s</label>' % (x.group(1), INLINE) if INLINE not in x.group(1) else x.group(0), lab, 1, flags=re.S)
    return seg[:lab_start] + lab + seg[e:]


def aeon():
    p = os.path.join(D, 'Includes_Aeon_Video.xml')
    s = io.open(p, encoding='utf-8').read()
    n = 0
    while True:
        found = None
        for x in re.finditer(re.escape(MARK) + r'<control type="grouplist">(.*?)<control type="button">', s, re.S):
            if '!$PARAM[focused]' in x.group(1):
                found = x.start()
                break
        if found is None:
            break
        s = unwrap(s, found)
        n += 1
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return n


def fused():
    p = os.path.join(D, 'Includes_Fused.xml')
    s = io.open(p, encoding='utf-8').read()
    a = s.index('<include name="FG_V510_View">')
    n = 0
    while True:
        i = s.find(MARK, a)
        if i < 0:
            break
        lay = max(s.rfind('<itemlayout', a, i), s.rfind('<focusedlayout', a, i))
        if not s.startswith('<itemlayout', lay):
            a = i + len(MARK)
            continue
        s = s[:a] + unwrap(s[a:], i - a)
        n += 1
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return n


def main():
    n1, n2 = aeon(), fused()
    p = os.path.join(D, 'Includes_Aeon_Views2.xml')
    s = io.open(p, encoding='utf-8').read()
    if '<variable name="Aeon_VerInline">' not in s:
        i = s.index('\t<variable name="Aeon_VerStat">')
        s = s[:i] + VAR + s[i:]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('version tag rows: Aeon %d and Fused %d unfocused rows now inline' % (n1, n2))


if __name__ == '__main__':
    main()
