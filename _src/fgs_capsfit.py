"""Which Skin settings names and categories do not fit in capitals (Figtree 24 bold, as focused) in the Fused Glass
style: name width = namefgs (namew + 87), categories 284. Prints the misses and the widths a condensed face would need.
Run from the skin folder: python _src/fgs_capsfit.py [face file in fonts/, default Figtree-Bold.ttf]"""
import io
import os
import re
import sys

from PIL import ImageFont

SK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
FACE = sys.argv[1] if len(sys.argv) > 1 else 'Figtree-Bold.ttf'
FONT = ImageFont.truetype(os.path.join(SK, 'fonts', FACE), 24)
po = io.open(os.path.join(SK, 'language', 'resource.language.en_gb', 'strings.po'), encoding='utf-8').read()
S = {}
for m in re.finditer(r'msgctxt "#(\d+)"\s*\nmsgid "(.*)"', po):
    S[int(m.group(1))] = m.group(2)


def text(v):
    v = re.sub(r'\$ADDON\[skin\.aeon\.fuse (\d+)\]', lambda m: S.get(int(m.group(1)), '?' + m.group(1)), v)
    return re.sub(r'\$LOCALIZE\[(\d+)\]', lambda m: S.get(int(m.group(1)), '?' + m.group(1)), v)


x = io.open(os.path.join(SK, '1080i', 'SkinSettings.xml'), encoding='utf-8').read()
miss = []
rows = 0
for m in re.finditer(r'<include content="Dlg_SkinRowChrome">(.*?)</include>', x, re.S):
    p = dict(re.findall(r'<param name="(\w+)" value="([^"]*)"/>', m.group(1)))
    lab = text(p.get('label', ''))
    if not lab or lab.startswith('$'):
        continue
    rows += 1
    room = int(p.get("namefgs", int(p.get("namew", 520)) + 101))
    need = FONT.getlength(lab.upper())
    if need > room:
        miss.append((int(need - room), p.get('id'), room, int(need), lab))
print('%s: %d rows measured, %d too long' % (FACE, rows, len(miss)))
for r in sorted(miss, reverse=True):
    print('  +%3d  id %s room %d need %d  %s' % r)
for m in re.finditer(r'<include content="Dlg_SkinCategory">(.*?)</include>', x, re.S):
    p = dict(re.findall(r'<param name="(\w+)" value="([^"]*)"/>', m.group(1)))
    lab = text(p.get('label', ''))
    need = FONT.getlength(lab.upper())
    if need > 284:
        print('  category +%d  %s (%d)' % (need - 284, lab, need))
