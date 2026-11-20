# -*- coding: utf-8 -*-
"""0.56.15 strings, all 23 languages. Safe to run again.
32606 "{t} left" (the helper's 0:07 left after ENDS), 31084 the music Compact list's picker line (was "Fanart list with
A-Z keys"), 32607-32611 the new settings rows, 32612-32614 their help lines."""
import io
import os
import re

LANGS = ['cs_cz', 'da_dk', 'de_de', 'el_gr', 'es_es', 'fi_fi', 'fr_fr', 'hu_hu', 'it_it', 'ja_jp', 'ko_kr', 'nb_no', 'nl_nl',
         'pl_pl', 'pt_br', 'pt_pt', 'ru_ru', 'sv_se', 'tr_tr', 'uk_ua', 'zh_cn', 'zh_tw']


def row(*vals):
    assert len(vals) == len(LANGS), len(vals)
    return dict(zip(LANGS, vals))


S = {
    32606: ('{t} left', row('zbývá {t}', '{t} tilbage', 'noch {t}', 'απομένουν {t}', 'quedan {t}', '{t} jäljellä', 'encore {t}', 'még {t}',
                            'mancano {t}', '残り {t}', '{t} 남음', '{t} igjen', 'nog {t}', 'zostało {t}', 'faltam {t}', 'faltam {t}', 'осталось {t}',
                            '{t} kvar', '{t} kaldı', 'лишилось {t}', '还剩 {t}', '還剩 {t}')),
    31084: ('Rows with A-Z keys', row('Řádky s klávesami A-Z', 'Rækker med A-Å-taster', 'Zeilen mit A–Z-Tasten', 'Γραμμές με πλήκτρα Α-Ω',
                                      'Filas con teclas A-Z', 'Rivit A-Ö-näppäimin', 'Lignes avec touches A-Z', 'Sorok A-Z gombokkal',
                                      'Righe con tasti A-Z', 'A-Z キー付きの行', 'A-Z 키가 있는 행', 'Rader med A-Å-taster', 'Rijen met A-Z-toetsen',
                                      'Wiersze z klawiszami A-Z', 'Linhas com teclas A-Z', 'Linhas com teclas A-Z', 'Строки с кнопками А-Я',
                                      'Rader med A-Ö-tangenter', 'A-Z tuşlu satırlar', 'Рядки з кнопками А-Я', '带 A-Z 键的行', '附 A-Z 鍵的列')),
    32607: ('Home menu underline', row('Podtržení v menu Domů', 'Understregning i Hjem-menuen', 'Unterstrich im Home-Menü', 'Υπογράμμιση στο μενού Αρχικής',
                                       'Subrayado del menú de inicio', 'Alleviivaus kotivalikossa', "Soulignement du menu d'accueil", 'Aláhúzás a kezdőmenüben',
                                       'Sottolineatura del menu Home', 'ホームメニューの下線', '홈 메뉴 밑줄', 'Understreking i Hjem-menyen',
                                       'Onderstreping in het startmenu', 'Podkreślenie w menu głównym', 'Sublinhado do menu inicial', 'Sublinhado do menu inicial',
                                       'Подчёркивание в главном меню', 'Understrykning i hemmenyn', 'Ana menü alt çizgisi', 'Підкреслення в головному меню',
                                       '主页菜单下划线', '主頁選單底線')),
    32608: ('Fanart look', row('Vzhled fanartu', 'Fanart-udseende', 'Fanart-Darstellung', 'Εμφάνιση fanart', 'Aspecto del fanart', 'Fanartin ulkoasu',
                               'Aspect du fanart', 'Fanart megjelenése', 'Aspetto del fanart', 'ファンアートの見た目', '팬아트 모양', 'Fanart-utseende',
                               'Fanart-weergave', 'Wygląd fanartu', 'Aparência do fanart', 'Aspeto do fanart', 'Вид фанарта', 'Fanartens utseende',
                               'Fanart görünümü', 'Вигляд фанарту', '背景图外观', '背景圖外觀')),
    32609: ('Dimmed', row('Ztlumený', 'Dæmpet', 'Abgedunkelt', 'Σκοτεινιασμένο', 'Atenuado', 'Himmennetty', 'Assombri', 'Tompított', 'Attenuato', '暗め',
                          '어둡게', 'Dempet', 'Gedimd', 'Przyciemniony', 'Escurecido', 'Escurecido', 'Затемнённый', 'Dämpad', 'Karartılmış', 'Затемнений',
                          '调暗', '調暗')),
    32610: ('Ratings shown as', row('Hodnocení zobrazit jako', 'Vis bedømmelser som', 'Bewertungen anzeigen als', 'Εμφάνιση βαθμολογιών ως',
                                    'Mostrar valoraciones como', 'Arviot näytetään', 'Afficher les notes en', 'Értékelések megjelenítése',
                                    'Mostra valutazioni come', '評価の表示', '평점 표시 방식', 'Vis vurderinger som', 'Beoordelingen tonen als',
                                    'Pokaż oceny jako', 'Mostrar avaliações como', 'Mostrar classificações como', 'Показывать рейтинги как',
                                    'Visa betyg som', 'Puanları göster', 'Показувати рейтинги як', '评分显示为', '評分顯示為')),
    32611: ('Text', row('Text', 'Tekst', 'Text', 'Κείμενο', 'Texto', 'Teksti', 'Texte', 'Szöveg', 'Testo', 'テキスト', '텍스트', 'Tekst', 'Tekst', 'Tekst',
                        'Texto', 'Texto', 'Текст', 'Text', 'Metin', 'Текст', '文字', '文字')),
    32612: ('The accent line under the focused Home menu item, as in Fused Glass.',
            row('Zvýrazňující čára pod vybranou položkou menu Domů, jako ve Fused Glass.',
                'Accentstregen under det valgte punkt i Hjem-menuen, som i Fused Glass.',
                'Die Akzentlinie unter dem gewählten Eintrag im Home-Menü, wie in Fused Glass.',
                'Η γραμμή έμφασης κάτω από το επιλεγμένο στοιχείο του μενού Αρχικής, όπως στο Fused Glass.',
                'La línea de acento bajo el elemento seleccionado del menú de inicio, como en Fused Glass.',
                'Korostusviiva valitun kotivalikon kohdan alla, kuten Fused Glassissa.',
                "La ligne d'accent sous l'élément sélectionné du menu d'accueil, comme dans Fused Glass.",
                'Kiemelő vonal a kijelölt kezdőmenü-elem alatt, mint a Fused Glassban.',
                "La linea d'accento sotto la voce selezionata del menu Home, come in Fused Glass.",
                '選択中のホームメニュー項目の下にアクセントの線を表示します（Fused Glass と同じ）。',
                '선택한 홈 메뉴 항목 아래의 강조선 (Fused Glass와 같음).',
                'Aksentstreken under det valgte punktet i Hjem-menyen, som i Fused Glass.',
                'De accentlijn onder het gekozen item in het startmenu, zoals in Fused Glass.',
                'Linia akcentu pod wybraną pozycją menu głównego, jak w Fused Glass.',
                'A linha de destaque sob o item selecionado do menu inicial, como no Fused Glass.',
                'A linha de destaque sob o item selecionado do menu inicial, como no Fused Glass.',
                'Акцентная линия под выбранным пунктом главного меню, как в Fused Glass.',
                'Accentlinjen under det valda objektet i hemmenyn, som i Fused Glass.',
                "Seçili ana menü öğesinin altındaki vurgu çizgisi, Fused Glass'taki gibi.",
                'Акцентна лінія під вибраним пунктом головного меню, як у Fused Glass.',
                '在选中的主页菜单项下方显示强调线，与 Fused Glass 相同。',
                '在選取的主頁選單項目下方顯示強調線，與 Fused Glass 相同。')),
    32613: ('The fanart behind the library views: dimmed under a dark veil, or light with a frosted colour tint.',
            row('Fanart za zobrazeními knihovny: ztlumený pod tmavým závojem, nebo světlý s matným barevným nádechem.',
                'Fanart bag biblioteksvisningerne: dæmpet under et mørkt slør eller lyst med en frostet farvetone.',
                'Das Fanart hinter den Bibliotheksansichten: abgedunkelt unter einem dunklen Schleier oder hell mit einem frostigen Farbton.',
                'Το fanart πίσω από τις προβολές της βιβλιοθήκης: σκοτεινιασμένο κάτω από σκούρο πέπλο ή φωτεινό με παγωμένη χρωματική απόχρωση.',
                'El fanart tras las vistas de la biblioteca: atenuado bajo un velo oscuro, o claro con un tinte de color esmerilado.',
                'Kirjastonäkymien taustan fanart: himmennettynä tumman verhon alla tai vaaleana huurteisella värisävyllä.',
                'Le fanart derrière les vues de la bibliothèque : assombri sous un voile sombre, ou clair avec une teinte colorée givrée.',
                'A könyvtárnézetek mögötti fanart: sötét fátyol alatt tompítva, vagy világosan, dérszerű színárnyalattal.',
                'Il fanart dietro le viste della libreria: attenuato sotto un velo scuro, oppure chiaro con una tinta colorata smerigliata.',
                'ライブラリ表示の背景のファンアート：暗いベールで暗めにするか、明るく曇りガラスのような色味にします。',
                '라이브러리 보기 뒤의 팬아트: 어두운 막으로 어둡게, 또는 서리 낀 색조로 밝게.',
                'Fanart bak bibliotekvisningene: dempet under et mørkt slør, eller lyst med en frostet fargetone.',
                'De fanart achter de bibliotheekweergaven: gedimd onder een donkere sluier, of licht met een berijpte kleurtint.',
                'Fanart za widokami biblioteki: przyciemniony pod ciemną zasłoną albo jasny z oszronionym odcieniem koloru.',
                'O fanart atrás das visualizações da biblioteca: escurecido sob um véu escuro ou claro com um tom de cor fosco.',
                'O fanart atrás das vistas da biblioteca: escurecido sob um véu escuro ou claro com um tom de cor fosco.',
                'Фанарт за видами библиотеки: затемнённый под тёмной вуалью или светлый с матовым цветным оттенком.',
                'Fanart bakom biblioteksvyerna: dämpad under en mörk slöja, eller ljus med en frostad färgton.',
                'Kitaplık görünümlerinin arkasındaki fanart: koyu bir perde altında karartılmış ya da buzlu bir renk tonuyla açık.',
                'Фанарт за виглядами бібліотеки: затемнений під темною вуаллю або світлий з матовим кольоровим відтінком.',
                '媒体库视图后面的背景图：在深色遮罩下调暗，或以磨砂色调提亮。',
                '媒體庫檢視後面的背景圖：在深色遮罩下調暗，或以霧面色調提亮。')),
    32614: ('Show the rating providers as their icons or as their names.',
            row('Zobrazit poskytovatele hodnocení jako ikony nebo jako názvy.', 'Vis bedømmelsestjenesterne som deres ikoner eller deres navne.',
                'Bewertungsanbieter als ihre Symbole oder als ihre Namen anzeigen.', 'Εμφάνιση των παρόχων βαθμολογίας ως εικονίδια ή ως ονόματα.',
                'Mostrar los proveedores de valoraciones como iconos o como nombres.', 'Näytä arvioiden lähteet kuvakkeina tai niminä.',
                "Afficher les fournisseurs de notes sous forme d'icônes ou de noms.", 'Az értékelésszolgáltatók megjelenítése ikonként vagy névként.',
                'Mostra i fornitori di valutazioni come icone o come nomi.', '評価の提供元をアイコンまたは名前で表示します。',
                '평점 제공자를 아이콘 또는 이름으로 표시합니다.', 'Vis vurderingstjenestene som ikoner eller som navn.',
                'Toon de beoordelingsbronnen als hun pictogrammen of als hun namen.', 'Pokaż dostawców ocen jako ikony lub jako nazwy.',
                'Mostrar os provedores de avaliação como ícones ou como nomes.', 'Mostrar os fornecedores de classificações como ícones ou como nomes.',
                'Показывать источники рейтингов значками или названиями.', 'Visa betygskällorna som ikoner eller som namn.',
                'Puan sağlayıcılarını simgeleriyle ya da adlarıyla göster.', 'Показувати джерела рейтингів значками або назвами.',
                '以图标或名称显示评分来源。', '以圖示或名稱顯示評分來源。')),
}


def po_esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


for d in sorted(os.listdir('language')):
    code = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    for sid, (en, tr) in sorted(S.items()):
        entry = 'msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, po_esc(en), '' if code == 'en_gb' else po_esc(tr[code]))
        pat = re.compile(r'msgctxt "#%d"\nmsgid "(?:[^"\\]|\\.)*"\nmsgstr "(?:[^"\\]|\\.)*"\n' % sid)
        if pat.search(t):
            t = pat.sub(lambda m: entry, t, count=1)
        else:
            t = t.rstrip('\n') + '\n\n' + entry
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
