"""0.56.49 Color needs KarmaMole (the user, 2026-11-18: "If Karmamole's helper is not installed, then colors is not an
option for backgrounds or corner boxes").

Every colour look comes from script.karmamole.helper (the helper's sync_karmamole: aeon.boxcol / aeon.artcol /
aeon.wash, and Groove.Art.Soft). Without it a Color choice falls back: Colors corner boxes = the Neutral accent, the
Color screensaver / spotlight / widget screens = the fanart, the Color library background = the plain dark ground.
So without KarmaMole (System.AddonIsEnabled(script.karmamole.helper) false) Color is not offered:

- Skin settings rows 9736 Screensaver background, 9745 Library background, 9747 Corner boxes, 9753 Spotlight
  background, 9756 Widget screens: the Color pill is gone, the other pills share the row; a Color already chosen shows
  (and opens) as the look it falls back to; Left / Right do not reach Color
- View settings (Library panel): Background and Corner boxes skip Color when cycling
- Spotlight options (1162) and the section editor (1163): Color is skipped
- setup wizard steps 16 (corner boxes) and 30 (library background): the Color card is hidden, the marks and positions
  follow

Run from the skin folder after the settings generators, pickmode_05645.py, renav and ok_only.py, and after
wizard_05640.py. Repeatable."""
import io
import os
import re

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
KM = 'System.AddonIsEnabled(script.karmamole.helper)'
P = 'Window(Home).Property(aeon.pick)'
# row: (Color's option index, the option it falls back to)
ROWS = {9736: (2, 1), 9745: (2, 0), 9747: (0, 1), 9753: (2, 1), 9756: (2, 1)}


def rd(name):
    return io.open(os.path.join(X, name), encoding='utf-8').read()


def wr(name, t):
    io.open(os.path.join(X, name), 'w', encoding='utf-8', newline='\n').write(t)


def row(t, rid, color, eff):
    e = 'String.IsEqual(Window(Home).Property(aeon.pickrow),%d)' % rid
    b0 = t.index('<control type="button" id="%d">' % rid)
    b1 = t.index('</control>', b0)
    btn = t[b0:b1]
    if KM in btn:
        return t, 'done'
    opens = {int(j): c for c, j in re.findall(r'<onclick condition="!%s \+ (.*?)">SetProperty\(aeon\.pick,(\d+),home\)</onclick>'
                                             % re.escape(e), btn)}
    n = len(opens)
    assert sorted(opens) == list(range(n)) and 'color' in opens[color] and color in (0, n - 1), (rid, opens)
    cc, ce = opens[color], opens[eff]
    # Left / Right never reach Color
    nb, tag = (color - 1, 'onright') if color == n - 1 else (color + 1, 'onleft')
    old = '<%s condition="%s + String.IsEqual(%s,%d)">SetProperty(aeon.pick,%d,home)</%s>' % (tag, e, P, nb, color, tag)
    assert btn.count(old) == 1, (rid, old)
    btn = btn.replace(old, old.replace('%d)">' % nb, '%d) + %s">' % (nb, KM), 1) +
                      '\n\t\t\t\t\t<%s condition="%s + String.IsEqual(%s,%d) + !%s">noop</%s>' % (tag, e, P, nb, KM, tag))
    # a Color already chosen opens on the look it falls back to (the later SetProperty wins: Kodi checks every
    # condition first, then runs the actions in order)
    o = '<onclick condition="!%s + %s">SetProperty(aeon.pick,%d,home)</onclick>' % (e, cc, color)
    assert btn.count(o) == 1, (rid, o)
    btn = btn.replace(o, o + '\n\t\t\t\t\t<onclick condition="!%s + %s + !%s">SetProperty(aeon.pick,%d,home)</onclick>' % (e, cc, KM, eff))
    t = t[:b0] + btn + t[b1:]
    # the pills
    b1 = t.index('</control>', b0)
    end = t.index('\n\t</control>', b1)
    seg = t[b1:end]
    lines = seg.split('\n')
    pill = re.compile(r'<left>(\d+)</left><top>13</top><width>(\d+)</width>.*Property\(aeon\.pick\),(\d+)\)\]\]')
    opts, idx = {}, []
    for i, l in enumerate(lines):
        m = pill.search(l)
        if m:
            j = int(m.group(3))
            opts.setdefault(j, (int(m.group(1)), int(m.group(2))))
            idx.append((i, j))
    assert sorted(opts) == list(range(n)), (rid, opts)
    x0 = min(a for a, _w in opts.values())
    x1 = max(a + w for a, w in opts.values())
    keep = [j for j in range(n) if j != color]
    spare = opts[color][1]
    total = float(sum(opts[j][1] for j in keep))
    geo, x = {}, x0
    for k, j in enumerate(keep):
        w = opts[j][1] + int(round(spare * opts[j][1] / total))
        if k == len(keep) - 1:
            w = x1 - x
        geo[j] = (x, w)
        x += w
    copies = []
    for i, j in idx:
        l = lines[i]
        vis = re.search(r'<visible>(.*)</visible>', l).group(1)
        lines[i] = l.replace('<visible>%s</visible>' % vis, '<visible>[%s] + %s</visible>' % (vis, KM))
        if j == color:
            continue
        a, w = opts[j]
        c = l.replace('<left>%d</left>' % a, '<left>%d</left>' % geo[j][0], 1).replace('<width>%d</width>' % w, '<width>%d</width>' % geo[j][1], 1)
        v2 = vis
        if j == eff:
            assert ('!%s + %s' % (e, ce)) in v2, (rid, j)
            v2 = v2.replace('!%s + %s' % (e, ce), '!%s + [%s | %s]' % (e, ce, cc))
        copies.append(c.replace('<visible>%s</visible>' % vis, '<visible>[%s] + !%s</visible>' % (v2, KM)))
    last = max(i for i, _j in idx)
    indent = re.match(r'\s*', lines[last]).group(0)
    lines[last + 1:last + 1] = [indent + '<!-- 0.56.49 karma: without KarmaMole, no Color -->'] + [indent + c.strip() for c in copies]
    return t[:b1] + '\n'.join(lines) + t[end:], 'ok'


def settings():
    t = rd('SkinSettings.xml')
    out = []
    for rid, (color, eff) in sorted(ROWS.items()):
        t, how = row(t, rid, color, eff)
        out.append('%d %s' % (rid, how))
    wr('SkinSettings.xml', t)
    return out


def panel():
    """View settings: Background (fanart -> color -> default) and Corner boxes (default -> colors -> neutral)"""
    t = rd('Includes_LibraryPanel.xml')
    if KM in t:
        return 'done'
    base = '$INFO[Window(Home).Property(aeon.vo.base)]'
    a = ('<onclick condition="String.IsEqual(Window(Home).Property(aeon.vo.bg),fanart)">Skin.SetString(%sbg,color)</onclick>' % base)
    b = ('<onclick condition="String.IsEmpty(Window(Home).Property(aeon.vo.boxbg))">Skin.SetString(%sboxbg,colors)</onclick>' % base)
    assert t.count(a) == 1 and t.count(b) == 1
    ind = '\n' + '\t' * 6
    t = t.replace(a, a.replace(',fanart)">', ',fanart) + %s">' % KM) + ind +
                  '<onclick condition="String.IsEqual(Window(Home).Property(aeon.vo.bg),fanart) + !%s">Skin.Reset(%sbg)</onclick>' % (KM, base))
    t = t.replace(b, b.replace('aeon.vo.boxbg))">', 'aeon.vo.boxbg)) + %s">' % KM) + ind +
                  '<onclick condition="String.IsEmpty(Window(Home).Property(aeon.vo.boxbg)) + !%s">Skin.SetString(%sboxbg,neutral)</onclick>' % (KM, base))
    wr('Includes_LibraryPanel.xml', t)
    return 'ok'


def spotlight():
    out = []
    t = rd('Custom_1162_SpotlightOptions.xml')
    a = ('<onclick condition="String.IsEmpty(Skin.String(aeon.wsbg)) | String.IsEqual(Skin.String(aeon.wsbg),fanart)">'
         'Skin.SetString(aeon.wsbg,color)</onclick>')
    if KM not in t:
        assert t.count(a) == 1
        t = t.replace(a, a.replace('condition="String.IsEmpty(Skin.String(aeon.wsbg)) | String.IsEqual(Skin.String(aeon.wsbg),fanart)"',
                                   'condition="[String.IsEmpty(Skin.String(aeon.wsbg)) | String.IsEqual(Skin.String(aeon.wsbg),fanart)] + %s"' % KM) +
                      '\n\t\t\t<onclick condition="[String.IsEmpty(Skin.String(aeon.wsbg)) | String.IsEqual(Skin.String(aeon.wsbg),fanart)] + !%s">'
                      'Skin.SetString(aeon.wsbg,neutral)</onclick>' % KM)
        wr('Custom_1162_SpotlightOptions.xml', t)
        out.append('1162 ok')
    t = rd('Custom_1163_Spotlight.xml')
    if KM not in t:
        pat = re.compile(r'(\t*)<onclick condition="([^"]*)">Skin\.SetString\((aeon\.vbg\.[a-z0-9]+),color\)</onclick>')
        t, k = pat.subn(lambda m: '%s<onclick condition="%s + %s">Skin.SetString(%s,color)</onclick>\n%s<onclick condition="%s + !%s">Skin.Reset(%s)</onclick>'
                        % (m.group(1), m.group(2), KM, m.group(3), m.group(1), m.group(2), KM, m.group(3)), t)
        assert k == 13, k
        wr('Custom_1163_Spotlight.xml', t)
        out.append('1163 %d' % k)
    return out


def wizard():
    t = rd('Custom_1173_SetupWizard.xml')
    out = []
    for act in ('<onclick>Skin.Reset(aeon.boxbg)</onclick>', '<onclick>Skin.SetString(aeon.vbg,color)</onclick>'):
        i = t.index(act)
        s = t.rindex('<item>', 0, i)
        if KM in t[s:i]:
            continue
        lab = t.index('</label>', s) + len('</label>')
        t = t[:lab] + '\n\t\t\t\t\t\t<visible>%s</visible>' % KM + t[lab:]
        out.append('card')
    wr('Custom_1173_SetupWizard.xml', t)
    w = rd('Includes_Aeon_Wizard.xml')
    box = '[String.IsEmpty(Skin.String(aeon.boxbg)) | String.IsEqual(Skin.String(aeon.boxbg),colors) | String.IsEqual(Skin.String(aeon.boxbg),neutral)]'
    adds = {
        'Wiz_Cur_16': ['<value condition="!%s + %s">neutral</value>' % (KM, box)],
        'Wiz_Pos_16': ['<value condition="!%s + %s">$NUMBER[0]</value>' % (KM, box),
                       '<value condition="!%s + String.IsEqual(Skin.String(aeon.boxbg),fanart)">$NUMBER[1]</value>' % KM,
                       '<value condition="!%s + String.IsEqual(Skin.String(aeon.boxbg),follow)">$NUMBER[2]</value>' % KM],
        'Wiz_Cur_30': ['<value condition="!%s + String.IsEqual(Skin.String(aeon.vbg),color)">default</value>' % KM],
        'Wiz_Pos_30': ['<value condition="!%s + String.IsEqual(Skin.String(aeon.vbg),color)">$NUMBER[0]</value>' % KM],
    }
    for name, vals in adds.items():
        head = '<variable name="%s">\n' % name
        i = w.index(head) + len(head)
        if KM in w[i:w.index('</variable>', i)]:
            continue
        w = w[:i] + ''.join('\t\t%s\n' % v for v in vals) + w[i:]
        out.append(name)
    wr('Includes_Aeon_Wizard.xml', w)
    return out


def boxart_row():
    """row 9526 Box colors from artwork (aeon.nopalette): the helper colours boxes only with KarmaMole
    (service.sync_karmamole: boxes = installed and not nopalette), so the row shows only with it; Up / Down of the
    Libraries list written again (settings_rows.renav)"""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import settings_rows as sr
    t = rd('SkinSettings.xml')
    s, e = sr.item_span(t, 9526)
    if KM in t[s:e][:400]:
        return 'done'
    old = re.search(r'<visible>(.*?)</visible>', t[s:e][:400])
    cond = KM if not old or 'Control.HasFocus' in old.group(1) else '[%s] + %s' % (old.group(1), KM)
    t = sr.set_item_visible(t, 9526, cond)
    t = sr.renav(t, 9777)
    wr('SkinSettings.xml', t)
    return 'ok'


PREVIEW_ROWS = (9736, 9745, 9747, 9753, 9756)
CTL = re.compile(r'<control type="(?:image|label)"><left>(\d+)</left><top>(\d+)</top><width>(\d+)</width>.*?</control>')


def previews():
    """the preview card beside each row lists every look with its share ('Color 67 %'): without KarmaMole the Color
    line (its picture, name, share and marks) goes too"""
    t = rd('SkinSettings.xml')
    out = []
    for rid in PREVIEW_ROWS:
        head = '<control type="group"><visible>Control.HasFocus(%d)</visible>' % rid
        if head not in t:
            continue
        a = t.index(head)
        b = t.index('\n', a)
        line = t[a:b]
        if KM in line:
            out.append('%d done' % rid)
            continue
        lab = re.search(r'<control type="label"><left>70</left><top>(\d+)</top><width>120</width>(?:(?!</control>).)*?<label>\$LOCALIZE\[(?:31680|31551)\]</label>', line)
        if not lab:
            continue
        top = int(lab.group(1))

        def hide(m):
            left, y, w = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if not (16 <= left and w < 248 and top - 2 <= y <= top + 20):
                return m.group(0)
            c = m.group(0)
            v = re.search(r'<visible>(.*?)</visible>', c)
            if v:
                return c.replace(v.group(0), '<visible>[%s] + %s</visible>' % (v.group(1), KM))
            return c[:-len('</control>')] + '<visible>%s</visible></control>' % KM
        new, k = CTL.subn(hide, line)
        t = t[:a] + new + t[b:]
        out.append('%d %d' % (rid, sum(1 for x, y in zip(CTL.finditer(line), CTL.finditer(new)) if x.group(0) != y.group(0))))
    wr('SkinSettings.xml', t)
    return out


def main():
    print('karma:', settings(), panel(), spotlight(), wizard(), boxart_row(), previews())


if __name__ == '__main__':
    main()
