"""0.56.39 Panel shadow help (32669): how high the panels float, not a rim. All 23 languages. Repeatable."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
EN = 'How high the glass panels seem to float: their shadow grows and drops. Mild: close to the page. Medium: as before. Strong: higher. Heavy: highest.'
T = {
    'cs_cz': 'Jak vysoko se skleněné panely zdají vznášet: jejich stín roste a klesá. Mírný: těsně nad stránkou. Střední: jako dosud. Silný: výš. Těžký: nejvýš.',
    'da_dk': 'Hvor højt glaspanelerne ser ud til at svæve: deres skygge vokser og falder. Mild: tæt på siden. Medium: som før. Stærk: højere. Kraftig: højest.',
    'de_de': 'Wie hoch die Glasflächen zu schweben scheinen: ihr Schatten wird größer und tiefer. Mild: nah an der Seite. Mittel: wie bisher. Stark: höher. Kräftig: am höchsten.',
    'el_gr': 'Πόσο ψηλά φαίνεται να αιωρούνται τα γυάλινα πάνελ: η σκιά τους μεγαλώνει και κατεβαίνει. Ήπια: κοντά στη σελίδα. Μέτρια: όπως πριν. Έντονη: ψηλότερα. Βαριά: ψηλότερα από όλα.',
    'es_es': 'Lo alto que parecen flotar los paneles de cristal: su sombra crece y baja. Suave: cerca de la página. Media: como antes. Fuerte: más alto. Intensa: lo más alto.',
    'fi_fi': 'Kuinka korkealla lasipaneelit näyttävät leijuvan: niiden varjo kasvaa ja laskee. Mieto: lähellä sivua. Keskitaso: kuten ennen. Vahva: korkeammalla. Raskas: korkeimmalla.',
    'fr_fr': "La hauteur à laquelle les panneaux de verre semblent flotter : leur ombre grandit et descend. Douce : près de la page. Moyenne : comme avant. Forte : plus haut. Intense : le plus haut.",
    'hu_hu': 'Milyen magasan látszanak lebegni az üvegpanelek: az árnyékuk nő és lejjebb kerül. Enyhe: közel a laphoz. Közepes: mint eddig. Erős: magasabban. Nehéz: a legmagasabban.',
    'it_it': "Quanto in alto sembrano fluttuare i pannelli di vetro: la loro ombra cresce e scende. Lieve: vicino alla pagina. Media: come prima. Forte: più in alto. Intensa: il più in alto.",
    'ja_jp': 'ガラスのパネルがどれだけ高く浮いて見えるか：影が大きく、下に伸びます。弱：ページの近く。中：これまで通り。強：より高く。最強：最も高く。',
    'ko_kr': '유리 패널이 얼마나 높이 떠 보이는지: 그림자가 커지고 아래로 내려갑니다. 약하게: 페이지 가까이. 보통: 이전과 같음. 강하게: 더 높이. 아주 강하게: 가장 높이.',
    'nb_no': 'Hvor høyt glasspanelene ser ut til å sveve: skyggen deres vokser og synker. Mild: nær siden. Middels: som før. Sterk: høyere. Kraftig: høyest.',
    'nl_nl': 'Hoe hoog de glazen panelen lijken te zweven: hun schaduw groeit en zakt. Mild: dicht bij de pagina. Gemiddeld: zoals voorheen. Sterk: hoger. Zwaar: het hoogst.',
    'pl_pl': 'Jak wysoko zdają się unosić szklane panele: ich cień rośnie i opada. Łagodny: blisko strony. Średni: jak dotąd. Mocny: wyżej. Ciężki: najwyżej.',
    'pt_br': 'Quão alto os painéis de vidro parecem flutuar: a sombra deles cresce e desce. Suave: perto da página. Média: como antes. Forte: mais alto. Intensa: o mais alto.',
    'pt_pt': 'Quão alto os painéis de vidro parecem flutuar: a sombra deles cresce e desce. Suave: perto da página. Média: como antes. Forte: mais alto. Intensa: o mais alto.',
    'ru_ru': 'Насколько высоко кажутся парящими стеклянные панели: их тень растёт и опускается. Мягкая: близко к странице. Средняя: как раньше. Сильная: выше. Тяжёлая: выше всего.',
    'sv_se': 'Hur högt glaspanelerna verkar sväva: deras skugga växer och sjunker. Mild: nära sidan. Medel: som förut. Stark: högre. Kraftig: högst.',
    'tr_tr': 'Cam panellerin ne kadar yüksekte süzülüyor görüneceği: gölgeleri büyür ve aşağı iner. Hafif: sayfaya yakın. Orta: eskisi gibi. Güçlü: daha yüksek. Ağır: en yüksek.',
    'uk_ua': 'Наскільки високо здаються ширяти скляні панелі: їхня тінь зростає й опускається. М’яка: близько до сторінки. Середня: як раніше. Сильна: вище. Важка: найвище.',
    'zh_cn': '玻璃面板看起来浮得多高：阴影变大并下移。轻：贴近页面。中：与以前相同。强：更高。重：最高。',
    'zh_tw': '玻璃面板看起來浮得多高：陰影變大並下移。輕：貼近頁面。中：與以前相同。強：更高。重：最高。',
}
for d in sorted(os.listdir(L)):
    p = os.path.join(L, d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    code = d.replace('resource.language.', '')
    m = re.search(r'(msgctxt "#32669"\nmsgid ")(.*)("\nmsgstr ")(.*)(")', t)
    assert m, d
    t = t[:m.start()] + m.group(1) + EN + m.group(3) + ('' if code == 'en_gb' else T[code].replace('"', '\\"')) + m.group(5) + t[m.end():]
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('done')
