# -*- coding: utf-8 -*-
"""0.43.0 strings for the Fused Glass Planner: 32524-32540. {n} is filled in by script.aeon.helper and stays as it is.
Run from the skin folder."""
import io
import os

EN = {
    32524: 'Next 7 days',
    32525: 'Shows you watch',
    32526: 'View settings',
    32527: 'Background',
    32528: 'Nothing out',
    32529: '{n} this week',
    32530: '1 episode',
    32531: '{n} episodes',
    32532: '1 film',
    32533: '{n} films',
    32534: 'Week: seven days side by side. Day: one day at a time.',
    32535: 'Episodes, films or both.',
    32536: 'Only the episodes of shows you have watched before.',
    32537: "Colors: the colours of the selected title's artwork. Neutral: plain. Fanart: the picture itself.",
    32538: 'The first day of a week. Today: always the next seven days.',
    32539: 'This week',
    32540: 'Next week',
}
TR = {
    'cs_cz': ('Příštích 7 dní', 'Seriály, které sledujete', 'Nastavení zobrazení', 'Pozadí', 'Nic nevychází', '{n} tento týden', '1 díl', '{n} dílů', '1 film', '{n} filmů', 'Týden: sedm dní vedle sebe. Den: jeden den najednou.', 'Díly, filmy nebo obojí.', 'Jen díly seriálů, které jste už sledovali.', 'Barvy: barvy obrázku vybraného titulu. Neutrální: jednobarevné. Fanart: samotný obrázek.', 'První den týdne. Dnes: vždy příštích sedm dní.', 'Tento týden', 'Příští týden'),
    'da_dk': ('De næste 7 dage', 'Serier du ser', 'Visningsindstillinger', 'Baggrund', 'Intet udkommer', '{n} denne uge', '1 afsnit', '{n} afsnit', '1 film', '{n} film', 'Uge: syv dage side om side. Dag: én dag ad gangen.', 'Afsnit, film eller begge.', 'Kun afsnit af serier, du har set før.', 'Farver: farverne fra den valgte titels billede. Neutral: ensfarvet. Fanart: selve billedet.', 'Ugens første dag. I dag: altid de næste syv dage.', 'Denne uge', 'Næste uge'),
    'de_de': ('Nächste 7 Tage', 'Serien, die du schaust', 'Ansichtseinstellungen', 'Hintergrund', 'Nichts erscheint', '{n} diese Woche', '1 Folge', '{n} Folgen', '1 Film', '{n} Filme', 'Woche: sieben Tage nebeneinander. Tag: ein Tag nach dem anderen.', 'Folgen, Filme oder beides.', 'Nur Folgen von Serien, die du schon geschaut hast.', 'Farben: die Farben des Bildes des gewählten Titels. Neutral: schlicht. Fanart: das Bild selbst.', 'Der erste Tag einer Woche. Heute: immer die nächsten sieben Tage.', 'Diese Woche', 'Nächste Woche'),
    'el_gr': ('Επόμενες 7 ημέρες', 'Σειρές που βλέπετε', 'Ρυθμίσεις προβολής', 'Φόντο', 'Τίποτα δεν βγαίνει', '{n} αυτή την εβδομάδα', '1 επεισόδιο', '{n} επεισόδια', '1 ταινία', '{n} ταινίες', 'Εβδομάδα: επτά ημέρες δίπλα δίπλα. Ημέρα: μία ημέρα τη φορά.', 'Επεισόδια, ταινίες ή και τα δύο.', 'Μόνο επεισόδια σειρών που έχετε ήδη δει.', 'Χρώματα: τα χρώματα της εικόνας του επιλεγμένου τίτλου. Ουδέτερο: απλό. Fanart: η ίδια η εικόνα.', 'Η πρώτη ημέρα της εβδομάδας. Σήμερα: πάντα οι επόμενες επτά ημέρες.', 'Αυτή την εβδομάδα', 'Επόμενη εβδομάδα'),
    'es_es': ('Próximos 7 días', 'Series que ves', 'Ajustes de vista', 'Fondo', 'No sale nada', '{n} esta semana', '1 episodio', '{n} episodios', '1 película', '{n} películas', 'Semana: siete días uno junto a otro. Día: un día cada vez.', 'Episodios, películas o ambos.', 'Solo episodios de series que ya has visto.', 'Colores: los colores de la imagen del título elegido. Neutro: liso. Fanart: la imagen misma.', 'El primer día de la semana. Hoy: siempre los próximos siete días.', 'Esta semana', 'La próxima semana'),
    'fi_fi': ('Seuraavat 7 päivää', 'Katsomasi sarjat', 'Näkymän asetukset', 'Tausta', 'Ei mitään', '{n} tällä viikolla', '1 jakso', '{n} jaksoa', '1 elokuva', '{n} elokuvaa', 'Viikko: seitsemän päivää rinnakkain. Päivä: yksi päivä kerrallaan.', 'Jaksot, elokuvat tai molemmat.', 'Vain jo katsomiesi sarjojen jaksot.', 'Värit: valitun nimikkeen kuvan värit. Neutraali: tasainen. Fanart: itse kuva.', 'Viikon ensimmäinen päivä. Tänään: aina seuraavat seitsemän päivää.', 'Tämä viikko', 'Ensi viikko'),
    'fr_fr': ('7 prochains jours', 'Séries que vous regardez', "Réglages d'affichage", 'Arrière-plan', 'Rien ne sort', '{n} cette semaine', '1 épisode', '{n} épisodes', '1 film', '{n} films', 'Semaine : sept jours côte à côte. Jour : un jour à la fois.', 'Épisodes, films ou les deux.', 'Seulement les épisodes des séries déjà regardées.', "Couleurs : les couleurs de l'image du titre choisi. Neutre : uni. Fanart : l'image elle-même.", "Le premier jour de la semaine. Aujourd'hui : toujours les sept prochains jours.", 'Cette semaine', 'La semaine prochaine'),
    'hu_hu': ('Következő 7 nap', 'Sorozatok, amelyeket nézel', 'Nézetbeállítások', 'Háttér', 'Nincs megjelenés', '{n} ezen a héten', '1 epizód', '{n} epizód', '1 film', '{n} film', 'Hét: hét nap egymás mellett. Nap: egyszerre egy nap.', 'Epizódok, filmek vagy mindkettő.', 'Csak a már nézett sorozatok epizódjai.', 'Színek: a kiválasztott cím képének színei. Semleges: egyszínű. Fanart: maga a kép.', 'A hét első napja. Ma: mindig a következő hét nap.', 'Ezen a héten', 'Jövő héten'),
    'it_it': ('Prossimi 7 giorni', 'Serie che guardi', 'Impostazioni vista', 'Sfondo', 'Non esce nulla', '{n} questa settimana', '1 episodio', '{n} episodi', '1 film', '{n} film', 'Settimana: sette giorni affiancati. Giorno: un giorno alla volta.', 'Episodi, film o entrambi.', 'Solo episodi di serie che hai già guardato.', "Colori: i colori dell'immagine del titolo scelto. Neutro: semplice. Fanart: l'immagine stessa.", 'Il primo giorno della settimana. Oggi: sempre i prossimi sette giorni.', 'Questa settimana', 'La prossima settimana'),
    'ja_jp': ('今後7日間', '見ている番組', '表示設定', '背景', '予定なし', '今週 {n}', '1 エピソード', '{n} エピソード', '1 本の映画', '{n} 本の映画', '週: 7日を並べて表示。日: 1日ずつ表示。', 'エピソード、映画、または両方。', '見たことのある番組のエピソードのみ。', 'カラー: 選択したタイトルの画像の色。ニュートラル: 無地。ファンアート: 画像そのもの。', '週の最初の日。今日: 常に今後7日間。', '今週', '来週'),
    'ko_kr': ('앞으로 7일', '시청 중인 프로그램', '보기 설정', '배경', '공개 예정 없음', '이번 주 {n}', '에피소드 1편', '에피소드 {n}편', '영화 1편', '영화 {n}편', '주: 7일을 나란히 표시. 일: 하루씩 표시.', '에피소드, 영화 또는 둘 다.', '본 적이 있는 프로그램의 에피소드만.', '색상: 선택한 작품 이미지의 색. 중립: 단색. 팬아트: 이미지 그대로.', '한 주의 첫날. 오늘: 항상 앞으로 7일.', '이번 주', '다음 주'),
    'nb_no': ('Neste 7 dager', 'Serier du ser', 'Visningsinnstillinger', 'Bakgrunn', 'Ingenting kommer', '{n} denne uken', '1 episode', '{n} episoder', '1 film', '{n} filmer', 'Uke: sju dager side om side. Dag: én dag om gangen.', 'Episoder, filmer eller begge.', 'Bare episoder av serier du har sett før.', 'Farger: fargene fra bildet til valgt tittel. Nøytral: ensfarget. Fanart: selve bildet.', 'Ukens første dag. I dag: alltid de neste sju dagene.', 'Denne uken', 'Neste uke'),
    'nl_nl': ('Komende 7 dagen', 'Series die je kijkt', 'Weergave-instellingen', 'Achtergrond', 'Niets verwacht', '{n} deze week', '1 aflevering', '{n} afleveringen', '1 film', '{n} films', 'Week: zeven dagen naast elkaar. Dag: één dag tegelijk.', 'Afleveringen, films of beide.', 'Alleen afleveringen van series die je al hebt gekeken.', 'Kleuren: de kleuren van de afbeelding van de gekozen titel. Neutraal: effen. Fanart: de afbeelding zelf.', 'De eerste dag van een week. Vandaag: altijd de komende zeven dagen.', 'Deze week', 'Volgende week'),
    'pl_pl': ('Najbliższe 7 dni', 'Seriale, które oglądasz', 'Ustawienia widoku', 'Tło', 'Nic nie wychodzi', '{n} w tym tygodniu', '1 odcinek', 'Odcinki: {n}', '1 film', 'Filmy: {n}', 'Tydzień: siedem dni obok siebie. Dzień: jeden dzień naraz.', 'Odcinki, filmy lub oba.', 'Tylko odcinki seriali, które już oglądasz.', 'Kolory: kolory obrazu wybranego tytułu. Neutralne: jednolite. Fanart: sam obraz.', 'Pierwszy dzień tygodnia. Dziś: zawsze najbliższe siedem dni.', 'Ten tydzień', 'Następny tydzień'),
    'pt_br': ('Próximos 7 dias', 'Séries que você assiste', 'Ajustes de exibição', 'Fundo', 'Nada estreia', '{n} esta semana', '1 episódio', '{n} episódios', '1 filme', '{n} filmes', 'Semana: sete dias lado a lado. Dia: um dia por vez.', 'Episódios, filmes ou ambos.', 'Só episódios de séries que você já assistiu.', 'Cores: as cores da imagem do título escolhido. Neutro: liso. Fanart: a própria imagem.', 'O primeiro dia da semana. Hoje: sempre os próximos sete dias.', 'Esta semana', 'Próxima semana'),
    'pt_pt': ('Próximos 7 dias', 'Séries que vê', 'Definições de vista', 'Fundo', 'Nada estreia', '{n} esta semana', '1 episódio', '{n} episódios', '1 filme', '{n} filmes', 'Semana: sete dias lado a lado. Dia: um dia de cada vez.', 'Episódios, filmes ou ambos.', 'Só episódios de séries que já viu.', 'Cores: as cores da imagem do título escolhido. Neutro: liso. Fanart: a própria imagem.', 'O primeiro dia da semana. Hoje: sempre os próximos sete dias.', 'Esta semana', 'Próxima semana'),
    'ru_ru': ('Ближайшие 7 дней', 'Сериалы, которые вы смотрите', 'Настройки вида', 'Фон', 'Ничего не выходит', '{n} на этой неделе', '1 серия', 'Серий: {n}', '1 фильм', 'Фильмов: {n}', 'Неделя: семь дней рядом. День: по одному дню.', 'Серии, фильмы или всё вместе.', 'Только серии сериалов, которые вы уже смотрели.', 'Цвета: цвета изображения выбранного названия. Нейтральный: однотонный. Fanart: само изображение.', 'Первый день недели. Сегодня: всегда ближайшие семь дней.', 'Эта неделя', 'Следующая неделя'),
    'sv_se': ('Kommande 7 dagar', 'Serier du tittar på', 'Visningsinställningar', 'Bakgrund', 'Inget kommer ut', '{n} den här veckan', '1 avsnitt', '{n} avsnitt', '1 film', '{n} filmer', 'Vecka: sju dagar sida vid sida. Dag: en dag i taget.', 'Avsnitt, filmer eller båda.', 'Bara avsnitt av serier du har sett förut.', 'Färger: färgerna i den valda titelns bild. Neutral: enfärgad. Fanart: själva bilden.', 'Veckans första dag. I dag: alltid de kommande sju dagarna.', 'Den här veckan', 'Nästa vecka'),
    'tr_tr': ('Önümüzdeki 7 gün', 'İzlediğin diziler', 'Görünüm ayarları', 'Arka plan', 'Çıkan bir şey yok', 'Bu hafta {n}', '1 bölüm', '{n} bölüm', '1 film', '{n} film', 'Hafta: yedi gün yan yana. Gün: bir seferde bir gün.', 'Bölümler, filmler veya ikisi.', 'Yalnızca daha önce izlediğin dizilerin bölümleri.', 'Renkler: seçili başlığın görselinin renkleri. Nötr: düz. Fanart: görselin kendisi.', 'Haftanın ilk günü. Bugün: her zaman önümüzdeki yedi gün.', 'Bu hafta', 'Gelecek hafta'),
    'uk_ua': ('Найближчі 7 днів', 'Серіали, які ви дивитеся', 'Налаштування вигляду', 'Тло', 'Нічого не виходить', '{n} цього тижня', '1 серія', 'Серій: {n}', '1 фільм', 'Фільмів: {n}', 'Тиждень: сім днів поруч. День: по одному дню.', 'Серії, фільми або все разом.', 'Лише серії серіалів, які ви вже дивилися.', 'Кольори: кольори зображення вибраної назви. Нейтральний: однотонний. Fanart: саме зображення.', 'Перший день тижня. Сьогодні: завжди найближчі сім днів.', 'Цей тиждень', 'Наступний тиждень'),
    'zh_cn': ('未来 7 天', '你在看的剧集', '视图设置', '背景', '没有新内容', '本周 {n}', '1 集', '{n} 集', '1 部电影', '{n} 部电影', '周：七天并排显示。日：一次一天。', '剧集、电影或两者。', '只显示看过的剧集的新集。', '色彩：所选标题图片的颜色。中性：纯色。Fanart：图片本身。', '一周的第一天。今天：始终为未来七天。', '本周', '下周'),
    'zh_tw': ('未來 7 天', '你在看的影集', '檢視設定', '背景', '沒有新內容', '本週 {n}', '1 集', '{n} 集', '1 部電影', '{n} 部電影', '週：七天並排顯示。日：一次一天。', '劇集、電影或兩者。', '只顯示看過的影集的新集。', '色彩：所選標題圖片的顏色。中性：純色。Fanart：圖片本身。', '一週的第一天。今天：一律為未來七天。', '本週', '下週'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32524"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    assert lang == 'en_gb' or len(tr) == len(EN), (lang, len(tr))
    if lang != 'en_gb':
        for i, ident in enumerate(sorted(EN)):
            assert ('{n}' in EN[ident]) == ('{n}' in tr[i]), (lang, ident)
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else tr[i].replace('"', '\\"')
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32524-32540 added in %d languages' % done)
