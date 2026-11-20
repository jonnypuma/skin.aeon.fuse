# -*- coding: utf-8 -*-
"""0.56.18 the user (2026-11-16, Aeon Glass, Look > Watched indicators): "pill for watched indicator too close to the
unwatched option".

Every Aeon / Aeon Glass option picker in Skin settings: each segment is made at least as wide as its longest label in
the Latin-script languages (Figtree Bold 22, the selected state) plus 16 px on each side. Segments only grow; the
picker keeps its right edge and grows to the left (the track with it), but never into the setting's name: the English
name (Figtree Bold 24) keeps 16 px before the track (a longer translated name ends in "..." there and scrolls when the
row has focus: picker_names_05618.py). Where 16 px a side does not fit, 14 down to 4 px are tried, then the same with
each segment sized for English with that padding and 4 px around its longest label; a picker that fits none keeps its old left edge. Run after
pickers_flush_05618.py; once (marker).

Fixed after the Fuse survey (2026-11-16): the gaps between segments are measured in their old places; measured against
the moved ones they came out negative and the widened segments overlapped by up to 27 px."""
import io
import os
import re
import xml.etree.ElementTree as ET

from PIL import ImageFont

S = os.path.join('1080i', 'SkinSettings.xml')
MARK = '0.56.18 pickers_fit'
PAD = 16
LATIN = ('en_gb', 'cs_cz', 'da_dk', 'de_de', 'es_es', 'fi_fi', 'fr_fr', 'hu_hu', 'it_it', 'nb_no', 'nl_nl', 'pl_pl',
         'pt_br', 'pt_pt', 'sv_se', 'tr_tr')
GEO = re.compile(r'<left>(-?\d+)</left><top>(-?\d+)</top><width>(\d+)</width><height>(\d+)</height>')
TRACK = re.compile(r'colordiffuse="(22ffffff|26000000)">\$VAR\[Aeon_MenuTexPill\]')
PILL = re.compile(r'colordiffuse="\$VAR\[(Aeon_Accent|Aeon_OnBarFill)\]">\$VAR\[Aeon_MenuTexPill\]')


def strings(lang):
    t = io.open(os.path.join('language', 'resource.language.%s' % lang, 'strings.po'), encoding='utf-8').read()
    return dict((m.group(1), m.group(3) or m.group(2)) for m in re.finditer(r'msgctxt "#(\d+)"\nmsgid "(.*)"\nmsgstr "(.*)"', t))


def resolve(label, table):
    txt = re.sub(r'\$ADDON\[skin\.aeon\.fuse (\d+)\]', lambda m: table.get(m.group(1), ''), label)
    txt = re.sub(r'\$LOCALIZE\[(\d+)\]', lambda m: table.get(m.group(1), ''), txt)
    txt = re.sub(r'\[/?[A-Z]+[^\]]*\]', '', txt)                 # [B] ... [/B]
    return None if '$' in txt else txt


def main():
    text = io.open(S, encoding='utf-8').read()
    if MARK in text:
        print('already')
        return
    font = ImageFont.truetype(os.path.join('fonts', 'Figtree-Bold.ttf'), 22)
    namefont = ImageFont.truetype(os.path.join('fonts', 'Figtree-Bold.ttf'), 24)
    tables = [strings(l) for l in LATIN]
    lines = text.split('\n')
    # pickers: the track line(s) and the segment pills after them, up to the next track
    found, cur, name = [], None, None
    for i, line in enumerate(lines):
        m = re.search(r'param name="label" value="([^"]*)"', line)
        if m:
            mx = re.search(r'param name="labelx" value="(\d+)"', line)
            name = (m.group(1), int(mx.group(1)) if mx else 16)
        g = GEO.search(line)
        if g and TRACK.search(line):
            if cur is None or cur['track'] != g.groups() or i - cur['last'] > 2:   # each row its own picker
                cur = {'start': i, 'track': g.groups(), 'segs': set(), 'name': name}
                found.append(cur)
            cur['last'] = i
            continue
        if cur is not None and g and PILL.search(line) and g.group(2) == cur['track'][1]:
            cur['segs'].add((int(g.group(1)), int(g.group(3))))
    grown = []
    for n, p in enumerate(found):
        if len(p['segs']) < 2:
            continue
        stop = found[n + 1]['start'] if n + 1 < len(found) else len(lines)
        tl, tt, tw, th = map(int, p['track'])
        segs = sorted(p['segs'])
        text_w, en_w = {}, {}
        for i in range(p['start'], stop):
            g = GEO.search(lines[i])
            m = re.search(r'<label>(.*?)</label>', lines[i])
            if not g or not m or (int(g.group(1)), int(g.group(3))) not in p['segs'] or int(g.group(2)) != tt:
                continue
            for table in tables:
                txt = resolve(m.group(1), table)
                if txt:
                    key = (int(g.group(1)), int(g.group(3)))
                    text_w[key] = max(text_w.get(key, 0), int(font.getlength(txt) + 0.999))
                    if table is tables[0]:
                        en_w[key] = int(font.getlength(txt) + 0.999)
        floor = -10 ** 6                                            # the track may not start left of this
        if p['name']:
            label, labx = p['name']
            english = resolve(label, tables[0])
            floor = labx + int(namefont.getlength(english) + 0.999) + 16 if english else tl   # unknown name: stay

        def layout(pad, shrink):
            new, right, nxt = {}, tl + tw, tl + tw
            for left, width in reversed(segs):
                gap = nxt - (left + width)                          # keep any gap the segments had (old places)
                nxt = left
                if (left, width) in text_w:
                    if shrink:                                      # 4 px for the longest label, pad for English
                        w = max(text_w[(left, width)] + 8, en_w.get((left, width), 0) + 2 * pad)
                    else:
                        w = max(width, text_w[(left, width)] + 2 * pad)
                else:
                    w = width
                right -= gap
                new[(left, width)] = (right - w, w)
                right -= w
            return new
        new = None
        # segments only grow; where no padding fits that way, each segment is sized for English with that padding and
        # 4 px around its longest translation (a segment may shrink)
        for shrink in (False, True):
            for pad in (PAD, 14, 12, 10, 8, 7, 6, 5, 4):
                trial = layout(pad, shrink)
                if min(v[0] for v in trial.values()) >= min(floor, tl):
                    new = trial
                    break
            if new is not None:
                break
        if new is None or all(new[s] == s for s in segs):
            continue
        ntl = min(v[0] for v in new.values())
        moves = [((tl, tw), (ntl, tl + tw - ntl))] + [(s, new[s]) for s in segs if new[s] != s]
        for i in range(p['start'], stop):
            for (ol, ow), (nl, nw) in moves:
                old = '<left>%d</left><top>%d</top><width>%d</width>' % (ol, tt, ow)
                if old in lines[i]:
                    lines[i] = lines[i].replace(old, '<left>%d</left><top>%d</top><width>%d</width>' % (nl, tt, nw))
                    break
        grown.append((p['start'] + 1, tl - ntl))
    text = '\n'.join(lines).replace('<window', '<!-- %s: picker segments as wide as their longest label + 16 px a side -->\n<window' % MARK, 1)
    io.open(S, 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(S)
    print('grew', len(grown), 'pickers; more than 40 px:', [g for g in grown if g[1] > 40])


if __name__ == '__main__':
    main()
