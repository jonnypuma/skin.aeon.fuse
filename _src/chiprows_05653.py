# -*- coding: utf-8 -*-
"""0.56.53 Skin settings > Information: the rows Resolution and codec (9700, aeon.hide.res), HDR tag (9701,
aeon.hide.hdr) and Audio codec and channels (9702, aeon.hide.audio) go (user, 2026-11-19: "there is an overlap here and
it is confusing"). They switched the same settings as three ticks of Media info chips (9780, helper chippick), which
covers every chip, and their names promised more than they did (the codec and the channels are chips of their own).
The settings, their defaults and what they show are unchanged; only the picker sets them now.
Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_rows as sr  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'SkinSettings.xml')
ROWS = (9700, 9701, 9702)


def main():
    t = io.open(P, encoding='utf-8').read()
    lists = set()
    gone = 0
    for rid in ROWS:
        try:
            lists.add(sr.list_of(t, rid))
            s, e = sr.item_span(t, rid)
        except ValueError:
            continue
        t = t[:s].rstrip('\t ') + t[e:].lstrip('\n')
        gone += 1
    for gid in lists:
        t = sr.renav(t, gid)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('information rows removed: %d, lists rewired: %s' % (gone, sorted(lists)))


if __name__ == '__main__':
    main()
