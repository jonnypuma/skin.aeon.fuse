# -*- coding: utf-8 -*-
"""0.56.45 strings, all 23 languages: 32748 the help line of an open Skin settings row (choose mode), 32749 / 32750
Home menu > Start on and its help, and 32683 (changed) Library fanart blur's help for the new -2 .. +2 steps.
Repeatable: an id that is there is written again."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
IDS = [32748, 32749, 32750, 32683]
EN = ['Left / Right: choose an option. OK: set it. Up, Down or Back: keep the one in use.',
      'Start on',
      'The Home menu item that has the focus when Kodi starts, once the splash has gone.',
      'Blurs the fanart behind the library views: -2 a little, +2 the most; 0 is the default. Off: sharp.']
T = {
    'cs_cz': ['Vlevo / Vpravo: vyberte možnost. OK: nastavte ji. Nahoru, Dolů nebo Zpět: ponechte stávající.', 'Začít na',
              'Položka hlavní nabídky, na které je výběr při spuštění Kodi, jakmile zmizí úvodní obrazovka.',
              'Rozmaže fanart za zobrazeními knihovny: -2 trochu, +2 nejvíc; 0 je výchozí. Vypnuto: ostrý.'],
    'da_dk': ['Venstre / Højre: vælg en mulighed. OK: indstil den. Op, Ned eller Tilbage: behold den nuværende.', 'Start på',
              'Det punkt i hjemmemenuen, der har fokus, når Kodi starter, når startskærmen er væk.',
              'Slører fanart bag biblioteksvisningerne: -2 lidt, +2 mest; 0 er standard. Fra: skarp.'],
    'de_de': ['Links / Rechts: Option wählen. OK: übernehmen. Hoch, Runter oder Zurück: die aktuelle behalten.', 'Starten auf',
              'Der Eintrag des Hauptmenüs, der beim Start von Kodi den Fokus hat, sobald der Startbildschirm weg ist.',
              'Zeichnet den Fanart hinter den Bibliotheksansichten weich: -2 ein wenig, +2 am stärksten; 0 ist der Standard. Aus: scharf.'],
    'el_gr': ['Αριστερά / Δεξιά: επιλέξτε. OK: ορίστε το. Πάνω, Κάτω ή Πίσω: κρατήστε το τρέχον.', 'Έναρξη σε',
              'Το στοιχείο του αρχικού μενού που έχει την εστίαση όταν ξεκινά το Kodi, μόλις φύγει η οθόνη εκκίνησης.',
              'Θολώνει το fanart πίσω από τις προβολές βιβλιοθήκης: -2 λίγο, +2 περισσότερο· 0 είναι το προεπιλεγμένο. Ανενεργό: καθαρό.'],
    'es_es': ['Izquierda / Derecha: elige una opción. OK: aplícala. Arriba, Abajo o Atrás: mantén la actual.', 'Empezar en',
              'El elemento del menú de inicio que tiene el foco al arrancar Kodi, cuando desaparece la pantalla de inicio.',
              'Desenfoca el fanart detrás de las vistas de la biblioteca: -2 un poco, +2 al máximo; 0 es el predeterminado. Desactivado: nítido.'],
    'fi_fi': ['Vasen / Oikea: valitse vaihtoehto. OK: ota se käyttöön. Ylös, Alas tai Takaisin: pidä nykyinen.', 'Aloita kohdasta',
              'Kotivalikon kohta, jossa kohdistus on Kodin käynnistyessä, kun aloitusnäyttö on poistunut.',
              'Sumentaa kirjastonäkymien taustakuvan: -2 hieman, +2 eniten; 0 on oletus. Pois: terävä.'],
    'fr_fr': ['Gauche / Droite : choisir une option. OK : l\'appliquer. Haut, Bas ou Retour : garder l\'actuelle.', 'Démarrer sur',
              'L\'élément du menu d\'accueil sélectionné au démarrage de Kodi, une fois l\'écran de démarrage disparu.',
              'Floute le fanart derrière les vues de la médiathèque : -2 un peu, +2 le plus ; 0 est la valeur par défaut. Désactivé : net.'],
    'hu_hu': ['Balra / Jobbra: válasszon. OK: beállítás. Fel, Le vagy Vissza: a jelenlegi marad.', 'Indulás itt',
              'A főmenü azon eleme, amelyen a fókusz van, amikor a Kodi elindul, miután az indítóképernyő eltűnt.',
              'Elmossa a könyvtárnézetek mögötti fanartot: -2 kicsit, +2 a legjobban; 0 az alapérték. Ki: éles.'],
    'it_it': ['Sinistra / Destra: scegli un\'opzione. OK: applicala. Su, Giù o Indietro: mantieni quella attuale.', 'Inizia da',
              'La voce del menu Home selezionata all\'avvio di Kodi, una volta scomparsa la schermata iniziale.',
              'Sfoca il fanart dietro le viste della libreria: -2 poco, +2 al massimo; 0 è il predefinito. Disattivato: nitido.'],
    'ja_jp': ['左 / 右：オプションを選ぶ。OK：設定する。上、下、戻る：今のままにする。', '開始位置',
              'Kodi の起動時、スプラッシュが消えたあとにフォーカスが置かれるホームメニューの項目。',
              'ライブラリ表示の背後のファンアートをぼかします：-2 で少し、+2 で最大。0 が既定。オフ：くっきり。'],
    'ko_kr': ['왼쪽 / 오른쪽: 옵션을 고르세요. OK: 설정합니다. 위, 아래 또는 뒤로: 지금 것을 유지합니다.', '시작 위치',
              'Kodi가 시작될 때 시작 화면이 사라진 뒤 포커스가 놓이는 홈 메뉴 항목.',
              '라이브러리 보기 뒤의 팬아트를 흐리게 합니다: -2 조금, +2 가장 많이; 0이 기본값. 끔: 선명하게.'],
    'nb_no': ['Venstre / Høyre: velg et alternativ. OK: bruk det. Opp, Ned eller Tilbake: behold det nåværende.', 'Start på',
              'Punktet i hjemmemenyen som har fokus når Kodi starter, når oppstartsbildet er borte.',
              'Gjør fanart bak bibliotekvisningene uskarpt: -2 litt, +2 mest; 0 er standard. Av: skarpt.'],
    'nl_nl': ['Links / Rechts: kies een optie. OK: stel hem in. Omhoog, Omlaag of Terug: houd de huidige.', 'Starten op',
              'Het item van het hoofdmenu dat de focus heeft als Kodi start, zodra het opstartscherm weg is.',
              'Vervaagt de fanart achter de bibliotheekweergaven: -2 een beetje, +2 het meest; 0 is de standaard. Uit: scherp.'],
    'pl_pl': ['Lewo / Prawo: wybierz opcję. OK: ustaw ją. Góra, Dół lub Wstecz: zostaw obecną.', 'Zacznij od',
              'Pozycja menu głównego zaznaczona po uruchomieniu Kodi, gdy zniknie ekran startowy.',
              'Rozmywa fanart za widokami biblioteki: -2 trochę, +2 najbardziej; 0 to domyślne. Wyłączone: ostry.'],
    'pt_br': ['Esquerda / Direita: escolha uma opção. OK: aplique. Cima, Baixo ou Voltar: mantenha a atual.', 'Começar em',
              'O item do menu inicial que fica em foco quando o Kodi inicia, depois que a tela de abertura some.',
              'Desfoca o fanart atrás das exibições da biblioteca: -2 pouco, +2 o máximo; 0 é o padrão. Desligado: nítido.'],
    'pt_pt': ['Esquerda / Direita: escolha uma opção. OK: aplique-a. Cima, Baixo ou Voltar: mantenha a atual.', 'Começar em',
              'O item do menu inicial que fica selecionado quando o Kodi arranca, depois de o ecrã de abertura desaparecer.',
              'Desfoca o fanart atrás das vistas da biblioteca: -2 pouco, +2 o máximo; 0 é o predefinido. Desligado: nítido.'],
    'ru_ru': ['Влево / Вправо: выберите вариант. OK: применить. Вверх, Вниз или Назад: оставить текущий.', 'Начинать с',
              'Пункт главного меню, на котором фокус при запуске Kodi, после того как исчезнет заставка.',
              'Размывает фанарт за видами медиатеки: -2 немного, +2 сильнее всего; 0 по умолчанию. Выкл.: чётко.'],
    'sv_se': ['Vänster / Höger: välj ett alternativ. OK: använd det. Upp, Ned eller Tillbaka: behåll det nuvarande.', 'Starta på',
              'Det objekt i hemmenyn som har fokus när Kodi startar, när startskärmen har försvunnit.',
              'Gör fanart bakom biblioteksvyerna suddig: -2 lite, +2 mest; 0 är standard. Av: skarp.'],
    'tr_tr': ['Sol / Sağ: bir seçenek seçin. Tamam: uygulayın. Yukarı, Aşağı veya Geri: mevcut olan kalsın.', 'Başlangıç öğesi',
              'Kodi açılırken, açılış ekranı kaybolduktan sonra odakta olan ana menü öğesi.',
              'Kitaplık görünümlerinin arkasındaki fanartı bulanıklaştırır: -2 biraz, +2 en çok; 0 varsayılandır. Kapalı: net.'],
    'uk_ua': ['Вліво / Вправо: виберіть варіант. OK: застосувати. Вгору, Вниз або Назад: залишити поточний.', 'Починати з',
              'Пункт головного меню, на якому фокус під час запуску Kodi, коли зникне заставка.',
              'Розмиває фанарт за видами медіатеки: -2 трохи, +2 найсильніше; 0 за замовчуванням. Вимк.: чітко.'],
    'zh_cn': ['左 / 右：选择选项。确定：应用。上、下或返回：保留当前选项。', '启动于',
              'Kodi 启动时、启动画面消失后获得焦点的主菜单项目。',
              '模糊媒体库视图背后的同人画：-2 轻微，+2 最强；0 为默认。关闭：清晰。'],
    'zh_tw': ['左 / 右：選擇選項。確定：套用。上、下或返回：保留目前的選項。', '啟動於',
              'Kodi 啟動時、啟動畫面消失後取得焦點的首頁選單項目。',
              '模糊媒體櫃檢視背後的同人圖：-2 輕微，+2 最強；0 為預設。關閉：清晰。'],
}


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    for code, row in T.items():
        assert len(row) == len(IDS), (code, len(row))
    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        code = d.replace('resource.language.', '')
        for i, sid in enumerate(IDS):
            tr = '' if code == 'en_gb' else esc(T[code][i])
            m = re.search(r'(msgctxt "#%d"\nmsgid ")(.*)("\nmsgstr ")(.*)(")' % sid, t)
            if m:
                t = t[:m.start()] + m.group(1) + esc(EN[i]) + m.group(3) + tr + m.group(5) + t[m.end():]
            else:
                t = t.rstrip('\n') + '\n\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(EN[i]), tr)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('ok', len(IDS), 'strings in', len(os.listdir(L)), 'languages')


if __name__ == '__main__':
    main()
