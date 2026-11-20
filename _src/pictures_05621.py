# -*- coding: utf-8 -*-
"""0.56.21: Pictures, from the approved canvas QGCfFk4L8RfaXGRipeK7ga (boards PicturesHome / PicturesWindow), in every
theme. Runs once (marker in Includes_Fused.xml).

Home > Pictures (like the Weather section: Aeon_LowBand / Aeon_LowSubSlide, cards dressed per theme):
  - the newest photo of the picture sources behind Home, darkened at the left;
  - "Newest folder": its name, the folder above it, how many photos and videos, the dates of its files, its four newest
    photos and "+N", the hint "OK plays the folder as a slideshow · Down for the folders";
  - under the menu "Folders, newest first": list 9311, 16:9 cards (plugin://script.aeon.helper/?info=picfolders,
    helper 0.3.98), the last card opens the Pictures window. OK on a card opens that folder.
  - OK on the Pictures menu item: a slideshow of the newest folder (swap.py picshow); the Pictures window when there
    is no picture yet. No source: "No pictures yet" and how to add one.
Pictures window: view 519 "Photos" (first in <views>): the list on the left (name; date taken / file date and size),
the photo panel on the right (the picture, its name, date / resolution / size, the camera and exposure, the photos
around it), a band with the folder, its number of items, the hint and the sort. The window's frame
(Misc_MediaWindow_L) hides its card / detail panel / count while 519 shows and moves the sub-nav (sort, slideshow,
randomise, view) above the list. A View button (Container.NextViewMode) in the sub-nav switches views."""
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.21 pictures'
FUSED = os.path.join('1080i', 'Includes_Fused.xml')
HOME = os.path.join('1080i', 'Includes_Aeon_Home.xml')
MISC = os.path.join('1080i', 'Includes_Misc.xml')
PICS = os.path.join('1080i', 'Includes_Aeon_Pics.xml')
MYPICS = os.path.join('1080i', 'MyPics.xml')

S = {   # 32629 .. 32643
    'en_gb': ('Newest folder', 'Folders, newest first', 'photos', 'photo', 'videos', 'video',
              'OK plays the folder as a slideshow · Down for the folders', 'All pictures', 'sources', 'source',
              'No pictures yet', 'Add a folder of photos as a picture source in the Pictures window. OK opens it.',
              'Photos', 'OK opens the photo · Up for sort, slideshow and view', 'View'),
    'cs_cz': ('Nejnovější složka', 'Složky, nejnovější první', 'fotek', 'fotka', 'videí', 'video',
              'OK spustí prezentaci složky · Dolů pro složky', 'Všechny obrázky', 'zdrojů', 'zdroj',
              'Zatím žádné obrázky', 'V okně Obrázky přidejte složku s fotkami jako zdroj obrázků. OK ho otevře.',
              'Fotky', 'OK otevře fotku · Nahoru pro řazení, prezentaci a zobrazení', 'Zobrazení'),
    'da_dk': ('Nyeste mappe', 'Mapper, nyeste først', 'fotos', 'foto', 'videoer', 'video',
              'OK viser mappen som diasshow · Ned for mapperne', 'Alle billeder', 'kilder', 'kilde',
              'Ingen billeder endnu', 'Tilføj en mappe med fotos som billedkilde i vinduet Billeder. OK åbner det.',
              'Fotos', 'OK åbner fotoet · Op for sortering, diasshow og visning', 'Visning'),
    'de_de': ('Neuester Ordner', 'Ordner, neueste zuerst', 'Fotos', 'Foto', 'Videos', 'Video',
              'OK zeigt den Ordner als Diashow · Runter für die Ordner', 'Alle Bilder', 'Quellen', 'Quelle',
              'Noch keine Bilder', 'Füge im Fenster Bilder einen Ordner mit Fotos als Bildquelle hinzu. OK öffnet es.',
              'Fotos', 'OK öffnet das Foto · Hoch für Sortierung, Diashow und Ansicht', 'Ansicht'),
    'el_gr': ('Νεότερος φάκελος', 'Φάκελοι, νεότεροι πρώτα', 'φωτογραφίες', 'φωτογραφία', 'βίντεο', 'βίντεο',
              'Το OK παίζει τον φάκελο ως προβολή · Κάτω για τους φακέλους', 'Όλες οι εικόνες', 'πηγές', 'πηγή',
              'Δεν υπάρχουν εικόνες ακόμη', 'Προσθέστε έναν φάκελο με φωτογραφίες ως πηγή εικόνων στο παράθυρο Εικόνες. Το OK το ανοίγει.',
              'Φωτογραφίες', 'Το OK ανοίγει τη φωτογραφία · Πάνω για ταξινόμηση, προβολή και εμφάνιση', 'Εμφάνιση'),
    'es_es': ('Carpeta más reciente', 'Carpetas, más recientes primero', 'fotos', 'foto', 'vídeos', 'vídeo',
              'OK reproduce la carpeta como presentación · Abajo para las carpetas', 'Todas las imágenes', 'fuentes', 'fuente',
              'Aún no hay imágenes', 'Añade una carpeta de fotos como fuente de imágenes en la ventana Imágenes. OK la abre.',
              'Fotos', 'OK abre la foto · Arriba para orden, presentación y vista', 'Vista'),
    'fi_fi': ('Uusin kansio', 'Kansiot, uusin ensin', 'kuvaa', 'kuva', 'videota', 'video',
              'OK näyttää kansion diaesityksenä · Alas kansioihin', 'Kaikki kuvat', 'lähdettä', 'lähde',
              'Ei vielä kuvia', 'Lisää kuvakansio kuvalähteeksi Kuvat-ikkunassa. OK avaa sen.',
              'Kuvat', 'OK avaa kuvan · Ylös lajitteluun, diaesitykseen ja näkymään', 'Näkymä'),
    'fr_fr': ('Dossier le plus récent', 'Dossiers, plus récents d’abord', 'photos', 'photo', 'vidéos', 'vidéo',
              'OK lance le diaporama du dossier · Bas pour les dossiers', 'Toutes les images', 'sources', 'source',
              'Pas encore d’images', 'Ajoutez un dossier de photos comme source d’images dans la fenêtre Images. OK l’ouvre.',
              'Photos', 'OK ouvre la photo · Haut pour le tri, le diaporama et la vue', 'Vue'),
    'hu_hu': ('Legújabb mappa', 'Mappák, legújabb elöl', 'fotó', 'fotó', 'videó', 'videó',
              'Az OK diavetítésként játssza a mappát · Le a mappákhoz', 'Összes kép', 'forrás', 'forrás',
              'Még nincsenek képek', 'A Képek ablakban add hozzá egy fotómappát képforrásként. Az OK megnyitja.',
              'Fotók', 'Az OK megnyitja a fotót · Fel a rendezéshez, diavetítéshez és nézethez', 'Nézet'),
    'it_it': ('Cartella più recente', 'Cartelle, più recenti prima', 'foto', 'foto', 'video', 'video',
              'OK riproduce la cartella come presentazione · Giù per le cartelle', 'Tutte le immagini', 'sorgenti', 'sorgente',
              'Ancora nessuna immagine', 'Aggiungi una cartella di foto come sorgente immagini nella finestra Immagini. OK la apre.',
              'Foto', 'OK apre la foto · Su per ordine, presentazione e vista', 'Vista'),
    'ja_jp': ('最新のフォルダー', 'フォルダー（新しい順）', '枚', '枚', '本の動画', '本の動画',
              'OK でフォルダーをスライドショー · 下でフォルダー', 'すべての画像', 'ソース', 'ソース',
              'まだ画像がありません', '画像ウィンドウで写真のフォルダーを画像ソースとして追加してください。OK で開きます。',
              '写真', 'OK で写真を開く · 上で並べ替え・スライドショー・表示', '表示'),
    'ko_kr': ('최신 폴더', '폴더, 최신 순', '장의 사진', '장의 사진', '개의 동영상', '개의 동영상',
              'OK로 폴더를 슬라이드쇼로 보기 · 아래로 폴더', '모든 사진', '개 소스', '개 소스',
              '아직 사진이 없습니다', '사진 창에서 사진 폴더를 사진 소스로 추가하세요. OK로 엽니다.',
              '사진', 'OK로 사진 열기 · 위로 정렬, 슬라이드쇼, 보기', '보기'),
    'nb_no': ('Nyeste mappe', 'Mapper, nyeste først', 'bilder', 'bilde', 'videoer', 'video',
              'OK viser mappen som lysbildefremvisning · Ned for mappene', 'Alle bilder', 'kilder', 'kilde',
              'Ingen bilder ennå', 'Legg til en mappe med bilder som bildekilde i Bilder-vinduet. OK åpner det.',
              'Bilder', 'OK åpner bildet · Opp for sortering, fremvisning og visning', 'Visning'),
    'nl_nl': ('Nieuwste map', 'Mappen, nieuwste eerst', "foto's", 'foto', "video's", 'video',
              'OK speelt de map af als diavoorstelling · Omlaag voor de mappen', 'Alle afbeeldingen', 'bronnen', 'bron',
              'Nog geen afbeeldingen', "Voeg in het venster Afbeeldingen een map met foto's toe als afbeeldingsbron. OK opent het.",
              "Foto's", 'OK opent de foto · Omhoog voor sorteren, diavoorstelling en weergave', 'Weergave'),
    'pl_pl': ('Najnowszy folder', 'Foldery, najnowsze najpierw', 'zdjęć', 'zdjęcie', 'filmów', 'film',
              'OK odtwarza folder jako pokaz slajdów · W dół do folderów', 'Wszystkie obrazy', 'źródeł', 'źródło',
              'Brak obrazów', 'Dodaj folder ze zdjęciami jako źródło obrazów w oknie Obrazy. OK je otwiera.',
              'Zdjęcia', 'OK otwiera zdjęcie · W górę do sortowania, pokazu i widoku', 'Widok'),
    'pt_br': ('Pasta mais recente', 'Pastas, mais recentes primeiro', 'fotos', 'foto', 'vídeos', 'vídeo',
              'OK mostra a pasta como apresentação · Abaixo para as pastas', 'Todas as imagens', 'fontes', 'fonte',
              'Ainda não há imagens', 'Adicione uma pasta de fotos como fonte de imagens na janela Imagens. OK a abre.',
              'Fotos', 'OK abre a foto · Acima para ordem, apresentação e exibição', 'Exibição'),
    'pt_pt': ('Pasta mais recente', 'Pastas, mais recentes primeiro', 'fotografias', 'fotografia', 'vídeos', 'vídeo',
              'OK mostra a pasta como apresentação · Baixo para as pastas', 'Todas as imagens', 'fontes', 'fonte',
              'Ainda sem imagens', 'Adicione uma pasta de fotografias como fonte de imagens na janela Imagens. OK abre-a.',
              'Fotografias', 'OK abre a fotografia · Cima para ordenar, apresentação e vista', 'Vista'),
    'ru_ru': ('Новейшая папка', 'Папки, сначала новые', 'фото', 'фото', 'видео', 'видео',
              'OK показывает папку слайд-шоу · Вниз к папкам', 'Все изображения', 'источников', 'источник',
              'Изображений пока нет', 'Добавьте папку с фото как источник изображений в окне «Изображения». OK открывает его.',
              'Фото', 'OK открывает фото · Вверх для сортировки, слайд-шоу и вида', 'Вид'),
    'sv_se': ('Nyaste mappen', 'Mappar, nyaste först', 'foton', 'foto', 'videor', 'video',
              'OK visar mappen som bildspel · Ned för mapparna', 'Alla bilder', 'källor', 'källa',
              'Inga bilder ännu', 'Lägg till en mapp med foton som bildkälla i fönstret Bilder. OK öppnar det.',
              'Foton', 'OK öppnar fotot · Upp för sortering, bildspel och vy', 'Vy'),
    'tr_tr': ('En yeni klasör', 'Klasörler, en yeni önce', 'fotoğraf', 'fotoğraf', 'video', 'video',
              'OK klasörü slayt gösterisi olarak oynatır · Klasörler için aşağı', 'Tüm resimler', 'kaynak', 'kaynak',
              'Henüz resim yok', 'Resimler penceresinde bir fotoğraf klasörünü resim kaynağı olarak ekleyin. OK açar.',
              'Fotoğraflar', 'OK fotoğrafı açar · Sıralama, slayt ve görünüm için yukarı', 'Görünüm'),
    'uk_ua': ('Найновіша тека', 'Теки, спершу нові', 'фото', 'фото', 'відео', 'відео',
              'OK показує теку слайд-шоу · Вниз до тек', 'Усі зображення', 'джерел', 'джерело',
              'Зображень ще немає', 'Додайте теку з фото як джерело зображень у вікні «Зображення». OK відкриває його.',
              'Фото', 'OK відкриває фото · Вгору для сортування, слайд-шоу та вигляду', 'Вигляд'),
    'zh_cn': ('最新文件夹', '文件夹（最新在前）', '张照片', '张照片', '个视频', '个视频',
              '确定以幻灯片播放文件夹 · 向下查看文件夹', '所有图片', '个来源', '个来源',
              '还没有图片', '在“图片”窗口中将照片文件夹添加为图片来源。确定将其打开。',
              '照片', '确定打开照片 · 向上进行排序、幻灯片和视图', '视图'),
    'zh_tw': ('最新資料夾', '資料夾（最新在前）', '張照片', '張照片', '部影片', '部影片',
              '確定以投影片播放資料夾 · 向下查看資料夾', '所有圖片', '個來源', '個來源',
              '還沒有圖片', '在「圖片」視窗中將照片資料夾新增為圖片來源。確定將其開啟。',
              '照片', '確定開啟照片 · 向上進行排序、投影片和檢視', '檢視'),
}
FIRST = 32629


def A(n):
    return '$ADDON[skin.aeon.fuse %d]' % (FIRST + n)


def strings():
    for folder in sorted(os.listdir('language')):
        lang = folder.replace('resource.language.', '')
        p = os.path.join('language', folder, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        tr = S[lang]
        assert len(tr) == len(S['en_gb']), lang
        add = ''
        for i, en in enumerate(S['en_gb']):
            sid = FIRST + i
            if 'msgctxt "#%d"' % sid in t:
                continue
            esc = lambda s: s.replace('\\', '\\\\').replace('"', '\\"')
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), '' if lang == 'en_gb' else esc(tr[i]))
        if add:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)


P = 'Window(Home).Property(aeon.pic.%s)'


def card_frame(focus_cond):
    """Favourites' 280x158 card at 16,14 (Aeon: white frame behind; Fused Glass: frosted, white ring in focus)."""
    o = []
    if focus_cond:
        o.append('<control type="image"><left>12</left><top>10</top><width>288</width><height>166</height><texture colordiffuse="aeon_white">common/white.png</texture><visible>%s + !$EXP[Aeon_FGlass]</visible></control>' % focus_cond)
    o.append('<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture border="16" colordiffuse="$VAR[FG_Frost]">fg/r16.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>')
    o.append('<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture colordiffuse="%s">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>' % ('ff1a1a1a' if focus_cond else '73000000'))
    o.append('<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" diffuse="fg/m280x158.png">$INFO[ListItem.Art(thumb)]</texture><visible>!String.IsEmpty(ListItem.Art(thumb))</visible></control>')
    o.append('<control type="image"><left>126</left><top>63</top><width>60</width><height>60</height><aspectratio>keep</aspectratio><texture colordiffuse="ccffffff">aeon/icons/image.png</texture><visible>String.IsEmpty(ListItem.Art(thumb))</visible></control>')
    if focus_cond:
        o.append('<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture border="16" colordiffuse="ffffffff">fg/ri16.png</texture><visible>%s + $EXP[Aeon_FGlass]</visible></control>' % focus_cond)
    a = '0.7' if not focus_cond else '1'
    o.append('<control type="label"><left>16</left><top>182</top><width>280</width><height>24</height><font>hm_cap_16</font><textcolor>%s</textcolor>'
             '<label>[UPPERCASE]$VAR[Aeon_PicCardSub][/UPPERCASE]</label></control>' % ('99ffffff' if not focus_cond else 'b3ffffff'))
    o.append('<control type="label"><left>16</left><top>206</top><width>280</width><height>32</height><font>hm_ui_24_semibold</font><textcolor>%s</textcolor>%s'
             '<label>$VAR[Aeon_PicCardName]</label></control>' % ('e6ffffff' if not focus_cond else 'ffffffff', '<scroll>true</scroll>' if focus_cond else ''))
    return '\n\t\t\t\t\t\t\t'.join(o)


def thumb(i, x):
    p = P % ('thumb%d' % i)
    return ('<control type="image"><left>%d</left><top>0</top><width>178</width><height>100</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m178x100.png">$INFO[%s]</texture><visible>!String.IsEmpty(%s) + $EXP[Aeon_FGlass]</visible></control>'
            '<control type="image"><left>%d</left><top>0</top><width>178</width><height>100</height><aspectratio>scale</aspectratio>'
            '<texture background="true">$INFO[%s]</texture><visible>!String.IsEmpty(%s) + !$EXP[Aeon_FGlass]</visible></control>' % (x, p, p, x, p, p))


HOME_INC = '''
	<!-- ===================================================== %(m)s: Pictures section of Home (all themes)
	     The newest folder of the picture sources and a row of folders, newest first (helper ?info=picfolders sets the
	     aeon.pic.* properties and fills list 9311). OK on the menu item: a slideshow of the newest folder. -->
	<expression name="Aeon_H_PicturesSec">String.IsEqual(Container(9000).ListItem.Label2,pictures)</expression>
	<variable name="Aeon_PicPhotos">
		<value condition="String.IsEqual(%(photos)s,1)">1 %(A3)s</value>
		<value condition="!String.IsEmpty(%(photos)s)">$INFO[%(photos)s] %(A2)s</value>
	</variable>
	<variable name="Aeon_PicVideos">
		<value condition="String.IsEqual(%(videos)s,1) + !String.IsEmpty(%(photos)s)">, 1 %(A5)s</value>
		<value condition="String.IsEqual(%(videos)s,1)">1 %(A5)s</value>
		<value condition="!String.IsEmpty(%(videos)s) + !String.IsEmpty(%(photos)s)">, $INFO[%(videos)s] %(A4)s</value>
		<value condition="!String.IsEmpty(%(videos)s)">$INFO[%(videos)s] %(A4)s</value>
	</variable>
	<variable name="Aeon_PicCardSub">
		<value condition="!String.IsEmpty(ListItem.Property(aeon.pic.all)) + String.IsEqual(%(sources)s,1)">1 %(A9)s</value>
		<value condition="!String.IsEmpty(ListItem.Property(aeon.pic.all))">$INFO[%(sources)s] %(A8)s</value>
		<value>$INFO[ListItem.Label2,,  ·  ]$VAR[Aeon_PicCardPhotos]$VAR[Aeon_PicCardVideos]</value>
	</variable>
	<variable name="Aeon_PicCardPhotos">
		<value condition="String.IsEqual(ListItem.Property(photos),1)">1 %(A3)s</value>
		<value condition="Integer.IsGreater(ListItem.Property(photos),1)">$INFO[ListItem.Property(photos)] %(A2)s</value>
	</variable>
	<variable name="Aeon_PicCardVideos">
		<value condition="String.IsEqual(ListItem.Property(videos),1) + Integer.IsGreater(ListItem.Property(photos),0)">, 1 %(A5)s</value>
		<value condition="String.IsEqual(ListItem.Property(videos),1)">1 %(A5)s</value>
		<value condition="Integer.IsGreater(ListItem.Property(videos),1) + Integer.IsGreater(ListItem.Property(photos),0)">, $INFO[ListItem.Property(videos)] %(A4)s</value>
		<value condition="Integer.IsGreater(ListItem.Property(videos),1)">$INFO[ListItem.Property(videos)] %(A4)s</value>
	</variable>
	<variable name="Aeon_PicCardName">
		<value condition="!String.IsEmpty(ListItem.Property(aeon.pic.all))">%(A7)s</value>
		<value>$INFO[ListItem.Label]</value>
	</variable>
	<include name="Aeon_H_PicturesBg">
		<control type="group">
			<visible>$EXP[Aeon_H_PicturesSec] + !$EXP[Aeon_H_SpotAny] + !String.IsEmpty(%(bg)s)</visible>
			<include>Anim_FadeVisible</include>
			<control type="image"><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>400</fadetime><texture background="true" colordiffuse="d9ffffff">$INFO[%(bg)s]</texture></control>
			<control type="image"><left>0</left><top>0</top><width>1300</width><height>1080</height><texture flipx="true" colordiffuse="b3000000">common/aeon_fade_left.png</texture></control>
		</control>
	</include>
	<include name="Aeon_H_Pictures">
		<control type="group">
			<include>Aeon_LowBand</include>
			<visible>$EXP[Aeon_H_PicturesSec] + [Control.HasFocus(9000) | Control.HasFocus(9311)] + !$EXP[Aeon_H_SpotAny]</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="150" time="300"/><effect type="slide" start="0,24" end="0,0" delay="150" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<!-- still walking the sources -->
			<control type="group">
				<visible>String.IsEmpty(%(done)s)</visible>
				<control type="image"><left>120</left><top>124</top><width>22</width><height>22</height><texture colordiffuse="b3ffffff">common/aeon_spinner.gif</texture><visible>!Skin.HasSetting(aeon.reducemotion)</visible></control>
				<control type="image"><left>120</left><top>124</top><width>22</width><height>22</height><texture colordiffuse="b3ffffff">common/aeon_spinner_still.png</texture><visible>Skin.HasSetting(aeon.reducemotion)</visible></control>
				<control type="label"><left>152</left><top>118</top><width>600</width><height>34</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[31952][/UPPERCASE]</label></control>
			</control>
			<!-- no picture found -->
			<control type="group">
				<visible>!String.IsEmpty(%(done)s) + !String.IsEmpty(%(none)s)</visible>
				<control type="label"><left>120</left><top>118</top><width>1100</width><height>28</height><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[1][/UPPERCASE]</label></control>
				<control type="label"><left>120</left><top>150</top><width>1300</width><height>84</height><aligny>center</aligny><font>hm_aeon_title_66</font><textcolor>ffffffff</textcolor><label>%(A10)s</label></control>
				<control type="textbox"><left>120</left><top>250</top><width>900</width><height>110</height><font>hm_body_24</font><textcolor>ccffffff</textcolor><label>%(A11)s</label></control>
			</control>
			<!-- the newest folder -->
			<control type="group">
				<visible>!String.IsEmpty(%(name)s)</visible>
				<control type="label"><left>120</left><top>118</top><width>1100</width><height>28</height><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]%(A0)s[/UPPERCASE]</label></control>
				<control type="label"><left>120</left><top>150</top><width>1300</width><height>84</height><aligny>center</aligny><font>hm_aeon_title_66</font><textcolor>ffffffff</textcolor><label>$INFO[%(name)s]</label></control>
				<control type="label"><left>120</left><top>240</top><width>1300</width><height>36</height><aligny>center</aligny><font>hm_ui_24_semibold</font><textcolor>e6ffffff</textcolor><label>$INFO[%(parent)s,,  ·  ]$VAR[Aeon_PicPhotos]$VAR[Aeon_PicVideos]$INFO[%(dates)s,  ·  ,]</label></control>
				<control type="group"><left>120</left><top>300</top>
					%(thumbs)s
					<control type="group"><left>760</left><top>0</top><visible>!String.IsEmpty(%(more)s)</visible>
						<control type="image"><left>0</left><top>0</top><width>178</width><height>100</height><texture border="16" colordiffuse="$VAR[FG_Frost]">fg/r16.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
						<control type="image"><left>0</left><top>0</top><width>178</width><height>100</height><texture colordiffuse="33ffffff">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>
						<control type="label"><left>0</left><top>0</top><width>178</width><height>100</height><align>center</align><aligny>center</aligny><font>hm_ui_26</font><textcolor>e6ffffff</textcolor><label>+$INFO[%(more)s]</label></control>
					</control>
				</control>
				<control type="label"><left>120</left><top>420</top><width>1300</width><height>30</height><aligny>center</aligny><font>hm_small_20</font><textcolor>a6ffffff</textcolor><label>%(A6)s</label></control>
			</control>
		</control>
		<!-- the folders, newest first, under the menu -->
		<control type="group">
			<include>Aeon_LowSubSlide</include>
			<visible>$EXP[Aeon_H_PicturesSec] + !$EXP[Aeon_H_SpotAny] + [Control.HasFocus(9000) | Control.HasFocus(9311)]</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="group">
				<include>Aeon_LowSubZoom</include>
				<control type="label"><left>120</left><top>772</top><width>800</width><height>26</height><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]%(A1)s[/UPPERCASE]</label><visible>!String.IsEmpty(%(name)s)</visible></control>
				<control type="list" id="9311">
					<left>104</left><top>790</top><width>1716</width><height>290</height>
					<orientation>horizontal</orientation>
					<scrolltime tween="cubic" easing="out">220</scrolltime>
					<onup>9000</onup>
					<onback>9000</onback>
					<itemlayout width="312" height="280">
						%(item)s
					</itemlayout>
					<focusedlayout width="312" height="280">
						%(focused)s
					</focusedlayout>
					<content target="pictures">plugin://script.aeon.helper/?info=picfolders</content>
				</control>
			</control>
		</control>
	</include>'''


def home():
    f = io.open(FUSED, encoding='utf-8').read()
    if MARK in f:
        return False
    a = f.index('\t<include name="Aeon_H_Weather">')
    b = f.index('\n\t</include>', a) + len('\n\t</include>')
    vals = {k: P % k for k in ('photos', 'videos', 'sources', 'bg', 'done', 'none', 'name', 'parent', 'dates', 'more')}
    vals.update({'A%d' % i: A(i) for i in range(15)})
    vals.update({'m': MARK, 'thumbs': '\n\t\t\t\t\t'.join(thumb(i + 1, i * 190) for i in range(4)),
                 'item': card_frame(''), 'focused': card_frame('Control.HasFocus(9311)')})
    f = f[:b] + HOME_INC % vals + f[b:]
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
    ET.parse(FUSED)

    h = io.open(HOME, encoding='utf-8').read()
    for old, new in (('\t\t<include>Aeon_H_WeatherBg</include>\n', '\t\t<include>Aeon_H_WeatherBg</include>\n\t\t<include>Aeon_H_PicturesBg</include><!-- %s -->\n' % MARK),
                     ('\t\t<include>Aeon_H_Weather</include>\n', '\t\t<include>Aeon_H_Weather</include>\n\t\t<include>Aeon_H_Pictures</include><!-- %s -->\n' % MARK),
                     ('+ !$EXP[Aeon_H_WeatherSec] + !$EXP[Aeon_H_FavSec]]] + !$EXP[Aeon_H_SpotAny] + !$EXP[Aeon_SP2Show]</visible>',
                      '+ !$EXP[Aeon_H_WeatherSec] + !$EXP[Aeon_H_PicturesSec] + !$EXP[Aeon_H_FavSec]]] + !$EXP[Aeon_H_SpotAny] + !$EXP[Aeon_SP2Show]</visible>'),
                     ('\t\t\t<ondown condition="$EXP[Aeon_H_WeatherSec] + !$EXP[Aeon_H_SpotAny] + Integer.IsGreater(Container(9306).NumItems,0)">SetFocus(9306)</ondown>\n',
                      '\t\t\t<ondown condition="$EXP[Aeon_H_WeatherSec] + !$EXP[Aeon_H_SpotAny] + Integer.IsGreater(Container(9306).NumItems,0)">SetFocus(9306)</ondown>\n'
                      '\t\t\t<ondown condition="$EXP[Aeon_H_PicturesSec] + !$EXP[Aeon_H_SpotAny] + Integer.IsGreater(Container(9311).NumItems,0)">SetFocus(9311)</ondown><!-- %s -->\n' % MARK),
                     ('+ ![$EXP[Aeon_H_WeatherSec] + Integer.IsGreater(Container(9306).NumItems,0)] + !$EXP[Aeon_H_SearchRecent]',
                      '+ ![$EXP[Aeon_H_WeatherSec] + Integer.IsGreater(Container(9306).NumItems,0)] + ![$EXP[Aeon_H_PicturesSec] + Integer.IsGreater(Container(9311).NumItems,0)] + !$EXP[Aeon_H_SearchRecent]')):
        assert h.count(old) == 1, old[:80]
        h = h.replace(old, new)
    old = '<label2>pictures</label2>\n\t\t\t\t\t<property name="icon">$INFO[Skin.String(aeon.icon.pictures)]</property>\n\t\t\t\t\t<onclick>ActivateWindow(Pictures)</onclick>'
    n = h.count(old)
    assert n == 24, n
    h = h.replace(old, '<label2>pictures</label2>\n\t\t\t\t\t<property name="icon">$INFO[Skin.String(aeon.icon.pictures)]</property>\n'
                       '\t\t\t\t\t<onclick condition="!String.IsEmpty(Window(Home).Property(aeon.pic.folder))">RunScript(script.aeon.helper,picshow)</onclick>'
                       '<onclick condition="String.IsEmpty(Window(Home).Property(aeon.pic.folder))">ActivateWindow(Pictures)</onclick>')
    io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)
    ET.parse(HOME)
    return True


# ------------------------------------------------------------------ the window
BAR = """<control type="image"><left>0</left><top>0</top><width>1000</width><height>64</height><texture border="20" colordiffuse="ffffffff">$VAR[Aeon_MenuRowTex]</texture><visible>%(F)s + !$EXP[Aeon_VGlass]</visible></control>
						<control type="image"><left>4</left><top>4</top><width>992</width><height>56</height><texture border="24" colordiffuse="$VAR[AG_Accent_L]">$VAR[Aeon_TexCard20]</texture><visible>%(F)s + $EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible></control>
						<control type="image"><left>12</left><top>4</top><width>976</width><height>56</height><texture border="20" colordiffuse="$VAR[AG_Accent_L]">$VAR[Aeon_MenuFocusRowTex]</texture><visible>%(F)s + $EXP[Aeon_FGlass]</visible></control>
						<control type="image"><left>0</left><top>63</top><width>1000</width><height>1</height><texture colordiffuse="18ffffff">common/white.png</texture><visible>!$EXP[Aeon_VGlass]</visible></control>"""
TEXT = """<control type="image"><left>28</left><top>16</top><width>32</width><height>32</height><aspectratio>keep</aspectratio><texture colordiffuse="%(ICON)s">$VAR[AeonP_RowIcon]</texture><visible>ListItem.IsFolder + %(C)s</visible></control>
						<control type="label"><left>76</left><top>0</top><width>500</width><height>64</height><aligny>center</aligny><font>%(FONT)s</font><textcolor>%(INK)s</textcolor><selectedcolor>%(INK)s</selectedcolor>%(SCROLL)s<label>$VAR[AG_RowLabel]</label><visible>ListItem.IsFolder + %(C)s</visible></control>
						<control type="label"><left>28</left><top>0</top><width>548</width><height>64</height><aligny>center</aligny><font>%(FONT)s</font><textcolor>%(INK)s</textcolor><selectedcolor>%(INK)s</selectedcolor>%(SCROLL)s<label>$VAR[AG_RowLabel]</label><visible>!ListItem.IsFolder + %(C)s</visible></control>
						<control type="label"><left>576</left><top>0</top><width>396</width><height>64</height><align>right</align><aligny>center</aligny><font>lb_small_20</font><textcolor>%(INK2)s</textcolor><selectedcolor>%(INK2)s</selectedcolor><label>$VAR[AeonP_RowFacts]</label><visible>%(C)s</visible></control>"""


def row(focused):
    plain = TEXT % {'ICON': 'ccffffff', 'FONT': 'lb_ui_24', 'INK': '$VAR[AG_Ink]', 'INK2': '$VAR[AG_Ink2]', 'SCROLL': '', 'C': '%s'}
    if not focused:
        return BAR % {'F': 'false'} + '\n\t\t\t\t\t\t' + plain % ('true', 'true', 'true', 'true')
    lit = TEXT % {'ICON': '$VAR[AG_OnAccent_L]', 'FONT': 'lb_ui_24_semibold', 'INK': '$VAR[AG_OnAccent_L]', 'INK2': '$VAR[AG_OnAccent_L]',
                  'SCROLL': '<scroll>true</scroll>', 'C': 'Control.HasFocus(519)'}
    off = plain % (('!Control.HasFocus(519)',) * 4)
    return BAR % {'F': 'Control.HasFocus(519)'} + '\n\t\t\t\t\t\t' + off + '\n\t\t\t\t\t\t' + lit


def nb(i, x):
    li = 'Container(519).ListItem(%d)' % i
    o = []
    o.append('<control type="image"><left>%d</left><top>0</top><width>128</width><height>72</height><aspectratio scalediffuse="false">scale</aspectratio>'
             '<texture background="true" diffuse="fg/m128x72.png">$INFO[%s.Art(thumb)]</texture><visible>!String.IsEmpty(%s.Art(thumb)) + $EXP[Aeon_FGlass]</visible></control>' % (x, li, li))
    o.append('<control type="image"><left>%d</left><top>0</top><width>128</width><height>72</height><aspectratio>scale</aspectratio>'
             '<texture background="true">$INFO[%s.Art(thumb)]</texture><visible>!String.IsEmpty(%s.Art(thumb)) + !$EXP[Aeon_FGlass]</visible></control>' % (x, li, li))
    if i == 0:
        o.append('<control type="image"><left>%d</left><top>0</top><width>128</width><height>72</height><texture border="12" colordiffuse="ffffffff">fg/ri12.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>' % x)
        o.append('<control type="image"><left>%d</left><top>-4</top><width>136</width><height>4</height><texture colordiffuse="ffffffff">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>' % (x - 4))
        o.append('<control type="image"><left>%d</left><top>72</top><width>136</width><height>4</height><texture colordiffuse="ffffffff">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>' % (x - 4))
        o.append('<control type="image"><left>%d</left><top>0</top><width>4</width><height>72</height><texture colordiffuse="ffffffff">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>' % (x - 4))
        o.append('<control type="image"><left>%d</left><top>0</top><width>4</width><height>72</height><texture colordiffuse="ffffffff">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>' % (x + 128))
    else:
        o.append('<control type="image"><left>%d</left><top>0</top><width>128</width><height>72</height><texture border="12" colordiffuse="80000000">fg/r12.png</texture><visible>!String.IsEmpty(%s.Art(thumb)) + $EXP[Aeon_FGlass]</visible></control>' % (x, li))
        o.append('<control type="image"><left>%d</left><top>0</top><width>128</width><height>72</height><texture colordiffuse="80000000">common/white.png</texture><visible>!String.IsEmpty(%s.Art(thumb)) + !$EXP[Aeon_FGlass]</visible></control>' % (x, li))
    return '\n\t\t\t\t\t'.join(o)


PICS_INC = '''
	<!-- ===================================================== %(m)s: view 519 "Photos" (canvas QGCfFk4L8RfaXGRipeK7ga,
	     board PicturesWindow): the list on the left, the photo panel on the right, the folder's band at the bottom.
	     The frame (Misc_MediaWindow_L, hide = Control.IsVisible(519)) keeps the top bar and moves the sub-nav above
	     the list. Every theme: Aeon flat, Aeon Glass glass card, Fused Glass frosted cards (highlight 12 px in). -->
	<variable name="AeonP_RowIcon">
		<value condition="ListItem.IsParentFolder">aeon/icons/back.png</value>
		<value>$INFO[ListItem.Icon]</value>
	</variable>
	<variable name="AeonP_RowX"><value condition="ListItem.IsFolder">76</value><value>28</value></variable>
	<variable name="AeonP_RowInk"><value condition="Control.HasFocus(519)">$VAR[AG_OnAccent_L]</value><value>$VAR[AG_Ink]</value></variable>
	<variable name="AeonP_RowInk2"><value condition="Control.HasFocus(519)">$VAR[AG_OnAccent_L]</value><value>$VAR[AG_Ink2]</value></variable>
	<variable name="AeonP_RowIconInk"><value condition="Control.HasFocus(519)">$VAR[AG_OnAccent_L]</value><value>ccffffff</value></variable>
	<variable name="AeonP_RowFont"><value condition="Control.HasFocus(519)">lb_ui_24_semibold</value><value>lb_ui_24</value></variable>
	<variable name="AeonP_RowFacts">
		<value condition="ListItem.IsFolder">$INFO[ListItem.Label2]</value>
		<value condition="!String.IsEmpty(ListItem.PictureDatetime)">$INFO[ListItem.PictureDatetime]$INFO[ListItem.Size,     ,]</value>
		<value>$INFO[ListItem.Date]$INFO[ListItem.Size,     ,]</value>
	</variable>
	<variable name="AeonP_Facts">
		<value condition="Container(519).ListItem.IsFolder">$INFO[Container(519).ListItem.Label2]</value>
		<value condition="!String.IsEmpty(Container(519).ListItem.PictureDatetime)">$INFO[Container(519).ListItem.PictureDatetime]$INFO[Container(519).ListItem.PictureResolution,  •  ,]$INFO[Container(519).ListItem.Size,  •  ,]</value>
		<value>$INFO[Container(519).ListItem.Date]$INFO[Container(519).ListItem.PictureResolution,  •  ,]$INFO[Container(519).ListItem.Size,  •  ,]</value>
	</variable>
	<variable name="AeonP_Cam">
		<value condition="String.IsEmpty(Container(519).ListItem.PictureCamMake) | String.StartsWith(Container(519).ListItem.PictureCamModel,Canon) | String.StartsWith(Container(519).ListItem.PictureCamModel,NIKON) | String.StartsWith(Container(519).ListItem.PictureCamModel,Nikon) | String.StartsWith(Container(519).ListItem.PictureCamModel,Samsung) | String.StartsWith(Container(519).ListItem.PictureCamModel,SAMSUNG) | String.StartsWith(Container(519).ListItem.PictureCamModel,Pixel) | String.StartsWith(Container(519).ListItem.PictureCamModel,Google)">$INFO[Container(519).ListItem.PictureCamModel]</value>
		<value>$INFO[Container(519).ListItem.PictureCamMake]$INFO[Container(519).ListItem.PictureCamModel, ,]</value>
	</variable>
	<include name="Aeon_519_View">
		<control type="group">
			<visible>Control.IsVisible(519)</visible>
			<include>Anim_VisibleFade</include>
			<control type="label"><left>1300</left><top>136</top><width>500</width><height>40</height><align>right</align><aligny>center</aligny><font>lb_small_20</font><textcolor>$VAR[AG_Ink2]</textcolor><label>$INFO[Container.CurrentItem,, / ]$INFO[Container.NumItems]</label></control>
			<!-- the list's card -->
			<control type="group"><left>90</left><top>196</top><width>1000</width><height>768</height><include>AG_Card_L</include></control>
			<control type="list" id="519">
				<left>90</left><top>196</top><width>1000</width><height>768</height>
				<onup>9000</onup>
				<ondown>noop</ondown>
				<onleft>noop</onleft>
				<onright>5190</onright>
				<pagecontrol>5190</pagecontrol>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<viewtype label="%(A12)s">list</viewtype>
				<itemlayout width="1000" height="64">
						%(row)s
				</itemlayout>
				<focusedlayout width="1000" height="64">
						%(rowf)s
				</focusedlayout>
			</control>
			<control type="scrollbar" id="5190">
				<left>1096</left><top>196</top><width>8</width><height>768</height>
				<texturesliderbackground colordiffuse="22ffffff">common/white.png</texturesliderbackground>
				<texturesliderbar colordiffuse="66ffffff">common/white.png</texturesliderbar>
				<texturesliderbarfocus colordiffuse="ffffffff">common/white.png</texturesliderbarfocus>
				<textureslidernib colordiffuse="66ffffff">common/white.png</textureslidernib>
				<textureslidernibfocus colordiffuse="ffffffff">common/white.png</textureslidernibfocus>
				<orientation>vertical</orientation>
				<showonepage>false</showonepage>
				<onleft>519</onleft><onright>noop</onright><onup>9000</onup><ondown>noop</ondown><onback>519</onback>
			</control>
			<control type="label"><left>130</left><top>240</top><width>920</width><height>40</height><font>lb_ui_24</font><textcolor>$VAR[AG_Ink2]</textcolor><label>$LOCALIZE[31230]</label><visible>Integer.IsEqual(Container.NumItems,0) + !Container.IsUpdating</visible></control>
			<!-- the photo panel -->
			<control type="group">
				<left>1130</left><top>196</top>
				<visible>Integer.IsGreater(Container.NumItems,0)</visible>
				<control type="image"><left>0</left><top>0</top><width>670</width><height>504</height><texture border="28" colordiffuse="$VAR[FG_Frost]">fg/r28.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
				<control type="image"><left>0</left><top>0</top><width>670</width><height>504</height><texture border="28" colordiffuse="$VAR[FG_Edge]">fg/e28.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
				<control type="image"><left>0</left><top>0</top><width>670</width><height>504</height><texture colordiffuse="4d000000">common/white.png</texture><visible>!$EXP[Aeon_VGlass]</visible></control><control type="image"><left>0</left><top>0</top><width>670</width><height>504</height><texture border="24" colordiffuse="66000000">$VAR[Aeon_TexCard20]</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible></control>
				<control type="image"><left>12</left><top>12</top><width>646</width><height>480</height><aspectratio>keep</aspectratio><fadetime>160</fadetime><texture background="true">$VAR[AeonP_PanelArt]</texture><visible>!Container(519).ListItem.IsParentFolder</visible></control>
				<control type="image"><left>295</left><top>212</top><width>80</width><height>80</height><aspectratio>keep</aspectratio><texture colordiffuse="99ffffff">aeon/icons/back.png</texture><visible>Container(519).ListItem.IsParentFolder</visible></control>
				<control type="label"><left>0</left><top>524</top><width>670</width><height>44</height><aligny>center</aligny><font>lb_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>$VAR[AeonP_PanelLabel]</label></control>
				<control type="label"><left>0</left><top>572</top><width>670</width><height>32</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>$VAR[AG_Ink]</textcolor><label>$VAR[AeonP_Facts]</label></control>
				<control type="label"><left>0</left><top>608</top><width>670</width><height>32</height><aligny>center</aligny><font>lb_ui_22</font><textcolor>$VAR[AG_Ink2]</textcolor><label>$VAR[AeonP_Cam]$INFO[Container(519).ListItem.PictureAperture,  •  f/,]$INFO[Container(519).ListItem.PictureExpTime,  •  ,]$INFO[Container(519).ListItem.PictureISO,  •  ISO ,]</label><visible>!Container(519).ListItem.IsFolder</visible></control>
				<control type="group"><left>0</left><top>664</top>
					%(nb)s
				</control>
			</control>
			<!-- the band: the folder, its items, the hint, the sort -->
			<control type="image"><left>0</left><top>976</top><width>1820</width><height>104</height><texture colordiffuse="ff121214">common/white.png</texture><visible>!$EXP[Aeon_VGlass]</visible></control>
			<control type="image"><left>0</left><top>976</top><width>1820</width><height>1</height><texture colordiffuse="1fffffff">common/white.png</texture><visible>!$EXP[Aeon_VGlass]</visible></control>
			<control type="image"><left>90</left><top>980</top><width>1710</width><height>88</height><texture border="24" colordiffuse="$VAR[FG_Frost]">fg/r24.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
			<control type="image"><left>90</left><top>980</top><width>1710</width><height>88</height><texture border="24" colordiffuse="$VAR[FG_Edge]">fg/e24.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
			<control type="image"><left>90</left><top>980</top><width>1710</width><height>88</height><texture border="24" colordiffuse="66000000">$VAR[Aeon_TexCard20]</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible></control>
			<control type="label"><left>120</left><top>986</top><width>1300</width><height>38</height><aligny>center</aligny><font>lb_ui_26_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]$INFO[Container.FolderName]$INFO[Container.NumItems,  •  , $LOCALIZE[31954]][/UPPERCASE]</label></control>
			<control type="label"><left>120</left><top>1026</top><width>1300</width><height>32</height><aligny>center</aligny><font>lb_small_20</font><textcolor>$VAR[AG_Ink2]</textcolor><label>%(A13)s</label></control>
			<control type="label"><left>1300</left><top>1026</top><width>470</width><height>32</height><align>right</align><aligny>center</aligny><font>lb_small_20</font><textcolor>$VAR[AG_Ink2]</textcolor><label>[UPPERCASE]$LOCALIZE[31010]: [B]$INFO[Container.SortMethod][/B][/UPPERCASE]</label></control>
		</control>
	</include>
	<variable name="AeonP_PanelLabel">
		<value condition="Container(519).ListItem.IsParentFolder">$LOCALIZE[31245]</value>
		<value>$INFO[Container(519).ListItem.Label]</value>
	</variable>
	<variable name="AeonP_PanelArt">
		<value condition="!String.IsEmpty(Container(519).ListItem.Art(thumb))">$INFO[Container(519).ListItem.Art(thumb)]</value>
		<value>$INFO[Container(519).ListItem.Icon]</value>
	</variable>
'''


def window():
    p = io.open(PICS, encoding='utf-8').read()
    if MARK in p:
        return
    vals = {'m': MARK, 'A12': A(12), 'A13': A(13), 'row': row(False).replace('\n\t\t\t\t\t\t', '\n\t\t\t\t\t\t'), 'rowf': row(True),
            'nb': '\n\t\t\t\t\t'.join(nb(i, (i + 2) * 136) for i in range(-2, 3))}
    p = p.replace('</includes>', PICS_INC % vals + '</includes>')
    io.open(PICS, 'w', encoding='utf-8', newline='\n').write(p)
    ET.parse(PICS)

    m = io.open(MISC, encoding='utf-8').read()
    a = m.index('\t<include name="Misc_MediaWindow_L">')
    b = m.index('\n\t</include>', a)
    seg = m[a:b]
    reps = [
        ('\t\t<param name="extra">Misc_None</param>\n', '\t\t<param name="extra">Misc_None</param>\n\t\t<param name="hide">false</param><!-- %s: true while a view draws its own layout (Pictures 519) -->\n\t\t<param name="subnav_w">1040</param>\n\t\t<param name="count">true</param>\n' % MARK),
        ('\t\t\t\t<height>848</height>\n\t\t\t\t<include>AG_Card_L</include>', '\t\t\t\t<height>848</height>\n\t\t\t\t<visible>!$PARAM[hide]</visible>\n\t\t\t\t<include>AG_Card_L</include>'),
        ('\t\t\t<include>AG_GenericDetail</include>\n', '\t\t\t<control type="group"><visible>!$PARAM[hide]</visible><include>AG_GenericDetail</include></control>\n'),
        ('\t\t\t\t<visible>$EXP[Aeon_VGlass]</visible>\n\t\t\t</control>\n\t\t\t<control type="grouplist" id="9000">',
         '\t\t\t\t<visible>$EXP[Aeon_VGlass] + !$PARAM[hide]</visible>\n\t\t\t</control>\n\t\t\t<control type="grouplist" id="9000">\n'
         '\t\t\t\t<animation effect="slide" end="-630,-72" time="0" condition="$PARAM[hide]">Conditional</animation>'),
        ('\t\t\t\t<width>1040</width>\n\t\t\t\t<height>subnav_h</height>\n\t\t\t\t<orientation>horizontal</orientation>', '\t\t\t\t<width>$PARAM[subnav_w]</width>\n\t\t\t\t<height>subnav_h</height>\n\t\t\t\t<orientation>horizontal</orientation>'),
        ('\t\t\t\t<label>$INFO[Container.CurrentItem,, $ADDON[skin.aeon.fuse 32285] ]$INFO[Container.NumItems]</label>\n',
         '\t\t\t\t<label>$INFO[Container.CurrentItem,, $ADDON[skin.aeon.fuse 32285] ]$INFO[Container.NumItems]</label>\n\t\t\t\t<visible>!$PARAM[hide] + $PARAM[count]</visible>\n'),
        ('\t\t\t\t<visible>Integer.IsEqual(Container.NumItems,0) + !Container.IsUpdating</visible>\n',
         '\t\t\t\t<visible>Integer.IsEqual(Container.NumItems,0) + !Container.IsUpdating + !$PARAM[hide]</visible>\n'),
    ]
    for old, new in reps:
        assert seg.count(old) == 1, old[:70]
        seg = seg.replace(old, new)
    m = m[:a] + seg + m[b:]
    old = '''		<include content="Misc_AddonButtons_L"><param name="kind" value="image"/></include>
	</include>'''
    new = '''		<include content="Misc_AddonButtons_L"><param name="kind" value="image"/></include>
		<include content="AG_SubNavButton_L"><!-- %s: the views (519 Photos, 516 cards, 50 list) -->
			<param name="id" value="6054"/>
			<param name="label" value="$INFO[Container.Viewmode]"/>
			<param name="onclick" value="Container.NextViewMode"/>
		</include>
	</include>''' % MARK
    assert m.count(old) == 1
    m = m.replace(old, new)
    old = '<param name="width" value="190"/>\n\t\t\t<param name="radiox" value="156"/>'      # Randomise, a little narrower
    assert m.count(old) == 1
    m = m.replace(old, '<param name="width" value="178"/>\n\t\t\t<param name="radiox" value="144"/>')
    io.open(MISC, 'w', encoding='utf-8', newline='\n').write(m)
    ET.parse(MISC)

    w = io.open(MYPICS, encoding='utf-8').read()
    for old, new in (('<views>516,50</views>', '<views>519,516,50</views>'),
                     ('\t\t\t<param name="extra" value="Misc_Extra_Pictures"/>\n', '\t\t\t<param name="extra" value="Misc_Extra_Pictures"/>\n\t\t\t<param name="hide" value="Control.IsVisible(519)"/>\n\t\t\t<param name="subnav_w" value="1080"/>\n\t\t\t<param name="count" value="false"/>\n'),
                     ('\t\t<include>Aeon_516_View</include>', '\t\t<include>Aeon_519_View</include><!-- %s -->\n\t\t<include>Aeon_516_View</include>' % MARK)):
        assert w.count(old) == 1, old
        w = w.replace(old, new)
    io.open(MYPICS, 'w', encoding='utf-8', newline='\n').write(w)
    ET.parse(MYPICS)


def ring12():
    from PIL import Image, ImageDraw
    out = os.path.join('media', 'fg', 'ri12.png')
    if os.path.exists(out):
        return
    k, size, r, w = 8, 40, 12, 3
    big = Image.new('L', (size * k, size * k), 0)
    d = ImageDraw.Draw(big)
    d.rounded_rectangle((0, 0, size * k - 1, size * k - 1), radius=r * k, fill=255)
    d.rounded_rectangle((w * k, w * k, size * k - 1 - w * k, size * k - 1 - w * k), radius=(r - w) * k, fill=0)
    a = big.resize((size, size), Image.LANCZOS)
    im = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    im.putalpha(a)
    im.save(out)


def main():
    ring12()
    strings()
    if home():
        window()
        print('ok')
    else:
        print('already')


if __name__ == '__main__':
    main()
