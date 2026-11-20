# -*- coding: utf-8 -*-
"""0.56.18 the user (2026-11-16): "the highlight bar/pill does not completely cover the grey options strip background.
... Should not be able to see the option strip background or outline and be completely covered by the button at each
end."

The Aeon / Aeon Glass option pickers in Skin settings draw a track (22ffffff / 26000000, Aeon_MenuTexPill) and segment
pills inset 4 - 10 px from its ends, so a selected first or last segment left the track's end showing. Every picker's
first segment now starts at the track's left edge and its last segment ends at the track's right edge (its pills and
its labels: the text stays centred in the wider pill). Runs once (marker) on the finished SkinSettings.xml; run again
after a generator rewrites SkinSettings.xml."""
import io
import os
import re
import xml.etree.ElementTree as ET

S = os.path.join('1080i', 'SkinSettings.xml')
MARK = '0.56.18 pickers_flush'
GEO = re.compile(r'<left>(-?\d+)</left><top>(-?\d+)</top><width>(\d+)</width><height>(\d+)</height>')
TRACK = re.compile(r'colordiffuse="(22ffffff|26000000)">\$VAR\[Aeon_MenuTexPill\]')
RIGHT = 860                                       # the right edge most pickers share
PILL = re.compile(r'colordiffuse="\$VAR\[(Aeon_Accent|Aeon_OnBarFill)\]">\$VAR\[Aeon_MenuTexPill\]')


def pickers(lines):
    out, cur = [], None
    for i, line in enumerate(lines):
        g = GEO.search(line)
        if g and TRACK.search(line):
            if cur is None or cur['track'] != g.groups() or i - cur['last'] > 2:   # each row its own picker
                cur = {'start': i, 'track': g.groups(), 'segs': set()}
                out.append(cur)
            cur['end'] = cur['last'] = i
            continue
        if cur is not None and g and PILL.search(line) and g.group(2) == cur['track'][1]:
            cur['segs'].add((int(g.group(1)), int(g.group(3))))
            cur['end'] = i
    return out


def main():
    text = io.open(S, encoding='utf-8').read()
    lines = text.split('\n')                      # safe to run again: only ends that are off move
    found = pickers(lines)
    fixed = 0
    for n, p in enumerate(found):
        if not p['segs']:
            continue
        tl, tt, tw, th = map(int, p['track'])
        first = min(p['segs'])
        last = max(p['segs'], key=lambda s: s[0] + s[1])
        stop = found[n + 1]['start'] if n + 1 < len(found) else len(lines)
        moves = []
        if first[0] != tl:
            moves.append((first, (tl, first[1] + first[0] - tl)))
        if last[0] + last[1] != tl + tw:
            moves.append((last, (last[0], tl + tw - last[0]) if last != first else (tl, tw)))
        if not moves:
            continue
        for i in range(p['start'], stop):
            for (ol, ow), (nl, nw) in moves:
                old = '<left>%d</left><top>%s</top><width>%d</width>' % (ol, tt, ow)
                if old in lines[i]:
                    lines[i] = lines[i].replace(old, '<left>%d</left><top>%s</top><width>%d</width>' % (nl, tt, nw))
        # a picker whose first and last moves touch the same segment twice (one segment) is handled by the second move
        fixed += 1
    text = '\n'.join(lines)
    # every picker ends on the same line (the common right edge, 860): shift the odd ones whole
    lines = text.split('\n')
    found = pickers(lines)
    shifted = 0
    for n, p in enumerate(found):
        tl, tt, tw, th = map(int, p['track'])
        delta = RIGHT - (tl + tw)
        if not delta or not p['segs']:
            continue
        stop = found[n + 1]['start'] if n + 1 < len(found) else len(lines)
        geos = {(tl, tw)} | set(p['segs'])
        for i in range(p['start'], stop):
            for ol, ow in geos:
                old = '<left>%d</left><top>%d</top><width>%d</width>' % (ol, tt, ow)
                if old in lines[i]:
                    lines[i] = lines[i].replace(old, '<left>%d</left><top>%d</top><width>%d</width>' % (ol + delta, tt, ow))
                    break
        shifted += 1
    text = '\n'.join(lines)
    print('shifted to the common right edge:', shifted)
    if MARK not in text:
        text = text.replace('<window', '<!-- %s: the option pickers\' end segments reach the track ends -->\n<window' % MARK, 1)
    io.open(S, 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(S)
    left = [p for p in pickers(text.split('\n')) if p['segs'] and (min(p['segs'])[0] != int(p['track'][0]) or max(s[0] + s[1] for s in p['segs']) != int(p['track'][0]) + int(p['track'][2]))]
    print('fixed', fixed, 'of', len(found), '- still off:', len(left))


if __name__ == '__main__':
    main()
