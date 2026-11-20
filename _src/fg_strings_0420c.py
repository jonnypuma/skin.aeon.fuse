# -*- coding: utf-8 -*-
"""0.42.0 strings for Fused Glass Home > Favourites: 32510-32515. Fields in {braces} are filled in by script.aeon.helper
and stay as they are in every language. Run from the skin folder."""
import io
import os

EN = {
    32510: 'All episodes',
    32511: 'to the tile',
    32512: '{n} min left',
    32513: '{episode} airs {date}',
    32514: '{n} more waiting in season {season}',
    32515: '1 more waiting in season {season}',
}
TR = {
    'cs_cz': ('Všechny díly', 'zpět na dlaždici', 'zbývá {n} min', '{episode} vyjde {date}', 'v řadě {season} čeká ještě {n}', 'v řadě {season} čeká ještě 1'),
    'da_dk': ('Alle afsnit', 'til flisen', '{n} min tilbage', '{episode} sendes {date}', '{n} mere venter i sæson {season}', '1 mere venter i sæson {season}'),
    'de_de': ('Alle Folgen', 'zur Kachel', 'noch {n} Min.', '{episode} läuft am {date}', '{n} weitere warten in Staffel {season}', '1 weitere wartet in Staffel {season}'),
    'el_gr': ('Όλα τα επεισόδια', 'στο πλακίδιο', 'απομένουν {n} λεπ.', 'Το {episode} προβάλλεται {date}', 'Άλλα {n} περιμένουν στη σεζόν {season}', 'Άλλο 1 περιμένει στη σεζόν {season}'),
    'es_es': ('Todos los episodios', 'a la ficha', 'quedan {n} min', '{episode} se emite el {date}', '{n} más esperan en la temporada {season}', '1 más espera en la temporada {season}'),
    'fi_fi': ('Kaikki jaksot', 'ruutuun', '{n} min jäljellä', '{episode} tulee {date}', 'Kaudella {season} odottaa vielä {n}', 'Kaudella {season} odottaa vielä 1'),
    'fr_fr': ('Tous les épisodes', 'vers la vignette', 'encore {n} min', '{episode} diffusé le {date}', '{n} autres attendent dans la saison {season}', '1 autre attend dans la saison {season}'),
    'hu_hu': ('Minden epizód', 'vissza a csempéhez', 'még {n} perc', '{episode} adásban: {date}', 'Még {n} vár a(z) {season}. évadban', 'Még 1 vár a(z) {season}. évadban'),
    'it_it': ('Tutti gli episodi', 'al riquadro', 'mancano {n} min', '{episode} in onda {date}', 'Altri {n} in attesa nella stagione {season}', 'Ancora 1 in attesa nella stagione {season}'),
    'ja_jp': ('すべてのエピソード', 'タイルへ', '残り {n} 分', '{episode} は {date} に放送', 'シーズン {season} にあと {n} 話', 'シーズン {season} にあと 1 話'),
    'ko_kr': ('모든 에피소드', '타일로', '{n}분 남음', '{episode} {date} 방영', '시즌 {season}에 {n}편 더 남음', '시즌 {season}에 1편 더 남음'),
    'nb_no': ('Alle episoder', 'til flisen', '{n} min igjen', '{episode} sendes {date}', '{n} til venter i sesong {season}', '1 til venter i sesong {season}'),
    'nl_nl': ('Alle afleveringen', 'naar de tegel', 'nog {n} min', '{episode} komt {date}', 'nog {n} wachten in seizoen {season}', 'nog 1 wacht in seizoen {season}'),
    'pl_pl': ('Wszystkie odcinki', 'do kafelka', 'zostało {n} min', '{episode} emisja {date}', 'W sezonie {season} czeka jeszcze {n}', 'W sezonie {season} czeka jeszcze 1'),
    'pt_br': ('Todos os episódios', 'para o bloco', 'faltam {n} min', '{episode} estreia {date}', 'mais {n} esperando na temporada {season}', 'mais 1 esperando na temporada {season}'),
    'pt_pt': ('Todos os episódios', 'para o mosaico', 'faltam {n} min', '{episode} estreia {date}', 'mais {n} à espera na temporada {season}', 'mais 1 à espera na temporada {season}'),
    'ru_ru': ('Все серии', 'к плитке', 'осталось {n} мин', '{episode} выйдет {date}', 'Ещё {n} ждут в сезоне {season}', 'Ещё 1 ждёт в сезоне {season}'),
    'sv_se': ('Alla avsnitt', 'till rutan', '{n} min kvar', '{episode} sänds {date}', '{n} till väntar i säsong {season}', '1 till väntar i säsong {season}'),
    'tr_tr': ('Tüm bölümler', 'kutucuğa', '{n} dk kaldı', '{episode} yayında: {date}', '{season}. sezonda {n} bölüm daha var', '{season}. sezonda 1 bölüm daha var'),
    'uk_ua': ('Усі серії', 'до плитки', 'лишилось {n} хв', '{episode} вийде {date}', 'Ще {n} чекають у сезоні {season}', 'Ще 1 чекає у сезоні {season}'),
    'zh_cn': ('所有剧集', '回到磁贴', '还剩 {n} 分钟', '{episode} 将于 {date} 播出', '第 {season} 季还有 {n} 集', '第 {season} 季还有 1 集'),
    'zh_tw': ('所有劇集', '回到磚塊', '還剩 {n} 分鐘', '{episode} 將於 {date} 播出', '第 {season} 季還有 {n} 集', '第 {season} 季還有 1 集'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32510"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    assert lang == 'en_gb' or len(tr) == len(EN), lang
    for i, ident in enumerate(sorted(EN)):            # every field of the English text must survive the translation
        if lang != 'en_gb':
            for field in ('{n}', '{season}', '{episode}', '{date}'):
                assert (field in EN[ident]) == (field in tr[i]), (lang, ident, field)
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else tr[i].replace('"', '\\"')
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32510-32515 added in %d languages' % done)
