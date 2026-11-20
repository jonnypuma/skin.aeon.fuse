# -*- coding: utf-8 -*-
"""0.56.18 (after the Fuse survey, 2026-11-16): the option pickers in Skin settings grow to the left as far as the
English setting name allows (pickers_fit_05618.py), so a longer translated name (French "Indicateurs de visionnage")
would run under the track. Dlg_SkinRowChrome takes a name width (namew, 520 as before when not given); every row with
a picker gets namew = its track's left edge - 16 - the name's x, so the name ends in "..." before the track, and the
name of the focused row scrolls instead. Run after pickers_flush_05618.py; safe to run again (it rewrites namew)."""
import io
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pickers_flush_05618 as pf  # noqa: E402

S = os.path.join('1080i', 'SkinSettings.xml')
INC = os.path.join('1080i', 'Includes_Settings.xml')
MARK = '0.56.18 picker_names'


def include():
    t = io.open(INC, encoding='utf-8').read()
    if MARK in t:
        return False
    a = t.index('<include name="Dlg_SkinRowChrome">')
    b = t.index('</include>', a)
    s = t[a:b]
    s = s.replace('<param name="hintw">520</param>',
                  '<param name="hintw">520</param>\n\t\t<param name="namew">520</param><!-- %s: the name ends before the row\'s picker -->' % MARK, 1)
    n = s.count('<label>$PARAM[label]</label>')
    assert n == 4, n
    parts = s.split('<label>$PARAM[label]</label>')
    out = parts[0]
    for part in parts[1:]:
        # the label's own <width>520</width> is the last one before its <label>
        i = out.rindex('<width>520</width>')
        out = out[:i] + '<width>$PARAM[namew]</width>' + out[i + len('<width>520</width>'):]
        focused = part.split('</control>', 1)[0]
        tag = '<label>$PARAM[label]</label>'
        if 'Control.HasFocus($PARAM[id])</visible>' in focused and '!Control.HasFocus($PARAM[id])' not in focused:
            tag += '<scroll>true</scroll>'
        out += tag + part
    t = t[:a] + out + t[b:]
    io.open(INC, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(INC)
    return True


def main():
    changed = include()
    text = io.open(S, encoding='utf-8').read()
    lines = text.split('\n')
    rows = 0
    for p in pf.pickers(lines):
        track = lines[p['start']]
        m = re.search(r'Control\.HasFocus\((\d+)\)', track)
        if not m:
            continue
        rid = m.group(1)
        tl = int(p['track'][0])
        hits = [i for i, l in enumerate(lines) if 'param name="id" value="%s"/>' % rid in l
                and 'Dlg_SkinRowChrome' in lines[i - 1] + l.split('<param', 1)[0]]
        if len(hits) != 1:
            print('row', rid, 'chrome calls:', len(hits))
            continue
        i = hits[0]
        lx = re.search(r'param name="labelx" value="(\d+)"', lines[i])
        labx = int(lx.group(1)) if lx else 16
        w = min(520, tl - 16 - labx)
        lines[i] = re.sub(r'<param name="namew" value="\d+"/>', '', lines[i])
        if w < 520:
            lines[i] = lines[i].replace('<param name="id" value="%s"/>' % rid,
                                        '<param name="id" value="%s"/><param name="namew" value="%d"/>' % (rid, w), 1)
            rows += 1
    text = '\n'.join(lines)
    io.open(S, 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(S)
    print('include', 'changed' if changed else 'already', '- rows with a name width:', rows)


if __name__ == '__main__':
    main()
