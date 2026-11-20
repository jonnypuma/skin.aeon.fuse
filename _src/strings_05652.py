# -*- coding: utf-8 -*-
"""0.56.52 strings, all 23 languages: Information > Ratings shown in (32751) / Media info shown in (32752), the places
of their modal (32753-32759) and the two help lines (32760 / 32761). Repeatable: an id that is there is written again."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
IDS = list(range(32751, 32762))
EN = ['Ratings shown in', 'Media info shown in', 'Library views', 'Information pages', 'Widget & Spotlight screens',
      'Home spotlights', 'Player info', 'Screensaver', 'Live TV',
      'Where the ratings (IMDb, TMDb, Rotten Tomatoes, Trakt) appear. OK opens the list: tick the places.',
      'Where the media info chips (resolution, HDR, audio ...) appear. OK opens the list: tick the places. Which chips: Media info chips.']
T = {
    'cs_cz': ['Hodnocení zobrazit v', 'Informace o médiu zobrazit v', 'Zobrazení knihovny', 'Stránky informací',
              'Obrazovky widgetů a Spotlightu', 'Spotlighty na hlavní obrazovce', 'Informace přehrávače', 'Spořič obrazovky',
              'Živá TV', 'Kde se zobrazí hodnocení (IMDb, TMDb, Rotten Tomatoes, Trakt). OK otevře seznam: zaškrtněte místa.',
              'Kde se zobrazí štítky médií (rozlišení, HDR, zvuk ...). OK otevře seznam: zaškrtněte místa. Které štítky: Štítky informací o médiu.'],
    'da_dk': ['Bedømmelser vises i', 'Medieinfo vises i', 'Biblioteksvisninger', 'Informationssider', 'Widget- og Spotlight-skærme',
              'Spotlights på startskærmen', 'Afspillerinfo', 'Pauseskærm', 'Live-tv',
              'Hvor bedømmelserne (IMDb, TMDb, Rotten Tomatoes, Trakt) vises. OK åbner listen: sæt flueben ved stederne.',
              'Hvor medieinfo-mærkerne (opløsning, HDR, lyd ...) vises. OK åbner listen: sæt flueben ved stederne. Hvilke mærker: Medieinfo-mærker.'],
    'de_de': ['Bewertungen anzeigen in', 'Medieninfos anzeigen in', 'Bibliotheksansichten', 'Informationsseiten',
              'Widget- und Spotlight-Bildschirme', 'Spotlights im Hauptmenü', 'Player-Infos', 'Bildschirmschoner', 'Live-TV',
              'Wo die Bewertungen (IMDb, TMDb, Rotten Tomatoes, Trakt) erscheinen. OK öffnet die Liste: die Orte ankreuzen.',
              'Wo die Medieninfo-Chips (Auflösung, HDR, Audio ...) erscheinen. OK öffnet die Liste: die Orte ankreuzen. Welche Chips: Medieninfo-Chips.'],
    'el_gr': ['Βαθμολογίες σε', 'Πληροφορίες μέσου σε', 'Προβολές βιβλιοθήκης', 'Σελίδες πληροφοριών', 'Οθόνες widget και Spotlight',
              'Spotlight αρχικής οθόνης', 'Πληροφορίες αναπαραγωγής', 'Προφύλαξη οθόνης', 'Ζωντανή TV',
              'Πού εμφανίζονται οι βαθμολογίες (IMDb, TMDb, Rotten Tomatoes, Trakt). Το OK ανοίγει τη λίστα: σημειώστε τα σημεία.',
              'Πού εμφανίζονται οι ετικέτες μέσου (ανάλυση, HDR, ήχος ...). Το OK ανοίγει τη λίστα: σημειώστε τα σημεία. Ποιες ετικέτες: Ετικέτες πληροφοριών μέσου.'],
    'es_es': ['Valoraciones en', 'Info del medio en', 'Vistas de la biblioteca', 'Páginas de información', 'Pantallas de widgets y Spotlight',
              'Spotlights de inicio', 'Info del reproductor', 'Salvapantallas', 'TV en directo',
              'Dónde aparecen las valoraciones (IMDb, TMDb, Rotten Tomatoes, Trakt). OK abre la lista: marca los lugares.',
              'Dónde aparecen las etiquetas del medio (resolución, HDR, audio ...). OK abre la lista: marca los lugares. Qué etiquetas: Etiquetas de info del medio.'],
    'fi_fi': ['Arviot näkyvät', 'Mediatiedot näkyvät', 'Kirjastonäkymät', 'Tietosivut', 'Widget- ja Spotlight-näkymät',
              'Aloitusnäytön Spotlightit', 'Soittimen tiedot', 'Näytönsäästäjä', 'Suora TV',
              'Missä arviot (IMDb, TMDb, Rotten Tomatoes, Trakt) näkyvät. OK avaa listan: rastita paikat.',
              'Missä mediatietojen merkit (resoluutio, HDR, ääni ...) näkyvät. OK avaa listan: rastita paikat. Mitkä merkit: Mediatietojen merkit.'],
    'fr_fr': ['Notes affichées dans', 'Infos média affichées dans', 'Vues de la bibliothèque', "Pages d'information",
              'Écrans de widgets et Spotlight', "Spotlights de l'accueil", 'Infos du lecteur', 'Économiseur d’écran', 'TV en direct',
              'Où les notes (IMDb, TMDb, Rotten Tomatoes, Trakt) apparaissent. OK ouvre la liste : cochez les endroits.',
              'Où les pastilles média (résolution, HDR, audio ...) apparaissent. OK ouvre la liste : cochez les endroits. Quelles pastilles : Pastilles infos média.'],
    'hu_hu': ['Értékelések itt', 'Médiainfó itt', 'Könyvtárnézetek', 'Információs oldalak', 'Widget- és Spotlight-képernyők',
              'Kezdőképernyő Spotlightjai', 'Lejátszó információi', 'Képernyővédő', 'Élő TV',
              'Hol jelenjenek meg az értékelések (IMDb, TMDb, Rotten Tomatoes, Trakt). Az OK megnyitja a listát: jelölje be a helyeket.',
              'Hol jelenjenek meg a médiainfó-címkék (felbontás, HDR, hang ...). Az OK megnyitja a listát: jelölje be a helyeket. Mely címkék: Médiainfó-címkék.'],
    'it_it': ['Valutazioni in', 'Info media in', 'Viste della libreria', 'Pagine informazioni', 'Schermate widget e Spotlight',
              'Spotlight della Home', 'Info del lettore', 'Salvaschermo', 'TV in diretta',
              'Dove compaiono le valutazioni (IMDb, TMDb, Rotten Tomatoes, Trakt). OK apre l’elenco: spunta i posti.',
              'Dove compaiono le etichette media (risoluzione, HDR, audio ...). OK apre l’elenco: spunta i posti. Quali etichette: Etichette info media.'],
    'ja_jp': ['評価の表示場所', 'メディア情報の表示場所', 'ライブラリ表示', '情報ページ', 'ウィジェットとスポットライト画面',
              'ホームのスポットライト', 'プレーヤー情報', 'スクリーンセーバー', 'ライブTV',
              '評価 (IMDb、TMDb、Rotten Tomatoes、Trakt) を表示する場所。OK で一覧を開き、場所にチェックします。',
              'メディア情報チップ (解像度、HDR、音声 ...) を表示する場所。OK で一覧を開き、場所にチェックします。どのチップか: メディア情報チップ。'],
    'ko_kr': ['평점 표시 위치', '미디어 정보 표시 위치', '라이브러리 보기', '정보 페이지', '위젯 및 스포트라이트 화면',
              '홈 스포트라이트', '플레이어 정보', '화면 보호기', '실시간 TV',
              '평점 (IMDb, TMDb, Rotten Tomatoes, Trakt) 이 표시되는 곳. OK 로 목록을 열고 위치를 선택하세요.',
              '미디어 정보 칩 (해상도, HDR, 오디오 ...) 이 표시되는 곳. OK 로 목록을 열고 위치를 선택하세요. 어떤 칩: 미디어 정보 칩.'],
    'nb_no': ['Vurderinger vises i', 'Medieinfo vises i', 'Bibliotekvisninger', 'Informasjonssider', 'Widget- og Spotlight-skjermer',
              'Spotlights på startskjermen', 'Spillerinfo', 'Skjermsparer', 'Direkte-TV',
              'Hvor vurderingene (IMDb, TMDb, Rotten Tomatoes, Trakt) vises. OK åpner listen: kryss av stedene.',
              'Hvor medieinfo-merkene (oppløsning, HDR, lyd ...) vises. OK åpner listen: kryss av stedene. Hvilke merker: Medieinfo-merker.'],
    'nl_nl': ['Beoordelingen tonen in', 'Media-info tonen in', 'Bibliotheekweergaven', 'Informatiepagina’s', 'Widget- en Spotlight-schermen',
              'Spotlights op het startscherm', 'Spelerinfo', 'Schermbeveiliging', 'Live-tv',
              'Waar de beoordelingen (IMDb, TMDb, Rotten Tomatoes, Trakt) verschijnen. OK opent de lijst: vink de plaatsen aan.',
              'Waar de media-infolabels (resolutie, HDR, audio ...) verschijnen. OK opent de lijst: vink de plaatsen aan. Welke labels: Media-infolabels.'],
    'pl_pl': ['Oceny pokazuj w', 'Informacje o mediach pokazuj w', 'Widoki biblioteki', 'Strony informacji', 'Ekrany widżetów i Spotlight',
              'Spotlighty ekranu głównego', 'Informacje odtwarzacza', 'Wygaszacz ekranu', 'Telewizja na żywo',
              'Gdzie pojawiają się oceny (IMDb, TMDb, Rotten Tomatoes, Trakt). OK otwiera listę: zaznacz miejsca.',
              'Gdzie pojawiają się etykiety mediów (rozdzielczość, HDR, dźwięk ...). OK otwiera listę: zaznacz miejsca. Które etykiety: Etykiety informacji o mediach.'],
    'pt_br': ['Classificações em', 'Info de mídia em', 'Visualizações da biblioteca', 'Páginas de informação', 'Telas de widgets e Spotlight',
              'Spotlights da tela inicial', 'Info do player', 'Protetor de tela', 'TV ao vivo',
              'Onde as classificações (IMDb, TMDb, Rotten Tomatoes, Trakt) aparecem. OK abre a lista: marque os lugares.',
              'Onde as etiquetas de mídia (resolução, HDR, áudio ...) aparecem. OK abre a lista: marque os lugares. Quais etiquetas: Etiquetas de info de mídia.'],
    'pt_pt': ['Classificações em', 'Info de multimédia em', 'Vistas da biblioteca', 'Páginas de informação', 'Ecrãs de widgets e Spotlight',
              'Spotlights do ecrã inicial', 'Info do leitor', 'Proteção de ecrã', 'TV em direto',
              'Onde as classificações (IMDb, TMDb, Rotten Tomatoes, Trakt) aparecem. OK abre a lista: marque os locais.',
              'Onde as etiquetas de multimédia (resolução, HDR, áudio ...) aparecem. OK abre a lista: marque os locais. Que etiquetas: Etiquetas de info de multimédia.'],
    'ru_ru': ['Рейтинги показывать в', 'Информацию о медиа показывать в', 'Виды библиотеки', 'Страницы информации',
              'Экраны виджетов и Spotlight', 'Spotlight на главном экране', 'Информация плеера', 'Заставка', 'ТВ в эфире',
              'Где показываются рейтинги (IMDb, TMDb, Rotten Tomatoes, Trakt). OK открывает список: отметьте места.',
              'Где показываются метки медиа (разрешение, HDR, звук ...). OK открывает список: отметьте места. Какие метки: Метки информации о медиа.'],
    'sv_se': ['Betyg visas i', 'Mediainfo visas i', 'Biblioteksvyer', 'Informationssidor', 'Widget- och Spotlight-skärmar',
              'Spotlights på startskärmen', 'Spelarinfo', 'Skärmsläckare', 'Live-tv',
              'Var betygen (IMDb, TMDb, Rotten Tomatoes, Trakt) visas. OK öppnar listan: bocka för platserna.',
              'Var mediainfo-märkena (upplösning, HDR, ljud ...) visas. OK öppnar listan: bocka för platserna. Vilka märken: Mediainfo-märken.'],
    'tr_tr': ['Puanların gösterildiği yerler', 'Medya bilgisinin gösterildiği yerler', 'Kitaplık görünümleri', 'Bilgi sayfaları',
              'Widget ve Spotlight ekranları', 'Ana ekran Spotlightları', 'Oynatıcı bilgisi', 'Ekran koruyucu', 'Canlı TV',
              'Puanların (IMDb, TMDb, Rotten Tomatoes, Trakt) göründüğü yerler. OK listeyi açar: yerleri işaretleyin.',
              'Medya bilgi etiketlerinin (çözünürlük, HDR, ses ...) göründüğü yerler. OK listeyi açar: yerleri işaretleyin. Hangi etiketler: Medya bilgi etiketleri.'],
    'uk_ua': ['Рейтинги показувати в', 'Інформацію про медіа показувати в', 'Види бібліотеки', 'Сторінки інформації',
              'Екрани віджетів і Spotlight', 'Spotlight на головному екрані', 'Інформація плеєра', 'Заставка', 'ТБ наживо',
              'Де показуються рейтинги (IMDb, TMDb, Rotten Tomatoes, Trakt). OK відкриває список: позначте місця.',
              'Де показуються мітки медіа (роздільність, HDR, звук ...). OK відкриває список: позначте місця. Які мітки: Мітки інформації про медіа.'],
    'zh_cn': ['评分显示位置', '媒体信息显示位置', '媒体库视图', '信息页面', '小部件和聚光灯屏幕', '主页聚光灯', '播放器信息', '屏幕保护程序', '直播电视',
              '评分 (IMDb、TMDb、Rotten Tomatoes、Trakt) 显示的位置。按 OK 打开列表：勾选位置。',
              '媒体信息标签 (分辨率、HDR、音频 ...) 显示的位置。按 OK 打开列表：勾选位置。哪些标签：媒体信息标签。'],
    'zh_tw': ['評分顯示位置', '媒體資訊顯示位置', '媒體庫檢視', '資訊頁面', '小工具與聚光燈畫面', '首頁聚光燈', '播放器資訊', '螢幕保護程式', '直播電視',
              '評分 (IMDb、TMDb、Rotten Tomatoes、Trakt) 顯示的位置。按 OK 開啟清單：勾選位置。',
              '媒體資訊標籤 (解析度、HDR、音訊 ...) 顯示的位置。按 OK 開啟清單：勾選位置。哪些標籤：媒體資訊標籤。'],
}


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    for code, row in T.items():
        assert len(row) == len(IDS), (code, len(row))
    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        code = d.replace('resource.language.', '')
        for i, sid in enumerate(IDS):
            tr = '' if code == 'en_gb' else esc(T[code][i])
            m = re.search(r'(msgctxt "#%d"\nmsgid ")(.*)("\nmsgstr ")(.*)(")' % sid, t)
            if m:
                t = t[:m.start()] + m.group(1) + esc(EN[i]) + m.group(3) + tr + m.group(5) + t[m.end():]
            else:
                t = t.rstrip('\n') + '\n\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(EN[i]), tr)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('ok', len(IDS), 'strings in', len(os.listdir(L)), 'languages')


if __name__ == '__main__':
    main()
