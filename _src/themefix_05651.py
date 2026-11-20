"""0.56.51 Skin settings > Theme & style > Theme (row 9744) could only set Aeon Glass (the user, 2026-11-18: "I try to
click OK on Fused Glass and the focus jumps to Aeon Glass and nothing happens"). Since 0.56.45 (choose mode,
pickmode_05645.plan_theme) all three pills ran RunScript(script.aeon.helper,theme,glass): the theme was guessed from
the word "glass" in each pill's condition, and aeon.vglass and aeon.fglass both contain it. Now each pill sets its own
theme (pick 0 Aeon = aeon, 1 Aeon Glass = glass, 2 Fused Glass = fused; the helper's swap.py theme names), checked
against the pill's condition; plan_theme uses pickmode_05645.theme_key from now on. Run from the skin folder. Repeatable."""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pickmode_05645 as pm  # noqa: E402

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'SkinSettings.xml')
LINE = re.compile(r'<onclick condition="String\.IsEqual\(Window\(Home\)\.Property\(aeon\.pickrow\),9744\) \+ '
                  r'String\.IsEqual\(Window\(Home\)\.Property\(aeon\.pick\),(\d)\) \+ !\[(.*?)\]">'
                  r'RunScript\(script\.aeon\.helper,theme,(\w+)\)</onclick>')
WANT = ['aeon', 'glass', 'fused']


def main():
    t = io.open(P, encoding='utf-8').read()
    found = []

    def fix(m):
        j, cond, now = int(m.group(1)), m.group(2), m.group(3)
        key = pm.theme_key(cond)
        assert key == WANT[j], (j, cond, key)
        found.append((j, now, key))
        return m.group(0).replace('theme,%s)' % now, 'theme,%s)' % key)
    t2 = LINE.sub(fix, t)
    assert sorted(j for j, _n, _k in found) == [0, 1, 2], found
    # one theme switch reloads the skin twice, 4 s apart (box log 23:56:26 / 23:56:30): the first reload put the focus
    # back and cleared the note, the second fell to the category list. The note now clears 8 s after the window opens.
    clear = '\t<onload>ClearProperty(aeon.skinback,home)</onload>\n'
    later = ('\t<onload>CancelAlarm(aeonskinback,true)</onload>\n'
             '\t<onload>AlarmClock(aeonskinback,ClearProperty(aeon.skinback,home),00:08,silent)</onload>\n')
    if clear in t2:
        t2 = t2.replace(clear, later, 1)
    assert later in t2
    # a pending clear (the settings opened less than 8 s before) must not take the note of the row just set
    t2, k = re.subn(r'(\s*)<onclick condition="([^"]*)">SetProperty\(aeon\.skinback,(\d+),home\)</onclick>(?!\s*<onclick condition="[^"]*">CancelAlarm)',
                    lambda m: '%s<onclick condition="%s">SetProperty(aeon.skinback,%s,home)</onclick>%s<onclick condition="%s">CancelAlarm(aeonskinback,true)</onclick>'
                    % (m.group(1), m.group(2), m.group(3), m.group(1), m.group(2)), t2)
    t2, k2 = re.subn(r'<onclick>SetProperty\(aeon\.skinback,(\d+),home\)</onclick>(?!<onclick>CancelAlarm)',
                     r'<onclick>SetProperty(aeon.skinback,\1,home)</onclick><onclick>CancelAlarm(aeonskinback,true)</onclick>', t2)
    print('themefix: %d rows that reload cancel the pending clear' % (k + k2))
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t2)
    print('themefix:', ', '.join('pick %d %s -> %s' % f for f in sorted(found)))


if __name__ == '__main__':
    main()
