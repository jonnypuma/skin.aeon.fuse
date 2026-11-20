# -*- coding: utf-8 -*-
"""0.56.26 Media info chips (the user: "you are missing options for <video_source>, <source_format>, <video_codec>
... and an option to show Version, or edition, as it is called in the cmm sidecar"). Idempotent; run from the skin
folder. Needs script.aeon.helper 0.3.102 (aeon.mi.format / vsource / vcodec, the picker's three new rows).

- The Source chip is the sidecar's <source_format> now (aeon.mi.format; named "Source format (sidecar)", string 32653);
  the information page's card line keeps aeon.mi.source (the format, else the video source).
- New chips on the information page, off by default, in the picker: Video source (<video_source>, aeon.chip.vsource,
  32665), Video codec (<video_codec>, aeon.chip.vcodec, 32666), Version (<edition>, aeon.chip.edition, 32667).
  Order: video source, source format, video codec, version, then container ... as before.
- The picker row's default count reads 7 / 17.
"""
import io
import os
import re

D = '1080i'
L = 'language'
EN = {32653: 'Source format (sidecar)', 32665: 'Video source (sidecar)', 32666: 'Video codec (sidecar)', 32667: 'Version (sidecar)'}
# per language: source format, video source, video codec, version (the "(sidecar)" part is taken from its 32653)
T = {
    'cs_cz': ('Formát zdroje', 'Zdroj videa', 'Kodek videa', 'Verze'),
    'da_dk': ('Kildeformat', 'Videokilde', 'Videocodec', 'Version'),
    'de_de': ('Quellformat', 'Videoquelle', 'Videocodec', 'Fassung'),
    'el_gr': ('Μορφή πηγής', 'Πηγή βίντεο', 'Κωδικοποιητής βίντεο', 'Έκδοση'),
    'es_es': ('Formato de origen', 'Origen del vídeo', 'Códec de vídeo', 'Versión'),
    'fi_fi': ('Lähteen muoto', 'Videon lähde', 'Videokoodekki', 'Versio'),
    'fr_fr': ('Format de la source', 'Source vidéo', 'Codec vidéo', 'Version'),
    'hu_hu': ('Forrás formátuma', 'Videóforrás', 'Videokodek', 'Változat'),
    'it_it': ('Formato sorgente', 'Sorgente video', 'Codec video', 'Versione'),
    'ja_jp': ('ソース形式', '映像ソース', '映像コーデック', 'バージョン'),
    'ko_kr': ('소스 형식', '비디오 소스', '비디오 코덱', '버전'),
    'nb_no': ('Kildeformat', 'Videokilde', 'Videokodek', 'Versjon'),
    'nl_nl': ('Bronformaat', 'Videobron', 'Videocodec', 'Versie'),
    'pl_pl': ('Format źródła', 'Źródło wideo', 'Kodek wideo', 'Wersja'),
    'pt_br': ('Formato de origem', 'Origem do vídeo', 'Codec de vídeo', 'Versão'),
    'pt_pt': ('Formato de origem', 'Origem do vídeo', 'Codec de vídeo', 'Versão'),
    'ru_ru': ('Формат источника', 'Источник видео', 'Видеокодек', 'Версия'),
    'sv_se': ('Källformat', 'Videokälla', 'Videokodek', 'Version'),
    'tr_tr': ('Kaynak biçimi', 'Video kaynağı', 'Video kodeki', 'Sürüm'),
    'uk_ua': ('Формат джерела', 'Джерело відео', 'Відеокодек', 'Версія'),
    'zh_cn': ('来源格式', '视频来源', '视频编码', '版本'),
    'zh_tw': ('來源格式', '影片來源', '影片編碼', '版本'),
}


def strings():
    n = 0
    for d in sorted(os.listdir(L)):
        code = d.replace('resource.language.', '')
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        m = re.search(r'msgctxt "#32653"\nmsgid "[^\n]*"\nmsgstr "([^\n]*)"', t)
        assert m, code
        old_tr = m.group(1)
        if code == 'en_gb':
            words = None
        else:
            words = T[code]
            suffix = re.search(r'\s*[（(][^)）]*[)）]$', old_tr)
            suffix = suffix.group(0) if suffix else ' (sidecar)'
            if old_tr.startswith(words[0]):          # already done
                suffix = old_tr[len(words[0]):]
        def tr(i):
            return '' if words is None else words[i] + suffix
        t = re.sub(r'(msgctxt "#32653"\nmsgid ")[^\n]*("\nmsgstr ")[^\n]*(")', lambda mm: mm.group(1) + EN[32653] + mm.group(2) + tr(0) + mm.group(3), t)
        if 'msgctxt "#32665"' not in t:
            m = re.search(r'msgctxt "#32664"\nmsgid "[^\n]*"\nmsgstr "[^\n]*"\n', t)
            assert m, code
            add = ''.join('\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, EN[sid], tr(i)) for i, sid in ((1, 32665), (2, 32666), (3, 32667)))
            t = t[:m.end()] + add + t[m.end():]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        n += 1
    print('strings: %d languages' % n)


def info_page():
    p = os.path.join(D, 'Includes_VideoInfo.xml')
    t = io.open(p, encoding='utf-8').read()
    lines = t.split('\n')
    # the two Source chips (Glass / Aeon) show the format now
    src = [i for i, l in enumerate(lines) if 'aeon.hide.source' in l and '<control type="button">' in l]
    assert len(src) == 2, src
    for i in src:
        lines[i] = lines[i].replace('aeon.mi.source', 'aeon.mi.format')
    if not any('aeon.chip.vsource' in l for l in lines):
        cont = [l for l in lines if 'aeon.chip.container' in l and '<control type="button">' in l]
        assert len(cont) == 2
        indent = re.match(r'\s*', cont[0]).group(0)

        def pair(key):
            return [l.replace('aeon.mi.container', 'aeon.mi.' + key).replace('aeon.chip.container', 'aeon.chip.' + key) for l in cont]
        before = [indent + '<!-- 0.56.26 chips_05626: the sidecar\'s video source, before the source format -->'] + pair('vsource')
        after = [indent + '<!-- 0.56.26 chips_05626: the sidecar\'s video codec and edition (Version) -->'] + pair('vcodec') + pair('edition')
        a, b = src
        lines = lines[:a] + before + lines[a:b + 1] + after + lines[b + 1:]
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('information page chips written')


def chip_room():
    """the information page's chip row and the column that clips it: 1100 -> 1290 wide (472-1762, the card ends at
    1820), so the sidecar chips have room after the seven default ones (on the box all on ended at about 1700)"""
    p = os.path.join(D, 'Includes_VideoInfo.xml')
    t = io.open(p, encoding='utf-8').read()
    old = '<width>1100</width><!-- 0.56.20: the 1100-wide chip row inside is clipped to this list -->'
    new = '<width>1290</width><!-- 0.56.20 / 0.56.26: the chip row inside (1290 wide) is clipped to this list -->'
    if new not in t:
        assert t.count(old) == 1
        t = t.replace(old, new)
    old = ('<width>1100</width><height>34</height><orientation>horizontal</orientation><itemgap>8</itemgap><usecontrolcoords>true</usecontrolcoords>'
           "<!-- 0.56.20 mediainfo_skin2: room for the sidecar's source chip -->")
    new = '<width>1290</width><height>34</height><orientation>horizontal</orientation><itemgap>8</itemgap><usecontrolcoords>true</usecontrolcoords><!-- 0.56.20 mediainfo_skin2 / 0.56.26 chips_05626: room for the sidecar chips -->'
    if new not in t:
        assert t.count(old) == 1, t.count(old)
        t = t.replace(old, new)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('chip row widened')


def picker_row():
    p = os.path.join(D, 'Includes_Settings.xml')
    t = io.open(p, encoding='utf-8').read()
    if '<value>7 / 17</value>' not in t:
        assert t.count('<value>7 / 14</value>') == 1
        t = t.replace('<value>7 / 14</value>', '<value>7 / 17</value>')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('picker row count written')


if __name__ == '__main__':
    strings()
    info_page()
    chip_room()
    picker_row()
