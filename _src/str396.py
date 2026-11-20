"""0.39.6 strings 32433-32439: the Home heading of a custom item's spotlight ("Random %s" ...), %s = the item's name.
Each language's template comes from its own translation of the movie phrases 31400-31406 with the word for
"movies" replaced by %s, so the word order is the language's own. Run from the skin folder."""
import io
import os
import re

IDS = (32433, 32434, 32435, 32436, 32437, 32438, 32439)
SRC = ('31400', '31401', '31402', '31403', '31404', '31405', '31406')
EN = ('Random %s', 'Recently added %s', 'Recently played %s', 'Top rated %s', 'Most played %s', 'Newest %s', '%s by title')
NOUN = {'cs_cz': 'filmy', 'da_dk': 'film', 'de_de': 'Filme', 'el_gr': 'ταινίες', 'es_es': 'Películas', 'fi_fi': 'elokuvat',
        'fr_fr': 'Films', 'hu_hu': 'filmek', 'it_it': 'Film', 'ja_jp': '映画', 'ko_kr': '영화', 'nb_no': 'filmer',
        'nl_nl': 'films', 'pl_pl': 'filmy', 'pt_br': 'Filmes', 'pt_pt': 'Filmes', 'ru_ru': 'фильмы', 'sv_se': 'filmer',
        'tr_tr': 'filmler', 'uk_ua': 'фільми', 'zh_cn': '电影', 'zh_tw': '電影'}
CJK = ('ja_jp', 'ko_kr', 'zh_cn', 'zh_tw')

base = 'language'
for d in sorted(os.listdir(base)):
    lang = d.replace('resource.language.', '')
    p = os.path.join(base, d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32433"' in t:
        print(lang, 'has them')
        continue
    out = []
    for sid, src, en in zip(IDS, SRC, EN):
        if lang == 'en_gb':
            tr = ''
        else:
            m = re.search(r'msgctxt "#%s"\nmsgid "[^"]*"\nmsgstr "([^"]*)"' % src, t)
            assert m and m.group(1), (lang, src)
            phrase = m.group(1)
            noun = NOUN[lang]
            if lang in CJK:
                assert noun in phrase, (lang, phrase)
                tr = phrase.replace(noun, '%s', 1)
            else:
                tr, n = re.subn(r'(?i)(?<!\w)%s(?!\w)' % re.escape(noun), '%s', phrase, count=1)
                assert n == 1, (lang, phrase)
        out.append('msgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, en, tr))
    if not t.endswith('\n'):
        t += '\n'
    t += '\n' + '\n'.join(out)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print(lang, ' | '.join(re.findall(r'msgstr "([^"]*)"\n?$', o, re.M)[0] for o in out))
