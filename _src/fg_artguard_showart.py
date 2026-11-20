# -*- coding: utf-8 -*-
"""0.39.14 string 32450 for the library art check's summary: seasons whose art has the wrong shape and nothing in the
folder fits are left empty: the skin shows the show's own picture there, and a media manager fills an empty slot later. All languages. Run from the skin
folder."""
import io
import os

EN = "Left empty, the skin shows the show's own picture"
TR = {'cs_cz': 'Ponecháno prázdné, skin ukáže obrázek seriálu', 'da_dk': 'Efterladt tom, skinnet viser seriens eget billede', 'de_de': 'Leer gelassen, der Skin zeigt das Bild der Serie', 'el_gr': 'Έμεινε κενό, το skin δείχνει την εικόνα της σειράς', 'es_es': 'Se deja vacío, la piel muestra la imagen de la serie', 'fi_fi': 'Jätetty tyhjäksi, teema näyttää sarjan oman kuvan', 'fr_fr': "Laissé vide, le skin affiche l'image de la série", 'hu_hu': 'Üresen hagyva, a felület a sorozat saját képét mutatja', 'it_it': "Lasciato vuoto, la skin mostra l'immagine della serie", 'ja_jp': '空欄のまま。スキンが番組自体の画像を表示します', 'ko_kr': '비워 둠, 스킨이 프로그램 자체의 그림을 보여 줌', 'nb_no': 'Latt tom, skallet viser seriens eget bilde', 'nl_nl': 'Leeg gelaten, de skin toont de eigen afbeelding van de serie', 'pl_pl': 'Pozostawiono puste, skórka pokazuje obraz serialu', 'pt_br': 'Deixado vazio, a skin mostra a imagem da série', 'pt_pt': 'Deixado vazio, o skin mostra a imagem da série', 'ru_ru': 'Оставлено пустым, обложка покажет изображение сериала', 'sv_se': 'Lämnad tom, skalet visar seriens egen bild', 'tr_tr': 'Boş bırakıldı, tema dizinin kendi görselini gösterir', 'uk_ua': 'Залишено порожнім, оболонка покаже зображення серіалу', 'zh_cn': '留空，皮肤会显示剧集本身的图片', 'zh_tw': '留空，外觀會顯示影集本身的圖片'}
n = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32450"' in t:
        continue
    msgstr = '' if lang == 'en_gb' else TR[lang]
    t = t.rstrip('\n') + '\n\nmsgctxt "#32450"\nmsgid "%s"\nmsgstr "%s"\n' % (EN, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    n += 1
print('32450 added in %d languages' % n)
