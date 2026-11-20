# -*- coding: utf-8 -*-
"""0.40.3 strings 32462-32465: Skin settings > Behaviour > Skippy: skip button style (Aeon theme), all languages."""
import io
import os

EN = {
    32462: 'Skippy: skip button style',
    32463: 'Box pair',
    32464: 'Clock dock',
    32465: 'Aeon theme: a palette tile and a label box at the bottom right (above the player controls when they are open), or a row at the top right that ends in the clock box.',
}
TR = {
    'cs_cz': ('Skippy: styl tlačítka přeskočení', 'Dvojice boxů', 'U hodin', 'Motiv Aeon: barevná dlaždice a popisek vpravo dole (nad ovládáním přehrávače, když je otevřené), nebo řada vpravo nahoře zakončená boxem s hodinami.'),
    'da_dk': ('Skippy: stil for spring over-knap', 'Bokspar', 'Ved uret', 'Aeon-tema: en farvet flise og en tekstboks nederst til højre (over afspillerens knapper, når de er åbne), eller en række øverst til højre, der ender i urboksen.'),
    'de_de': ('Skippy: Stil der Überspringen-Taste', 'Boxpaar', 'An der Uhr', 'Aeon-Thema: eine Farbkachel und ein Textfeld unten rechts (über der Player-Steuerung, wenn sie offen ist) oder eine Reihe oben rechts, die an der Uhrbox endet.'),
    'el_gr': ('Skippy: στυλ κουμπιού παράλειψης', 'Ζεύγος πλαισίων', 'Στο ρολόι', 'Θέμα Aeon: ένα χρωματιστό πλακίδιο και ένα πλαίσιο κειμένου κάτω δεξιά (πάνω από τα χειριστήρια όταν είναι ανοιχτά), ή μια σειρά πάνω δεξιά που τελειώνει στο πλαίσιο του ρολογιού.'),
    'es_es': ('Skippy: estilo del botón de saltar', 'Par de cajas', 'Junto al reloj', 'Tema Aeon: una ficha de color y una caja de texto abajo a la derecha (sobre los controles del reproductor cuando están abiertos), o una fila arriba a la derecha que acaba en la caja del reloj.'),
    'fi_fi': ('Skippy: ohituspainikkeen tyyli', 'Laatikkopari', 'Kellon vieressä', 'Aeon-teema: värilaatta ja tekstilaatikko oikeassa alakulmassa (soittimen säätimien yläpuolella, kun ne ovat auki), tai rivi oikeassa yläkulmassa, joka päättyy kellolaatikkoon.'),
    'fr_fr': ('Skippy : style du bouton Passer', 'Paire de blocs', 'Contre l\'horloge', 'Thème Aeon : une tuile de couleur et un bloc de texte en bas à droite (au-dessus des commandes du lecteur quand elles sont ouvertes), ou une rangée en haut à droite qui finit sur le bloc de l\'horloge.'),
    'hu_hu': ('Skippy: átugrás gomb stílusa', 'Dobozpár', 'Az óránál', 'Aeon téma: színes csempe és szövegdoboz jobbra lent (a lejátszó vezérlői fölött, ha nyitva vannak), vagy egy sor jobbra fent, amely az óra dobozában végződik.'),
    'it_it': ('Skippy: stile del pulsante Salta', 'Coppia di riquadri', 'Accanto all\'orologio', 'Tema Aeon: una tessera colorata e un riquadro di testo in basso a destra (sopra i controlli del lettore quando sono aperti), o una riga in alto a destra che finisce nel riquadro dell\'orologio.'),
    'ja_jp': ('Skippy: スキップボタンのスタイル', 'ボックスペア', '時計の横', 'Aeon テーマ: 右下にカラータイルと文字ボックス（プレーヤーの操作パネルが開いているときはその上）、または右上の時計ボックスにつながる一列。'),
    'ko_kr': ('Skippy: 건너뛰기 버튼 스타일', '상자 쌍', '시계 옆', 'Aeon 테마: 오른쪽 아래의 색 타일과 글자 상자(플레이어 컨트롤이 열려 있으면 그 위), 또는 오른쪽 위에서 시계 상자로 끝나는 한 줄.'),
    'nb_no': ('Skippy: stil for hopp over-knapp', 'Bokspar', 'Ved klokken', 'Aeon-tema: en farget flis og en tekstboks nede til høyre (over spillerens knapper når de er åpne), eller en rad oppe til høyre som ender i klokkeboksen.'),
    'nl_nl': ('Skippy: stijl van de overslaanknop', 'Vakkenpaar', 'Bij de klok', 'Aeon-thema: een gekleurde tegel en een tekstvak rechtsonder (boven de spelerknoppen als die open zijn), of een rij rechtsboven die eindigt in het klokvak.'),
    'pl_pl': ('Skippy: styl przycisku pomijania', 'Para pól', 'Przy zegarze', 'Motyw Aeon: kolorowy kafel i pole tekstu w prawym dolnym rogu (nad sterowaniem odtwarzacza, gdy jest otwarte) albo rząd w prawym górnym rogu kończący się polem zegara.'),
    'pt_br': ('Skippy: estilo do botão pular', 'Par de caixas', 'Junto ao relógio', 'Tema Aeon: um bloco colorido e uma caixa de texto no canto inferior direito (acima dos controles do player quando abertos), ou uma fileira no canto superior direito que termina na caixa do relógio.'),
    'pt_pt': ('Skippy: estilo do botão saltar', 'Par de caixas', 'Junto ao relógio', 'Tema Aeon: um bloco colorido e uma caixa de texto no canto inferior direito (acima dos controlos do leitor quando abertos), ou uma fila no canto superior direito que acaba na caixa do relógio.'),
    'ru_ru': ('Skippy: стиль кнопки пропуска', 'Пара блоков', 'У часов', 'Тема Aeon: цветная плитка и блок с текстом справа внизу (над управлением плеером, когда оно открыто) или ряд справа вверху, который заканчивается блоком часов.'),
    'sv_se': ('Skippy: stil för hoppa över-knapp', 'Ruta-par', 'Vid klockan', 'Aeon-tema: en färgad platta och en textruta nere till höger (ovanför spelarens knappar när de är öppna), eller en rad uppe till höger som slutar i klockrutan.'),
    'tr_tr': ('Skippy: atla düğmesi stili', 'Kutu çifti', 'Saatin yanında', 'Aeon teması: sağ altta renkli bir karo ve yazı kutusu (oynatıcı denetimleri açıkken onların üstünde) ya da sağ üstte saat kutusunda biten bir sıra.'),
    'uk_ua': ('Skippy: стиль кнопки пропуску', 'Пара блоків', 'Біля годинника', 'Тема Aeon: кольорова плитка й блок із текстом праворуч унизу (над керуванням плеєром, коли воно відкрите) або ряд праворуч угорі, що закінчується блоком годинника.'),
    'zh_cn': ('Skippy：跳过按钮样式', '方框组', '靠时钟', 'Aeon 主题：右下角的色块和文字框（播放器控件打开时在其上方），或右上角以时钟框结尾的一行。'),
    'zh_tw': ('Skippy：跳過按鈕樣式', '方框組', '靠時鐘', 'Aeon 主題：右下角的色塊和文字框（播放器控制項開啟時在其上方），或右上角以時鐘框結尾的一列。'),
}
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32462"' in t:
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
print('strings 32462-32465 added in %d languages' % done)
