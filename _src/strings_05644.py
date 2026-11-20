# -*- coding: utf-8 -*-
"""0.56.44 string 32747, all 23 languages: the help line of Aeon Glass's Panel blur (Skin settings > Theme & style,
row 9518). Repeatable: an id that is there is written again."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
IDS = [32747]
EN = ['How strongly the picture behind the menus and dialogs is blurred. Off: sharp, as before.']
T = {
    'cs_cz': ['Jak silně se rozmaže obrázek za nabídkami a dialogy. Vypnuto: ostrý, jako dosud.'],
    'da_dk': ['Hvor kraftigt billedet bag menuer og dialoger sløres. Fra: skarpt, som hidtil.'],
    'de_de': ['Wie stark das Bild hinter Menüs und Dialogen verschwimmt. Aus: scharf, wie bisher.'],
    'el_gr': ['Πόσο έντονα θολώνει η εικόνα πίσω από τα μενού και τους διαλόγους. Ανενεργό: καθαρή, όπως πριν.'],
    'es_es': ['Cuánto se desenfoca la imagen detrás de los menús y diálogos. Desactivado: nítida, como hasta ahora.'],
    'fi_fi': ['Kuinka voimakkaasti valikoiden ja valintaikkunoiden takana oleva kuva sumennetaan. Pois: terävä, kuten ennen.'],
    'fr_fr': ['Intensité du flou de l\'image derrière les menus et les dialogues. Désactivé : nette, comme avant.'],
    'hu_hu': ['Mennyire legyen elmosva a menük és párbeszédablakok mögötti kép. Ki: éles, mint eddig.'],
    'it_it': ['Quanto viene sfocata l\'immagine dietro menu e finestre di dialogo. Disattivato: nitida, come prima.'],
    'ja_jp': ['メニューやダイアログの背後の画像をどれだけぼかすか。オフ：これまでどおりくっきり。'],
    'ko_kr': ['메뉴와 대화 상자 뒤의 그림을 얼마나 흐리게 할지. 끔: 지금처럼 선명하게.'],
    'nb_no': ['Hvor kraftig bildet bak menyer og dialoger gjøres uskarpt. Av: skarpt, som før.'],
    'nl_nl': ['Hoe sterk de afbeelding achter menu\'s en dialogen vervaagt. Uit: scherp, zoals voorheen.'],
    'pl_pl': ['Jak mocno rozmywany jest obraz za menu i oknami dialogowymi. Wyłączone: ostry, jak dotąd.'],
    'pt_br': ['Quanto a imagem atrás dos menus e diálogos fica desfocada. Desligado: nítida, como antes.'],
    'pt_pt': ['Quanto a imagem por trás dos menus e diálogos fica desfocada. Desligado: nítida, como antes.'],
    'ru_ru': ['Насколько сильно размывается изображение за меню и диалогами. Выкл.: чёткое, как раньше.'],
    'sv_se': ['Hur kraftigt bilden bakom menyer och dialoger görs suddig. Av: skarp, som tidigare.'],
    'tr_tr': ['Menülerin ve iletişim kutularının arkasındaki resmin ne kadar bulanıklaşacağı. Kapalı: eskisi gibi net.'],
    'uk_ua': ['Наскільки сильно розмивається зображення за меню та діалогами. Вимк.: чітке, як раніше.'],
    'zh_cn': ['菜单和对话框背后的图片模糊程度。关闭：与以前一样清晰。'],
    'zh_tw': ['選單與對話框背後圖片的模糊程度。關閉：與以前一樣清晰。'],
}


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    for code, row in T.items():
        assert len(row) == len(IDS), (code, len(row))
    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        code = d.replace('resource.language.', '')
        for i, sid in enumerate(IDS):
            tr = '' if code == 'en_gb' else esc(T[code][i])
            m = re.search(r'(msgctxt "#%d"\nmsgid ")(.*)("\nmsgstr ")(.*)(")' % sid, t)
            if m:
                t = t[:m.start()] + m.group(1) + esc(EN[i]) + m.group(3) + tr + m.group(5) + t[m.end():]
            else:
                t = t.rstrip('\n') + '\n\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(EN[i]), tr)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('ok', len(IDS), 'strings in', len(os.listdir(L)), 'languages')


if __name__ == '__main__':
    main()
