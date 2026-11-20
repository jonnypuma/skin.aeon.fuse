# -*- coding: utf-8 -*-
"""0.39.14 library art check wording: everything happens in Kodi's library, never on disk, and an emptied season slot
shows the show's picture only until real season art arrives. Rewords 32444 / 32447 / 32450, adds 32451 (the
summary's first line). All languages. Run from the skin folder."""
import io
import os
import re

EN = {
    32444: 'Now uses a picture from the same folder that fits',
    32447: 'Fixed in the library: %d',
    32450: "Slot left empty: the skin shows the show's picture until season art is added",
    32451: "Only Kodi's library changed. Your files are untouched.",
}
TR = {
    'cs_cz': ('Nyní používá vhodný obrázek ze stejné složky', 'Opraveno v knihovně: %d', 'Pole ponecháno prázdné: skin ukazuje obrázek seriálu, dokud nepřibude obrázek řady', 'Změnila se jen knihovna Kodi. Vaše soubory zůstaly beze změny.'),
    'da_dk': ('Bruger nu et passende billede fra samme mappe', 'Rettet i biblioteket: %d', 'Feltet er tomt: skinnet viser seriens billede, indtil der kommer sæsonbilleder', 'Kun Kodis bibliotek er ændret. Dine filer er urørte.'),
    'de_de': ('Verwendet jetzt ein passendes Bild aus demselben Ordner', 'In der Bibliothek korrigiert: %d', 'Feld leer gelassen: Der Skin zeigt das Bild der Serie, bis Staffelbilder hinzukommen', 'Nur die Kodi-Bibliothek wurde geändert. Ihre Dateien bleiben unberührt.'),
    'el_gr': ('Χρησιμοποιεί τώρα κατάλληλη εικόνα από τον ίδιο φάκελο', 'Διορθώθηκαν στη βιβλιοθήκη: %d', 'Η θέση έμεινε κενή: το skin δείχνει την εικόνα της σειράς μέχρι να προστεθεί εικόνα σεζόν', 'Άλλαξε μόνο η βιβλιοθήκη του Kodi. Τα αρχεία σας δεν άλλαξαν.'),
    'es_es': ('Ahora usa una imagen adecuada de la misma carpeta', 'Corregidas en la biblioteca: %d', 'Hueco vacío: la skin muestra la imagen de la serie hasta que haya imágenes de la temporada', 'Solo cambió la biblioteca de Kodi. Tus archivos no se han tocado.'),
    'fi_fi': ('Käyttää nyt sopivaa kuvaa samasta kansiosta', 'Korjattu kirjastossa: %d', 'Paikka jätetty tyhjäksi: teema näyttää sarjan kuvan, kunnes kaudelle lisätään kuva', 'Vain Kodin kirjasto muuttui. Tiedostoihisi ei koskettu.'),
    'fr_fr': ('Utilise désormais une image adaptée du même dossier', 'Corrigées dans la médiathèque : %d', "Emplacement laissé vide : le skin affiche l'image de la série jusqu'à l'ajout d'images de saison", 'Seule la médiathèque de Kodi a changé. Vos fichiers ne sont pas modifiés.'),
    'hu_hu': ('Most egy illő képet használ ugyanabból a mappából', 'Javítva a könyvtárban: %d', 'A hely üresen maradt: a felület a sorozat képét mutatja, amíg nincs évadkép', 'Csak a Kodi könyvtára változott. A fájljaihoz nem nyúlt.'),
    'it_it': ("Ora usa un'immagine adatta della stessa cartella", 'Corrette nella libreria: %d', "Spazio lasciato vuoto: la skin mostra l'immagine della serie finché non c'è un'immagine della stagione", 'È cambiata solo la libreria di Kodi. I tuoi file non sono stati toccati.'),
    'ja_jp': ('同じフォルダーの合う画像を使うようにしました', 'ライブラリで修正: %d', '空欄のまま：シーズンの画像が入るまでスキンが番組の画像を表示します', '変更したのは Kodi のライブラリだけです。ファイルはそのままです。'),
    'ko_kr': ('이제 같은 폴더의 맞는 그림을 사용함', '라이브러리에서 수정함: %d', '칸을 비워 둠: 시즌 그림이 추가될 때까지 스킨이 프로그램 그림을 보여 줌', 'Kodi 라이브러리만 바뀌었습니다. 파일은 그대로입니다.'),
    'nb_no': ('Bruker nå et passende bilde fra samme mappe', 'Rettet i biblioteket: %d', 'Feltet står tomt: skallet viser seriens bilde til sesongbilder kommer', 'Bare Kodis bibliotek er endret. Filene dine er urørt.'),
    'nl_nl': ('Gebruikt nu een passende afbeelding uit dezelfde map', 'Hersteld in de bibliotheek: %d', 'Plek leeg gelaten: de skin toont de afbeelding van de serie tot er seizoensafbeeldingen zijn', 'Alleen de bibliotheek van Kodi is gewijzigd. Je bestanden zijn ongemoeid gelaten.'),
    'pl_pl': ('Teraz używa pasującego obrazu z tego samego folderu', 'Poprawiono w bibliotece: %d', 'Pole pozostawione puste: skórka pokazuje obraz serialu, dopóki nie pojawi się obraz sezonu', 'Zmieniła się tylko biblioteka Kodi. Twoje pliki pozostały nietknięte.'),
    'pt_br': ('Agora usa uma imagem adequada da mesma pasta', 'Corrigidas na biblioteca: %d', 'Espaço deixado vazio: a skin mostra a imagem da série até haver imagens da temporada', 'Só a biblioteca do Kodi mudou. Seus arquivos não foram tocados.'),
    'pt_pt': ('Agora usa uma imagem adequada da mesma pasta', 'Corrigidas na biblioteca: %d', 'Espaço deixado vazio: o skin mostra a imagem da série até haver imagens da temporada', 'Só a biblioteca do Kodi mudou. Os seus ficheiros não foram tocados.'),
    'ru_ru': ('Теперь использует подходящее изображение из той же папки', 'Исправлено в медиатеке: %d', 'Поле оставлено пустым: обложка показывает изображение сериала, пока не появится изображение сезона', 'Изменилась только медиатека Kodi. Ваши файлы не тронуты.'),
    'sv_se': ('Använder nu en passande bild från samma mapp', 'Rättade i biblioteket: %d', 'Platsen lämnas tom: skalet visar seriens bild tills säsongsbilder finns', 'Bara Kodis bibliotek har ändrats. Dina filer är orörda.'),
    'tr_tr': ('Artık aynı klasördeki uygun bir görseli kullanıyor', 'Kütüphanede düzeltildi: %d', 'Alan boş bırakıldı: sezon görseli eklenene kadar tema dizinin görselini gösterir', 'Yalnızca Kodi kütüphanesi değişti. Dosyalarınıza dokunulmadı.'),
    'uk_ua': ('Тепер використовує відповідне зображення з тієї ж теки', 'Виправлено в медіатеці: %d', "Поле залишено порожнім: оболонка показує зображення серіалу, доки не з'явиться зображення сезону", 'Змінилася лише медіатека Kodi. Ваші файли не змінено.'),
    'zh_cn': ('现在使用同一文件夹中合适的图片', '已在媒体库中修正：%d', '此项留空：在加入季图片前，皮肤会显示剧集图片', '只更改了 Kodi 的媒体库，你的文件没有改动。'),
    'zh_tw': ('現在使用同一資料夾中合適的圖片', '已在媒體櫃中修正：%d', '此欄留空：在加入季圖片前，外觀會顯示影集圖片', '只變更了 Kodi 的媒體櫃，你的檔案沒有改動。'),
}
IDS = sorted(EN)
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    for i, ident in enumerate(IDS):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else TR[lang][i].replace('"', '\\"')
        entry = 'msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
        m = re.search(r'msgctxt "#%d"\nmsgid "[^\n]*"\nmsgstr "[^\n]*"\n' % ident, t)
        if m:
            t = t[:m.start()] + entry + t[m.end():]
        else:
            t = t.rstrip('\n') + '\n\n' + entry
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('32444 / 32447 / 32450 reworded, 32451 added in %d languages' % len(os.listdir('language')))
