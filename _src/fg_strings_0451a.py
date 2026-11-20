# -*- coding: utf-8 -*-
"""0.45.1 strings: Planner Earlier days, Home menu names in capitals: 32552-32555. Run from the skin folder."""
import io
import os

EN = {
    32552: 'Earlier days',
    32553: 'Also show what aired on the days of this week before today (episodes in your library).',
    32554: 'Menu names in capitals',
    32555: 'Fused Glass: the Home menu names in capital letters instead of sentence case.',
}
TR = {
    'cs_cz': ('Dřívější dny', 'Zobrazit i to, co vyšlo v dnech tohoto týdne před dneškem (díly v knihovně).', 'Názvy nabídky velkými písmeny', 'Fused Glass: názvy v domovské nabídce velkými písmeny.'),
    'da_dk': ('Tidligere dage', 'Vis også, hvad der blev sendt på ugens dage før i dag (afsnit i biblioteket).', 'Menunavne med store bogstaver', 'Fused Glass: navnene i hjemmemenuen med store bogstaver.'),
    'de_de': ('Frühere Tage', 'Auch zeigen, was an den Tagen dieser Woche vor heute lief (Folgen in der Bibliothek).', 'Menünamen in Großbuchstaben', 'Fused Glass: die Namen im Hauptmenü in Großbuchstaben.'),
    'el_gr': ('Προηγούμενες ημέρες', 'Εμφάνιση και όσων προβλήθηκαν τις ημέρες της εβδομάδας πριν από σήμερα (επεισόδια στη βιβλιοθήκη).', 'Ονόματα μενού με κεφαλαία', 'Fused Glass: τα ονόματα του αρχικού μενού με κεφαλαία.'),
    'es_es': ('Días anteriores', 'Mostrar también lo emitido en los días de esta semana antes de hoy (episodios de la biblioteca).', 'Nombres del menú en mayúsculas', 'Fused Glass: los nombres del menú de inicio en mayúsculas.'),
    'fi_fi': ('Aiemmat päivät', 'Näytä myös, mitä tuli tämän viikon päivinä ennen tätä päivää (kirjaston jaksot).', 'Valikon nimet isoilla kirjaimilla', 'Fused Glass: aloitusvalikon nimet isoilla kirjaimilla.'),
    'fr_fr': ('Jours précédents', "Montrer aussi ce qui est sorti les jours de cette semaine avant aujourd'hui (épisodes de la médiathèque).", 'Noms du menu en majuscules', "Fused Glass : les noms du menu d'accueil en majuscules."),
    'hu_hu': ('Korábbi napok', 'Mutassa azt is, mi jelent meg a hét mai nap előtti napjain (epizódok a médiatárban).', 'Menünevek nagybetűvel', 'Fused Glass: a főmenü nevei nagybetűvel.'),
    'it_it': ('Giorni precedenti', 'Mostra anche cosa è uscito nei giorni di questa settimana prima di oggi (episodi in libreria).', 'Nomi del menu in maiuscolo', 'Fused Glass: i nomi del menu Home in maiuscolo.'),
    'ja_jp': ('前の日', '今週の今日より前の日に放送されたもの (ライブラリのエピソード) も表示します。', 'メニュー名を大文字に', 'Fused Glass: ホームメニューの名前を大文字で表示します。'),
    'ko_kr': ('이전 날짜', '이번 주 오늘 이전 날에 방영된 것도 표시 (라이브러리의 에피소드).', '메뉴 이름 대문자', 'Fused Glass: 홈 메뉴 이름을 대문자로 표시합니다.'),
    'nb_no': ('Tidligere dager', 'Vis også hva som ble sendt på ukens dager før i dag (episoder i biblioteket).', 'Menynavn med store bokstaver', 'Fused Glass: navnene i hjemmemenyen med store bokstaver.'),
    'nl_nl': ('Eerdere dagen', 'Ook tonen wat er deze week vóór vandaag uitkwam (afleveringen in je bibliotheek).', 'Menunamen in hoofdletters', 'Fused Glass: de namen in het hoofdmenu in hoofdletters.'),
    'pl_pl': ('Wcześniejsze dni', 'Pokaż też, co wyszło w dniach tego tygodnia przed dziś (odcinki w bibliotece).', 'Nazwy menu wielkimi literami', 'Fused Glass: nazwy w menu głównym wielkimi literami.'),
    'pt_br': ('Dias anteriores', 'Mostrar também o que estreou nos dias desta semana antes de hoje (episódios da biblioteca).', 'Nomes do menu em maiúsculas', 'Fused Glass: os nomes do menu inicial em maiúsculas.'),
    'pt_pt': ('Dias anteriores', 'Mostrar também o que estreou nos dias desta semana antes de hoje (episódios da biblioteca).', 'Nomes do menu em maiúsculas', 'Fused Glass: os nomes do menu inicial em maiúsculas.'),
    'ru_ru': ('Прошедшие дни', 'Показывать и то, что вышло в дни этой недели до сегодня (серии в медиатеке).', 'Названия меню заглавными', 'Fused Glass: названия в главном меню заглавными буквами.'),
    'sv_se': ('Tidigare dagar', 'Visa också vad som sändes veckans dagar före i dag (avsnitt i biblioteket).', 'Menynamn med versaler', 'Fused Glass: namnen i hemmenyn med versaler.'),
    'tr_tr': ('Önceki günler', 'Bu haftanın bugünden önceki günlerinde yayınlananları da göster (kütüphanedeki bölümler).', 'Menü adları büyük harfle', 'Fused Glass: ana menü adları büyük harflerle.'),
    'uk_ua': ('Минулі дні', 'Показувати й те, що вийшло в дні цього тижня до сьогодні (серії в медіатеці).', 'Назви меню великими', 'Fused Glass: назви в головному меню великими літерами.'),
    'zh_cn': ('之前的日子', '也显示本周今天之前播出的内容（媒体库中的剧集）。', '菜单名称大写', 'Fused Glass：主菜单名称使用大写字母。'),
    'zh_tw': ('之前的日子', '也顯示本週今天之前播出的內容（媒體櫃中的劇集）。', '選單名稱大寫', 'Fused Glass：主選單名稱使用大寫字母。'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32552"' in t:
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
print('strings 32552-32555 added in %d languages' % done)
