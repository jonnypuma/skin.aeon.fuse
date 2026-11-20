# -*- coding: utf-8 -*-
"""0.56.7 Names in every script: music names and Live TV names (the user, 2026-11-16: Japanese artist names showed as
rectangles; chose "Names in music views"; then: "changing fonts for artists and live tv, we really need to ensure that
it is also done for all the font sets").

Kodi has no fallback font for a missing character: a label's font either has the glyph or draws a box, and the skin's
font families have no Japanese, Chinese or Korean (Figtree not even Cyrillic). Kodi's own special://xbmc/media/Fonts/
arial.ttf (DejaVu Sans with the CJK glyphs added, 34 275 characters) has them all.
  - every skin font X that a name label uses gets a twin un_X in EVERY font set of Font.xml: Kodi's arial.ttf at the
    size X has in that font set (each set keeps its own sizes), bold when X is bold or semibold. Plain names: the
    helper's fonts.py rebuilds only the section blocks (lb_ / hm_ / ...), so these stay.
  - name labels (scopes below) take the twin; every other text keeps the skin's font:
      music views (FG_V513 / 530 / 531 / 532 / 533 / 534, not the A-Z letters): artist / album / track names,
        the header, card caption and row subline;
      Live TV: channel names and programme titles (ChannelName, EpgEventTitle, next programme) wherever they are,
        and item names / titles inside the PVR windows and dialogs and their Fused Glass parts.
Run from the skin folder: python _src/fg_cjk_names.py [box Font.xml copy] (the box keeps its own Font.xml: fetch it,
run this with its path, put it back). Safe to run again."""
import io
import os
import re
import sys

D = '1080i'
ARIAL = 'special://xbmc/media/Fonts/arial.ttf'
MARK = "<!-- 0.56.7 names in every script (Kodi's arial.ttf has CJK): _src/fg_cjk_names.py -->"
MUSIC = re.compile(r'ListItem\.(?:Label|Artist|Album|Title|AlbumArtist)\b|ListItem\.Property\((?:artist|album|Album_|Artist_)|'
                   r'\$VAR\[(?:FG_M_(?:HTitle|Name|ArtistName|HKicker|RowSub)|AeonM_Header)\]')
LIVE = re.compile(r'ChannelName|EpgEventTitle|NextTitle|NextEpisodeName')
PVR_ITEM = re.compile(r'ListItem\.(?:Label|Title|EpisodeName)\b|' + LIVE.pattern)
CONTROL = re.compile(r'<control type="(?:label|fadelabel|textbox|button)"[^>]*>(?:(?!</control>).)*?</control>', re.S)
FG_PVR = re.compile(r'^(?:FG_PVR\w*|FG_ChOSD|FG_OSDCard|FG_OSDGhost|Misc_PVR\w*|FG_H_LiveTV\w*|Aeon_H_LiveTV\w*)$')


def labels(blk, pattern):
    """(start, end, font) of the name labels in blk"""
    for c in CONTROL.finditer(blk):
        s = c.group(0)
        lab = re.search(r'<label>([^<]*)</label>', s)
        f = re.search(r'<font>([^<]*)</font>', s)
        if lab and f and not f.group(1).startswith('un_') and pattern.search(lab.group(1)):
            yield c.start(), c.end(), f.group(1)


def includes(text, name_re):
    for m in re.finditer(r'<include name="([^"]+)">', text):
        if name_re.match(m.group(1)):
            yield m.group(1), m.start(), text.find('\n\t</include>', m.end())


def views():
    counts = {}
    for name in sorted(os.listdir(D)):
        if not name.endswith('.xml') or name == 'Font.xml':
            continue
        p = os.path.join(D, name)
        t = io.open(p, encoding='utf-8').read()
        spans = []
        for inc, a, b in includes(t, re.compile(r'^FG_V(?:513|53[0-4])_View$')):          # music views
            blk = t[a:b]
            rail = re.search(r'<control type="list" id="(5\d\d0001)">', blk)
            skip = (rail.start(), blk.find('</content></control>', rail.start())) if rail else (-1, -1)
            spans += [(a + x, a + y, f) for x, y, f in labels(blk, MUSIC) if not skip[0] <= x < skip[1]]
        if re.match(r'(MyPVR|DialogPVR)', name):                                            # Live TV windows
            spans += list(labels(t, PVR_ITEM))
        else:
            for inc, a, b in includes(t, FG_PVR):                                           # Live TV parts
                spans += [(a + x, a + y, f) for x, y, f in labels(t[a:b], PVR_ITEM)]
            spans += list(labels(t, LIVE))                                                  # channel / programme anywhere
        spans = sorted(set(spans))
        if not spans:
            continue
        out, pos = [], 0
        for a, b, f in spans:
            if a < pos:                                                                     # nested: done already
                continue
            out.append(t[pos:a] + t[a:b].replace('<font>%s</font>' % f, '<font>un_%s</font>' % f, 1))
            pos = b
        out.append(t[pos:])
        io.open(p, 'w', encoding='utf-8', newline='\n').write(''.join(out))
        counts[name] = len(spans)
    print('name labels:', counts)


def fonts(path):
    used = set()
    for name in os.listdir(D):
        if name.endswith('.xml') and name != 'Font.xml':
            used |= set(re.findall(r'<font>un_([^<]+)</font>', io.open(os.path.join(D, name), encoding='utf-8').read()))
    t = io.open(path, encoding='utf-8').read()
    t = re.sub(r'\t\t<!-- 0\.56\.7 names in every script[^\n]*\n(?:\t\t<font><name>un_[^\n]*\n)+', '', t)
    out, pos, sets, missing = [], 0, 0, set()
    for m in re.finditer(r'\t</fontset>', t):
        fs = t[t.rfind('<fontset id=', 0, m.start()):m.start()]
        add = []
        for f in sorted(used):
            d = re.search(r'<font>\s*<name>%s</name>(.*?)</font>' % re.escape(f), fs, flags=re.S)
            if not d:
                missing.add(f)
                continue
            size = re.search(r'<size>(\d+)</size>', d.group(1)).group(1)
            fn = re.search(r'<filename>([^<]*)</filename>', d.group(1)).group(1)
            style = re.search(r'<style>([^<]*)</style>', d.group(1))
            bold = bool(re.search(r'Bold|SemiBold|Semibold|Black|Heavy', fn)) or bool(style and 'bold' in style.group(1))
            line = re.search(r'<linespacing>[^<]*</linespacing>', d.group(1))
            add.append('\t\t<font><name>un_%s</name><filename>%s</filename><size>%s</size>%s%s</font>\n'
                       % (f, ARIAL, size, '<style>bold</style>' if bold else '', line.group(0) if line else ''))
        out.append(t[pos:m.start()] + '\t\t' + MARK + '\n' + ''.join(add))
        pos = m.start()
        sets += 1
    out.append(t[pos:])
    io.open(path, 'w', encoding='utf-8', newline='\n').write(''.join(out))
    print('%s: %d font sets, %d twins (%s)%s' % (path, sets, len(used), ', '.join(sorted(used)),
                                              '; NOT in every set: %s' % sorted(missing) if missing else ''))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        views()
    fonts(sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, 'Font.xml'))
