# -*- coding: utf-8 -*-
"""0.56.15 the user's second round of notes on the Aeon library views (canvas HJTtCDChVWkaZZAyt76wJA, boards Built05614b
and Built05614c):
- "again, let's not use square badges, only text labels with bullet point separators. also add hh:mm left if in progress
  after the Ends at time": every Aeon info band / strip / panel writes its facts and media info as text with bullets
  ("1996  •  RATED R  •  105 MINS  •  ENDS 17:10  •  0:07 LEFT", "DTS 5.1  •  1.78:1  •  FULL HD"): the List band, the
  Banner / Compact list band, the wall strip, the Low list / Flix chips, the Episode list panel. The status line says
  IN PROGRESS where the facts carry the time left. (Helper 0.3.95: aeon.left.N.hhmm, skin string 32606.)
- List (510): "Actual title, e.g. 28 DAYS LATER YEAR GENRE" and "move WATCHED icon and label up here" (the line over
  the rows), "remove mediainfo badges. we have them in the footer already" (rows keep Aeon's resolution pill, on the far
  right), "Remove year from here" (the band).
- Episode list: "next episode text label in yellow highlight color" (also in Flix).
- Compact list (524): "the posters and info section is just too large ... we need it the other way around to allow for
  longer titles in the list" (list 1000 wide, the poster / picture / text column 700), "progress bar?" (on the picture,
  with the Progress line setting), "circle season progress?" (a ring on the poster: a show's or season's share of
  watched episodes; in an episode list the list's own share, helper 0.3.95 aeon.cont.pct), "put the network logo ...
  below the thumb on the right" (Compact and Banner list; the band keeps the clearlogo).
Run from the skin folder after aeon_lib_other.py; runs once (marker per file)."""
import io
import os
import re
import xml.etree.ElementTree as ET

VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
V3 = os.path.join('1080i', 'Includes_Aeon_Views3.xml')
MARK = '0.56.15 aeon_lib_round2'
B = '  •  '
PROG = 'Integer.IsGreater(ListItem.PercentPlayed,0)'
FACTS = ('<control type="label"><width min="10" max="1500">auto</width><height>34</height><aligny>center</aligny><font>lb_ui_24_bold</font>'
         '<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$VAR[%s]</label></control>')
SMALL = ('<control type="label"><width min="10" max="1500">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font>'
         '<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>%s</label><visible>%s</visible></control>')
BULLET = ('<control type="label"><width min="10" max="60">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font>'
          '<textcolor>99ffffff</textcolor><selectedcolor>99ffffff</selectedcolor><label>•</label><visible>%s</visible></control>')
MEDIA = SMALL % ('$VAR[Aeon_TxMedia]', '$EXP[Aeon_TxHasMedia]')
SO = 'String.IsEqual(Window(Home).Property(aeon.studio.of),ListItem.Studio)'


def network(x, y, w, h):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><aspectratio align="right" aligny="center">keep</aspectratio>'
            '<texture background="true">resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png</texture>'
            '<visible>!Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + %s</visible></control>\n'
            '\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>right</align><aligny>center</aligny><font>lb_small_20_bold</font>'
            '<textcolor>d9ffffff</textcolor><label>[UPPERCASE]$INFO[Window(Home).Property(aeon.studio.text)][/UPPERCASE]</label>'
            '<visible>!Skin.HasSetting(aeon.nostudio) + String.IsEmpty(Window(Home).Property(aeon.studio)) + !String.IsEmpty(Window(Home).Property(aeon.studio.text)) + %s</visible></control>'
            % (x, y, w, h, SO, x, y, w, h, SO))


def is_chip(l):
    """a chip button (the media / certificate / run-time badges) or one of the plain labels the facts text replaces"""
    l = l.strip()
    if l.startswith('<control type="button">'):
        return any(k in l for k in ('Aeon_LVRated', 'Aeon_LVDur', 'FG_EcAudio', 'Aeon_LVAsp', 'FG_L_HdrChip', 'Aeon_LVRes',
                                    'FG_L510_Audio', 'FG_L510_Hdr', '_Audio]', '_Hdr]', 'VideoAspect', 'Res]'))
    return False


def grouplists(block):
    """(start, end) of each grouplist's item lines in a block: end at the grouplist's own closing line"""
    out = []
    for m in re.finditer(r'<control type="grouplist">', block):
        s = block.index('\n', m.start()) + 1
        e = block.index('</control>\n', s) if False else None
        # the grouplist's items are one per line; its closing tag is the first line that is only </control>
        pos = s
        while True:
            nl = block.index('\n', pos)
            if block[pos:nl].strip() == '</control>':
                out.append((s, pos))
                break
            pos = nl + 1
    return out


def facts_row(items, var, drop_status=False, status_tx=None, bullet_status=True):
    """a facts row's item lines: ratings kept, the year / certificate / run time / Ends become one text label"""
    out, placed = [], False
    for l in items:
        st = l.strip()
        plain = st.startswith('<control type="label"><width min="10" max="300">auto</width>') and (
            '$INFO[ListItem.Year]' in st or '$LOCALIZE[31030]' in st)
        if is_chip(l) or plain:
            if not placed:
                out.append(FACTS % var)
                placed = True
            continue
        if drop_status and any(k in st for k in ('aeon_eye', 'fg/pring', '_Status]', '<width>6</width><height>34</height><label></label>',
                                                   '<width>4</width><height>34</height><label></label>')):
            continue
        if status_tx and '_Status][/UPPERCASE]' in st:
            l = re.sub(r'\$VAR\[(\w+)_Status\]', lambda m: '$VAR[%s]' % status_tx, l)
        if bullet_status and (st.startswith('<control type="label"><width>6</width><height>34</height><label></label>') or
                              st.startswith('<control type="label"><width>4</width><height>34</height><label></label>')):
            vis = re.search(r'<visible>(.*?)</visible>', st)
            l = BULLET % (vis.group(1) if vis else 'true')
        out.append(l)
    if not placed:
        out.append(FACTS % var)
    return out


def media_row(items, bullet_first=False):
    out, placed = [], False
    for l in items:
        if is_chip(l):
            if not placed:
                if bullet_first:
                    out.append(BULLET % '$EXP[Aeon_TxHasMedia]')
                out.append(MEDIA)
                placed = True
            continue
        st = l.strip()
        if bullet_first and st.startswith('<control type="label"><width>6</width><height>34</height><label></label>'):
            continue
        out.append(l)
    return out


def convert(block, plan):
    """plan: [(kind, kwargs)] per grouplist in order; kind facts / media / skip"""
    gls = grouplists(block)
    assert len(gls) >= len(plan), (len(gls), len(plan))
    for (s, e), (kind, kw) in reversed(list(zip(gls, plan))):
        items = [l for l in block[s:e].split('\n') if l.strip()]
        if kind == 'facts':
            items = facts_row(items, **kw)
        elif kind == 'media':
            items = media_row(items, **kw)
        else:
            continue
        block = block[:s] + '\n'.join(items) + '\n' + block[e:]
    return block


def text_vars(v2):
    a = v2.index('<variable name="Aeon_LV_Status">')
    b = v2.index('</variable>', a)
    left = ''
    for cond, body in re.findall(r'<value condition="([^"]*)">\$INFO\[Window\(Home\)\.Property\(aeon\.left\.(\d+)\.text\)\]</value>', v2[a:b]):
        left += '\t\t<value condition="%s">%s[UPPERCASE]$INFO[Window(Home).Property(aeon.left.%s.hhmm)][/UPPERCASE]</value>\n' % (cond, B, body)
    assert left.count('<value') == 40, left.count('<value')
    r510 = left.replace('ListItem.', 'Container(510).ListItem.')
    return ('\t<!-- %s: the info bands as text with bullets (the user: "only text labels with bullet point separators") -->\n'
            '\t<variable name="Aeon_TxRatedB"><value condition="!String.IsEmpty(ListItem.MPAA)">%s$VAR[Aeon_LVRated]</value></variable>\n'
            '\t<variable name="Aeon_TxDurB"><value condition="Integer.IsGreater(ListItem.Duration(mins),0)">%s$VAR[Aeon_LVDur]</value></variable>\n'
            '\t<variable name="Aeon_TxEndsB"><value condition="!String.IsEmpty(ListItem.EndTimeResume)">%s[UPPERCASE]$LOCALIZE[31030][/UPPERCASE] $INFO[ListItem.EndTimeResume]</value></variable>\n'
            '\t<variable name="Aeon_TxLeftB">\n%s\t</variable>\n'
            '\t<variable name="Aeon_TxFacts">\n'
            '\t\t<value condition="!String.IsEmpty(ListItem.Year)">$INFO[ListItem.Year]$VAR[Aeon_TxRatedB]$VAR[Aeon_TxDurB]$VAR[Aeon_TxEndsB]$VAR[Aeon_TxLeftB]</value>\n'
            '\t\t<value>$VAR[Aeon_TxFactsNY]</value>\n'
            '\t</variable>\n'
            '\t<variable name="Aeon_TxFactsNY">\n'
            '\t\t<value condition="!String.IsEmpty(ListItem.MPAA)">$VAR[Aeon_LVRated]$VAR[Aeon_TxDurB]$VAR[Aeon_TxEndsB]$VAR[Aeon_TxLeftB]</value>\n'
            '\t\t<value condition="Integer.IsGreater(ListItem.Duration(mins),0)">$VAR[Aeon_LVDur]$VAR[Aeon_TxEndsB]$VAR[Aeon_TxLeftB]</value>\n'
            '\t\t<value condition="!String.IsEmpty(ListItem.EndTimeResume)">[UPPERCASE]$LOCALIZE[31030][/UPPERCASE] $INFO[ListItem.EndTimeResume]$VAR[Aeon_TxLeftB]</value>\n'
            '\t</variable>\n'
            '\t<expression name="Aeon_TxHasAud">!Skin.HasSetting(aeon.hide.audio) + !String.IsEmpty(ListItem.AudioCodec)</expression>\n'
            '\t<expression name="Aeon_TxHasRes">!Skin.HasSetting(aeon.hide.res) + !String.IsEmpty(ListItem.VideoResolution)</expression>\n'
            '\t<expression name="Aeon_TxHasMedia">$EXP[Aeon_VOMedia] + [$EXP[Aeon_TxHasAud] | $EXP[Aeon_TxHasRes]]</expression>\n'
            '\t<variable name="Aeon_TxAspB"><value condition="$EXP[Aeon_TxHasRes] + !String.IsEmpty(ListItem.VideoAspect)">%s$INFO[ListItem.VideoAspect,,:1]</value></variable>\n'
            '\t<variable name="Aeon_TxHdrB"><value condition="$EXP[Aeon_TxHasRes] + !Skin.HasSetting(aeon.hide.hdr) + !String.IsEmpty(ListItem.HdrType)">%s[UPPERCASE]$VAR[FG_L_HdrChip][/UPPERCASE]</value></variable>\n'
            '\t<variable name="Aeon_TxResB"><value condition="$EXP[Aeon_TxHasRes]">%s[UPPERCASE]$VAR[Aeon_LVRes][/UPPERCASE]</value></variable>\n'
            '\t<variable name="Aeon_TxMedia">\n'
            '\t\t<value condition="$EXP[Aeon_TxHasAud]">[UPPERCASE]$VAR[FG_EcAudio][/UPPERCASE]$VAR[Aeon_TxAspB]$VAR[Aeon_TxHdrB]$VAR[Aeon_TxResB]</value>\n'
            '\t\t<value condition="$EXP[Aeon_TxHasRes] + !String.IsEmpty(ListItem.VideoAspect)">$INFO[ListItem.VideoAspect,,:1]$VAR[Aeon_TxHdrB]$VAR[Aeon_TxResB]</value>\n'
            '\t\t<value condition="$EXP[Aeon_TxHasRes]">[UPPERCASE]$VAR[Aeon_LVRes][/UPPERCASE]</value>\n'
            '\t</variable>\n'
            '\t<!-- the status where the facts carry the time left: IN PROGRESS rather than the time left twice -->\n'
            '\t<variable name="Aeon_LV_StatusTx"><value condition="$EXP[Aeon_LV_Ring]">$LOCALIZE[575]</value><value>$VAR[Aeon_LV_Status]</value></variable>\n'
            '\t<variable name="FG_L510_StatusTx"><value condition="$EXP[FG_L510_Ring]">$LOCALIZE[575]</value><value>$VAR[FG_L510_Status]</value></variable>\n'
            '\t<!-- List (510): the line over the rows, "28 DAYS LATER  •  2002  •  HORROR" -->\n'
            '\t<variable name="Aeon_L510_Head">\n'
            '\t\t<value condition="String.IsEqual(Container(510).ListItem.DBType,episode)">$INFO[Container(510).ListItem.Title]$INFO[Container(510).ListItem.Season,%s$LOCALIZE[20373] ,]$INFO[Container(510).ListItem.Episode,%s$LOCALIZE[20359] ,]</value>\n'
            '\t\t<value>$INFO[Container(510).ListItem.Title]$INFO[Container(510).ListItem.Year,%s,]$INFO[Container(510).ListItem.Genre,%s,]</value>\n'
            '\t</variable>\n'
            % (MARK, B, B, B, left, B, B, B, B, B, B, B))


def round_vid(t):
    if MARK in t:
        return t, False
    # ---- List (510) rows: no audio / aspect / HDR badges (the band has them); the title runs to the resolution pill
    a = t.index('<include name="Aeon_Row">')
    b = t.index('\n\t</include>', a)
    row = t[a:b]
    row, n = re.subn(r'<control type="(?:image|label)"><left>(?:693|605|447|709|551|699|611|453|715|557)</left><top>34</top>.*?</control>', '', row)
    assert n == 20, n
    row = re.sub(r'\n[ \t]+(?=\n)', '', row)
    for w in ('395', '291'):
        assert row.count('<width>%s</width>' % w) == 4, w
        row = row.replace('<width>%s</width>' % w, '<width>641</width>')
    t = t[:a] + row + t[b:]
    # ---- List (510): the line over the rows: title, year, genre, then the status
    old = '<label>[UPPERCASE]$VAR[Aeon_L510_Kicker][/UPPERCASE]</label>'
    i = t.index(old)
    s = t.rindex('<control type="label">', 0, i)
    e = t.index('</control>', i) + len('</control>')
    head = ('<control type="grouplist"><left>0</left><top>-6</top><width>1010</width><height>40</height><orientation>horizontal</orientation><itemgap>10</itemgap>'
            '<control type="label"><width min="10" max="760">auto</width><height>40</height><aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$VAR[Aeon_L510_Head][/UPPERCASE]</label></control>'
            '<control type="label"><width min="10" max="60">auto</width><height>40</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>99ffffff</textcolor><label>•</label></control>'
            '<control type="image"><width>32</width><height>40</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye_off.png</texture><visible>$EXP[FG_L510_Dot]</visible></control>'
            '<control type="image"><width>32</width><height>40</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye.png</texture><visible>$EXP[FG_L510_Tick]</visible></control>'
            '<control type="image"><width>28</width><height>40</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">fg/pring/$INFO[Container(510).ListItem.PercentPlayed].png</texture><visible>$EXP[FG_L510_Ring]</visible></control>'
            '<control type="label"><width min="10" max="400">auto</width><height>40</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$VAR[FG_L510_StatusTx][/UPPERCASE]</label><visible>!$EXP[FG_L510_Ring]</visible></control>'
            '<control type="label"><width min="10" max="400">auto</width><height>40</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>fg_mark</textcolor><label>[UPPERCASE]$VAR[FG_L510_StatusTx][/UPPERCASE]</label><visible>$EXP[FG_L510_Ring]</visible></control>'
            '</control>')
    t = t[:s] + head + t[e:]
    # ---- Episode list panel (Aeon / Glass branches): the certificate and the media info as text
    a = t.index('<include name="Aeon_EpInfo">')
    b = t.index('\n\t</include>', a)
    inc = t[a:b]
    fg_end = inc.index('<control type="group"><visible>!$EXP[Aeon_FGlass] + $PARAM[fill]</visible>')
    keep, rest = inc[:fg_end], inc[fg_end:]
    rated = SMALL % ('$VAR[Aeon_LVRated]', '!String.IsEmpty(ListItem.MPAA)')
    out = []
    for l in rest.split('\n'):
        st = l.strip()
        if st.startswith('<control type="button">') and '$VAR[Aeon_LVRated]' in st:
            if 'Skin.HasSetting(aeon.vglass) + ' in st and '!Skin.HasSetting(aeon.vglass)' not in st:
                continue
            out.append(rated)
            continue
        if st == '<control type="label"><width>8</width><height>34</height><label></label></control>':
            out.append(BULLET % 'true')
            continue
        out.append(l)
    rest = '\n'.join(out)
    found = 0
    for (s, e) in reversed(grouplists(rest)):
        items = [l for l in rest[s:e].split('\n') if l.strip()]
        if any(is_chip(l) for l in items) and not any('$VAR[Aeon_LVRated]' in l for l in items):
            rest = rest[:s] + '\n'.join(media_row(items)) + '\n' + rest[e:]
            found += 1
    assert found == 2, found
    t = t[:a] + keep + rest + t[b:]
    # ---- NEXT EPISODE in the yellow highlight colour
    n = 0
    for m in list(re.finditer(r'<control type="label">[^\n]*?\$ADDON\[skin\.aeon\.fuse 32605\][^\n]*?</control>', t)):
        seg = m.group(0)
        new = seg.replace('<textcolor>$VAR[Aeon_Accent]</textcolor>', '<textcolor>fg_mark</textcolor>')
        if new != seg:
            t = t.replace(seg, new)
            n += 1
    assert n >= 1, n
    t = t.replace('<include name="Aeon_Row">', '<!-- %s: rows without media badges, the title line, the panel as text -->\n\t<include name="Aeon_Row">' % MARK, 1)
    return t, True


def round_v2(v):
    if MARK in v:
        return v, False
    # ---- Banner / Compact list band
    a = v.index('<include name="Aeon_V_Bar">')
    b = v.index('\n\t</include>', a)
    bar = v[a:b]
    bar = convert(bar, [('facts', dict(var='Aeon_TxFacts')), ('media', dict(bullet_first=True))])
    bar = bar.replace('$VAR[Aeon_LV_Status]', '$VAR[Aeon_LV_StatusTx]')
    # the studio leaves the band: it goes under the picture in each view
    bar, n = re.subn(r'\n\t\t\t<!-- 0\.56\.14 aeon_lib_lists: the studio[^\n]*\n\t\t\t<control type="image"><left>1040</left>[^\n]*\n\t\t\t<control type="label"><left>700</left>[^\n]*', '', bar)
    assert n == 1, n
    v = v[:a] + bar + v[b:]
    # ---- List band: no year (it is over the rows), no status (it is over the rows too)
    a = v.index('<include name="Aeon_V_Bar510">')
    b = v.index('\n\t</include>', a)
    bar = v[a:b]
    gls = grouplists(bar)
    s, e = gls[1]
    items = [l for l in bar[s:e].split('\n') if l.strip()]
    items = [l for l in items if not any(k in l for k in ('aeon_eye', 'fg/pring', '_Status]', '<width>6</width><height>34</height><label></label>'))]
    bar = bar[:s] + '\n'.join(items) + '\n' + bar[e:]
    bar = convert(bar, [('facts', dict(var='Aeon_TxFactsNY')), ('media', dict())])
    v = v[:a] + bar + v[b:]
    # ---- the wall strip
    a = v.index('<include name="Aeon_V_Info">')
    b = v.index('\n\t</include>', a)
    inc = convert(v[a:b], [('facts', dict(var='Aeon_TxFacts', status_tx='Aeon_LV_StatusTx')), ('media', dict())])
    v = v[:a] + inc + v[b:]
    # ---- Low list / Flix chips: certificate (and run time) as text, the media info as text
    a = v.index('<include name="Aeon_V_Chips2">')
    b = v.index('\n\t</include>', a)
    inc = v[a:b]
    gls = grouplists(inc)
    s, e = gls[0]
    items = []
    for l in [l for l in inc[s:e].split('\n') if l.strip()]:
        st = l.strip()
        if st.startswith('<control type="button">') and '$VAR[Aeon_LVRated]' in st:
            if '!$EXP[Aeon_VGlass]' in st:
                items.append(SMALL % ('$VAR[Aeon_LVRated]', '!String.IsEmpty(ListItem.MPAA)'))
            continue
        if st.startswith('<control type="button">') and '$VAR[Aeon_LVDur]' in st:
            if '!$EXP[Aeon_VGlass]' in st:
                items.append(SMALL % ('$VAR[Aeon_TxDurB]', '$PARAM[dur] + Integer.IsGreater(ListItem.Duration(mins),0)'))
            continue
        if st.startswith('<control type="label"><width>4</width><height>34</height><label></label>'):
            items.append(BULLET % '$PARAM[stat]')
            continue
        items.append(l)
    inc = inc[:s] + '\n'.join(items) + '\n' + inc[e:]
    inc = convert(inc, [('skip', {}), ('media', dict())])
    v = v[:a] + inc + v[b:]
    # ---- Compact list (524): the list 1000 wide, the poster / picture / text column 700 (1100..1800)
    a = v.index('<include name="Aeon_V_Row">')
    b = v.index('\n\t</include>', a)
    row = v[a:b]
    row = re.sub(r'<left>(\d+)</left>', lambda m: '<left>%d</left>' % (int(m.group(1)) + 240 if int(m.group(1)) >= 300 else int(m.group(1))), row)
    row = re.sub(r'<param name="left">(\d+)</param>', lambda m: '<param name="left">%d</param>' % (int(m.group(1)) + 240 if int(m.group(1)) >= 300 else int(m.group(1))), row)
    for old, new in (('<width>760</width>', '<width>1000</width>'), ('<width>724</width>', '<width>964</width>'), ('<width>840</width>', '<width>1080</width>'),
                     ('<width>291</width>', '<width>531</width>'), ('<width>327</width>', '<width>567</width>'), ('<width>446</width>', '<width>686</width>'),
                     ('<width>536</width>', '<width>776</width>'), ('<width>386</width>', '<width>626</width>')):
        row = row.replace(old, new)
    v = v[:a] + row + v[b:]
    a = v.index('<include name="Aeon_V524_ViewAeon">')
    b = v.index('\n\t</include>', a)
    view = v[a:b]
    reps = (('<left>90</left><top>108</top><width>760</width><height>868</height>', '<left>90</left><top>108</top><width>1000</width><height>868</height>', 1),
            ('width="760" height="62"', 'width="1000" height="62"', 2),
            ('<left>740</left><top>38</top><width>513</width><height>649</height>', '<left>980</left><top>38</top><width>470</width><height>585</height>', 1),
            ('<left>1033</left><top>38</top><width>887</width><height>649</height>', '<left>1226</left><top>38</top><width>694</width><height>495</height>', 1),
            ('<left>860</left><top>128</top><width>273</width><height>409</height>', '<left>1100</left><top>128</top><width>230</width><height>345</height>', 2),
            ('<left>1153</left><top>128</top><width>647</width><height>409</height>', '<left>1346</left><top>128</top><width>454</width><height>255</height>', 2),
            ('<left>860</left><top>557</top><width>940</width>', '<left>1100</left><top>492</top><width>700</width>', 3),
            ('<left>860</left><top>605</top><width>940</width>', '<left>1100</left><top>540</top><width>700</width>', 3),
            ('<left>860</left><top>645</top><width>940</width>', '<left>1100</left><top>580</top><width>700</width>', 3),
            ('<left>860</left><top>687</top><width>940</width><height>266</height>', '<left>1100</left><top>620</top><width>700</width><height>333</height>', 3),
            ('<left>860</left><top>128</top>\n', '<left>1100</left><top>128</top>\n', 1))
    for old, new, n in reps:
        assert view.count(old) == n, (old, view.count(old))
        view = view.replace(old, new)
    # the versions / set panels at the poster's new size
    g = view.index('<!-- versions / set members')
    gmap = {'273': 230, '409': 345, '136': 115, '204': 172, '132': 111, '200': 168, '403': 339, '267': 224, '245': 206, '198': 167,
            '257': 216, '96': 75, '256': 216, '122': 100, '282': 242, '368': 310, '104': 83, '353': 289, '359': 295, '332': 268, '70': 59, '120': 101}
    tail = re.sub(r'<(left|top|width|height)>(\d+)</\1>', lambda m: '<%s>%s</%s>' % (m.group(1), gmap.get(m.group(2), m.group(2)), m.group(1)), view[g:])
    tail = tail.replace('width="273" height="409"', 'width="230" height="345"').replace('width="136" height="204"', 'width="115" height="172"')
    view = view[:g] + tail
    i = view.rindex('\n', 0, view.index('<label>[UPPERCASE]$INFO[ListItem.Title][/UPPERCASE]')) + 1
    i = view.rindex('\n', 0, i - 1) + 1 if '<control type="group">' in view[view.rindex('\n', 0, i - 1):i] else i
    extra =('\t\t\t<!-- %s: the network logo under the picture, on the right; the progress line on the picture; the share of\n'
             '\t\t\t     watched episodes as a ring on the poster (a show or season; in an episode list the list\'s own, helper aeon.cont.pct) -->\n'
             '\t\t\t%s\n' % (MARK, network(1346, 395, 454, 70)) +
             '\t\t\t<control type="group"><left>1346</left><top>128</top><width>454</width><height>255</height><visible>Skin.HasSetting(aeon.progressline) + %s + !Control.HasFocus(5241) + !Control.HasFocus(5244)</visible>'
             '<control type="image"><left>0</left><top>249</top><width>454</width><height>6</height><texture colordiffuse="b0000000">common/white.png</texture></control>'
             '<control type="progress"><left>0</left><top>249</top><width>454</width><height>6</height><texturebg colordiffuse="00ffffff">common/aeon_line_6.png</texturebg>'
             '<midtexture colordiffuse="fg_mark">common/aeon_line_6.png</midtexture><info>ListItem.PercentPlayed</info></control></control>\n' % PROG +
             '\t\t\t<control type="group"><left>1270</left><top>136</top><visible>Skin.HasSetting(aeon.progressline) + !Control.HasFocus(5241) + !Control.HasFocus(5244) + '
             '[[Container.Content(episodes) + String.IsEqual(Window(Home).Property(aeon.cont.path),Container.FolderPath) + Integer.IsGreater(Window(Home).Property(aeon.cont.pct),0)] | '
             '[[Container.Content(tvshows) | Container.Content(seasons)] + Integer.IsGreater(ListItem.Property(WatchedEpisodePercent),0)]]</visible>'
             '<control type="image"><left>0</left><top>0</top><width>52</width><height>52</height><texture colordiffuse="b3080a0e">aeon/circle_12.png</texture></control>'
             '<control type="image"><left>6</left><top>6</top><width>40</width><height>40</height><texture colordiffuse="fg_mark">fg/pring/$INFO[Window(Home).Property(aeon.cont.pct)].png</texture><visible>Container.Content(episodes)</visible></control>'
             '<control type="image"><left>6</left><top>6</top><width>40</width><height>40</height><texture colordiffuse="fg_mark">fg/pring/$INFO[ListItem.Property(WatchedEpisodePercent)].png</texture><visible>!Container.Content(episodes)</visible></control>'
             '</control>\n')
    view = view[:i] + extra + view[i:]
    v = v[:a] + view + v[b:]
    # ---- Banner list (522): the network logo under the picture on the right of the title
    a = v.index('<include name="Aeon_V522_ViewAeon">')
    b = v.index('\n\t</include>', a)
    view = v[a:b]
    old = '<left>860</left><top>557</top><width>940</width>'
    assert view.count(old) == 3
    view = view.replace(old, '<left>860</left><top>557</top><width>620</width>')
    i = view.rindex('\n', 0, view.index('<label>[UPPERCASE]$INFO[ListItem.Title][/UPPERCASE]')) + 1
    i = view.rindex('\n', 0, i - 1) + 1 if '<control type="group">' in view[view.rindex('\n', 0, i - 1):i] else i
    view = view[:i] +'\t\t\t<!-- %s: the network logo under the picture, on the right -->\n\t\t\t%s\n' % (MARK, network(1500, 549, 300, 60)) + view[i:]
    v = v[:a] + view + v[b:]
    assert v.count('</includes>') == 1
    v = v.replace('</includes>', text_vars(v) + '</includes>')
    return v, True


def round_v3(v3):
    if MARK in v3:
        return v3, False
    n = 0
    for m in list(re.finditer(r'<control type="label">[^\n]*?\$ADDON\[skin\.aeon\.fuse 32605\][^\n]*?</control>', v3)):
        seg = m.group(0)
        new = seg.replace('<textcolor>$VAR[Aeon_Accent]</textcolor>', '<textcolor>fg_mark</textcolor>')
        if new != seg:
            v3 = v3.replace(seg, new)
            n += 1
    assert n == 1, n
    v3 = v3.replace('<!-- 0.56.14 aeon_lib_other: the next episode', '<!-- %s: NEXT EPISODE in yellow -->\n\t\t\t<!-- 0.56.14 aeon_lib_other: the next episode' % MARK, 1)
    return v3, True


def main():
    t = io.open(VID, encoding='utf-8').read()
    v = io.open(V2, encoding='utf-8').read()
    v3 = io.open(V3, encoding='utf-8').read()
    t, d1 = round_vid(t)
    v, d2 = round_v2(v)
    v3, d3 = round_v3(v3)
    for fn, txt, done in ((VID, t, d1), (V2, v, d2), (V3, v3, d3)):
        if done:
            io.open(fn, 'w', encoding='utf-8', newline='\n').write(txt)
            ET.parse(fn)
    print('ok' if (d1 or d2 or d3) else 'already done', d1, d2, d3)


if __name__ == '__main__':
    main()
