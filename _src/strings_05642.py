# -*- coding: utf-8 -*-
"""0.56.42 Skin settings categories (_src/regroup_05642.py), all 23 languages.
Renamed in place (only the category list and the title band use them): 31725 Appearance -> Theme & style,
31727 Playback -> Player, 31728 OSD settings -> Music player, 31730 Spotlight & widgets -> Widget & Spotlight screens,
31731 Motion, memory, reset -> System. New: 32722 Libraries, 32723 Information, 32724 Screensaver & backdrops.
Repeatable."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
IDS = [31725, 31727, 31728, 31730, 31731, 32722, 32723, 32724]
EN = ['Theme & style', 'Player', 'Music player', 'Widget & Spotlight screens', 'System', 'Libraries', 'Information',
      'Screensaver & backdrops']
T = {
    'cs_cz': ['Motiv a styl', 'Přehrávač', 'Hudební přehrávač', 'Obrazovky widgetů a Spotlight', 'Systém', 'Knihovny', 'Informace', 'Spořič obrazovky a pozadí'],
    'da_dk': ['Tema og stil', 'Afspiller', 'Musikafspiller', 'Widget- og Spotlight-skærme', 'System', 'Biblioteker', 'Information', 'Pauseskærm og baggrunde'],
    'de_de': ['Theme & Stil', 'Player', 'Musikplayer', 'Widget- & Spotlight-Seiten', 'System', 'Bibliotheken', 'Informationen', 'Bildschirmschoner & Hintergründe'],
    'el_gr': ['Θέμα και στυλ', 'Αναπαραγωγή', 'Αναπαραγωγή μουσικής', 'Οθόνες widget & Spotlight', 'Σύστημα', 'Βιβλιοθήκες', 'Πληροφορίες', 'Προφύλαξη οθόνης & φόντα'],
    'es_es': ['Tema y estilo', 'Reproductor', 'Reproductor de música', 'Pantallas de widgets y Spotlight', 'Sistema', 'Bibliotecas', 'Información', 'Salvapantallas y fondos'],
    'fi_fi': ['Teema ja tyyli', 'Soitin', 'Musiikkisoitin', 'Widget- ja Spotlight-näkymät', 'Järjestelmä', 'Kirjastot', 'Tiedot', 'Näytönsäästäjä ja taustat'],
    'fr_fr': ['Thème et style', 'Lecteur', 'Lecteur de musique', 'Écrans widgets & Spotlight', 'Système', 'Médiathèques', 'Informations', 'Économiseur & fonds'],
    'hu_hu': ['Téma és stílus', 'Lejátszó', 'Zenelejátszó', 'Widget- és Spotlight-képernyők', 'Rendszer', 'Könyvtárak', 'Információ', 'Képernyővédő és hátterek'],
    'it_it': ['Tema e stile', 'Lettore', 'Lettore musicale', 'Schermate widget e Spotlight', 'Sistema', 'Librerie', 'Informazioni', 'Salvaschermo e sfondi'],
    'ja_jp': ['テーマとスタイル', 'プレーヤー', '音楽プレーヤー', 'ウィジェットと Spotlight 画面', 'システム', 'ライブラリ', '情報', 'スクリーンセーバーと背景'],
    'ko_kr': ['테마 및 스타일', '플레이어', '음악 플레이어', '위젯 및 Spotlight 화면', '시스템', '라이브러리', '정보', '화면 보호기 및 배경'],
    'nb_no': ['Tema og stil', 'Avspiller', 'Musikkavspiller', 'Widget- og Spotlight-skjermer', 'System', 'Biblioteker', 'Informasjon', 'Skjermsparer og bakgrunner'],
    'nl_nl': ['Thema & stijl', 'Speler', 'Muziekspeler', 'Widget- & Spotlight-schermen', 'Systeem', 'Bibliotheken', 'Informatie', 'Schermbeveiliging & achtergronden'],
    'pl_pl': ['Motyw i styl', 'Odtwarzacz', 'Odtwarzacz muzyki', 'Ekrany widżetów i Spotlight', 'System', 'Biblioteki', 'Informacje', 'Wygaszacz i tła'],
    'pt_br': ['Tema e estilo', 'Player', 'Player de música', 'Telas de widgets e Spotlight', 'Sistema', 'Bibliotecas', 'Informações', 'Protetor de tela e fundos'],
    'pt_pt': ['Tema e estilo', 'Leitor', 'Leitor de música', 'Ecrãs de widgets e Spotlight', 'Sistema', 'Bibliotecas', 'Informações', 'Proteção de ecrã e fundos'],
    'ru_ru': ['Тема и стиль', 'Плеер', 'Музыкальный плеер', 'Экраны виджетов и Spotlight', 'Система', 'Медиатеки', 'Информация', 'Заставка и фоны'],
    'sv_se': ['Tema och stil', 'Spelare', 'Musikspelare', 'Widget- och Spotlight-skärmar', 'System', 'Bibliotek', 'Information', 'Skärmsläckare och bakgrunder'],
    'tr_tr': ['Tema ve stil', 'Oynatıcı', 'Müzik çalar', 'Widget ve Spotlight ekranları', 'Sistem', 'Kütüphaneler', 'Bilgi', 'Ekran koruyucu ve arka planlar'],
    'uk_ua': ['Тема і стиль', 'Програвач', 'Музичний програвач', 'Екрани віджетів і Spotlight', 'Система', 'Медіатеки', 'Інформація', 'Заставка і тла'],
    'zh_cn': ['主题与样式', '播放器', '音乐播放器', '小部件与 Spotlight 画面', '系统', '媒体库', '信息', '屏幕保护与背景'],
    'zh_tw': ['主題與樣式', '播放器', '音樂播放器', '小工具與 Spotlight 畫面', '系統', '媒體庫', '資訊', '螢幕保護與背景'],
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
