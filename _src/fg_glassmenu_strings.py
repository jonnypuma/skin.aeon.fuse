# -*- coding: utf-8 -*-
"""0.53.0 strings: Menu theme in Fused Glass (Dark | Glass, help), Backgrounds > Home bar (Off | Bar | Keys | Shelf,
help) and the corrected help of Look > Material (32551: it names what the material changes). Each help text names
the Look category and the material choices as that language's skin strings call them (31726, 32547-32549, Kodi's
Today). Help texts fit the Skin settings help box (two lines, 1250 px of Figtree 20). Run from the skin folder before
_src/fg_glassmenus.py (which measures the pill labels); writes or rewrites the strings in every language."""
import io
import os
import re

KEYS = (32551, 32573, 32574, 32575, 32576, 32577, 32578, 32579)
SKIN = {
    32551: 'The glass of the frosted panels: library views, Home panels, the Home bar, and menus and dialogs when Menu '
           'theme is Glass. Frost: lighter. Raised: lit rim, deep shadow. Clear: thin, no blur. Today: darker.',
    32573: 'Dark',
    32574: 'Dark: settings menus, dialogs and information pages on dark panels. Glass: on frosted glass in the material '
           'chosen under Look.',
    32575: 'Home bar',
    32576: 'Bar',
    32577: 'Keys',
    32578: 'Shelf',
    32579: 'Frosted glass behind the Home menu, in the material chosen under Look. Bar: one capsule. Keys: glass under '
           'each icon. Shelf: a band across the screen.',
}
TR = {
    'cs_cz': ('Sklo matných panelů: zobrazení knihovny, panely Domů, lišta Domů a nabídky a dialogy, je-li Téma nabídek Glass. Mráz: světlejší. Vyvýšené: světlý okraj, hluboký stín. Čiré: tenké, bez rozostření. Dnes: tmavší.',
              'Tmavé',
              'Tmavé: nabídky nastavení, dialogy a informační stránky na tmavých panelech. Glass: na matném skle v materiálu zvoleném ve Styl.',
              'Lišta Domů', 'Kapsle', 'Klávesy', 'Pás',
              'Matné sklo za nabídkou Domů v materiálu zvoleném ve Styl. Kapsle: jedna kapsle. Klávesy: sklo pod každou ikonou. Pás: pruh přes celou obrazovku.'),
    'da_dk': ('Glasset i de matte paneler: biblioteksvisninger, hjemmepaneler, hjemmebjælken samt menuer og dialoger, når Menutema er Glass. Frost: lysere. Hævet: lys kant, dyb skygge. Klar: tyndt, ingen sløring. I dag: mørkere.',
              'Mørk',
              'Mørk: indstillingsmenuer, dialoger og infosider på mørke paneler. Glass: på matteret glas i materialet valgt under Stil.',
              'Hjemmebjælke', 'Bjælke', 'Taster', 'Hylde',
              'Matteret glas bag hjemmemenuen i materialet valgt under Stil. Bjælke: én kapsel. Taster: glas under hvert ikon. Hylde: et bånd over hele skærmen.'),
    'de_de': ('Das Glas der Milchglasflächen: Bibliotheksansichten, Startseiten-Felder, die Startleiste sowie Menüs und Dialoge bei Menüthema Glass. Frost: heller. Erhaben: heller Rand, tiefer Schatten. Klar: dünn. Heute: dunkler.',
              'Dunkel',
              'Dunkel: Einstellungsmenüs, Dialoge und Infoseiten auf dunklen Flächen. Glass: auf Milchglas im unter Aussehen gewählten Material.',
              'Startleiste', 'Leiste', 'Tasten', 'Band',
              'Milchglas hinter dem Hauptmenü im unter Aussehen gewählten Material. Leiste: eine Kapsel. Tasten: Glas unter jedem Symbol. Band: über die ganze Breite.'),
    'el_gr': ('Γυαλί των θαμπών πλαισίων: βιβλιοθήκη, πλαίσια και μπάρα Αρχικής, μενού και διάλογοι με Θέμα μενού Glass. Παγωμένο: πιο ανοιχτό. Ανυψωμένο: φωτεινό χείλος, βαθιά σκιά. Διάφανο: λεπτό. Σήμερα: πιο σκούρο.',
              'Σκούρο',
              'Σκούρο: μενού ρυθμίσεων, διάλογοι και σελίδες πληροφοριών σε σκούρα πλαίσια. Glass: σε θαμπό γυαλί με το υλικό της Όψης.',
              'Μπάρα Αρχικής', 'Μπάρα', 'Πλήκτρα', 'Ράφι',
              'Θαμπό γυαλί πίσω από το κεντρικό μενού, με το υλικό της Όψης. Μπάρα: μία κάψουλα. Πλήκτρα: γυαλί κάτω από κάθε εικονίδιο. Ράφι: λωρίδα σε όλο το πλάτος.'),
    'es_es': ('Cristal de los paneles esmerilados: biblioteca, paneles y barra de Inicio, y menús y diálogos con el tema Glass. Escarcha: más claro. Elevado: borde iluminado, sombra profunda. Claro: fino. Hoy: más oscuro.',
              'Oscuro',
              'Oscuro: menús de ajustes, diálogos y páginas de información sobre paneles oscuros. Glass: sobre cristal esmerilado con el material de Aspecto.',
              'Barra de Inicio', 'Barra', 'Teclas', 'Estante',
              'Cristal esmerilado tras el menú de inicio, con el material de Aspecto. Barra: una cápsula. Teclas: cristal bajo cada icono. Estante: una banda de lado a lado.'),
    'fi_fi': ('Huurrepaneelien lasi: kirjastonäkymät, aloitusnäytön paneelit ja palkki sekä valikot ja ikkunat, kun Valikkoteema on Glass. Huurre: vaaleampi. Kohotettu: valaistu reuna, syvä varjo. Kirkas: ohut. Tänään: tummempi.',
              'Tumma',
              'Tumma: asetusvalikot, valintaikkunat ja tietosivut tummilla paneeleilla. Glass: huurrelasilla, Tyyli-kohdan materiaalilla.',
              'Aloituspalkki', 'Palkki', 'Näppäimet', 'Hylly',
              'Huurrelasi aloitusvalikon takana, Tyyli-kohdan materiaalilla. Palkki: yksi kapseli. Näppäimet: lasi jokaisen kuvakkeen alla. Hylly: kaista koko leveydeltä.'),
    'fr_fr': ("Le verre des panneaux dépolis : vues de la bibliothèque, panneaux et barre d'accueil, et menus et dialogues avec le thème Glass. Givre : plus clair. Surélevé : bord éclairé, ombre profonde. Clair : fin. Aujourd'hui : plus sombre.",
              'Sombre',
              "Sombre : menus de réglages, dialogues et pages d'infos sur panneaux sombres. Glass : sur verre dépoli, dans la matière choisie sous Aspect.",
              "Barre d'accueil", 'Barre', 'Touches', 'Étagère',
              "Verre dépoli derrière le menu d'accueil, dans la matière choisie sous Aspect. Barre : une capsule. Touches : du verre sous chaque icône. Étagère : une bande sur toute la largeur."),
    'hu_hu': ('A matt panelek üvege: könyvtárnézetek, kezdőpanelek, a kezdősáv, valamint menük és párbeszédek Glass menütémánál. Dér: világosabb. Kiemelt: fényes perem, mély árnyék. Átlátszó: vékony. Ma: sötétebb.',
              'Sötét',
              'Sötét: beállítási menük, párbeszédek és infóoldalak sötét paneleken. Glass: matt üvegen, a Stílus alatt választott anyaggal.',
              'Kezdősáv', 'Sáv', 'Gombok', 'Polc',
              'Matt üveg a kezdőmenü mögött, a Stílus alatt választott anyaggal. Sáv: egy kapszula. Gombok: üveg minden ikon alatt. Polc: sáv a teljes szélességben.'),
    'it_it': ('Il vetro dei pannelli satinati: viste della libreria, pannelli e barra Home, e menu e dialoghi con il tema Glass. Brina: più chiaro. Rialzato: bordo luminoso, ombra profonda. Trasparente: sottile. Oggi: più scuro.',
              'Scuro',
              'Scuro: menu delle impostazioni, dialoghi e pagine info su pannelli scuri. Glass: su vetro satinato, nel materiale scelto in Stile.',
              'Barra Home', 'Barra', 'Tasti', 'Mensola',
              'Vetro satinato dietro il menu Home, nel materiale scelto in Stile. Barra: una capsula. Tasti: vetro sotto ogni icona. Mensola: una fascia da bordo a bordo.'),
    'ja_jp': ('すりガラスのパネルのガラス: ライブラリ表示、ホームのパネルとホームバー、メニューのテーマが Glass のときのメニューとダイアログ。フロスト: 明るめ。レイズド: 光る縁と深い影。クリア: 薄い。今日: 暗め。',
              'ダーク',
              'ダーク: 設定メニュー、ダイアログ、情報ページを暗いパネルに表示。Glass: 外観で選んだ素材のすりガラスに表示。',
              'ホームバー', 'バー', 'キー', 'シェルフ',
              'ホームメニューの後ろのすりガラス (外観で選んだ素材)。バー: 1 つのカプセル。キー: 各アイコンの下にガラス。シェルフ: 画面幅の帯。'),
    'ko_kr': ('반투명 패널의 유리: 라이브러리 보기, 홈 패널과 홈 바, 메뉴 테마가 Glass일 때 메뉴와 대화 상자. 프로스트: 더 밝게. 돋움: 빛나는 테두리, 깊은 그림자. 투명: 얇게. 오늘: 더 어둡게.',
              '어둡게',
              '어둡게: 설정 메뉴, 대화 상자, 정보 페이지를 어두운 패널에 표시. Glass: 모양에서 고른 재질의 반투명 유리에 표시.',
              '홈 바', '바', '키', '선반',
              '홈 메뉴 뒤의 반투명 유리 (모양에서 고른 재질). 바: 캡슐 하나. 키: 아이콘마다 유리. 선반: 화면 너비의 띠.'),
    'nb_no': ('Glasset i de matte panelene: biblioteksvisninger, hjemmepaneler, hjemmelinjen og menyer og dialoger når Menytema er Glass. Frost: lysere. Hevet: lys kant, dyp skygge. Klar: tynt, uten uskarphet. I dag: mørkere.',
              'Mørk',
              'Mørk: innstillingsmenyer, dialoger og infosider på mørke paneler. Glass: på matt glass i materialet valgt under Stil.',
              'Hjemmelinje', 'Linje', 'Taster', 'Hylle',
              'Matt glass bak hjemmemenyen i materialet valgt under Stil. Linje: én kapsel. Taster: glass under hvert ikon. Hylle: et bånd over hele skjermen.'),
    'nl_nl': ("Het glas van de matglazen panelen: bibliotheekweergaven, panelen en balk van het hoofdscherm, en menu's en dialogen bij Menuthema Glass. Rijp: lichter. Verhoogd: lichte rand, diepe schaduw. Helder: dun. Vandaag: donkerder.",
              'Donker',
              "Donker: instellingenmenu's, dialogen en infopagina's op donkere panelen. Glass: op matglas, in het materiaal gekozen onder Stijl.",
              'Hoofdmenubalk', 'Balk', 'Toetsen', 'Plank',
              'Matglas achter het hoofdmenu, in het materiaal gekozen onder Stijl. Balk: één capsule. Toetsen: glas onder elk pictogram. Plank: een band over de hele breedte.'),
    'pl_pl': ('Szkło matowych paneli: widoki biblioteki, panele i pasek ekranu głównego oraz menu i okna dialogowe przy motywie Glass. Szron: jaśniejsze. Uniesione: jasna krawędź, głęboki cień. Przejrzyste: cienkie. Dzisiaj: ciemniejsze.',
              'Ciemne',
              'Ciemne: menu ustawień, okna dialogowe i strony informacji na ciemnych panelach. Glass: na matowym szkle w materiale wybranym w Styl.',
              'Pasek główny', 'Pasek', 'Klawisze', 'Półka',
              'Matowe szkło za menu głównym w materiale wybranym w Styl. Pasek: jedna kapsuła. Klawisze: szkło pod każdą ikoną. Półka: pas na całą szerokość.'),
    'pt_br': ('O vidro dos painéis foscos: visualizações da biblioteca, painéis e barra do início, e menus e diálogos com o tema Glass. Geada: mais claro. Elevado: borda iluminada, sombra profunda. Transparente: fino. Hoje: mais escuro.',
              'Escuro',
              'Escuro: menus de configurações, diálogos e páginas de informação em painéis escuros. Glass: em vidro fosco, no material escolhido em Visual.',
              'Barra inicial', 'Barra', 'Teclas', 'Prateleira',
              'Vidro fosco atrás do menu inicial, no material escolhido em Visual. Barra: uma cápsula. Teclas: vidro sob cada ícone. Prateleira: uma faixa de lado a lado.'),
    'pt_pt': ('O vidro dos painéis foscos: vistas da biblioteca, painéis e barra do início, e menus e diálogos com o tema Glass. Geada: mais claro. Elevado: rebordo iluminado, sombra profunda. Transparente: fino. Hoje: mais escuro.',
              'Escuro',
              'Escuro: menus de definições, diálogos e páginas de informação em painéis escuros. Glass: em vidro fosco, no material escolhido em Aspeto.',
              'Barra inicial', 'Barra', 'Teclas', 'Prateleira',
              'Vidro fosco atrás do menu inicial, no material escolhido em Aspeto. Barra: uma cápsula. Teclas: vidro sob cada ícone. Prateleira: uma faixa de lado a lado.'),
    'ru_ru': ('Стекло матовых панелей: виды библиотеки, панели и полоса главного экрана, а также меню и диалоги при теме Glass. Иней: светлее. Приподнятый: светлый край, глубокая тень. Прозрачный: тонкое. Сегодня: темнее.',
              'Тёмная',
              'Тёмная: меню настроек, диалоги и страницы сведений на тёмных панелях. Glass: на матовом стекле из материала во Внешнем виде.',
              'Полоса меню', 'Полоса', 'Клавиши', 'Полка',
              'Матовое стекло за главным меню из материала во Внешнем виде. Полоса: одна капсула. Клавиши: стекло под каждым значком. Полка: лента во всю ширину.'),
    'sv_se': ('Glaset i de frostade panelerna: biblioteksvyer, hempaneler, hemlisten samt menyer och dialoger när Menytema är Glass. Frost: ljusare. Upphöjd: ljus kant, djup skugga. Klar: tunt, ingen oskärpa. Idag: mörkare.',
              'Mörk',
              'Mörk: inställningsmenyer, dialoger och infosidor på mörka paneler. Glass: på frostat glas i materialet valt under Stil.',
              'Hemlist', 'List', 'Tangenter', 'Hylla',
              'Frostat glas bakom hemmenyn i materialet valt under Stil. List: en kapsel. Tangenter: glas under varje ikon. Hylla: ett band över hela skärmen.'),
    'tr_tr': ('Buzlu panellerin camı: kitaplık görünümleri, ana ekran panelleri ve çubuğu, Menü teması Glass iken menüler ve iletişim kutuları. Buzlu: daha açık. Yükseltilmiş: parlak kenar, derin gölge. Şeffaf: ince. Bugün: daha koyu.',
              'Koyu',
              'Koyu: ayar menüleri, iletişim kutuları ve bilgi sayfaları koyu panellerde. Glass: Tarz altında seçilen malzemede buzlu camda.',
              'Ana çubuk', 'Çubuk', 'Tuşlar', 'Raf',
              'Ana menünün arkasında, Tarz altında seçilen malzemede buzlu cam. Çubuk: tek kapsül. Tuşlar: her simgenin altında cam. Raf: ekran boyunca bir şerit.'),
    'uk_ua': ('Скло матових панелей: види бібліотеки, панелі й смуга головного екрана, а також меню й діалоги з темою Glass. Іній: світліше. Піднятий: світлий край, глибока тінь. Прозорий: тонке. Сьогодні: темніше.',
              'Темна',
              'Темна: меню налаштувань, діалоги й сторінки відомостей на темних панелях. Glass: на матовому склі з матеріалу у Вигляді.',
              'Смуга меню', 'Смуга', 'Клавіші', 'Полиця',
              'Матове скло за головним меню з матеріалу у Вигляді. Смуга: одна капсула. Клавіші: скло під кожною піктограмою. Полиця: стрічка на всю ширину.'),
    'zh_cn': ('磨砂面板的玻璃：媒体库视图、主页面板和主页栏，以及菜单主题为 Glass 时的菜单和对话框。磨砂：更亮。浮起：亮边、深阴影。透明：薄。今天：更暗。',
              '深色',
              '深色：设置菜单、对话框和信息页使用深色面板。Glass：使用在样式中所选材质的磨砂玻璃。',
              '主页栏', '长条', '按键', '横架',
              '主页菜单后的磨砂玻璃，使用在样式中所选的材质。长条：一个胶囊。按键：每个图标下有玻璃。横架：横贯屏幕的玻璃带。'),
    'zh_tw': ('霧面面板的玻璃：媒體櫃檢視、主頁面板和主頁列，以及選單主題為 Glass 時的選單和對話框。霧面：較亮。浮起：亮邊、深陰影。透明：薄。今天：較暗。',
              '深色',
              '深色：設定選單、對話框和資訊頁使用深色面板。Glass：使用在樣式中所選材質的霧面玻璃。',
              '主頁列', '長條', '按鍵', '橫架',
              '主頁選單後的霧面玻璃，使用在樣式中所選的材質。長條：一個膠囊。按鍵：每個圖示下有玻璃。橫架：橫貫螢幕的玻璃帶。'),
}


def esc(text):
    return text.replace('\\', '\\\\').replace('"', '\\"')


def write(folder):
    done = 0
    for d in sorted(os.listdir(folder)):
        lang = d.replace('resource.language.', '')
        p = os.path.join(folder, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        tr = TR.get(lang)
        assert tr or lang == 'en_gb', lang
        for i, ident in enumerate(KEYS):
            entry = 'msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, esc(SKIN[ident]), '' if lang == 'en_gb' else esc(tr[i]))
            old = re.compile(r'msgctxt "#%d"\nmsgid ".*"\nmsgstr ".*"\n' % ident)
            if old.search(t):
                t = old.sub(lambda _m: entry, t, count=1)
            else:
                t = t.rstrip('\n') + '\n\n' + entry
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        done += 1
    return done


assert len(TR) == 22 and all(len(v) == len(KEYS) for v in TR.values())
print('skin', write('language'), 'languages')
