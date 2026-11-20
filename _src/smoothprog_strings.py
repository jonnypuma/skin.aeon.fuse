# -*- coding: utf-8 -*-
"""0.52.1 strings: Skin settings > Motion, memory, reset row "Smooth song progress" (row 9579, skin 32568) and its
help line (32569). The help line wraps to two lines in the 1250 x 64 help box (st_small_20). Run from the skin
folder; writes (or rewrites) both strings in every language."""
import io
import os
import re

SKIN = {
    32568: 'Smooth song progress',
    32569: "Fused Glass Now playing: the song's progress behind the waveform glides instead of jumping 1 % at a time. "
           'Uses a little more processor time while the screen is open.',
}
TR = {
    'cs_cz': ('Plynulý průběh skladby',
              'Právě hraje ve Fused Glass: průběh skladby za vlnou se posouvá plynule místo skoků po 1 %. Když je obrazovka otevřená, spotřebuje trochu víc výkonu procesoru.'),
    'da_dk': ('Glidende sangforløb',
              'Afspilles nu i Fused Glass: sangens forløb bag bølgeformen glider i stedet for at springe 1 % ad gangen. Bruger lidt mere processorkraft, mens skærmen er åben.'),
    'de_de': ('Flüssiger Liedfortschritt',
              'Aktuelle Wiedergabe in Fused Glass: Der Fortschritt des Lieds hinter der Wellenform gleitet, statt in 1-%-Schritten zu springen. Braucht etwas mehr Prozessorzeit, solange die Ansicht offen ist.'),
    'el_gr': ('Ομαλή πρόοδος τραγουδιού',
              'Αναπαράγεται τώρα στο Fused Glass: η πρόοδος του τραγουδιού πίσω από την κυματομορφή κυλά ομαλά αντί να πηδά ανά 1 %. Χρησιμοποιεί λίγο περισσότερο τον επεξεργαστή όσο η οθόνη είναι ανοιχτή.'),
    'es_es': ('Progreso suave de la canción',
              'Reproduciendo en Fused Glass: el progreso de la canción detrás de la onda avanza con suavidad en lugar de saltar de 1 % en 1 %. Usa algo más de procesador mientras la pantalla está abierta.'),
    'fi_fi': ('Kappaleen sujuva eteneminen',
              'Nyt toistetaan (Fused Glass): kappaleen eteneminen aaltomuodon takana liukuu tasaisesti eikä hyppää 1 % kerrallaan. Käyttää hieman enemmän suoritinaikaa, kun näkymä on auki.'),
    'fr_fr': ('Progression fluide du morceau',
              "Lecture en cours de Fused Glass : la progression du morceau derrière la forme d'onde glisse au lieu d'avancer par sauts de 1 %. Utilise un peu plus de processeur tant que l'écran est ouvert."),
    'hu_hu': ('A dal folyamatos haladása',
              'Most játszott (Fused Glass): a dal haladása a hullámforma mögött folyamatosan csúszik, nem 1 %-os ugrásokkal. Kicsivel több processzoridőt használ, amíg a képernyő nyitva van.'),
    'it_it': ('Avanzamento fluido del brano',
              "In riproduzione di Fused Glass: l'avanzamento del brano dietro la forma d'onda scorre fluido invece di saltare dell'1 % alla volta. Usa un po' più di processore mentre la schermata è aperta."),
    'ja_jp': ('曲の進行をなめらかに表示',
              'Fused Glass の再生中画面: 波形の後ろの曲の進行が 1 % ずつ飛ばずになめらかに進みます。画面を開いている間、CPU を少し多く使います。'),
    'ko_kr': ('노래 진행을 부드럽게 표시',
              'Fused Glass 재생 중 화면: 파형 뒤의 노래 진행이 1 %씩 건너뛰지 않고 부드럽게 움직입니다. 화면이 열려 있는 동안 CPU를 조금 더 사용합니다.'),
    'nb_no': ('Glidende sangfremdrift',
              'Spilles nå i Fused Glass: sangens fremdrift bak bølgeformen glir i stedet for å hoppe 1 % om gangen. Bruker litt mer prosessorkraft mens skjermen er åpen.'),
    'nl_nl': ('Vloeiende voortgang van het nummer',
              'Speelt nu in Fused Glass: de voortgang van het nummer achter de golfvorm glijdt in plaats van per 1 % te verspringen. Kost iets meer processortijd zolang het scherm open is.'),
    'pl_pl': ('Płynny postęp utworu',
              'Teraz odtwarzane w Fused Glass: postęp utworu za falą przesuwa się płynnie zamiast skakać co 1 %. Zużywa nieco więcej procesora, gdy ekran jest otwarty.'),
    'pt_br': ('Progresso suave da música',
              'Reproduzindo no Fused Glass: o progresso da música atrás da forma de onda desliza em vez de pular de 1 % em 1 %. Usa um pouco mais de processador enquanto a tela está aberta.'),
    'pt_pt': ('Progresso suave da música',
              'A reproduzir no Fused Glass: o progresso da música atrás da forma de onda desliza em vez de saltar de 1 % em 1 %. Usa um pouco mais de processador enquanto o ecrã está aberto.'),
    'ru_ru': ('Плавный прогресс песни',
              '«Сейчас играет» в Fused Glass: прогресс песни за волной движется плавно, а не скачками по 1 %. Немного больше нагружает процессор, пока экран открыт.'),
    'sv_se': ('Mjukt låtförlopp',
              'Spelas nu i Fused Glass: låtens förlopp bakom vågformen glider i stället för att hoppa 1 % i taget. Använder lite mer processorkraft medan skärmen är öppen.'),
    'tr_tr': ('Akıcı şarkı ilerlemesi',
              "Fused Glass Şimdi oynatılıyor: dalga formunun arkasındaki şarkı ilerlemesi %1'lik adımlarla atlamak yerine akıcı biçimde kayar. Ekran açıkken biraz daha fazla işlemci kullanır."),
    'uk_ua': ('Плавний поступ пісні',
              '«Зараз грає» у Fused Glass: поступ пісні за хвилею рухається плавно, а не стрибками по 1 %. Трохи більше навантажує процесор, поки екран відкритий.'),
    'zh_cn': ('平滑显示歌曲进度',
              'Fused Glass 正在播放：波形后面的歌曲进度平滑移动，而不是每次跳 1%。屏幕打开时会多占用一点处理器。'),
    'zh_tw': ('平滑顯示歌曲進度',
              'Fused Glass 正在播放：波形後面的歌曲進度平滑移動，而不是每次跳 1%。畫面開啟時會多佔用一點處理器。'),
}


def esc(text):
    return text.replace('\\', '\\\\').replace('"', '\\"')


def write(folder, strings):
    done = 0
    for d in sorted(os.listdir(folder)):
        lang = d.replace('resource.language.', '')
        p = os.path.join(folder, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        tr = TR.get(lang)
        assert tr or lang == 'en_gb', lang
        for i, ident in enumerate(sorted(strings)):
            entry = 'msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (
                ident, esc(strings[ident]), '' if lang == 'en_gb' else esc(tr[i]))
            old = re.compile(r'msgctxt "#%d"\nmsgid ".*"\nmsgstr ".*"\n' % ident)
            if old.search(t):
                t = old.sub(lambda _m: entry, t, count=1)
            else:
                t = t.rstrip('\n') + '\n\n' + entry
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        done += 1
    return done


assert len(TR) == 22
print('skin', write('language', SKIN), 'languages')
