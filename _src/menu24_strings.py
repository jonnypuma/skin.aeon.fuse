# -*- coding: utf-8 -*-
"""0.54.0 strings: Add item in Skin settings > Home menu (row, picker heading, the panel's text while the row has the
focus), the help line under the rows (31671, now naming Add item) and the custom items message (31912, ten instead of
three). Each language keeps its own words for Custom item / Spotlight / lists. The help line fits the 860 px label
(Figtree Medium 20), measured by measure() below. Run from the skin folder; writes or rewrites the entries."""
import io
import os
import re

KEYS = (31671, 31912, 32591, 32592)
SKIN = {
    31671: 'Pick an item, then use the buttons on the right. Add item puts a new one at the end.',
    31912: 'All ten custom items are in use. Free one first.',
    32591: 'Add item',
    32592: "Puts a new item at the end of the menu: one of the skin's items that is not on it yet, or a custom item with "
           "its own path, Spotlight and lists.[CR][CR]OK opens the list of types.",
}
TR = {
    'cs_cz': ('Vyberte položku a použijte tlačítka vpravo. Přidat položku vloží novou na konec.',
              'Všech deset vlastních položek je obsazeno. Nejprve jednu uvolněte.',
              'Přidat položku',
              'Vloží novou položku na konec nabídky: položku vzhledu, která v ní ještě není, nebo vlastní položku s vlastní cestou, Spotlightem a seznamy.[CR][CR]OK otevře seznam typů.'),
    'da_dk': ('Vælg et element, og brug knapperne til højre. Tilføj element sætter et nyt sidst.',
              'Alle ti egne elementer er i brug. Frigør ét først.',
              'Tilføj element',
              'Sætter et nyt element sidst i menuen: et af skinnets elementer, der ikke er med endnu, eller et eget element med egen sti, Spotlight og lister.[CR][CR]OK åbner listen over typer.'),
    'de_de': ('Eintrag wählen, dann die Tasten rechts. Eintrag hinzufügen setzt einen neuen ans Ende.',
              'Alle zehn eigenen Einträge sind belegt. Zuerst einen freigeben.',
              'Eintrag hinzufügen',
              'Setzt einen neuen Eintrag ans Ende des Menüs: einen Eintrag des Skins, der noch fehlt, oder einen eigenen Eintrag mit eigenem Pfad, Spotlight und Listen.[CR][CR]OK öffnet die Liste der Arten.'),
    'el_gr': ('Επιλέξτε στοιχείο και μετά τα κουμπιά δεξιά. Η Προσθήκη στοιχείου βάζει νέο στο τέλος.',
              'Και τα δέκα προσαρμοσμένα στοιχεία χρησιμοποιούνται. Ελευθερώστε πρώτα ένα.',
              'Προσθήκη στοιχείου',
              'Βάζει νέο στοιχείο στο τέλος του μενού: ένα στοιχείο του θέματος που δεν υπάρχει ακόμη ή ένα προσαρμοσμένο στοιχείο με δική του διαδρομή, Spotlight και λίστες.[CR][CR]Το OK ανοίγει τη λίστα τύπων.'),
    'es_es': ('Elige un elemento y usa los botones de la derecha. Añadir elemento pone uno nuevo al final.',
              'Los diez elementos propios están en uso. Libera uno primero.',
              'Añadir elemento',
              'Pone un elemento nuevo al final del menú: uno de los elementos del skin que aún no está, o un elemento propio con su ruta, Spotlight y listas.[CR][CR]OK abre la lista de tipos.'),
    'fi_fi': ('Valitse kohde ja käytä oikean puolen painikkeita. Lisää kohde lisää uuden loppuun.',
              'Kaikki kymmenen omaa kohdetta ovat käytössä. Vapauta ensin yksi.',
              'Lisää kohde',
              'Lisää uuden kohteen valikon loppuun: teeman kohteen, joka ei vielä ole valikossa, tai oman kohteen omalla polulla, Spotlightilla ja luetteloilla.[CR][CR]OK avaa tyyppien luettelon.'),
    'fr_fr': ('Choisissez un élément, puis les boutons à droite. Ajouter un élément en met un nouveau à la fin.',
              "Les dix éléments personnalisés sont utilisés. Libérez-en un d'abord.",
              'Ajouter un élément',
              "Ajoute un nouvel élément à la fin du menu : un élément du skin qui n'y est pas encore, ou un élément personnalisé avec son chemin, son Spotlight et ses listes.[CR][CR]OK ouvre la liste des types."),
    'hu_hu': ('Válassz elemet, majd a jobb oldali gombokat. Az Elem hozzáadása újat tesz a végére.',
              'Mind a tíz egyéni elem foglalt. Előbb szabadíts fel egyet.',
              'Elem hozzáadása',
              'Új elemet tesz a menü végére: a felület egy még hiányzó elemét, vagy egyéni elemet saját útvonallal, Spotlighttal és listákkal.[CR][CR]Az OK megnyitja a típusok listáját.'),
    'it_it': ('Scegli una voce e usa i pulsanti a destra. Aggiungi voce ne mette una nuova in fondo.',
              'Tutte e dieci le voci personalizzate sono in uso. Liberane prima una.',
              'Aggiungi voce',
              "Aggiunge una nuova voce in fondo al menu: una voce della skin non ancora presente, o una voce personalizzata con percorso, Spotlight ed elenchi propri.[CR][CR]OK apre l'elenco dei tipi."),
    'ja_jp': ('項目を選び、右のボタンを使います。項目を追加は新しい項目を最後に加えます。',
              '10個のカスタム項目はすべて使用中です。先に1つ空けてください。',
              '項目を追加',
              'メニューの最後に新しい項目を加えます: まだ無いスキンの項目、または独自のパス、Spotlight、リストを持つカスタム項目。[CR][CR]OK で種類の一覧が開きます。'),
    'ko_kr': ('항목을 고른 다음 오른쪽 버튼을 사용하세요. 항목 추가는 새 항목을 끝에 넣습니다.',
              '사용자 항목 열 개가 모두 사용 중입니다. 먼저 하나를 비우세요.',
              '항목 추가',
              '메뉴 끝에 새 항목을 넣습니다: 아직 없는 스킨 항목 또는 자체 경로, Spotlight, 목록을 가진 사용자 항목.[CR][CR]OK를 누르면 유형 목록이 열립니다.'),
    'nb_no': ('Velg et element, og bruk knappene til høyre. Legg til element setter et nytt sist.',
              'Alle ti egne elementer er i bruk. Frigjør ett først.',
              'Legg til element',
              'Setter et nytt element sist i menyen: et av skinnets elementer som ikke er med ennå, eller et eget element med egen sti, Spotlight og lister.[CR][CR]OK åpner listen over typer.'),
    'nl_nl': ('Kies een item en gebruik de knoppen rechts. Item toevoegen zet een nieuw item achteraan.',
              'Alle tien eigen items zijn in gebruik. Maak er eerst een vrij.',
              'Item toevoegen',
              'Zet een nieuw item achteraan het menu: een item van de skin dat er nog niet in staat, of een eigen item met eigen pad, Spotlight en lijsten.[CR][CR]OK opent de lijst met soorten.'),
    'pl_pl': ('Wybierz pozycję i użyj przycisków po prawej. Dodaj pozycję wstawia nową na końcu.',
              'Wszystkie dziesięć własnych pozycji jest zajętych. Najpierw zwolnij jedną.',
              'Dodaj pozycję',
              'Wstawia nową pozycję na końcu menu: pozycję skórki, której jeszcze w nim nie ma, albo własną pozycję z własną ścieżką, Spotlightem i listami.[CR][CR]OK otwiera listę typów.'),
    'pt_br': ('Escolha um item e use os botões à direita. Adicionar item coloca um novo no fim.',
              'Os dez itens personalizados estão em uso. Libere um primeiro.',
              'Adicionar item',
              'Coloca um item novo no fim do menu: um item da skin que ainda não está nele, ou um item personalizado com caminho, Spotlight e listas próprios.[CR][CR]OK abre a lista de tipos.'),
    'pt_pt': ('Escolha um item e use os botões à direita. Adicionar item coloca um novo no fim.',
              'Os dez itens personalizados estão em uso. Liberte um primeiro.',
              'Adicionar item',
              'Coloca um item novo no fim do menu: um item do skin que ainda não está nele, ou um item personalizado com caminho, Spotlight e listas próprios.[CR][CR]OK abre a lista de tipos.'),
    'ru_ru': ('Выберите пункт, затем кнопки справа. «Добавить пункт» ставит новый в конец.',
              'Все десять своих пунктов заняты. Сначала освободите один.',
              'Добавить пункт',
              'Добавляет новый пункт в конец меню: пункт оболочки, которого в нём ещё нет, или свой пункт со своим путём, Spotlight и списками.[CR][CR]OK открывает список типов.'),
    'sv_se': ('Välj ett objekt och använd knapparna till höger. Lägg till objekt lägger ett nytt sist.',
              'Alla tio egna objekt används. Frigör ett först.',
              'Lägg till objekt',
              'Lägger ett nytt objekt sist i menyn: ett av skalets objekt som inte finns där än, eller ett eget objekt med egen sökväg, Spotlight och listor.[CR][CR]OK öppnar listan över typer.'),
    'tr_tr': ('Bir öğe seçin ve sağdaki düğmeleri kullanın. Öğe ekle sona yeni bir öğe koyar.',
              'On özel öğenin tümü kullanımda. Önce birini boşaltın.',
              'Öğe ekle',
              "Menünün sonuna yeni bir öğe koyar: menüde henüz olmayan bir kaplama öğesi ya da kendi yolu, Spotlight'ı ve listeleri olan özel bir öğe.[CR][CR]OK türlerin listesini açar."),
    'uk_ua': ('Виберіть пункт, а тоді кнопки праворуч. «Додати пункт» ставить новий у кінець.',
              'Усі десять власних пунктів зайняті. Спершу звільніть один.',
              'Додати пункт',
              'Додає новий пункт у кінець меню: пункт оболонки, якого в ньому ще немає, або власний пункт із власним шляхом, Spotlight і списками.[CR][CR]OK відкриває список типів.'),
    'zh_cn': ('选择一个项目，然后使用右侧按钮。添加项目会在末尾加入新项目。',
              '十个自定义项目都已使用。请先腾出一个。',
              '添加项目',
              '在菜单末尾加入新项目：菜单中还没有的皮肤项目，或带有自己路径、Spotlight 和列表的自定义项目。[CR][CR]按 OK 打开类型列表。'),
    'zh_tw': ('選擇一個項目，然後使用右側按鈕。新增項目會在末尾加入新項目。',
              '十個自訂項目都已使用。請先空出一個。',
              '新增項目',
              '在選單末尾加入新項目：選單中還沒有的外觀項目，或帶有自己路徑、Spotlight 和清單的自訂項目。[CR][CR]按 OK 開啟類型清單。'),
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


def measure():
    """the help line (31671) against its 860 px label, in Figtree Medium 20 (CJK falls back to the box's font: measured
    with Noto if present, else skipped)"""
    from PIL import ImageFont
    fig = ImageFont.truetype(os.path.join('fonts', 'Figtree-Medium.ttf'), 20)
    worst = []
    for lang, tr in sorted(list(TR.items()) + [('en_gb', (SKIN[31671],))]):
        if lang in ('ja_jp', 'ko_kr', 'zh_cn', 'zh_tw'):
            continue
        w = fig.getlength(tr[0])
        worst.append((w, lang))
    return sorted(worst)[-5:]


assert len(TR) == 22 and all(len(v) == len(KEYS) for v in TR.values())
if __name__ == '__main__':
    print('widest help lines (px of 860):', measure())
    print('skin', write('language'), 'languages')
