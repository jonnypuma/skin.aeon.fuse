# -*- coding: utf-8 -*-
"""0.56.20 strings for Skin settings > Spotlight & widgets > In cinemas now: films from (32619), its value Everywhere
(32620) and its help line (32621), every language. Safe to run again (an id already there is left alone)."""
import io
import os

S = {
    'en_gb': ('In cinemas now: films from', 'Everywhere',
              "In cinemas now (the screensaver and the widgets) is what TMDb Helper's country has in cinemas: the United States unless TMDb Helper's language is set to another country. Pick your country to keep only films made in the United States or there; Everywhere keeps them all."),
    'cs_cz': ('V kinech: filmy z', 'Odkudkoli',
              'V kinech (spořič a widgety) ukazuje, co je v kinech v zemi TMDb Helperu: ve Spojených státech, pokud jazyk TMDb Helperu není nastaven na jinou zemi. Vyberte svou zemi a zůstanou jen filmy natočené ve Spojených státech nebo v ní; Odkudkoli ponechá všechny.'),
    'da_dk': ('I biografen nu: film fra', 'Overalt',
              'I biografen nu (pauseskærm og widgets) er det, TMDb Helpers land har i biografen: USA, medmindre TMDb Helpers sprog er sat til et andet land. Vælg dit land for kun at beholde film lavet i USA eller dér; Overalt beholder dem alle.'),
    'de_de': ('Jetzt im Kino: Filme aus', 'Überall',
              'Jetzt im Kino (Bildschirmschoner und Widgets) zeigt, was im Land von TMDb Helper im Kino läuft: in den USA, sofern die Sprache von TMDb Helper nicht auf ein anderes Land gestellt ist. Wählen Sie Ihr Land, um nur Filme aus den USA oder von dort zu behalten; Überall behält alle.'),
    'el_gr': ('Τώρα στους κινηματογράφους: ταινίες από', 'Παντού',
              'Το Τώρα στους κινηματογράφους (προφύλαξη οθόνης και widgets) δείχνει ό,τι παίζεται στη χώρα του TMDb Helper: στις ΗΠΑ, εκτός αν η γλώσσα του TMDb Helper έχει οριστεί σε άλλη χώρα. Επιλέξτε τη χώρα σας για να μείνουν μόνο ταινίες από τις ΗΠΑ ή από εκεί· το Παντού τις κρατά όλες.'),
    'es_es': ('En cines ahora: películas de', 'Cualquier lugar',
              'En cines ahora (salvapantallas y widgets) muestra lo que hay en los cines del país de TMDb Helper: Estados Unidos, salvo que el idioma de TMDb Helper indique otro país. Elige tu país para dejar solo películas hechas en Estados Unidos o allí; Cualquier lugar las deja todas.'),
    'fi_fi': ('Nyt teattereissa: elokuvat maasta', 'Kaikkialta',
              'Nyt teattereissa (näytönsäästäjä ja widgetit) näyttää, mitä TMDb Helperin maan teattereissa pyörii: Yhdysvalloissa, ellei TMDb Helperin kieleksi ole asetettu toista maata. Valitse maasi, niin jäljelle jäävät vain Yhdysvalloissa tai siellä tehdyt elokuvat; Kaikkialta pitää kaikki.'),
    'fr_fr': ('Au cinéma : films de', 'Partout',
              "Au cinéma (économiseur d'écran et widgets) montre ce qui passe au cinéma dans le pays de TMDb Helper : les États-Unis, sauf si la langue de TMDb Helper indique un autre pays. Choisissez votre pays pour ne garder que les films faits aux États-Unis ou chez vous ; Partout les garde tous."),
    'hu_hu': ('Most a mozikban: filmek innen', 'Bárhonnan',
              'A Most a mozikban (képernyővédő és widgetek) azt mutatja, mi megy a mozikban a TMDb Helper országában: az Egyesült Államokban, hacsak a TMDb Helper nyelve nincs más országra állítva. Válassza ki az országát, és csak az Egyesült Államokban vagy ott készült filmek maradnak; a Bárhonnan mindet megtartja.'),
    'it_it': ('Ora al cinema: film da', 'Ovunque',
              "Ora al cinema (salvaschermo e widget) mostra cosa c'è al cinema nel paese di TMDb Helper: gli Stati Uniti, a meno che la lingua di TMDb Helper non indichi un altro paese. Scegli il tuo paese per tenere solo i film fatti negli Stati Uniti o lì; Ovunque li tiene tutti."),
    'ja_jp': ('上映中: 製作国', 'すべて',
              '上映中（スクリーンセーバーとウィジェット）は TMDb Helper の国で上映中の作品です: TMDb Helper の言語で別の国を選んでいなければアメリカ。国を選ぶと、アメリカまたはその国で製作された映画だけが残ります。「すべて」はすべて残します。'),
    'ko_kr': ('현재 상영작: 제작 국가', '전체',
              '현재 상영작(화면 보호기와 위젯)은 TMDb Helper 국가의 극장 상영작입니다: TMDb Helper 언어에서 다른 국가를 고르지 않았다면 미국. 국가를 고르면 미국 또는 그 나라에서 만든 영화만 남습니다. 전체는 모두 남깁니다.'),
    'nb_no': ('På kino nå: filmer fra', 'Overalt',
              'På kino nå (skjermsparer og widgeter) er det TMDb Helpers land har på kino: USA, med mindre TMDb Helpers språk er satt til et annet land. Velg landet ditt for å bare beholde filmer laget i USA eller der; Overalt beholder alle.'),
    'nl_nl': ('Nu in de bioscoop: films uit', 'Overal',
              'Nu in de bioscoop (schermbeveiliging en widgets) toont wat er draait in het land van TMDb Helper: de Verenigde Staten, tenzij de taal van TMDb Helper op een ander land staat. Kies je land om alleen films uit de Verenigde Staten of daar te houden; Overal houdt ze allemaal.'),
    'pl_pl': ('Teraz w kinach: filmy z', 'Wszędzie',
              'Teraz w kinach (wygaszacz i widżety) pokazuje, co grają kina w kraju TMDb Helper: w Stanach Zjednoczonych, chyba że język TMDb Helper wskazuje inny kraj. Wybierz swój kraj, aby zostały tylko filmy zrobione w Stanach Zjednoczonych lub tam; Wszędzie zostawia wszystkie.'),
    'pt_br': ('Em cartaz: filmes de', 'Qualquer lugar',
              'Em cartaz (protetor de tela e widgets) mostra o que está nos cinemas do país do TMDb Helper: os Estados Unidos, a menos que o idioma do TMDb Helper indique outro país. Escolha seu país para manter só filmes feitos nos Estados Unidos ou lá; Qualquer lugar mantém todos.'),
    'pt_pt': ('Em exibição: filmes de', 'Qualquer lado',
              'Em exibição (proteção de ecrã e widgets) mostra o que está nos cinemas do país do TMDb Helper: os Estados Unidos, a não ser que o idioma do TMDb Helper indique outro país. Escolha o seu país para manter só filmes feitos nos Estados Unidos ou lá; Qualquer lado mantém todos.'),
    'ru_ru': ('Сейчас в кино: фильмы из', 'Отовсюду',
              '«Сейчас в кино» (заставка и виджеты) показывает, что идёт в кинотеатрах страны TMDb Helper: в США, если язык TMDb Helper не задаёт другую страну. Выберите свою страну, чтобы остались только фильмы, снятые в США или там; «Отовсюду» оставляет все.'),
    'sv_se': ('På bio nu: filmer från', 'Överallt',
              'På bio nu (skärmsläckare och widgetar) visar vad som går på bio i TMDb Helpers land: USA, om inte TMDb Helpers språk är satt till ett annat land. Välj ditt land för att bara behålla filmer gjorda i USA eller där; Överallt behåller alla.'),
    'tr_tr': ('Şimdi sinemalarda: filmlerin ülkesi', 'Her yer',
              "Şimdi sinemalarda (ekran koruyucu ve widget'lar) TMDb Helper ülkesinde gösterimde olanları gösterir: TMDb Helper dili başka bir ülkeye ayarlı değilse ABD. Ülkenizi seçin, yalnızca ABD'de ya da orada yapılan filmler kalsın; Her yer hepsini tutar."),
    'uk_ua': ('Зараз у кіно: фільми з', 'Звідусіль',
              '«Зараз у кіно» (заставка й віджети) показує, що йде в кінотеатрах країни TMDb Helper: у США, якщо мова TMDb Helper не задає іншу країну. Виберіть свою країну, щоб лишилися тільки фільми, зняті в США або там; «Звідусіль» лишає всі.'),
    'zh_cn': ('正在上映：影片产地', '不限',
              '正在上映（屏幕保护和小部件）显示 TMDb Helper 所在国家正在上映的影片：除非 TMDb Helper 的语言设为其他国家，否则为美国。选择你的国家后，只保留美国或该国制作的影片；“不限”保留全部。'),
    'zh_tw': ('現正上映：影片產地', '不限',
              '現正上映（螢幕保護程式與小工具）顯示 TMDb Helper 所在國家正在上映的影片：除非 TMDb Helper 的語言設為其他國家，否則為美國。選擇你的國家後，只保留美國或該國製作的影片；「不限」保留全部。'),
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
        for sid, en, local in ((32619, EN[0], tr[0]), (32620, EN[1], tr[1]), (32621, EN[2], tr[2])):
            if 'msgctxt "#%d"' % sid in t:
                continue
            add += '\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, esc(en), '' if lang == 'en_gb' else esc(local))
        if add:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + add)
    print('ok', len(os.listdir('language')))


if __name__ == '__main__':
    main()
