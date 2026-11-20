"""0.56.39 Panel shadow = how high a panel floats (the user, 2026-11-17: "panel shadow should be ... increasing the size of
the shadow underneath a panel so it seems it is raised higher, nothing to do with outline").

Before, the four strengths mostly changed the shadow's darkness and Heavy added a lit rim, so the preview showed no
difference but Heavy's outline. Now:
- every panel shadow image (colordiffuse $VAR[FG_PanelSh_xx], 111 of them) picks its picture from the strength: the
  shadow pictures are hollow rings (clear where the glass panel is) or soft solid shapes; each gets a Mild / Strong /
  Heavy version (fg/<name>_<strength>.png): the panel's shape dropped and blurred, the hole kept exactly where the
  panel is: Mild tight, Strong wider and lower, Heavy widest and lowest, so the panel seems to float higher (a first
  try zoomed the ring, which moved its hole off the panel);
- the darkness follows: Mild x0.8, Strong x1.4, Heavy x1.75 of Medium (at most e6): on a busy picture a higher
  panel's shadow has to read as one;
- no rim: FG_Edge / FG_EdgeM lose Heavy's lit edge;
- the dialog panels' baked shadows (dialogs/panel_fg*_sh{mild,strong,heavy}.png) are drawn again the same way: the
  panel's shape blurred and dropped inside the picture's 40-px margin (Medium = the picture as it was);
- fg_material.py and expert_05628.py write the same from now on.
Run from the skin folder after fg_material / expert_05628 (and before skin_previews' re-run). Repeatable."""
import io
import os
import re

from PIL import Image, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, '1080i')
SH = 'String.IsEqual(Skin.String(aeon.fgshadow),%s)'
LIFT = (('mild', -4, 2), ('strong', 10, 10), ('heavy', 22, 20))
SHARE = {'mild': (99, 1), 'strong': (103, 10), 'heavy': (106, 20)}        # size from the group: percent, drop
OPACITY = {'mild': 0.8, 'strong': 1.4, 'heavy': 1.75}
TAG = '<!-- lift -->'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


TEXTURES = ('sho14', 'sho18', 'sho20', 'sho24', 'sho28', 'sho32', 'sh24', 'sh32', 'hb_sm', 'hb_csh', 'hb_sr', 'hb_sl')
# per strength, relative to the ring's margin m (image edge to the panel): blur sigma, drop, darkness of the ring
LOOK = {'mild': (0.20, 0.06, 0.85), 'strong': (0.32, 0.30, 1.2), 'heavy': (0.40, 0.50, 1.4)}
RING_PEAK = {'mild': 0.7, 'strong': 1.0, 'heavy': 1.0}      # a ring's darkness (the blur gives half of it at the panel's edge)


def hole(im):
    """the panel's area in a hollow shadow ring: the clear pixels joined to the centre (None for a solid shadow)"""
    w, h = im.size
    a = im.split()[3].load()
    if a[w // 2, h // 2] > 8:
        return None
    seen = set()
    stack = [(w // 2, h // 2)]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or x < 0 or y < 0 or x >= w or y >= h or a[x, y] > 8:
            continue
        seen.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return seen


def variants():
    """fg/<name>_{mild,strong,heavy}.png: the panel's shape (a ring's hole, or the solid shadow itself) dropped and
    blurred, the ring's hole kept clear so the glass is not darkened; the strength is in the size and the drop"""
    for name in TEXTURES:
        src = os.path.join(ROOT, 'media', 'fg', name + '.png')
        if not os.path.isfile(src):
            continue
        im = Image.open(src).convert('RGBA')
        w, h = im.size
        hl = hole(im)
        a0 = im.split()[3]
        if hl:
            shape = Image.new('L', im.size, 0)
            sp = shape.load()
            for x, y in hl:
                sp[x, y] = 255
            col = [y for y in range(h) if (w // 2, y) in hl]
            m = min(col) if col else h // 4
        else:
            shape = a0
            m = max(4, min(w, h) // 4)
        for look, (ks, kd, kp) in LOOK.items():
            sigma, drop = max(1.0, ks * m), int(round(kd * m))
            moved = Image.new('L', im.size, 0)
            moved.paste(shape, (0, drop))
            blur = moved.filter(ImageFilter.GaussianBlur(sigma)).load()
            out = Image.new('RGBA', im.size, (0, 0, 0, 0))
            op = out.load()
            peak = RING_PEAK[look] if hl else kp
            for y in range(h):
                for x in range(w):
                    if hl and (x, y) in hl:
                        continue
                    op[x, y] = (0, 0, 0, min(255, int(round(blur[x, y] * peak))))
            out.save(os.path.join(ROOT, 'media', 'fg', '%s_%s.png' % (name, look)), optimize=True)
    print('shadow pictures done')


IMG = re.compile(r'<control type="image">((?:(?!<control).)*?\$VAR\[FG_PanelSh_(?:(?!<control).)*?)</control>', re.S)
UNLIFT = re.compile(r'<!-- lift -->(?:<animation type="Conditional" condition="String\.IsEqual\(Skin\.String\(aeon\.fgshadow\),(?:mild|strong|heavy)\)">.*?</animation>)+', re.S)


def lift_all():
    """every panel shadow picks its picture from the strength ($VAR[FG_Sh_<name>]); the 0.56.39 first try's zoom
    (it scaled a ring's hole away from its panel) comes out"""
    total = 0
    for fn in sorted(os.listdir(D)):
        if not fn.endswith('.xml') or fn == 'Font.xml':
            continue
        t = rd(fn)
        n = [0]

        def sub(m):
            b = UNLIFT.sub('', m.group(1))
            for name in TEXTURES:
                b2 = b.replace('>fg/%s.png<' % name, '>$VAR[FG_Sh_%s]<' % name)
                if b2 != b:
                    n[0] += 1
                    b = b2
            return '<control type="image">' + b + '</control>'
        new = IMG.sub(sub, t)
        if new != t:
            wr(fn, new)
            print('%-28s %d shadows' % (fn, n[0]))
            total += n[0]
    t = rd('Includes_Fused.xml')
    if 'name="FG_Sh_sho28"' not in t:
        block = '\t<!-- 0.56.39 Panel shadow: the shadow picture of each strength (shadow_lift_05639) -->\n'
        for name in TEXTURES:
            block += ('\t<variable name="FG_Sh_%s">\n' % name +
                      ''.join('\t\t<value condition="%s">fg/%s_%s.png</value>\n' % (SH % k, name, k) for k in ('heavy', 'strong', 'mild')) +
                      '\t\t<value>fg/%s.png</value>\n\t</variable>\n' % name)
        t = t.replace('\t<include name="FGS_RowTex">', block + '\t<include name="FGS_RowTex">', 1)
        wr('Includes_Fused.xml', t)
    print('switched', total)


def variables():
    t = rd('Includes_Fused.xml')
    t = t.replace('\t\t<value condition="%s">66ffffff</value>\n' % (SH % 'heavy'), '')
    t = t.replace('<variable name="FG_EdgeM">\n\t\t<value condition="%s">4dffffff</value>\n' % (SH % 'heavy'), '<variable name="FG_EdgeM">\n')

    def rebuild(m):
        a = m.group(1)
        base = int(a, 16)
        lines = ''.join('\t\t<value condition="%s">%02x000000</value>\n' % (SH % k, min(0xe6, int(round(base * OPACITY[k]))))
                        for k in ('heavy', 'strong', 'mild'))
        return '<variable name="FG_PanelSh_%s">\n%s\t\t<value>%s000000</value>\n\t</variable>' % (a, lines, a)
    t = re.sub(r'<variable name="FG_PanelSh_([0-9a-f]{2})">.*?</variable>', rebuild, t, flags=re.S)
    wr('Includes_Fused.xml', t)
    print('variables done')


def sources():
    p = os.path.join(ROOT, '_src', 'fg_material.py')
    s = io.open(p, encoding='utf-8').read()
    s = s.replace("        '\\t\\t<value condition=\"%s\">66ffffff</value>\\n'\n        '\\t\\t<value condition=\"%s\">33ffffff</value>\\n'\n        '\\t\\t<value condition=\"%s\">26ffffff</value>\\n'\n        '\\t\\t<value>1fffffff</value>\\n\\t</variable>\\n' % (SH % 'heavy', IS('frost'), IS('clear')) +      # 0.56.28: Heavy's lit rim",
                  "        '\\t\\t<value condition=\"%s\">33ffffff</value>\\n'\n        '\\t\\t<value condition=\"%s\">26ffffff</value>\\n'\n        '\\t\\t<value>1fffffff</value>\\n\\t</variable>\\n' % (IS('frost'), IS('clear')) +      # 0.56.39: no rim (shadow_lift_05639)")
    s = s.replace("'\\t<variable name=\"FG_EdgeM\">\\n\\t\\t<value condition=\"%s\">4dffffff</value>\\n\\t\\t<value>1fffffff</value>\\n\\t</variable>\\n' % (SH % 'heavy') +",
                  "'\\t<variable name=\"FG_EdgeM\">\\n\\t\\t<value>1fffffff</value>\\n\\t</variable>\\n' +")
    s = s.replace("''.join('\\t<variable name=\"FG_PanelSh_%s\">\\n\\t\\t<value condition=\"%s\">e6000000</value>\\n'",
                  "''.join('\\t<variable name=\"FG_PanelSh_%s\">\\n\\t\\t<value condition=\"%s\">%02x000000</value>\\n'")
    s = s.replace("% (a, SH % 'heavy', SH % 'strong', min(0xd9, int(int(a, 16) * 1.6)), SH % 'mild', int(int(a, 16) * 0.5), a)",
                  "% (a, SH % 'heavy', min(0xe6, int(round(int(a, 16) * 1.3))), SH % 'strong', min(0xe6, int(round(int(a, 16) * 1.15))), SH % 'mild', min(0xe6, int(round(int(a, 16) * 0.8))), a)")
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    p = os.path.join(ROOT, '_src', 'expert_05628.py')
    s = io.open(p, encoding='utf-8').read()
    s = s.replace("SHADES = {'mild': (0.5, None), 'strong': (1.6, None), 'heavy': (2.0, 0.55)}",
                  "SHADES = {'mild': (0.5, None), 'strong': (1.6, None), 'heavy': (2.0, None)}   # 0.56.39: drawn again by shadow_lift_05639 (size, not darkness)")
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('sources done')


# the dialog panels: the panel's shape blurred and dropped (sigma, drop, peak alpha) inside the 40-px margin
DLG = {'mild': (5, 2, 0.42), 'strong': (11, 9, 0.62), 'heavy': (15, 15, 0.72)}
PANELS = {'panel_fg': ((26, 29, 36), 0.94, 0.227), 'panel_fgg': ((23, 26, 32), 0xc8 / 255.0, 0.20),
          'panel_fgf': ((30, 33, 41), 0xb3 / 255.0, 0.30)}


def dialog_panels():
    base = Image.open(os.path.join(ROOT, 'media', 'dialogs', 'panel_fg.png')).convert('RGBA')
    bp = base.load()
    w, h = base.size
    mask = Image.new('L', base.size, 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = bp[x, y]
            if (r, g, b) != (0, 0, 0):
                mp[x, y] = a
    for shname, (sigma, drop, peak) in DLG.items():
        sh = Image.new('L', base.size, 0)
        sh.paste(mask, (0, drop))
        sh = sh.filter(ImageFilter.GaussianBlur(sigma))
        sp = sh.load()
        for name, (fill, alpha, edge) in PANELS.items():
            out = Image.new('RGBA', base.size)
            op = out.load()
            for y in range(h):
                for x in range(w):
                    r, g, b, a = bp[x, y]
                    if (r, g, b) == (0, 0, 0) or a == 0:
                        op[x, y] = (0, 0, 0, min(255, int(round(sp[x, y] * peak))))
                    elif (r, g, b) == (26, 29, 36):
                        op[x, y] = fill + (int(round(a / 0.94 * alpha)),)
                    else:
                        lit = tuple(int(round(c + (255 - c) * edge)) for c in fill)
                        op[x, y] = lit + (int(round(a / 0.94 * max(alpha, 0.5))),)
            out.save(os.path.join(ROOT, 'media', 'dialogs', '%s_sh%s.png' % (name, shname)), optimize=True)
    print('dialog panels done')


if __name__ == '__main__':
    variants()
    lift_all()
    variables()
    sources()
    dialog_panels()
