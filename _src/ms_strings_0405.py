# -*- coding: utf-8 -*-
"""0.40.5 strings 32472-32475: Band under the Home menu, Toasts from the clock pill (labels and help), all languages."""
import io
import os

EN = {
    32472: 'Band under the Home menu',
    32473: 'A dark band from the Home menu down to the bottom of the screen, with a thin line on top, over the spotlight pictures. It follows the menu: middle or low.',
    32474: 'Toasts from the clock pill',
    32475: 'A notification widens the clock pill to the left and shows itself in it, instead of a capsule of its own. Library views and full-screen video keep the capsule.',
}
TR = {
    'cs_cz': ('Pruh pod hlavní nabídkou', 'Tmavý pruh od hlavní nabídky až ke spodnímu okraji obrazovky s tenkou linkou nahoře, přes obrázky spotlightu. Řídí se nabídkou: uprostřed nebo dole.',
              'Oznámení z kapsle s hodinami', 'Oznámení rozšíří kapsli s hodinami doleva a zobrazí se v ní, místo vlastní kapsle. Zobrazení knihovny a video na celou obrazovku si kapsli ponechají.'),
    'da_dk': ('Bånd under hjemmemenuen', 'Et mørkt bånd fra hjemmemenuen ned til bunden af skærmen med en tynd linje øverst, over spotlight-billederne. Det følger menuen: midt eller lavt.',
              'Meddelelser fra urets kapsel', 'En meddelelse gør urets kapsel bredere mod venstre og vises i den i stedet for i sin egen kapsel. Biblioteksvisninger og video i fuld skærm beholder kapslen.'),
    'de_de': ('Band unter dem Hauptmenü', 'Ein dunkles Band vom Hauptmenü bis zum unteren Bildrand mit einer feinen Linie oben, über den Spotlight-Bildern. Es folgt dem Menü: mittig oder unten.',
              'Meldungen aus der Uhr-Kapsel', 'Eine Meldung verbreitert die Uhr-Kapsel nach links und erscheint darin statt in einer eigenen Kapsel. Bibliotheksansichten und Vollbildvideo behalten die Kapsel.'),
    'el_gr': ('Λωρίδα κάτω από το κεντρικό μενού', 'Μια σκούρα λωρίδα από το κεντρικό μενού ως το κάτω μέρος της οθόνης με μια λεπτή γραμμή στην κορυφή, πάνω από τις εικόνες του spotlight. Ακολουθεί το μενού: στη μέση ή χαμηλά.',
              'Ειδοποιήσεις από την κάψουλα του ρολογιού', 'Μια ειδοποίηση φαρδαίνει την κάψουλα του ρολογιού προς τα αριστερά και εμφανίζεται μέσα της, αντί για δική της κάψουλα. Οι προβολές βιβλιοθήκης και το βίντεο σε πλήρη οθόνη κρατούν την κάψουλα.'),
    'es_es': ('Banda bajo el menú de inicio', 'Una banda oscura desde el menú de inicio hasta el borde inferior de la pantalla, con una línea fina arriba, sobre las imágenes del spotlight. Sigue al menú: en el centro o abajo.',
              'Avisos desde la cápsula del reloj', 'Un aviso ensancha la cápsula del reloj hacia la izquierda y aparece dentro de ella, en lugar de en una cápsula propia. Las vistas de biblioteca y el vídeo a pantalla completa mantienen la cápsula.'),
    'fi_fi': ('Kaistale aloitusvalikon alla', 'Tumma kaistale aloitusvalikosta näytön alareunaan, ohut viiva ylhäällä, spotlight-kuvien päällä. Se seuraa valikkoa: keskellä tai alhaalla.',
              'Ilmoitukset kellokapselista', 'Ilmoitus leventää kellokapselia vasemmalle ja näkyy sen sisällä oman kapselin sijaan. Kirjastonäkymät ja koko näytön video pitävät kapselin.'),
    'fr_fr': ("Bande sous le menu d'accueil", "Une bande sombre du menu d'accueil jusqu'au bas de l'écran, avec un trait fin en haut, par-dessus les images du spotlight. Elle suit le menu : au milieu ou en bas.",
              "Notifications depuis la capsule de l'horloge", "Une notification élargit la capsule de l'horloge vers la gauche et s'y affiche, au lieu d'une capsule à elle. Les vues de la bibliothèque et la vidéo en plein écran gardent la capsule."),
    'hu_hu': ('Sáv a kezdőmenü alatt', 'Sötét sáv a kezdőmenütől a képernyő aljáig, felül vékony vonallal, a spotlight képei fölött. Követi a menüt: középen vagy lent.',
              'Értesítések az óra kapszulájából', 'Az értesítés balra kiszélesíti az óra kapszuláját, és abban jelenik meg saját kapszula helyett. A könyvtárnézetek és a teljes képernyős videó megtartják a kapszulát.'),
    'it_it': ('Fascia sotto il menu Home', "Una fascia scura dal menu Home fino al fondo dello schermo, con una linea sottile in alto, sopra le immagini dello spotlight. Segue il menu: al centro o in basso.",
              "Notifiche dalla capsula dell'orologio", "Una notifica allarga la capsula dell'orologio verso sinistra e vi compare dentro, invece che in una capsula propria. Le viste della libreria e il video a schermo intero mantengono la capsula."),
    'ja_jp': ('ホームメニューの下の帯', 'ホームメニューから画面の下端までの暗い帯。上端に細い線があり、スポットライトの画像の上に重なります。メニューの位置（中央または下）に合わせます。',
              '時計のピルから出る通知', '通知が時計のピルを左へ広げ、その中に表示されます（専用のカプセルの代わり）。ライブラリ表示と全画面の動画では今のカプセルのままです。'),
    'ko_kr': ('홈 메뉴 아래 띠', '홈 메뉴에서 화면 아래까지 이어지는 어두운 띠, 위쪽에 가는 선, 스포트라이트 그림 위에 놓입니다. 메뉴 위치(가운데 또는 아래)를 따릅니다.',
              '시계 알약에서 나오는 알림', '알림이 시계 알약을 왼쪽으로 넓히고 그 안에 나타납니다(자체 캡슐 대신). 라이브러리 보기와 전체 화면 동영상은 캡슐을 유지합니다.'),
    'nb_no': ('Bånd under hjemmemenyen', 'Et mørkt bånd fra hjemmemenyen ned til bunnen av skjermen med en tynn linje øverst, over spotlight-bildene. Det følger menyen: midt eller lavt.',
              'Varsler fra klokkekapselen', 'Et varsel gjør klokkekapselen bredere mot venstre og vises i den i stedet for i sin egen kapsel. Bibliotekvisninger og video i fullskjerm beholder kapselen.'),
    'nl_nl': ('Band onder het hoofdmenu', 'Een donkere band van het hoofdmenu tot de onderkant van het scherm, met een dunne lijn bovenaan, over de spotlightafbeeldingen. Hij volgt het menu: midden of laag.',
              'Meldingen uit de klokcapsule', 'Een melding maakt de klokcapsule naar links breder en verschijnt daarin, in plaats van in een eigen capsule. Bibliotheekweergaven en video op volledig scherm houden de capsule.'),
    'pl_pl': ('Pas pod menu głównym', 'Ciemny pas od menu głównego do dołu ekranu z cienką linią na górze, nad obrazami spotlightu. Podąża za menu: na środku lub nisko.',
              'Powiadomienia z kapsuły zegara', 'Powiadomienie poszerza kapsułę zegara w lewo i pojawia się w niej zamiast we własnej kapsule. Widoki biblioteki i wideo na pełnym ekranie zachowują kapsułę.'),
    'pt_br': ('Faixa sob o menu inicial', 'Uma faixa escura do menu inicial até a parte de baixo da tela, com uma linha fina em cima, sobre as imagens do spotlight. Ela segue o menu: no meio ou embaixo.',
              'Avisos saindo da cápsula do relógio', 'Um aviso alarga a cápsula do relógio para a esquerda e aparece dentro dela, em vez de numa cápsula própria. As visualizações da biblioteca e o vídeo em tela cheia mantêm a cápsula.'),
    'pt_pt': ('Faixa sob o menu inicial', 'Uma faixa escura do menu inicial até ao fundo do ecrã, com uma linha fina em cima, sobre as imagens do spotlight. Acompanha o menu: ao meio ou em baixo.',
              'Avisos a sair da cápsula do relógio', 'Um aviso alarga a cápsula do relógio para a esquerda e aparece dentro dela, em vez de numa cápsula própria. As vistas da biblioteca e o vídeo em ecrã inteiro mantêm a cápsula.'),
    'ru_ru': ('Полоса под главным меню', 'Тёмная полоса от главного меню до низа экрана с тонкой линией сверху, поверх изображений spotlight. Следует за меню: посередине или внизу.',
              'Уведомления из капсулы часов', 'Уведомление расширяет капсулу часов влево и появляется в ней, а не в собственной капсуле. Виды библиотеки и полноэкранное видео сохраняют капсулу.'),
    'sv_se': ('Band under hemmenyn', 'Ett mörkt band från hemmenyn ner till skärmens nederkant, med en tunn linje överst, över spotlightbilderna. Det följer menyn: mitten eller lågt.',
              'Aviseringar från klockkapseln', 'En avisering gör klockkapseln bredare åt vänster och visas i den i stället för i en egen kapsel. Biblioteksvyer och video i helskärm behåller kapseln.'),
    'tr_tr': ('Ana menünün altında şerit', 'Ana menüden ekranın altına kadar, üstünde ince bir çizgi olan koyu bir şerit; spotlight görsellerinin üstünde. Menüyü izler: ortada ya da aşağıda.',
              'Saat kapsülünden bildirimler', 'Bildirim saat kapsülünü sola doğru genişletir ve kendi kapsülü yerine onun içinde görünür. Kitaplık görünümleri ve tam ekran video kapsülü korur.'),
    'uk_ua': ('Смуга під головним меню', 'Темна смуга від головного меню до низу екрана з тонкою лінією вгорі, поверх зображень spotlight. Вона йде за меню: посередині або внизу.',
              'Сповіщення з капсули годинника', 'Сповіщення розширює капсулу годинника ліворуч і з’являється в ній, а не у власній капсулі. Види бібліотеки та повноекранне відео зберігають капсулу.'),
    'zh_cn': ('主页菜单下方的色带', '从主页菜单到屏幕底部的一条深色带，顶部有一条细线，位于聚光灯图片之上。它跟随菜单位置：中间或底部。',
              '从时钟胶囊弹出通知', '通知会把时钟胶囊向左加宽并显示在其中，而不是使用自己的胶囊。媒体库视图和全屏视频保留原来的胶囊。'),
    'zh_tw': ('主頁選單下方的色帶', '從主頁選單到螢幕底部的一條深色帶，頂端有一條細線，位於聚光燈圖片之上。它跟隨選單位置：中間或底部。',
              '從時鐘膠囊彈出通知', '通知會把時鐘膠囊向左加寬並顯示在其中，而不是使用自己的膠囊。媒體櫃檢視和全螢幕影片保留原來的膠囊。'),
}
done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32472"' in t:
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
print('strings 32472-32475 added in %d languages' % done)
