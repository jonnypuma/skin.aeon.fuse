# -*- coding: utf-8 -*-
"""0.56.41 Skin settings renames from the user's review of 2026-11-18, all 23 languages. Replaces msgid / msgstr of
existing strings; repeatable."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
IDS = (32474, 31763, 31764, 31767, 32608, 32680, 32682, 32684, 32663, 31751, 31804, 31805, 31818, 31875, 31785, 32427, 31848, 31860)
EN = ('Toasts expand from clock pill', 'Fanart Menu Backdrop', 'Menu Backdrop Strength', 'Library background',
      'Library fanart look', 'Library fanart opacity', 'Library fanart blur', 'Library fanart tint',
      'Combine multi-episode files into a single row in library', 'Subtitle offset strip', 'Show clock on OSD',
      'Show weather on OSD', 'Words style placement', 'Show language flags on OSD', 'Show poster on OSD controls',
      'Segment skip button placement', 'Show weather on screensaver', 'Show clock on screensaver')
T = {
    'cs_cz': ('Oznámení se rozbalují z kapsle hodin', 'Fanart pozadí nabídek', 'Síla pozadí nabídek', 'Pozadí knihovny',
              'Vzhled fanartu knihovny', 'Krytí fanartu knihovny', 'Rozmazání fanartu knihovny', 'Tónování fanartu knihovny',
              'Spojit soubory s více epizodami do jednoho řádku v knihovně', 'Lišta posunu titulků', 'Zobrazit hodiny v OSD',
              'Zobrazit počasí v OSD', 'Umístění stylu Slova', 'Zobrazit vlajky jazyků v OSD', 'Zobrazit plakát u ovládání OSD',
              'Umístění tlačítka přeskočení segmentu', 'Zobrazit počasí na spořiči', 'Zobrazit hodiny na spořiči'),
    'da_dk': ('Notifikationer udfoldes fra urkapslen', 'Fanart-menubaggrund', 'Menubaggrundens styrke', 'Biblioteksbaggrund',
              'Bibliotekets fanart-udseende', 'Bibliotekets fanart-dækkevne', 'Bibliotekets fanart-sløring', 'Bibliotekets fanart-toning',
              'Saml filer med flere afsnit i én række i biblioteket', 'Bjælke til undertekstforskydning', 'Vis ur i OSD',
              'Vis vejr i OSD', 'Placering af Ord-stilen', 'Vis sprogflag i OSD', 'Vis plakat ved OSD-knapperne',
              'Placering af knap til at springe segment over', 'Vis vejr på pauseskærmen', 'Vis ur på pauseskærmen'),
    'de_de': ('Hinweise klappen aus der Uhr-Kapsel auf', 'Fanart-Menühintergrund', 'Stärke des Menühintergrunds', 'Bibliothekshintergrund',
              'Fanart-Look der Bibliothek', 'Fanart-Deckkraft der Bibliothek', 'Fanart-Unschärfe der Bibliothek', 'Fanart-Tönung der Bibliothek',
              'Dateien mit mehreren Folgen in der Bibliothek zu einer Zeile zusammenfassen', 'Leiste für den Untertitelversatz', 'Uhr im OSD anzeigen',
              'Wetter im OSD anzeigen', 'Platzierung des Wörter-Stils', 'Sprachflaggen im OSD anzeigen', 'Poster bei den OSD-Bedienelementen anzeigen',
              'Platzierung der Segment-Überspringen-Taste', 'Wetter im Bildschirmschoner anzeigen', 'Uhr im Bildschirmschoner anzeigen'),
    'el_gr': ('Οι ειδοποιήσεις ανοίγουν από την κάψουλα του ρολογιού', 'Φόντο μενού με fanart', 'Ένταση φόντου μενού', 'Φόντο βιβλιοθήκης',
              'Εμφάνιση fanart βιβλιοθήκης', 'Αδιαφάνεια fanart βιβλιοθήκης', 'Θόλωμα fanart βιβλιοθήκης', 'Απόχρωση fanart βιβλιοθήκης',
              'Συνένωση αρχείων πολλών επεισοδίων σε μία γραμμή στη βιβλιοθήκη', 'Λωρίδα μετατόπισης υποτίτλων', 'Εμφάνιση ρολογιού στο OSD',
              'Εμφάνιση καιρού στο OSD', 'Θέση του στυλ Λέξεις', 'Εμφάνιση σημαιών γλώσσας στο OSD', 'Εμφάνιση αφίσας στα χειριστήρια OSD',
              'Θέση κουμπιού παράλειψης τμήματος', 'Εμφάνιση καιρού στην προφύλαξη οθόνης', 'Εμφάνιση ρολογιού στην προφύλαξη οθόνης'),
    'es_es': ('Los avisos se despliegan desde la cápsula del reloj', 'Fondo fanart de los menús', 'Intensidad del fondo de los menús', 'Fondo de la biblioteca',
              'Aspecto del fanart de la biblioteca', 'Opacidad del fanart de la biblioteca', 'Desenfoque del fanart de la biblioteca', 'Tinte del fanart de la biblioteca',
              'Combinar archivos de varios episodios en una sola fila en la biblioteca', 'Barra de desfase de subtítulos', 'Mostrar el reloj en el OSD',
              'Mostrar el tiempo en el OSD', 'Posición del estilo Palabras', 'Mostrar banderas de idioma en el OSD', 'Mostrar el póster en los controles del OSD',
              'Posición del botón para saltar segmentos', 'Mostrar el tiempo en el salvapantallas', 'Mostrar el reloj en el salvapantallas'),
    'fi_fi': ('Ilmoitukset avautuvat kellokapselista', 'Valikoiden fanart-tausta', 'Valikkotaustan voimakkuus', 'Kirjaston tausta',
              'Kirjaston fanartin ulkoasu', 'Kirjaston fanartin peittävyys', 'Kirjaston fanartin sumennus', 'Kirjaston fanartin sävytys',
              'Yhdistä usean jakson tiedostot yhdeksi riviksi kirjastossa', 'Tekstityksen siirtopalkki', 'Näytä kello OSD:ssä',
              'Näytä sää OSD:ssä', 'Sanat-tyylin sijainti', 'Näytä kieliliput OSD:ssä', 'Näytä juliste OSD-säätimissä',
              'Jakson ohituspainikkeen sijainti', 'Näytä sää näytönsäästäjässä', 'Näytä kello näytönsäästäjässä'),
    'fr_fr': ("Les notifications s'ouvrent depuis la capsule de l'horloge", 'Fond fanart des menus', 'Intensité du fond des menus', 'Fond de la médiathèque',
              'Aspect du fanart de la médiathèque', 'Opacité du fanart de la médiathèque', 'Flou du fanart de la médiathèque', 'Teinte du fanart de la médiathèque',
              'Regrouper les fichiers à plusieurs épisodes sur une seule ligne dans la médiathèque', 'Bande de décalage des sous-titres', "Afficher l'horloge dans l'OSD",
              "Afficher la météo dans l'OSD", 'Position du style Mots', "Afficher les drapeaux des langues dans l'OSD", "Afficher l'affiche près des commandes de l'OSD",
              'Position du bouton pour passer un segment', "Afficher la météo sur l'économiseur d'écran", "Afficher l'horloge sur l'économiseur d'écran"),
    'hu_hu': ('Az értesítések az óra kapszulájából nyílnak', 'Menük fanart háttere', 'Menühátter erőssége', 'Könyvtár háttere',
              'Könyvtári fanart megjelenése', 'Könyvtári fanart átlátszatlansága', 'Könyvtári fanart elmosása', 'Könyvtári fanart színezése',
              'Több epizódot tartalmazó fájlok egy sorba vonása a könyvtárban', 'Feliratcsúsztatási sáv', 'Óra megjelenítése az OSD-n',
              'Időjárás megjelenítése az OSD-n', 'A Szavak stílus elhelyezése', 'Nyelvi zászlók megjelenítése az OSD-n', 'Plakát megjelenítése az OSD-vezérlők mellett',
              'A szakaszátugró gomb elhelyezése', 'Időjárás megjelenítése a képernyővédőn', 'Óra megjelenítése a képernyővédőn'),
    'it_it': ("Le notifiche si aprono dalla capsula dell'orologio", 'Sfondo fanart dei menu', 'Intensità dello sfondo dei menu', 'Sfondo della libreria',
              'Aspetto del fanart della libreria', 'Opacità del fanart della libreria', 'Sfocatura del fanart della libreria', 'Tinta del fanart della libreria',
              'Unisci i file con più episodi in una sola riga nella libreria', 'Barra di ritardo dei sottotitoli', "Mostra l'orologio nell'OSD",
              "Mostra il meteo nell'OSD", 'Posizione dello stile Parole', "Mostra le bandiere delle lingue nell'OSD", "Mostra la locandina accanto ai comandi dell'OSD",
              'Posizione del pulsante per saltare i segmenti', 'Mostra il meteo nello screensaver', "Mostra l'orologio nello screensaver"),
    'ja_jp': ('通知を時計カプセルから展開', 'メニューのファンアート背景', 'メニュー背景の強さ', 'ライブラリの背景',
              'ライブラリのファンアートの見た目', 'ライブラリのファンアートの不透明度', 'ライブラリのファンアートのぼかし', 'ライブラリのファンアートの色合い',
              '複数エピソードのファイルをライブラリで1行にまとめる', '字幕オフセットのストリップ', 'OSD に時計を表示',
              'OSD に天気を表示', '単語スタイルの配置', 'OSD に言語の国旗を表示', 'OSD コントロールにポスターを表示',
              'セグメントスキップボタンの配置', 'スクリーンセーバーに天気を表示', 'スクリーンセーバーに時計を表示'),
    'ko_kr': ('알림이 시계 캡슐에서 펼쳐짐', '메뉴 팬아트 배경', '메뉴 배경 강도', '라이브러리 배경',
              '라이브러리 팬아트 모양', '라이브러리 팬아트 불투명도', '라이브러리 팬아트 흐림', '라이브러리 팬아트 색조',
              '여러 에피소드가 든 파일을 라이브러리에서 한 행으로 합치기', '자막 오프셋 스트립', 'OSD에 시계 표시',
              'OSD에 날씨 표시', '단어 스타일 위치', 'OSD에 언어 국기 표시', 'OSD 컨트롤에 포스터 표시',
              '구간 건너뛰기 버튼 위치', '화면 보호기에 날씨 표시', '화면 보호기에 시계 표시'),
    'nb_no': ('Varsler foldes ut fra klokkekapselen', 'Fanart-menybakgrunn', 'Styrke på menybakgrunnen', 'Bibliotekbakgrunn',
              'Bibliotekets fanart-utseende', 'Bibliotekets fanart-dekkevne', 'Bibliotekets fanart-uskarphet', 'Bibliotekets fanart-toning',
              'Slå sammen filer med flere episoder til én rad i biblioteket', 'Stripe for undertekstforskyvning', 'Vis klokke i OSD',
              'Vis vær i OSD', 'Plassering av Ord-stilen', 'Vis språkflagg i OSD', 'Vis plakat ved OSD-kontrollene',
              'Plassering av knapp for å hoppe over segment', 'Vis vær på skjermspareren', 'Vis klokke på skjermspareren'),
    'nl_nl': ('Meldingen klappen uit vanuit de klokcapsule', 'Fanart-menuachtergrond', 'Sterkte van de menuachtergrond', 'Bibliotheekachtergrond',
              'Uiterlijk van de bibliotheekfanart', 'Dekking van de bibliotheekfanart', 'Vervaging van de bibliotheekfanart', 'Tint van de bibliotheekfanart',
              'Bestanden met meerdere afleveringen samenvoegen tot één rij in de bibliotheek', 'Strook voor ondertitelverschuiving', 'Klok tonen in de OSD',
              'Weer tonen in de OSD', 'Plaatsing van de Woorden-stijl', 'Taalvlaggen tonen in de OSD', 'Poster tonen bij de OSD-bediening',
              'Plaatsing van de knop om segmenten over te slaan', 'Weer tonen op de schermbeveiliging', 'Klok tonen op de schermbeveiliging'),
    'pl_pl': ('Powiadomienia rozwijają się z kapsuły zegara', 'Tło fanart menu', 'Siła tła menu', 'Tło biblioteki',
              'Wygląd fanartu biblioteki', 'Krycie fanartu biblioteki', 'Rozmycie fanartu biblioteki', 'Odcień fanartu biblioteki',
              'Łącz pliki z wieloma odcinkami w jeden wiersz w bibliotece', 'Pasek przesunięcia napisów', 'Pokaż zegar w OSD',
              'Pokaż pogodę w OSD', 'Położenie stylu Słowa', 'Pokaż flagi języków w OSD', 'Pokaż plakat przy sterowaniu OSD',
              'Położenie przycisku pomijania segmentu', 'Pokaż pogodę na wygaszaczu', 'Pokaż zegar na wygaszaczu'),
    'pt_br': ('Notificações se abrem a partir da cápsula do relógio', 'Fundo fanart dos menus', 'Intensidade do fundo dos menus', 'Fundo da biblioteca',
              'Aparência do fanart da biblioteca', 'Opacidade do fanart da biblioteca', 'Desfoque do fanart da biblioteca', 'Tom do fanart da biblioteca',
              'Combinar arquivos de vários episódios em uma única linha na biblioteca', 'Faixa de atraso das legendas', 'Mostrar relógio no OSD',
              'Mostrar o tempo no OSD', 'Posição do estilo Palavras', 'Mostrar bandeiras de idioma no OSD', 'Mostrar pôster nos controles do OSD',
              'Posição do botão de pular segmento', 'Mostrar o tempo no protetor de tela', 'Mostrar relógio no protetor de tela'),
    'pt_pt': ('As notificações abrem a partir da cápsula do relógio', 'Fundo fanart dos menus', 'Intensidade do fundo dos menus', 'Fundo da biblioteca',
              'Aspeto do fanart da biblioteca', 'Opacidade do fanart da biblioteca', 'Desfocagem do fanart da biblioteca', 'Tonalidade do fanart da biblioteca',
              'Combinar ficheiros de vários episódios numa única linha na biblioteca', 'Faixa de desfasamento das legendas', 'Mostrar relógio no OSD',
              'Mostrar o tempo no OSD', 'Posição do estilo Palavras', 'Mostrar bandeiras de idioma no OSD', 'Mostrar cartaz nos controlos do OSD',
              'Posição do botão para saltar segmentos', 'Mostrar o tempo na proteção de ecrã', 'Mostrar relógio na proteção de ecrã'),
    'ru_ru': ('Уведомления раскрываются из капсулы часов', 'Фанарт-фон меню', 'Сила фона меню', 'Фон медиатеки',
              'Вид фанарта медиатеки', 'Непрозрачность фанарта медиатеки', 'Размытие фанарта медиатеки', 'Оттенок фанарта медиатеки',
              'Объединять файлы с несколькими эпизодами в одну строку в медиатеке', 'Полоса сдвига субтитров', 'Показывать часы в OSD',
              'Показывать погоду в OSD', 'Положение стиля «Слова»', 'Показывать флаги языков в OSD', 'Показывать постер у элементов OSD',
              'Положение кнопки пропуска фрагмента', 'Показывать погоду на заставке', 'Показывать часы на заставке'),
    'sv_se': ('Aviseringar vecklas ut från klockkapseln', 'Fanart-menybakgrund', 'Styrka på menybakgrunden', 'Biblioteksbakgrund',
              'Bibliotekets fanart-utseende', 'Bibliotekets fanart-opacitet', 'Bibliotekets fanart-oskärpa', 'Bibliotekets fanart-ton',
              'Slå ihop filer med flera avsnitt till en rad i biblioteket', 'Remsa för undertextförskjutning', 'Visa klocka i OSD',
              'Visa väder i OSD', 'Placering av Ord-stilen', 'Visa språkflaggor i OSD', 'Visa affisch vid OSD-kontrollerna',
              'Placering av knappen för att hoppa över segment', 'Visa väder på skärmsläckaren', 'Visa klocka på skärmsläckaren'),
    'tr_tr': ('Bildirimler saat kapsülünden açılır', 'Fanart menü arka planı', 'Menü arka planı gücü', 'Kütüphane arka planı',
              'Kütüphane fanart görünümü', 'Kütüphane fanart opaklığı', 'Kütüphane fanart bulanıklığı', 'Kütüphane fanart tonu',
              'Çok bölümlü dosyaları kütüphanede tek satırda birleştir', 'Altyazı kaydırma şeridi', "OSD'de saati göster",
              "OSD'de hava durumunu göster", 'Kelimeler stilinin yerleşimi', "OSD'de dil bayraklarını göster", 'OSD kontrollerinde afişi göster',
              'Bölüm atlama düğmesinin yerleşimi', 'Ekran koruyucuda hava durumunu göster', 'Ekran koruyucuda saati göster'),
    'uk_ua': ('Сповіщення розгортаються з капсули годинника', 'Фанарт-тло меню', 'Сила тла меню', 'Тло медіатеки',
              'Вигляд фанарту медіатеки', 'Непрозорість фанарту медіатеки', 'Розмиття фанарту медіатеки', 'Відтінок фанарту медіатеки',
              "Об'єднувати файли з кількома епізодами в один рядок у медіатеці", 'Смуга зсуву субтитрів', 'Показувати годинник в OSD',
              'Показувати погоду в OSD', 'Розташування стилю «Слова»', 'Показувати прапори мов в OSD', 'Показувати постер біля елементів OSD',
              'Розташування кнопки пропуску фрагмента', 'Показувати погоду на заставці', 'Показувати годинник на заставці'),
    'zh_cn': ('通知从时钟胶囊展开', '菜单同人画背景', '菜单背景强度', '媒体库背景',
              '媒体库同人画外观', '媒体库同人画不透明度', '媒体库同人画模糊', '媒体库同人画色调',
              '在媒体库中将多集文件合并为一行', '字幕偏移条', '在 OSD 上显示时钟',
              '在 OSD 上显示天气', '逐字样式位置', '在 OSD 上显示语言旗帜', '在 OSD 控制旁显示海报',
              '片段跳过按钮位置', '在屏幕保护程序上显示天气', '在屏幕保护程序上显示时钟'),
    'zh_tw': ('通知從時鐘膠囊展開', '選單同人畫背景', '選單背景強度', '媒體庫背景',
              '媒體庫同人畫外觀', '媒體庫同人畫不透明度', '媒體庫同人畫模糊', '媒體庫同人畫色調',
              '在媒體庫中將多集檔案合併為一列', '字幕偏移條', '在 OSD 上顯示時鐘',
              '在 OSD 上顯示天氣', '逐字樣式位置', '在 OSD 上顯示語言旗幟', '在 OSD 控制旁顯示海報',
              '片段跳過按鈕位置', '在螢幕保護程式上顯示天氣', '在螢幕保護程式上顯示時鐘'),
}


def esc(s):
    return s.replace('"', '\\"')


def main():
    for code, row in T.items():
        assert len(row) == len(IDS), (code, len(row))
    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        code = d.replace('resource.language.', '')
        for i, sid in enumerate(IDS):
            m = re.search(r'(msgctxt "#%d"\nmsgid ")(.*)("\nmsgstr ")(.*)(")' % sid, t)
            assert m, (d, sid)
            tr = '' if code == 'en_gb' else esc(T[code][i])
            t = t[:m.start()] + m.group(1) + esc(EN[i]) + m.group(3) + tr + m.group(5) + t[m.end():]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('renamed', len(IDS), 'in', len(os.listdir(L)), 'languages')


if __name__ == '__main__':
    main()
