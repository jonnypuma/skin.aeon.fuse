# -*- coding: utf-8 -*-
"""0.40.0 strings 32452-32457: the Aeon theme's menu styles (Skin settings > Appearance > Menu theme), all languages.
Run from the skin folder."""
import io
import os

EN = {
    32452: 'Mosaic',
    32453: 'Ledger',
    32454: 'Bridge',
    32455: 'Tab slab',
    32456: 'How the menus join their boxes: Mosaic, Ledger, Bridge or Tab slab. Fuse uses rounded cards and needs Kodi to start again.',
    32457: 'Glass keeps its own menus. Fuse uses rounded cards and needs Kodi to start again.',
}
TR = {
    'cs_cz': ('Mozaika', 'Kniha', 'Most', 'Karta',
              'Jak menu spojují své boxy: Mozaika, Kniha, Most nebo Karta. Fuse používá zaoblené karty a vyžaduje nové spuštění Kodi.',
              'Glass si ponechává vlastní menu. Fuse používá zaoblené karty a vyžaduje nové spuštění Kodi.'),
    'da_dk': ('Mosaik', 'Protokol', 'Bro', 'Fane',
              'Sådan samler menuerne deres bokse: Mosaik, Protokol, Bro eller Fane. Fuse bruger afrundede kort og kræver, at Kodi starter igen.',
              'Glass beholder sine egne menuer. Fuse bruger afrundede kort og kræver, at Kodi starter igen.'),
    'de_de': ('Mosaik', 'Tabelle', 'Brücke', 'Reiter',
              'Wie die Menüs ihre Boxen verbinden: Mosaik, Tabelle, Brücke oder Reiter. Fuse nutzt abgerundete Karten und braucht einen Neustart von Kodi.',
              'Glass behält seine eigenen Menüs. Fuse nutzt abgerundete Karten und braucht einen Neustart von Kodi.'),
    'el_gr': ('Ψηφιδωτό', 'Κατάστιχο', 'Γέφυρα', 'Καρτέλα',
              'Πώς τα μενού ενώνουν τα πλαίσιά τους: Ψηφιδωτό, Κατάστιχο, Γέφυρα ή Καρτέλα. Το Fuse χρησιμοποιεί στρογγυλεμένες κάρτες και θέλει επανεκκίνηση του Kodi.',
              'Το Glass κρατά τα δικά του μενού. Το Fuse χρησιμοποιεί στρογγυλεμένες κάρτες και θέλει επανεκκίνηση του Kodi.'),
    'es_es': ('Mosaico', 'Libro', 'Puente', 'Pestaña',
              'Cómo unen los menús sus cajas: Mosaico, Libro, Puente o Pestaña. Fuse usa tarjetas redondeadas y necesita reiniciar Kodi.',
              'Glass mantiene sus propios menús. Fuse usa tarjetas redondeadas y necesita reiniciar Kodi.'),
    'fi_fi': ('Mosaiikki', 'Kirja', 'Silta', 'Välilehti',
              'Miten valikot liittävät laatikkonsa: Mosaiikki, Kirja, Silta tai Välilehti. Fuse käyttää pyöristettyjä kortteja ja vaatii Kodin uudelleenkäynnistyksen.',
              'Glass pitää omat valikkonsa. Fuse käyttää pyöristettyjä kortteja ja vaatii Kodin uudelleenkäynnistyksen.'),
    'fr_fr': ('Mosaïque', 'Registre', 'Pont', 'Onglet',
              'Comment les menus assemblent leurs blocs : Mosaïque, Registre, Pont ou Onglet. Fuse utilise des cartes arrondies et demande de relancer Kodi.',
              'Glass garde ses propres menus. Fuse utilise des cartes arrondies et demande de relancer Kodi.'),
    'hu_hu': ('Mozaik', 'Főkönyv', 'Híd', 'Fül',
              'Hogyan illesztik a menük a dobozaikat: Mozaik, Főkönyv, Híd vagy Fül. A Fuse lekerekített kártyákat használ, és a Kodi újraindítását kéri.',
              'A Glass megtartja saját menüit. A Fuse lekerekített kártyákat használ, és a Kodi újraindítását kéri.'),
    'it_it': ('Mosaico', 'Registro', 'Ponte', 'Scheda',
              'Come i menu uniscono i loro riquadri: Mosaico, Registro, Ponte o Scheda. Fuse usa schede arrotondate e richiede di riavviare Kodi.',
              'Glass mantiene i propri menu. Fuse usa schede arrotondate e richiede di riavviare Kodi.'),
    'ja_jp': ('モザイク', '台帳', 'ブリッジ', 'タブ',
              'メニューのボックスのつなぎ方: モザイク、台帳、ブリッジ、タブ。Fuse は角の丸いカードを使い、Kodi の再起動が必要です。',
              'Glass は独自のメニューを使います。Fuse は角の丸いカードを使い、Kodi の再起動が必要です。'),
    'ko_kr': ('모자이크', '장부', '브리지', '탭',
              '메뉴가 상자를 잇는 방식: 모자이크, 장부, 브리지, 탭. Fuse는 둥근 카드를 쓰며 Kodi를 다시 시작해야 합니다.',
              'Glass는 자체 메뉴를 유지합니다. Fuse는 둥근 카드를 쓰며 Kodi를 다시 시작해야 합니다.'),
    'nb_no': ('Mosaikk', 'Protokoll', 'Bro', 'Fane',
              'Slik setter menyene sammen boksene sine: Mosaikk, Protokoll, Bro eller Fane. Fuse bruker avrundede kort og krever at Kodi starter på nytt.',
              'Glass beholder sine egne menyer. Fuse bruker avrundede kort og krever at Kodi starter på nytt.'),
    'nl_nl': ('Mozaïek', 'Grootboek', 'Brug', 'Tabblad',
              'Hoe de menu\'s hun vakken samenvoegen: Mozaïek, Grootboek, Brug of Tabblad. Fuse gebruikt afgeronde kaarten en vraagt om Kodi opnieuw te starten.',
              'Glass houdt zijn eigen menu\'s. Fuse gebruikt afgeronde kaarten en vraagt om Kodi opnieuw te starten.'),
    'pl_pl': ('Mozaika', 'Księga', 'Most', 'Karta',
              'Jak menu łączą swoje pola: Mozaika, Księga, Most lub Karta. Fuse używa zaokrąglonych kart i wymaga ponownego uruchomienia Kodi.',
              'Glass zachowuje własne menu. Fuse używa zaokrąglonych kart i wymaga ponownego uruchomienia Kodi.'),
    'pt_br': ('Mosaico', 'Livro', 'Ponte', 'Aba',
              'Como os menus juntam suas caixas: Mosaico, Livro, Ponte ou Aba. Fuse usa cartões arredondados e precisa reiniciar o Kodi.',
              'Glass mantém seus próprios menus. Fuse usa cartões arredondados e precisa reiniciar o Kodi.'),
    'pt_pt': ('Mosaico', 'Livro', 'Ponte', 'Separador',
              'Como os menus juntam as suas caixas: Mosaico, Livro, Ponte ou Separador. Fuse usa cartões arredondados e precisa de reiniciar o Kodi.',
              'Glass mantém os seus próprios menus. Fuse usa cartões arredondados e precisa de reiniciar o Kodi.'),
    'ru_ru': ('Мозаика', 'Реестр', 'Мост', 'Вкладка',
              'Как меню соединяют свои блоки: Мозаика, Реестр, Мост или Вкладка. Fuse использует скруглённые карточки и требует перезапуска Kodi.',
              'Glass сохраняет собственные меню. Fuse использует скруглённые карточки и требует перезапуска Kodi.'),
    'sv_se': ('Mosaik', 'Liggare', 'Bro', 'Flik',
              'Hur menyerna fogar ihop sina rutor: Mosaik, Liggare, Bro eller Flik. Fuse använder rundade kort och kräver att Kodi startas om.',
              'Glass behåller sina egna menyer. Fuse använder rundade kort och kräver att Kodi startas om.'),
    'tr_tr': ('Mozaik', 'Defter', 'Köprü', 'Sekme',
              'Menülerin kutularını birleştirme biçimi: Mozaik, Defter, Köprü veya Sekme. Fuse yuvarlatılmış kartlar kullanır ve Kodi\'nin yeniden başlamasını ister.',
              'Glass kendi menülerini korur. Fuse yuvarlatılmış kartlar kullanır ve Kodi\'nin yeniden başlamasını ister.'),
    'uk_ua': ('Мозаїка', 'Реєстр', 'Міст', 'Вкладка',
              'Як меню поєднують свої блоки: Мозаїка, Реєстр, Міст або Вкладка. Fuse використовує заокруглені картки й потребує перезапуску Kodi.',
              'Glass зберігає власні меню. Fuse використовує заокруглені картки й потребує перезапуску Kodi.'),
    'zh_cn': ('马赛克', '账本', '桥', '标签',
              '菜单拼接方框的方式：马赛克、账本、桥或标签。Fuse 使用圆角卡片，需要重新启动 Kodi。',
              'Glass 保留自己的菜单。Fuse 使用圆角卡片，需要重新启动 Kodi。'),
    'zh_tw': ('馬賽克', '帳本', '橋', '標籤',
              '選單拼接方框的方式：馬賽克、帳本、橋或標籤。Fuse 使用圓角卡片，需要重新啟動 Kodi。',
              'Glass 保留自己的選單。Fuse 使用圓角卡片，需要重新啟動 Kodi。'),
}
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32452"' in t:
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
print('strings 32452-32457 added in %d languages' % done)
