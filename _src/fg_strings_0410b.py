# -*- coding: utf-8 -*-
"""0.41.0 strings 32479-32486 (Fused Glass information screen): page names, file facts, cast photos option.
Run from the skin folder."""
import io
import os

EN = {
    32479: 'Overview',
    32480: 'File and season',
    32481: 'In this file',
    32482: 'File',
    32483: 'Size',
    32484: 'Playing on',
    32485: 'Cast photos in the information screen',
    32486: 'Fused Glass player: the information screen shows the cast as round photos with the name and the character under each, in one row you scroll through. Off: the names as chips.',
}
TR = {
    'cs_cz': ('Přehled', 'Soubor a řada', 'V tomto souboru', 'Soubor', 'Velikost', 'Přehrává se na', 'Fotky herců na informační obrazovce', 'Přehrávač Fused Glass: informační obrazovka ukáže herce jako kulaté fotky se jménem a postavou pod každou, v jedné řadě, kterou procházíte. Vypnuto: jména jako štítky.'),
    'da_dk': ('Oversigt', 'Fil og sæson', 'I denne fil', 'Fil', 'Størrelse', 'Afspilles på', 'Skuespillerfotos på informationsskærmen', 'Fused Glass-afspiller: informationsskærmen viser de medvirkende som runde fotos med navn og rolle under hvert, i én række du ruller igennem. Fra: navnene som mærker.'),
    'de_de': ('Übersicht', 'Datei und Staffel', 'In dieser Datei', 'Datei', 'Größe', 'Wiedergabe auf', 'Darstellerfotos im Infobildschirm', 'Fused-Glass-Player: Der Infobildschirm zeigt die Darsteller als runde Fotos mit Name und Rolle darunter, in einer Reihe zum Durchblättern. Aus: die Namen als Chips.'),
    'el_gr': ('Επισκόπηση', 'Αρχείο και σεζόν', 'Σε αυτό το αρχείο', 'Αρχείο', 'Μέγεθος', 'Αναπαραγωγή σε', 'Φωτογραφίες ηθοποιών στην οθόνη πληροφοριών', 'Πρόγραμμα αναπαραγωγής Fused Glass: η οθόνη πληροφοριών δείχνει τους ηθοποιούς ως στρογγυλές φωτογραφίες με το όνομα και τον ρόλο κάτω από την καθεμία, σε μία σειρά που κυλά. Ανενεργό: τα ονόματα ως ετικέτες.'),
    'es_es': ('Resumen', 'Archivo y temporada', 'En este archivo', 'Archivo', 'Tamaño', 'Reproduciendo en', 'Fotos del reparto en la pantalla de información', 'Reproductor Fused Glass: la pantalla de información muestra el reparto como fotos redondas con el nombre y el personaje debajo de cada una, en una fila que se desplaza. Desactivado: los nombres como etiquetas.'),
    'fi_fi': ('Yleiskatsaus', 'Tiedosto ja kausi', 'Tässä tiedostossa', 'Tiedosto', 'Koko', 'Toistetaan laitteella', 'Näyttelijäkuvat tietonäytössä', 'Fused Glass -soitin: tietonäyttö näyttää näyttelijät pyöreinä kuvina nimi ja rooli kunkin alla, yhdellä vieritettävällä rivillä. Pois: nimet tunnisteina.'),
    'fr_fr': ('Aperçu', 'Fichier et saison', 'Dans ce fichier', 'Fichier', 'Taille', 'Lecture sur', "Photos de la distribution dans l'écran d'informations", "Lecteur Fused Glass : l'écran d'informations montre la distribution en photos rondes avec le nom et le personnage sous chacune, sur une ligne que l'on fait défiler. Désactivé : les noms en étiquettes."),
    'hu_hu': ('Áttekintés', 'Fájl és évad', 'Ebben a fájlban', 'Fájl', 'Méret', 'Lejátszás ezen', 'Szereplőfotók az információs képernyőn', 'Fused Glass lejátszó: az információs képernyő kerek fotókként mutatja a szereplőket, alattuk a név és a szerep, egy görgethető sorban. Ki: a nevek címkékként.'),
    'it_it': ('Panoramica', 'File e stagione', 'In questo file', 'File', 'Dimensione', 'In riproduzione su', 'Foto del cast nella schermata informazioni', 'Lettore Fused Glass: la schermata informazioni mostra il cast come foto rotonde con il nome e il personaggio sotto ciascuna, in una fila da scorrere. Disattivato: i nomi come etichette.'),
    'ja_jp': ('概要', 'ファイルとシーズン', 'このファイル', 'ファイル', 'サイズ', '再生中の機器', '情報画面の出演者写真', 'Fused Glass プレーヤー：情報画面で出演者を丸い写真で表示し、その下に名前と役名を入れて、1 列でスクロールできます。オフ：名前をチップで表示。'),
    'ko_kr': ('개요', '파일과 시즌', '이 파일', '파일', '크기', '재생 기기', '정보 화면의 출연진 사진', 'Fused Glass 플레이어: 정보 화면에서 출연진을 둥근 사진으로 보여 주고 각 사진 아래에 이름과 배역을 표시하며, 한 줄로 스크롤합니다. 끔: 이름을 칩으로 표시.'),
    'nb_no': ('Oversikt', 'Fil og sesong', 'I denne filen', 'Fil', 'Størrelse', 'Spilles på', 'Skuespillerbilder på informasjonsskjermen', 'Fused Glass-spiller: informasjonsskjermen viser rollelisten som runde bilder med navn og rolle under hvert, i én rad du blar gjennom. Av: navnene som merker.'),
    'nl_nl': ('Overzicht', 'Bestand en seizoen', 'In dit bestand', 'Bestand', 'Grootte', 'Speelt op', 'Castfoto’s in het infoscherm', 'Fused Glass-speler: het infoscherm toont de cast als ronde foto’s met de naam en het personage eronder, in één rij om door te bladeren. Uit: de namen als labels.'),
    'pl_pl': ('Przegląd', 'Plik i sezon', 'W tym pliku', 'Plik', 'Rozmiar', 'Odtwarzane na', 'Zdjęcia obsady na ekranie informacji', 'Odtwarzacz Fused Glass: ekran informacji pokazuje obsadę jako okrągłe zdjęcia z imieniem i postacią pod każdym, w jednym przewijanym rzędzie. Wyłączone: imiona jako etykiety.'),
    'pt_br': ('Visão geral', 'Arquivo e temporada', 'Neste arquivo', 'Arquivo', 'Tamanho', 'Reproduzindo em', 'Fotos do elenco na tela de informações', 'Player Fused Glass: a tela de informações mostra o elenco como fotos redondas com o nome e o personagem embaixo de cada uma, em uma fileira que rola. Desligado: os nomes como etiquetas.'),
    'pt_pt': ('Resumo', 'Ficheiro e temporada', 'Neste ficheiro', 'Ficheiro', 'Tamanho', 'A reproduzir em', 'Fotos do elenco no ecrã de informações', 'Leitor Fused Glass: o ecrã de informações mostra o elenco como fotos redondas com o nome e a personagem por baixo de cada uma, numa fila que se percorre. Desligado: os nomes como etiquetas.'),
    'ru_ru': ('Обзор', 'Файл и сезон', 'В этом файле', 'Файл', 'Размер', 'Воспроизводится на', 'Фото актёров на экране информации', 'Плеер Fused Glass: экран информации показывает актёров круглыми фото с именем и ролью под каждым, в одном прокручиваемом ряду. Выкл.: имена ярлыками.'),
    'sv_se': ('Översikt', 'Fil och säsong', 'I den här filen', 'Fil', 'Storlek', 'Spelas på', 'Skådespelarfoton på informationsskärmen', 'Fused Glass-spelaren: informationsskärmen visar rollistan som runda foton med namn och roll under varje, i en rad du bläddrar i. Av: namnen som etiketter.'),
    'tr_tr': ('Genel bakış', 'Dosya ve sezon', 'Bu dosyada', 'Dosya', 'Boyut', 'Oynatıldığı yer', 'Bilgi ekranında oyuncu fotoğrafları', 'Fused Glass oynatıcı: bilgi ekranı oyuncuları her birinin altında adı ve karakteriyle yuvarlak fotoğraflar olarak, kaydırılan tek bir sırada gösterir. Kapalı: adlar etiket olarak.'),
    'uk_ua': ('Огляд', 'Файл і сезон', 'У цьому файлі', 'Файл', 'Розмір', 'Відтворюється на', 'Фото акторів на екрані інформації', 'Програвач Fused Glass: екран інформації показує акторів круглими фото з іменем і роллю під кожним, в одному прокручуваному ряду. Вимк.: імена ярликами.'),
    'zh_cn': ('概览', '文件与季', '此文件', '文件', '大小', '播放设备', '信息页显示演员照片', 'Fused Glass 播放器：信息页以圆形照片显示演员，每张照片下有姓名和角色，排成一行可滚动。关闭：以标签显示姓名。'),
    'zh_tw': ('概覽', '檔案與季', '此檔案', '檔案', '大小', '播放裝置', '資訊頁顯示演員照片', 'Fused Glass 播放器：資訊頁以圓形照片顯示演員，每張照片下有姓名和角色，排成一列可捲動。關閉：以標籤顯示姓名。'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32479"' in t:
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
print('strings 32479-32486 added in %d languages' % done)
