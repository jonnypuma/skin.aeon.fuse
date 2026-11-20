"""0.56.52 Widget & Spotlight screens (Custom_1157_Spotlight.xml): a dot for every item. The user, 2026-11-19: moving
past the last dot of the autoscroll, no more dots appeared and the focus dot was gone. The lists hold 30 items
(content limit), the pager drew a dot only for the autoscroll count (aeon.spot.countnow, at most 15 slots). Now every
item of the list has a dot, ten per page: items 1-10 on the first page, 11-20 on the second, 21-30 on the third; the
page follows the focused item. The autoscroll itself still runs over its count (Timers.xml unchanged).
Slot geometry and looks come from the old pager (slot n = old item n). Run from the skin folder. Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Custom_1157_Spotlight.xml')
HEAD = ('\t\t<!-- pager: ring on the current item, a dot for each other item (outside the lists so Container.CurrentItem '
        'is read from the focused page) -->\n\t\t<control type="group">\n')
MARK = '<!-- 0.56.52 dots for every item, ten per page -->'
PAGE, ITEMS, LISTS = 10, 30, range(9401, 9407)


def main():
    t = io.open(P, encoding='utf-8').read()
    s = t.index(HEAD) + len(HEAD)
    e = t.index('\t\t</control>\n\t\t<!-- header + clock', s)
    body = t[s:e]
    lines = [x for x in body.split('\n') if x.strip()]
    if MARK in body:
        lines = [x for x in lines if MARK not in x]
        # templates: the first PAGE slots of list 9401 (6 controls each) in the new form
        tpl = [x for x in lines if 'Control.HasFocus(9401)' in x][:PAGE * 6]
    else:
        tpl = [x for x in lines if 'Control.HasFocus(9401)' in x][:PAGE * 6]
    assert len(tpl) == PAGE * 6, len(tpl)
    out = ['\t\t\t' + MARK]
    for c in LISTS:
        for k in range(1, ITEMS + 1):
            slot = (k - 1) % PAGE + 1
            page = (k - 1) // PAGE
            pg = ('Integer.IsGreater(Container(%d).CurrentItem,%d) + !Integer.IsGreater(Container(%d).CurrentItem,%d)'
                  % (c, page * PAGE, c, (page + 1) * PAGE))
            for x in tpl[(slot - 1) * 6:slot * 6]:
                y = x.replace('Container(9401)', 'Container(%d)' % c).replace('Control.HasFocus(9401)', 'Control.HasFocus(%d)' % c)
                # old form: countnow gate; new form (rerun): the page gate of slot `slot` on page 0
                y = re.sub(r'Integer\.IsGreater\(Window\(Home\)\.Property\(aeon\.spot\.countnow\),\d+\)', pg, y)
                y = re.sub(r'Integer\.IsGreater\(Container\(%d\)\.CurrentItem,\d+\) \+ !Integer\.IsGreater\(Container\(%d\)'
                           r'\.CurrentItem,\d+\)' % (c, c), pg, y)
                y = re.sub(r'Integer\.IsEqual\(Container\(%d\)\.CurrentItem,%d\)' % (c, slot),
                           'Integer.IsEqual(Container(%d).CurrentItem,%d)' % (c, k), y)
                y = re.sub(r'Integer\.IsGreater\(Container\(%d\)\.NumItems,%d\)' % (c, slot - 1),
                           'Integer.IsGreater(Container(%d).NumItems,%d)' % (c, k - 1), y)
                assert pg in y, y[:200]
                out.append(y)
    t = t[:s] + '\n'.join(out) + '\n' + t[e:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('spotdots: %d lists x %d items, %d per page (%d controls)' % (len(LISTS), ITEMS, PAGE, len(out) - 1))


if __name__ == '__main__':
    main()
