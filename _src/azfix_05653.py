# -*- coding: utf-8 -*-
"""0.56.53 the A-Z strips jump to the right letter (user, 2026-11-20: "The A-Z picker doesn't work properly anymore. in
Movies List view, pressing the letter B jumps to the letter C. Pressing A jumps to #").

Each letter set the focus on the view (keeping its position) and pressed Kodi's phone-key jumps (JumpSMS2 = A B C 2,
JumpSMS3 = D E F 3, ...) once, twice or three times. Kodi counts those from the letter of the item in focus: on an "A"
title one press of 2 goes to B, on a "C" title to 2 (the # titles) - so the letter depended on where you were.
Now each letter first goes to the top of the view (SetFocus(view,0,absolute)), where the count starts fresh; when the
view's first item already begins with that letter, it stays there (the presses are skipped). Every letter strip of the
video and music libraries. Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
ITEM = re.compile(r'<item>\s*<label>([A-Z])</label>((?:\s*<onclick[^>]*>[^<]*</onclick>)+)\s*</item>')


def fix(m):
    letter, clicks = m.group(1), m.group(2)
    sf = re.search(r'<onclick>SetFocus\((\d+)\)</onclick>', clicks)
    if not sf or 'JumpSMS' not in clicks or 'ListItemAbsolute(0).SortLetter' in clicks:
        return m.group(0)
    view = sf.group(1)
    cond = '!String.IsEqual(Container(%s).ListItemAbsolute(0).SortLetter,%s)' % (view, letter)
    clicks = clicks.replace(sf.group(0), '<onclick>SetFocus(%s,0,absolute)</onclick>' % view, 1)
    clicks = re.sub(r'<onclick>(Action\(JumpSMS\d\))</onclick>', r'<onclick condition="%s">\1</onclick>' % cond, clicks)
    return m.group(0).replace(m.group(2), clicks, 1)


BUTTON = re.compile(r'(<control type="button" id="[^"]*">(?:(?!</control>).)*?<label>([A-Z])</label>(?:(?!</control>).)*?)'
                    r'<onclick>SetFocus\((\$PARAM\[cid\]|\d+)\)</onclick>((?:\s*<onclick>Action\(JumpSMS\d\)</onclick>)+)', re.S)


def fix_button(m):
    head, letter, view, presses = m.group(1), m.group(2), m.group(3), m.group(4)
    cond = '!String.IsEqual(Container(%s).ListItemAbsolute(0).SortLetter,%s)' % (view, letter)
    presses = re.sub(r'<onclick>(Action\(JumpSMS\d\))</onclick>', r'<onclick condition="%s">\1</onclick>' % cond, presses)
    return head + '<onclick>SetFocus(%s,0,absolute)</onclick>' % view + presses


def main():
    total = 0
    for name in sorted(os.listdir(D)):
        if not name.endswith('.xml'):
            continue
        p = os.path.join(D, name)
        t = io.open(p, encoding='utf-8').read()
        if 'JumpSMS' not in t:
            continue
        t2, n = ITEM.subn(fix, t)
        t2, nb = BUTTON.subn(fix_button, t2)
        changed = sum(1 for a, b in zip(ITEM.findall(t), ITEM.findall(t2)) if a != b) + nb
        if t2 != t:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t2)
            print('%-28s %d letters' % (name, changed))
            total += changed
    print('letters fixed: %d' % total)


if __name__ == '__main__':
    main()
