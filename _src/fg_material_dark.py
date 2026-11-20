# -*- coding: utf-8 -*-
"""0.56.2 Skin settings > Look > Material: the fourth choice is called Dark, not Today (the user: "material is Today
(change that name to Dark or something sensible)"). The value stays '' (the default look); only the name changes:
the row uses the skin's "Dark" (32573, the Menu theme row's word, all languages) instead of Kodi's "Today" (33006),
and the help line (32551) says Dark too, in every language. Run from the skin folder; safe to run again."""
import glob
import io
import os
import re

TODAY = {'cs_cz': u'Dnes', 'da_dk': u'I dag', 'de_de': u'Heute', 'el_gr': u'Σήμερα', 'en_gb': u'Today', 'es_es': u'Hoy',
         'fi_fi': u'Tänään', 'fr_fr': u"Aujourd'hui", 'hu_hu': u'Ma', 'it_it': u'Oggi', 'ja_jp': u'今日', 'ko_kr': u'오늘',
         'nb_no': u'I dag', 'nl_nl': u'Vandaag', 'pl_pl': u'Dzisiaj', 'pt_br': u'Hoje', 'pt_pt': u'Hoje', 'ru_ru': u'Сегодня',
         'sv_se': u'Idag', 'tr_tr': u'Bugün', 'uk_ua': u'Сьогодні', 'zh_cn': u'今天', 'zh_tw': u'今天'}


def row():
    p = os.path.join('1080i', 'SkinSettings.xml')
    t = io.open(p, encoding='utf-8').read()
    i = t.find('<control type="button" id="9529">')
    g = t.rfind('<control type="group">', 0, i)
    depth = 0
    for m in re.finditer(r'<control[ >]|</control>', t[g:]):
        depth += -1 if m.group(0) == '</control>' else 1
        if depth == 0:
            e = g + m.end()
            break
    c = t[g:e]
    n = c.count('$LOCALIZE[33006]')
    if n:
        t = t[:g] + c.replace('$LOCALIZE[33006]', '$ADDON[skin.aeon.fuse 32573]') + t[e:]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('Material row: %d labels now Dark' % n)
    # the generator that made the row, so a fresh build says Dark too
    g = os.path.join('_src', 'fg_material.py')
    s = io.open(g, encoding='utf-8').read()
    s2 = s.replace("('$LOCALIZE[31072]', '$LOCALIZE[33006]')", "('$LOCALIZE[31072]', '$ADDON[skin.aeon.fuse 32573]')")
    if s2 != s:
        io.open(g, 'w', encoding='utf-8', newline='\n').write(s2)


def help_line():
    for p in sorted(glob.glob(os.path.join('language', '*', 'strings.po'))):
        lang = os.path.basename(os.path.dirname(p))[len('resource.language.'):]
        t = io.open(p, encoding='utf-8').read()
        dm = re.search(r'msgctxt "#32573"\nmsgid "(.*)"\nmsgstr "(.*)"', t)
        dark = dm.group(2) or dm.group(1)
        m = re.search(r'msgctxt "#32551"\nmsgid "(.*)"\nmsgstr "(.*)"', t)
        msgid, msgstr = m.group(1), m.group(2)
        msgid2 = msgid.replace('Today: darker.', 'Dark: darker.')
        word = TODAY[lang]
        msgstr2 = msgstr
        if msgstr:
            k = msgstr.rfind(word)
            if k >= 0:                          # (already Dark on a second run)
                msgstr2 = msgstr[:k] + dark + msgstr[k + len(word):]
        if (msgid2, msgstr2) != (msgid, msgstr):
            t = t[:m.start()] + 'msgctxt "#32551"\nmsgid "%s"\nmsgstr "%s"' % (msgid2, msgstr2) + t[m.end():]
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('help line 32551: Dark in every language')


if __name__ == '__main__':
    row()
    help_line()
