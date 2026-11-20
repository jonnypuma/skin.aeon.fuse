"""0.52.4 Skin settings > Motion, memory, reset > Progress bar updates per second (row 9763): narrower pills, so the
longer label (the user asked for "Progress bar updates per second" instead of "Updates per second") ends left of them
in every language. Track x 454-860 -> 506-860; Screen 140 -> 136 px (Czech "Obrazovka", the widest, is 112 px), the
numbers 64 -> 52 px ("60" is 28 px). Labels: _src/smoothprog_rate_strings.py. Run from the skin folder; runs once."""
import io

SET = '1080i/SkinSettings.xml'
# (left, width) before -> after, inside row 9763 only
MOVES = [((454, 406), (506, 354)), ((458, 140), (510, 136)), ((598, 64), (646, 52)), ((662, 64), (698, 52)),
         ((726, 64), (750, 52)), ((790, 64), (802, 52))]

s = io.open(SET, encoding='utf-8').read()
start = s.index('<param name="id" value="9763"/>')
gs = s.rindex('<control type="group">', 0, start)
ge = s.index('\n\t\t\t</control>\n', start) + 1
row = s[gs:ge]
if '<left>506</left>' not in row:
    for (x0, w0), (x1, w1) in MOVES:
        old = '<left>%d</left><top>13</top><width>%d</width>' % (x0, w0)
        new = '<left>%d</left><top>13</top><width>%d</width>' % (x1, w1)
        n = row.count(old)
        assert n == (2 if x0 == 454 else 6), (x0, n)
        row = row.replace(old, new)
    s = s[:gs] + row + s[ge:]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)
print(sorted(set(int(x) for x in __import__('re').findall(r'<left>(\d+)</left><top>13</top>', row))))
