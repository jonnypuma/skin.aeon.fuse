# -*- coding: utf-8 -*-
"""0.56.53 strings, all 23 languages: Recommended add-ons (32762-32770, 32790) and Update and clean on another Kodi
(32771-32789). Repeatable: an id that is there is written again."""
import io
import os
import re

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
IDS = [32762, 32764, 32765, 32766, 32767, 32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775, 32776, 32777, 32778,
       32779, 32780, 32781, 32782, 32783, 32784, 32785, 32786, 32789, 32790, 32791, 32792, 32793, 32794]
from strings_05653_data import EN, T  # noqa: E402,F401


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    for code, row in T.items():
        assert len(row) == len(IDS), (code, len(row))
    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        code = d.replace('resource.language.', '')
        for i, sid in enumerate(IDS):
            tr = '' if code == 'en_gb' else esc(T[code][i])
            m = re.search(r'(msgctxt "#%d"\nmsgid ")(.*)("\nmsgstr ")(.*)(")' % sid, t)
            if m:
                t = t[:m.start()] + m.group(1) + esc(EN[i]) + m.group(3) + tr + m.group(5) + t[m.end():]
            else:
                t = t.rstrip('\n') + '\n\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(EN[i]), tr)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('ok', len(IDS), 'strings in', len(os.listdir(L)), 'languages')


if __name__ == '__main__':
    main()
