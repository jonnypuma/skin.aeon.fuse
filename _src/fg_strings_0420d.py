# -*- coding: utf-8 -*-
"""0.42.0 strings for Fused Glass Search (Home > Search and the Search window): 32516-32523. {episode} is filled in
by script.aeon.helper and stays as it is in every language. Run from the skin folder."""
import io
import os

EN = {
    32516: 'Search your library',
    32517: 'Films, shows, episodes, music, people',
    32518: "You're on {episode}",
    32519: 'Last search:',
    32520: 'Also search',
    32521: 'TMDb, not in the library',
    32522: 'People',
    32523: 'Online',
}
TR = {
    'cs_cz': ('Hledat v knihovně', 'Filmy, seriály, díly, hudba, lidé', 'Jste na {episode}', 'Poslední hledání:', 'Hledat také', 'TMDb, mimo knihovnu', 'Lidé', 'Online'),
    'da_dk': ('Søg i dit bibliotek', 'Film, serier, afsnit, musik, personer', 'Du er på {episode}', 'Seneste søgning:', 'Søg også', 'TMDb, ikke i biblioteket', 'Personer', 'Online'),
    'de_de': ('Bibliothek durchsuchen', 'Filme, Serien, Folgen, Musik, Personen', 'Du bist bei {episode}', 'Letzte Suche:', 'Auch suchen', 'TMDb, nicht in der Bibliothek', 'Personen', 'Online'),
    'el_gr': ('Αναζήτηση στη βιβλιοθήκη', 'Ταινίες, σειρές, επεισόδια, μουσική, άτομα', 'Είστε στο {episode}', 'Τελευταία αναζήτηση:', 'Αναζήτηση και σε', 'TMDb, εκτός βιβλιοθήκης', 'Άτομα', 'Online'),
    'es_es': ('Buscar en tu biblioteca', 'Películas, series, episodios, música, personas', 'Vas por {episode}', 'Última búsqueda:', 'Buscar también', 'TMDb, fuera de la biblioteca', 'Personas', 'En línea'),
    'fi_fi': ('Hae kirjastosta', 'Elokuvat, sarjat, jaksot, musiikki, henkilöt', 'Olet kohdassa {episode}', 'Viimeisin haku:', 'Hae myös', 'TMDb, ei kirjastossa', 'Henkilöt', 'Verkossa'),
    'fr_fr': ('Rechercher dans la médiathèque', 'Films, séries, épisodes, musique, personnes', 'Vous en êtes à {episode}', 'Dernière recherche :', 'Chercher aussi', 'TMDb, hors médiathèque', 'Personnes', 'En ligne'),
    'hu_hu': ('Keresés a médiatárban', 'Filmek, sorozatok, epizódok, zene, személyek', 'Itt tartasz: {episode}', 'Utolsó keresés:', 'Keresés még itt', 'TMDb, nincs a médiatárban', 'Személyek', 'Online'),
    'it_it': ('Cerca nella libreria', 'Film, serie, episodi, musica, persone', 'Sei a {episode}', 'Ultima ricerca:', 'Cerca anche', 'TMDb, non in libreria', 'Persone', 'Online'),
    'ja_jp': ('ライブラリを検索', '映画、番組、エピソード、音楽、人物', '{episode} まで視聴中', '前回の検索:', 'ほかの検索先', 'TMDb (ライブラリ外)', '人物', 'オンライン'),
    'ko_kr': ('라이브러리 검색', '영화, 프로그램, 에피소드, 음악, 인물', '{episode} 시청 중', '최근 검색:', '다른 곳에서도 검색', 'TMDb (라이브러리에 없음)', '인물', '온라인'),
    'nb_no': ('Søk i biblioteket', 'Filmer, serier, episoder, musikk, personer', 'Du er på {episode}', 'Siste søk:', 'Søk også', 'TMDb, ikke i biblioteket', 'Personer', 'På nett'),
    'nl_nl': ('Zoek in je bibliotheek', 'Films, series, afleveringen, muziek, personen', 'Je bent bij {episode}', 'Laatste zoekopdracht:', 'Zoek ook', 'TMDb, niet in de bibliotheek', 'Personen', 'Online'),
    'pl_pl': ('Szukaj w bibliotece', 'Filmy, seriale, odcinki, muzyka, osoby', 'Jesteś na {episode}', 'Ostatnie wyszukiwanie:', 'Szukaj też', 'TMDb, spoza biblioteki', 'Osoby', 'Online'),
    'pt_br': ('Buscar na biblioteca', 'Filmes, séries, episódios, música, pessoas', 'Você está em {episode}', 'Última busca:', 'Buscar também', 'TMDb, fora da biblioteca', 'Pessoas', 'Online'),
    'pt_pt': ('Pesquisar na biblioteca', 'Filmes, séries, episódios, música, pessoas', 'Está em {episode}', 'Última pesquisa:', 'Pesquisar também', 'TMDb, fora da biblioteca', 'Pessoas', 'Online'),
    'ru_ru': ('Поиск по медиатеке', 'Фильмы, сериалы, серии, музыка, люди', 'Вы на {episode}', 'Последний поиск:', 'Искать также', 'TMDb, не в медиатеке', 'Люди', 'Онлайн'),
    'sv_se': ('Sök i biblioteket', 'Filmer, serier, avsnitt, musik, personer', 'Du är på {episode}', 'Senaste sökning:', 'Sök också', 'TMDb, inte i biblioteket', 'Personer', 'Online'),
    'tr_tr': ('Kütüphanede ara', 'Filmler, diziler, bölümler, müzik, kişiler', '{episode} bölümündesin', 'Son arama:', 'Şurada da ara', 'TMDb, kütüphanede değil', 'Kişiler', 'Çevrimiçi'),
    'uk_ua': ('Пошук у медіатеці', 'Фільми, серіали, серії, музика, люди', 'Ви на {episode}', 'Останній пошук:', 'Шукати також', 'TMDb, не в медіатеці', 'Люди', 'Онлайн'),
    'zh_cn': ('搜索媒体库', '电影、剧集、单集、音乐、人物', '看到 {episode}', '上次搜索:', '还可搜索', 'TMDb（不在媒体库中）', '人物', '在线'),
    'zh_tw': ('搜尋媒體櫃', '電影、影集、單集、音樂、人物', '看到 {episode}', '上次搜尋:', '還可搜尋', 'TMDb（不在媒體櫃中）', '人物', '線上'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32516"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    assert lang == 'en_gb' or len(tr) == len(EN), lang
    if lang != 'en_gb':
        for i, ident in enumerate(sorted(EN)):
            assert ('{episode}' in EN[ident]) == ('{episode}' in tr[i]), (lang, ident)
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else tr[i].replace('"', '\\"')
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32516-32523 added in %d languages' % done)
