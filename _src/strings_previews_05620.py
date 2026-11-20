# -*- coding: utf-8 -*-
"""0.56.20 strings for the settings preview cards' option table: Tint (32626), Picture (32627) and blurred
(32628), every language. Safe to run again (an id already there is left alone)."""
import io
import os

S = {
    'en_gb': ('Tint', 'Picture', 'blurred'),
    'cs_cz': ('Tónování', 'Obraz', 'rozmazaný'),
    'da_dk': ('Toning', 'Billede', 'sløret'),
    'de_de': ('Tönung', 'Bild', 'unscharf'),
    'el_gr': ('Απόχρωση', 'Εικόνα', 'θολή'),
    'es_es': ('Tinte', 'Imagen', 'difuminada'),
    'fi_fi': ('Sävy', 'Kuva', 'sumea'),
    'fr_fr': ('Teinte', 'Image', 'floutée'),
    'hu_hu': ('Színezés', 'Kép', 'elmosott'),
    'it_it': ('Tinta', 'Immagine', 'sfocata'),
    'ja_jp': ('色合い', '画像', 'ぼかし'),
    'ko_kr': ('색조', '그림', '흐림'),
    'nb_no': ('Toning', 'Bilde', 'uskarpt'),
    'nl_nl': ('Tint', 'Beeld', 'vervaagd'),
    'pl_pl': ('Odcień', 'Obraz', 'rozmyty'),
    'pt_br': ('Tom', 'Imagem', 'desfocada'),
    'pt_pt': ('Tom', 'Imagem', 'desfocada'),
    'ru_ru': ('Оттенок', 'Картинка', 'размыта'),
    'sv_se': ('Toning', 'Bild', 'suddig'),
    'tr_tr': ('Ton', 'Resim', 'bulanık'),
    'uk_ua': ('Відтінок', 'Зображення', 'розмите'),
    'zh_cn': ('色调', '画面', '模糊'),
    'zh_tw': ('色調', '畫面', '模糊'),
}
EN = S['en_gb']


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    for folder in sorted(os.listdir('language')):
        lang = folder.replace('resource.language.', '')
        p = os.path.join('language', folder, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        tr = S.get(lang)
        assert tr, lang
        add = ''
        for sid, en, local in ((32626, EN[0], tr[0]), (32627, EN[1], tr[1]), (32628, EN[2], tr[2])):
            if 'msgctxt "#%d"' % sid in t:
                continue
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), '' if lang == 'en_gb' else esc(local))
        if add:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)
    print('ok', len(os.listdir('language')))


if __name__ == '__main__':
    main()
