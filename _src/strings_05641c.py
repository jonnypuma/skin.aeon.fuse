# -*- coding: utf-8 -*-
"""0.56.41 help texts: Spinning disc art (Off / Videos / Music / Both) and Plotline (Plot / Tagline / Both), all 23
languages. Appends after #32719; repeatable."""
import io
import os

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
EN = [(32720, 'The disc art spinning beside the poster on the player controls: for videos, for music, for both, or off.'),
      (32721, 'What the text under a title shows in every library view: the plot, the tagline (when there is one) or both.')]
T = {
    'cs_cz': ('Točící se obal disku vedle plakátu v ovládání přehrávače: pro videa, pro hudbu, pro obojí, nebo vypnuto.', 'Co ukazuje text pod titulem ve všech zobrazeních knihovny: děj, slogan (pokud existuje) nebo obojí.'),
    'da_dk': ('Den roterende diskgrafik ved plakaten på afspillerknapperne: til videoer, til musik, til begge eller fra.', 'Hvad teksten under en titel viser i alle biblioteksvisninger: handlingen, taglinen (når der er en) eller begge.'),
    'de_de': ('Das sich drehende Disc-Bild neben dem Poster bei den Player-Bedienelementen: für Videos, für Musik, für beides oder aus.', 'Was der Text unter einem Titel in allen Bibliotheksansichten zeigt: die Handlung, den Slogan (falls vorhanden) oder beides.'),
    'el_gr': ('Η περιστρεφόμενη εικόνα δίσκου δίπλα στην αφίσα στα χειριστήρια: για βίντεο, για μουσική, και για τα δύο ή ανενεργή.', 'Τι δείχνει το κείμενο κάτω από έναν τίτλο σε κάθε προβολή βιβλιοθήκης: την πλοκή, το σλόγκαν (όταν υπάρχει) ή και τα δύο.'),
    'es_es': ('La imagen del disco girando junto al póster en los controles del reproductor: para vídeos, para música, para ambos o desactivada.', 'Lo que muestra el texto bajo un título en todas las vistas de la biblioteca: la sinopsis, el lema (si lo hay) o ambos.'),
    'fi_fi': ('Pyörivä levykuva julisteen vieressä soittimen säätimissä: videoille, musiikille, molemmille tai pois.', 'Mitä otsikon alla oleva teksti näyttää kaikissa kirjastonäkymissä: juonen, iskulauseen (jos on) tai molemmat.'),
    'fr_fr': ("L'image du disque qui tourne à côté de l'affiche dans les commandes du lecteur : pour les vidéos, pour la musique, pour les deux, ou désactivée.", "Ce que montre le texte sous un titre dans toutes les vues de la médiathèque : le résumé, l'accroche (s'il y en a une) ou les deux."),
    'hu_hu': ('A forgó lemezkép a plakát mellett a lejátszó vezérlőin: videókhoz, zenéhez, mindkettőhöz vagy kikapcsolva.', 'Mit mutat a cím alatti szöveg minden könyvtárnézetben: a cselekményt, a szlogent (ha van) vagy mindkettőt.'),
    'it_it': ("L'immagine del disco che gira accanto alla locandina nei comandi del lettore: per i video, per la musica, per entrambi o disattivata.", 'Cosa mostra il testo sotto un titolo in tutte le viste della libreria: la trama, lo slogan (se c\'è) o entrambi.'),
    'ja_jp': ('プレーヤーのコントロールでポスターの横に回転するディスクアート：動画、音楽、両方、またはオフ。', 'すべてのライブラリビューでタイトルの下のテキストに表示するもの：あらすじ、キャッチコピー（あれば）、または両方。'),
    'ko_kr': ('플레이어 컨트롤에서 포스터 옆에 도는 디스크 아트: 비디오, 음악, 둘 다 또는 끄기.', '모든 라이브러리 보기에서 제목 아래 텍스트에 표시할 내용: 줄거리, 태그라인(있을 때) 또는 둘 다.'),
    'nb_no': ('Den roterende diskbildet ved plakaten på avspillerkontrollene: for videoer, for musikk, for begge eller av.', 'Hva teksten under en tittel viser i alle bibliotekvisninger: handlingen, slagordet (når det finnes) eller begge.'),
    'nl_nl': ('De draaiende disc-afbeelding naast de poster bij de spelerbediening: voor video’s, voor muziek, voor beide of uit.', 'Wat de tekst onder een titel toont in elke bibliotheekweergave: de plot, de tagline (als die er is) of beide.'),
    'pl_pl': ('Obracający się obraz płyty obok plakatu w sterowaniu odtwarzaczem: dla wideo, dla muzyki, dla obu lub wyłączony.', 'Co pokazuje tekst pod tytułem w każdym widoku biblioteki: fabułę, hasło (jeśli jest) lub oba.'),
    'pt_br': ('A arte do disco girando ao lado do pôster nos controles do player: para vídeos, para música, para ambos ou desligada.', 'O que o texto abaixo de um título mostra em todas as visualizações da biblioteca: a sinopse, o slogan (quando houver) ou ambos.'),
    'pt_pt': ('A arte do disco a girar ao lado do cartaz nos controlos do leitor: para vídeos, para música, para ambos ou desligada.', 'O que o texto por baixo de um título mostra em todas as vistas da biblioteca: a sinopse, o slogan (quando existe) ou ambos.'),
    'ru_ru': ('Вращающийся диск рядом с постером в элементах плеера: для видео, для музыки, для обоих или выкл.', 'Что показывает текст под названием во всех видах медиатеки: сюжет, слоган (если есть) или оба.'),
    'sv_se': ('Den snurrande skivbilden bredvid affischen vid spelarkontrollerna: för videor, för musik, för båda eller av.', 'Vad texten under en titel visar i alla biblioteksvyer: handlingen, taglinen (när det finns en) eller båda.'),
    'tr_tr': ('Oynatıcı kontrollerinde afişin yanında dönen disk resmi: videolar için, müzik için, ikisi için ya da kapalı.', 'Tüm kütüphane görünümlerinde başlığın altındaki metnin gösterdiği: konu, slogan (varsa) ya da ikisi.'),
    'uk_ua': ('Обертовий диск поруч із постером в елементах програвача: для відео, для музики, для обох або вимкнено.', 'Що показує текст під назвою в усіх видах медіатеки: сюжет, гасло (якщо є) або обидва.'),
    'zh_cn': ('播放器控制中海报旁旋转的光盘图：用于视频、音乐、两者，或关闭。', '在所有媒体库视图中标题下方文字显示的内容：剧情、标语（如有）或两者。'),
    'zh_tw': ('播放器控制中海報旁旋轉的光碟圖：用於影片、音樂、兩者，或關閉。', '在所有媒體庫檢視中標題下方文字顯示的內容：劇情、標語（如有）或兩者。'),
}


def esc(s):
    return s.replace('"', '\\"')


def main():
    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        if 'msgctxt "#32720"' in t:
            continue
        code = d.replace('resource.language.', '')
        add = ''.join('\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), '' if code == 'en_gb' else esc(T[code][i]))
                      for i, (sid, en) in enumerate(EN))
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)
    print('ok')


if __name__ == '__main__':
    main()
