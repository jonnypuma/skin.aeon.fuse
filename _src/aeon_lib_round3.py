# -*- coding: utf-8 -*-
"""0.56.16 the user's third round of notes on the Aeon library views (canvas HJTtCDChVWkaZZAyt76wJA, board Built05615):
- List (510): "genre?" (the line over the rows: an episode's genres too); "List pane must stop around here so as to not
  overlap info pane above" (the rows and the list pane start under the title line and plot: an info pane 0..216, the
  list pane from 216, seven rows; the plot three lines); "If in the movie list and there are several versions and user
  is scrolling the versions, the media pane up top has to show that version's metadata" (the line over the rows and the
  plot follow the version / set film in focus);
- Banner / Compact list band: "genre?" (year, genres, certificate, run time ...);
- "no ends at on TV show or season level view, only when on a movie or an episode ... show status (continuing, ended
  etc). Please add that instead of ends at" (the bands' Ends only for films, episodes and music videos; a show writes its
  status there, Aeon_ShowStatus);
- the bands of the version / set panes (5101 / 5104 / 5221 / 5224 / 5241 / 5244) as text with bullets too (the rule of
  0.56.15);
- music Compact list (513): the track count and its note centred on the row like the run time.
Run from the skin folder after views_05615.py / aeon_lib_round2b.py; each file once."""
import io
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aeon_lib_round2 as r2  # noqa: E402

VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
ML = os.path.join('1080i', 'Includes_Aeon_MusicLib.xml')
MARK = '0.56.16 aeon_lib_round3'
B = r2.B
TOP = 216
PLAYABLE = '[String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,musicvideo)]'


_is_chip = r2.is_chip


def is_chip(l):
    s = l.strip()
    return _is_chip(l) or (s.startswith('<control type="button">') and any(k in s for k in ('Aeon_LVHdr', 'Aeon_LVAud', 'Aeon_LVCh', 'Aeon_LVRated', 'Aeon_LVDur', 'Aeon_LVRes', 'Aeon_LVAsp')))


r2.is_chip = is_chip


def v2_part(v):
    if MARK in v:
        return v, False
    # ---- the bands' facts: Ends for playable items only, a show's status, the genres (Banner / Compact list)
    old = '<variable name="Aeon_TxEndsB"><value condition="!String.IsEmpty(ListItem.EndTimeResume)">'
    assert v.count(old) == 1
    v = v.replace(old, '<variable name="Aeon_TxEndsB"><value condition="!String.IsEmpty(ListItem.EndTimeResume) + %s">' % PLAYABLE)
    n = v.count('$VAR[Aeon_TxEndsB]$VAR[Aeon_TxLeftB]')
    assert n == 3, n
    v = v.replace('$VAR[Aeon_TxEndsB]$VAR[Aeon_TxLeftB]', '$VAR[Aeon_TxEndsB]$VAR[Aeon_TxStatusB]$VAR[Aeon_TxLeftB]')
    old = '\t\t<value condition="!String.IsEmpty(ListItem.EndTimeResume)">[UPPERCASE]$LOCALIZE[31030][/UPPERCASE] $INFO[ListItem.EndTimeResume]$VAR[Aeon_TxLeftB]</value>\n'
    assert v.count(old) == 1
    v = v.replace(old, old.replace('<value condition="!String.IsEmpty(ListItem.EndTimeResume)">', '<value condition="!String.IsEmpty(ListItem.EndTimeResume) + %s">' % PLAYABLE)
                  + '\t\t<value condition="String.IsEqual(ListItem.DBType,tvshow) + !String.IsEmpty(ListItem.Status)">[UPPERCASE]$VAR[Aeon_ShowStatus][/UPPERCASE]</value>\n')
    defs = ('\t<!-- %s: a show\'s status where a film or episode has Ends; the genres in the Banner / Compact list band -->\n'
            '\t<variable name="Aeon_TxStatusB"><value condition="String.IsEqual(ListItem.DBType,tvshow) + !String.IsEmpty(ListItem.Status)">%s[UPPERCASE]$VAR[Aeon_ShowStatus][/UPPERCASE]</value></variable>\n'
            '\t<variable name="Aeon_TxGenreB"><value condition="!String.IsEmpty(ListItem.Genre)">%s[UPPERCASE]$INFO[ListItem.Genre][/UPPERCASE]</value></variable>\n'
            '\t<variable name="Aeon_TxFactsG">\n'
            '\t\t<value condition="!String.IsEmpty(ListItem.Year)">$INFO[ListItem.Year]$VAR[Aeon_TxGenreB]$VAR[Aeon_TxRatedB]$VAR[Aeon_TxDurB]$VAR[Aeon_TxEndsB]$VAR[Aeon_TxStatusB]$VAR[Aeon_TxLeftB]</value>\n'
            '\t\t<value condition="!String.IsEmpty(ListItem.Genre)">[UPPERCASE]$INFO[ListItem.Genre][/UPPERCASE]$VAR[Aeon_TxRatedB]$VAR[Aeon_TxDurB]$VAR[Aeon_TxEndsB]$VAR[Aeon_TxStatusB]$VAR[Aeon_TxLeftB]</value>\n'
            '\t\t<value>$VAR[Aeon_TxFactsNY]</value>\n'
            '\t</variable>\n' % (MARK, B, B))
    # ---- the List's line over the rows: an episode's genres too
    old = '$INFO[Container(510).ListItem.Episode,%s$LOCALIZE[20359] ,]</value>' % B
    assert v.count(old) == 1
    v = v.replace(old, '$INFO[Container(510).ListItem.Episode,%s$LOCALIZE[20359] ,]$INFO[Container(510).ListItem.Genre,%s,]</value>' % (B, B))
    defs += ('\t<!-- the line over the List\'s rows for the version / set film in focus (5101 / 5104) -->\n'
             '\t<variable name="Aeon_L510_HeadPane">\n'
             '\t\t<value>$INFO[ListItem.Title]$INFO[ListItem.VideoVersionName,%s,]$INFO[ListItem.Year,%s,]$INFO[ListItem.Genre,%s,]</value>\n'
             '\t</variable>\n' % (B, B, B))
    # ---- Banner / Compact list band: the genres
    a = v.index('<include name="Aeon_V_Bar">')
    b = v.index('\n\t</include>', a)
    bar = v[a:b]
    assert bar.count('<label>$VAR[Aeon_TxFacts]</label>') == 1
    v = v[:a] + bar.replace('<label>$VAR[Aeon_TxFacts]</label>', '<label>$VAR[Aeon_TxFactsG]</label>') + v[b:]
    # ---- the version / set panes' bands as text
    for name, var in (('Aeon_V_Bar5101', 'Aeon_TxFactsNY'), ('Aeon_V_Bar5104', 'Aeon_TxFactsNY'), ('Aeon_V_Bar5221', 'Aeon_TxFactsG'),
                      ('Aeon_V_Bar5224', 'Aeon_TxFactsG'), ('Aeon_V_Bar5241', 'Aeon_TxFactsG'), ('Aeon_V_Bar5244', 'Aeon_TxFactsG')):
        a = v.index('<include name="%s">' % name)
        b = v.index('\n\t</include>', a)
        inc = r2.convert(v[a:b], [('facts', dict(var=var)), ('media', dict())])
        assert '<control type="button">' not in inc, name
        v = v[:a] + inc + v[b:]
    assert v.count('</includes>') == 1
    v = v.replace('</includes>', defs + '</includes>')
    return v, True


def vid_part(t):
    if MARK in t:
        return t, False
    a = t.index('<include name="Aeon_510_ViewAeon">')
    b = t.index('\n\t</include>', a)
    view = t[a:b]
    # the list pane and its column tints start under the info pane; the info pane its own box above
    n = 0
    for col in ('lib_x_deep_f0', 'lib_x_deep_8c'):
        old = ('\t\t\t\t<left>aeon_list_x</left>\n\t\t\t\t<top>0</top>\n\t\t\t\t<width>aeon_list_w</width>\n\t\t\t\t<height>1080</height>\n'
               '\t\t\t\t<texture colordiffuse="%s">common/white.png</texture>' % col)
        assert view.count(old) == 1, col
        view = view.replace(old, old.replace('<top>0</top>', '<top>%d</top>' % TOP).replace('<height>1080</height>', '<height>%d</height>' % (1080 - TOP)))
        n += 1
    old = ('\t\t\t\t<left>aeon_list_x</left>\n\t\t\t\t<top>0</top>\n\t\t\t\t<width>100</width>\n\t\t\t\t<height>1080</height>\n'
           '\t\t\t\t<texture colordiffuse="lib_x_column">common/white.png</texture>')
    assert view.count(old) == 1
    view = view.replace(old, old.replace('<top>0</top>', '<top>%d</top>' % TOP).replace('<height>1080</height>', '<height>%d</height>' % (1080 - TOP)))
    old = '<control type="image"><left>1720</left><top>0</top><width>100</width><height>1080</height><texture colordiffuse="lib_x_column">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>'
    assert view.count(old) == 1
    view = view.replace(old, old.replace('<top>0</top><width>100</width><height>1080</height>', '<top>%d</top><width>100</width><height>%d</height>' % (TOP, 1080 - TOP)) +
                        '\n\t\t\t<!-- %s: the info pane over the list pane: the title line and the plot (0..%d) -->\n'
                        '\t\t\t<control type="image"><left>aeon_list_x</left><top>0</top><width>aeon_list_w</width><height>%d</height><texture colordiffuse="lib_x_deep">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>'
                        % (MARK, TOP, TOP))
    # the line over the rows and the plot: the 510 item, or the version / set film in focus
    old = '<control type="group"><left>760</left><top>56</top><visible>!$EXP[Aeon_FGlass] + Control.IsVisible(510) + [String.IsEqual(Container(510).ListItem.DBType,movie) | String.IsEqual(Container(510).ListItem.DBType,episode)]</visible>'
    assert view.count(old) == 1
    i = view.index(old)
    e = view.index('\n', view.index('</control>\n\t\t\t<!-- right strip', i)) if '<!-- right strip' in view[i:] else None
    gs, ge = i, view.index('\n\t\t\t<!-- right strip', i)
    grp = view[gs:ge]
    grp = grp.replace(old, old.replace('</visible>', ' + !Control.HasFocus(5101) + !Control.HasFocus(5104)</visible>'))
    grp = grp.replace('<width>1010</width><height>200</height>', '<width>1010</width><height>108</height>')
    assert '<height>108</height>' in grp
    pane = grp.replace(' + !Control.HasFocus(5101) + !Control.HasFocus(5104)</visible>', '</visible>', 1)
    pane = pane.replace('Control.IsVisible(510) + [String.IsEqual(Container(510).ListItem.DBType,movie) | String.IsEqual(Container(510).ListItem.DBType,episode)]',
                        '[Control.HasFocus(5101) | Control.HasFocus(5104)]')
    pane = pane.replace('$VAR[Aeon_L510_Head]', '$VAR[Aeon_L510_HeadPane]').replace('Container(510).ListItem.', 'ListItem.')
    for k in ('Dot', 'Tick', 'Ring'):
        pane = pane.replace('$EXP[FG_L510_%s]' % k, '$EXP[Aeon_LV_%s]' % k)
    pane = pane.replace('$VAR[FG_L510_StatusTx]', '$VAR[Aeon_LV_StatusTx]')
    view = view[:gs] + grp + '\n\t\t\t<!-- %s: the same for the version / set film in focus -->\n\t\t\t' % MARK + pane + view[ge:]
    t = t[:a] + view + t[b:]
    return t, True


def ml_part(m):
    if MARK in m:
        return m, False
    out, n = [], 0
    for l in m.split('\n'):
        if 'aeon.tc.' in l and 'Container(513)' in l:
            l2 = re.sub(r'<top>(\d+)</top>', lambda mm: '<top>%d</top>' % (int(mm.group(1)) - 18), l, count=1)
            n += l2 != l
            l = l2
        out.append(l)
    assert n == 30, n
    m = '\n'.join(out)
    m = m.replace('<include name="AeonM_Row">', '<!-- %s: the track count overlay centred on the row (18 px up) -->\n\t<include name="AeonM_Row">' % MARK, 1)
    return m, True


def main():
    done = []
    for fn, fx in ((V2, v2_part), (VID, vid_part), (ML, ml_part)):
        t = io.open(fn, encoding='utf-8').read()
        t, d = fx(t)
        if d:
            io.open(fn, 'w', encoding='utf-8', newline='\n').write(t)
            ET.parse(fn)
            done.append(os.path.basename(fn))
    print('ok' if done else 'already done', done)


if __name__ == '__main__':
    main()
