"""0.56.35 Raw format names everywhere (the user, 2026-11-17: "eac3 atmos instead of DD+ Atmos"; "the raw labels
mapping should be applied everywhere for both video and audio formats").

Kodi names a stream eac3_ddp_atmos, truehd_atmos, dtshd_ma, hevc ...; the box's library also holds the spellings of
the NFO files its tools wrote: eac3 atmos, truehd atmos, truehd/atmos, dts-hd ma, dts_x, ac-3, dca, x264, avc, x265,
h265, mpeg2video, vc-1, hdr. The skin's tests only knew Kodi's names, so those titles showed the raw name
("EAC3 ATMOS") or the wrong one (hdr -> SDR). Every String.IsEqual(<info>.AudioCodec|VideoCodec|HdrType,<key>) in
1080i/*.xml becomes [that test | the aliases of key]; the value it belongs to keeps its label, so every variable
(spotlights, views, info page, OSD, flags) maps the raw names like Kodi's. Spaces, slashes and '+' cannot stand in a
Kodi condition, so the aliases test the start and the end of the name (eac3 ... atmos).

Precedence: the Atmos / DTS:X lines must come before plain DD+ / TrueHD / DTS-HD in a variable (the plain aliases
are wider); the script checks it in every variable it touches. Repeatable (a wrapped test starts with '['; an alias
is never a key itself, or a second run would wrap it again).
Run from the skin folder after every generator that writes codec tests (they are written plain)."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')


def ALIAS(x, field, key):
    a = '%s.%s' % (x, field)
    eq = lambda v: 'String.IsEqual(%s,%s)' % (a, v)                     # noqa: E731
    sw = lambda v: 'String.StartsWith(%s,%s)' % (a, v)                  # noqa: E731
    ew = lambda v: 'String.EndsWith(%s,%s)' % (a, v)                    # noqa: E731
    co = lambda v: 'String.Contains(%s,%s)' % (a, v)                    # noqa: E731
    table = {
        'AudioCodec': {
            'eac3_ddp_atmos': ['[%s + %s]' % (sw('eac3'), co('atmos')), '[%s + %s]' % (sw('e-ac-3'), co('atmos'))],
            'truehd_atmos': ['[%s + %s]' % (sw('truehd'), co('atmos'))],
            'dtshd_ma_x': ['[%s + %s]' % (sw('dts'), ew('x')), eq('dts_x')],
            'dtshd_ma': ['[%s + %s]' % (sw('dts-hd'), ew('ma'))],
            'dtshd_hra': ['[%s + %s]' % (sw('dts-hd'), ew('hra'))],
            'eac3': [eq('e-ac-3'), eq('eac-3'), sw('eac3')],
            'truehd': [sw('truehd')],
            'ac3': [eq('ac-3'), eq('a52')],
            'dts': [eq('dca')],
            'aac': [sw('aac'), eq('mp4a')],
            'pcm': [sw('pcm'), eq('lpcm')],
        },
        'VideoCodec': {
            'hevc': [eq('x265'), eq('h265'), eq('h.265'), eq('hev1'), eq('hvc1')],
            'h264': [eq('x264'), eq('avc'), eq('avc1'), eq('h.264')],
            'mpeg2': [eq('mpeg2video'), eq('mpeg-2')],
            'vc1': [eq('vc-1'), eq('wvc1')],
            'mpeg4': [eq('xvid'), eq('divx'), eq('dx50')],
        },
        'HdrType': {
            'dolbyvision': [eq('dv'), eq('dovi')],
            'hdr10': [eq('hdr')],
        },
    }
    return table.get(field, {}).get(key, [])


ATOM = re.compile(r'(?<!\[)String\.IsEqual\(([A-Za-z0-9_().]+?)\.(AudioCodec|VideoCodec|HdrType),([a-z0-9_.-]+)\)')
VAR = re.compile(r'<variable name="([^"]+)">(.*?)</variable>', re.S)
# a line that must come first (its key) before a line with the wider plain key
ORDER = (('eac3_ddp_atmos', 'eac3'), ('truehd_atmos', 'truehd'), ('dtshd_ma_x', 'dtshd_ma'), ('dtshd_ma_x', 'dts'))


def check(text, name):
    bad = []
    for m in VAR.finditer(text):
        lines = re.findall(r'<value condition="([^"]*)"', m.group(2))
        firsts = {}
        for i, c in enumerate(lines):
            for k in re.findall(r'\.(?:AudioCodec),([a-z0-9_.-]+)\)', c):
                firsts.setdefault(k, i)
        for hi, lo in ORDER:
            if hi in firsts and lo in firsts and firsts[hi] > firsts[lo]:
                bad.append((name, m.group(1), hi, lo))
    return bad


def main():
    total, bad = 0, []
    for fn in sorted(os.listdir(D)):
        if not fn.endswith('.xml') or fn == 'Font.xml':
            continue
        p = os.path.join(D, fn)
        t = io.open(p, encoding='utf-8').read()
        n = [0]

        def sub(m):
            al = ALIAS(m.group(1), m.group(2), m.group(3))
            if not al:
                return m.group(0)
            n[0] += 1
            return '[%s | %s]' % (m.group(0), ' | '.join(al))
        new = ATOM.sub(sub, t)
        bad += check(new, fn)
        if n[0]:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(new)
            print('%-32s %d tests' % (fn, n[0]))
            total += n[0]
    print('aliases added to %d tests' % total)
    for b in bad:
        print('ORDER', b)


if __name__ == '__main__':
    main()
