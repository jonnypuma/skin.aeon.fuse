# -*- coding: utf-8 -*-
"""0.39.13 Skin settings > Motion & reset: the library art check gets its own rows (the "More options" list of the
helper is not reachable any more: every option sits in a category). Under Reset (and the Linux memory rows):
  9548  Auto-fix art with the wrong shape   switch, On unless Skin.HasSetting(aeon.artguard.off)
  9549  Check library art now               RunScript(script.aeon.helper,artcheck), "Start" on the right
Rows at 541 / 611; where the memory rows are hidden (not Linux) they move up 140. Help lines 32448 / 32449 (all
languages). Run from the skin folder."""
import io
import os
import re

X = '1080i'
HELP = {
    'en_gb': ('After a refresh or a library scan, a poster, banner, landscape or fanart of the wrong shape is replaced by a picture of the same name in the same folder that fits. Your files stay as they are.',
              'Checks every picture Kodi has shown and fixes what it can. A list shows what was replaced and what is still the wrong shape.'),
    'cs_cz': ('Po obnovení nebo prohledání knihovny se plakát, banner, krajina nebo fanart špatného tvaru nahradí vhodným obrázkem stejného jména ze stejné složky. Vaše soubory zůstanou beze změny.',
              'Zkontroluje každý obrázek, který Kodi zobrazilo, a opraví, co jde. Seznam ukáže, co bylo nahrazeno a co má stále špatný tvar.'),
    'da_dk': ('Efter en opdatering eller biblioteksscanning erstattes en plakat, et banner, et landskab eller en fanart med forkert form af et passende billede med samme navn fra samme mappe. Dine filer forbliver uændrede.',
              'Tjekker alle billeder, Kodi har vist, og retter det, der kan rettes. En liste viser, hvad der blev erstattet, og hvad der stadig har forkert form.'),
    'de_de': ('Nach einer Aktualisierung oder einem Bibliotheksscan wird ein Poster, Banner, Landschaftsbild oder Fanart mit falscher Form durch ein passendes Bild gleichen Namens aus demselben Ordner ersetzt. Ihre Dateien bleiben unverändert.',
              'Prüft jedes Bild, das Kodi angezeigt hat, und korrigiert, was möglich ist. Eine Liste zeigt, was ersetzt wurde und was noch die falsche Form hat.'),
    'el_gr': ('Μετά από ανανέωση ή σάρωση της βιβλιοθήκης, μια αφίσα, ένα banner, ένα landscape ή ένα fanart με λάθος σχήμα αντικαθίσταται από κατάλληλη εικόνα με το ίδιο όνομα από τον ίδιο φάκελο. Τα αρχεία σας μένουν ως έχουν.',
              'Ελέγχει κάθε εικόνα που έχει εμφανίσει το Kodi και διορθώνει ό,τι μπορεί. Μια λίστα δείχνει τι αντικαταστάθηκε και τι έχει ακόμα λάθος σχήμα.'),
    'es_es': ('Tras una actualización o un escaneo de la biblioteca, un póster, banner, paisaje o fanart con forma incorrecta se sustituye por una imagen adecuada del mismo nombre de la misma carpeta. Tus archivos no se modifican.',
              'Comprueba cada imagen que Kodi ha mostrado y corrige lo que puede. Una lista muestra lo sustituido y lo que sigue con forma incorrecta.'),
    'fi_fi': ('Päivityksen tai kirjaston skannauksen jälkeen väärän muotoinen juliste, banneri, maisemakuva tai fanart korvataan samannimisellä sopivalla kuvalla samasta kansiosta. Tiedostosi pysyvät ennallaan.',
              'Tarkistaa jokaisen Kodin näyttämän kuvan ja korjaa minkä voi. Luettelo näyttää, mitä korvattiin ja mikä on yhä väärän muotoinen.'),
    'fr_fr': ("Après une actualisation ou une analyse de la médiathèque, une affiche, une bannière, un paysage ou un fanart de mauvaise forme est remplacé par une image adaptée du même nom dans le même dossier. Vos fichiers restent inchangés.",
              "Vérifie chaque image affichée par Kodi et corrige ce qui peut l'être. Une liste indique ce qui a été remplacé et ce qui a encore une mauvaise forme."),
    'hu_hu': ('Frissítés vagy könyvtárkeresés után a rossz alakú poszter, banner, tájkép vagy fanart helyére egy azonos nevű, illő kép kerül ugyanabból a mappából. A fájljai változatlanok maradnak.',
              'Ellenőriz minden képet, amelyet a Kodi megjelenített, és kijavítja, amit lehet. Egy lista mutatja, mi lett lecserélve, és mi rossz alakú még.'),
    'it_it': ("Dopo un aggiornamento o una scansione della libreria, un poster, banner, landscape o fanart di forma errata viene sostituito da un'immagine adatta con lo stesso nome nella stessa cartella. I tuoi file restano invariati.",
              'Controlla ogni immagine mostrata da Kodi e corregge ciò che può. Un elenco mostra cosa è stato sostituito e cosa ha ancora la forma errata.'),
    'ja_jp': ('更新やライブラリのスキャン後、形の合わないポスター、バナー、ランドスケープ、ファンアートを、同じフォルダーにある同じ名前の合う画像に置き換えます。ファイル自体は変更しません。',
              'Kodi が表示したすべての画像を確認し、直せるものを直します。置き換えたものと形が合わないままのものを一覧で表示します。'),
    'ko_kr': ('새로 고침이나 라이브러리 스캔 후 모양이 맞지 않는 포스터, 배너, 랜드스케이프, 팬아트를 같은 폴더에 있는 같은 이름의 맞는 그림으로 바꿉니다. 파일은 그대로 둡니다.',
              'Kodi가 표시한 모든 그림을 확인하고 고칠 수 있는 것을 고칩니다. 바꾼 것과 여전히 모양이 맞지 않는 것을 목록으로 보여 줍니다.'),
    'nb_no': ('Etter en oppdatering eller et biblioteksøk erstattes en plakat, et banner, et landskap eller en fanart med feil form av et passende bilde med samme navn fra samme mappe. Filene dine forblir uendret.',
              'Sjekker alle bilder Kodi har vist, og retter det som kan rettes. En liste viser hva som ble erstattet og hva som fortsatt har feil form.'),
    'nl_nl': ('Na een vernieuwing of bibliotheekscan wordt een poster, banner, landschap of fanart met de verkeerde vorm vervangen door een passende afbeelding met dezelfde naam uit dezelfde map. Je bestanden blijven zoals ze zijn.',
              'Controleert elke afbeelding die Kodi heeft getoond en herstelt wat kan. Een lijst toont wat vervangen is en wat nog de verkeerde vorm heeft.'),
    'pl_pl': ('Po odświeżeniu lub skanowaniu biblioteki plakat, baner, krajobraz lub fanart o złym kształcie zostaje zastąpiony pasującym obrazem o tej samej nazwie z tego samego folderu. Twoje pliki pozostają bez zmian.',
              'Sprawdza każdy obraz wyświetlony przez Kodi i poprawia, co się da. Lista pokazuje, co zastąpiono, a co nadal ma zły kształt.'),
    'pt_br': ('Após uma atualização ou varredura da biblioteca, um pôster, banner, paisagem ou fanart com formato errado é substituído por uma imagem adequada com o mesmo nome da mesma pasta. Seus arquivos permanecem como estão.',
              'Verifica cada imagem que o Kodi mostrou e corrige o que puder. Uma lista mostra o que foi substituído e o que ainda está com formato errado.'),
    'pt_pt': ('Após uma atualização ou análise da biblioteca, um póster, banner, paisagem ou fanart com formato errado é substituído por uma imagem adequada com o mesmo nome da mesma pasta. Os seus ficheiros mantêm-se inalterados.',
              'Verifica cada imagem que o Kodi mostrou e corrige o que for possível. Uma lista mostra o que foi substituído e o que continua com formato errado.'),
    'ru_ru': ('После обновления или сканирования медиатеки постер, баннер, пейзаж или фанарт неправильной формы заменяется подходящим изображением с тем же именем из той же папки. Ваши файлы не изменяются.',
              'Проверяет каждое изображение, которое показывал Kodi, и исправляет, что можно. Список показывает, что заменено и что всё ещё неправильной формы.'),
    'sv_se': ('Efter en uppdatering eller biblioteksskanning ersätts en affisch, banner, landskapsbild eller fanart med fel form av en passande bild med samma namn från samma mapp. Dina filer förblir oförändrade.',
              'Kontrollerar varje bild som Kodi har visat och rättar det som går. En lista visar vad som ersattes och vad som fortfarande har fel form.'),
    'tr_tr': ('Yenilemeden veya kütüphane taramasından sonra yanlış biçimli afiş, banner, manzara ya da fanart, aynı klasördeki aynı adlı uygun bir görselle değiştirilir. Dosyalarınız olduğu gibi kalır.',
              "Kodi'nin gösterdiği her görseli denetler ve düzeltilebilenleri düzeltir. Bir liste neyin değiştirildiğini ve neyin hâlâ yanlış biçimde olduğunu gösterir."),
    'uk_ua': ('Після оновлення або сканування медіатеки постер, банер, пейзаж чи фанарт неправильної форми замінюється відповідним зображенням з тією ж назвою з тієї ж теки. Ваші файли не змінюються.',
              'Перевіряє кожне зображення, яке показував Kodi, і виправляє, що можна. Список показує, що замінено і що досі неправильної форми.'),
    'zh_cn': ('刷新或扫描媒体库后，形状不对的海报、横幅、风景图或同人画会换成同一文件夹中同名且形状合适的图片。你的文件保持不变。',
              '检查 Kodi 显示过的每张图片，能修正的就修正。列表显示已替换的和仍然形状不对的图片。'),
    'zh_tw': ('重新整理或掃描媒體櫃後，形狀不對的海報、橫幅、風景圖或背景圖會換成同一資料夾中同名且形狀合適的圖片。你的檔案保持不變。',
              '檢查 Kodi 顯示過的每張圖片，能修正的就修正。清單會列出已替換的與仍然形狀不對的圖片。'),
}

# ---- strings 32448 / 32449
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32448"' in t:
        continue
    en, tr = HELP['en_gb'], HELP[lang]
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate((32448, 32449)):
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, en[i].replace('"', '\\"'), '' if lang == 'en_gb' else tr[i].replace('"', '\\"'))
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

# ---- rows
p = os.path.join(X, 'SkinSettings.xml')
s = io.open(p, encoding='utf-8').read()


def once(old, new):
    global s
    assert s.count(old) == 1, old[:90]
    s = s.replace(old, new)


SLIDE = '<animation effect="slide" end="0,-140" time="0" condition="!$EXP[Aeon_MemTrimRows]">Conditional</animation>'

# focus bars: copies of Reset's (9541) at 541 / 611
a = s.index('\t\t\t\t<top>331</top>\n\t\t\t\t<visible>Control.HasFocus(9541)</visible>')
a = s.rindex('\t\t\t<control type="group">', 0, a)
# a group closes with exactly three tabs: match the whole line (a four-tab close contains the three-tab text)
CLOSE = '\n\t\t\t</control>\n'
b = s.index(CLOSE, a) + len(CLOSE)
bar = s[a:b]
bars = ''
for ident, top in ((9548, 541), (9549, 611)):
    bars += bar.replace('<top>331</top>', '<top>%d</top>\n\t\t\t\t%s' % (top, SLIDE)).replace('Control.HasFocus(9541)', 'Control.HasFocus(%d)' % ident)
s = s[:b] + bars + s[b:]

# the switch row: Reduce motion's (9540) chrome and switch pictures, with its own button
# the row group that holds button 9540 (the same opening lines start rows on other pages too)
a = s.rindex('\t\t\t<control type="group">\n\t\t\t\t<top>191</top>\n', 0, s.index('<control type="button" id="9540">'))
b = s.index(CLOSE, s.index('<control type="button" id="9540">', a)) + len(CLOSE)
row = s[a:b]
head = row[:row.index('\t\t\t\t<control type="button" id="9540">')]
tail = row[row.index('\t\t\t\t</control>\n', row.index('<control type="button" id="9540">')) + len('\t\t\t\t</control>\n'):]
head = head.replace('<top>191</top>', '<top>541</top>\n\t\t\t\t' + SLIDE).replace('delay="0"', 'delay="80"')
head = head.replace('<param name="id" value="9540"/><param name="label" value="$LOCALIZE[31058]"/>',
                    '<param name="id" value="9548"/><param name="label" value="$ADDON[skin.aeon.fuse 32441]"/>')
head = re.sub(r'<param name="icon" value="[^"]*"/>', '<param name="icon" value="aeon/icons/poster.png"/>', head)
tail = tail.replace('Skin.HasSetting(aeon.reducemotion)', '!Skin.HasSetting(aeon.artguard.off)').replace('9540', '9548')
button = '''				<control type="button" id="9548">
					<include>Dlg_SkinRowButton</include>
					<onup condition="$EXP[Aeon_MemTrimRows]">SetFocus(9544)</onup><onup condition="!$EXP[Aeon_MemTrimRows]">SetFocus(9541)</onup>
					<ondown>9549</ondown>
					<onback>9553</onback>
					<onclick condition="Skin.HasSetting(aeon.artguard.off)">Skin.Reset(aeon.artguard.off)</onclick>
					<onclick condition="!Skin.HasSetting(aeon.artguard.off)">Skin.SetBool(aeon.artguard.off)</onclick>
					<onleft>SetFocus(9553)</onleft>
				</control>
'''
switch_row = '\t\t\t<!-- 0.39.13 library art (script.aeon.helper artguard.py): auto-fix after library updates, and a check now -->\n' + head + button + tail

# the action row: the setup wizard's (9545)
a = s.index('\t\t\t<!-- the setup wizard (dialog 1173), any time -->')
b = s.index(CLOSE, s.index('<control type="button" id="9545">', a)) + len(CLOSE)
wiz = s[a:b]
act = wiz.replace('\t\t\t<!-- the setup wizard (dialog 1173), any time -->\n', '')
act = act.replace('<top>261</top>', '<top>611</top>\n\t\t\t\t' + SLIDE).replace('delay="20"', 'delay="100"')
act = act.replace('<param name="id" value="9545"/><param name="label" value="$ADDON[skin.aeon.fuse 32361]"/>',
                  '<param name="id" value="9549"/><param name="label" value="$ADDON[skin.aeon.fuse 32442]"/>')
act = re.sub(r'<param name="icon" value="[^"]*"/>', '<param name="icon" value="aeon/icons/search.png"/>', act)
act = act.replace('<control type="button" id="9545">', '<control type="button" id="9549">')
act = act.replace('<onup>9540</onup>\n\t\t\t\t\t<ondown>9541</ondown>', '<onup>9548</onup>\n\t\t\t\t\t<ondown>9540</ondown>')
act = act.replace('<onclick>RunScript(script.aeon.helper,wizard,open)</onclick>', '<onclick>RunScript(script.aeon.helper,artcheck)</onclick>')
act = act.replace('Control.HasFocus(9545)', 'Control.HasFocus(9549)').replace('$ADDON[skin.aeon.fuse 32362]', '$ADDON[skin.aeon.fuse 32035]')
assert '9545' not in act and '9549' in act and 'artcheck' in act

# both rows after the memory rows, at the end of the Motion & reset page
end_mem = s.index('</control>\n\t\t</control>\n\t\t<control type="group">\n\t\t\t<left>600</left>', s.index('<control type="button" id="9544">'))
cut = end_mem + len('</control>\n')
s = s[:cut] + switch_row + act + s[cut:]

# navigation: Reset / memory rows go down to the new rows, Reduce motion goes up to the last one
once('<ondown condition="$EXP[Aeon_MemTrimRows]">SetFocus(9543)</ondown><ondown condition="!$EXP[Aeon_MemTrimRows]">SetFocus(9540)</ondown>',
     '<ondown condition="$EXP[Aeon_MemTrimRows]">SetFocus(9543)</ondown><ondown condition="!$EXP[Aeon_MemTrimRows]">SetFocus(9548)</ondown>')
once('<onup>9543</onup>\n\t\t\t\t\t\t<ondown>9540</ondown>', '<onup>9543</onup>\n\t\t\t\t\t\t<ondown>9548</ondown>')
once('<onup condition="$EXP[Aeon_MemTrimRows]">SetFocus(9544)</onup><onup condition="!$EXP[Aeon_MemTrimRows]">SetFocus(9541)</onup>\n\t\t\t\t\t<ondown>9545</ondown>',
     '<onup>9549</onup>\n\t\t\t\t\t<ondown>9545</ondown>')
io.open(p, 'w', encoding='utf-8', newline='').write(s)

# help lines
p = os.path.join(X, 'Includes_Settings.xml')
t = io.open(p, encoding='utf-8').read()
old = '\t<variable name="Dlg_SkinHelp">\n'
assert t.count(old) == 1
t = t.replace(old, old + '\t\t<value condition="Control.HasFocus(9548)">$ADDON[skin.aeon.fuse 32448]</value>\n'
                          '\t\t<value condition="Control.HasFocus(9549)">$ADDON[skin.aeon.fuse 32449]</value>\n')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('rows 9548 / 9549 added')
