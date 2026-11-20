# -*- coding: utf-8 -*-
"""0.56.41 the setup wizard's theme texts (the user: "Fused Glass and Aeon Glass sound the same in description. What you
need to describe Aeon Glass is Aeon with glass menus basically, no palettes"), all 23 languages. Replaces msgid /
msgstr; repeatable."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
IDS = (32713, 32694, 32714, 32701, 32050)
EN = ('Aeon: solid panels in a palette you pick. Aeon Glass: the same Aeon layout and views with glass menus, no palettes. Fused Glass: its own library views, rounded glass cards over the artwork.',
      'Its own library views and menus: rounded glass cards with soft shadows float over the artwork, in Dark, Clear, Frost or the Fused Glass style.',
      'Its own views, glass cards',
      'Aeon with glass menus: the same layout and library views as Aeon, with see-through glass menus and dialogs instead of solid ones. No palettes.',
      'Aeon with glass menus, no palettes')
T = {
    'cs_cz': ('Aeon: plné panely v paletě, kterou si vyberete. Aeon Glass: stejné rozvržení a zobrazení Aeon se skleněnými nabídkami, bez palet. Fused Glass: vlastní zobrazení knihovny, zaoblené skleněné karty nad obrázky.',
              'Vlastní zobrazení knihovny a nabídky: zaoblené skleněné karty s jemnými stíny se vznášejí nad obrázky, ve stylu Tmavý, Čirý, Matný nebo Fused Glass.',
              'Vlastní zobrazení, skleněné karty',
              'Aeon se skleněnými nabídkami: stejné rozvržení a zobrazení knihovny jako Aeon, s průhlednými skleněnými nabídkami a dialogy místo plných. Bez palet.',
              'Aeon se skleněnými nabídkami, bez palet'),
    'da_dk': ('Aeon: faste paneler i en palet, du vælger. Aeon Glass: samme Aeon-layout og visninger med glasmenuer, uden paletter. Fused Glass: egne biblioteksvisninger, afrundede glaskort over billederne.',
              'Egne biblioteksvisninger og menuer: afrundede glaskort med bløde skygger svæver over billederne, i stilen Mørk, Klar, Frost eller Fused Glass.',
              'Egne visninger, glaskort',
              'Aeon med glasmenuer: samme layout og biblioteksvisninger som Aeon, med gennemsigtige glasmenuer og dialoger i stedet for faste. Ingen paletter.',
              'Aeon med glasmenuer, uden paletter'),
    'de_de': ('Aeon: feste Flächen in einer Palette deiner Wahl. Aeon Glass: dasselbe Aeon-Layout und dieselben Ansichten mit Glasmenüs, ohne Paletten. Fused Glass: eigene Bibliotheksansichten, abgerundete Glaskarten über den Bildern.',
              'Eigene Bibliotheksansichten und Menüs: abgerundete Glaskarten mit weichen Schatten schweben über den Bildern, im Stil Dunkel, Klar, Frost oder Fused Glass.',
              'Eigene Ansichten, Glaskarten',
              'Aeon mit Glasmenüs: dasselbe Layout und dieselben Bibliotheksansichten wie Aeon, mit durchscheinenden Glasmenüs und -dialogen statt fester. Keine Paletten.',
              'Aeon mit Glasmenüs, ohne Paletten'),
    'el_gr': ('Aeon: συμπαγή πάνελ σε παλέτα της επιλογής σας. Aeon Glass: η ίδια διάταξη και προβολές Aeon με γυάλινα μενού, χωρίς παλέτες. Fused Glass: δικές του προβολές βιβλιοθήκης, στρογγυλεμένες γυάλινες κάρτες πάνω από τις εικόνες.',
              'Δικές του προβολές βιβλιοθήκης και μενού: στρογγυλεμένες γυάλινες κάρτες με απαλές σκιές αιωρούνται πάνω από τις εικόνες, σε στυλ Σκοτεινό, Διάφανο, Παγωμένο ή Fused Glass.',
              'Δικές του προβολές, γυάλινες κάρτες',
              'Aeon με γυάλινα μενού: η ίδια διάταξη και προβολές βιβλιοθήκης με το Aeon, με διάφανα γυάλινα μενού και διαλόγους αντί για συμπαγή. Χωρίς παλέτες.',
              'Aeon με γυάλινα μενού, χωρίς παλέτες'),
    'es_es': ('Aeon: paneles sólidos en la paleta que elijas. Aeon Glass: el mismo diseño y vistas de Aeon con menús de cristal, sin paletas. Fused Glass: sus propias vistas de biblioteca, tarjetas de cristal redondeadas sobre las imágenes.',
              'Sus propias vistas de biblioteca y menús: tarjetas de cristal redondeadas con sombras suaves flotan sobre las imágenes, en estilo Oscuro, Claro, Escarcha o Fused Glass.',
              'Vistas propias, tarjetas de cristal',
              'Aeon con menús de cristal: el mismo diseño y las mismas vistas de biblioteca que Aeon, con menús y diálogos de cristal translúcido en lugar de sólidos. Sin paletas.',
              'Aeon con menús de cristal, sin paletas'),
    'fi_fi': ('Aeon: umpinaiset paneelit valitsemallasi paletilla. Aeon Glass: sama Aeonin asettelu ja näkymät lasivalikoin, ei paletteja. Fused Glass: omat kirjastonäkymät, pyöristetyt lasikortit kuvien yllä.',
              'Omat kirjastonäkymät ja valikot: pyöristetyt lasikortit pehmein varjoin leijuvat kuvien yllä, tyylinä Tumma, Kirkas, Huurre tai Fused Glass.',
              'Omat näkymät, lasikortit',
              'Aeon lasivalikoin: sama asettelu ja kirjastonäkymät kuin Aeonissa, umpinaisten sijaan läpikuultavat lasivalikot ja -ikkunat. Ei paletteja.',
              'Aeon lasivalikoin, ei paletteja'),
    'fr_fr': ("Aeon : des panneaux pleins dans la palette de votre choix. Aeon Glass : la même mise en page et les mêmes vues qu'Aeon avec des menus en verre, sans palettes. Fused Glass : ses propres vues de médiathèque, des cartes en verre arrondies au-dessus des images.",
              'Ses propres vues de médiathèque et menus : des cartes en verre arrondies aux ombres douces flottent au-dessus des images, en style Sombre, Clair, Givré ou Fused Glass.',
              'Vues propres, cartes en verre',
              "Aeon avec des menus en verre : la même mise en page et les mêmes vues de médiathèque qu'Aeon, avec des menus et dialogues en verre translucide au lieu de pleins. Pas de palettes.",
              'Aeon avec menus en verre, sans palettes'),
    'hu_hu': ('Aeon: tömör panelek a választott palettával. Aeon Glass: ugyanaz az Aeon-elrendezés és nézetek üvegmenükkel, paletták nélkül. Fused Glass: saját könyvtárnézetek, lekerekített üvegkártyák a képek felett.',
              'Saját könyvtárnézetek és menük: lekerekített, lágy árnyékú üvegkártyák lebegnek a képek felett, Sötét, Tiszta, Dér vagy Fused Glass stílusban.',
              'Saját nézetek, üvegkártyák',
              'Aeon üvegmenükkel: ugyanaz az elrendezés és könyvtárnézetek, mint az Aeonban, tömör helyett áttetsző üvegmenükkel és párbeszédablakokkal. Paletták nélkül.',
              'Aeon üvegmenükkel, paletták nélkül'),
    'it_it': ("Aeon: pannelli pieni nella tavolozza che scegli. Aeon Glass: lo stesso layout e le stesse viste di Aeon con menu di vetro, senza tavolozze. Fused Glass: viste della libreria proprie, schede di vetro arrotondate sopra le immagini.",
              'Viste della libreria e menu propri: schede di vetro arrotondate con ombre morbide fluttuano sopra le immagini, in stile Scuro, Chiaro, Brina o Fused Glass.',
              'Viste proprie, schede di vetro',
              'Aeon con menu di vetro: lo stesso layout e le stesse viste della libreria di Aeon, con menu e finestre di vetro trasparente invece che pieni. Niente tavolozze.',
              'Aeon con menu di vetro, senza tavolozze'),
    'ja_jp': ('Aeon：選んだパレットの不透明なパネル。Aeon Glass：同じ Aeon のレイアウトとビューにガラスのメニュー、パレットなし。Fused Glass：独自のライブラリビューと、アートワークの上の角の丸いガラスカード。',
              '独自のライブラリビューとメニュー：柔らかな影の角の丸いガラスカードがアートワークの上に浮かびます。スタイルはダーク、クリア、フロスト、Fused Glass。',
              '独自のビュー、ガラスカード',
              'ガラスのメニューの Aeon：Aeon と同じレイアウトとライブラリビューで、メニューとダイアログが不透明ではなく半透明のガラスになります。パレットはありません。',
              'ガラスのメニューの Aeon、パレットなし'),
    'ko_kr': ('Aeon: 고른 팔레트의 불투명 패널. Aeon Glass: 같은 Aeon 레이아웃과 보기에 유리 메뉴, 팔레트 없음. Fused Glass: 자체 라이브러리 보기, 아트워크 위의 둥근 유리 카드.',
              '자체 라이브러리 보기와 메뉴: 부드러운 그림자의 둥근 유리 카드가 아트워크 위에 떠 있으며, 다크, 클리어, 프로스트 또는 Fused Glass 스타일입니다.',
              '자체 보기, 유리 카드',
              '유리 메뉴의 Aeon: Aeon과 같은 레이아웃과 라이브러리 보기에, 메뉴와 대화상자가 불투명 대신 반투명 유리입니다. 팔레트 없음.',
              '유리 메뉴의 Aeon, 팔레트 없음'),
    'nb_no': ('Aeon: faste paneler i en palett du velger. Aeon Glass: samme Aeon-oppsett og visninger med glassmenyer, uten paletter. Fused Glass: egne bibliotekvisninger, avrundede glasskort over bildene.',
              'Egne bibliotekvisninger og menyer: avrundede glasskort med myke skygger svever over bildene, i stilen Mørk, Klar, Frost eller Fused Glass.',
              'Egne visninger, glasskort',
              'Aeon med glassmenyer: samme oppsett og bibliotekvisninger som Aeon, med gjennomsiktige glassmenyer og dialoger i stedet for faste. Ingen paletter.',
              'Aeon med glassmenyer, uten paletter'),
    'nl_nl': ('Aeon: dichte panelen in een palet naar keuze. Aeon Glass: dezelfde Aeon-indeling en weergaven met glazen menu’s, zonder paletten. Fused Glass: eigen bibliotheekweergaven, afgeronde glazen kaarten boven de afbeeldingen.',
              'Eigen bibliotheekweergaven en menu’s: afgeronde glazen kaarten met zachte schaduwen zweven boven de afbeeldingen, in de stijl Donker, Helder, Rijp of Fused Glass.',
              'Eigen weergaven, glazen kaarten',
              'Aeon met glazen menu’s: dezelfde indeling en bibliotheekweergaven als Aeon, met doorschijnende glazen menu’s en dialogen in plaats van dichte. Geen paletten.',
              'Aeon met glazen menu’s, zonder paletten'),
    'pl_pl': ('Aeon: pełne panele w wybranej palecie. Aeon Glass: ten sam układ i widoki Aeon ze szklanymi menu, bez palet. Fused Glass: własne widoki biblioteki, zaokrąglone szklane karty nad obrazami.',
              'Własne widoki biblioteki i menu: zaokrąglone szklane karty z miękkimi cieniami unoszą się nad obrazami, w stylu Ciemny, Przejrzysty, Szron lub Fused Glass.',
              'Własne widoki, szklane karty',
              'Aeon ze szklanymi menu: ten sam układ i widoki biblioteki co Aeon, z przejrzystymi szklanymi menu i oknami zamiast pełnych. Bez palet.',
              'Aeon ze szklanymi menu, bez palet'),
    'pt_br': ('Aeon: painéis sólidos na paleta que você escolher. Aeon Glass: o mesmo layout e visualizações do Aeon com menus de vidro, sem paletas. Fused Glass: visualizações de biblioteca próprias, cartões de vidro arredondados sobre as imagens.',
              'Visualizações de biblioteca e menus próprios: cartões de vidro arredondados com sombras suaves flutuam sobre as imagens, no estilo Escuro, Claro, Geada ou Fused Glass.',
              'Visualizações próprias, cartões de vidro',
              'Aeon com menus de vidro: o mesmo layout e as mesmas visualizações de biblioteca do Aeon, com menus e diálogos de vidro translúcido em vez de sólidos. Sem paletas.',
              'Aeon com menus de vidro, sem paletas'),
    'pt_pt': ('Aeon: painéis sólidos na paleta que escolher. Aeon Glass: o mesmo esquema e vistas do Aeon com menus de vidro, sem paletas. Fused Glass: vistas de biblioteca próprias, cartões de vidro arredondados sobre as imagens.',
              'Vistas de biblioteca e menus próprios: cartões de vidro arredondados com sombras suaves flutuam sobre as imagens, no estilo Escuro, Claro, Geada ou Fused Glass.',
              'Vistas próprias, cartões de vidro',
              'Aeon com menus de vidro: o mesmo esquema e as mesmas vistas de biblioteca do Aeon, com menus e diálogos de vidro translúcido em vez de sólidos. Sem paletas.',
              'Aeon com menus de vidro, sem paletas'),
    'ru_ru': ('Aeon: сплошные панели в выбранной палитре. Aeon Glass: та же раскладка и виды Aeon со стеклянными меню, без палитр. Fused Glass: собственные виды медиатеки, скруглённые стеклянные карточки над изображениями.',
              'Собственные виды медиатеки и меню: скруглённые стеклянные карточки с мягкими тенями парят над изображениями, в стиле Тёмный, Прозрачный, Иней или Fused Glass.',
              'Свои виды, стеклянные карточки',
              'Aeon со стеклянными меню: та же раскладка и виды медиатеки, что у Aeon, но меню и диалоги из полупрозрачного стекла вместо сплошных. Без палитр.',
              'Aeon со стеклянными меню, без палитр'),
    'sv_se': ('Aeon: fasta paneler i en palett du väljer. Aeon Glass: samma Aeon-layout och vyer med glasmenyer, utan paletter. Fused Glass: egna biblioteksvyer, rundade glaskort över bilderna.',
              'Egna biblioteksvyer och menyer: rundade glaskort med mjuka skuggor svävar över bilderna, i stilen Mörk, Klar, Frost eller Fused Glass.',
              'Egna vyer, glaskort',
              'Aeon med glasmenyer: samma layout och biblioteksvyer som Aeon, med genomskinliga glasmenyer och dialoger i stället för fasta. Inga paletter.',
              'Aeon med glasmenyer, utan paletter'),
    'tr_tr': ('Aeon: seçtiğiniz paletle dolu paneller. Aeon Glass: aynı Aeon düzeni ve görünümleri cam menülerle, paletsiz. Fused Glass: kendi kütüphane görünümleri, görsellerin üzerinde yuvarlak cam kartlar.',
              'Kendi kütüphane görünümleri ve menüleri: yumuşak gölgeli yuvarlak cam kartlar görsellerin üzerinde süzülür; Koyu, Şeffaf, Buzlu ya da Fused Glass stilinde.',
              'Kendi görünümleri, cam kartlar',
              'Cam menülü Aeon: Aeon ile aynı düzen ve kütüphane görünümleri, dolu yerine yarı saydam cam menü ve iletişim kutularıyla. Palet yok.',
              'Cam menülü Aeon, paletsiz'),
    'uk_ua': ('Aeon: суцільні панелі у вибраній палітрі. Aeon Glass: та сама розкладка й види Aeon зі скляними меню, без палітр. Fused Glass: власні види медіатеки, заокруглені скляні картки над зображеннями.',
              'Власні види медіатеки та меню: заокруглені скляні картки з м’якими тінями ширяють над зображеннями, у стилі Темний, Прозорий, Іній або Fused Glass.',
              'Власні види, скляні картки',
              'Aeon зі скляними меню: та сама розкладка й види медіатеки, що в Aeon, але меню та діалоги з напівпрозорого скла замість суцільних. Без палітр.',
              'Aeon зі скляними меню, без палітр'),
    'zh_cn': ('Aeon：所选调色板的实心面板。Aeon Glass：相同的 Aeon 布局和视图，配玻璃菜单，无调色板。Fused Glass：自有媒体库视图，图片之上的圆角玻璃卡片。',
              '自有媒体库视图和菜单：带柔和阴影的圆角玻璃卡片浮在图片之上，风格为深色、透明、磨砂或 Fused Glass。',
              '自有视图，玻璃卡片',
              '玻璃菜单的 Aeon：与 Aeon 相同的布局和媒体库视图，菜单和对话框是半透明玻璃而非实心。无调色板。',
              '玻璃菜单的 Aeon，无调色板'),
    'zh_tw': ('Aeon：所選調色盤的實心面板。Aeon Glass：相同的 Aeon 版面和檢視，搭配玻璃選單，無調色盤。Fused Glass：自有媒體庫檢視，圖片之上的圓角玻璃卡片。',
              '自有媒體庫檢視和選單：帶柔和陰影的圓角玻璃卡片浮在圖片之上，風格為深色、透明、霧面或 Fused Glass。',
              '自有檢視，玻璃卡片',
              '玻璃選單的 Aeon：與 Aeon 相同的版面和媒體庫檢視，選單和對話框是半透明玻璃而非實心。無調色盤。',
              '玻璃選單的 Aeon，無調色盤'),
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
    print('wizard theme texts in', len(os.listdir(L)), 'languages')


if __name__ == '__main__':
    main()
