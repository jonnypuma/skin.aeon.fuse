# -*- coding: utf-8 -*-
"""0.52.3 strings: Skin settings > Motion, memory, reset row "Progress bar updates per second" (row 9763, skin 32570;
"Updates per second" until 0.52.4, the user asked for the full name), its pill "Screen" (32571, as often as Kodi draws
the GUI) and its help line (32572). Row labels were measured with Figtree Bold 24 to end left of the pills (x 506 since
0.52.4): the longest, Polish, ends near 483; long translations name the bar more briefly ("barra", "Balken", "Sáv"),
Greek abbreviates the second. "Screen" fits its 136 px pill in every language (Czech, the widest: 112 px). Run from
the skin folder; writes (or rewrites) the three strings in every language."""
import io
import os
import re

SKIN = {
    32570: 'Progress bar updates per second',
    32571: 'Screen',
    32572: 'How often a second Smooth song progress moves the fill. Screen: as often as Kodi draws the screen. Fewer '
           'updates use less processor time; on a long song even 10 looks smooth.',
}
TR = {
    'cs_cz': ('Aktualizace ukazatele za sekundu', 'Obrazovka',
              'Jak často za sekundu plynulý průběh skladby posune výplň. Obrazovka: tak často, jak Kodi kreslí obrazovku. Méně aktualizací spotřebuje méně výkonu procesoru; u dlouhé skladby vypadá plynule i 10.'),
    'da_dk': ('Opdateringer af statuslinjen pr. sekund', 'Skærm',
              'Hvor mange gange i sekundet glidende sangforløb flytter fyldet. Skærm: lige så ofte som Kodi tegner skærmen. Færre opdateringer bruger mindre processorkraft; på en lang sang ser selv 10 jævnt ud.'),
    'de_de': ('Balkenaktualisierungen pro Sekunde', 'Bildschirm',
              'Wie oft pro Sekunde der flüssige Liedfortschritt die Füllung bewegt. Bildschirm: so oft, wie Kodi das Bild zeichnet. Weniger Aktualisierungen brauchen weniger Prozessorzeit; bei langen Liedern wirkt schon 10 flüssig.'),
    'el_gr': ('Ενημερώσεις μπάρας ανά δευτ.', 'Οθόνη',
              'Πόσες φορές το δευτερόλεπτο η ομαλή πρόοδος τραγουδιού μετακινεί τη γέμιση. Οθόνη: όσο συχνά σχεδιάζει το Kodi την οθόνη. Λιγότερες ενημερώσεις θέλουν λιγότερο επεξεργαστή· σε μεγάλο τραγούδι και το 10 φαίνεται ομαλό.'),
    'es_es': ('Actualizaciones de barra por segundo', 'Pantalla',
              'Cuántas veces por segundo el progreso suave de la canción mueve el relleno. Pantalla: tan a menudo como Kodi dibuja la pantalla. Menos actualizaciones usan menos procesador; en una canción larga incluso 10 se ve suave.'),
    'fi_fi': ('Edistymispalkin päivitykset sekunnissa', 'Näyttö',
              'Kuinka monta kertaa sekunnissa sujuva eteneminen siirtää täyttöä. Näyttö: yhtä usein kuin Kodi piirtää näytön. Harvemmat päivitykset vievät vähemmän suoritinaikaa; pitkässä kappaleessa jo 10 näyttää sujuvalta.'),
    'fr_fr': ('Mises à jour de la barre par seconde', 'Écran',
              "Combien de fois par seconde la progression fluide déplace le remplissage. Écran : aussi souvent que Kodi dessine l'écran. Moins de mises à jour utilisent moins de processeur ; sur un long morceau, 10 suffit déjà."),
    'hu_hu': ('Sáv frissítése másodpercenként', 'Képernyő',
              'Másodpercenként hányszor mozdul a dal folyamatos haladása. Képernyő: ahányszor a Kodi kirajzolja a képet. Kevesebb frissítés kevesebb processzoridőt használ; hosszú dalnál már 10 is folyamatosnak látszik.'),
    'it_it': ('Aggiornamenti barra al secondo', 'Schermo',
              "Quante volte al secondo l'avanzamento fluido sposta il riempimento. Schermo: tante volte quante Kodi disegna lo schermo. Meno aggiornamenti usano meno processore; su un brano lungo anche 10 sembra fluido."),
    'ja_jp': ('プログレスバーの毎秒更新回数', '画面',
              'なめらかな曲の進行を 1 秒に何回動かすか。画面: Kodi が画面を描く回数と同じ。回数が少ないほど CPU の使用が減ります。長い曲なら 10 でもなめらかです。'),
    'ko_kr': ('진행 막대 초당 업데이트 횟수', '화면',
              '부드러운 노래 진행이 1초에 몇 번 움직일지 정합니다. 화면: Kodi가 화면을 그리는 횟수만큼. 횟수가 적을수록 CPU를 덜 씁니다. 긴 노래는 10도 부드럽게 보입니다.'),
    'nb_no': ('Fremdriftslinje: oppdateringer per sek.', 'Skjerm',
              'Hvor mange ganger i sekundet glidende sangfremdrift flytter fyllet. Skjerm: like ofte som Kodi tegner skjermen. Færre oppdateringer bruker mindre prosessorkraft; på en lang sang ser selv 10 jevnt ut.'),
    'nl_nl': ('Voortgangsbalk: updates per seconde', 'Scherm',
              'Hoe vaak per seconde de vloeiende voortgang de vulling verschuift. Scherm: zo vaak als Kodi het scherm tekent. Minder updates kosten minder processortijd; bij een lang nummer oogt zelfs 10 vloeiend.'),
    'pl_pl': ('Aktualizacje paska postępu na sekundę', 'Ekran',
              'Ile razy na sekundę płynny postęp utworu przesuwa wypełnienie. Ekran: tak często, jak Kodi rysuje ekran. Mniej aktualizacji to mniej pracy procesora; przy długim utworze nawet 10 wygląda płynnie.'),
    'pt_br': ('Atualizações da barra por segundo', 'Tela',
              'Quantas vezes por segundo o progresso suave da música move o preenchimento. Tela: tantas vezes quanto o Kodi desenha a tela. Menos atualizações usam menos processador; numa música longa até 10 parece suave.'),
    'pt_pt': ('Atualizações da barra por segundo', 'Ecrã',
              'Quantas vezes por segundo o progresso suave da música move o preenchimento. Ecrã: tantas vezes quanto o Kodi desenha o ecrã. Menos atualizações usam menos processador; numa música longa até 10 parece suave.'),
    'ru_ru': ('Обновлений полосы в секунду', 'Экран',
              'Сколько раз в секунду плавный прогресс песни сдвигает заливку. Экран: так часто, как Kodi рисует экран. Меньше обновлений — меньше нагрузка на процессор; для длинной песни плавно выглядит даже 10.'),
    'sv_se': ('Förloppsfält: uppdateringar per sekund', 'Skärm',
              'Hur många gånger i sekunden mjukt låtförlopp flyttar fyllningen. Skärm: lika ofta som Kodi ritar skärmen. Färre uppdateringar använder mindre processorkraft; på en lång låt ser redan 10 mjukt ut.'),
    'tr_tr': ('Çubuğun saniyedeki güncellemesi', 'Ekran',
              'Akıcı şarkı ilerlemesinin dolguyu saniyede kaç kez kaydıracağı. Ekran: Kodi ekranı ne sıklıkta çiziyorsa. Daha az güncelleme daha az işlemci kullanır; uzun bir şarkıda 10 bile akıcı görünür.'),
    'uk_ua': ('Оновлень смуги за секунду', 'Екран',
              'Скільки разів на секунду плавний поступ пісні зсуває заливку. Екран: так часто, як Kodi малює екран. Менше оновлень — менше навантаження на процесор; для довгої пісні плавно виглядає навіть 10.'),
    'zh_cn': ('进度条每秒更新次数', '屏幕',
              '平滑歌曲进度每秒移动填充的次数。屏幕：与 Kodi 绘制屏幕的频率相同。次数越少越省处理器；长歌曲用 10 也很平滑。'),
    'zh_tw': ('進度列每秒更新次數', '螢幕',
              '平滑歌曲進度每秒移動填充的次數。螢幕：與 Kodi 繪製畫面的頻率相同。次數越少越省處理器；長歌曲用 10 也很平滑。'),
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
