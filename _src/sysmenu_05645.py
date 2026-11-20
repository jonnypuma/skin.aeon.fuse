# -*- coding: utf-8 -*-
"""0.56.45 the System menu (custom dialog 1151): the line under the focused item lists what is inside it (the user,
2026-11-18: "I would have expected under COREELEC to see the labels for: System - Updates - Network etc in smaller,
darker font"). Aeon_MenuRow shows ListItem.Property(cats) before Label2; the words are Kodi's and the skin's own
strings, so they are translated already ("Bluetooth" is the same everywhere). Update library keeps its counts, the
power items their sentences. Run from the skin folder. Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Custom_1151_SystemMenu.xml')
L = '$LOCALIZE[%d]'
A = '$ADDON[skin.aeon.fuse %d]'
DOT = '  •  '
CATS = {
    '$LOCALIZE[31200]': [L % 31725, L % 10000, A % 32722, A % 32723, L % 31727, L % 31731],   # Aeon Fuse settings
    '$LOCALIZE[5]': [L % 14200, L % 14211, L % 14022, L % 14204, L % 14036, L % 14206, L % 857],   # Kodi settings
    '$LOCALIZE[10003]': [L % 115, L % 116, L % 118, L % 117],                                  # File manager
    '$LOCALIZE[138]': [L % 20037, L % 154, L % 705, L % 157, L % 13281],                        # System info
    'CoreELEC': [L % 857, L % 14303, L % 705, 'Bluetooth', L % 14036],
    'LibreELEC': [L % 857, L % 14303, L % 705, 'Bluetooth', L % 14036],
    '$LOCALIZE[24001]': [L % 24998, L % 24033, L % 14303],                                     # Add-ons
    '$LOCALIZE[744]': [L % 3, L % 2, L % 1],                                                   # Media sources
    '$LOCALIZE[31205]': [L % 3, L % 2],                                                        # Clean library
}


def main():
    t = io.open(P, encoding='utf-8').read()
    n = 0
    for m in list(re.finditer(r'<item[^>]*>(.*?)</item>', t, re.S))[::-1]:
        body = m.group(1)
        lab = re.search(r'<label>([^<]*)</label>', body)
        if not lab or lab.group(1) not in CATS or '<property name="cats">' in body:
            continue
        cats = '<property name="cats">%s</property>' % DOT.join(CATS[lab.group(1)])
        k = m.start(1) + lab.end()
        t = t[:k] + '\n\t\t\t\t\t\t' + cats + t[k:]
        n += 1
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('System menu: %d items list their sections' % n)


if __name__ == '__main__':
    main()
