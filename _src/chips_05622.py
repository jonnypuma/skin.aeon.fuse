# -*- coding: utf-8 -*-
"""0.56.22 Media info chips picker (the user: "you were also supposed to add a picker for which media info chips to
display (includes mediainfo from sidecars)"). Runs once (marker); then run _src/ok_only.py.

- Skin settings > Details gets row 9780 "Media info chips" under Media info from sidecars: OK opens the helper's
  multi-select (RunScript(script.aeon.helper,chippick)); the row shows how many are on (Skin.String(aeon.chips.shown),
  default 7 / 14).
- Chips that are on by default keep their hide switch: aeon.hide.res / hdr / audio / aspect (the rows Details already
  has stay in step), new aeon.hide.channels / dvp / source. Every chip BUTTON (the chip rows that close up: the
  information page, Home's hero, the library panels, the Fused Glass panels) gets its switch; the small chips drawn at
  fixed places inside list rows keep only the switches they had (res / hdr / audio).
- New sidecar chips on the information page, off by default (Skin.HasSetting(aeon.chip.<key>)): container, bit rate,
  file size, subtitles, chapters, commentary, 3D (need Media info from sidecars, like the source chip)."""
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.22 chips'
SET = os.path.join('1080i', 'SkinSettings.xml')
INC = os.path.join('1080i', 'Includes_Settings.xml')
INFO = os.path.join('1080i', 'Includes_VideoInfo.xml')
FILES = ['Includes_Aeon_Home.xml', 'Includes_Aeon_Sub.xml', 'Includes_Aeon_Views2.xml', 'Includes_Fused.xml', 'Includes_VideoInfo.xml']
FIRST = 32645
EN = ('Media info chips', 'Which chips the information page, Home and the library panels show. The sidecar chips need Media info from sidecars.',
      'Resolution', 'Aspect ratio', 'HDR and Dolby Vision', 'Dolby Vision profile', 'Audio format', 'Audio channels', 'Source (sidecar)',
      'Container (sidecar)', 'Bit rate (sidecar)', 'File size (sidecar)', 'Subtitles (sidecar)', 'Chapters (sidecar)',
      'Commentary (sidecar)', '3D (sidecar)', 'chapters', 'commentary')
S = {
    'cs_cz': ('Čipy s informacemi o médiu', 'Které čipy ukazuje stránka informací, Domů a panely knihovny. Čipy ze sidecar potřebují Informace o médiu ze sidecar.',
              'Rozlišení', 'Poměr stran', 'HDR a Dolby Vision', 'Profil Dolby Vision', 'Formát zvuku', 'Zvukové kanály', 'Zdroj (sidecar)',
              'Kontejner (sidecar)', 'Datový tok (sidecar)', 'Velikost souboru (sidecar)', 'Titulky (sidecar)', 'Kapitoly (sidecar)',
              'Komentář (sidecar)', '3D (sidecar)', 'kapitol', 'komentář'),
    'da_dk': ('Medieinfo-chips', 'Hvilke chips informationssiden, Hjem og bibliotekets paneler viser. Sidecar-chips kræver Medieinfo fra sidecar-filer.',
              'Opløsning', 'Billedformat', 'HDR og Dolby Vision', 'Dolby Vision-profil', 'Lydformat', 'Lydkanaler', 'Kilde (sidecar)',
              'Container (sidecar)', 'Bitrate (sidecar)', 'Filstørrelse (sidecar)', 'Undertekster (sidecar)', 'Kapitler (sidecar)',
              'Kommentarspor (sidecar)', '3D (sidecar)', 'kapitler', 'kommentar'),
    'de_de': ('Medieninfo-Chips', 'Welche Chips die Infoseite, Home und die Bibliotheksfelder zeigen. Die Sidecar-Chips brauchen Medieninfo aus Sidecars.',
              'Auflösung', 'Seitenverhältnis', 'HDR und Dolby Vision', 'Dolby-Vision-Profil', 'Tonformat', 'Tonkanäle', 'Quelle (Sidecar)',
              'Container (Sidecar)', 'Bitrate (Sidecar)', 'Dateigröße (Sidecar)', 'Untertitel (Sidecar)', 'Kapitel (Sidecar)',
              'Kommentar (Sidecar)', '3D (Sidecar)', 'Kapitel', 'Kommentar'),
    'el_gr': ('Ετικέτες πληροφοριών μέσου', 'Ποιες ετικέτες δείχνουν η σελίδα πληροφοριών, η Αρχική και τα πάνελ της βιβλιοθήκης. Οι ετικέτες sidecar χρειάζονται Πληροφορίες μέσου από sidecar.',
              'Ανάλυση', 'Αναλογία εικόνας', 'HDR και Dolby Vision', 'Προφίλ Dolby Vision', 'Μορφή ήχου', 'Κανάλια ήχου', 'Πηγή (sidecar)',
              'Περιέκτης (sidecar)', 'Ρυθμός bit (sidecar)', 'Μέγεθος αρχείου (sidecar)', 'Υπότιτλοι (sidecar)', 'Κεφάλαια (sidecar)',
              'Σχολιασμός (sidecar)', '3D (sidecar)', 'κεφάλαια', 'σχολιασμός'),
    'es_es': ('Etiquetas de información del medio', 'Qué etiquetas muestran la página de información, Inicio y los paneles de la biblioteca. Las etiquetas sidecar necesitan Información del medio de sidecar.',
              'Resolución', 'Relación de aspecto', 'HDR y Dolby Vision', 'Perfil Dolby Vision', 'Formato de audio', 'Canales de audio', 'Origen (sidecar)',
              'Contenedor (sidecar)', 'Tasa de bits (sidecar)', 'Tamaño del archivo (sidecar)', 'Subtítulos (sidecar)', 'Capítulos (sidecar)',
              'Comentarios (sidecar)', '3D (sidecar)', 'capítulos', 'comentarios'),
    'fi_fi': ('Mediatietojen merkit', 'Mitkä merkit tietosivu, Koti ja kirjaston paneelit näyttävät. Sidecar-merkit tarvitsevat Mediatiedot sidecar-tiedostoista.',
              'Tarkkuus', 'Kuvasuhde', 'HDR ja Dolby Vision', 'Dolby Vision -profiili', 'Äänimuoto', 'Äänikanavat', 'Lähde (sidecar)',
              'Säiliö (sidecar)', 'Bittinopeus (sidecar)', 'Tiedostokoko (sidecar)', 'Tekstitykset (sidecar)', 'Kappaleet (sidecar)',
              'Kommentaariraita (sidecar)', '3D (sidecar)', 'kappaletta', 'kommentaari'),
    'fr_fr': ('Pastilles d’infos média', 'Les pastilles que montrent la page d’infos, l’accueil et les panneaux de la bibliothèque. Les pastilles sidecar demandent Infos média des fichiers sidecar.',
              'Résolution', 'Format d’image', 'HDR et Dolby Vision', 'Profil Dolby Vision', 'Format audio', 'Canaux audio', 'Source (sidecar)',
              'Conteneur (sidecar)', 'Débit (sidecar)', 'Taille du fichier (sidecar)', 'Sous-titres (sidecar)', 'Chapitres (sidecar)',
              'Commentaire (sidecar)', '3D (sidecar)', 'chapitres', 'commentaire'),
    'hu_hu': ('Médiainfó-címkék', 'Mely címkéket mutat az infóoldal, a Kezdőlap és a könyvtár paneljei. A sidecar címkékhez kell a Médiainfó sidecar fájlokból.',
              'Felbontás', 'Képarány', 'HDR és Dolby Vision', 'Dolby Vision-profil', 'Hangformátum', 'Hangcsatornák', 'Forrás (sidecar)',
              'Konténer (sidecar)', 'Bitráta (sidecar)', 'Fájlméret (sidecar)', 'Feliratok (sidecar)', 'Fejezetek (sidecar)',
              'Kommentár (sidecar)', '3D (sidecar)', 'fejezet', 'kommentár'),
    'it_it': ('Etichette info media', 'Quali etichette mostrano la pagina info, la Home e i pannelli della libreria. Le etichette sidecar richiedono Info media dai file sidecar.',
              'Risoluzione', 'Formato', 'HDR e Dolby Vision', 'Profilo Dolby Vision', 'Formato audio', 'Canali audio', 'Sorgente (sidecar)',
              'Contenitore (sidecar)', 'Bitrate (sidecar)', 'Dimensione file (sidecar)', 'Sottotitoli (sidecar)', 'Capitoli (sidecar)',
              'Commento (sidecar)', '3D (sidecar)', 'capitoli', 'commento'),
    'ja_jp': ('メディア情報チップ', '情報ページ、ホーム、ライブラリのパネルに表示するチップ。サイドカーのチップには「サイドカーのメディア情報」が必要です。',
              '解像度', 'アスペクト比', 'HDR と Dolby Vision', 'Dolby Vision プロファイル', '音声形式', '音声チャンネル', 'ソース（サイドカー）',
              'コンテナー（サイドカー）', 'ビットレート（サイドカー）', 'ファイルサイズ（サイドカー）', '字幕（サイドカー）', 'チャプター（サイドカー）',
              'コメンタリー（サイドカー）', '3D（サイドカー）', 'チャプター', 'コメンタリー'),
    'ko_kr': ('미디어 정보 칩', '정보 페이지, 홈, 라이브러리 패널에 보일 칩. 사이드카 칩은 사이드카 미디어 정보가 필요합니다.',
              '해상도', '화면 비율', 'HDR 및 Dolby Vision', 'Dolby Vision 프로필', '오디오 형식', '오디오 채널', '소스(사이드카)',
              '컨테이너(사이드카)', '비트레이트(사이드카)', '파일 크기(사이드카)', '자막(사이드카)', '챕터(사이드카)',
              '코멘터리(사이드카)', '3D(사이드카)', '챕터', '코멘터리'),
    'nb_no': ('Medieinfo-brikker', 'Hvilke brikker infosiden, Hjem og bibliotekets paneler viser. Sidecar-brikkene trenger Medieinfo fra sidecar-filer.',
              'Oppløsning', 'Bildeformat', 'HDR og Dolby Vision', 'Dolby Vision-profil', 'Lydformat', 'Lydkanaler', 'Kilde (sidecar)',
              'Container (sidecar)', 'Bitrate (sidecar)', 'Filstørrelse (sidecar)', 'Undertekster (sidecar)', 'Kapitler (sidecar)',
              'Kommentarspor (sidecar)', '3D (sidecar)', 'kapitler', 'kommentar'),
    'nl_nl': ('Media-infochips', 'Welke chips de infopagina, Home en de bibliotheekpanelen tonen. De sidecar-chips hebben Media-info uit sidecars nodig.',
              'Resolutie', 'Beeldverhouding', 'HDR en Dolby Vision', 'Dolby Vision-profiel', 'Audioformaat', 'Audiokanalen', 'Bron (sidecar)',
              'Container (sidecar)', 'Bitrate (sidecar)', 'Bestandsgrootte (sidecar)', 'Ondertitels (sidecar)', 'Hoofdstukken (sidecar)',
              'Commentaar (sidecar)', '3D (sidecar)', 'hoofdstukken', 'commentaar'),
    'pl_pl': ('Plakietki informacji o mediach', 'Które plakietki pokazuje strona informacji, Ekran główny i panele biblioteki. Plakietki sidecar wymagają Informacji o mediach z plików sidecar.',
              'Rozdzielczość', 'Proporcje obrazu', 'HDR i Dolby Vision', 'Profil Dolby Vision', 'Format dźwięku', 'Kanały dźwięku', 'Źródło (sidecar)',
              'Kontener (sidecar)', 'Przepływność (sidecar)', 'Rozmiar pliku (sidecar)', 'Napisy (sidecar)', 'Rozdziały (sidecar)',
              'Komentarz (sidecar)', '3D (sidecar)', 'rozdziałów', 'komentarz'),
    'pt_br': ('Etiquetas de informação de mídia', 'Quais etiquetas a página de informação, o Início e os painéis da biblioteca mostram. As etiquetas sidecar precisam de Informação de mídia do sidecar.',
              'Resolução', 'Proporção', 'HDR e Dolby Vision', 'Perfil Dolby Vision', 'Formato de áudio', 'Canais de áudio', 'Origem (sidecar)',
              'Contêiner (sidecar)', 'Taxa de bits (sidecar)', 'Tamanho do arquivo (sidecar)', 'Legendas (sidecar)', 'Capítulos (sidecar)',
              'Comentários (sidecar)', '3D (sidecar)', 'capítulos', 'comentários'),
    'pt_pt': ('Etiquetas de informação multimédia', 'Que etiquetas mostram a página de informação, o Início e os painéis da biblioteca. As etiquetas sidecar precisam de Informação multimédia do sidecar.',
              'Resolução', 'Proporção', 'HDR e Dolby Vision', 'Perfil Dolby Vision', 'Formato de áudio', 'Canais de áudio', 'Origem (sidecar)',
              'Contentor (sidecar)', 'Taxa de bits (sidecar)', 'Tamanho do ficheiro (sidecar)', 'Legendas (sidecar)', 'Capítulos (sidecar)',
              'Comentários (sidecar)', '3D (sidecar)', 'capítulos', 'comentários'),
    'ru_ru': ('Значки сведений о медиа', 'Какие значки показывают страница сведений, Главная и панели библиотеки. Значкам из sidecar нужны Сведения о медиа из sidecar.',
              'Разрешение', 'Соотношение сторон', 'HDR и Dolby Vision', 'Профиль Dolby Vision', 'Формат звука', 'Каналы звука', 'Источник (sidecar)',
              'Контейнер (sidecar)', 'Битрейт (sidecar)', 'Размер файла (sidecar)', 'Субтитры (sidecar)', 'Главы (sidecar)',
              'Комментарии (sidecar)', '3D (sidecar)', 'глав', 'комментарии'),
    'sv_se': ('Medieinfo-märken', 'Vilka märken infosidan, Hem och bibliotekets paneler visar. Sidecar-märkena behöver Medieinfo från sidecar-filer.',
              'Upplösning', 'Bildformat', 'HDR och Dolby Vision', 'Dolby Vision-profil', 'Ljudformat', 'Ljudkanaler', 'Källa (sidecar)',
              'Container (sidecar)', 'Bithastighet (sidecar)', 'Filstorlek (sidecar)', 'Undertexter (sidecar)', 'Kapitel (sidecar)',
              'Kommentarspår (sidecar)', '3D (sidecar)', 'kapitel', 'kommentar'),
    'tr_tr': ('Medya bilgisi etiketleri', 'Bilgi sayfası, Ana sayfa ve kitaplık panellerinin gösterdiği etiketler. Sidecar etiketleri için Sidecar medya bilgisi gerekir.',
              'Çözünürlük', 'En boy oranı', 'HDR ve Dolby Vision', 'Dolby Vision profili', 'Ses biçimi', 'Ses kanalları', 'Kaynak (sidecar)',
              'Kapsayıcı (sidecar)', 'Bit hızı (sidecar)', 'Dosya boyutu (sidecar)', 'Altyazılar (sidecar)', 'Bölümler (sidecar)',
              'Yorum (sidecar)', '3D (sidecar)', 'bölüm', 'yorum'),
    'uk_ua': ('Значки відомостей про медіа', 'Які значки показують сторінка відомостей, Головна та панелі бібліотеки. Значкам із sidecar потрібні Відомості про медіа з sidecar.',
              'Роздільність', 'Співвідношення сторін', 'HDR і Dolby Vision', 'Профіль Dolby Vision', 'Формат звуку', 'Канали звуку', 'Джерело (sidecar)',
              'Контейнер (sidecar)', 'Бітрейт (sidecar)', 'Розмір файлу (sidecar)', 'Субтитри (sidecar)', 'Розділи (sidecar)',
              'Коментарі (sidecar)', '3D (sidecar)', 'розділів', 'коментарі'),
    'zh_cn': ('媒体信息标签', '信息页、主页和媒体库面板显示哪些标签。附属文件标签需要“附属文件的媒体信息”。',
              '分辨率', '画面比例', 'HDR 和 Dolby Vision', 'Dolby Vision 配置', '音频格式', '音频声道', '来源（附属文件）',
              '容器（附属文件）', '码率（附属文件）', '文件大小（附属文件）', '字幕（附属文件）', '章节（附属文件）',
              '评论音轨（附属文件）', '3D（附属文件）', '章节', '评论'),
    'zh_tw': ('媒體資訊標籤', '資訊頁、首頁和媒體庫面板顯示哪些標籤。附屬檔案標籤需要「附屬檔案的媒體資訊」。',
              '解析度', '畫面比例', 'HDR 與 Dolby Vision', 'Dolby Vision 設定檔', '音訊格式', '音訊聲道', '來源（附屬檔案）',
              '容器（附屬檔案）', '位元率（附屬檔案）', '檔案大小（附屬檔案）', '字幕（附屬檔案）', '章節（附屬檔案）',
              '評論音軌（附屬檔案）', '3D（附屬檔案）', '章節', '評論'),
}
A = lambda n: '$ADDON[skin.aeon.fuse %d]' % (FIRST + n)

# label pattern of a chip button -> its hide switch (the switches that already exist are only added where missing)
HIDE = [('aeon.hide.res', r'\$VAR\[(?:Aeon_LVRes\w*|FG_L\d+_Res|Aeon_ResR|Aeon_ResL|Home_HeroChip)\]'),
        ('aeon.hide.aspect', r'\$VAR\[Aeon_LVAsp\w*\]|VideoAspect\]:1'),
        ('aeon.hide.hdr', r'\$VAR\[(?:Aeon_LVHdr\w*|FG_L\d+_Hdr|FG_L_HdrChip)\]'),
        ('aeon.hide.dvp', r'aeon\.dvp\)\]'),
        ('aeon.hide.audio', r'\$VAR\[(?:Aeon_LVAud\w*|FG_L\d+_Audio|FG_EcAudio)\]'),
        ('aeon.hide.channels', r'\$VAR\[Aeon_LVCh\w*\]'),
        ('aeon.hide.source', r'aeon\.mi\.source\)\]')]
# new sidecar chips (off by default): key, label
SIDE = [('container', '$INFO[Window(Home).Property(aeon.mi.container)]'),
        ('bitrate', '$INFO[Window(Home).Property(aeon.mi.bitrate)]'),
        ('size', '$INFO[Window(Home).Property(aeon.mi.size)]'),
        ('subs', '$INFO[Window(Home).Property(aeon.mi.subs.count)] $LOCALIZE[287]', 'subs.count'),
        ('chapters', '$INFO[Window(Home).Property(aeon.mi.chapters)] %s' % A(16)),
        ('commentary', A(17)),
        ('3d', '3D')]


def strings():
    for folder in sorted(os.listdir('language')):
        lang = folder.replace('resource.language.', '')
        p = os.path.join('language', folder, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        tr = EN if lang == 'en_gb' else S[lang]
        assert len(tr) == len(EN), lang
        add = ''
        for i, en in enumerate(EN):
            sid = FIRST + i
            if 'msgctxt "#%d"' % sid in t:
                continue
            esc = lambda s: s.replace('\\', '\\\\').replace('"', '\\"')
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), '' if lang == 'en_gb' else esc(tr[i]))
        if add:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)


def switches():
    counts = {}
    for name in FILES:
        p = os.path.join('1080i', name)
        t = io.open(p, encoding='utf-8').read()

        def fix(m):
            ctl = m.group(0)
            label = re.search(r'<label>(.*?)</label>', ctl)
            if not label:
                return ctl
            for flag, pat in HIDE:
                if re.search(pat, label.group(1)) and flag + ')' not in ctl:
                    cond = '!Skin.HasSetting(%s)' % flag
                    counts[flag] = counts.get(flag, 0) + 1
                    if '<visible>' in ctl:
                        ctl = re.sub(r'<visible>(.*?)</visible>', lambda v: '<visible>[%s] + %s</visible>' % (v.group(1), cond), ctl, count=1)
                    else:
                        ctl = ctl.replace('</control>', '<visible>%s</visible></control>' % cond)
            return ctl
        t = re.sub(r'<control type="button">(?:(?!<control ).)*?</control>', fix, t)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        ET.parse(p)
    return counts


def sidecar_chips():
    t = io.open(INFO, encoding='utf-8').read()
    lines = [l for l in t.split('\n') if '<control type="button">' in l and 'aeon.mi.source)]' in l and '<label>' in l]
    assert len(lines) == 2, len(lines)
    out = []
    for key, label, *prop in SIDE:
        p = prop[0] if prop else key
        for line in lines:
            new = re.sub(r'<label>.*?</label>', '<label>[UPPERCASE]%s[/UPPERCASE]</label>' % label, line, count=1)
            new = new.replace('!String.IsEmpty(Window(Home).Property(aeon.mi.source))', '!String.IsEmpty(Window(Home).Property(aeon.mi.%s)) + Skin.HasSetting(aeon.chip.%s)' % (p, key))
            new = new.replace(' + !Skin.HasSetting(aeon.hide.source)', '').replace('[', '[', 1)
            new = re.sub(r'<visible>\[(.*)\] \+ !Skin\.HasSetting\(aeon\.hide\.source\)</visible>', r'<visible>\1</visible>', new)
            out.append(new)
    i = t.index(lines[1]) + len(lines[1])
    t = t[:i] + '\n\t\t\t\t\t\t\t<!-- %s: the sidecar chips you pick (Skin settings > Details > Media info chips), off by default -->\n' % MARK + '\n'.join(out) + t[i:]
    io.open(INFO, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(INFO)


ROW = '''	<control type="group"><!-- row 9780 (%(m)s) -->
		<width>1100</width><height>70</height>
<control type="group"><left>41</left><top>0</top><visible>Control.HasFocus(9780)</visible>
				<animation type="Visible"><effect type="fade" start="0" end="100" time="150"/></animation>
				<include>FG_LandVisible</include>
				<animation type="Hidden"><effect type="fade" start="100" end="0" time="100"/></animation>
%(bar)s
			</control>
<control type="group"><left>160</left><top>0</top>
				<include content="Dlg_SkinRowChrome">
					<param name="id" value="9780"/><param name="label" value="%(label)s"/><param name="hint" value=""/><param name="labelTop" value="0"/><param name="labelH" value="70"/><param name="icon" value="aeon/icons/layers.png"/><param name="labelx" value="46"/>
				</include>
				<control type="button" id="9780">
					<onup>9776</onup><ondown>9700</ondown>
					<include>Dlg_SkinRowButton</include>
					<onback>9566</onback>
					<onleft>SetFocus(9566)</onleft>
					<onclick>RunScript(script.aeon.helper,chippick)</onclick>
				</control>
				<control type="label"><left>480</left><top>9</top><width>380</width><height>52</height><align>right</align><font>st_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$VAR[Aeon_ChipsShown]</label><visible>!Control.HasFocus(9780)</visible></control>
				<control type="label"><left>480</left><top>9</top><width>380</width><height>52</height><align>right</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_OnBarInk]</textcolor><label>$VAR[Aeon_ChipsShown]</label><visible>Control.HasFocus(9780)</visible></control>
			</control>
	</control>'''


def row():
    t = io.open(SET, encoding='utf-8').read()
    a = t.index('<control type="group"><!-- row 9776 -->')
    b = t.index('\n\t</control>', t.index('<control type="button" id="9776">', a)) + len('\n\t</control>')
    old = t[a:b]
    bar = re.search(r'<control type="group"><left>41</left><top>0</top><visible>Control.HasFocus\(9776\)</visible>(.*?)\n\t\t\t</control>', old, re.S)
    bar_lines = [l for l in bar.group(1).split('\n') if '<control type="image">' in l]
    new_row = ROW % {'m': MARK, 'bar': '\n'.join(bar_lines), 'label': A(0)}
    old2 = old.replace('<onup>9761</onup><ondown>9700</ondown>', '<onup>9761</onup><ondown>9780</ondown>')
    assert old2 != old
    t = t[:a] + old2 + '\n' + new_row + t[b:]
    i = t.index('<control type="button" id="9700">')
    j = t.index('<onup>9776</onup>', i)
    assert j - i < 200, j - i
    t = t[:j] + '<onup>9780</onup>' + t[j + len('<onup>9776</onup>'):]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(SET)
    s = io.open(INC, encoding='utf-8').read()
    old = '\t\t<value condition="Control.HasFocus(9776)">$ADDON[skin.aeon.fuse 32616]</value><!-- 0.56.20 settings_details -->'
    assert s.count(old) == 1
    s = s.replace(old, old + '\n\t\t<value condition="Control.HasFocus(9780)">%s</value><!-- %s -->' % (A(1), MARK))
    i = s.index('<includes>') + len('<includes>')
    s = s[:i] + ('\n\t<!-- %s: Media info chips, how many are on (the helper writes it when you pick; 7 of 14 by default) -->\n'
                 '\t<variable name="Aeon_ChipsShown">\n\t\t<value condition="!String.IsEmpty(Skin.String(aeon.chips.shown))">$INFO[Skin.String(aeon.chips.shown)]</value>\n'
                 '\t\t<value>7 / 14</value>\n\t</variable>\n') % MARK + s[i:].lstrip('\n')
    io.open(INC, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(INC)


def main():
    if MARK in io.open(SET, encoding='utf-8').read():
        print('already')
        return
    strings()
    print('switches', switches())
    sidecar_chips()
    row()
    print('ok')


if __name__ == '__main__':
    main()
