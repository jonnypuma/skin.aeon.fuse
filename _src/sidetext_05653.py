# -*- coding: utf-8 -*-
"""0.56.53 the Aeon / Aeon Glass library views write the media info as a line of text ($VAR[Aeon_TxMedia]:
"TRUEHD 7.1  •  1.78:1  •  DV P7 MEL  •  4K"), not as chips, so the sidecar chips (sidechips_05653.py) never reached
them (sweep 2026-11-19). $VAR[Aeon_TxSide] (Includes_Aeon_Views2.xml, after Aeon_TxMedia) adds the sidecar values
switched on in Media info chips to that line, in the same "  •  " way: video codec, container, bitrate first, then
video source, version, size, subtitles, chapters, commentary, 3D; only while the sidecar is the focused file's.
Every label that shows $VAR[Aeon_TxMedia] gets $VAR[Aeon_TxSide] right after it. Repeatable."""
import glob
import io
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
V = os.path.join(D, 'Includes_Aeon_Views2.xml')
MI = 'Window(Home).Property(aeon.mi.%s)'
SEP = '  •  '
PARTS = [('vcodec', '$INFO[%s,%s,]' % (MI % 'vcodec', SEP)),
         ('container', '$INFO[%s,%s,]' % (MI % 'container', SEP)),
         ('bitrate', '$INFO[%s,%s,]' % (MI % 'bitrate', SEP)),
         ('vsource', '$INFO[%s,%s,]' % (MI % 'vsource', SEP)),
         ('size', '$INFO[%s,%s,]' % (MI % 'size', SEP)),
         ('subs', '$INFO[%s,%s, $LOCALIZE[287]]' % (MI % 'subs.count', SEP)),
         ('chapters', '$INFO[%s,%s, $ADDON[skin.aeon.fuse 32661]]' % (MI % 'chapters', SEP)),
         ('commentary', '%s$ADDON[skin.aeon.fuse 32662]' % SEP),
         ('3d', '%s3D' % SEP)]
GATE = ('Skin.HasSetting(aeon.mi.sidecar) + '
        'String.IsEqual(Window(Home).Property(aeon.mi.path),ListItem.FileNameAndPath)')
MARK = '<!-- 0.56.53 sidecar text -->'


def variables():
    out = ['\t' + MARK]
    for key, text in PARTS:
        cond = 'Skin.HasSetting(aeon.chip.%s)' % key
        if key in ('commentary', '3d'):
            cond += ' + !String.IsEmpty(%s)' % (MI % key)
        out.append('\t<variable name="Aeon_TxSide_%s"><value condition="%s">%s</value></variable>' % (key, cond, text))
    out.append('\t<variable name="Aeon_TxSide"><value condition="%s">[UPPERCASE]%s[/UPPERCASE]</value></variable>'
               % (GATE, ''.join('$VAR[Aeon_TxSide_%s]' % k for k, _t in PARTS)))
    return '\n'.join(out) + '\n'


def main():
    s = io.open(V, encoding='utf-8').read()
    if MARK not in s:
        i = s.index('\t<variable name="Aeon_TxMedia">')
        s = s[:i] + variables() + s[i:]
        io.open(V, 'w', encoding='utf-8', newline='\n').write(s)
    n = 0
    for p in glob.glob(os.path.join(D, '*.xml')):
        t = io.open(p, encoding='utf-8').read()
        u = t.replace('$VAR[Aeon_TxMedia]$VAR[Aeon_TxSide]', '$VAR[Aeon_TxMedia]')
        k = u.count('$VAR[Aeon_TxMedia]')
        u = u.replace('$VAR[Aeon_TxMedia]', '$VAR[Aeon_TxMedia]$VAR[Aeon_TxSide]')
        if u != t:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(u)
        n += k
    print('sidecar text after %d Aeon_TxMedia uses' % n)


if __name__ == '__main__':
    main()
