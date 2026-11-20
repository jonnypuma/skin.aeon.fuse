# -*- coding: utf-8 -*-
"""0.45.1 strings, part 2: the screensaver's new slides (skin 32556-32558, screensaver.aeon.fuse 32006-32008) and the
Player row "Save lyrics next to the song" (32559-32560). Run from the skin folder."""
import io
import os

SKIN = {
    32556: 'In cinemas now',
    32557: 'Airing today',
    32558: 'Airing tomorrow',
    32559: 'Save lyrics next to the song',
    32560: 'Lyrics that CU LRC Lyrics finds are also saved as a file next to the song (.lrc or .txt), so they are there next time and for other players. The music folder must be writable.',
}
SAVER = {
    32006: 'Show a film in the cinemas now',
    32007: 'Show what airs today (Planner)',
    32008: 'Show what airs tomorrow (Planner)',
}
# skin 32556-32560, then screensaver 32006-32008
TR = {
    'cs_cz': ('Nyní v kinech', 'Vysílá se dnes', 'Vysílá se zítra', 'Ukládat texty vedle skladby',
              'Texty, které najde CU LRC Lyrics, se uloží i jako soubor vedle skladby (.lrc nebo .txt), takže budou příště k dispozici i pro jiné přehrávače. Do složky s hudbou musí jít zapisovat.',
              'Zobrazit film, který je nyní v kinech', 'Zobrazit, co se vysílá dnes (Plánovač)', 'Zobrazit, co se vysílá zítra (Plánovač)'),
    'da_dk': ('I biografen nu', 'Sendes i dag', 'Sendes i morgen', 'Gem sangtekster ved siden af sangen',
              'Sangtekster, som CU LRC Lyrics finder, gemmes også som en fil ved siden af sangen (.lrc eller .txt), så de er der næste gang og for andre afspillere. Musikmappen skal være skrivbar.',
              'Vis en film, der går i biografen nu', 'Vis hvad der sendes i dag (Planlægger)', 'Vis hvad der sendes i morgen (Planlægger)'),
    'de_de': ('Jetzt im Kino', 'Läuft heute', 'Läuft morgen', 'Songtexte neben dem Lied speichern',
              'Songtexte, die CU LRC Lyrics findet, werden auch als Datei neben dem Lied gespeichert (.lrc oder .txt), damit sie beim nächsten Mal und für andere Player da sind. Der Musikordner muss beschreibbar sein.',
              'Einen Film zeigen, der jetzt im Kino läuft', 'Zeigen, was heute läuft (Planer)', 'Zeigen, was morgen läuft (Planer)'),
    'el_gr': ('Τώρα στους κινηματογράφους', 'Προβάλλεται σήμερα', 'Προβάλλεται αύριο', 'Αποθήκευση στίχων δίπλα στο τραγούδι',
              'Οι στίχοι που βρίσκει το CU LRC Lyrics αποθηκεύονται και ως αρχείο δίπλα στο τραγούδι (.lrc ή .txt), ώστε να υπάρχουν την επόμενη φορά και για άλλες εφαρμογές. Ο φάκελος μουσικής πρέπει να είναι εγγράψιμος.',
              'Εμφάνιση ταινίας που παίζεται τώρα στους κινηματογράφους', 'Εμφάνιση όσων προβάλλονται σήμερα (Πρόγραμμα)', 'Εμφάνιση όσων προβάλλονται αύριο (Πρόγραμμα)'),
    'es_es': ('Ahora en cines', 'Se emite hoy', 'Se emite mañana', 'Guardar letras junto a la canción',
              'Las letras que encuentra CU LRC Lyrics también se guardan como archivo junto a la canción (.lrc o .txt), para que estén ahí la próxima vez y para otros reproductores. La carpeta de música debe admitir escritura.',
              'Mostrar una película que está ahora en cines', 'Mostrar lo que se emite hoy (Planificador)', 'Mostrar lo que se emite mañana (Planificador)'),
    'fi_fi': ('Nyt elokuvateattereissa', 'Tulee tänään', 'Tulee huomenna', 'Tallenna sanoitukset kappaleen viereen',
              'CU LRC Lyricsin löytämät sanoitukset tallennetaan myös tiedostona kappaleen viereen (.lrc tai .txt), jolloin ne ovat tallessa seuraavalla kerralla ja muille soittimille. Musiikkikansioon on voitava kirjoittaa.',
              'Näytä elokuva, joka on nyt teattereissa', 'Näytä, mitä tulee tänään (Suunnittelija)', 'Näytä, mitä tulee huomenna (Suunnittelija)'),
    'fr_fr': ('Actuellement au cinéma', "Diffusé aujourd'hui", 'Diffusé demain', 'Enregistrer les paroles à côté du morceau',
              "Les paroles trouvées par CU LRC Lyrics sont aussi enregistrées dans un fichier à côté du morceau (.lrc ou .txt), pour la prochaine fois et pour d'autres lecteurs. Le dossier de musique doit être accessible en écriture.",
              'Afficher un film actuellement au cinéma', "Afficher ce qui est diffusé aujourd'hui (Planning)", 'Afficher ce qui est diffusé demain (Planning)'),
    'hu_hu': ('Most a mozikban', 'Ma adásban', 'Holnap adásban', 'Dalszövegek mentése a dal mellé',
              'A CU LRC Lyrics által talált dalszövegek fájlként is mentésre kerülnek a dal mellé (.lrc vagy .txt), így legközelebb és más lejátszóknak is megvannak. A zenemappának írhatónak kell lennie.',
              'Egy most a mozikban futó film megjelenítése', 'A ma adásba kerülők megjelenítése (Tervező)', 'A holnap adásba kerülők megjelenítése (Tervező)'),
    'it_it': ('Ora al cinema', 'In onda oggi', 'In onda domani', 'Salva i testi accanto al brano',
              'I testi trovati da CU LRC Lyrics vengono salvati anche come file accanto al brano (.lrc o .txt), così ci saranno la prossima volta e per altri lettori. La cartella della musica deve essere scrivibile.',
              'Mostra un film ora al cinema', 'Mostra cosa va in onda oggi (Planner)', 'Mostra cosa va in onda domani (Planner)'),
    'ja_jp': ('上映中', '今日放送', '明日放送', '歌詞を曲の隣に保存',
              'CU LRC Lyrics が見つけた歌詞を曲ファイルの隣にもファイル (.lrc または .txt) として保存し、次回や他のプレーヤーでも使えるようにします。音楽フォルダーに書き込める必要があります。',
              '上映中の映画を表示', '今日放送されるものを表示 (プランナー)', '明日放送されるものを表示 (プランナー)'),
    'ko_kr': ('현재 상영작', '오늘 방영', '내일 방영', '가사를 노래 옆에 저장',
              'CU LRC Lyrics가 찾은 가사를 노래 파일 옆에도 파일(.lrc 또는 .txt)로 저장하여 다음에도, 다른 플레이어에서도 쓸 수 있게 합니다. 음악 폴더에 쓰기가 가능해야 합니다.',
              '현재 상영 중인 영화 표시', '오늘 방영되는 것 표시 (플래너)', '내일 방영되는 것 표시 (플래너)'),
    'nb_no': ('På kino nå', 'Sendes i dag', 'Sendes i morgen', 'Lagre sangtekster ved siden av sangen',
              'Sangtekster som CU LRC Lyrics finner, lagres også som en fil ved siden av sangen (.lrc eller .txt), slik at de er der neste gang og for andre spillere. Musikkmappen må være skrivbar.',
              'Vis en film som går på kino nå', 'Vis hva som sendes i dag (Planlegger)', 'Vis hva som sendes i morgen (Planlegger)'),
    'nl_nl': ('Nu in de bioscoop', 'Vandaag te zien', 'Morgen te zien', 'Songteksten naast het nummer opslaan',
              'Songteksten die CU LRC Lyrics vindt, worden ook als bestand naast het nummer opgeslagen (.lrc of .txt), zodat ze er de volgende keer en voor andere spelers zijn. In de muziekmap moet geschreven kunnen worden.',
              'Een film tonen die nu in de bioscoop draait', 'Tonen wat vandaag uitkomt (Planner)', 'Tonen wat morgen uitkomt (Planner)'),
    'pl_pl': ('Teraz w kinach', 'Emisja dziś', 'Emisja jutro', 'Zapisuj teksty obok utworu',
              'Teksty znalezione przez CU LRC Lyrics są też zapisywane jako plik obok utworu (.lrc lub .txt), aby były dostępne następnym razem i dla innych odtwarzaczy. Folder z muzyką musi być zapisywalny.',
              'Pokaż film, który jest teraz w kinach', 'Pokaż, co ma emisję dziś (Planer)', 'Pokaż, co ma emisję jutro (Planer)'),
    'pt_br': ('Agora nos cinemas', 'No ar hoje', 'No ar amanhã', 'Salvar letras ao lado da música',
              'As letras encontradas pelo CU LRC Lyrics também são salvas como arquivo ao lado da música (.lrc ou .txt), para estarem lá na próxima vez e para outros players. A pasta de músicas precisa permitir gravação.',
              'Mostrar um filme agora nos cinemas', 'Mostrar o que vai ao ar hoje (Planejador)', 'Mostrar o que vai ao ar amanhã (Planejador)'),
    'pt_pt': ('Agora nos cinemas', 'Em exibição hoje', 'Em exibição amanhã', 'Guardar letras junto da música',
              'As letras encontradas pelo CU LRC Lyrics também são guardadas como ficheiro junto da música (.lrc ou .txt), para estarem lá da próxima vez e para outros leitores. A pasta de música tem de permitir escrita.',
              'Mostrar um filme agora nos cinemas', 'Mostrar o que é exibido hoje (Planeador)', 'Mostrar o que é exibido amanhã (Planeador)'),
    'ru_ru': ('Сейчас в кино', 'Выходит сегодня', 'Выходит завтра', 'Сохранять тексты рядом с песней',
              'Тексты, найденные CU LRC Lyrics, также сохраняются файлом рядом с песней (.lrc или .txt), чтобы они были под рукой в следующий раз и для других плееров. Папка с музыкой должна быть доступна для записи.',
              'Показывать фильм, который сейчас в кино', 'Показывать то, что выходит сегодня (Планировщик)', 'Показывать то, что выходит завтра (Планировщик)'),
    'sv_se': ('På bio nu', 'Sänds i dag', 'Sänds i morgon', 'Spara låttexter bredvid låten',
              'Låttexter som CU LRC Lyrics hittar sparas också som en fil bredvid låten (.lrc eller .txt), så att de finns där nästa gång och för andra spelare. Musikmappen måste vara skrivbar.',
              'Visa en film som går på bio nu', 'Visa vad som sänds i dag (Planerare)', 'Visa vad som sänds i morgon (Planerare)'),
    'tr_tr': ('Şimdi sinemalarda', 'Bugün yayında', 'Yarın yayında', 'Şarkı sözlerini şarkının yanına kaydet',
              'CU LRC Lyrics\'in bulduğu sözler şarkının yanına dosya olarak da kaydedilir (.lrc veya .txt); böylece bir dahaki sefere ve diğer oynatıcılar için hazır olur. Müzik klasörü yazılabilir olmalıdır.',
              'Şimdi sinemalarda olan bir filmi göster', 'Bugün yayınlananları göster (Planlayıcı)', 'Yarın yayınlananları göster (Planlayıcı)'),
    'uk_ua': ('Зараз у кіно', 'Виходить сьогодні', 'Виходить завтра', 'Зберігати тексти поруч із піснею',
              'Тексти, знайдені CU LRC Lyrics, також зберігаються файлом поруч із піснею (.lrc або .txt), щоб вони були наступного разу й для інших плеєрів. Тека з музикою має бути доступна для запису.',
              'Показувати фільм, що зараз у кіно', 'Показувати те, що виходить сьогодні (Планувальник)', 'Показувати те, що виходить завтра (Планувальник)'),
    'zh_cn': ('正在上映', '今天播出', '明天播出', '将歌词保存在歌曲旁边',
              'CU LRC Lyrics 找到的歌词也会以文件 (.lrc 或 .txt) 保存在歌曲旁边，下次和其他播放器都能用。音乐文件夹必须可写。',
              '显示一部正在上映的电影', '显示今天播出的内容（计划表）', '显示明天播出的内容（计划表）'),
    'zh_tw': ('正在上映', '今天播出', '明天播出', '將歌詞儲存在歌曲旁邊',
              'CU LRC Lyrics 找到的歌詞也會以檔案 (.lrc 或 .txt) 儲存在歌曲旁邊，下次和其他播放器都能使用。音樂資料夾必須可寫入。',
              '顯示一部正在上映的電影', '顯示今天播出的內容（計劃表）', '顯示明天播出的內容（計劃表）'),
}


def add(folder, strings, offset, first):
    done = 0
    for d in sorted(os.listdir(folder)):
        lang = d.replace('resource.language.', '')
        p = os.path.join(folder, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        if 'msgctxt "#%d"' % first in t:
            continue
        tr = TR.get(lang)
        assert tr or lang == 'en_gb', lang
        t = t.rstrip('\n') + '\n'
        for i, ident in enumerate(sorted(strings)):
            msgid = strings[ident].replace('"', '\\"')
            msgstr = '' if lang == 'en_gb' else tr[offset + i].replace('"', '\\"')
            t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        done += 1
    return done


print('skin', add('language', SKIN, 0, 32556), 'languages')
print('screensaver', add(os.path.join('..', 'screensaver.aeon.fuse', 'resources', 'language'), SAVER, 5, 32006), 'languages')
