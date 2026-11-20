# -*- coding: utf-8 -*-
"""0.47.0 View settings for the redrawn Fused Glass library views (fg_lib.py): per view and media type
- Watched status (aeon.vo.watched): Default / On / Off (was Default / Off, and only in the Low list); in Fused Glass it
  shows in every video view and stands for the gold dots and the ticks,
- Progress rings (aeon.vo.rings, skin string 32563): Default / On / Off,
- Logos instead of titles (aeon.vo.logos, the global row's string 31746): Default / On / Off.
Default follows the global setting (Watched indicators, the rings are on, Logos instead of titles). The helper
publishes the options (VIEW_OPTIONS). Run from the skin folder; safe to run again."""
import io
import os
import re

PANEL = '1080i/Includes_LibraryPanel.xml'
SUB = '1080i/Includes_Aeon_Sub.xml'
FUSED = '1080i/Includes_Fused.xml'
SERVICE = '../script.aeon.helper/service.py'
B = 'Window(Home).Property(aeon.vo.base)'


def cycle(opt):
    p = 'Window(Home).Property(aeon.vo.%s)' % opt
    return ('\t\t\t\t\t\t<onclick condition="String.IsEmpty(%(p)s)">Skin.SetString($INFO[%(b)s]%(o)s,on)</onclick>\n'
            '\t\t\t\t\t\t<onclick condition="String.IsEqual(%(p)s,on)">Skin.SetString($INFO[%(b)s]%(o)s,off)</onclick>\n'
            '\t\t\t\t\t\t<onclick condition="String.IsEqual(%(p)s,off)">Skin.Reset($INFO[%(b)s]%(o)s)</onclick>\n' % {'p': p, 'b': B, 'o': opt})


def item(label, opt, icon, vis):
    return ('\t\t\t\t\t<item>\n\t\t\t\t\t\t<label>%s</label>\n\t\t\t\t\t\t<label2>$VAR[FG_VOS_%s]</label2>\n\t\t\t\t\t\t<icon>%s</icon>\n%s'
            '\t\t\t\t\t\t<visible>%s</visible>\n\t\t\t\t\t</item>\n' % (label, opt, icon, cycle(opt), vis))


p = io.open(PANEL, encoding='utf-8').read()
if 'aeon.vo.rings' not in p:
    old = re.search(r'\t\t\t\t\t<item>\n\t\t\t\t\t\t<label>\$LOCALIZE\[31863\]</label>.*?\t\t\t\t\t</item>\n', p, re.S)
    assert old
    fg = 'Window.IsActive(videos) + Skin.HasSetting(aeon.fglass)'
    new = item('$LOCALIZE[31863]', 'watched', 'aeon/icons/check.png',
               'Window.IsActive(videos) + [String.Contains(%s,.$LOCALIZE[31148].) | Skin.HasSetting(aeon.fglass)]' % B)
    new += item('$ADDON[skin.aeon.fuse 32563]', 'rings', 'fg/ring/a65.png', fg)
    new += item('$LOCALIZE[31746]', 'logos', 'aeon/icons/image.png', fg)
    p = p[:old.start()] + new + p[old.end():]
    io.open(PANEL, 'w', encoding='utf-8', newline='\n').write(p)

s = io.open(SUB, encoding='utf-8').read()
s = re.sub(r'\t<variable name="Aeon_VOS_watched">.*?</variable>\n', '', s, flags=re.S)
io.open(SUB, 'w', encoding='utf-8', newline='\n').write(s)
VARS = ''.join('''	<variable name="FG_VOS_%(o)s">
		<value condition="String.IsEqual(Window(Home).Property(aeon.vo.%(o)s),on)">$LOCALIZE[31547]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.vo.%(o)s),off)">$LOCALIZE[31548]</value>
		<value>$LOCALIZE[571]</value>
	</variable>
''' % {'o': o} for o in ('watched', 'rings', 'logos'))
f = io.open(FUSED, encoding='utf-8').read()
f = re.sub(r'\t<!-- FG_VOS:begin.*?<!-- FG_VOS:end -->\n', '', f, flags=re.S)
f = f.replace('</includes>', '\t<!-- FG_VOS:begin (written by _src/fg_lib_options.py): View settings values -->\n' + VARS + '\t<!-- FG_VOS:end -->\n</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)

sv = io.open(SERVICE, encoding='utf-8').read()
if "'rings'" not in sv:
    a = "'watched', 'trailer', 'boxbg')"
    assert a in sv
    sv = sv.replace(a, "'watched', 'trailer', 'boxbg', 'rings', 'logos')")
    io.open(SERVICE, 'w', encoding='utf-8', newline='\n').write(sv)

# the row's name in every language
TR = {
    'cs_cz': 'Kroužky průběhu', 'da_dk': 'Fremskridtsringe', 'de_de': 'Fortschrittsringe', 'el_gr': 'Δακτύλιοι προόδου',
    'es_es': 'Anillos de progreso', 'fi_fi': 'Edistymisrenkaat', 'fr_fr': 'Anneaux de progression', 'hu_hu': 'Haladási gyűrűk',
    'it_it': 'Anelli di avanzamento', 'ja_jp': '進捗リング', 'ko_kr': '진행률 링', 'nb_no': 'Fremdriftsringer',
    'nl_nl': 'Voortgangsringen', 'pl_pl': 'Pierścienie postępu', 'pt_br': 'Anéis de progresso', 'pt_pt': 'Anéis de progresso',
    'ru_ru': 'Кольца прогресса', 'sv_se': 'Förloppsringar', 'tr_tr': 'İlerleme halkaları', 'uk_ua': 'Кільця прогресу',
    'zh_cn': '进度环', 'zh_tw': '進度環',
}
assert len(TR) == 22
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    path = os.path.join('language', d, 'strings.po')
    t = io.open(path, encoding='utf-8').read()
    entry = 'msgctxt "#32563"\nmsgid "Progress rings"\nmsgstr "%s"\n' % ('' if lang == 'en_gb' else TR[lang])
    old = re.compile(r'msgctxt "#32563"\nmsgid ".*"\nmsgstr ".*"\n')
    t = old.sub(lambda _m: entry, t, count=1) if old.search(t) else t.rstrip('\n') + '\n\n' + entry
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
import xml.etree.ElementTree as ET
for name in (PANEL, SUB, FUSED):
    ET.parse(name)
print('ok', done, 'languages')
