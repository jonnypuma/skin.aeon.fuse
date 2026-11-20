"""0.56.32 strings: the Fused Glass style's menus and dialogs (Menu background row, key hints), all 23 languages.
Appends after #32688; repeatable."""
import io
import os

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
EN = [
    (32689, 'Menu background'),
    (32690, 'Screen'),
    (32691, "Menus and dialogs in the Fused Glass style. Fanart: the item's fanart behind them. Screen: the screen they opened on, dimmed."),
    (32692, 'OK runs it  ·  Back closes'),
    (32693, 'OK chooses  ·  Back closes'),
]
T = {
    'cs_cz': ('Pozadí nabídek', 'Obrazovka', 'Nabídky a dialogy ve stylu Fused Glass. Fanart: fanart položky za nimi. Obrazovka: ztlumená obrazovka, na které se otevřely.', 'OK spustí  ·  Zpět zavře', 'OK vybere  ·  Zpět zavře'),
    'da_dk': ('Menubaggrund', 'Skærm', 'Menuer og dialoger i Fused Glass-stilen. Fanart: elementets fanart bag dem. Skærm: skærmen de blev åbnet på, dæmpet.', 'OK kører  ·  Tilbage lukker', 'OK vælger  ·  Tilbage lukker'),
    'de_de': ('Menühintergrund', 'Bildschirm', 'Menüs und Dialoge im Fused-Glass-Stil. Fanart: das Fanart des Eintrags dahinter. Bildschirm: der Bildschirm, auf dem sie geöffnet wurden, abgedunkelt.', 'OK führt aus  ·  Zurück schließt', 'OK wählt  ·  Zurück schließt'),
    'el_gr': ('Φόντο μενού', 'Οθόνη', 'Μενού και διάλογοι στο στυλ Fused Glass. Fanart: το fanart του στοιχείου από πίσω. Οθόνη: η οθόνη όπου άνοιξαν, σκοτεινιασμένη.', 'OK εκτελεί  ·  Πίσω κλείνει', 'OK επιλέγει  ·  Πίσω κλείνει'),
    'es_es': ('Fondo de los menús', 'Pantalla', 'Menús y diálogos con el estilo Fused Glass. Fanart: el fanart del elemento detrás. Pantalla: la pantalla en la que se abrieron, atenuada.', 'OK lo ejecuta  ·  Atrás cierra', 'OK elige  ·  Atrás cierra'),
    'fi_fi': ('Valikoiden tausta', 'Näyttö', 'Fused Glass -tyylin valikot ja valintaikkunat. Fanart: kohteen fanart taustalla. Näyttö: näkymä, jossa ne avattiin, himmennettynä.', 'OK suorittaa  ·  Takaisin sulkee', 'OK valitsee  ·  Takaisin sulkee'),
    'fr_fr': ('Fond des menus', 'Écran', "Menus et dialogues dans le style Fused Glass. Fanart : le fanart de l'élément derrière eux. Écran : l'écran sur lequel ils se sont ouverts, assombri.", "OK l'exécute  ·  Retour ferme", 'OK choisit  ·  Retour ferme'),
    'hu_hu': ('Menük háttere', 'Képernyő', 'Menük és párbeszédablakok Fused Glass stílusban. Fanart: az elem fanartja mögöttük. Képernyő: az a képernyő, amelyen megnyíltak, elsötétítve.', 'OK futtatja  ·  Vissza bezár', 'OK kiválaszt  ·  Vissza bezár'),
    'it_it': ('Sfondo dei menu', 'Schermo', "Menu e finestre di dialogo nello stile Fused Glass. Fanart: il fanart dell'elemento dietro. Schermo: la schermata su cui si sono aperti, scurita.", 'OK lo esegue  ·  Indietro chiude', 'OK sceglie  ·  Indietro chiude'),
    'ja_jp': ('メニューの背景', '画面', 'Fused Glass スタイルのメニューとダイアログ。ファンアート: 項目のファンアートを背景に表示。画面: 開いた画面を暗くして表示。', 'OK で実行  ·  戻るで閉じる', 'OK で選択  ·  戻るで閉じる'),
    'ko_kr': ('메뉴 배경', '화면', 'Fused Glass 스타일의 메뉴와 대화상자. 팬아트: 항목의 팬아트를 뒤에 표시. 화면: 열린 화면을 어둡게 표시.', 'OK 실행  ·  뒤로 닫기', 'OK 선택  ·  뒤로 닫기'),
    'nb_no': ('Menybakgrunn', 'Skjerm', 'Menyer og dialoger i Fused Glass-stilen. Fanart: elementets fanart bak dem. Skjerm: skjermen de ble åpnet på, dempet.', 'OK kjører  ·  Tilbake lukker', 'OK velger  ·  Tilbake lukker'),
    'nl_nl': ('Menuachtergrond', 'Scherm', "Menu's en dialogen in de Fused Glass-stijl. Fanart: de fanart van het item erachter. Scherm: het scherm waarop ze openden, gedimd.", 'OK voert uit  ·  Terug sluit', 'OK kiest  ·  Terug sluit'),
    'pl_pl': ('Tło menu', 'Ekran', 'Menu i okna dialogowe w stylu Fused Glass. Fanart: fanart elementu w tle. Ekran: ekran, na którym się otworzyły, przyciemniony.', 'OK uruchamia  ·  Wstecz zamyka', 'OK wybiera  ·  Wstecz zamyka'),
    'pt_br': ('Fundo dos menus', 'Tela', 'Menus e diálogos no estilo Fused Glass. Fanart: o fanart do item atrás deles. Tela: a tela em que foram abertos, escurecida.', 'OK executa  ·  Voltar fecha', 'OK escolhe  ·  Voltar fecha'),
    'pt_pt': ('Fundo dos menus', 'Ecrã', 'Menus e diálogos no estilo Fused Glass. Fanart: o fanart do item atrás deles. Ecrã: o ecrã em que foram abertos, escurecido.', 'OK executa  ·  Voltar fecha', 'OK escolhe  ·  Voltar fecha'),
    'ru_ru': ('Фон меню', 'Экран', 'Меню и диалоги в стиле Fused Glass. Фанарт: фанарт элемента на фоне. Экран: экран, на котором они открылись, затемнённый.', 'OK — выполнить  ·  Назад — закрыть', 'OK — выбрать  ·  Назад — закрыть'),
    'sv_se': ('Menybakgrund', 'Skärm', 'Menyer och dialogrutor i Fused Glass-stilen. Fanart: objektets fanart bakom dem. Skärm: skärmen de öppnades på, nedtonad.', 'OK kör  ·  Bakåt stänger', 'OK väljer  ·  Bakåt stänger'),
    'tr_tr': ('Menü arka planı', 'Ekran', 'Fused Glass stilindeki menüler ve iletişim kutuları. Fanart: arkada öğenin fanartı. Ekran: açıldıkları ekran, karartılmış.', 'OK çalıştırır  ·  Geri kapatır', 'OK seçer  ·  Geri kapatır'),
    'uk_ua': ('Тло меню', 'Екран', 'Меню та діалоги у стилі Fused Glass. Фанарт: фанарт елемента позаду. Екран: екран, на якому вони відкрилися, затемнений.', 'OK — виконати  ·  Назад — закрити', 'OK — вибрати  ·  Назад — закрити'),
    'zh_cn': ('菜单背景', '屏幕', 'Fused Glass 风格的菜单和对话框。同人画：在后面显示项目的同人画。屏幕：变暗显示打开它们的屏幕。', 'OK 执行  ·  返回关闭', 'OK 选择  ·  返回关闭'),
    'zh_tw': ('選單背景', '螢幕', 'Fused Glass 風格的選單和對話框。同人畫：在後面顯示項目的同人畫。螢幕：變暗顯示開啟它們的螢幕。', 'OK 執行  ·  返回關閉', 'OK 選擇  ·  返回關閉'),
}


def esc(s):
    return s.replace('"', '\\"')


for d in sorted(os.listdir(L)):
    p = os.path.join(L, d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32689"' in t:
        continue
    code = d.replace('resource.language.', '')
    add = ''
    for i, (sid, en) in enumerate(EN):
        tr = '' if code == 'en_gb' else T[code][i]
        add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), esc(tr))
    t = t.rstrip('\n') + '\n' + add
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print(d, 'ok')
