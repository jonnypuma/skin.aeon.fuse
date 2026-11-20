# -*- coding: utf-8 -*-
"""0.40.2 strings 32458-32461: Skin settings > Look > Library options (Strip | Box), all languages. Run from the skin folder."""
import io
import os

EN = {
    32458: 'Library options',
    32459: 'Strip',
    32460: 'Box',
    32461: 'Left at the edge of a view or the Menu key opens the side strip, or a big box in the menu style.',
}
TR = {
    'cs_cz': ('Možnosti knihovny', 'Lišta', 'Box', 'Vlevo na okraji zobrazení nebo klávesa Menu otevře boční lištu, nebo velký box ve stylu menu.'),
    'da_dk': ('Biblioteksvalg', 'Bjælke', 'Boks', 'Venstre ved kanten af en visning eller Menu-tasten åbner sidebjælken eller en stor boks i menustilen.'),
    'de_de': ('Bibliotheksoptionen', 'Leiste', 'Box', 'Links am Rand einer Ansicht oder die Menütaste öffnet die Seitenleiste oder eine große Box im Menüstil.'),
    'el_gr': ('Επιλογές βιβλιοθήκης', 'Λωρίδα', 'Πλαίσιο', 'Αριστερά στην άκρη μιας προβολής ή το πλήκτρο Μενού ανοίγει την πλαϊνή λωρίδα ή ένα μεγάλο πλαίσιο στο στυλ του μενού.'),
    'es_es': ('Opciones de la biblioteca', 'Franja', 'Caja', 'Izquierda en el borde de una vista o la tecla Menú abre la franja lateral o una caja grande en el estilo del menú.'),
    'fi_fi': ('Kirjaston valinnat', 'Palkki', 'Laatikko', 'Vasen näkymän reunassa tai Valikko-näppäin avaa sivupalkin tai ison laatikon valikon tyylillä.'),
    'fr_fr': ('Options de la médiathèque', 'Bande', 'Boîte', 'Gauche au bord d\'une vue ou la touche Menu ouvre la bande latérale, ou une grande boîte dans le style du menu.'),
    'hu_hu': ('Könyvtár beállításai', 'Sáv', 'Doboz', 'Balra a nézet szélén vagy a Menü gomb az oldalsávot nyitja meg, vagy egy nagy dobozt a menü stílusában.'),
    'it_it': ('Opzioni della libreria', 'Striscia', 'Riquadro', 'Sinistra sul bordo di una vista o il tasto Menu apre la striscia laterale, o un grande riquadro nello stile del menu.'),
    'ja_jp': ('ライブラリのオプション', 'ストリップ', 'ボックス', 'ビューの端で左、またはメニューキーで、サイドストリップかメニュースタイルの大きなボックスが開きます。'),
    'ko_kr': ('라이브러리 옵션', '스트립', '상자', '보기 가장자리에서 왼쪽 또는 메뉴 키를 누르면 옆 스트립이나 메뉴 스타일의 큰 상자가 열립니다.'),
    'nb_no': ('Bibliotekvalg', 'Stripe', 'Boks', 'Venstre i kanten av en visning eller Meny-tasten åpner sidestripen, eller en stor boks i menystilen.'),
    'nl_nl': ('Bibliotheekopties', 'Strook', 'Vak', 'Links aan de rand van een weergave of de Menutoets opent de zijstrook, of een groot vak in de menustijl.'),
    'pl_pl': ('Opcje biblioteki', 'Pasek', 'Okno', 'W lewo przy krawędzi widoku lub klawisz Menu otwiera pasek boczny albo duże okno w stylu menu.'),
    'pt_br': ('Opções da biblioteca', 'Faixa', 'Caixa', 'Esquerda na borda de uma visualização ou a tecla Menu abre a faixa lateral ou uma caixa grande no estilo do menu.'),
    'pt_pt': ('Opções da biblioteca', 'Faixa', 'Caixa', 'Esquerda na margem de uma vista ou a tecla Menu abre a faixa lateral ou uma caixa grande no estilo do menu.'),
    'ru_ru': ('Параметры медиатеки', 'Полоса', 'Окно', 'Влево у края вида или клавиша «Меню» открывает боковую полосу или большое окно в стиле меню.'),
    'sv_se': ('Biblioteksval', 'Remsa', 'Ruta', 'Vänster vid kanten av en vy eller Meny-knappen öppnar sidoremsan eller en stor ruta i menystilen.'),
    'tr_tr': ('Kitaplık seçenekleri', 'Şerit', 'Kutu', 'Görünümün kenarında sol veya Menü tuşu yan şeridi ya da menü stilinde büyük bir kutuyu açar.'),
    'uk_ua': ('Параметри медіатеки', 'Смуга', 'Вікно', 'Ліворуч біля краю вигляду або клавіша «Меню» відкриває бічну смугу або велике вікно у стилі меню.'),
    'zh_cn': ('媒体库选项', '侧栏', '方框', '在视图边缘按左或按菜单键会打开侧栏，或菜单样式的大方框。'),
    'zh_tw': ('媒體櫃選項', '側欄', '方框', '在檢視邊緣按左或按選單鍵會開啟側欄，或選單樣式的大方框。'),
}
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32458"' in t:
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
print('strings 32458-32461 added in %d languages' % done)
