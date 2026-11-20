# -*- coding: utf-8 -*-
"""0.56.6 Skin settings > Backgrounds > Home vignette (row 9733): Off | Light | Medium | Strong | Heavy.

The user (2026-11-16): "the home vignette strong, is a bit too strong, i want something in the middle from Medium and
strong ... Perhaps it should be called strong and the strong we have now shall be called Heavy and be the strongest".
Skin.String(aeon.vignette): a Off, b Light, c Medium (default), e Strong (new, between), d Heavy (the old Strong, so a
stored d keeps its look). OK steps a > b > c > e > d > a.
  - Aeon_VignetteCol: Light 55, Medium 99, Strong cc, Heavy ff (alpha of the vignette picture, Round or Side)
  - Aeon_VignetteLow: Off 70, Light 88, Medium a0, Strong b0, Heavy c0 (the scrim under the Home rows)
The pill stays 394..860 (the row's name needs the room on its left in Polish and German, which is why the first five-choice
try in 0.56.0 was taken out); five choices inside it: Off 80, Light 86, Medium 102, Strong 94, Heavy 96.
String 32603 Heavy, all languages. Run from the skin folder; safe to run again."""
import io
import os
import re

SP = os.path.join('1080i', 'SkinSettings.xml')
SUB = os.path.join('1080i', 'Includes_Aeon_Sub.xml')
HEAVY = 32603
TR = {'cs_cz': u'Těžké', 'da_dk': u'Kraftig', 'de_de': u'Intensiv', 'el_gr': u'Βαρύ', 'es_es': u'Intenso', 'fi_fi': u'Voimakas',
      'fr_fr': u'Intense', 'hu_hu': u'Intenzív', 'it_it': u'Intenso', 'ja_jp': u'最強', 'ko_kr': u'아주 강하게', 'nb_no': u'Kraftig',
      'nl_nl': u'Intens', 'pl_pl': u'Ciężki', 'pt_br': u'Intenso', 'pt_pt': u'Intenso', 'ru_ru': u'Плотный', 'sv_se': u'Kraftig',
      'tr_tr': u'Yoğun', 'uk_ua': u'Щільний', 'zh_cn': u'最强', 'zh_tw': u'最強'}
V = 'Skin.String(aeon.vignette)'
# (value, label, left, width): the five choices left to right
SEGS = (('a', '$LOCALIZE[31548]', 398, 80), ('b', '$LOCALIZE[31672]', 478, 86), ('c', '$LOCALIZE[31071]', 564, 102),
        ('e', '$LOCALIZE[31673]', 666, 94), ('d', '$ADDON[skin.aeon.fuse %d]' % HEAVY, 760, 96))
OLD = {'a': (398, 104), 'b': (502, 104), 'c': (606, 132), 'd': (738, 116)}


def strings():
    for lang in sorted(os.listdir('language')):
        k = lang[len('resource.language.'):]
        p = os.path.join('language', lang, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        entry = u'msgctxt "#%d"\nmsgid "Heavy"\nmsgstr "%s"\n' % (HEAVY, '' if k == 'en_gb' else TR[k])
        m = re.search(r'msgctxt "#%d"\nmsgid "[^\n]*"\nmsgstr "[^\n]*"\n' % HEAVY, t)
        t = t[:m.start()] + entry + t[m.end():] if m else t.rstrip('\n') + '\n\n' + entry
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('string %d in %d languages' % (HEAVY, len(os.listdir('language'))))


def group_of(t, cid):
    i = t.find('<control type="button" id="%d">' % cid)
    g = t.rfind('<control type="group">', 0, i)
    depth = 0
    for m in re.finditer(r'<control[ >]|</control>', t[g:]):
        depth += -1 if m.group(0) == '</control>' else 1
        if depth == 0:
            return g, g + m.end()


def row():
    t = io.open(SP, encoding='utf-8').read()
    g, e = group_of(t, 9733)
    c = t[g:e]
    if 'vignette),e)' in c:
        print('row 9733 already has five choices')
        return
    lines = c.split('\n')
    seg = {v: [l for l in lines if '<left>%d</left><top>13</top><width>%d</width>' % OLD[v] in l] for v in OLD}
    assert all(len(seg[v]) == 6 for v in OLD), {v: len(seg[v]) for v in seg}
    first = lines.index(seg['a'][0])
    keep = [l for l in lines if not any(l in seg[v] for v in OLD)]
    new = []
    for v, label, x, w in SEGS:
        src = seg['d' if v == 'e' else v]
        for l in src:
            l = l.replace('<left>%d</left><top>13</top><width>%d</width>' % OLD['d' if v == 'e' else v], '<left>%d</left><top>13</top><width>%d</width>' % (x, w))
            if v == 'e':
                l = l.replace('String.IsEqual(%s,d)' % V, 'String.IsEqual(%s,e)' % V)
            l = re.sub(r'<label>[^<]*</label>', '<label>%s</label>' % label, l)
            new.append(l)
    lines = keep[:first] + new + keep[first:]
    c = '\n'.join(lines)
    # OK: a > b > c > e > d > a
    c = c.replace('<onclick condition="String.IsEqual(%s,c)">Skin.SetString(aeon.vignette,d)</onclick>' % V,
                  '<onclick condition="String.IsEqual(%s,c)">Skin.SetString(aeon.vignette,e)</onclick>\n'
                  '\t\t\t\t\t<onclick condition="String.IsEqual(%s,e)">Skin.SetString(aeon.vignette,d)</onclick>' % (V, V))
    assert c.count('Skin.SetString(aeon.vignette,') == 5
    io.open(SP, 'w', encoding='utf-8', newline='\n').write(t[:g] + c + t[e:])
    print('row 9733: Off | Light | Medium | Strong | Heavy')


def variables():
    t = io.open(SUB, encoding='utf-8').read()
    if 'aeon.vignette),e)">cc' not in t:
        t = t.replace('\t\t<value condition="String.IsEqual(%s,d)">ffffffff</value>\n' % V,
                      '\t\t<value condition="String.IsEqual(%s,e)">ccffffff</value>\n'
                      '\t\t<value condition="String.IsEqual(%s,d)">ffffffff</value>\n' % (V, V), 1)
        t = t.replace('\t\t<value condition="String.IsEqual(%s,d)">c0000000</value>\n' % V,
                      '\t\t<value condition="String.IsEqual(%s,e)">b0000000</value>\n'
                      '\t\t<value condition="String.IsEqual(%s,d)">c0000000</value>\n' % (V, V), 1)
        assert 'aeon.vignette),e)">cc' in t and 'aeon.vignette),e)">b0' in t
        io.open(SUB, 'w', encoding='utf-8', newline='\n').write(t)
    print('Aeon_VignetteCol / Aeon_VignetteLow: Strong between Medium and Heavy')


if __name__ == '__main__':
    strings()
    row()
    variables()
