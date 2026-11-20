# -*- coding: utf-8 -*-
"""0.56.13 strings, all 23 languages: 32605 Next episode (Aeon Episode list, under the network logo). Safe to run again."""
import io
import os
import re

EN = 'Next episode'
T = {'cs_cz': 'Další epizoda', 'da_dk': 'Næste afsnit', 'de_de': 'Nächste Folge', 'el_gr': 'Επόμενο επεισόδιο',
     'es_es': 'Siguiente episodio', 'fi_fi': 'Seuraava jakso', 'fr_fr': 'Prochain épisode', 'hu_hu': 'Következő epizód',
     'it_it': 'Prossimo episodio', 'ja_jp': '次のエピソード', 'ko_kr': '다음 에피소드', 'nb_no': 'Neste episode',
     'nl_nl': 'Volgende aflevering', 'pl_pl': 'Następny odcinek', 'pt_br': 'Próximo episódio', 'pt_pt': 'Próximo episódio',
     'ru_ru': 'Следующая серия', 'sv_se': 'Nästa avsnitt', 'tr_tr': 'Sonraki bölüm', 'uk_ua': 'Наступна серія',
     'zh_cn': '下一集', 'zh_tw': '下一集'}

for d in sorted(os.listdir('language')):
    code = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    entry = 'msgctxt "#32605"\nmsgid "%s"\nmsgstr "%s"\n' % (EN, '' if code == 'en_gb' else T[code])
    pat = re.compile(r'msgctxt "#32605"\nmsgid "[^"]*"\nmsgstr "[^"]*"\n')
    t = pat.sub(lambda m: entry, t, count=1) if pat.search(t) else t.rstrip('\n') + '\n\n' + entry
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
