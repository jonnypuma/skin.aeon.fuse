# -*- coding: utf-8 -*-
"""0.56.53 strings, all 23 languages: Delete for custom Home menu items (32795 the question, 32796 the note on the
dimmed button for presets). The button and the dialog heading are Kodi's own "Delete" ($LOCALIZE[117]).
Repeatable."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import strings_05653 as base  # noqa: E402

IDS = [32795, 32796]
EN = ['Delete %s? Its name, path, icon, widgets and submenu are removed; the items below it move up one place.',
      'Custom items only']
T = {
    'cs_cz': ['Smazat %s? Jeho název, cesta, ikona, widgety a podnabídka budou odstraněny; položky pod ní se posunou o jedno místo nahoru.', 'Jen vlastní položky'],
    'da_dk': ['Slet %s? Navn, sti, ikon, widgets og undermenu fjernes; punkterne under det rykker én plads op.', 'Kun egne punkter'],
    'de_de': ['%s löschen? Name, Pfad, Symbol, Widgets und Untermenü werden entfernt; die Einträge darunter rücken eine Stelle nach oben.', 'Nur eigene Einträge'],
    'el_gr': ['Διαγραφή %s; Το όνομα, η διαδρομή, το εικονίδιο, τα widgets και το υπομενού του αφαιρούνται· τα στοιχεία από κάτω ανεβαίνουν μία θέση.', 'Μόνο προσαρμοσμένα στοιχεία'],
    'es_es': ['¿Eliminar %s? Se quitan su nombre, ruta, icono, widgets y submenú; los elementos de debajo suben un puesto.', 'Solo elementos propios'],
    'fi_fi': ['Poistetaanko %s? Sen nimi, polku, kuvake, widgetit ja alivalikko poistetaan; alla olevat kohteet siirtyvät yhden paikan ylös.', 'Vain omat kohteet'],
    'fr_fr': ['Supprimer %s ? Son nom, son chemin, son icône, ses widgets et son sous-menu sont retirés ; les éléments en dessous remontent d’une place.', 'Éléments perso uniquement'],
    'hu_hu': ['Törli: %s? A neve, útvonala, ikonja, widgetjei és almenüje törlődik; az alatta lévő elemek egy hellyel feljebb kerülnek.', 'Csak saját elemek'],
    'it_it': ['Eliminare %s? Nome, percorso, icona, widget e sottomenu vengono rimossi; le voci sotto salgono di un posto.', 'Solo voci personali'],
    'ja_jp': ['%s を削除しますか？名前、パス、アイコン、ウィジェット、サブメニューが削除され、下の項目が1つ上に移動します。', 'カスタム項目のみ'],
    'ko_kr': ['%s 을(를) 삭제할까요? 이름, 경로, 아이콘, 위젯, 하위 메뉴가 지워지고 아래 항목이 한 칸 위로 올라갑니다.', '사용자 항목만'],
    'nb_no': ['Slette %s? Navn, sti, ikon, widgeter og undermeny fjernes; elementene under flyttes én plass opp.', 'Bare egne elementer'],
    'nl_nl': ['%s verwijderen? De naam, het pad, het pictogram, de widgets en het submenu worden gewist; de items eronder schuiven één plaats op.', 'Alleen eigen items'],
    'pl_pl': ['Usunąć %s? Nazwa, ścieżka, ikona, widżety i podmenu zostaną usunięte; pozycje poniżej przesuną się o jedno miejsce w górę.', 'Tylko własne pozycje'],
    'pt_br': ['Excluir %s? O nome, caminho, ícone, widgets e submenu são removidos; os itens abaixo sobem uma posição.', 'Só itens próprios'],
    'pt_pt': ['Eliminar %s? O nome, caminho, ícone, widgets e submenu são removidos; os itens abaixo sobem uma posição.', 'Só itens próprios'],
    'ru_ru': ['Удалить %s? Название, путь, значок, виджеты и подменю будут удалены; пункты ниже поднимутся на одно место.', 'Только свои пункты'],
    'sv_se': ['Ta bort %s? Namn, sökväg, ikon, widgetar och undermeny tas bort; objekten under flyttas upp ett steg.', 'Endast egna objekt'],
    'tr_tr': ['%s silinsin mi? Adı, yolu, simgesi, widget’ları ve alt menüsü kaldırılır; altındaki öğeler bir sıra yukarı çıkar.', 'Yalnızca özel öğeler'],
    'uk_ua': ['Видалити %s? Назву, шлях, значок, віджети й підменю буде видалено; пункти нижче піднімуться на одне місце.', 'Лише власні пункти'],
    'zh_cn': ['删除 %s？其名称、路径、图标、小部件和子菜单将被移除；下方的项目上移一位。', '仅限自定义项目'],
    'zh_tw': ['刪除 %s？其名稱、路徑、圖示、小工具和子選單將被移除；下方的項目上移一位。', '僅限自訂項目'],
}

if __name__ == '__main__':
    base.IDS, base.EN, base.T = IDS, EN, T
    base.main()
