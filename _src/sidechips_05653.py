# -*- coding: utf-8 -*-
"""0.56.53 sidecar chips everywhere the media chips are (user, 2026-11-19: "i have turned a lot of the sidecar chips
on and they are not showing most places ... not in library views, spotlight or widgets").
The sidecar values (helper MediaInfoSidecar: Window(Home).Property(aeon.mi.<key>) for the file aeon.mi.path) were
drawn on the information page only. Every chip row of the skin is a run of chip buttons that carry the place gate
($EXP[Aeon_Chip_<place>], placegate_05652.py); after each run this adds the sidecar chips switched on in Media info
chips (video source, video codec, container, bitrate, size, subtitles, chapters, commentary, 3D), one set
per theme look found in the run (each clone keeps its template's look, theme condition and place gate), shown only
while the sidecar belongs to that row's item (<prefix>FileNameAndPath of the row's container).
Run after placegate_05652.py (and so after the view generators). Repeatable (a run that has them is skipped)."""
import glob
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
SKIP = ('SkinSettings.xml', 'Includes_VideoInfo.xml', 'Custom_1173_SetupWizard.xml')
MARK = '<!-- 0.56.53 sidecar chips -->'
MI = 'Window(Home).Property(aeon.mi.%s)'
CHIPS = [('vsource', '[UPPERCASE]$INFO[%s][/UPPERCASE]' % (MI % 'vsource')),
         ('vcodec', '[UPPERCASE]$INFO[%s][/UPPERCASE]' % (MI % 'vcodec')),
         ('container', '[UPPERCASE]$INFO[%s][/UPPERCASE]' % (MI % 'container')),
         ('bitrate', '[UPPERCASE]$INFO[%s][/UPPERCASE]' % (MI % 'bitrate')),
         ('size', '[UPPERCASE]$INFO[%s][/UPPERCASE]' % (MI % 'size')),
         ('subs', '[UPPERCASE]$INFO[%s] $LOCALIZE[287][/UPPERCASE]' % (MI % 'subs.count')),
         ('chapters', '[UPPERCASE]$INFO[%s] $ADDON[skin.aeon.fuse 32661][/UPPERCASE]' % (MI % 'chapters')),
         ('commentary', '[UPPERCASE]$ADDON[skin.aeon.fuse 32662][/UPPERCASE]'),
         ('3d', '3D')]
KEYOF = {'subs': 'subs.count'}
BTN = re.compile(r'<control type="button">(?:(?!<control).)*?</control>', re.S)
GATE = re.compile(r'<visible>\$EXP\[Aeon_Chip_\w+\]</visible>|\$EXP\[Aeon_Chip_\$PARAM\[place\]\]|\$EXP\[Aeon_Chip_\w+\]')
EXP = re.compile(r'!?\$EXP\[(\w+)\]')
PFX = re.compile(r'(Container\(\d+\)\.ListItem\.|ListItem\.)(?:VideoResolution|AudioChannels|AudioCodec|VideoAspect|VideoCodec|Property|FileName)')


def is_chip(x):
    return bool(GATE.search(x)) and 'aeon.mi.' not in x


def signature(x):
    vis = re.search(r'<visible>(.*?)</visible>', x, re.S)
    toks = EXP.findall(vis.group(1)) if vis else []
    raw = re.findall(r'!?\$EXP\[\w+\]', vis.group(1)) if vis else []
    return tuple(t for t, n in zip(raw, toks) if not n.startswith('Aeon_Chip') and n not in ('Aeon_VOMedia',))


def clone(tpl, key, label, sig, pfx):
    x = re.sub(r'<label>.*?</label>', '<label>%s</label>' % label, tpl, count=1, flags=re.S)
    k = KEYOF.get(key, key)
    cond = ' + '.join(list(sig) + ['Skin.HasSetting(aeon.mi.sidecar)',
                                   'String.IsEqual(Window(Home).Property(aeon.mi.path),%sFileNameAndPath)' % pfx,
                                   '!String.IsEmpty(%s)' % (MI % k), 'Skin.HasSetting(aeon.chip.%s)' % key])
    parts = re.split(r'(<visible>.*?</visible>)', x, flags=re.S)
    out, first = [], True
    for p in parts:
        if p.startswith('<visible>') and first and not GATE.fullmatch(p):
            out.append('<visible>[%s]</visible>' % cond)
            first = False
        else:
            out.append(p)
    x = ''.join(out)
    if first:          # no theme visible of its own: put one in front of the gate
        x = x.replace('</control>', '<visible>[%s]</visible></control>' % cond, 1)
    return x


def runs(s):
    """[(start, end, [chip button texts])] of adjacent chip buttons (whitespace between them only)"""
    out, cur = [], None
    for m in BTN.finditer(s):
        if not is_chip(m.group(0)):
            if cur:
                out.append(cur)
                cur = None
            continue
        if cur and s[cur[1]:m.start()].strip() == '':
            cur[1] = m.end()
            cur[2].append(m.group(0))
        else:
            if cur:
                out.append(cur)
            cur = [m.start(), m.end(), [m.group(0)]]
    if cur:
        out.append(cur)
    return out


def main():
    total = 0
    for p in sorted(glob.glob(os.path.join(D, '*.xml'))):
        if os.path.basename(p) in SKIP:
            continue
        s = io.open(p, encoding='utf-8').read()
        n = 0
        for start, end, btns in reversed(runs(s)):
            if s[end:end + len(MARK) + 4].lstrip().startswith(MARK):
                continue
            pfx = None
            for b in btns:
                m = PFX.search(b)
                if m:
                    pfx = m.group(1)
                    break
            if not pfx:
                continue
            last = {}
            for b in btns:
                last[signature(b)] = b
            add = ''.join(clone(tpl, key, label, sig, pfx) for sig, tpl in last.items() for key, label in CHIPS)
            s = s[:end] + MARK + add + s[end:]
            n += 1
        if n:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
            print('%-32s %d chip rows' % (os.path.basename(p), n))
            total += n
    print('sidecar chips added to %d rows' % total)


if __name__ == '__main__':
    main()
