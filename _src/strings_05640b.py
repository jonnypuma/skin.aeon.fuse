# -*- coding: utf-8 -*-
"""0.56.40 strings, part 2: the setup wizard in its original look, one setting per step (_src/wizard_05640.py), all 23
languages. Appends after #32712; repeatable."""
import io
import os

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
EN = [
    (32713, 'Fused Glass floats frosted glass cards over the artwork. Aeon draws solid panels with a bright focus bar. Aeon Glass keeps the Aeon layout in see-through panels.'),
    (32714, 'Frosted glass cards'),
    (32715, 'Take the theme as it comes, or go through its look step by step. Everything can be changed later in Skin settings.'),
    (32716, 'How the settings strip of the library views shows: over the view (Overlay) or always beside it (Permanent).'),
    (32717, 'How much the edges of the Home screen darken behind the menu and the text.'),
    (32718, 'The colour of the clock box and the corner boxes with the Aeon palette.'),
    (32719, 'Optional add-ons that give the skin more to show. Install the ones you want; the rest can wait.'),
]
T = {
    'cs_cz': ('Fused Glass nechává nad obrázky vznášet matné skleněné karty. Aeon kreslí plné panely s výrazným pruhem fokusu. Aeon Glass zachovává rozvržení Aeon v průhledných panelech.',
              'Matné skleněné karty', 'Vezměte motiv, jak je, nebo projděte jeho vzhled krok za krokem. Vše lze později změnit v nastavení skinu.',
              'Jak se zobrazuje pruh nastavení v zobrazeních knihovny: přes zobrazení (Překryv) nebo stále vedle něj (Trvale).',
              'Jak moc ztmavnou okraje obrazovky Domů za nabídkou a textem.', 'Barva boxu hodin a rohových boxů s paletou Aeon.',
              'Volitelné doplňky, díky kterým skin ukáže víc. Nainstalujte ty, které chcete; ostatní počkají.'),
    'da_dk': ('Fused Glass lader matte glaskort svæve over billederne. Aeon tegner faste paneler med en lys fokusbjælke. Aeon Glass beholder Aeon-layoutet i gennemsigtige paneler.',
              'Matte glaskort', 'Tag temaet, som det er, eller gå dets udseende igennem trin for trin. Alt kan ændres senere i Skin-indstillinger.',
              'Hvordan indstillingsbjælken i biblioteksvisningerne vises: over visningen (Overlejring) eller altid ved siden af (Permanent).',
              'Hvor meget kanterne af Hjem-skærmen mørknes bag menuen og teksten.', 'Farven på urboksen og hjørneboksene med Aeon-paletten.',
              'Valgfrie tilføjelser, der giver skinnet mere at vise. Installer dem, du vil have; resten kan vente.'),
    'de_de': ('Fused Glass lässt Mattglas-Karten über den Bildern schweben. Aeon zeichnet feste Flächen mit einem hellen Fokusbalken. Aeon Glass behält das Aeon-Layout mit durchscheinenden Flächen.',
              'Mattglas-Karten', 'Das Theme so nehmen, wie es ist, oder sein Aussehen Schritt für Schritt einstellen. Alles lässt sich später in den Skin-Einstellungen ändern.',
              'Wie die Einstellungsleiste der Bibliotheksansichten erscheint: über der Ansicht (Überlagernd) oder immer daneben (Dauerhaft).',
              'Wie stark die Ränder der Startseite hinter dem Menü und dem Text abgedunkelt werden.', 'Die Farbe der Uhrbox und der Eckboxen mit der Aeon-Palette.',
              'Optionale Add-ons, mit denen der Skin mehr zeigen kann. Installiere die gewünschten; der Rest kann warten.'),
    'el_gr': ('Το Fused Glass αιωρεί ματ γυάλινες κάρτες πάνω από τις εικόνες. Το Aeon σχεδιάζει συμπαγή πάνελ με φωτεινή μπάρα εστίασης. Το Aeon Glass κρατά τη διάταξη Aeon σε διάφανα πάνελ.',
              'Ματ γυάλινες κάρτες', 'Πάρτε το θέμα όπως είναι ή περάστε την εμφάνισή του βήμα προς βήμα. Όλα αλλάζουν αργότερα στις ρυθμίσεις κελύφους.',
              'Πώς εμφανίζεται η λωρίδα ρυθμίσεων στις προβολές βιβλιοθήκης: πάνω από την προβολή (Επικάλυψη) ή πάντα δίπλα της (Μόνιμα).',
              'Πόσο σκουραίνουν οι άκρες της Αρχικής οθόνης πίσω από το μενού και το κείμενο.', 'Το χρώμα του πλαισίου ρολογιού και των γωνιακών πλαισίων με την παλέτα Aeon.',
              'Προαιρετικά πρόσθετα που δίνουν στο κέλυφος περισσότερα να δείξει. Εγκαταστήστε όσα θέλετε· τα υπόλοιπα μπορούν να περιμένουν.'),
    'es_es': ('Fused Glass hace flotar tarjetas de cristal esmerilado sobre las imágenes. Aeon dibuja paneles sólidos con una barra de foco brillante. Aeon Glass mantiene el diseño de Aeon con paneles translúcidos.',
              'Tarjetas de cristal esmerilado', 'Usa el tema tal como viene o recorre su aspecto paso a paso. Todo se puede cambiar después en los ajustes de la skin.',
              'Cómo se muestra la barra de ajustes de las vistas de la biblioteca: sobre la vista (Superpuesta) o siempre a su lado (Permanente).',
              'Cuánto se oscurecen los bordes de la pantalla de Inicio detrás del menú y del texto.', 'El color del recuadro del reloj y de los recuadros de las esquinas con la paleta Aeon.',
              'Complementos opcionales que dan a la skin más que mostrar. Instala los que quieras; el resto puede esperar.'),
    'fi_fi': ('Fused Glass leijuttaa himmeitä lasikortteja kuvien yllä. Aeon piirtää umpinaiset paneelit ja kirkkaan kohdistuspalkin. Aeon Glass säilyttää Aeonin asettelun läpikuultavin paneelein.',
              'Himmeät lasikortit', 'Ota teema sellaisenaan tai käy sen ulkoasu läpi vaihe vaiheelta. Kaiken voi muuttaa myöhemmin teeman asetuksissa.',
              'Miten kirjastonäkymien asetuspalkki näkyy: näkymän päällä (Peittävä) tai aina sen vieressä (Pysyvä).',
              'Kuinka paljon Koti-näkymän reunat tummuvat valikon ja tekstin takana.', 'Kellolaatikon ja kulmalaatikoiden väri Aeon-paletilla.',
              'Valinnaisia lisäosia, joilla teema voi näyttää enemmän. Asenna haluamasi; loput voivat odottaa.'),
    'fr_fr': ("Fused Glass fait flotter des cartes en verre dépoli au-dessus des images. Aeon dessine des panneaux pleins avec une barre de sélection claire. Aeon Glass garde la mise en page d'Aeon avec des panneaux translucides.",
              'Cartes en verre dépoli', "Prenez le thème tel quel, ou parcourez son apparence étape par étape. Tout peut être changé plus tard dans les paramètres du skin.",
              "Comment s'affiche la bande de réglages des vues de la médiathèque : par-dessus la vue (Superposée) ou toujours à côté (Permanente).",
              "À quel point les bords de l'écran d'accueil s'assombrissent derrière le menu et le texte.", "La couleur du cadre de l'horloge et des cadres d'angle avec la palette Aeon.",
              'Des extensions facultatives qui donnent plus à montrer au skin. Installez celles que vous voulez ; les autres peuvent attendre.'),
    'hu_hu': ('A Fused Glass matt üvegkártyákat lebegtet a képek felett. Az Aeon tömör paneleket rajzol világos fókuszsávval. Az Aeon Glass megtartja az Aeon elrendezését áttetsző panelekkel.',
              'Matt üvegkártyák', 'Vegye a témát úgy, ahogy van, vagy haladjon végig a megjelenésén lépésről lépésre. Később minden módosítható a felület beállításaiban.',
              'Hogyan jelenik meg a könyvtárnézetek beállítássávja: a nézet fölött (Átfedő) vagy mindig mellette (Állandó).',
              'Mennyire sötétednek el a Kezdőlap szélei a menü és a szöveg mögött.', 'Az óradoboz és a sarokdobozok színe az Aeon palettával.',
              'Opcionális kiegészítők, amelyekkel a felület többet mutathat. Telepítse, amelyeket szeretne; a többi várhat.'),
    'it_it': ("Fused Glass fa fluttuare schede di vetro smerigliato sopra le immagini. Aeon disegna pannelli pieni con una barra di selezione chiara. Aeon Glass mantiene il layout di Aeon con pannelli trasparenti.",
              'Schede di vetro smerigliato', "Usa il tema così com'è, oppure scorri il suo aspetto passo dopo passo. Tutto si può cambiare in seguito nelle impostazioni della skin.",
              'Come si mostra la barra delle impostazioni nelle viste della libreria: sopra la vista (Sovrapposta) o sempre accanto (Permanente).',
              'Quanto si scuriscono i bordi della schermata Home dietro il menu e il testo.', "Il colore del riquadro dell'orologio e dei riquadri d'angolo con la tavolozza Aeon.",
              'Add-on facoltativi che danno alla skin altro da mostrare. Installa quelli che vuoi; il resto può aspettare.'),
    'ja_jp': ('Fused Glass はすりガラスのカードをアートワークの上に浮かべます。Aeon は不透明なパネルと明るいフォーカスバーで描きます。Aeon Glass は Aeon のレイアウトを半透明のパネルで表示します。',
              'すりガラスのカード', 'テーマをそのまま使うか、外観を一歩ずつ設定します。後からスキン設定でいつでも変更できます。',
              'ライブラリビューの設定ストリップの表示方法：ビューの上に重ねる（オーバーレイ）か、常に横に表示する（固定）。',
              'メニューとテキストの後ろで、ホーム画面の端をどれだけ暗くするか。', 'Aeon パレットでの時計ボックスと隅のボックスの色。',
              'スキンの表示を増やすオプションのアドオン。必要なものをインストールしてください。残りは後でも構いません。'),
    'ko_kr': ('Fused Glass는 반투명 유리 카드를 아트워크 위에 띄웁니다. Aeon은 불투명한 패널과 밝은 포커스 막대를 그립니다. Aeon Glass는 Aeon 레이아웃을 반투명 패널로 유지합니다.',
              '반투명 유리 카드', '테마를 그대로 쓰거나 모양을 한 단계씩 설정하세요. 나중에 스킨 설정에서 모두 바꿀 수 있습니다.',
              '라이브러리 보기의 설정 스트립 표시 방식: 보기 위에 겹쳐서(오버레이) 또는 항상 옆에(고정).',
              '메뉴와 텍스트 뒤에서 홈 화면 가장자리를 얼마나 어둡게 할지.', 'Aeon 팔레트에서 시계 상자와 모서리 상자의 색.',
              '스킨이 더 많은 것을 보여 주게 하는 선택 애드온입니다. 원하는 것을 설치하세요. 나머지는 나중에 해도 됩니다.'),
    'nb_no': ('Fused Glass lar matte glasskort sveve over bildene. Aeon tegner faste paneler med en lys fokuslinje. Aeon Glass beholder Aeon-oppsettet i gjennomsiktige paneler.',
              'Matte glasskort', 'Ta temaet slik det er, eller gå gjennom utseendet trinn for trinn. Alt kan endres senere i skallinnstillingene.',
              'Hvordan innstillingsstripen i bibliotekvisningene vises: over visningen (Overlegg) eller alltid ved siden av (Permanent).',
              'Hvor mye kantene av Hjem-skjermen mørkner bak menyen og teksten.', 'Fargen på klokkeboksen og hjørneboksene med Aeon-paletten.',
              'Valgfrie tillegg som gir skallet mer å vise. Installer de du vil ha; resten kan vente.'),
    'nl_nl': ('Fused Glass laat kaarten van matglas boven de afbeeldingen zweven. Aeon tekent dichte panelen met een heldere focusbalk. Aeon Glass houdt de Aeon-indeling met doorschijnende panelen.',
              'Kaarten van matglas', 'Neem het thema zoals het is, of loop het uiterlijk stap voor stap door. Alles is later te wijzigen in de skininstellingen.',
              'Hoe de instellingenstrook van de bibliotheekweergaven verschijnt: over de weergave (Overlay) of altijd ernaast (Permanent).',
              'Hoeveel de randen van het Home-scherm donkerder worden achter het menu en de tekst.', 'De kleur van het klokvak en de hoekvakken met het Aeon-palet.',
              'Optionele add-ons die de skin meer te tonen geven. Installeer de add-ons die je wilt; de rest kan wachten.'),
    'pl_pl': ('Fused Glass unosi karty z matowego szkła nad obrazami. Aeon rysuje pełne panele z jasnym paskiem zaznaczenia. Aeon Glass zachowuje układ Aeon w przejrzystych panelach.',
              'Karty z matowego szkła', 'Weź motyw w oryginalnej postaci albo przejdź jego wygląd krok po kroku. Wszystko można później zmienić w ustawieniach skórki.',
              'Jak pokazuje się pasek ustawień w widokach biblioteki: nad widokiem (Nakładka) lub zawsze obok (Stały).',
              'Jak bardzo ciemnieją krawędzie ekranu głównego za menu i tekstem.', 'Kolor ramki zegara i ramek narożnych z paletą Aeon.',
              'Opcjonalne dodatki, dzięki którym skórka pokaże więcej. Zainstaluj te, które chcesz; reszta może poczekać.'),
    'pt_br': ('Fused Glass faz cartões de vidro fosco flutuarem sobre as imagens. Aeon desenha painéis sólidos com uma barra de foco clara. Aeon Glass mantém o layout do Aeon em painéis translúcidos.',
              'Cartões de vidro fosco', 'Use o tema como vem ou passe pela aparência passo a passo. Tudo pode ser mudado depois nas configurações da skin.',
              'Como a faixa de configurações das visualizações da biblioteca aparece: sobre a visualização (Sobreposta) ou sempre ao lado (Permanente).',
              'O quanto as bordas da tela Início escurecem atrás do menu e do texto.', 'A cor da caixa do relógio e das caixas de canto com a paleta Aeon.',
              'Complementos opcionais que dão à skin mais para mostrar. Instale os que quiser; o resto pode esperar.'),
    'pt_pt': ('Fused Glass faz flutuar cartões de vidro fosco sobre as imagens. Aeon desenha painéis sólidos com uma barra de foco clara. Aeon Glass mantém o esquema do Aeon em painéis translúcidos.',
              'Cartões de vidro fosco', 'Use o tema tal como vem ou percorra o seu aspeto passo a passo. Tudo pode ser alterado depois nas definições da skin.',
              'Como a faixa de definições das vistas da biblioteca aparece: sobre a vista (Sobreposta) ou sempre ao lado (Permanente).',
              'Quanto escurecem as margens do ecrã Início atrás do menu e do texto.', 'A cor da caixa do relógio e das caixas de canto com a paleta Aeon.',
              'Extras opcionais que dão à skin mais para mostrar. Instale os que quiser; o resto pode esperar.'),
    'ru_ru': ('Fused Glass парит карточки из матового стекла над изображениями. Aeon рисует сплошные панели с яркой полосой фокуса. Aeon Glass сохраняет раскладку Aeon в полупрозрачных панелях.',
              'Карточки из матового стекла', 'Возьмите тему как есть или настройте её вид шаг за шагом. Всё можно изменить позже в настройках обложки.',
              'Как показывается полоса настроек в видах медиатеки: поверх вида (Наложение) или всегда рядом (Постоянно).',
              'Насколько темнеют края главного экрана за меню и текстом.', 'Цвет блока часов и угловых блоков с палитрой Aeon.',
              'Дополнительные дополнения, с которыми обложка покажет больше. Установите нужные; остальное подождёт.'),
    'sv_se': ('Fused Glass låter matta glaskort sväva över bilderna. Aeon ritar fasta paneler med en ljus fokusrad. Aeon Glass behåller Aeon-layouten i genomskinliga paneler.',
              'Matta glaskort', 'Ta temat som det är, eller gå igenom utseendet steg för steg. Allt kan ändras senare i skalinställningarna.',
              'Hur inställningsremsan i biblioteksvyerna visas: över vyn (Överlägg) eller alltid bredvid (Permanent).',
              'Hur mycket kanterna på Hem-skärmen mörknar bakom menyn och texten.', 'Färgen på klockrutan och hörnrutorna med Aeon-paletten.',
              'Valfria tillägg som ger skalet mer att visa. Installera de du vill ha; resten kan vänta.'),
    'tr_tr': ('Fused Glass, görsellerin üzerinde buzlu cam kartlar süzdürür. Aeon, parlak bir odak çubuğuyla dolu paneller çizer. Aeon Glass, Aeon düzenini yarı saydam panellerle korur.',
              'Buzlu cam kartlar', 'Temayı olduğu gibi kullanın ya da görünümünü adım adım ayarlayın. Her şey daha sonra kaplama ayarlarından değiştirilebilir.',
              'Kütüphane görünümlerindeki ayar şeridinin nasıl görüneceği: görünümün üzerinde (Kaplama) ya da her zaman yanında (Kalıcı).',
              'Ana ekranın kenarlarının menü ve metnin arkasında ne kadar kararacağı.', 'Aeon paletiyle saat kutusunun ve köşe kutularının rengi.',
              'Kaplamaya gösterecek daha çok şey veren isteğe bağlı eklentiler. İstediklerinizi kurun; gerisi bekleyebilir.'),
    'uk_ua': ('Fused Glass підносить картки з матового скла над зображеннями. Aeon малює суцільні панелі з яскравою смугою фокуса. Aeon Glass зберігає розкладку Aeon у напівпрозорих панелях.',
              'Картки з матового скла', 'Візьміть тему як є або налаштуйте її вигляд крок за кроком. Усе можна змінити пізніше в налаштуваннях оболонки.',
              'Як показується смуга налаштувань у видах медіатеки: поверх вигляду (Накладка) або завжди поруч (Постійно).',
              'Наскільки темніють краї головного екрана за меню й текстом.', 'Колір блока годинника та кутових блоків з палітрою Aeon.',
              'Додаткові доповнення, з якими оболонка покаже більше. Установіть потрібні; решта зачекає.'),
    'zh_cn': ('Fused Glass 让磨砂玻璃卡片浮在图片之上。Aeon 绘制实心面板和明亮的焦点条。Aeon Glass 以半透明面板保留 Aeon 布局。',
              '磨砂玻璃卡片', '按原样使用主题，或逐步设置它的外观。以后可在皮肤设置中更改一切。',
              '媒体库视图中设置条的显示方式：覆盖在视图上（覆盖）或始终在旁边（固定）。',
              '主页画面边缘在菜单和文字后面变暗的程度。', '使用 Aeon 调色板时时钟框和角落框的颜色。',
              '让皮肤显示更多内容的可选附加组件。安装你想要的；其余的可以以后再说。'),
    'zh_tw': ('Fused Glass 讓霧面玻璃卡片浮在圖片之上。Aeon 繪製實心面板和明亮的焦點條。Aeon Glass 以半透明面板保留 Aeon 版面。',
              '霧面玻璃卡片', '依原樣使用主題，或逐步設定它的外觀。之後可在外觀設定中變更一切。',
              '媒體庫檢視中設定條的顯示方式：覆蓋在檢視上（覆蓋）或一直在旁邊（固定）。',
              '首頁畫面邊緣在選單和文字後面變暗的程度。', '使用 Aeon 調色盤時時鐘框和角落框的顏色。',
              '讓外觀顯示更多內容的選用附加元件。安裝你想要的；其餘的可以之後再說。'),
}


def esc(s):
    return s.replace('"', '\\"')


def main():
    for code, row in T.items():
        assert len(row) == len(EN), (code, len(row))
    for d in sorted(os.listdir(L)):
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        if 'msgctxt "#32713"' in t:
            continue
        code = d.replace('resource.language.', '')
        add = ''
        for i, (sid, en) in enumerate(EN):
            tr = '' if code == 'en_gb' else T[code][i]
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), esc(tr))
        t = t.rstrip('\n') + '\n' + add
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        print(d, 'ok')


if __name__ == '__main__':
    main()
