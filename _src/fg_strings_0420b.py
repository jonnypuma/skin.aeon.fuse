# -*- coding: utf-8 -*-
"""0.42.0 strings for Fused Glass Home > System: 32502-32509. Run from the skin folder."""
import io
import os

EN = {
    32502: 'Health',
    32503: 'All good',
    32504: 'Running warm',
    32505: 'Memory almost full',
    32506: 'Processor',
    32507: 'Shortcuts',
    32508: 'Recently used add-ons',
    32509: 'Library jobs',
}
TR = {
    'cs_cz': ('Stav', 'Vše v pořádku', 'Zahřívá se', 'Paměť je téměř plná', 'Procesor', 'Zkratky', 'Nedávno použité doplňky', 'Úlohy knihovny'),
    'da_dk': ('Tilstand', 'Alt er fint', 'Kører varmt', 'Hukommelsen er næsten fuld', 'Processor', 'Genveje', 'Senest brugte tilføjelser', 'Biblioteksopgaver'),
    'de_de': ('Zustand', 'Alles in Ordnung', 'Läuft warm', 'Speicher fast voll', 'Prozessor', 'Verknüpfungen', 'Zuletzt benutzte Add-ons', 'Bibliotheksaufgaben'),
    'el_gr': ('Κατάσταση', 'Όλα καλά', 'Ζεσταίνεται', 'Η μνήμη σχεδόν γεμάτη', 'Επεξεργαστής', 'Συντομεύσεις', 'Πρόσφατα πρόσθετα', 'Εργασίες βιβλιοθήκης'),
    'es_es': ('Estado', 'Todo bien', 'Algo caliente', 'Memoria casi llena', 'Procesador', 'Accesos directos', 'Complementos usados hace poco', 'Tareas de biblioteca'),
    'fi_fi': ('Kunto', 'Kaikki kunnossa', 'Käy lämpimänä', 'Muisti lähes täynnä', 'Suoritin', 'Pikakuvakkeet', 'Viimeksi käytetyt lisäosat', 'Kirjaston tehtävät'),
    'fr_fr': ('État', 'Tout va bien', 'Chauffe un peu', 'Mémoire presque pleine', 'Processeur', 'Raccourcis', 'Extensions utilisées récemment', 'Tâches de la médiathèque'),
    'hu_hu': ('Állapot', 'Minden rendben', 'Melegszik', 'A memória majdnem megtelt', 'Processzor', 'Parancsikonok', 'Nemrég használt kiegészítők', 'Médiatár-feladatok'),
    'it_it': ('Stato', 'Tutto bene', 'Un po\' caldo', 'Memoria quasi piena', 'Processore', 'Scorciatoie', 'Add-on usati di recente', 'Operazioni libreria'),
    'ja_jp': ('状態', '問題なし', '温度が高め', 'メモリがほぼいっぱい', 'プロセッサー', 'ショートカット', '最近使ったアドオン', 'ライブラリの作業'),
    'ko_kr': ('상태', '모두 정상', '온도가 높음', '메모리가 거의 가득 참', '프로세서', '바로 가기', '최근 사용한 애드온', '라이브러리 작업'),
    'nb_no': ('Tilstand', 'Alt er bra', 'Går varm', 'Minnet er nesten fullt', 'Prosessor', 'Snarveier', 'Nylig brukte tillegg', 'Bibliotekoppgaver'),
    'nl_nl': ('Conditie', 'Alles in orde', 'Wordt warm', 'Geheugen bijna vol', 'Processor', 'Snelkoppelingen', 'Recent gebruikte add-ons', 'Bibliotheektaken'),
    'pl_pl': ('Stan', 'Wszystko w porządku', 'Nagrzewa się', 'Pamięć prawie pełna', 'Procesor', 'Skróty', 'Ostatnio używane dodatki', 'Zadania biblioteki'),
    'pt_br': ('Estado', 'Tudo certo', 'Esquentando', 'Memória quase cheia', 'Processador', 'Atalhos', 'Complementos usados recentemente', 'Tarefas da biblioteca'),
    'pt_pt': ('Estado', 'Tudo bem', 'A aquecer', 'Memória quase cheia', 'Processador', 'Atalhos', 'Extras usados recentemente', 'Tarefas da biblioteca'),
    'ru_ru': ('Состояние', 'Всё в порядке', 'Греется', 'Память почти заполнена', 'Процессор', 'Ярлыки', 'Недавние дополнения', 'Задачи медиатеки'),
    'sv_se': ('Skick', 'Allt är bra', 'Går varm', 'Minnet är nästan fullt', 'Processor', 'Genvägar', 'Senast använda tillägg', 'Biblioteksjobb'),
    'tr_tr': ('Durum', 'Her şey yolunda', 'Isınıyor', 'Bellek neredeyse dolu', 'İşlemci', 'Kısayollar', 'Son kullanılan eklentiler', 'Kütüphane işleri'),
    'uk_ua': ('Стан', 'Усе гаразд', 'Нагрівається', 'Пам\'ять майже заповнена', 'Процесор', 'Ярлики', 'Нещодавні доповнення', 'Завдання медіатеки'),
    'zh_cn': ('状态', '一切正常', '温度偏高', '内存快满了', '处理器', '快捷方式', '最近使用的附加组件', '媒体库任务'),
    'zh_tw': ('狀態', '一切正常', '溫度偏高', '記憶體快滿了', '處理器', '捷徑', '最近使用的附加元件', '媒體櫃工作'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32502"' in t:
        continue
    tr = TR.get(lang)
    assert tr or lang == 'en_gb', lang
    assert lang == 'en_gb' or len(tr) == len(EN), lang
    t = t.rstrip('\n') + '\n'
    for i, ident in enumerate(sorted(EN)):
        msgid = EN[ident].replace('"', '\\"')
        msgstr = '' if lang == 'en_gb' else tr[i].replace('"', '\\"')
        t += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (ident, msgid, msgstr)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    done += 1
print('strings 32502-32509 added in %d languages' % done)
