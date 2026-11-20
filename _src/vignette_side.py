# -*- coding: utf-8 -*-
"""0.56.0 Home vignette shape (Skin settings > Backgrounds > Vignette shape: Round | Side, row 9765,
Skin.HasSetting(aeon.vignette.side)).

The user (2026-11-15): "we don't have a vignette which looks as good as the one you had in your font mockups". The
font mockups (skin.glass/mockups/fonts) darken the screen from the left: linear-gradient(90deg, #0a0b0e 30%,
rgba(10,11,14,.8) 58%, rgba(10,11,14,.25)). Side is that gradient as a picture (media/common/aeon_vignette_side.png);
Round is the vignette so far (default). The row above (Home vignette: Off / Light / Medium / Strong) sets how strong
either shape is: Strong gives the mockups' look exactly. (A fifth choice in the Home vignette row did not fit: the long
translations of the row's name would run into the choices.)
Strings 32599 Side, 32600 Vignette shape, 32601 Round, 32602 the help line, all languages.
Run from the skin folder; safe to run again (it also undoes the five-choice row of the first try)."""
import io
import os
import re

from PIL import Image, ImageFont

SP = os.path.join('1080i', 'SkinSettings.xml')
TR = {
    32599: ('Side', {'cs_cz': u'Boční', 'da_dk': u'Side', 'de_de': u'Seitlich', 'el_gr': u'Πλάγια', 'es_es': u'Lateral', 'fi_fi': u'Sivu',
                     'fr_fr': u'Latéral', 'hu_hu': u'Oldalsó', 'it_it': u'Laterale', 'ja_jp': u'サイド', 'ko_kr': u'측면', 'nb_no': u'Side',
                     'nl_nl': u'Zijkant', 'pl_pl': u'Boczna', 'pt_br': u'Lateral', 'pt_pt': u'Lateral', 'ru_ru': u'Боковая', 'sv_se': u'Sida',
                     'tr_tr': u'Yan', 'uk_ua': u'Бічна', 'zh_cn': u'侧边', 'zh_tw': u'側邊'}),
    32600: ('Vignette shape', {'cs_cz': u'Tvar vinětace', 'da_dk': u'Vignettens form', 'de_de': u'Vignettenform', 'el_gr': u'Σχήμα βινιέτας',
                               'es_es': u'Forma de la viñeta', 'fi_fi': u'Vinjetin muoto', 'fr_fr': u'Forme du vignettage', 'hu_hu': u'Vignetta alakja',
                               'it_it': u'Forma della vignettatura', 'ja_jp': u'ビネットの形', 'ko_kr': u'비네트 모양', 'nb_no': u'Vignettens form',
                               'nl_nl': u'Vorm van vignet', 'pl_pl': u'Kształt winiety', 'pt_br': u'Forma da vinheta', 'pt_pt': u'Forma da vinheta',
                               'ru_ru': u'Форма виньетки', 'sv_se': u'Vinjettens form', 'tr_tr': u'Vinyet şekli', 'uk_ua': u'Форма віньєтки',
                               'zh_cn': u'暗角形状', 'zh_tw': u'暗角形狀'}),
    32601: ('Round', {'cs_cz': u'Kulatá', 'da_dk': u'Rund', 'de_de': u'Rund', 'el_gr': u'Στρογγυλή', 'es_es': u'Redonda', 'fi_fi': u'Pyöreä',
                      'fr_fr': u'Rond', 'hu_hu': u'Kerek', 'it_it': u'Rotonda', 'ja_jp': u'円形', 'ko_kr': u'원형', 'nb_no': u'Rund', 'nl_nl': u'Rond',
                      'pl_pl': u'Okrągła', 'pt_br': u'Redonda', 'pt_pt': u'Redonda', 'ru_ru': u'Круглая', 'sv_se': u'Rund', 'tr_tr': u'Yuvarlak',
                      'uk_ua': u'Кругла', 'zh_cn': u'圆形', 'zh_tw': u'圓形'}),
    32602: ('Round darkens the edges all round. Side darkens the screen from the left and fades out to the right, under the Home text. The row above sets how strong it is.',
            {'cs_cz': u'Kulatá ztmaví okraje dokola. Boční ztmaví obrazovku zleva a doprava slábne, pod textem na domovské obrazovce. Sílu nastavuje řádek nad tímto.',
             'da_dk': u'Rund gør kanterne mørkere hele vejen rundt. Side gør skærmen mørk fra venstre og toner ud mod højre under teksten på startskærmen. Rækken ovenfor bestemmer styrken.',
             'de_de': u'Rund dunkelt die Ränder rundum ab. Seitlich dunkelt den Bildschirm von links ab und läuft nach rechts aus, unter dem Text der Startseite. Die Zeile darüber legt die Stärke fest.',
             'el_gr': u'Η στρογγυλή σκουραίνει τις άκρες γύρω-γύρω. Η πλάγια σκουραίνει την οθόνη από αριστερά και σβήνει προς τα δεξιά, κάτω από το κείμενο της αρχικής οθόνης. Η ένταση ορίζεται στην παραπάνω γραμμή.',
             'es_es': u'Redonda oscurece los bordes alrededor. Lateral oscurece la pantalla desde la izquierda y se desvanece hacia la derecha, bajo el texto de Inicio. La fila de arriba fija la intensidad.',
             'fi_fi': u'Pyöreä tummentaa reunat ympäriinsä. Sivu tummentaa näytön vasemmalta ja häivyttää oikealle, aloitusnäytön tekstin alle. Voimakkuus asetetaan yllä olevalla rivillä.',
             'fr_fr': u"Rond assombrit les bords tout autour. Latéral assombrit l'écran depuis la gauche et s'estompe vers la droite, sous le texte de l'accueil. La ligne du dessus règle l'intensité.",
             'hu_hu': u'A kerek körben sötétíti a széleket. Az oldalsó balról sötétíti a képernyőt, és jobbra halványul, a kezdőképernyő szövege alatt. Az erősséget a fenti sor állítja.',
             'it_it': u"Rotonda scurisce i bordi tutt'intorno. Laterale scurisce lo schermo da sinistra e sfuma verso destra, sotto il testo della Home. L'intensità si imposta nella riga sopra.",
             'ja_jp': u'円形は周囲の縁を暗くします。サイドは画面を左から暗くし、右へ向かって薄くなります（ホームの文字の下）。強さは上の行で設定します。',
             'ko_kr': u'원형은 가장자리를 둥글게 어둡게 합니다. 측면은 화면을 왼쪽부터 어둡게 하고 오른쪽으로 갈수록 옅어집니다(홈 텍스트 아래). 강도는 위 행에서 설정합니다.',
             'nb_no': u'Rund gjør kantene mørkere hele veien rundt. Side gjør skjermen mørk fra venstre og toner ut mot høyre, under teksten på startskjermen. Raden over bestemmer styrken.',
             'nl_nl': u'Rond maakt de randen rondom donkerder. Zijkant maakt het scherm vanaf links donker en vervaagt naar rechts, onder de tekst op het startscherm. De rij erboven bepaalt hoe sterk.',
             'pl_pl': u'Okrągła przyciemnia krawędzie dookoła. Boczna przyciemnia ekran od lewej i zanika w prawo, pod tekstem ekranu głównego. Siłę ustawia wiersz powyżej.',
             'pt_br': u'Redonda escurece as bordas ao redor. Lateral escurece a tela a partir da esquerda e some para a direita, sob o texto do Início. A linha acima define a intensidade.',
             'pt_pt': u'Redonda escurece as margens à volta. Lateral escurece o ecrã a partir da esquerda e desvanece para a direita, sob o texto do Início. A linha acima define a intensidade.',
             'ru_ru': u'Круглая затемняет края по кругу. Боковая затемняет экран слева и сходит на нет вправо, под текстом главного экрана. Силу задаёт строка выше.',
             'sv_se': u'Rund gör kanterna mörkare runt om. Sida gör skärmen mörk från vänster och tonar ut mot höger, under texten på startskärmen. Raden ovanför styr styrkan.',
             'tr_tr': u'Yuvarlak kenarları çepeçevre karartır. Yan, ekranı soldan karartır ve sağa doğru kaybolur; ana ekran yazısının altında. Gücü üstteki satır belirler.',
             'uk_ua': u'Кругла затемнює краї довкола. Бічна затемнює екран зліва й згасає праворуч, під текстом головного екрана. Силу задає рядок вище.',
             'zh_cn': u'圆形会让四周边缘变暗。侧边从左侧压暗画面并向右渐隐，位于主页文字下方。强度由上一行设置。',
             'zh_tw': u'圓形會讓四周邊緣變暗。側邊從左側壓暗畫面並向右漸隱，位於主頁文字下方。強度由上一列設定。'}),
}
LANGS = sorted(set(k for _, d in TR.values() for k in d) | {'en_gb'})


def strings():
    for lang in LANGS:
        p = os.path.join('language', 'resource.language.' + lang, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        for sid, (en, tr) in sorted(TR.items()):
            ms = '' if lang == 'en_gb' else tr[lang].replace('"', '\\"')
            entry = u'msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, en, ms)
            m = re.search(r'msgctxt "#%d"\nmsgid "[^\n]*"\nmsgstr "[^\n]*"\n' % sid, t)
            t = t[:m.start()] + entry + t[m.end():] if m else t.rstrip('\n') + '\n\n' + entry
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('strings %s in %d languages' % (sorted(TR), len(LANGS)))


def texture():
    p = os.path.join('media', 'common', 'aeon_vignette_side.png')
    W, H = 960, 16
    im = Image.new('RGBA', (W, H))
    px = im.load()
    for x in range(W):
        f = x / float(W - 1)
        a = 1.0 if f <= 0.30 else (1.0 - 0.2 * (f - 0.30) / 0.28 if f <= 0.58 else 0.8 - 0.55 * (f - 0.58) / 0.42)
        for y in range(H):
            px[x, y] = (10, 11, 14, int(round(a * 255)))
    im.save(p, optimize=True)


def group_of(t, cid):
    i = t.find('<control type="button" id="%d">' % cid)
    g = t.rfind('<control type="group">', 0, i)
    depth = 0
    for m in re.finditer(r'<control[ >]|</control>', t[g:]):
        depth += -1 if m.group(0) == '</control>' else 1
        if depth == 0:
            return g, g + m.end()


def undo_five(t):
    """the first try put Side into the Home vignette row as a fifth choice: take it out again"""
    g, e = group_of(t, 9733)
    c = t[g:e]
    if '$ADDON[skin.aeon.fuse 32599]' not in c:
        return t
    w5 = int(re.search(r'<left>(\d+)</left><top>13</top><width>(\d+)</width>', c).group(1))
    w5 = 394 - w5
    c = re.sub(r'\t*<control type="(?:image|label)"><left>%d</left><top>13</top><width>%d</width>.*?</control>\n' % (854 - w5, w5), '', c)
    c = c.replace('<left>%d</left><top>13</top><width>%d</width>' % (394 - w5, 466 + w5), '<left>394</left><top>13</top><width>466</width>')
    for x in (738, 606, 502, 398):                # right to left, so a piece is never moved twice
        c = c.replace('<left>%d</left><top>13</top>' % (x - w5), '<left>%d</left><top>13</top>' % x)
    c = c.replace('Skin.SetString(aeon.vignette,e)</onclick>\n\t\t\t\t\t<onclick condition="String.IsEqual(Skin.String(aeon.vignette),e)">Skin.SetString(aeon.vignette,a)',
                  'Skin.SetString(aeon.vignette,a)')
    assert '32599' not in c and 'vignette),e)' not in c, 'undo'
    print('row 9733: back to four choices')
    return t[:g] + c + t[e:]


def seg_widths():
    fb = ImageFont.truetype(os.path.join('fonts', 'Figtree-Bold.ttf'), 22)
    w = []
    for sid in (32601, 32599):
        words = [TR[sid][0]] + list(TR[sid][1].values())
        w.append(max(150, max(int(fb.getlength(x)) for x in words) + 44))
    return w


def add_row(t):
    if 'id="9765"' in t:
        print('row 9765 already there')
        return t
    # the template: Appearance > Home menu position (two choices, a skin bool)
    g, e = group_of(t, 9746)
    c = t[g:e]
    w1, w2 = seg_widths()
    x2 = 854 - w2
    x1 = x2 - w1
    rep = [('id="9746"', 'id="9765"'), ('value="9746"', 'value="9765"'), ('Control.HasFocus(9746)', 'Control.HasFocus(9765)'),
           ('$LOCALIZE[31856]', '$ADDON[skin.aeon.fuse 32600]'), ('aeon/icons/home.png', 'aeon/icons/vignette.png'),
           ('<onup>9745</onup>', '<onup>9733</onup>'), ('<ondown>9747</ondown>', '<ondown>9734</ondown>'),
           ('<onback>9600</onback>', '<onback>9569</onback>'), ('<onleft>SetFocus(9600)</onleft>', '<onleft>SetFocus(9569)</onleft>'),
           ('Skin.ToggleSetting(aeon.lowmenu)', 'Skin.ToggleSetting(aeon.vignette.side)'),
           ('Skin.HasSetting(aeon.lowmenu)', 'Skin.HasSetting(aeon.vignette.side)'),
           ('$LOCALIZE[31857]', '$ADDON[skin.aeon.fuse 32601]'), ('$LOCALIZE[31858]', '$ADDON[skin.aeon.fuse 32599]'),
           ('<left>484</left><top>13</top><width>376</width>', '<left>%d</left><top>13</top><width>%d</width>' % (x1 - 4, 860 - x1 + 4)),
           ('<left>488</left><top>13</top><width>180</width>', '<left>%d</left><top>13</top><width>%d</width>' % (x1, w1)),
           ('<left>668</left><top>13</top><width>186</width>', '<left>%d</left><top>13</top><width>%d</width>' % (x2, w2))]
    for a, b in rep:
        assert a in c, a
        c = c.replace(a, b)
    # the group's place and entrance: those of the row it goes before (9734); then the rows below move down a row
    g4, e4 = group_of(t, 9734)
    head4 = t[g4:t.find('<include content="Dlg_SkinRowChrome">', g4)]
    c = head4 + c[c.find('<include content="Dlg_SkinRowChrome">'):]
    page_s = t.rfind('<visible>String.IsEqual(Window(Home).Property(aeon.skincat),backgrounds)</visible>', 0, g4)
    page_e = t.find('<visible>String.IsEqual(Window(Home).Property(aeon.skincat),widgets)</visible>', g4)
    seg = t[g4:page_e]
    for top in (681, 611, 541, 471):
        seg = seg.replace('<control type="group">\n\t\t\t\t<top>%d</top>' % top, '<control type="group">\n\t\t\t\t<top>%d</top>' % (top + 70))
    t = t[:g4] + c + '\n\t\t\t' + seg + t[page_e:]
    # navigation: Home vignette > Vignette shape > Weather box on the screensaver
    g3, e3 = group_of(t, 9733)
    r3 = t[g3:e3].replace('<ondown>9734</ondown>', '<ondown>9765</ondown>', 1)
    t = t[:g3] + r3 + t[e3:]
    g5, e5 = group_of(t, 9734)
    r5 = t[g5:e5].replace('<onup>9733</onup>', '<onup>9765</onup>', 1)
    t = t[:g5] + r5 + t[e5:]
    print('row 9765 added (%d + %d px)' % (w1, w2))
    return t


def bars(t):
    """every settings row has its own focus bar group (left -119, at the row's top, shown while the row has the focus):
    the new row needs one, and the bars of the rows that moved down must move with them"""
    def row_top(cid):
        g, _ = group_of(t, cid)
        return int(re.search(r'<top>(\d+)</top>', t[g:g + 200]).group(1))
    lit = '<control type="group">\n\t\t\t\t<left>-119</left>\n\t\t\t\t<top>%d</top>\n\t\t\t\t<visible>Control.HasFocus(%d)</visible>'

    def find(cid):
        return re.search(r'<control type="group">\n\t\t\t\t<left>-119</left>\n\t\t\t\t<top>(\d+)</top>\n\t\t\t\t'
                         r'<visible>Control\.HasFocus\(%d\)(?: \+ [^<]*)?</visible>' % cid, t)

    for cid in (9734, 9735, 9736, 9737, 9764):
        m = find(cid)
        assert m, cid
        top = row_top(cid)
        if int(m.group(1)) != top:
            t = t[:m.start(1)] + str(top) + t[m.end(1):]
    if not find(9765):
        m = find(9733)
        s, e = m.start(), m.start()
        depth = 0
        for mm in re.finditer(r'<control[ >]|</control>', t[s:]):
            depth += -1 if mm.group(0) == '</control>' else 1
            if depth == 0:
                e = s + mm.end()
                break
        bar = t[s:e].replace('Control.HasFocus(9733)', 'Control.HasFocus(9765)')
        bar = re.sub(r'<top>\d+</top>', '<top>%d</top>' % row_top(9765), bar, count=1)
        g, _ = group_of(t, 9765)
        t = t[:g] + bar + '\n\t\t\t' + t[g:]
    print('focus bars:', [(c, int(find(c).group(1)), row_top(c)) for c in (9733, 9765, 9734, 9735, 9736, 9737, 9764)])
    return t


def help_line():
    p = os.path.join('1080i', 'Includes_Settings.xml')
    t = io.open(p, encoding='utf-8').read()
    if 'Control.HasFocus(9765)' in t:
        return
    old = '\t<variable name="Dlg_SkinHelp">\n'
    assert t.count(old) == 1
    t = t.replace(old, old + '\t\t<value condition="Control.HasFocus(9765)">$ADDON[skin.aeon.fuse 32602]</value>\n')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def home():
    p = os.path.join('1080i', 'Includes_Aeon_Home.xml')
    t = io.open(p, encoding='utf-8').read()
    t = re.sub(r'\n\t\t<!-- 0.56.0 Side \(e\).*?</control>', '', t, flags=re.S)        # the first try
    t = t.replace('<visible>!String.IsEqual(Skin.String(aeon.vignette),a) + !String.IsEqual(Skin.String(aeon.vignette),e)</visible>',
                  '<visible>!String.IsEqual(Skin.String(aeon.vignette),a)</visible>')
    if 'aeon.vignette.side' in t:
        print('Home already draws both shapes')
        return
    old = ('<texture colordiffuse="$VAR[Aeon_VignetteCol]">common/aeon_vignette.png</texture>\n'
           '\t\t\t<visible>!String.IsEqual(Skin.String(aeon.vignette),a)</visible>\n\t\t</control>')
    assert t.count(old) == 1
    new = ('<texture colordiffuse="$VAR[Aeon_VignetteCol]">common/aeon_vignette.png</texture>\n'
           '\t\t\t<visible>!String.IsEqual(Skin.String(aeon.vignette),a) + !Skin.HasSetting(aeon.vignette.side)</visible>\n\t\t</control>\n'
           '\t\t<!-- 0.56.0 Vignette shape Side: dark from the left like the font mockups, as strong as Home vignette says (_src/vignette_side.py) -->\n'
           '\t\t<control type="image">\n\t\t\t<left>0</left><top>0</top><width>1920</width><height>1080</height>\n'
           '\t\t\t<texture colordiffuse="$VAR[Aeon_VignetteCol]">common/aeon_vignette_side.png</texture>\n'
           '\t\t\t<visible>!String.IsEqual(Skin.String(aeon.vignette),a) + Skin.HasSetting(aeon.vignette.side)</visible>\n\t\t</control>')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
    print('Home draws Round or Side')


def spotlight_side():
    """the Home spotlights (wraplists 9421 ... 9424, item layout Aeon_H_Spot2Item) draw their picture full-screen over
    the Home darkening layers, then their own scrims, logo and plot. So Side is also drawn inside the spotlight layout,
    after its scrims and before its logo and text: the picture darkens, the text does not. (A first try drew Side over
    all the spotlights: that darkened their logo and plot too; it is put back next to Round here.) Round stays as it
    was, so the default look does not change."""
    p = os.path.join('1080i', 'Includes_Aeon_Home.xml')
    t = io.open(p, encoding='utf-8').read()
    m = re.search(r'\t\t<!-- 0\.56\.0 Vignette shape Side:[^\n]*over the spotlight pictures[^\n]*-->\n.*?</control>\n', t, re.S)
    if m:
        block = m.group(0).replace('over the spotlight pictures, ', '')
        t = t[:m.start()] + t[m.end():]
        k = t.find('<texture colordiffuse="$VAR[Aeon_VignetteCol]">common/aeon_vignette.png</texture>')
        k = t.find('</control>\n', k) + len('</control>\n')
        t = t[:k] + block + t[k:]
        print('Side back next to Round')
    i = t.find('<include name="Aeon_H_Spot2Item">')
    j = t.find('<texture background="true">$VAR[Aeon_SP2Logo]</texture>', i)
    if 'aeon_vignette_side' not in t[i:j]:
        old = '<texture colordiffuse="e0000000">aeon/osd_scrim_bottom.png</texture>\n\t\t</control>\n'
        k = t.find(old, i)
        assert 0 < k < j, 'spotlight scrim'
        k += len(old)
        side = ('\t\t<!-- 0.56.0 Vignette shape Side over the spotlight picture, under its logo and text (_src/vignette_side.py) -->\n'
                '\t\t<control type="image">\n\t\t\t<width>1920</width><height>1080</height>\n'
                '\t\t\t<texture colordiffuse="$VAR[Aeon_VignetteCol]">common/aeon_vignette_side.png</texture>\n'
                '\t\t\t<visible>!String.IsEqual(Skin.String(aeon.vignette),a) + Skin.HasSetting(aeon.vignette.side)</visible>\n\t\t</control>\n')
        t = t[:k] + side + t[k:]
        print('Side in the spotlight layout')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

if __name__ == '__main__':
    strings()
    texture()
    t = io.open(SP, encoding='utf-8').read()
    t = bars(add_row(undo_five(t)))
    io.open(SP, 'w', encoding='utf-8', newline='\n').write(t)
    help_line()
    home()
    spotlight_side()
