# -*- coding: utf-8 -*-
"""0.45.2 strings: Skin settings > Spotlight & widgets row "Home spotlight: recently watched sets" (row 9757, skin
32561) and its help line (32562). Row labels fit the 520 px label (st_ui_24_bold) in every language: the long ones
drop the "of Home" part. Help lines wrap to two lines in the 1250 x 64 help box (st_small_20). Run from the skin
folder; writes (or rewrites) both strings in every language."""
import io
import os
import re

SKIN = {
    32561: 'Home spotlight: recently watched sets',
    32562: 'The spotlight of a Home item that shows movie sets (Sets, for example) lists the sets you watched last, newest first. Off: all sets, as its spotlight settings say.',
}
TR = {
    'cs_cz': ('Spotlight: nedávno zhlédnuté kolekce',
              'Spotlight položky Domů, která ukazuje filmové kolekce (třeba Kolekce), ukáže kolekce, které jste sledovali naposledy, od nejnovější. Vypnuto: všechny kolekce podle nastavení jejího Spotlightu.'),
    'da_dk': ('Spotlight på Hjem: senest sete samlinger',
              'Spotlight for et Hjem-punkt, der viser filmsamlinger (f.eks. Samlinger), viser de samlinger, du senest har set, nyeste først. Fra: alle samlinger som valgt i dets Spotlight-indstillinger.'),
    'de_de': ('Spotlight: zuletzt gesehene Sammlungen',
              'Der Spotlight eines Startseiten-Eintrags mit Filmsammlungen (etwa Sammlungen) zeigt die zuletzt gesehenen Sammlungen, die neueste zuerst. Aus: alle Sammlungen wie in seinen Spotlight-Einstellungen.'),
    'el_gr': ('Spotlight: συλλογές που είδατε πρόσφατα',
              'Το Spotlight ενός στοιχείου της Αρχικής με συλλογές ταινιών (π.χ. Συλλογές) δείχνει τις συλλογές που είδατε τελευταίες, πρώτα τη νεότερη. Ανενεργό: όλες οι συλλογές, όπως στις ρυθμίσεις του Spotlight.'),
    'es_es': ('Spotlight: colecciones vistas recientemente',
              'El Spotlight de un elemento de Inicio con colecciones de películas (por ejemplo, Colecciones) muestra las que viste por última vez, la más reciente primero. Desactivado: todas, según sus ajustes de Spotlight.'),
    'fi_fi': ('Kodin Spotlight: viimeksi katsotut kokoelmat',
              'Elokuvakokoelmia näyttävän Kodin kohteen (esim. Kokoelmat) Spotlight näyttää viimeksi katsomasi kokoelmat uusin ensin. Pois: kaikki kokoelmat sen Spotlight-asetusten mukaan.'),
    'fr_fr': ('Spotlight : collections vues récemment',
              "Le Spotlight d'un élément de l'accueil qui montre des collections de films (par exemple Collections) affiche celles vues en dernier, la plus récente d'abord. Désactivé : toutes, selon ses réglages de Spotlight."),
    'hu_hu': ('Spotlight: nemrég megnézett gyűjtemények',
              'A filmgyűjteményeket mutató kezdőlapi elem (például Gyűjtemények) Spotlightja a legutóbb megnézett gyűjteményeket mutatja, a legújabbal kezdve. Ki: minden gyűjtemény a Spotlight-beállításai szerint.'),
    'it_it': ('Spotlight: collezioni viste di recente',
              'Lo Spotlight di una voce della Home con collezioni di film (per esempio Collezioni) mostra quelle viste per ultime, la più recente per prima. Disattivato: tutte, secondo le sue impostazioni Spotlight.'),
    'ja_jp': ('ホームの Spotlight: 最近視聴したコレクション',
              '映画コレクションを表示するホームの項目 (例: コレクション) の Spotlight に、最近視聴したコレクションを新しい順に表示します。オフ: Spotlight 設定どおりにすべてのコレクションを表示します。'),
    'ko_kr': ('홈 Spotlight: 최근 시청한 컬렉션',
              '영화 컬렉션을 보여 주는 홈 항목(예: 컬렉션)의 Spotlight에 최근 시청한 컬렉션을 최신순으로 보여 줍니다. 끔: Spotlight 설정대로 모든 컬렉션을 보여 줍니다.'),
    'nb_no': ('Spotlight på Hjem: nylig sette samlinger',
              'Spotlight for et Hjem-element som viser filmsamlinger (for eksempel Samlinger), viser samlingene du så sist, nyeste først. Av: alle samlinger slik Spotlight-innstillingene sier.'),
    'nl_nl': ('Spotlight op Start: recent bekeken collecties',
              'De Spotlight van een Start-onderdeel met filmcollecties (bijvoorbeeld Collecties) toont de collecties die je het laatst hebt bekeken, nieuwste eerst. Uit: alle collecties, zoals in de Spotlight-instellingen.'),
    'pl_pl': ('Spotlight: ostatnio obejrzane kolekcje',
              'Spotlight pozycji ekranu głównego z kolekcjami filmów (np. Kolekcje) pokazuje ostatnio obejrzane kolekcje, od najnowszej. Wyłączone: wszystkie kolekcje według ustawień jej Spotlightu.'),
    'pt_br': ('Spotlight: coleções assistidas recentemente',
              'O Spotlight de um item do Início com coleções de filmes (por exemplo, Coleções) mostra as que você assistiu por último, a mais recente primeiro. Desligado: todas, conforme as configurações do Spotlight.'),
    'pt_pt': ('Spotlight: coleções vistas recentemente',
              'O Spotlight de um item do Início com coleções de filmes (por exemplo, Coleções) mostra as que viu por último, a mais recente primeiro. Desligado: todas, conforme as definições do Spotlight.'),
    'ru_ru': ('Spotlight: недавние просмотры коллекций',
              'Spotlight пункта главной с коллекциями фильмов (например, «Коллекции») показывает недавно просмотренные коллекции, начиная с новейшей. Выкл.: все коллекции по настройкам его Spotlight.'),
    'sv_se': ('Hems Spotlight: nyligen sedda samlingar',
              'Spotlight för ett Hem-objekt som visar filmsamlingar (till exempel Samlingar) visar de samlingar du såg senast, nyaste först. Av: alla samlingar enligt dess Spotlight-inställningar.'),
    'tr_tr': ('Ana sayfa Spotlight: son izlenen koleksiyonlar',
              "Film koleksiyonlarını gösteren bir Ana sayfa öğesinin (örneğin Koleksiyonlar) Spotlight'ı, en son izlediğiniz koleksiyonları en yenisi önce gösterir. Kapalı: Spotlight ayarlarına göre tüm koleksiyonlar."),
    'uk_ua': ('Spotlight: нещодавно переглянуті колекції',
              'Spotlight пункту головної з колекціями фільмів (наприклад, «Колекції») показує нещодавно переглянуті колекції, починаючи з найновішої. Вимк.: усі колекції за налаштуваннями його Spotlight.'),
    'zh_cn': ('主页 Spotlight：最近观看的合集',
              '显示电影合集的主页项目（例如“合集”）的 Spotlight 按从新到旧显示你最近观看的合集。关闭：按其 Spotlight 设置显示所有合集。'),
    'zh_tw': ('首頁 Spotlight：最近觀看的系列',
              '顯示電影系列的首頁項目（例如「系列」）的 Spotlight 依由新到舊顯示你最近觀看的系列。關閉：依其 Spotlight 設定顯示所有系列。'),
}


def esc(text):
    return text.replace('\\', '\\\\').replace('"', '\\"')


def write(folder, strings):
    done = 0
    for d in sorted(os.listdir(folder)):
        lang = d.replace('resource.language.', '')
        p = os.path.join(folder, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        tr = TR.get(lang)
        assert tr or lang == 'en_gb', lang
        for i, ident in enumerate(sorted(strings)):
            entry = 'msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (
                ident, esc(strings[ident]), '' if lang == 'en_gb' else esc(tr[i]))
            old = re.compile(r'msgctxt "#%d"\nmsgid ".*"\nmsgstr ".*"\n' % ident)
            if old.search(t):
                t = old.sub(lambda _m: entry, t, count=1)
            else:
                t = t.rstrip('\n') + '\n\n' + entry
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        done += 1
    return done


assert len(TR) == 22
print('skin', write('language', SKIN), 'languages')
