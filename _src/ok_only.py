# -*- coding: utf-8 -*-
"""0.51.0: Skin settings change only with OK / Enter (the user's wish: Left on a row used to step the value back, so
going back to the category list by Left could switch a setting off).

For every button in 1080i/SkinSettings.xml:
- an <onright> that changes something is dropped (a row with no <onclick> of its own gets it as its <onclick>);
- an <onleft> that changes something is dropped, and Left goes back to where it already went from the first value
  (SetFocus(<category list>)), else to the row's <onback> target.
Safe to run again; run it after any generator that writes Skin settings rows (ms_settings_row.py,
fg_artguard_rows.py). Prints what it changed. Run from the skin folder."""
import re
import sys

PATH = '1080i/SkinSettings.xml'
ACTION = re.compile(r'[ \t]*<(onleft|onright)((?: [^>]*)?)>([^<]*)</\1>\n?')
# 0.56.45 pickmode: moving the pick of an open row (SetProperty(aeon.pick,N,home)) changes nothing
NAV = re.compile(r'^\s*(SetFocus\([^)]*\)|-?\d+|noop|Dialog\.Close\([^)]*\)|Back|Action\(Back\)|SetProperty\(aeon\.pick,\d+,home\))\s*$')


def fix_button(block, stats):
    actions = list(ACTION.finditer(block))
    changing = [m for m in actions if not NAV.match(m.group(3))]
    if not changing:
        return block
    stats['buttons'] += 1
    has_click = '<onclick' in block
    nav_left = [m for m in actions if m.group(1) == 'onleft' and NAV.match(m.group(3))]
    out = block
    for m in changing:
        if m.group(1) == 'onright' and not has_click:
            out = out.replace(m.group(0), m.group(0).replace('<onright', '<onclick').replace('</onright>', '</onclick>'), 1)
            stats['to_click'] += 1
        else:
            out = out.replace(m.group(0), '', 1)
            stats['dropped'] += 1
    if any(m.group(1) == 'onleft' for m in changing):
        targets = {m.group(3).strip() for m in nav_left}
        for m in nav_left:
            out = out.replace(m.group(0), '', 1)
        if len(targets) == 1:
            target = targets.pop()
        else:
            back = re.search(r'<onback>([^<]*)</onback>', out)
            target = back.group(1).strip() if back else 'noop'
        indent = re.search(r'\n([ \t]*)<on(?:click|up|down|back)', out)
        line = '%s<onleft>%s</onleft>\n' % (indent.group(1) if indent else '\t\t\t\t\t', target)
        anchor = re.search(r'[ \t]*<onback>[^<]*</onback>\n', out) or re.search(r'[ \t]*<ondown>[^<]*</ondown>\n', out)
        if anchor:
            out = out[:anchor.end()] + line + out[anchor.end():]
        else:
            out = out.replace('</control>', line + '</control>', 1)
        stats['left_nav'] += 1
    return out


def main():
    text = open(PATH, encoding='utf-8').read()
    stats = {'buttons': 0, 'dropped': 0, 'to_click': 0, 'left_nav': 0}
    text2 = re.sub(r'<control type="button"[^>]*>.*?</control>', lambda m: fix_button(m.group(0), stats), text, flags=re.S)
    left = [m.group(0).strip() for m in ACTION.finditer(text2) if not NAV.match(m.group(3))]
    if text2 != text:
        open(PATH, 'w', encoding='utf-8', newline='\n').write(text2)
    print(stats, 'left over:', len(left))
    for x in left[:10]:
        print('  ', x[:160])
    return 0


if __name__ == '__main__':
    sys.exit(main())
