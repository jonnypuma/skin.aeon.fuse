"""0.56.31 renames (the user, 2026-11-17): 32415 Landing animation -> Navigation animation,
32474 Toasts from the clock pill -> Toast expand from clock pill, in all 23 languages. Repeatable."""
import io
import os
import re

L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'language')
EN = {32415: 'Navigation animation', 32474: 'Toast expand from clock pill'}
T = {
    'cs_cz': ('Animace navigace', 'Oznámení rozbalená z kapsle s hodinami'),
    'da_dk': ('Navigationsanimation', 'Meddelelser udvides fra urets kapsel'),
    'de_de': ('Navigationsanimation', 'Meldungen klappen aus der Uhr-Kapsel auf'),
    'el_gr': ('Κίνηση πλοήγησης', 'Ειδοποιήσεις που ανοίγουν από την κάψουλα του ρολογιού'),
    'es_es': ('Animación de navegación', 'Avisos que se despliegan desde la cápsula del reloj'),
    'fi_fi': ('Navigoinnin animaatio', 'Ilmoitukset laajenevat kellokapselista'),
    'fr_fr': ('Animation de navigation', "Notifications dépliées depuis la capsule de l'horloge"),
    'hu_hu': ('Navigációs animáció', 'Értesítések kinyílva az óra kapszulájából'),
    'it_it': ('Animazione di navigazione', "Notifiche che si espandono dalla capsula dell'orologio"),
    'ja_jp': ('ナビゲーションの動き', '時計のピルから広がる通知'),
    'ko_kr': ('탐색 애니메이션', '시계 알약에서 펼쳐지는 알림'),
    'nb_no': ('Navigasjonsanimasjon', 'Varsler som utvides fra klokkekapselen'),
    'nl_nl': ('Navigatieanimatie', 'Meldingen klappen uit de klokcapsule'),
    'pl_pl': ('Animacja nawigacji', 'Powiadomienia rozwijane z kapsuły zegara'),
    'pt_br': ('Animação de navegação', 'Avisos que se expandem da cápsula do relógio'),
    'pt_pt': ('Animação de navegação', 'Avisos que se expandem da cápsula do relógio'),
    'ru_ru': ('Анимация навигации', 'Уведомления раскрываются из капсулы часов'),
    'sv_se': ('Navigeringsanimering', 'Aviseringar som fälls ut från klockkapseln'),
    'tr_tr': ('Gezinme animasyonu', 'Saat kapsülünden açılan bildirimler'),
    'uk_ua': ('Анімація навігації', 'Сповіщення розгортаються з капсули годинника'),
    'zh_cn': ('导航动画', '从时钟胶囊展开通知'),
    'zh_tw': ('導覽動畫', '從時鐘膠囊展開通知'),
}


def put(text, sid, msgid, msgstr):
    pat = re.compile(r'(msgctxt "#%d"\nmsgid ")(.*)("\nmsgstr ")(.*)(")' % sid)
    m = pat.search(text)
    assert m, sid
    return text[:m.start()] + m.group(1) + msgid + m.group(3) + msgstr + m.group(5) + text[m.end():]


for d in sorted(os.listdir(L)):
    p = os.path.join(L, d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    code = d.replace('resource.language.', '')
    for i, sid in enumerate((32415, 32474)):
        t = put(t, sid, EN[sid], '' if code == 'en_gb' else T[code][i])
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print(d, 'ok')
