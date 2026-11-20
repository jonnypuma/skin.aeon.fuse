# -*- coding: utf-8 -*-
"""0.56.53 row chips right-aligned (user, 2026-11-19: "Season Low List: mediachips on each row need to start from same
position on the right so they all look uniformly aligned on the right, that means there must be enough space between
chips and duration for when something is in progress and says there is x time left ... that's a general issue in most
list views").
The Fused Glass list rows drew their chips at fixed slots (resolution 0, audio 52, aspect 168, ...) in a group whose
left depended on the variant (HDR / rating or not), sliding 60-72 px left while an item is in progress: a chip that
does not apply left a hole, and rows in progress stood apart from the others. Now every chip run is a horizontal
grouplist aligned right, ending at one edge per layout: the duration column (FG_L_RowRight, right-aligned) keeps
RESERVE px for its text ("3·29 left") plus GAP, whether the item is in progress or not. A chip = a group of its
image's width (image at 0, label at 6) with the image's conditions, so a chip that does not apply takes no room.
Lists: List 510, Low list 527 (both layouts), the episode lists 511 / 5121 / 5171 / 5181, Compact list 524.
Run after the view generators and the 0.56.53 chip steps. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'Includes_Fused.xml')
MARK = '<!-- 0.56.53 row chips right -->'
LISTS = ('510', '527', '511', '5121', '5171', '5181', '524')
GAP = 10
GROUP = re.compile(r'<control type="group"><left>(\d+)</left><top>(\d+)</top>')
SLIDE = re.compile(r'<animation effect="slide" start="0,0" end="-(\d+),0" time="0" condition="Integer\.IsGreater\(ListItem\.PercentPlayed,0\)">Conditional</animation>')
RIGHT = re.compile(r'<control type="label"><left>(\d+)</left><top>(\d+)</top><width>(\d+)</width><height>(\d+)</height>'
                   r'<align>right</align><aligny>center</aligny><font>([^<]*)</font>(?:(?!</control>).)*?<label>\$VAR\[FG_L_RowRight\]</label>', re.S)
SUB = re.compile(r'<control type="label"><left>(\d+)</left><top>(\d+)</top><width>(\d+)</width><height>\d+</height>[^\n]*?'
                 r'<label>(?:\$VAR\[FG_L_RowSub\]|\$INFO\[ListItem\.Premiered\])</label>')


def reserve(font):
    return 124 if '_24' in font else 112


def chips(m, seg, a, e):
    """the chip group's children as [(width, height, chip xml)], or None when it holds anything but image / label pairs"""
    kids = ss.children(m, a, e)
    out = []
    i = 0
    while i < len(kids):
        x = seg[kids[i][0]:kids[i][1]]
        g = re.match(r'<control type="image"><left>(\d+)</left><top>0</top><width>(\d+)</width><height>(\d+)</height>', x)
        if not g:
            return None
        left, w, h = map(int, g.groups())
        lab = ''
        if i + 1 < len(kids):
            y = seg[kids[i + 1][0]:kids[i + 1][1]]
            if re.match(r'<control type="label"><left>%d</left><top>0</top>' % (left + 6), y):
                lab = y
                i += 1
        i += 1
        vis = ''.join('<visible>%s</visible>' % v for v in re.findall(r'<visible>(.*?)</visible>', x, re.S))
        img = x.replace('<left>%d</left>' % left, '<left>0</left>', 1)
        lab = lab.replace('<left>%d</left>' % (left + 6), '<left>6</left>', 1)
        # one disabled button per chip: a label or image inside a group inside a grouplist gets no item info in a
        # list row (the chips came out empty on the box); a button draws its own background and text
        tex = re.search(r'<texture([^>]*)>([^<]*)</texture>', x)
        if lab:
            text = re.search(r'<label>(.*?)</label>', lab, re.S).group(1)
            font = re.search(r'<font>([^<]*)</font>', lab).group(1)
            col = re.search(r'<textcolor>([^<]*)</textcolor>', lab).group(1)
        else:
            text, font, col = '', 'lb_cap_14', 'ffffffff'
        out.append((w, h, '<control type="button"><width>%d</width><height>%d</height><label>%s</label><font>%s</font>'
                          '<textcolor>%s</textcolor><focusedcolor>%s</focusedcolor><disabledcolor>%s</disabledcolor>'
                          '<align>center</align><aligny>center</aligny><textoffsetx>6</textoffsetx><enable>false</enable>'
                          '<texturenofocus%s>%s</texturenofocus><texturefocus%s>%s</texturefocus>%s</control>'
                          % (w, h, text, font, col, col, col, tex.group(1), tex.group(2), tex.group(1), tex.group(2), vis)))
    return out


def layout(x):
    """one item / focused layout: (new xml, [(old left, new left, width, content)])"""
    r = RIGHT.search(x)
    if not r:
        return x, []
    rl, rt, rw, rh, font = int(r.group(1)), int(r.group(2)), int(r.group(3)), int(r.group(4)), r.group(5)
    edge = rl + rw - reserve(font) - GAP
    report = []
    pos = 0
    while True:
        g = GROUP.search(x, pos)
        if not g:
            break
        m = ss.masked(x)
        a = g.start()
        e = ss.ctl_end(m, a)
        body = x[g.end():e - len('</control>')]
        if '<control type="group">' not in x[a + 10:e] and SLIDE.search(body) is None and 'Aeon_ResChip' not in body:
            pos = e
            continue
        inner_start = g.end()
        vis = ''
        mm = re.match(r'((?:<visible>.*?</visible>)*)', x[inner_start:], re.S)
        vis = mm.group(1)
        k = inner_start + len(vis)
        sl = SLIDE.match(x, k)
        slide = int(sl.group(1)) if sl else 0
        k = sl.end() if sl else k
        if not x.startswith('<control type="image">', k) or 'Aeon_ResChip' not in body:
            pos = e
            continue
        parts = chips(ss.masked(x), x, a, e)
        if not parts:
            pos = e
            continue
        left = int(g.group(1)) - slide
        h = max(p[1] for p in parts)
        content = sum(p[0] for p in parts) + 6 * (len(parts) - 1)
        left = min(left, edge - content)        # never narrower than its widest run
        new = ('%s<control type="grouplist"><left>%d</left><top>%s</top><width>%d</width><height>%d</height>'
               '<orientation>horizontal</orientation><align>right</align><itemgap>6</itemgap><usecontrolcoords>true</usecontrolcoords>'
               '%s%s</control>' % (MARK, left, g.group(2), edge - left, h, vis, ''.join(p[2] for p in parts)))
        report.append((int(g.group(1)), left, edge - left, content))
        x = x[:a] + new + x[e:]
        pos = a + len(new)
    return x, report


def main(dry=False):
    s = io.open(P, encoding='utf-8').read()
    if MARK in s and not dry:
        print('row chips: already there')
        return
    for lid in LISTS:
        j = s.find('id="%s"' % lid)
        if j < 0 or not re.search(r'<control type="(?:list|panel|fixedlist|wraplist)" id="%s"' % lid, s[j - 40:j + 10]):
            hits = [x.start() for x in re.finditer(r'<control type="(?:list|panel|fixedlist|wraplist)" id="%s"' % lid, s)]
            if not hits:
                print('  %s: no list' % lid)
                continue
            j = hits[0]
        end = s.index('</content>', j) if '</content>' in s[j:s.find('</control>', j) + 200000][:0] else None
        k = j
        while True:
            m = re.compile(r'<(itemlayout|focusedlayout)[^>]*>').search(s, k)
            nxt = re.compile(r'<control type="(?:list|panel|fixedlist|wraplist)" id=').search(s, k + 10)
            if not m or (nxt and nxt.start() < m.start()):
                break
            e = s.index('</%s>' % m.group(1), m.end())
            x, rep = layout(s[m.end():e])
            for r in rep:
                print('  %s %s: group %d -> %d, room %d, widest %d%s' % (lid, m.group(1)[0], r[0], r[1], r[2], r[3],
                                                                    '  TOO NARROW' if r[3] > r[2] else ''))
            s = s[:m.end()] + x + s[e:]
            k = m.end() + len(x)
    # Compact list: the title of a row not in progress was wider (its chips sat further right); every row now
    # ends its chips at the same edge, so the title keeps the in-progress width
    a = s.index('<include name="FG_V524_View">')
    b = s.find('<include name=', a + 10)
    seg = s[a:b]
    seg = seg.replace('<left>18</left><top>0</top><width>346</width><height>58</height>', '<left>18</left><top>0</top><width>290</width><height>58</height>')
    seg = seg.replace('<left>54</left><top>0</top><width>310</width><height>58</height>', '<left>54</left><top>0</top><width>254</width><height>58</height>')
    s = s[:a] + seg + s[b:]
    if not dry:
        io.open(P, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    main('--dry' in sys.argv)
