# -*- coding: utf-8 -*-
"""0.40.4 strings 32466-32471: where a palette applies, the Corner boxes and Palette help texts, all languages."""
import io
import os

EN = {
    32466: 'Use the palette for',
    32467: 'Menus and library views',
    32468: 'Menus only',
    32469: 'Library views only',
    32470: "Colors: the colour of the artwork; in the library with the Neutral backdrop and a palette other than Aeon, the palette's own darker box colour. Neutral: always the palette's box colour. Fanart: a window onto the fanart. Backdrop: as the library backdrop. View settings sets it per view.",
    32471: 'Colour of the highlight, the boxes, the strips and the settings pages, for the menus and the library views, the menus only or the library views only. The library background takes it with the Neutral backdrop only.',
}
TR = {
    'cs_cz': ('Použít paletu pro', 'Nabídky a zobrazení knihovny', 'Jen nabídky', 'Jen zobrazení knihovny',
              'Barvy: barva obrázku; v knihovně s neutrálním pozadím a jinou paletou než Aeon vlastní tmavší barva boxů palety. Neutrální: vždy barva boxů palety. Fanart: okno do fanartu. Pozadí: jako pozadí knihovny. Nastavení zobrazení to nastaví pro každé zobrazení.',
              'Barva zvýraznění, boxů, pruhů a stránek nastavení, pro nabídky i zobrazení knihovny, jen pro nabídky nebo jen pro zobrazení knihovny. Pozadí knihovny ji přebírá jen s neutrálním pozadím.'),
    'da_dk': ('Brug paletten til', 'Menuer og biblioteksvisninger', 'Kun menuer', 'Kun biblioteksvisninger',
              'Farver: billedets farve; i biblioteket med neutral baggrund og en anden palet end Aeon, paletens egen mørkere boksfarve. Neutral: altid paletens boksfarve. Fanart: et vindue ind til fanart. Baggrund: som bibliotekets baggrund. Visningsindstillinger sætter det pr. visning.',
              'Farve på markeringen, boksene, striberne og indstillingssiderne, til menuer og biblioteksvisninger, kun menuer eller kun biblioteksvisninger. Bibliotekets baggrund tager den kun med neutral baggrund.'),
    'de_de': ('Palette verwenden für', 'Menüs und Bibliotheksansichten', 'Nur Menüs', 'Nur Bibliotheksansichten',
              'Farben: die Farbe des Bildes; in der Bibliothek mit neutralem Hintergrund und einer anderen Palette als Aeon die eigene, dunklere Boxfarbe der Palette. Neutral: immer die Boxfarbe der Palette. Fanart: ein Fenster auf das Fanart. Hintergrund: wie der Bibliothekshintergrund. Die Ansichtseinstellungen legen es je Ansicht fest.',
              'Farbe der Markierung, der Boxen, der Leisten und der Einstellungsseiten, für Menüs und Bibliotheksansichten, nur für Menüs oder nur für Bibliotheksansichten. Der Bibliothekshintergrund übernimmt sie nur mit neutralem Hintergrund.'),
    'el_gr': ('Χρήση της παλέτας για', 'Μενού και προβολές βιβλιοθήκης', 'Μόνο μενού', 'Μόνο προβολές βιβλιοθήκης',
              'Χρώματα: το χρώμα της εικόνας· στη βιβλιοθήκη με ουδέτερο φόντο και παλέτα άλλη από την Aeon, το δικό της πιο σκούρο χρώμα πλαισίων. Ουδέτερο: πάντα το χρώμα πλαισίων της παλέτας. Fanart: ένα παράθυρο στο fanart. Φόντο: όπως το φόντο της βιβλιοθήκης. Οι ρυθμίσεις προβολής το ορίζουν ανά προβολή.',
              'Χρώμα της επισήμανσης, των πλαισίων, των λωρίδων και των σελίδων ρυθμίσεων, για μενού και προβολές βιβλιοθήκης, μόνο για μενού ή μόνο για προβολές βιβλιοθήκης. Το φόντο της βιβλιοθήκης το παίρνει μόνο με ουδέτερο φόντο.'),
    'es_es': ('Usar la paleta para', 'Menús y vistas de biblioteca', 'Solo menús', 'Solo vistas de biblioteca',
              'Colores: el color de la imagen; en la biblioteca con el fondo neutro y una paleta distinta de Aeon, el color de caja más oscuro de la propia paleta. Neutro: siempre el color de caja de la paleta. Fanart: una ventana al fanart. Fondo: como el fondo de la biblioteca. Los ajustes de vista lo fijan por vista.',
              'Color del resaltado, las cajas, las tiras y las páginas de ajustes, para menús y vistas de biblioteca, solo menús o solo vistas de biblioteca. El fondo de la biblioteca lo toma solo con el fondo neutro.'),
    'fi_fi': ('Käytä palettia', 'Valikot ja kirjastonäkymät', 'Vain valikot', 'Vain kirjastonäkymät',
              'Värit: kuvan väri; kirjastossa neutraalilla taustalla ja muulla paletilla kuin Aeon paletin oma tummempi laatikkoväri. Neutraali: aina paletin laatikkoväri. Fanart: ikkuna fanartiin. Tausta: kuten kirjaston tausta. Näkymäasetukset asettavat sen näkymäkohtaisesti.',
              'Korostuksen, laatikoiden, palkkien ja asetussivujen väri, valikoille ja kirjastonäkymille, vain valikoille tai vain kirjastonäkymille. Kirjaston tausta ottaa sen vain neutraalilla taustalla.'),
    'fr_fr': ('Utiliser la palette pour', 'Menus et vues de la bibliothèque', 'Menus seulement', 'Vues de la bibliothèque seulement',
              "Couleurs : la couleur de l'image ; dans la bibliothèque avec l'arrière-plan neutre et une palette autre qu'Aeon, la couleur de bloc plus sombre de la palette. Neutre : toujours la couleur de bloc de la palette. Fanart : une fenêtre sur le fanart. Arrière-plan : comme l'arrière-plan de la bibliothèque. Les réglages de vue le fixent par vue.",
              "Couleur de la surbrillance, des blocs, des bandeaux et des pages de réglages, pour les menus et les vues de la bibliothèque, les menus seulement ou les vues de la bibliothèque seulement. Le fond de la bibliothèque la prend seulement avec l'arrière-plan neutre."),
    'hu_hu': ('A paletta használata', 'Menük és könyvtárnézetek', 'Csak menük', 'Csak könyvtárnézetek',
              'Színek: a kép színe; a könyvtárban semleges háttérrel és nem Aeon palettával a paletta saját, sötétebb dobozszíne. Semleges: mindig a paletta dobozszíne. Fanart: ablak a fanartra. Háttér: mint a könyvtár háttere. A nézetbeállítások nézetenként állítják.',
              'A kiemelés, a dobozok, a sávok és a beállítási oldalak színe, menükhöz és könyvtárnézetekhez, csak menükhöz vagy csak könyvtárnézetekhez. A könyvtár háttere csak semleges háttérrel veszi át.'),
    'it_it': ('Usa la tavolozza per', 'Menu e viste della libreria', 'Solo menu', 'Solo viste della libreria',
              "Colori: il colore dell'immagine; nella libreria con lo sfondo neutro e una tavolozza diversa da Aeon, il colore dei riquadri più scuro della tavolozza. Neutro: sempre il colore dei riquadri della tavolozza. Fanart: una finestra sul fanart. Sfondo: come lo sfondo della libreria. Le impostazioni vista lo fissano per vista.",
              'Colore di evidenziazione, riquadri, strisce e pagine delle impostazioni, per menu e viste della libreria, solo menu o solo viste della libreria. Lo sfondo della libreria lo prende solo con lo sfondo neutro.'),
    'ja_jp': ('パレットの適用先', 'メニューとライブラリ表示', 'メニューのみ', 'ライブラリ表示のみ',
              'カラー: アートワークの色。ライブラリで背景がニュートラル、パレットが Aeon 以外のときはパレット自身の濃いボックス色。ニュートラル: 常にパレットのボックス色。ファンアート: ファンアートをのぞく窓。背景: ライブラリの背景と同じ。表示設定で表示ごとに設定できます。',
              'ハイライト、ボックス、ストリップ、設定ページの色。メニューとライブラリ表示、メニューのみ、またはライブラリ表示のみに使います。ライブラリの背景はニュートラル背景のときだけこの色になります。'),
    'ko_kr': ('팔레트 적용 대상', '메뉴와 라이브러리 보기', '메뉴만', '라이브러리 보기만',
              '색상: 아트워크의 색. 라이브러리에서 배경이 중립이고 Aeon이 아닌 팔레트이면 팔레트 고유의 더 어두운 상자 색. 중립: 항상 팔레트의 상자 색. 팬아트: 팬아트를 보여 주는 창. 배경: 라이브러리 배경과 같게. 보기 설정에서 보기마다 정합니다.',
              '강조, 상자, 띠, 설정 페이지의 색. 메뉴와 라이브러리 보기, 메뉴만 또는 라이브러리 보기만에 씁니다. 라이브러리 배경은 중립 배경일 때만 이 색을 씁니다.'),
    'nb_no': ('Bruk paletten til', 'Menyer og bibliotekvisninger', 'Bare menyer', 'Bare bibliotekvisninger',
              'Farger: bildets farge; i biblioteket med nøytral bakgrunn og en annen palett enn Aeon, palettens egen mørkere boksfarge. Nøytral: alltid palettens boksfarge. Fanart: et vindu inn til fanart. Bakgrunn: som bibliotekets bakgrunn. Visningsinnstillinger setter det per visning.',
              'Farge på markeringen, boksene, stripene og innstillingssidene, for menyer og bibliotekvisninger, bare menyer eller bare bibliotekvisninger. Bibliotekets bakgrunn tar den bare med nøytral bakgrunn.'),
    'nl_nl': ('Palet gebruiken voor', 'Menu\'s en bibliotheekweergaven', 'Alleen menu\'s', 'Alleen bibliotheekweergaven',
              'Kleuren: de kleur van de afbeelding; in de bibliotheek met de neutrale achtergrond en een ander palet dan Aeon de eigen, donkerdere vakkleur van het palet. Neutraal: altijd de vakkleur van het palet. Fanart: een venster op de fanart. Achtergrond: als de bibliotheekachtergrond. Weergave-instellingen stellen het per weergave in.',
              'Kleur van de markering, de vakken, de stroken en de instellingspagina\'s, voor menu\'s en bibliotheekweergaven, alleen menu\'s of alleen bibliotheekweergaven. De bibliotheekachtergrond neemt hem alleen over met de neutrale achtergrond.'),
    'pl_pl': ('Użyj palety dla', 'Menu i widoki biblioteki', 'Tylko menu', 'Tylko widoki biblioteki',
              'Kolory: kolor grafiki; w bibliotece z neutralnym tłem i paletą inną niż Aeon własny, ciemniejszy kolor pól palety. Neutralne: zawsze kolor pól palety. Fanart: okno na fanart. Tło: jak tło biblioteki. Ustawienia widoku ustawiają to dla każdego widoku.',
              'Kolor podświetlenia, pól, pasków i stron ustawień, dla menu i widoków biblioteki, tylko menu albo tylko widoków biblioteki. Tło biblioteki przyjmuje go tylko z neutralnym tłem.'),
    'pt_br': ('Usar a paleta para', 'Menus e visualizações da biblioteca', 'Só menus', 'Só visualizações da biblioteca',
              'Cores: a cor da imagem; na biblioteca com o fundo neutro e uma paleta diferente de Aeon, a cor de caixa mais escura da própria paleta. Neutro: sempre a cor de caixa da paleta. Fanart: uma janela para o fanart. Fundo: como o fundo da biblioteca. As configurações de visualização definem isso por visualização.',
              'Cor do destaque, das caixas, das faixas e das páginas de configurações, para menus e visualizações da biblioteca, só menus ou só visualizações da biblioteca. O fundo da biblioteca a usa só com o fundo neutro.'),
    'pt_pt': ('Usar a paleta para', 'Menus e vistas da biblioteca', 'Só menus', 'Só vistas da biblioteca',
              'Cores: a cor da imagem; na biblioteca com o fundo neutro e uma paleta diferente de Aeon, a cor de caixa mais escura da própria paleta. Neutro: sempre a cor de caixa da paleta. Fanart: uma janela para o fanart. Fundo: como o fundo da biblioteca. As definições de vista definem-no por vista.',
              'Cor do destaque, das caixas, das faixas e das páginas de definições, para menus e vistas da biblioteca, só menus ou só vistas da biblioteca. O fundo da biblioteca usa-a só com o fundo neutro.'),
    'ru_ru': ('Использовать палитру для', 'Меню и видов библиотеки', 'Только меню', 'Только видов библиотеки',
              'Цвета: цвет обложки; в библиотеке с нейтральным фоном и палитрой не Aeon — собственный более тёмный цвет блоков палитры. Нейтральный: всегда цвет блоков палитры. Фанарт: окно на фанарт. Фон: как фон библиотеки. Настройки вида задают это для каждого вида.',
              'Цвет выделения, блоков, полос и страниц настроек — для меню и видов библиотеки, только для меню или только для видов библиотеки. Фон библиотеки берёт его только при нейтральном фоне.'),
    'sv_se': ('Använd paletten för', 'Menyer och biblioteksvyer', 'Bara menyer', 'Bara biblioteksvyer',
              'Färger: bildens färg; i biblioteket med neutral bakgrund och en annan palett än Aeon, palettens egen mörkare rutfärg. Neutral: alltid palettens rutfärg. Fanart: ett fönster mot fanart. Bakgrund: som bibliotekets bakgrund. Vyinställningar anger det per vy.',
              'Färg på markeringen, rutorna, remsorna och inställningssidorna, för menyer och biblioteksvyer, bara menyer eller bara biblioteksvyer. Bibliotekets bakgrund tar den bara med neutral bakgrund.'),
    'tr_tr': ('Paleti şunlar için kullan', 'Menüler ve kitaplık görünümleri', 'Yalnızca menüler', 'Yalnızca kitaplık görünümleri',
              'Renkler: görselin rengi; kitaplıkta nötr arka plan ve Aeon dışında bir paletle, paletin kendi koyu kutu rengi. Nötr: her zaman paletin kutu rengi. Fanart: fanarta açılan bir pencere. Arka plan: kitaplık arka planı gibi. Görünüm ayarları bunu her görünüm için ayarlar.',
              'Vurgu, kutular, şeritler ve ayar sayfalarının rengi; menüler ve kitaplık görünümleri, yalnızca menüler ya da yalnızca kitaplık görünümleri için. Kitaplık arka planı onu yalnızca nötr arka planla alır.'),
    'uk_ua': ('Використовувати палітру для', 'Меню та видів бібліотеки', 'Лише меню', 'Лише видів бібліотеки',
              'Кольори: колір обкладинки; у бібліотеці з нейтральним тлом і палітрою не Aeon — власний темніший колір блоків палітри. Нейтральний: завжди колір блоків палітри. Фанарт: вікно на фанарт. Тло: як тло бібліотеки. Налаштування виду задають це для кожного виду.',
              'Колір виділення, блоків, смуг і сторінок налаштувань — для меню та видів бібліотеки, лише для меню або лише для видів бібліотеки. Тло бібліотеки бере його лише з нейтральним тлом.'),
    'zh_cn': ('调色板用于', '菜单和媒体库视图', '仅菜单', '仅媒体库视图',
              '色彩：图片的颜色；在媒体库中背景为中性且调色板不是 Aeon 时，使用调色板自己较深的方框颜色。中性：始终使用调色板的方框颜色。同人画：看到同人画的窗口。背景：与媒体库背景相同。视图设置可按视图设定。',
              '高亮、方框、条带和设置页面的颜色，用于菜单和媒体库视图、仅菜单或仅媒体库视图。媒体库背景仅在中性背景时使用它。'),
    'zh_tw': ('調色盤用於', '選單和媒體櫃檢視', '僅選單', '僅媒體櫃檢視',
              '色彩：圖片的顏色；在媒體櫃中背景為中性且調色盤不是 Aeon 時，使用調色盤自己較深的方框顏色。中性：一律使用調色盤的方框顏色。同人畫：看到同人畫的視窗。背景：與媒體櫃背景相同。檢視設定可依檢視設定。',
              '醒目提示、方框、條帶和設定頁面的顏色，用於選單和媒體櫃檢視、僅選單或僅媒體櫃檢視。媒體櫃背景僅在中性背景時使用它。'),
}
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32466"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else tr[i].replace('"', '\\"')
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32466-32471 added in %d languages' % done)
