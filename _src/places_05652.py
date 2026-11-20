"""0.56.52 Skin settings > Information: Ratings shown in (row 9500, after Ratings shown as) and Media info shown in
(row 9501, after Media info chips). OK opens a modal multi-select of the places (helper placepick rate|chip:
Library views, Information pages, Widget & Spotlight screens, Home spotlights, Player info, Screensaver, Live TV);
every place is on by default, an unticked place sets Skin.HasSetting(aeon.<kind>off.<place>). The row shows
"n / 6" (the screensaver shows no ratings, Live TV no chips: not in that list). The skin's ratings / chip blocks read the switches through $EXP[Aeon_Rate_<place>] / $EXP[Aeon_Chip_<place>]
(written here, used by placegate_05652.py). Clones row 9780 (the chip picker row). Run from the skin folder; run
pickmode / ok_only after it like every row generator. Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_rows as sr  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'SkinSettings.xml')
SET = os.path.join(HERE, '..', '1080i', 'Includes_Settings.xml')
PLACES = ['lib', 'info', 'widgets', 'spot', 'player', 'ss', 'pvr']
ROWS = [(9500, 9768, 'rate', 32751, 32760, 'aeon/icons/star.png', 'Aeon_RatePlaces'),
        (9501, 9780, 'chip', 32752, 32761, 'aeon/icons/layers.png', 'Aeon_ChipPlaces')]


def variables():
    out = ['\t<!-- 0.56.52 places: where ratings / media info chips are drawn (helper placepick; all on by default) -->']
    for _rid, _after, kind, _l, _h, _i, var in ROWS:
        out.append('\t<variable name="%s">\n\t\t<value condition="!String.IsEmpty(Skin.String(aeon.%s.places))">'
                   '$INFO[Skin.String(aeon.%s.places)]</value>\n\t\t<value>%d / %d</value>\n\t</variable>'
                   % (var, kind, kind, len(PLACES) - 1, len(PLACES) - 1))
        for p in PLACES:
            out.append('\t<expression name="Aeon_%s_%s">!Skin.HasSetting(aeon.%soff.%s)</expression>'
                       % (kind.capitalize(), p, kind, p))
    return '\n'.join(out) + '\n'


def main():
    t = io.open(P, encoding='utf-8').read()
    for rid, after, kind, label, helpid, icon, var in ROWS:
        if 'id="%d"' % rid in t:
            continue
        item = sr.clone(t, 9780, rid, [
            ('$ADDON[skin.aeon.fuse 32645]', '$ADDON[skin.aeon.fuse %d]' % label),
            ('aeon/icons/layers.png', icon),
            ('RunScript(script.aeon.helper,chippick)', 'RunScript(script.aeon.helper,placepick,%s)' % kind),
            ('$VAR[Aeon_ChipsShown]', '$VAR[%s]' % var), ('$VAR[Aeon_ChipsShown]', '$VAR[%s]' % var),
            ('0.56.22 chips', '0.56.52 places %s' % kind)])
        t = sr.insert_after(t, after, item)
    t = sr.renav(t, 9774)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)

    s = io.open(SET, encoding='utf-8').read()
    v = variables()
    mark = '\t<!-- 0.56.52 places:'
    if mark in s:
        a = s.index(mark)
        b = s.index('\t<!-- 0.56.22 chips:', a)
        s = s[:a] + v + s[b:]
    else:
        i = s.index('\t<!-- 0.56.22 chips:')
        s = s[:i] + v + s[i:]
    for rid, _a, _k, _l, helpid, _i, _v in ROWS:
        s = sr.add_help(s, rid, helpid) if '<variable name="Dlg_SkinHelp">' in s else s
    io.open(SET, 'w', encoding='utf-8', newline='\n').write(s)
    print('places: rows 9500 / 9501 on the Information page')


if __name__ == '__main__':
    main()
