# -*- coding: utf-8 -*-
"""0.56.12 strings, all 23 languages: Material -> Library view theme (32550), its hint (32551), the Fused Glass Menu
theme hint with Frost (32574), the Appearance heading All themes (32604). Run from the skin folder; safe to run again."""
import io
import os
import re

LANG = 'language'
EN = {
    32550: 'Library view theme',
    32551: 'The glass of the frosted panels: library views, Home panels, the Home bar, and menus and dialogs when Menu '
           'theme is Glass or Frost. Frost: lighter. Raised: lit rim, deep shadow. Clear: thin, no blur. Dark: darker.',
    32574: 'Dark: settings menus, dialogs and information pages on dark panels. Glass: on darker glass in the material '
           'of the library view theme. Frost: on light frosted glass over the blurred backdrop.',
    32604: 'All themes',
}
T = {
    'cs_cz': ('Téma knihovny', 'nebo', 'Mráz',
              'Tmavé: nabídky nastavení, dialogy a informační stránky na tmavých panelech. Glass: na tmavším skle v materiálu tématu knihovny. Mráz: na světlém matném skle nad rozmazaným pozadím.',
              'Všechna témata'),
    'da_dk': ('Tema for bibliotek', 'eller', 'Frost',
              'Mørk: indstillingsmenuer, dialoger og informationssider på mørke paneler. Glass: på mørkere glas i bibliotekstemaets materiale. Frost: på lyst frostet glas over den slørede baggrund.',
              'Alle temaer'),
    'de_de': ('Thema der Bibliothek', 'oder', 'Frost',
              'Dunkel: Einstellungsmenüs, Dialoge und Infoseiten auf dunklen Flächen. Glass: auf dunklerem Glas im Material des Bibliotheksthemas. Frost: auf hellem Milchglas über dem unscharfen Hintergrund.',
              'Alle Themen'),
    'el_gr': ('Θέμα βιβλιοθήκης', 'ή', 'Παγωμένο',
              'Σκούρο: μενού ρυθμίσεων, διάλογοι και σελίδες πληροφοριών σε σκούρα πλαίσια. Glass: σε πιο σκούρο γυαλί στο υλικό του θέματος βιβλιοθήκης. Παγωμένο: σε ανοιχτό θαμπό γυαλί πάνω από το θολό φόντο.',
              'Όλα τα θέματα'),
    'es_es': ('Tema de la biblioteca', 'o', 'Escarcha',
              'Oscuro: menús de ajustes, diálogos y páginas de información sobre paneles oscuros. Glass: sobre un cristal más oscuro con el material del tema de la biblioteca. Escarcha: sobre un cristal esmerilado claro encima del fondo desenfocado.',
              'Todos los temas'),
    'fi_fi': ('Kirjastonäkymien teema', 'tai', 'Huurre',
              'Tumma: asetusvalikot, valintaikkunat ja tietosivut tummilla paneeleilla. Glass: tummemmalla lasilla kirjastoteeman materiaalissa. Huurre: vaalealla huurrelasilla sumennetun taustan päällä.',
              'Kaikki teemat'),
    'fr_fr': ('Thème de la bibliothèque', 'ou', 'Givre',
              "Sombre : menus de réglages, dialogues et pages d'information sur des panneaux sombres. Glass : sur un verre plus sombre, dans la matière du thème de la bibliothèque. Givre : sur un verre dépoli clair au-dessus du fond flouté.",
              'Tous les thèmes'),
    'hu_hu': ('Könyvtár témája', 'vagy', 'Dér',
              'Sötét: beállítási menük, párbeszédablakok és információs oldalak sötét paneleken. Glass: sötétebb üvegen, a könyvtár témájának anyagában. Dér: világos matt üvegen az elmosott háttér fölött.',
              'Minden téma'),
    'it_it': ('Tema della libreria', 'o', 'Brina',
              'Scuro: menu delle impostazioni, finestre di dialogo e pagine informative su pannelli scuri. Glass: su un vetro più scuro nel materiale del tema della libreria. Brina: su un vetro smerigliato chiaro sopra lo sfondo sfocato.',
              'Tutti i temi'),
    'ja_jp': ('ライブラリ表示のテーマ', 'または', 'フロスト',
              'ダーク: 設定メニュー、ダイアログ、情報ページを暗いパネルに表示。Glass: ライブラリテーマの素材で、より暗いガラスに表示。フロスト: ぼかした背景の上の明るいすりガラスに表示。',
              'すべてのテーマ'),
    'ko_kr': ('라이브러리 보기 테마', '또는', '프로스트',
              '어둡게: 설정 메뉴, 대화 상자, 정보 페이지를 어두운 패널에 표시합니다. Glass: 라이브러리 테마의 재질로 더 어두운 유리에 표시합니다. 프로스트: 흐린 배경 위의 밝은 반투명 유리에 표시합니다.',
              '모든 테마'),
    'nb_no': ('Tema for bibliotek', 'eller', 'Frost',
              'Mørk: innstillingsmenyer, dialoger og informasjonssider på mørke paneler. Glass: på mørkere glass i bibliotektemaets materiale. Frost: på lyst frostet glass over den uskarpe bakgrunnen.',
              'Alle temaer'),
    'nl_nl': ('Bibliotheekthema', 'of', 'Rijp',
              "Donker: instellingenmenu's, dialogen en informatiepagina's op donkere panelen. Glass: op donkerder glas in het materiaal van het bibliotheekthema. Rijp: op licht matglas boven de vervaagde achtergrond.",
              "Alle thema's"),
    'pl_pl': ('Motyw biblioteki', 'lub', 'Szron',
              'Ciemne: menu ustawień, okna dialogowe i strony informacji na ciemnych panelach. Glass: na ciemniejszym szkle w materiale motywu biblioteki. Szron: na jasnym matowym szkle nad rozmytym tłem.',
              'Wszystkie motywy'),
    'pt_br': ('Tema da biblioteca', 'ou', 'Geada',
              'Escuro: menus de configurações, diálogos e páginas de informações em painéis escuros. Glass: em um vidro mais escuro, no material do tema da biblioteca. Geada: em vidro fosco claro sobre o fundo desfocado.',
              'Todos os temas'),
    'pt_pt': ('Tema da biblioteca', 'ou', 'Geada',
              'Escuro: menus de definições, diálogos e páginas de informação em painéis escuros. Glass: num vidro mais escuro, no material do tema da biblioteca. Geada: em vidro fosco claro sobre o fundo desfocado.',
              'Todos os temas'),
    'ru_ru': ('Тема библиотеки', 'или', 'Иней',
              'Тёмная: меню настроек, диалоги и информационные страницы на тёмных панелях. Glass: на более тёмном стекле в материале темы библиотеки. Иней: на светлом матовом стекле поверх размытого фона.',
              'Все темы'),
    'sv_se': ('Tema för biblioteket', 'eller', 'Frost',
              'Mörk: inställningsmenyer, dialoger och informationssidor på mörka paneler. Glass: på mörkare glas i bibliotekstemats material. Frost: på ljust frostat glas över den suddiga bakgrunden.',
              'Alla teman'),
    'tr_tr': ('Kitaplık teması', 'veya', 'Buzlu',
              'Koyu: ayar menüleri, iletişim kutuları ve bilgi sayfaları koyu panellerde. Glass: kitaplık temasının malzemesinde daha koyu camda. Buzlu: bulanık arka planın üzerinde açık buzlu camda.',
              'Tüm temalar'),
    'uk_ua': ('Тема бібліотеки', 'або', 'Іній',
              'Темна: меню налаштувань, діалоги та інформаційні сторінки на темних панелях. Glass: на темнішому склі в матеріалі теми бібліотеки. Іній: на світлому матовому склі над розмитим тлом.',
              'Усі теми'),
    'zh_cn': ('媒体库视图主题', '或', '磨砂',
              '深色：设置菜单、对话框和信息页显示在深色面板上。Glass：以媒体库主题的材质显示在更深的玻璃上。磨砂：显示在模糊背景上方的浅色磨砂玻璃上。',
              '所有主题'),
    'zh_tw': ('媒體櫃檢視主題', '或', '霧面',
              '深色：設定選單、對話框和資訊頁顯示在深色面板上。Glass：以媒體櫃主題的材質顯示在更深的玻璃上。霧面：顯示在模糊背景上方的淺色霧面玻璃上。',
              '所有主題'),
}


def q(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def set_entry(t, sid, en, tr):
    entry = 'msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, q(en), q(tr))
    pat = re.compile(r'msgctxt "#%d"\nmsgid "(?:[^"\\]|\\.)*"\nmsgstr "(?:[^"\\]|\\.)*"\n' % sid)
    if pat.search(t):
        return pat.sub(lambda m: entry, t, count=1)
    return t.rstrip('\n') + '\n\n' + entry


def main():
    for d in sorted(os.listdir(LANG)):
        code = d.replace('resource.language.', '')
        p = os.path.join(LANG, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        if code == 'en_gb':
            for sid, en in EN.items():
                t = set_entry(t, sid, en, '')
        else:
            name, orw, frost, menuhint, allt = T[code]
            old = re.search(r'msgctxt "#32551"\nmsgid "(?:[^"\\]|\\.)*"\nmsgstr "((?:[^"\\]|\\.)*)"\n', t).group(1)
            hint = old if (' %s %s' % (orw, frost)) in old or ('%s%s' % (orw, frost)) in old else (
                old.replace('Glass', 'Glass%s%s' % ('' if code.startswith('zh') else ' ', orw + ('' if code.startswith('zh') else ' ') + frost), 1))
            t = set_entry(t, 32550, EN[32550], name)
            t = set_entry(t, 32551, EN[32551], hint.replace('\\"', '"'))
            t = set_entry(t, 32574, EN[32574], menuhint)
            t = set_entry(t, 32604, EN[32604], allt)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('ok', len(T) + 1, 'languages')


if __name__ == '__main__':
    main()
