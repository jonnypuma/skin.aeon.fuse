# -*- coding: utf-8 -*-
"""0.41.0 strings 32487-32488: remote keys Up / Down for the hints of the Fused information screen."""
import io
import os
EN = {32487: 'Up', 32488: 'Down'}
TR = {'cs_cz': ('Nahoru', 'Dolů'), 'da_dk': ('Op', 'Ned'), 'de_de': ('Auf', 'Ab'), 'el_gr': ('Πάνω', 'Κάτω'), 'es_es': ('Arriba', 'Abajo'),
      'fi_fi': ('Ylös', 'Alas'), 'fr_fr': ('Haut', 'Bas'), 'hu_hu': ('Fel', 'Le'), 'it_it': ('Su', 'Giù'), 'ja_jp': ('上', '下'), 'ko_kr': ('위', '아래'),
      'nb_no': ('Opp', 'Ned'), 'nl_nl': ('Omhoog', 'Omlaag'), 'pl_pl': ('W górę', 'W dół'), 'pt_br': ('Cima', 'Baixo'), 'pt_pt': ('Cima', 'Baixo'),
      'ru_ru': ('Вверх', 'Вниз'), 'sv_se': ('Upp', 'Ner'), 'tr_tr': ('Yukarı', 'Aşağı'), 'uk_ua': ('Вгору', 'Вниз'), 'zh_cn': ('上', '下'), 'zh_tw': ('上', '下')}
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32487"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, EN[ident], '' if lang == 'en_gb' else tr[i])
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32487-32488 added in %d languages' % done)
