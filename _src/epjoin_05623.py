# -*- coding: utf-8 -*-
"""0.56.23 Episodes in one file as one row (approved board "1-2 LA X", canvas 1G1LeYYjENtdRdbvfKeHt3; the user: "Yes, build
them"). With Skin settings > Details > Episodes in one file as one row on (Skin.HasSetting(aeon.ep.join), off by
default), the helper (0.3.100) replaces a season's list that has episodes sharing one video file by its own list
(?info=episodes): those episodes are one row, the numbers a range in ListItem.Property(aeon.ep.range) ("1-2",
"36-38") and the episode code in the user's form in aeon.ep.code. Here:
- every Aeon_EpCode* variable of a list shows aeon.ep.code first;
- every label that shows an episode number ($INFO[<list>ListItem.Episode...], not in the player, the guide or Live TV)
  goes through a variable that shows the range when there is one, "Episode" becoming "Episodes" before it;
- Details gets row 9781 (switch, under Media info chips), help 32664, a preview card.
Runs once (marker); then run _src/ok_only.py and _src/skin_previews.py."""
import hashlib
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.23 epjoin'
D = '1080i'
SUB = os.path.join(D, 'Includes_Aeon_Sub.xml')
SET = os.path.join(D, 'SkinSettings.xml')
INC = os.path.join(D, 'Includes_Settings.xml')
SKIP = {'Includes_FusedPlayer.xml', 'MyPVRGuide.xml', 'Includes_Misc.xml', 'SkinSettings.xml'}
SID = 32663
S = {
    'en_gb': ('Episodes in one file as one row', 'Episodes stored in one video file (a double episode, three cartoons) show as one row: 1–2, one title, the file\'s running time. The season\'s list then comes from Aeon Fuse Helper.'),
    'cs_cz': ('Díly v jednom souboru jako jeden řádek', 'Díly uložené v jednom videosouboru (dvojdíl, tři kreslené grotesky) se ukážou jako jeden řádek: 1–2, jeden název, délka souboru. Seznam řady pak dodává Aeon Fuse Helper.'),
    'da_dk': ('Afsnit i én fil som én række', 'Afsnit i én videofil (et dobbeltafsnit, tre tegnefilm) vises som én række: 1–2, én titel, filens spilletid. Sæsonens liste kommer så fra Aeon Fuse Helper.'),
    'de_de': ('Folgen in einer Datei als eine Zeile', 'Folgen in einer Videodatei (eine Doppelfolge, drei Cartoons) erscheinen als eine Zeile: 1–2, ein Titel, die Laufzeit der Datei. Die Liste der Staffel kommt dann von Aeon Fuse Helper.'),
    'el_gr': ('Επεισόδια σε ένα αρχείο ως μία γραμμή', 'Επεισόδια σε ένα αρχείο βίντεο (διπλό επεισόδιο, τρία καρτούν) εμφανίζονται ως μία γραμμή: 1–2, ένας τίτλος, η διάρκεια του αρχείου. Η λίστα της σεζόν έρχεται τότε από το Aeon Fuse Helper.'),
    'es_es': ('Episodios en un archivo como una fila', 'Los episodios guardados en un archivo de vídeo (un episodio doble, tres dibujos) se ven como una fila: 1–2, un título, la duración del archivo. La lista de la temporada viene entonces de Aeon Fuse Helper.'),
    'fi_fi': ('Yhden tiedoston jaksot yhtenä rivinä', 'Yhteen videotiedostoon tallennetut jaksot (kaksoisjakso, kolme piirrettyä) näkyvät yhtenä rivinä: 1–2, yksi nimi, tiedoston kesto. Kauden luettelo tulee silloin Aeon Fuse Helperiltä.'),
    'fr_fr': ('Épisodes d’un même fichier sur une ligne', 'Les épisodes d’un même fichier vidéo (un double épisode, trois dessins animés) tiennent sur une ligne : 1–2, un titre, la durée du fichier. La liste de la saison vient alors d’Aeon Fuse Helper.'),
    'hu_hu': ('Egy fájlban lévő részek egy sorban', 'Az egy videofájlban tárolt részek (dupla rész, három rajzfilm) egy sorként jelennek meg: 1–2, egy cím, a fájl hossza. Az évad listáját ekkor az Aeon Fuse Helper adja.'),
    'it_it': ('Episodi in un file come una riga', 'Gli episodi in un unico file video (un doppio episodio, tre cartoni) appaiono come una riga: 1–2, un titolo, la durata del file. L’elenco della stagione arriva allora da Aeon Fuse Helper.'),
    'ja_jp': ('1つのファイルのエピソードを1行に', '1つの動画ファイルに入ったエピソード（前後編、3本のアニメ）を1行で表示します：1–2、タイトル1つ、ファイルの長さ。シーズンの一覧は Aeon Fuse Helper が出します。'),
    'ko_kr': ('한 파일의 에피소드를 한 줄로', '한 동영상 파일에 든 에피소드(2부작, 만화 세 편)를 한 줄로 보여 줍니다: 1–2, 제목 하나, 파일 길이. 시즌 목록은 Aeon Fuse Helper가 만듭니다.'),
    'nb_no': ('Episoder i én fil som én rad', 'Episoder i én videofil (en dobbeltepisode, tre tegnefilmer) vises som én rad: 1–2, én tittel, filens spilletid. Sesongens liste kommer da fra Aeon Fuse Helper.'),
    'nl_nl': ('Afleveringen in één bestand als één rij', 'Afleveringen in één videobestand (een dubbele aflevering, drie tekenfilms) staan als één rij: 1–2, één titel, de speelduur van het bestand. De lijst van het seizoen komt dan van Aeon Fuse Helper.'),
    'pl_pl': ('Odcinki z jednego pliku jako jeden wiersz', 'Odcinki zapisane w jednym pliku wideo (podwójny odcinek, trzy kreskówki) widać jako jeden wiersz: 1–2, jeden tytuł, czas trwania pliku. Listę sezonu daje wtedy Aeon Fuse Helper.'),
    'pt_br': ('Episódios em um arquivo como uma linha', 'Episódios guardados em um arquivo de vídeo (um episódio duplo, três desenhos) aparecem como uma linha: 1–2, um título, a duração do arquivo. A lista da temporada vem então do Aeon Fuse Helper.'),
    'pt_pt': ('Episódios num ficheiro como uma linha', 'Episódios guardados num ficheiro de vídeo (um episódio duplo, três desenhos) aparecem como uma linha: 1–2, um título, a duração do ficheiro. A lista da temporada vem então do Aeon Fuse Helper.'),
    'ru_ru': ('Серии в одном файле одной строкой', 'Серии в одном видеофайле (двойная серия, три мультфильма) показываются одной строкой: 1–2, одно название, длительность файла. Список сезона тогда даёт Aeon Fuse Helper.'),
    'sv_se': ('Avsnitt i en fil som en rad', 'Avsnitt i en videofil (ett dubbelavsnitt, tre tecknade) visas som en rad: 1–2, en titel, filens speltid. Säsongens lista kommer då från Aeon Fuse Helper.'),
    'tr_tr': ('Tek dosyadaki bölümler tek satır', 'Tek bir video dosyasındaki bölümler (çift bölüm, üç çizgi film) tek satır olarak görünür: 1–2, tek başlık, dosyanın süresi. Sezon listesi o zaman Aeon Fuse Helper’dan gelir.'),
    'uk_ua': ('Серії в одному файлі одним рядком', 'Серії в одному відеофайлі (подвійна серія, три мультфільми) показуються одним рядком: 1–2, одна назва, тривалість файлу. Список сезону тоді дає Aeon Fuse Helper.'),
    'zh_cn': ('同一文件的剧集合为一行', '存在同一视频文件中的剧集（上下集、三部动画）显示为一行：1–2、一个标题、文件时长。该季列表将由 Aeon Fuse Helper 提供。'),
    'zh_tw': ('同一檔案的劇集合為一列', '存在同一影片檔案中的劇集（上下集、三部卡通）顯示為一列：1–2、一個標題、檔案長度。該季清單將由 Aeon Fuse Helper 提供。'),
}
A = lambda n: '$ADDON[skin.aeon.fuse %d]' % (SID + n)
EP = re.compile(r'\$INFO\[((?:Container\(\d+\)\.)?ListItem)\.Episode(?:,([^,\]]*),([^,\]]*))?\]')


def strings():
    for folder in sorted(os.listdir('language')):
        lang = folder.replace('resource.language.', '')
        p = os.path.join('language', folder, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        add = ''
        for i in range(2):
            if 'msgctxt "#%d"' % (SID + i) in t:
                continue
            esc = lambda s: s.replace('\\', '\\\\').replace('"', '\\"')
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (SID + i, esc(S['en_gb'][i]), '' if lang == 'en_gb' else esc(S[lang][i]))
        if add:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)


def labels():
    """Label texts that show an episode number -> through a variable; returns the variables' XML."""
    made = {}

    def var_for(prefix, pre, post, word):
        key = '%s|%s|%s|%s' % (prefix, pre, post, word)
        name = 'Aeon_EpN_' + hashlib.md5(key.encode('utf-8')).hexdigest()[:8]
        if name not in made:
            rng = '$INFO[%s.Property(aeon.ep.range)]' % prefix
            if word:
                plain, many = '$LOCALIZE[20359] $INFO[%s.Episode]' % prefix, '$LOCALIZE[20360] ' + rng
            elif pre is None:
                plain, many = '$INFO[%s.Episode]' % prefix, rng
            else:
                plain = '$INFO[%s.Episode,%s,%s]' % (prefix, pre, post)
                many = pre.replace('$LOCALIZE[20359]', '$LOCALIZE[20360]') + rng + post
            made[name] = ('\t<variable name="%s">\n\t\t<value condition="!String.IsEmpty(%s.Property(aeon.ep.range))">%s</value>\n'
                          '\t\t<value>%s</value>\n\t</variable>' % (name, prefix, many, plain))
        return '$VAR[%s]' % name

    def fix_label(text):
        if 'ChannelName' in text or 'aeon.ep.range' in text:
            return text
        text = re.sub(r'\$LOCALIZE\[20359\] \$INFO\[((?:Container\(\d+\)\.)?ListItem)\.Episode\]', lambda m: var_for(m.group(1), None, None, True), text)
        return EP.sub(lambda m: var_for(m.group(1), m.group(2), m.group(3), False), text)

    count = 0
    for name in sorted(os.listdir(D)):
        if not name.endswith('.xml') or name in SKIP:
            continue
        p = os.path.join(D, name)
        t = io.open(p, encoding='utf-8').read()
        if 'ListItem.Episode' not in t:
            continue
        new = re.sub(r'(<label2?>)(.*?)(</label2?>)', lambda m: m.group(1) + fix_label(m.group(2)) + m.group(3), t)
        if new != t:
            count += sum(1 for a, b in zip(re.findall(r'<label2?>.*?</label2?>', t), re.findall(r'<label2?>.*?</label2?>', new)) if a != b)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(new)
            ET.parse(p)
    return made, count


def epcodes(made):
    t = io.open(SUB, encoding='utf-8').read()
    n = 0
    for m in list(re.finditer(r'<variable name="Aeon_EpCode\w*">', t)):
        a = t.index(m.group(0))
        b = t.index('</variable>', a)
        block = t[a:b]
        first = re.search(r'<value condition="String\.IsEmpty\(((?:Container\(\d+\)\.)?ListItem)\.Episode\)"></value>', block)
        if not first or 'aeon.ep.code' in block:
            continue                                    # the player's variables: a playing item has no row to join
        p = first.group(1)
        block = block.replace(first.group(0), '<value condition="!String.IsEmpty(%s.Property(aeon.ep.code))">$INFO[%s.Property(aeon.ep.code)]</value>\n\t\t%s'
                              % (p, p, first.group(0)))
        t = t[:a] + block + t[b:]
        n += 1
    i = t.index('<includes>') + len('<includes>')
    t = t[:i] + '\n\t<!-- %s: an episode number that may be a joined row\'s range (helper ?info=episodes) -->\n%s\n' % (MARK, '\n'.join(made[k] for k in sorted(made))) + t[i:]
    io.open(SUB, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(SUB)
    return n


ROW = '''	<control type="group"><!-- row 9781 (%(m)s) -->
		<width>1100</width><height>70</height>
<control type="group"><left>41</left><top>0</top><visible>Control.HasFocus(9781)</visible>
				<animation type="Visible"><effect type="fade" start="0" end="100" time="150"/></animation>
				<include>FG_LandVisible</include>
				<animation type="Hidden"><effect type="fade" start="100" end="0" time="100"/></animation>
%(bar)s
			</control>
<control type="group"><left>160</left><top>0</top>
				<include content="Dlg_SkinRowChrome">
					<param name="id" value="9781"/><param name="label" value="%(label)s"/><param name="hint" value=""/><param name="labelTop" value="0"/><param name="labelH" value="70"/><param name="icon" value="aeon/icons/tv.png"/><param name="labelx" value="46"/>
				</include>
				<control type="button" id="9781">
					<onup>9780</onup><ondown>9700</ondown>
					<include>Dlg_SkinRowButton</include>
					<onback>9566</onback>
					<onleft>SetFocus(9566)</onleft>
					<onclick>Skin.ToggleSetting(aeon.ep.join)</onclick>
				</control>
%(switch)s
			</control>
	</control>'''


def row():
    t = io.open(SET, encoding='utf-8').read()
    # the switch of row 9776 (Media info from sidecars), with this row's id and setting
    a = t.index('<control type="group"><!-- row 9776 -->')
    b = t.index('\n\t</control>', t.index('<control type="button" id="9776">', a)) + len('\n\t</control>')
    old = t[a:b]
    bar = re.search(r'<control type="group"><left>41</left><top>0</top><visible>Control.HasFocus\(9776\)</visible>(.*?)\n\t\t\t</control>', old, re.S)
    bar_lines = '\n'.join(l for l in bar.group(1).split('\n') if '<control type="image">' in l)
    j = old.index('<onclick>Skin.ToggleSetting(aeon.mi.sidecar)</onclick>')
    j = old.index('</control>', j) + len('</control>')
    k = old.rindex('\n\t\t\t</control>')
    switch = old[j:k].strip('\n').replace('aeon.mi.sidecar', 'aeon.ep.join').replace('9776', '9781')
    assert 'aeon.ep.join' in switch and '9781' in switch
    new_row = ROW % {'m': MARK, 'bar': bar_lines.replace('9776', '9781'), 'label': A(0), 'switch': switch}
    c = t.index('<control type="group"><!-- row 9780')
    d = t.index('\n\t</control>', t.index('<control type="button" id="9780">', c)) + len('\n\t</control>')
    r9780 = t[c:d]
    r2 = r9780.replace('<onup>9776</onup><ondown>9700</ondown>', '<onup>9776</onup><ondown>9781</ondown>')
    assert r2 != r9780
    t = t[:c] + r2 + '\n' + new_row + t[d:]
    i = t.index('<control type="button" id="9700">')
    j = t.index('<onup>9780</onup>', i)
    assert j - i < 200
    t = t[:j] + '<onup>9781</onup>' + t[j + len('<onup>9780</onup>'):]
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(SET)
    s = io.open(INC, encoding='utf-8').read()
    old = '<value condition="Control.HasFocus(9780)">$ADDON[skin.aeon.fuse 32646]</value>'
    assert s.count(old) == 1
    s = s.replace(old, old + '\n\t\t<value condition="Control.HasFocus(9781)">%s</value><!-- %s -->' % (A(1), MARK))
    io.open(INC, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(INC)


def main():
    if MARK in io.open(SUB, encoding='utf-8').read():
        print('already')
        return
    strings()
    made, count = labels()
    n = epcodes(made)
    row()
    print('labels', count, 'variables', len(made), 'episode codes', n)


if __name__ == '__main__':
    main()
