# -*- coding: utf-8 -*-
"""0.39.13 strings 32441-32447 for the helper's library art check (artguard.py, More options), all languages.
Run from the skin folder."""
import io
import os

EN = {
    32441: 'Auto-fix art with the wrong shape',
    32442: 'Check library art now',
    32443: 'Library art',
    32444: 'Replaced with a picture that fits from the same folder',
    32445: 'Wrong shape, nothing in the folder fits',
    32446: 'Every picture has the right shape.',
    32447: 'Replaced with a picture that fits: %d',
}
TR = {
    'cs_cz': ('Opravovat obrázky špatného tvaru', 'Zkontrolovat obrázky knihovny', 'Obrázky knihovny',
              'Nahrazeno vhodným obrázkem ze stejné složky', 'Špatný tvar, ve složce není nic vhodného',
              'Všechny obrázky mají správný tvar.', 'Nahrazeno vhodným obrázkem: %d'),
    'da_dk': ('Ret billeder med forkert form', 'Tjek bibliotekets billeder nu', 'Bibliotekets billeder',
              'Erstattet med et passende billede fra samme mappe', 'Forkert form, intet i mappen passer',
              'Alle billeder har den rigtige form.', 'Erstattet med et passende billede: %d'),
    'de_de': ('Falsch geformte Bilder korrigieren', 'Bibliotheksbilder jetzt prüfen',
              'Bibliotheksbilder', 'Durch ein passendes Bild aus demselben Ordner ersetzt', 'Falsche Form, nichts im Ordner passt',
              'Alle Bilder haben die richtige Form.', 'Durch ein passendes Bild ersetzt: %d'),
    'el_gr': ('Αυτόματη διόρθωση εικόνων με λάθος σχήμα', 'Έλεγχος εικόνων βιβλιοθήκης τώρα',
              'Εικόνες βιβλιοθήκης', 'Αντικαταστάθηκε με κατάλληλη εικόνα από τον ίδιο φάκελο',
              'Λάθος σχήμα, τίποτα στον φάκελο δεν ταιριάζει', 'Όλες οι εικόνες έχουν το σωστό σχήμα.',
              'Αντικαταστάθηκαν με κατάλληλη εικόνα: %d'),
    'es_es': ('Corregir imágenes de forma incorrecta', 'Comprobar ahora las imágenes de la biblioteca',
              'Imágenes de la biblioteca', 'Sustituida por una imagen adecuada de la misma carpeta',
              'Forma incorrecta, nada en la carpeta encaja', 'Todas las imágenes tienen la forma correcta.',
              'Sustituidas por una imagen adecuada: %d'),
    'fi_fi': ('Korjaa väärän muotoiset kuvat', 'Tarkista kirjaston kuvat nyt', 'Kirjaston kuvat',
              'Korvattu sopivalla kuvalla samasta kansiosta', 'Väärä muoto, kansiossa ei ole sopivaa kuvaa',
              'Kaikki kuvat ovat oikean muotoisia.', 'Korvattu sopivalla kuvalla: %d'),
    'fr_fr': ('Corriger les images mal proportionnées',
              'Vérifier maintenant les images de la médiathèque', 'Images de la médiathèque',
              'Remplacée par une image adaptée du même dossier', 'Mauvaise forme, rien ne convient dans le dossier',
              'Toutes les images ont la bonne forme.', 'Remplacées par une image adaptée : %d'),
    'hu_hu': ('Rossz alakú képek javítása', 'Könyvtár képeinek ellenőrzése most', 'Könyvtár képei',
              'Lecserélve egy illő képre ugyanabból a mappából', 'Rossz alak, a mappában nincs illő kép',
              'Minden kép alakja megfelelő.', 'Lecserélve illő képre: %d'),
    'it_it': ('Correggi immagini di forma errata',
              'Controlla ora le immagini della libreria', 'Immagini della libreria',
              "Sostituita con un'immagine adatta della stessa cartella", "Forma errata, nella cartella non c'è nulla di adatto",
              'Tutte le immagini hanno la forma giusta.', "Sostituite con un'immagine adatta: %d"),
    'ja_jp': ('形の合わないアートを自動修正', 'ライブラリのアートを今すぐ確認', 'ライブラリのアート',
              '同じフォルダーの合う画像に置き換えました', '形が合わず、フォルダーに合う画像がありません',
              'すべての画像の形が正しいです。', '合う画像に置き換えました: %d'),
    'ko_kr': ('모양이 맞지 않는 아트 자동 수정', '지금 라이브러리 아트 확인', '라이브러리 아트',
              '같은 폴더의 맞는 그림으로 바꿈', '모양이 맞지 않음, 폴더에 맞는 그림 없음',
              '모든 그림의 모양이 맞습니다.', '맞는 그림으로 바꿈: %d'),
    'nb_no': ('Rett bilder med feil form', 'Sjekk bibliotekets bilder nå', 'Bibliotekets bilder',
              'Erstattet med et passende bilde fra samme mappe', 'Feil form, ingenting i mappen passer',
              'Alle bilder har riktig form.', 'Erstattet med et passende bilde: %d'),
    'nl_nl': ('Afbeeldingen met foute vorm herstellen', 'Bibliotheekafbeeldingen nu controleren',
              'Bibliotheekafbeeldingen', 'Vervangen door een passende afbeelding uit dezelfde map',
              'Verkeerde vorm, niets in de map past', 'Alle afbeeldingen hebben de juiste vorm.',
              'Vervangen door een passende afbeelding: %d'),
    'pl_pl': ('Poprawiaj obrazy o złym kształcie', 'Sprawdź teraz obrazy biblioteki', 'Obrazy biblioteki',
              'Zastąpiono pasującym obrazem z tego samego folderu', 'Zły kształt, nic w folderze nie pasuje',
              'Wszystkie obrazy mają właściwy kształt.', 'Zastąpiono pasującym obrazem: %d'),
    'pt_br': ('Corrigir imagens com formato errado', 'Verificar agora as imagens da biblioteca',
              'Imagens da biblioteca', 'Substituída por uma imagem adequada da mesma pasta', 'Formato errado, nada na pasta serve',
              'Todas as imagens têm o formato certo.', 'Substituídas por uma imagem adequada: %d'),
    'pt_pt': ('Corrigir imagens com formato errado', 'Verificar agora as imagens da biblioteca',
              'Imagens da biblioteca', 'Substituída por uma imagem adequada da mesma pasta', 'Formato errado, nada na pasta serve',
              'Todas as imagens têm o formato certo.', 'Substituídas por uma imagem adequada: %d'),
    'ru_ru': ('Исправлять изображения неправильной формы', 'Проверить изображения медиатеки сейчас',
              'Изображения медиатеки', 'Заменено подходящим изображением из той же папки',
              'Неправильная форма, в папке нет подходящего', 'Все изображения правильной формы.',
              'Заменено подходящим изображением: %d'),
    'sv_se': ('Rätta bilder med fel form', 'Kontrollera bibliotekets bilder nu', 'Bibliotekets bilder',
              'Ersatt med en passande bild från samma mapp', 'Fel form, inget i mappen passar',
              'Alla bilder har rätt form.', 'Ersatt med en passande bild: %d'),
    'tr_tr': ('Yanlış biçimli görselleri düzelt', 'Kütüphane görsellerini şimdi denetle',
              'Kütüphane görselleri', 'Aynı klasörden uygun bir görselle değiştirildi', 'Yanlış biçim, klasörde uygun görsel yok',
              'Tüm görsellerin biçimi doğru.', 'Uygun bir görselle değiştirildi: %d'),
    'uk_ua': ('Виправляти зображення неправильної форми', 'Перевірити зображення медіатеки зараз',
              'Зображення медіатеки', 'Замінено відповідним зображенням з тієї ж теки',
              'Неправильна форма, у теці немає відповідного', 'Усі зображення мають правильну форму.',
              'Замінено відповідним зображенням: %d'),
    'zh_cn': ('自动修正形状不对的图片', '立即检查媒体库图片', '媒体库图片', '已换成同一文件夹中合适的图片',
              '形状不对，文件夹中没有合适的图片', '所有图片的形状都正确。', '已换成合适的图片：%d'),
    'zh_tw': ('自動修正形狀不對的圖片', '立即檢查媒體櫃圖片', '媒體櫃圖片', '已換成同一資料夾中合適的圖片',
              '形狀不對，資料夾中沒有合適的圖片', '所有圖片的形狀都正確。', '已換成合適的圖片：%d'),
}
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32441"' in t:
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
print('strings 32441-32447 added in %d languages' % done)
