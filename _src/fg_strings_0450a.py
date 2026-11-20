# -*- coding: utf-8 -*-
"""0.45.0 strings for Skin settings > Look > Material: 32547-32551. Run from the skin folder."""
import io
import os

EN = {
    32547: 'Frost',
    32548: 'Raised',
    32549: 'Clear',
    32550: 'Material',
    32551: "The glass of the panels. Frost: lighter, the picture's colours glow through, strong artwork shadows. Raised: the same with a lit rim and a deep shadow. Clear: thin glass, no blur. Today: the darker glass with a soft shadow.",
}
TR = {
    'cs_cz': ('Mráz', 'Vyvýšené', 'Čiré', 'Materiál', 'Sklo panelů. Mráz: světlejší, barvy obrázku prosvítají, výrazné stíny obrázků. Vyvýšené: totéž se světlým okrajem a hlubokým stínem. Čiré: tenké sklo bez rozmazání. Dnes: tmavší sklo s jemným stínem.'),
    'da_dk': ('Frost', 'Hævet', 'Klar', 'Materiale', 'Panelernes glas. Frost: lysere, billedets farver skinner igennem, kraftige skygger. Hævet: det samme med en lys kant og en dyb skygge. Klar: tyndt glas uden sløring. I dag: det mørkere glas med en blød skygge.'),
    'de_de': ('Frost', 'Erhaben', 'Klar', 'Material', 'Das Glas der Flächen. Frost: heller, die Farben des Bildes scheinen durch, kräftige Schatten. Erhaben: dasselbe mit hellem Rand und tiefem Schatten. Klar: dünnes Glas ohne Unschärfe. Heute: das dunklere Glas mit weichem Schatten.'),
    'el_gr': ('Παγωμένο', 'Ανυψωμένο', 'Διάφανο', 'Υλικό', 'Το γυαλί των πάνελ. Παγωμένο: πιο φωτεινό, τα χρώματα της εικόνας διακρίνονται, έντονες σκιές. Ανυψωμένο: το ίδιο με φωτεινό περίγραμμα και βαθιά σκιά. Διάφανο: λεπτό γυαλί χωρίς θόλωμα. Σήμερα: το σκουρότερο γυαλί με απαλή σκιά.'),
    'es_es': ('Escarcha', 'Elevado', 'Claro', 'Material', 'El cristal de los paneles. Escarcha: más claro, los colores de la imagen se transparentan, sombras marcadas. Elevado: lo mismo con un borde iluminado y una sombra profunda. Claro: cristal fino, sin desenfoque. Hoy: el cristal más oscuro con sombra suave.'),
    'fi_fi': ('Huurre', 'Kohotettu', 'Kirkas', 'Materiaali', 'Paneelien lasi. Huurre: vaaleampi, kuvan värit kuultavat läpi, vahvat varjot. Kohotettu: sama valaistulla reunalla ja syvällä varjolla. Kirkas: ohut lasi ilman sumennusta. Tänään: tummempi lasi pehmeällä varjolla.'),
    'fr_fr': ('Givre', 'Surélevé', 'Clair', 'Matière', "Le verre des panneaux. Givre : plus clair, les couleurs de l'image transparaissent, ombres marquées. Surélevé : pareil avec un bord éclairé et une ombre profonde. Clair : verre fin, sans flou. Aujourd'hui : le verre plus sombre à l'ombre douce."),
    'hu_hu': ('Dér', 'Kiemelt', 'Átlátszó', 'Anyag', 'A panelek üvege. Dér: világosabb, a kép színei átsejlenek, erős árnyékok. Kiemelt: ugyanez világos peremmel és mély árnyékkal. Átlátszó: vékony üveg elmosás nélkül. Ma: a sötétebb üveg lágy árnyékkal.'),
    'it_it': ('Brina', 'Rialzato', 'Trasparente', 'Materiale', "Il vetro dei pannelli. Brina: più chiaro, i colori dell'immagine traspaiono, ombre marcate. Rialzato: lo stesso con un bordo illuminato e un'ombra profonda. Trasparente: vetro sottile, senza sfocatura. Oggi: il vetro più scuro con ombra morbida."),
    'ja_jp': ('フロスト', 'レイズド', 'クリア', '素材', 'パネルのガラス。フロスト: 明るめで画像の色が透け、影が強い。レイズド: 同じく明るい縁と深い影。クリア: 薄いガラスでぼかしなし。今日: 暗めのガラスと柔らかい影。'),
    'ko_kr': ('프로스트', '돋움', '투명', '재질', '패널의 유리. 프로스트: 더 밝고 그림의 색이 비치며 그림자가 강함. 돋움: 같은 유리에 밝은 테두리와 깊은 그림자. 투명: 얇은 유리, 흐림 없음. 오늘: 더 어두운 유리와 부드러운 그림자.'),
    'nb_no': ('Frost', 'Hevet', 'Klar', 'Materiale', 'Panelenes glass. Frost: lysere, bildets farger skinner gjennom, kraftige skygger. Hevet: det samme med en lys kant og en dyp skygge. Klar: tynt glass uten uskarphet. I dag: det mørkere glasset med en myk skygge.'),
    'nl_nl': ('Rijp', 'Verhoogd', 'Helder', 'Materiaal', 'Het glas van de panelen. Rijp: lichter, de kleuren van het beeld schijnen door, sterke schaduwen. Verhoogd: hetzelfde met een lichte rand en een diepe schaduw. Helder: dun glas zonder vervaging. Vandaag: het donkere glas met een zachte schaduw.'),
    'pl_pl': ('Szron', 'Uniesione', 'Przejrzyste', 'Materiał', 'Szkło paneli. Szron: jaśniejsze, kolory obrazu prześwitują, mocne cienie. Uniesione: to samo z jasną krawędzią i głębokim cieniem. Przejrzyste: cienkie szkło bez rozmycia. Dziś: ciemniejsze szkło z miękkim cieniem.'),
    'pt_br': ('Geada', 'Elevado', 'Transparente', 'Material', 'O vidro dos painéis. Geada: mais claro, as cores da imagem aparecem, sombras fortes. Elevado: o mesmo com uma borda iluminada e sombra profunda. Transparente: vidro fino, sem desfoque. Hoje: o vidro mais escuro com sombra suave.'),
    'pt_pt': ('Geada', 'Elevado', 'Transparente', 'Material', 'O vidro dos painéis. Geada: mais claro, as cores da imagem transparecem, sombras fortes. Elevado: o mesmo com uma margem iluminada e sombra profunda. Transparente: vidro fino, sem desfoque. Hoje: o vidro mais escuro com sombra suave.'),
    'ru_ru': ('Иней', 'Приподнятый', 'Прозрачный', 'Материал', 'Стекло панелей. Иней: светлее, цвета изображения просвечивают, сильные тени. Приподнятый: то же со светлой кромкой и глубокой тенью. Прозрачный: тонкое стекло без размытия. Сегодня: более тёмное стекло с мягкой тенью.'),
    'sv_se': ('Frost', 'Upphöjd', 'Klar', 'Material', 'Panelernas glas. Frost: ljusare, bildens färger lyser igenom, kraftiga skuggor. Upphöjd: samma med en ljus kant och en djup skugga. Klar: tunt glas utan oskärpa. I dag: det mörkare glaset med en mjuk skugga.'),
    'tr_tr': ('Buzlu', 'Yükseltilmiş', 'Şeffaf', 'Malzeme', 'Panellerin camı. Buzlu: daha açık, resmin renkleri içeriden görünür, güçlü gölgeler. Yükseltilmiş: aynısı, aydınlık kenar ve derin gölgeyle. Şeffaf: ince cam, bulanıklık yok. Bugün: yumuşak gölgeli daha koyu cam.'),
    'uk_ua': ('Іній', 'Піднятий', 'Прозорий', 'Матеріал', 'Скло панелей. Іній: світліше, кольори зображення просвічують, сильні тіні. Піднятий: те саме зі світлим краєм і глибокою тінню. Прозорий: тонке скло без розмиття. Сьогодні: темніше скло з м’якою тінню.'),
    'zh_cn': ('磨砂', '浮起', '透明', '材质', '面板的玻璃。磨砂：更亮，图片的颜色透出来，阴影更强。浮起：同样的磨砂加亮边和深阴影。透明：薄玻璃，无模糊。今天：较暗的玻璃和柔和的阴影。'),
    'zh_tw': ('霧面', '浮起', '透明', '材質', '面板的玻璃。霧面：較亮，圖片的顏色透出來，陰影較強。浮起：同樣的霧面加亮邊和深陰影。透明：薄玻璃，無模糊。今天：較暗的玻璃和柔和的陰影。'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32547"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    assert lang == 'en_gb' or len(tr) == len(EN), lang
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else tr[i].replace('"', '\\"')
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32547-32551 added in %d languages' % done)
