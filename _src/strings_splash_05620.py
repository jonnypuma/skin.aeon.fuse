# -*- coding: utf-8 -*-
"""0.56.20 strings for the start-up splash: Getting Home ready (32622), Home rows (32623) OK or Back
skips (32624) and Live TV guide (32625), every language. Safe to run again (an id already there is left alone)."""
import io
import os

S = {
    'en_gb': ('Getting Home ready', 'Home rows', 'OK or Back skips', 'Live TV guide'),
    'cs_cz': ('Připravuje se Domů', 'Řádky Domů', 'OK nebo Zpět přeskočí', 'TV průvodce'),
    'da_dk': ('Gør Hjem klar', 'Rækker på Hjem', 'OK eller Tilbage springer over', 'TV-guide'),
    'de_de': ('Startseite wird vorbereitet', 'Zeilen der Startseite', 'OK oder Zurück überspringt', 'TV-Programm'),
    'el_gr': ('Προετοιμασία της Αρχικής', 'Σειρές της Αρχικής', 'OK ή Πίσω για παράλειψη', 'Οδηγός TV'),
    'es_es': ('Preparando Inicio', 'Filas de Inicio', 'OK o Atrás para saltar', 'Guía de TV'),
    'fi_fi': ('Kotinäkymää valmistellaan', 'Kotinäkymän rivit', 'OK tai Takaisin ohittaa', 'TV-opas'),
    'fr_fr': ("Préparation de l'accueil", "Rangées de l'accueil", 'OK ou Retour pour passer', 'Guide TV'),
    'hu_hu': ('Kezdőlap előkészítése', 'Kezdőlap sorai', 'OK vagy Vissza: kihagyás', 'TV-műsor'),
    'it_it': ('Preparazione della Home', 'Righe della Home', 'OK o Indietro per saltare', 'Guida TV'),
    'ja_jp': ('ホームを準備中', 'ホームの行', 'OK または戻るでスキップ', '番組表'),
    'ko_kr': ('홈 준비 중', '홈 행', '확인 또는 뒤로로 건너뛰기', 'TV 편성표'),
    'nb_no': ('Gjør Hjem klar', 'Rader på Hjem', 'OK eller Tilbake hopper over', 'TV-guide'),
    'nl_nl': ('Startscherm wordt klaargezet', 'Rijen van het startscherm', 'OK of Terug slaat over', 'Tv-gids'),
    'pl_pl': ('Przygotowywanie ekranu głównego', 'Rzędy ekranu głównego', 'OK lub Wstecz pomija', 'Program TV'),
    'pt_br': ('Preparando o Início', 'Linhas do Início', 'OK ou Voltar pula', 'Guia de TV'),
    'pt_pt': ('A preparar o Início', 'Linhas do Início', 'OK ou Voltar salta', 'Guia de TV'),
    'ru_ru': ('Подготовка главного экрана', 'Строки главного экрана', 'OK или Назад — пропустить', 'Телепрограмма'),
    'sv_se': ('Gör Hem redo', 'Rader på Hem', 'OK eller Tillbaka hoppar över', 'TV-guide'),
    'tr_tr': ('Ana ekran hazırlanıyor', 'Ana ekran satırları', 'Geçmek için Tamam veya Geri', 'TV rehberi'),
    'uk_ua': ('Підготовка головного екрана', 'Рядки головного екрана', 'OK або Назад — пропустити', 'Телепрограма'),
    'zh_cn': ('正在准备主页', '主页行', '按确定或返回跳过', '电视节目表'),
    'zh_tw': ('正在準備首頁', '首頁列', '按確定或返回略過', '電視節目表'),
}
EN = S['en_gb']


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main():
    for folder in sorted(os.listdir('language')):
        lang = folder.replace('resource.language.', '')
        p = os.path.join('language', folder, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        tr = S.get(lang)
        assert tr, lang
        add = ''
        for sid, en, local in ((32622, EN[0], tr[0]), (32623, EN[1], tr[1]), (32624, EN[2], tr[2]), (32625, EN[3], tr[3])):
            if 'msgctxt "#%d"' % sid in t:
                continue
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), '' if lang == 'en_gb' else esc(local))
        if add:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)
    print('ok', len(os.listdir('language')))


if __name__ == '__main__':
    main()
