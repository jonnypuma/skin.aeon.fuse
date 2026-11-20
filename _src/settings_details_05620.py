# -*- coding: utf-8 -*-
"""0.56.20 Skin settings > Details: a new row "Media info from sidecars" (9776, Skin.HasSetting(aeon.mi.sidecar), off by
default; help 32616: what it shows and that it needs Curator Media Manager's <name>.cmm_mediainfo.xml or
tinyMediaManager's <name>-mediainfo.xml next to the files). The user (2026-11-17): "we need an option to pick which
mediainfo we want displayed. standard kodi library ones on by default, extra ones from mediainfo sidecars off by
default and a clear note you need to have mediainfo sidecars ... next to files for them to work". The Kodi library
chips keep their own rows (on by default).

Details had eleven rows at fixed tops (the last at 891); a twelfth would leave the page, so Details becomes a list that
scrolls, as Appearance and Look did in 0.56.12 (settings_sections.main with this page: grouplist 9774, scroll bar 9775).
Then: python _src/skin_previews.py ; python _src/ok_only.py. Runs once (it stops when the list is there)."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings_sections as ss  # noqa: E402

P = os.path.join('1080i', 'SkinSettings.xml')
HELP = os.path.join('1080i', 'Includes_Settings.xml')
MARK = '0.56.20 settings_details'
DETAILS = [9700, 9701, 9702, 9703, 9704, 9705, 9706, 9707, 9708, 9709, 9761, 9776]


def block_at(t, start_text, open_at):
    """the whole <control ...> ... </control> that opens at index open_at"""
    depth, i = 0, open_at
    while True:
        a = t.find('<control', i)
        b = t.find('</control>', i)
        if a != -1 and a < b:
            depth += 1
            i = a + 8
        else:
            depth -= 1
            i = b + len('</control>')
            if depth == 0:
                return t[open_at:i]


def main():
    t = io.open(P, encoding='utf-8').read()
    if 'id="9774"' in t:
        print('already')
        return
    if 'id="9776"' not in t:
        # the row (cloned from 9761: an On / Off switch) and its focus bar
        b = t.index('<control type="button" id="9761">')
        row_open = t.rindex('<control type="group">', 0, t.rindex('<include content="Dlg_SkinRowChrome">', 0, b))
        row = block_at(t, '', row_open)
        bar_open = t.index('<control type="group">\n\t\t\t\t<left>-119</left>\n\t\t\t\t<top>891</top>\n\t\t\t\t<visible>Control.HasFocus(9761)</visible>')
        bar = block_at(t, '', bar_open)
        new_row = (row.replace('9761', '9776').replace('<top>891</top>', '<top>961</top>')
                   .replace('$ADDON[skin.aeon.fuse 32485]', '$ADDON[skin.aeon.fuse 32615]')
                   .replace('aeon.osd.castphotos', 'aeon.mi.sidecar'))
        new_bar = bar.replace('9761', '9776').replace('<top>891</top>', '<top>961</top>')
        assert new_row.count('aeon.mi.sidecar') >= 6, new_row.count('aeon.mi.sidecar')
        t = t[:row_open + len(row)] + '\n\t\t\t<!-- %s: Media info from sidecars -->\n\t\t\t' % MARK + new_row + t[row_open + len(row):]
        bar_open = t.index('<control type="group">\n\t\t\t\t<left>-119</left>\n\t\t\t\t<top>891</top>\n\t\t\t\t<visible>Control.HasFocus(9761)</visible>')
        t = t[:bar_open + len(bar)] + '\n\t\t\t' + new_bar + t[bar_open + len(bar):]
        io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    h = io.open(HELP, encoding='utf-8').read()
    if 'Control.HasFocus(9776)' not in h:
        old = '<value condition="Control.HasFocus(9761)">$ADDON[skin.aeon.fuse 32486]</value>'
        assert h.count(old) == 1, h.count(old)
        h = h.replace(old, old + '\n\t\t<value condition="Control.HasFocus(9776)">$ADDON[skin.aeon.fuse 32616]</value><!-- %s -->' % MARK)
        io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)
    ss.main(pages=(('details', 9566, DETAILS, 9774, 9775),), done='id="9774"')


if __name__ == '__main__':
    main()
