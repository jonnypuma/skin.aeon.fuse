# -*- coding: utf-8 -*-
"""0.44.0 strings for the Episode combined view: 32541-32546. {n}, {time} and {total} are filled in by script.aeon.helper.
Run from the skin folder."""
import io
import os

EN = {
    32541: '{n} in progress',
    32542: '{n} unwatched',
    32543: 'All watched',
    32544: 'Episode combined',
    32545: 'Season buttons, the episodes in a card and the one in focus beside it',
    32546: '{time} of {total}',
}
TR = {
    'cs_cz': ('{n} rozkoukané', '{n} nezhlédnuté', 'Vše zhlédnuto', 'Díly v kartě', 'Tlačítka řad, díly v kartě a vybraný díl vedle', '{time} z {total}'),
    'da_dk': ('{n} i gang', '{n} ikke set', 'Alt set', 'Afsnit samlet', 'Sæsonknapper, afsnittene på et kort og det valgte ved siden af', '{time} af {total}'),
    'de_de': ('{n} angefangen', '{n} ungesehen', 'Alles gesehen', 'Folgen kombiniert', 'Staffel-Knöpfe, die Folgen in einer Karte und die gewählte daneben', '{time} von {total}'),
    'el_gr': ('{n} σε εξέλιξη', '{n} δεν έχουν προβληθεί', 'Όλα προβλήθηκαν', 'Επεισόδια μαζί', 'Κουμπιά σεζόν, τα επεισόδια σε κάρτα και το επιλεγμένο δίπλα', '{time} από {total}'),
    'es_es': ('{n} empezados', '{n} sin ver', 'Todo visto', 'Episodios combinados', 'Botones de temporada, los episodios en una tarjeta y el elegido al lado', '{time} de {total}'),
    'fi_fi': ('{n} kesken', '{n} katsomatta', 'Kaikki katsottu', 'Jaksot yhdessä', 'Kausipainikkeet, jaksot kortissa ja valittu vieressä', '{time} / {total}'),
    'fr_fr': ('{n} en cours', '{n} non vus', 'Tout est vu', 'Épisodes combinés', "Boutons de saison, les épisodes dans une carte et celui choisi à côté", '{time} sur {total}'),
    'hu_hu': ('{n} folyamatban', '{n} nem látott', 'Minden megnézve', 'Epizódok együtt', 'Évadgombok, az epizódok egy kártyán és a kiválasztott mellette', '{time} / {total}'),
    'it_it': ('{n} in corso', '{n} da vedere', 'Tutto visto', 'Episodi combinati', 'Pulsanti delle stagioni, gli episodi in una scheda e quello scelto accanto', '{time} di {total}'),
    'ja_jp': ('{n} 件視聴中', '{n} 件未視聴', 'すべて視聴済み', 'エピソード一覧', 'シーズンボタン、カードのエピソード、横に選択中のエピソード', '{time} / {total}'),
    'ko_kr': ('{n}편 시청 중', '{n}편 안 봄', '모두 시청함', '에피소드 모아 보기', '시즌 버튼, 카드 속 에피소드, 옆에 선택한 에피소드', '{time} / {total}'),
    'nb_no': ('{n} påbegynt', '{n} ikke sett', 'Alt sett', 'Episoder samlet', 'Sesongknapper, episodene på et kort og den valgte ved siden av', '{time} av {total}'),
    'nl_nl': ('{n} begonnen', '{n} niet gezien', 'Alles gezien', 'Afleveringen gecombineerd', 'Seizoensknoppen, de afleveringen in een kaart en de gekozen ernaast', '{time} van {total}'),
    'pl_pl': ('W trakcie: {n}', 'Nieobejrzane: {n}', 'Wszystko obejrzane', 'Odcinki razem', 'Przyciski sezonów, odcinki na karcie i wybrany obok', '{time} z {total}'),
    'pt_br': ('{n} em andamento', '{n} não assistidos', 'Tudo assistido', 'Episódios combinados', 'Botões de temporada, os episódios num cartão e o escolhido ao lado', '{time} de {total}'),
    'pt_pt': ('{n} em curso', '{n} por ver', 'Tudo visto', 'Episódios combinados', 'Botões de temporada, os episódios num cartão e o escolhido ao lado', '{time} de {total}'),
    'ru_ru': ('В процессе: {n}', 'Не просмотрено: {n}', 'Всё просмотрено', 'Серии вместе', 'Кнопки сезонов, серии на карточке и выбранная рядом', '{time} из {total}'),
    'sv_se': ('{n} påbörjade', '{n} osedda', 'Allt sett', 'Avsnitt samlat', 'Säsongsknappar, avsnitten på ett kort och det valda bredvid', '{time} av {total}'),
    'tr_tr': ('{n} devam ediyor', '{n} izlenmedi', 'Hepsi izlendi', 'Bölümler bir arada', 'Sezon düğmeleri, bir kartta bölümler ve yanında seçili olan', '{time} / {total}'),
    'uk_ua': ('У процесі: {n}', 'Не переглянуто: {n}', 'Усе переглянуто', 'Серії разом', 'Кнопки сезонів, серії на картці й вибрана поруч', '{time} з {total}'),
    'zh_cn': ('{n} 集在看', '{n} 集未看', '全部看完', '剧集合并', '季按钮、卡片中的剧集和旁边选中的一集', '{time} / {total}'),
    'zh_tw': ('{n} 集在看', '{n} 集未看', '全部看完', '劇集合併', '季按鈕、卡片中的劇集和旁邊選取的一集', '{time} / {total}'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32541"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    assert lang == 'en_gb' or len(tr) == len(EN), lang
    if lang != 'en_gb':
        for i, ident in enumerate(sorted(EN)):
            for field in ('{n}', '{time}', '{total}'):
                assert (field in EN[ident]) == (field in tr[i]), (lang, ident, field)
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else tr[i].replace('"', '\\"')
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32541-32546 added in %d languages' % done)
