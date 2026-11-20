# -*- coding: utf-8 -*-
"""0.42.0 strings for Fused Glass Home > Power: 32489-32493, 32495-32501. Run from the skin folder."""
import io
import os

EN = {
    32489: 'Kodi running for',
    32490: 'Box up for',
    32491: 'Nothing is playing',
    32492: 'Sleep',
    32493: 'Restart Kodi',
    32495: 'Reboot to Android',
    32496: 'Shut down',
    32497: 'OK again to confirm',
    32498: 'Log off',
    32499: 'Exit Kodi',
    32500: 'When this ends',
    32501: 'min',
}
TR = {
    'cs_cz': ('Kodi běží', 'Zařízení běží', 'Nic se nepřehrává', 'Spánek', 'Restartovat Kodi', 'Restartovat do Androidu', 'Vypnout', 'Potvrďte dalším OK', 'Odhlásit', 'Ukončit Kodi', 'Až toto skončí', 'min'),
    'da_dk': ('Kodi har kørt i', 'Boksen har kørt i', 'Intet afspilles', 'Dvale', 'Genstart Kodi', 'Genstart til Android', 'Sluk', 'OK igen for at bekræfte', 'Log af', 'Afslut Kodi', 'Når dette slutter', 'min'),
    'de_de': ('Kodi läuft seit', 'Box läuft seit', 'Es läuft nichts', 'Ruhezustand', 'Kodi neu starten', 'In Android neu starten', 'Ausschalten', 'Zum Bestätigen noch einmal OK', 'Abmelden', 'Kodi beenden', 'Wenn das hier endet', 'Min.'),
    'el_gr': ('Το Kodi τρέχει', 'Η συσκευή τρέχει', 'Δεν παίζει τίποτα', 'Αναστολή', 'Επανεκκίνηση Kodi', 'Επανεκκίνηση σε Android', 'Τερματισμός', 'Ξανά OK για επιβεβαίωση', 'Αποσύνδεση', 'Έξοδος από το Kodi', 'Όταν τελειώσει αυτό', 'λεπ.'),
    'es_es': ('Kodi lleva encendido', 'El equipo lleva encendido', 'No se reproduce nada', 'Suspender', 'Reiniciar Kodi', 'Reiniciar en Android', 'Apagar', 'OK otra vez para confirmar', 'Cerrar sesión', 'Salir de Kodi', 'Cuando esto termine', 'min'),
    'fi_fi': ('Kodi käynnissä', 'Laite käynnissä', 'Mitään ei toisteta', 'Lepotila', 'Käynnistä Kodi uudelleen', 'Käynnistä Androidiin', 'Sammuta', 'Vahvista painamalla OK uudelleen', 'Kirjaudu ulos', 'Sulje Kodi', 'Kun tämä päättyy', 'min'),
    'fr_fr': ('Kodi tourne depuis', 'La box tourne depuis', 'Rien en lecture', 'Veille', 'Redémarrer Kodi', 'Redémarrer sous Android', 'Éteindre', 'OK encore pour confirmer', 'Se déconnecter', 'Quitter Kodi', 'À la fin de ceci', 'min'),
    'hu_hu': ('A Kodi fut', 'Az eszköz fut', 'Nincs lejátszás', 'Alvás', 'Kodi újraindítása', 'Újraindítás Androidra', 'Leállítás', 'Megerősítéshez újra OK', 'Kijelentkezés', 'Kilépés a Kodiból', 'Amikor ez véget ér', 'perc'),
    'it_it': ('Kodi acceso da', 'Box acceso da', 'Niente in riproduzione', 'Sospendi', 'Riavvia Kodi', 'Riavvia in Android', 'Spegni', 'Di nuovo OK per confermare', 'Esci dal profilo', 'Esci da Kodi', 'Alla fine di questo', 'min'),
    'ja_jp': ('Kodi の稼働時間', '本体の稼働時間', '再生していません', 'スリープ', 'Kodi を再起動', 'Android で再起動', 'シャットダウン', 'もう一度 OK で確定', 'ログオフ', 'Kodi を終了', '再生が終わったら', '分'),
    'ko_kr': ('Kodi 실행 시간', '기기 실행 시간', '재생 중인 항목 없음', '절전', 'Kodi 다시 시작', 'Android로 재부팅', '종료', '확인하려면 OK를 한 번 더', '로그오프', 'Kodi 끝내기', '이 항목이 끝나면', '분'),
    'nb_no': ('Kodi har kjørt i', 'Boksen har kjørt i', 'Ingenting spilles', 'Dvale', 'Start Kodi på nytt', 'Start på nytt i Android', 'Slå av', 'OK igjen for å bekrefte', 'Logg av', 'Avslutt Kodi', 'Når dette slutter', 'min'),
    'nl_nl': ('Kodi draait al', 'Box draait al', 'Er speelt niets', 'Slaapstand', 'Kodi herstarten', 'Herstarten naar Android', 'Uitschakelen', 'Nogmaals OK om te bevestigen', 'Afmelden', 'Kodi afsluiten', 'Als dit afgelopen is', 'min'),
    'pl_pl': ('Kodi działa od', 'Urządzenie działa od', 'Nic nie jest odtwarzane', 'Uśpij', 'Uruchom ponownie Kodi', 'Uruchom ponownie w Androidzie', 'Wyłącz', 'Ponownie OK, aby potwierdzić', 'Wyloguj', 'Zamknij Kodi', 'Gdy to się skończy', 'min'),
    'pt_br': ('Kodi ligado há', 'Aparelho ligado há', 'Nada sendo reproduzido', 'Suspender', 'Reiniciar o Kodi', 'Reiniciar no Android', 'Desligar', 'OK de novo para confirmar', 'Sair da conta', 'Sair do Kodi', 'Quando isto acabar', 'min'),
    'pt_pt': ('Kodi ligado há', 'Box ligada há', 'Nada em reprodução', 'Suspender', 'Reiniciar o Kodi', 'Reiniciar no Android', 'Desligar', 'OK novamente para confirmar', 'Terminar sessão', 'Sair do Kodi', 'Quando isto terminar', 'min'),
    'ru_ru': ('Kodi работает', 'Приставка работает', 'Ничего не воспроизводится', 'Сон', 'Перезапустить Kodi', 'Перезагрузить в Android', 'Выключить', 'Ещё раз OK для подтверждения', 'Выйти из профиля', 'Выйти из Kodi', 'Когда это закончится', 'мин'),
    'sv_se': ('Kodi har körts i', 'Boxen har körts i', 'Inget spelas', 'Viloläge', 'Starta om Kodi', 'Starta om i Android', 'Stäng av', 'OK igen för att bekräfta', 'Logga ut', 'Avsluta Kodi', 'När detta slutar', 'min'),
    'tr_tr': ('Kodi çalışma süresi', 'Cihaz çalışma süresi', 'Hiçbir şey oynatılmıyor', 'Uyku', 'Kodi\'yi yeniden başlat', 'Android\'e yeniden başlat', 'Kapat', 'Onaylamak için yine OK', 'Oturumu kapat', 'Kodi\'den çık', 'Bu bittiğinde', 'dk'),
    'uk_ua': ('Kodi працює', 'Приставка працює', 'Нічого не відтворюється', 'Сон', 'Перезапустити Kodi', 'Перезавантажити в Android', 'Вимкнути', 'Ще раз OK для підтвердження', 'Вийти з профілю', 'Вийти з Kodi', 'Коли це закінчиться', 'хв'),
    'zh_cn': ('Kodi 已运行', '设备已运行', '没有播放内容', '睡眠', '重启 Kodi', '重启到 Android', '关机', '再按一次 OK 确认', '注销', '退出 Kodi', '播放结束时', '分钟'),
    'zh_tw': ('Kodi 已執行', '裝置已執行', '沒有播放內容', '睡眠', '重新啟動 Kodi', '重新啟動到 Android', '關機', '再按一次 OK 確認', '登出', '結束 Kodi', '播放結束時', '分鐘'),
}

done = 0
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32489"' in t:
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
print('strings 32489-32501 added in %d languages' % done)
