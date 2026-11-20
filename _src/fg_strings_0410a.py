# -*- coding: utf-8 -*-
"""0.41.0 strings 32476-32478 (Fused Glass player card): Clearlogo in Now playing (label + help), Live (badge).
Run from the skin folder."""
import io
import os

EN = {
    32476: 'Clearlogo in Now playing',
    32477: 'Live',
    32478: 'Fused Glass player: the clearlogo of the show or film in the Now playing pill at the top left, instead of its title. Off: the title.',
}
TR = {
    'cs_cz': ('Clearlogo v Právě hraje', 'Živě', 'Přehrávač Fused Glass: clearlogo seriálu nebo filmu v kapsli Právě hraje vlevo nahoře místo názvu. Vypnuto: název.'),
    'da_dk': ('Clearlogo i Afspilles nu', 'Direkte', 'Fused Glass-afspiller: clearlogoet for serien eller filmen i pillen Afspilles nu øverst til venstre i stedet for titlen. Fra: titlen.'),
    'de_de': ('Clearlogo bei Aktuelle Wiedergabe', 'Live', 'Fused-Glass-Player: das Clearlogo der Serie oder des Films in der Kapsel „Aktuelle Wiedergabe“ oben links statt des Titels. Aus: der Titel.'),
    'el_gr': ('Clearlogo στο Αναπαράγεται τώρα', 'Ζωντανά', 'Πρόγραμμα αναπαραγωγής Fused Glass: το clearlogo της σειράς ή της ταινίας στην κάψουλα «Αναπαράγεται τώρα» πάνω αριστερά, αντί για τον τίτλο. Ανενεργό: ο τίτλος.'),
    'es_es': ('Clearlogo en Reproduciendo', 'En directo', 'Reproductor Fused Glass: el clearlogo de la serie o la película en la píldora Reproduciendo, arriba a la izquierda, en lugar del título. Desactivado: el título.'),
    'fi_fi': ('Clearlogo Nyt toistetaan -kohdassa', 'Suora', 'Fused Glass -soitin: sarjan tai elokuvan clearlogo Nyt toistetaan -pillerissä vasemmalla ylhäällä nimen sijaan. Pois: nimi.'),
    'fr_fr': ('Clearlogo dans Lecture en cours', 'Direct', 'Lecteur Fused Glass : le clearlogo de la série ou du film dans la pastille Lecture en cours, en haut à gauche, au lieu du titre. Désactivé : le titre.'),
    'hu_hu': ('Clearlogo a Most játszott elemben', 'Élő', 'Fused Glass lejátszó: a sorozat vagy a film clearlogója a bal felső Most játszott kapszulában a cím helyett. Ki: a cím.'),
    'it_it': ('Clearlogo in In riproduzione', 'Diretta', 'Lettore Fused Glass: il clearlogo della serie o del film nella pillola In riproduzione in alto a sinistra, al posto del titolo. Disattivato: il titolo.'),
    'ja_jp': ('再生中にクリアロゴ', 'ライブ', 'Fused Glass プレーヤー：左上の「再生中」ピルに、タイトルの代わりに番組または映画のクリアロゴを表示します。オフ：タイトル。'),
    'ko_kr': ('재생 중에 클리어로고', '생방송', 'Fused Glass 플레이어: 왼쪽 위 재생 중 알약에 제목 대신 프로그램이나 영화의 클리어로고를 표시합니다. 끔: 제목.'),
    'nb_no': ('Clearlogo i Spilles nå', 'Direkte', 'Fused Glass-spiller: clearlogoen til serien eller filmen i pillen Spilles nå øverst til venstre i stedet for tittelen. Av: tittelen.'),
    'nl_nl': ('Clearlogo bij Speelt nu', 'Live', 'Fused Glass-speler: het clearlogo van de serie of film in de pil Speelt nu linksboven, in plaats van de titel. Uit: de titel.'),
    'pl_pl': ('Clearlogo w Teraz odtwarzane', 'Na żywo', 'Odtwarzacz Fused Glass: clearlogo serialu lub filmu w kapsułce Teraz odtwarzane w lewym górnym rogu zamiast tytułu. Wyłączone: tytuł.'),
    'pt_br': ('Clearlogo em Reproduzindo', 'Ao vivo', 'Player Fused Glass: o clearlogo da série ou do filme na pílula Reproduzindo, no canto superior esquerdo, em vez do título. Desligado: o título.'),
    'pt_pt': ('Clearlogo em A reproduzir', 'Direto', 'Leitor Fused Glass: o clearlogo da série ou do filme na pílula A reproduzir, no canto superior esquerdo, em vez do título. Desligado: o título.'),
    'ru_ru': ('Clearlogo в «Сейчас играет»', 'Прямой эфир', 'Плеер Fused Glass: clearlogo сериала или фильма в капсуле «Сейчас играет» слева вверху вместо названия. Выкл.: название.'),
    'sv_se': ('Clearlogo i Spelas nu', 'Live', 'Fused Glass-spelaren: seriens eller filmens clearlogo i pillret Spelas nu uppe till vänster i stället för titeln. Av: titeln.'),
    'tr_tr': ('Şimdi oynatılıyor içinde clearlogo', 'Canlı', 'Fused Glass oynatıcı: sol üstteki Şimdi oynatılıyor hapında başlık yerine dizinin veya filmin clearlogo görseli. Kapalı: başlık.'),
    'uk_ua': ('Clearlogo у «Зараз грає»', 'Наживо', 'Програвач Fused Glass: clearlogo серіалу чи фільму в капсулі «Зараз грає» вгорі ліворуч замість назви. Вимк.: назва.'),
    'zh_cn': ('正在播放中显示透明标志', '直播', 'Fused Glass 播放器：左上角“正在播放”胶囊中显示剧集或电影的透明标志，而不是标题。关闭：显示标题。'),
    'zh_tw': ('正在播放中顯示透明標誌', '直播', 'Fused Glass 播放器：左上角「正在播放」膠囊中顯示影集或電影的透明標誌，而不是標題。關閉：顯示標題。'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32476"' in t:
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
print('strings 32476-32478 added in %d languages' % done)
