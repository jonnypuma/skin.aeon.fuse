# -*- coding: utf-8 -*-
"""0.56.20 strings for Skin settings > Details > Media info from sidecars (32615) and its help line (32616), every
language. Safe to run again (an id already there is left alone)."""
import io
import os

S = {
    'en_gb': ('Media info from sidecars',
              'Off: only what Kodi\'s library knows (the chips above). On: also the source (UHD Remux, Blu-ray, WEB-DL, DVD...), the edition, the audio and subtitle tracks and the chapters, read from a mediainfo sidecar next to each video file: <name>.cmm_mediainfo.xml from Curator Media Manager (used first) or <name>-mediainfo.xml from tinyMediaManager. Without sidecars nothing extra shows.'),
    'cs_cz': ('Informace o médiu ze sidecar souborů',
              'Vypnuto: jen to, co zná knihovna Kodi (štítky výše). Zapnuto: také zdroj (UHD Remux, Blu-ray, WEB-DL, DVD...), edice, zvukové stopy, titulky a kapitoly ze souboru mediainfo vedle každého videa: <název>.cmm_mediainfo.xml z Curator Media Manager (má přednost) nebo <název>-mediainfo.xml z tinyMediaManager. Bez těchto souborů se nic navíc nezobrazí.'),
    'da_dk': ('Medieinfo fra sidecar-filer',
              'Fra: kun det Kodis bibliotek ved (mærkerne ovenfor). Til: også kilden (UHD Remux, Blu-ray, WEB-DL, DVD...), udgaven, lyd- og undertekstspor og kapitler fra en mediainfo-fil ved siden af hver videofil: <navn>.cmm_mediainfo.xml fra Curator Media Manager (bruges først) eller <navn>-mediainfo.xml fra tinyMediaManager. Uden disse filer vises intet ekstra.'),
    'de_de': ('Medieninfo aus Begleitdateien',
              'Aus: nur was Kodis Bibliothek weiß (die Chips oben). Ein: auch die Quelle (UHD Remux, Blu-ray, WEB-DL, DVD...), die Fassung, Ton- und Untertitelspuren und Kapitel aus einer Mediainfo-Datei neben jeder Videodatei: <Name>.cmm_mediainfo.xml von Curator Media Manager (zuerst) oder <Name>-mediainfo.xml von tinyMediaManager. Ohne diese Dateien erscheint nichts zusätzlich.'),
    'el_gr': ('Πληροφορίες μέσου από αρχεία sidecar',
              'Ανενεργό: μόνο όσα ξέρει η βιβλιοθήκη του Kodi (οι ετικέτες πάνω). Ενεργό: επίσης η πηγή (UHD Remux, Blu-ray, WEB-DL, DVD...), η έκδοση, τα κανάλια ήχου και υποτίτλων και τα κεφάλαια από ένα αρχείο mediainfo δίπλα σε κάθε βίντεο: <όνομα>.cmm_mediainfo.xml από το Curator Media Manager (πρώτο) ή <όνομα>-mediainfo.xml από το tinyMediaManager. Χωρίς αυτά τα αρχεία δεν εμφανίζεται τίποτα επιπλέον.'),
    'es_es': ('Información del medio desde archivos sidecar',
              'Desactivado: solo lo que sabe la biblioteca de Kodi (las etiquetas de arriba). Activado: también la fuente (UHD Remux, Blu-ray, WEB-DL, DVD...), la edición, las pistas de audio y subtítulos y los capítulos, leídos de un archivo mediainfo junto a cada vídeo: <nombre>.cmm_mediainfo.xml de Curator Media Manager (primero) o <nombre>-mediainfo.xml de tinyMediaManager. Sin esos archivos no se muestra nada más.'),
    'fi_fi': ('Mediatiedot sivutiedostoista',
              'Pois: vain se, mitä Kodin kirjasto tietää (yllä olevat merkit). Päällä: myös lähde (UHD Remux, Blu-ray, WEB-DL, DVD...), versio, ääni- ja tekstitysraidat sekä kappaleet jokaisen videotiedoston vieressä olevasta mediainfo-tiedostosta: <nimi>.cmm_mediainfo.xml (Curator Media Manager, ensisijainen) tai <nimi>-mediainfo.xml (tinyMediaManager). Ilman näitä tiedostoja mitään lisää ei näy.'),
    'fr_fr': ('Infos média des fichiers sidecar',
              'Désactivé : seulement ce que sait la bibliothèque de Kodi (les étiquettes ci-dessus). Activé : aussi la source (UHD Remux, Blu-ray, WEB-DL, DVD...), l\'édition, les pistes audio et de sous-titres et les chapitres, lus dans un fichier mediainfo à côté de chaque vidéo : <nom>.cmm_mediainfo.xml de Curator Media Manager (en premier) ou <nom>-mediainfo.xml de tinyMediaManager. Sans ces fichiers, rien de plus ne s\'affiche.'),
    'hu_hu': ('Médiainformáció kísérőfájlokból',
              'Ki: csak amit a Kodi könyvtára tud (a fenti címkék). Be: a forrás (UHD Remux, Blu-ray, WEB-DL, DVD...), a változat, a hang- és feliratsávok és a fejezetek is, minden videófájl melletti mediainfo-fájlból: <név>.cmm_mediainfo.xml a Curator Media Managertől (elsőként) vagy <név>-mediainfo.xml a tinyMediaManagertől. Ilyen fájlok nélkül semmi több nem jelenik meg.'),
    'it_it': ('Info media dai file sidecar',
              'Disattivato: solo ciò che sa la libreria di Kodi (le etichette sopra). Attivato: anche la sorgente (UHD Remux, Blu-ray, WEB-DL, DVD...), l\'edizione, le tracce audio e dei sottotitoli e i capitoli, letti da un file mediainfo accanto a ogni video: <nome>.cmm_mediainfo.xml di Curator Media Manager (per primo) o <nome>-mediainfo.xml di tinyMediaManager. Senza questi file non appare nulla in più.'),
    'ja_jp': ('サイドカーのメディア情報',
              'オフ: Kodi ライブラリの情報のみ（上のチップ）。オン: 各動画ファイルの隣にある mediainfo サイドカーから、ソース（UHD Remux、Blu-ray、WEB-DL、DVD など）、エディション、音声・字幕トラック、チャプターも表示します: Curator Media Manager の <名前>.cmm_mediainfo.xml（優先）または tinyMediaManager の <名前>-mediainfo.xml。サイドカーがなければ何も追加されません。'),
    'ko_kr': ('사이드카 파일의 미디어 정보',
              '끔: Kodi 라이브러리가 아는 정보만(위의 칩). 켬: 각 동영상 파일 옆의 mediainfo 사이드카에서 소스(UHD Remux, Blu-ray, WEB-DL, DVD...), 에디션, 오디오·자막 트랙, 챕터도 표시: Curator Media Manager의 <이름>.cmm_mediainfo.xml(우선) 또는 tinyMediaManager의 <이름>-mediainfo.xml. 사이드카가 없으면 추가로 표시되는 것이 없습니다.'),
    'nb_no': ('Medieinfo fra sidefiler',
              'Av: bare det Kodis bibliotek vet (merkene over). På: også kilden (UHD Remux, Blu-ray, WEB-DL, DVD...), utgaven, lyd- og undertekstspor og kapitler fra en mediainfo-fil ved siden av hver videofil: <navn>.cmm_mediainfo.xml fra Curator Media Manager (brukes først) eller <navn>-mediainfo.xml fra tinyMediaManager. Uten slike filer vises ikke noe ekstra.'),
    'nl_nl': ('Media-info uit sidecar-bestanden',
              'Uit: alleen wat de bibliotheek van Kodi weet (de labels hierboven). Aan: ook de bron (UHD Remux, Blu-ray, WEB-DL, DVD...), de editie, de audio- en ondertitelsporen en de hoofdstukken uit een mediainfo-bestand naast elk videobestand: <naam>.cmm_mediainfo.xml van Curator Media Manager (eerst) of <naam>-mediainfo.xml van tinyMediaManager. Zonder die bestanden verschijnt er niets extra.'),
    'pl_pl': ('Informacje o mediach z plików sidecar',
              'Wyłączone: tylko to, co wie biblioteka Kodi (etykiety powyżej). Włączone: także źródło (UHD Remux, Blu-ray, WEB-DL, DVD...), wydanie, ścieżki dźwiękowe i napisów oraz rozdziały z pliku mediainfo obok każdego wideo: <nazwa>.cmm_mediainfo.xml z Curator Media Manager (najpierw) lub <nazwa>-mediainfo.xml z tinyMediaManager. Bez tych plików nic więcej się nie pojawia.'),
    'pt_br': ('Informações de mídia de arquivos sidecar',
              'Desligado: apenas o que a biblioteca do Kodi sabe (as etiquetas acima). Ligado: também a origem (UHD Remux, Blu-ray, WEB-DL, DVD...), a edição, as faixas de áudio e legendas e os capítulos, lidos de um arquivo mediainfo ao lado de cada vídeo: <nome>.cmm_mediainfo.xml do Curator Media Manager (primeiro) ou <nome>-mediainfo.xml do tinyMediaManager. Sem esses arquivos nada a mais aparece.'),
    'pt_pt': ('Informação de multimédia de ficheiros sidecar',
              'Desligado: só o que a biblioteca do Kodi sabe (as etiquetas acima). Ligado: também a origem (UHD Remux, Blu-ray, WEB-DL, DVD...), a edição, as faixas de áudio e legendas e os capítulos, lidos de um ficheiro mediainfo ao lado de cada vídeo: <nome>.cmm_mediainfo.xml do Curator Media Manager (primeiro) ou <nome>-mediainfo.xml do tinyMediaManager. Sem esses ficheiros nada mais aparece.'),
    'ru_ru': ('Сведения о медиа из файлов sidecar',
              'Выкл.: только то, что знает библиотека Kodi (метки выше). Вкл.: также источник (UHD Remux, Blu-ray, WEB-DL, DVD...), издание, аудиодорожки, субтитры и главы из файла mediainfo рядом с каждым видео: <имя>.cmm_mediainfo.xml от Curator Media Manager (в первую очередь) или <имя>-mediainfo.xml от tinyMediaManager. Без этих файлов ничего дополнительного не показывается.'),
    'sv_se': ('Mediainfo från sidofiler',
              'Av: bara det Kodis bibliotek vet (märkena ovan). På: även källan (UHD Remux, Blu-ray, WEB-DL, DVD...), utgåvan, ljud- och undertextspår och kapitel från en mediainfo-fil bredvid varje videofil: <namn>.cmm_mediainfo.xml från Curator Media Manager (används först) eller <namn>-mediainfo.xml från tinyMediaManager. Utan sådana filer visas inget extra.'),
    'tr_tr': ('Yan dosyalardan medya bilgisi',
              'Kapalı: yalnızca Kodi kitaplığının bildikleri (yukarıdaki etiketler). Açık: her video dosyasının yanındaki mediainfo dosyasından kaynak (UHD Remux, Blu-ray, WEB-DL, DVD...), sürüm, ses ve altyazı parçaları ve bölümler de: Curator Media Manager\'dan <ad>.cmm_mediainfo.xml (öncelikli) veya tinyMediaManager\'dan <ad>-mediainfo.xml. Bu dosyalar yoksa fazladan bir şey görünmez.'),
    'uk_ua': ('Відомості про медіа з файлів sidecar',
              'Вимк.: лише те, що знає бібліотека Kodi (мітки вище). Увімк.: також джерело (UHD Remux, Blu-ray, WEB-DL, DVD...), видання, звукові доріжки, субтитри й розділи з файлу mediainfo поруч із кожним відео: <назва>.cmm_mediainfo.xml від Curator Media Manager (спершу) або <назва>-mediainfo.xml від tinyMediaManager. Без цих файлів нічого додаткового не показується.'),
    'zh_cn': ('来自旁路文件的媒体信息',
              '关：只显示 Kodi 媒体库已知的信息（上面的标签）。开：还从每个视频文件旁的 mediainfo 旁路文件读取来源（UHD Remux、Blu-ray、WEB-DL、DVD 等）、版本、音轨与字幕轨以及章节：Curator Media Manager 的 <名称>.cmm_mediainfo.xml（优先）或 tinyMediaManager 的 <名称>-mediainfo.xml。没有这些文件就不会显示额外内容。'),
    'zh_tw': ('來自旁路檔案的媒體資訊',
              '關：只顯示 Kodi 媒體庫已知的資訊（上方的標籤）。開：還從每個影片檔旁的 mediainfo 旁路檔讀取來源（UHD Remux、Blu-ray、WEB-DL、DVD 等）、版本、音軌與字幕軌以及章節：Curator Media Manager 的 <名稱>.cmm_mediainfo.xml（優先）或 tinyMediaManager 的 <名稱>-mediainfo.xml。沒有這些檔案就不會顯示額外內容。'),
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
        for sid, en, local in ((32615, EN[0], tr[0]), (32616, EN[1], tr[1])):
            if 'msgctxt "#%d"' % sid in t:
                continue
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), '' if lang == 'en_gb' else esc(local))
        if add:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)
    print('ok', len(os.listdir('language')))


if __name__ == '__main__':
    main()
