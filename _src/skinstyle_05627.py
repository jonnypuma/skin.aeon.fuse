# -*- coding: utf-8 -*-
"""0.56.27 Skin style (the user, 2026-11-17: keep the Fused Glass menu themes, let the library follow them, no Library
view theme option, call the row "Skin style" in all three themes, drop Raised). Idempotent; run from the skin folder,
then _src/skin_previews.py, _src/fg_material.py, _src/ok_only.py.

- Row 9748 (string 32250) is named Skin style everywhere. Aeon / Aeon Glass: only the name changes (Mosaic, Ledger,
  Bridge, Tab slab, Fuse / Aeon Glass, Fuse).
- Fused Glass: Dark | Clear | Frost (aeon.fgmenu '' / glass / frost; "Glass" is named Clear, string 32549). OK on the
  row sets the library's glass with it (aeon.fgmat '' / clear / frost), so library views, Home panels, the Home bar,
  the player, Planner and the screensaver follow the style; script.aeon.helper 0.3.103 puts aeon.fgmat in step at start.
- Row 9529 (Library view theme) is hidden; Raised is gone with it. Help 32574 says what the style covers.
- The Fused Glass style (the System-style menus) joins later as the fourth value.
"""
import io
import os
import re

D = '1080i'
L = 'language'
SET = os.path.join(D, 'SkinSettings.xml')

EN = {32250: 'Skin style',
      32574: ('How menus and glass panels look: settings, dialogs, information pages, library views, Home panels, the Home bar, '
              'the player and the screensaver. Dark: dark panels. Clear: thin glass that shows more of the backdrop. Frost: light '
              'frosted glass over the blurred backdrop.')}
T = {
    'cs_cz': ('Styl vzhledu', 'Jak vypadají nabídky a skleněné panely: nastavení, dialogy, informační stránky, zobrazení knihovny, panely a lišta Domů, přehrávač a spořič obrazovky. Tmavé: tmavé panely. Čiré: tenké sklo, které ukazuje víc z pozadí. Mráz: světlé matné sklo nad rozmazaným pozadím.'),
    'da_dk': ('Skin-stil', 'Hvordan menuer og glaspaneler ser ud: indstillinger, dialoger, informationssider, biblioteksvisninger, hjemmepaneler og hjemmebjælken, afspilleren og pauseskærmen. Mørk: mørke paneler. Klar: tyndt glas, der viser mere af baggrunden. Frost: lyst frostet glas over den slørede baggrund.'),
    'de_de': ('Skin-Stil', 'Wie Menüs und Glasflächen aussehen: Einstellungen, Dialoge, Infoseiten, Bibliotheksansichten, Startseiten-Felder und Startleiste, Player und Bildschirmschoner. Dunkel: dunkle Flächen. Klar: dünnes Glas, das mehr vom Hintergrund zeigt. Frost: helles Milchglas über dem unscharfen Hintergrund.'),
    'el_gr': ('Στυλ κελύφους', 'Πώς φαίνονται τα μενού και τα γυάλινα πλαίσια: ρυθμίσεις, διάλογοι, σελίδες πληροφοριών, προβολές βιβλιοθήκης, πλαίσια και μπάρα Αρχικής, πρόγραμμα αναπαραγωγής και προφύλαξη οθόνης. Σκούρο: σκούρα πλαίσια. Διάφανο: λεπτό γυαλί που δείχνει περισσότερο φόντο. Παγωμένο: ανοιχτό θαμπό γυαλί πάνω από το θολό φόντο.'),
    'es_es': ('Estilo de la skin', 'Cómo se ven los menús y los paneles de cristal: ajustes, diálogos, páginas de información, vistas de la biblioteca, paneles y barra de Inicio, el reproductor y el salvapantallas. Oscuro: paneles oscuros. Claro: cristal fino que deja ver más el fondo. Escarcha: cristal esmerilado claro sobre el fondo desenfocado.'),
    'fi_fi': ('Ulkoasun tyyli', 'Miltä valikot ja lasipaneelit näyttävät: asetukset, valintaikkunat, tietosivut, kirjastonäkymät, aloitusnäytön paneelit ja palkki, soitin ja näytönsäästäjä. Tumma: tummat paneelit. Kirkas: ohut lasi, josta taustaa näkyy enemmän. Huurre: vaalea huurrelasi sumennetun taustan päällä.'),
    'fr_fr': ('Style du skin', "L'aspect des menus et des panneaux de verre : réglages, dialogues, pages d'information, vues de la bibliothèque, panneaux et barre d'accueil, lecteur et économiseur d'écran. Sombre : panneaux sombres. Clair : verre fin qui laisse voir davantage le fond. Givre : verre dépoli clair au-dessus du fond flouté."),
    'hu_hu': ('A felület stílusa', 'Hogyan néznek ki a menük és az üvegpanelek: beállítások, párbeszédablakok, információs oldalak, könyvtárnézetek, a kezdőképernyő panelei és sávja, a lejátszó és a képernyővédő. Sötét: sötét panelek. Átlátszó: vékony üveg, amelyen több látszik a háttérből. Dér: világos matt üveg az elmosott háttér fölött.'),
    'it_it': ('Stile della skin', "L'aspetto di menu e pannelli di vetro: impostazioni, finestre di dialogo, pagine informative, viste della libreria, pannelli e barra Home, lettore e salvaschermo. Scuro: pannelli scuri. Trasparente: vetro sottile che mostra di più lo sfondo. Brina: vetro smerigliato chiaro sopra lo sfondo sfocato."),
    'ja_jp': ('スキンのスタイル', 'メニューとガラスパネルの見た目: 設定、ダイアログ、情報ページ、ライブラリ表示、ホームのパネルとホームバー、プレーヤー、スクリーンセーバー。ダーク: 暗いパネル。クリア: 背景がよく見える薄いガラス。フロスト: ぼかした背景の上の明るいすりガラス。'),
    'ko_kr': ('스킨 스타일', '메뉴와 유리 패널의 모습: 설정, 대화 상자, 정보 페이지, 라이브러리 보기, 홈 패널과 홈 바, 플레이어, 화면 보호기. 어둡게: 어두운 패널. 투명: 배경이 더 많이 보이는 얇은 유리. 프로스트: 흐린 배경 위의 밝은 반투명 유리.'),
    'nb_no': ('Draktstil', 'Hvordan menyer og glasspaneler ser ut: innstillinger, dialoger, informasjonssider, biblioteksvisninger, hjemmepaneler og hjemmelinjen, avspilleren og skjermspareren. Mørk: mørke paneler. Klar: tynt glass som viser mer av bakgrunnen. Frost: lyst frostet glass over den uskarpe bakgrunnen.'),
    'nl_nl': ('Skinstijl', "Hoe menu's en glazen panelen eruitzien: instellingen, dialogen, informatiepagina's, bibliotheekweergaven, panelen en balk van het hoofdscherm, de speler en de schermbeveiliging. Donker: donkere panelen. Helder: dun glas dat meer van de achtergrond laat zien. Rijp: licht matglas boven de vervaagde achtergrond."),
    'pl_pl': ('Styl skórki', 'Wygląd menu i szklanych paneli: ustawienia, okna dialogowe, strony informacji, widoki biblioteki, panele i pasek ekranu głównego, odtwarzacz i wygaszacz ekranu. Ciemne: ciemne panele. Przejrzyste: cienkie szkło, przez które widać więcej tła. Szron: jasne matowe szkło nad rozmytym tłem.'),
    'pt_br': ('Estilo da skin', 'Como ficam os menus e os painéis de vidro: configurações, diálogos, páginas de informações, visualizações da biblioteca, painéis e barra do início, o player e o protetor de tela. Escuro: painéis escuros. Transparente: vidro fino que mostra mais do fundo. Geada: vidro fosco claro sobre o fundo desfocado.'),
    'pt_pt': ('Estilo do skin', 'Como ficam os menus e os painéis de vidro: definições, diálogos, páginas de informação, vistas da biblioteca, painéis e barra do início, o leitor e a proteção de ecrã. Escuro: painéis escuros. Transparente: vidro fino que mostra mais do fundo. Geada: vidro fosco claro sobre o fundo desfocado.'),
    'ru_ru': ('Стиль обложки', 'Как выглядят меню и стеклянные панели: настройки, диалоги, информационные страницы, виды библиотеки, панели и полоса главного экрана, проигрыватель и заставка. Тёмная: тёмные панели. Прозрачный: тонкое стекло, сквозь которое виднее фон. Иней: светлое матовое стекло поверх размытого фона.'),
    'sv_se': ('Skalstil', 'Hur menyer och glaspaneler ser ut: inställningar, dialoger, informationssidor, biblioteksvyer, hempaneler och hemlisten, spelaren och skärmsläckaren. Mörk: mörka paneler. Klar: tunt glas som visar mer av bakgrunden. Frost: ljust frostat glas över den suddiga bakgrunden.'),
    'tr_tr': ('Kaplama stili', 'Menülerin ve cam panellerin görünümü: ayarlar, iletişim kutuları, bilgi sayfaları, kitaplık görünümleri, ana ekran panelleri ve çubuğu, oynatıcı ve ekran koruyucu. Koyu: koyu paneller. Şeffaf: arka planı daha çok gösteren ince cam. Buzlu: bulanık arka planın üzerinde açık buzlu cam.'),
    'uk_ua': ('Стиль оболонки', 'Як виглядають меню та скляні панелі: налаштування, діалоги, інформаційні сторінки, види бібліотеки, панелі й смуга головного екрана, програвач і заставка. Темна: темні панелі. Прозорий: тонке скло, крізь яке видно більше тла. Іній: світле матове скло над розмитим тлом.'),
    'zh_cn': ('皮肤风格', '菜单和玻璃面板的外观：设置、对话框、信息页、媒体库视图、主页面板和主页栏、播放器和屏幕保护程序。深色：深色面板。透明：薄玻璃，能看到更多背景。磨砂：模糊背景上方的浅色磨砂玻璃。'),
    'zh_tw': ('面板風格', '選單和玻璃面板的外觀：設定、對話框、資訊頁、媒體櫃檢視、主頁面板和主頁列、播放器和螢幕保護程式。深色：深色面板。透明：薄玻璃，能看到更多背景。霧面：模糊背景上方的淺色霧面玻璃。'),
}


def strings():
    for d in sorted(os.listdir(L)):
        code = d.replace('resource.language.', '')
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        for i, sid in enumerate((32250, 32574)):
            rx = re.compile(r'(msgctxt "#%d"\nmsgid ")[^\n]*("\nmsgstr ")[^\n]*(")' % sid)
            assert len(rx.findall(t)) == 1, (code, sid)
            new = '' if code == 'en_gb' else T[code][i].replace('"', '\\"')
            t = rx.sub(lambda m: m.group(1) + EN[sid] + m.group(2) + new + m.group(3), t)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('strings: 23 languages')


def settings():
    t = io.open(SET, encoding='utf-8').read()
    # the Library view theme row: hidden (the grouplist closes up; navigation passes it)
    old = '<control type="group"><!-- row 9529 -->\n\t\t<width>1100</width><height>70</height>\n\t\t<visible>$EXP[Aeon_FGlass]</visible>'
    new = ('<control type="group"><!-- row 9529 -->\n\t\t<width>1100</width><height>70</height>\n\t\t<visible>false</visible>'
           '<!-- 0.56.27 Skin style: the library follows the style (_src/skinstyle_05627.py) -->')
    if new not in t and 'expert_05628' not in t:          # 0.56.28: row 9529 is Panel shadow (expert_05628.py)
        assert t.count(old) == 1, t.count(old)
        t = t.replace(old, new)
    # row 9748: OK sets the library's glass with the style
    pairs = (
        ('<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),glass)">Skin.SetString(aeon.fgmenu,frost)</onclick>',
         '<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),glass)">Skin.SetString(aeon.fgmat,frost)</onclick>'),
        ('<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.Reset(aeon.fgmenu)</onclick>',
         '<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.Reset(aeon.fgmat)</onclick>'),
        ('<onclick condition="Skin.HasSetting(aeon.fglass) + !String.IsEqual(Skin.String(aeon.fgmenu),glass) + !String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.SetString(aeon.fgmenu,glass)</onclick>',
         '<onclick condition="Skin.HasSetting(aeon.fglass) + !String.IsEqual(Skin.String(aeon.fgmenu),glass) + !String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.SetString(aeon.fgmat,clear)</onclick>'),
    )
    if 'RunScript(script.aeon.helper,skinstyle)' in t:     # 0.56.29: the helper steps the style (fgs_05629.py)
        io.open(SET, 'w', encoding='utf-8', newline='\n').write(t)
        print('settings rows written (0.56.29 row)')
        return
    for old, add in pairs:
        if add not in t:
            assert t.count(old) == 1, old[:80]
            t = t.replace(old, old + '\n\t\t\t\t\t' + add)
    # row 9748's Fused Glass pills: Glass is named Clear
    i = t.index('<!-- Fused Glass (0.56.12): Dark (default) | Glass | Frost, aeon.fgmenu (_src/fg_frostmenus.py) -->')
    j = t.index('</control>\n', t.index('$ADDON[skin.aeon.fuse 32547]', i))
    j = t.index('<!-- row', j) if '<!-- row' in t[j:j + 20000] else j
    seg = t[i:j]
    n = seg.count('<label>Glass</label>')
    assert n in (0, 4), n
    seg = seg.replace('<label>Glass</label>', '<label>$ADDON[skin.aeon.fuse 32549]</label>')
    t = t[:i] + seg + t[j:]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(t)
    print('settings rows written')


if __name__ == '__main__':
    strings()
    settings()
