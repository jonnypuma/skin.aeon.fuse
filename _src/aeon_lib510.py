# -*- coding: utf-8 -*-
"""0.56.13 the Aeon theme's List view (510) to the list row and info panel rules of Fused Glass, in Aeon dress.

The user (2026-11-16): "start thinking about making Aeon library views consistent in the same way we have now done
Fused Glass ... Aeon has some special icons (watched, resolution pill, certification etc.)"; on the mockup canvas
HJTtCDChVWkaZZAyt76wJA: "move watched status to before duration, they shall all be on the same column and aligned
vertically on every list". Then: "please shoot the new Aeon library views so I can review".
Aeon and Glass only (Fused Glass has its own List view); Aeon's marks stay: the certificate shape at the row's left, the
two-part FULL | HD pill, the eye.
Row (Aeon_Row, 1093 x 108):
  - media chips right-aligned, ending just before the mark: Aeon's resolution pill, then the audio (short names), the
    aspect ratio and HDR (with the Dolby Vision profile) as outlined Aeon pills; a variant for items with HDR; Kodi takes
    no grouplists in list rows, so the chips have fixed widths;
  - the mark (eye, or the progress ring while in progress) in its own column right before the run time;
  - while in progress the run-time column shows the time left (the helper's aeon.left slots) in the accent colour;
  - the title and grey line end before the chips.
Band (Aeon_V_Bar510): the facts line gains the year and Ends; the status line (mark and words) starts the chips row;
the chips are resolution, audio (one chip, short), aspect, HDR (no SDR); the studio's name at the right of the facts row.
Above the rows (free space): the kicker (FILM · genres) and the plot.
Run from the skin folder; runs once (stops when its marker is there)."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
VID = os.path.join(D, 'Includes_Aeon_Video.xml')
V2 = os.path.join(D, 'Includes_Aeon_Views2.xml')
MARK = '0.56.13 aeon_lib510'
NFG = '!$EXP[Aeon_FGlass]'
PROG = 'Integer.IsGreater(ListItem.PercentPlayed,0)'
HDR = '!String.IsEmpty(ListItem.HdrType)'
RES = '!String.IsEmpty(ListItem.VideoResolution)'

# geometry of the row's right side (row-relative x)
MARK_X = 955          # the mark column (28 px), then the run-time rule at 993
CHIPS_END = 941
GAP = 8
W_RES, W_AUD, W_ASP, W_HDR = 144, 150, 80, 96


def chip(x, w, label, vis, focused):
    line = '$VAR[Aeon_OnBarLine]' if focused else '88ffffff'
    ink = '$VAR[Aeon_OnBarInk2_L]' if focused else 'ccffffff'
    return ('<control type="image"><left>%d</left><top>34</top><width>%d</width><height>40</height><texture border="8" colordiffuse="%s">$VAR[Aeon_TexOutline]</texture><visible>%s</visible></control>'
            '<control type="label"><left>%d</left><top>34</top><width>%d</width><height>40</height><align>center</align><aligny>center</aligny><font>lb_cap_16</font>'
            '<textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>%s</label><visible>%s</visible></control>\n'
            % (x, w, line, vis, x + 6, w - 12, ink, ink, label, vis))


def chips(focused):
    f = '$PARAM[focused]' if focused else '!$PARAM[focused]'
    base = '%s + %s + %s' % (NFG, RES, f)
    out = ''
    for has_hdr in (True, False):
        hv = HDR if has_hdr else '!' + HDR
        # the user, on the built rows: "resolution pill shall be on the far right always": the pill ends at CHIPS_END,
        # the other chips run left from it (audio, aspect, HDR)
        x = CHIPS_END - W_RES - GAP
        parts = []
        if has_hdr:
            x -= W_HDR
            parts.append((x, W_HDR, '$VAR[FG_L_HdrChip]', '%s + %s' % (base, HDR)))
            x -= GAP
        x -= W_ASP
        parts.append((x, W_ASP, '$INFO[ListItem.VideoAspect]:1', '%s + %s + !String.IsEmpty(ListItem.VideoAspect)' % (base, hv)))
        x -= GAP + W_AUD
        parts.append((x, W_AUD, '[UPPERCASE]$VAR[FG_EcAudio][/UPPERCASE]', '%s + %s + !String.IsEmpty(ListItem.AudioCodec)' % (base, hv)))
        for px, pw, lab, vis in parts:
            out += chip(px, pw, lab, vis, focused)
    return out


def res_shift(has_hdr):
    """the resolution pill's x: rightmost, ending at CHIPS_END (the user: "on the far right always")"""
    return CHIPS_END - W_RES - 837    # the pill's two-part form starts at 837 today


def title_w(has_hdr):
    """the title and grey line end before the leftmost chip (audio)"""
    start = CHIPS_END - W_RES - GAP - (W_HDR + GAP if has_hdr else 0) - W_ASP - GAP - W_AUD
    return start - 16 - 140


def main():
    t = io.open(VID, encoding='utf-8').read()
    if MARK in t:
        print('already done')
        return
    a = t.index('<include name="Aeon_Row">')
    b = t.index('\t</include>', a)
    row = t[a:b]

    # 1. the resolution pill moves left, in front of the new chips (Aeon / Glass)
    rs = row.index('\t\t\t<!-- resolution badge')
    re_ = row.index('\t\t\t<!-- runtime column')
    pill = row[rs:re_]
    wrap = ('\t\t\t<!-- %s: the pill in front of the audio / aspect / HDR chips (Aeon, Glass) -->\n'
            '\t\t\t<control type="group">'
            '<animation effect="slide" start="0,0" end="%d,0" time="0" condition="%s + %s">Conditional</animation>'
            '<animation effect="slide" start="0,0" end="%d,0" time="0" condition="%s + !%s">Conditional</animation>\n'
            % (MARK, res_shift(True), NFG, HDR, res_shift(False), NFG, HDR)) + pill + '\t\t\t</control>\n'
    row = row[:rs] + wrap + row[re_:]

    # 2. title and grey line end before the chips: the 637-wide labels get two narrower twins
    def narrow(m):
        lab = m.group(0)
        out = lab.replace('</visible>', ' + [Skin.HasSetting(aeon.fglass) | String.IsEmpty(ListItem.VideoResolution)]</visible>', 1)
        for has_hdr in (False, True):
            twin = lab.replace('<width>637</width>', '<width>%d</width>' % title_w(has_hdr), 1)
            twin = twin.replace('</visible>', ' + %s + %s + %s</visible>' % (NFG, RES, HDR if has_hdr else '!' + HDR), 1)
            out += '\n' + twin
        return out
    row, n = re.subn(r'\t\t\t\t<control type="label">\n\t\t\t\t\t<left>140</left>\n\t\t\t\t\t<top>(?:20|58)</top>\n\t\t\t\t\t<width>637</width>.*?</control>',
                     narrow, row, flags=re.S)
    assert n == 4, n

    # 3. the run time gives way to the time left while in progress
    row, n = re.subn(r'(<include content="Aeon_Dur"><param name="left">1014</param>.*?<param name="vis" value=")([^"]*)("/>)',
                     lambda m: m.group(1) + m.group(2) + ' + ![%s + %s]' % (NFG, PROG) + m.group(3), row)
    assert n == 2, n

    # 4. the eye: in its column right before the run time (Aeon / Glass), not while in progress
    for f in ('!$PARAM[focused]', '$PARAM[focused]'):
        old = '<control type="group"><visible>!Container.Content(tvshows) + %s</visible>' % f
        assert row.count(old) == 1, old
        row = row.replace(old, '<control type="group"><visible>!Container.Content(tvshows) + %s + ![%s + %s]</visible>'
                          '<animation effect="slide" start="0,0" end="%d,0" time="0" condition="%s">Conditional</animation>'
                          % (f, NFG, PROG, MARK_X - 783, NFG), 1)

    # 5. new: chips, the progress ring and the time left
    new = ('\t\t\t<!-- %s: audio, aspect ratio, HDR chips right-aligned before the mark (Aeon, Glass) -->\n' % MARK +
           '\t\t\t' + chips(False) + '\t\t\t' + chips(True) +
           '\t\t\t<!-- in progress: the ring in the mark column, the time left in the run-time column -->\n'
           '\t\t\t<control type="image"><left>%d</left><top>40</top><width>28</width><height>28</height><texture colordiffuse="fg_mark">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>%s + %s + !$PARAM[focused]</visible></control>\n'
           '\t\t\t<control type="image"><left>%d</left><top>40</top><width>28</width><height>28</height><texture colordiffuse="$VAR[Aeon_OnBarInk_L]">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>%s + %s + $PARAM[focused]</visible></control>\n'
           '\t\t\t<control type="label"><left>996</left><top>0</top><width>94</width><height>aeon_row_h</height><align>center</align><aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>fg_mark</textcolor><selectedcolor>fg_mark</selectedcolor><label>$VAR[Aeon_RowLeft]</label><visible>%s + %s + !$PARAM[focused]</visible></control>\n'
           '\t\t\t<control type="label"><left>996</left><top>0</top><width>94</width><height>aeon_row_h</height><align>center</align><aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>$VAR[Aeon_OnBarInk_L]</textcolor><selectedcolor>$VAR[Aeon_OnBarInk_L]</selectedcolor><label>$VAR[Aeon_RowLeft]</label><visible>%s + %s + $PARAM[focused]</visible></control>\n'
           % (MARK_X, NFG, PROG, MARK_X, NFG, PROG, NFG, PROG, NFG, PROG))
    d = row.rindex('\t\t</definition>')
    row = row[:d] + new + row[d:]
    t = t[:a] + row + t[b:]

    # 6. above the rows: the kicker and the plot (the List view of films / episodes, Aeon and Glass)
    anchor = '\t\t\t<!-- right strip: clock box, A-Z jump list, scroll bar, item count. Boxes are one row high. -->'
    assert t.count(anchor) == 1
    L = 'Container(510).ListItem'
    top = ('\t\t\t<!-- %s: the info panel rule over the rows: kicker and plot (Aeon, Glass) -->\n'
           '\t\t\t<control type="group"><left>760</left><top>56</top><visible>%s + Control.IsVisible(510) + [String.IsEqual(%s.DBType,movie) | String.IsEqual(%s.DBType,episode)]</visible>\n'
           '\t\t\t\t<control type="label"><left>0</left><top>0</top><width>1010</width><height>30</height><font>lb_cap_20</font><textcolor>$VAR[Aeon_Accent]</textcolor><label>[UPPERCASE]$VAR[Aeon_L510_Kicker][/UPPERCASE]</label></control>\n'
           '\t\t\t\t<control type="textbox"><left>0</left><top>42</top><width>1010</width><height>200</height><font>lb_small_20</font><textcolor>c7ffffff</textcolor><label>$INFO[%s.Plot]</label><autoscroll delay="8000" time="3000" repeat="10000">true</autoscroll></control>\n'
           '\t\t\t</control>\n' % (MARK, NFG, L, L, L))
    t = t.replace(anchor, top + anchor)
    kick = ('\t<!-- %s: the List view\'s kicker (Aeon, Glass) -->\n'
            '\t<variable name="Aeon_L510_Kicker">\n'
            '\t\t<value condition="String.IsEqual(Container(510).ListItem.DBType,episode)">$INFO[Container(510).ListItem.Season,$LOCALIZE[20373] ,]$INFO[Container(510).ListItem.Episode,  ·  $LOCALIZE[20359] ,]</value>\n'
            '\t\t<value>$LOCALIZE[20338]$INFO[Container(510).ListItem.Genre,  ·  ,]</value>\n'
            '\t</variable>\n' % MARK)
    kick += ('\t<!-- the time left of a row\'s item as the run-time column writes a run time (helper 0.3.94 aeon.left.N.hm) -->\n'
             '\t<variable name="Aeon_RowLeft">\n' + ''.join(
                 '\t\t<value condition="Integer.IsGreater(ListItem.PercentPlayed,0) + String.IsEqual(ListItem.DBID,Window(Home).Property(aeon.left.%d.id)) + '
                 'String.IsEqual(ListItem.DBType,Window(Home).Property(aeon.left.%d.type))">$INFO[Window(Home).Property(aeon.left.%d.hm)]</value>\n' % (k, k, k)
                 for k in range(1, 41)) + '\t</variable>\n')
    assert t.count('</includes>') == 1
    t = t.replace('</includes>', kick + '</includes>')
    io.open(VID, 'w', encoding='utf-8', newline='\n').write(t)

    # 7. the band
    v = io.open(V2, encoding='utf-8').read()
    a = v.index('<include name="Aeon_V_Bar510">')
    b = v.index('\t</include>', a)
    bar = v[a:b]
    g1 = bar.index('<control type="grouplist"><left>760</left><top>984</top>')
    g1e = bar.index('\t\t\t</control>', g1)
    facts = bar[g1:g1e]
    # the year after the ratings, Ends after the run time
    plain = ('<control type="label"><width min="10" max="300">auto</width><height>34</height><aligny>center</aligny><font>lb_ui_24_bold</font>'
             '<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>%s</label><visible>%s</visible></control>\n')
    first_btn = facts.index('<control type="button">')
    facts = facts[:first_btn] + plain % ('$INFO[ListItem.Year]', '!String.IsEmpty(ListItem.Year)') + facts[first_btn:]
    facts += plain % ('[UPPERCASE]$LOCALIZE[31030] $INFO[ListItem.EndTimeResume][/UPPERCASE]', '!String.IsEmpty(ListItem.EndTimeResume)')
    bar = bar[:g1] + facts + bar[g1e:]
    # the chips row: the status line first; one audio chip; HDR with the profile; no SDR
    g2 = bar.index('<control type="grouplist"><left>760</left><top>1030</top>')
    g2e = bar.index('\t\t\t</control>', g2)
    row2 = bar[g2:g2e]
    lines = row2.split('\n')
    head, items = lines[0], [l for l in lines[1:] if l.strip()]
    keep = []
    for l in items:
        if '$VAR[Aeon_LVCh]' in l or 'Property(aeon.dvp)' in l:
            continue                                           # merged into the audio chip / the HDR chip
        l = l.replace('$VAR[Aeon_LVAud]', '$VAR[FG_L510_Audio]').replace('$VAR[Aeon_LVHdr]', '$VAR[FG_L510_Hdr]')
        if '$VAR[FG_L510_Hdr]' in l:
            l = re.sub(r'<visible>(.*?)</visible>', r'<visible>\1 + !String.IsEmpty(ListItem.HdrType)</visible>', l, count=1) \
                if '<visible>' in l else l.replace('</control>', '<visible>!String.IsEmpty(ListItem.HdrType)</visible></control>', 1)
        keep.append(l)
    # order: resolution, audio, aspect, HDR (pairs: unfocused / focused copies stay together)
    def key(l):
        for i, k in enumerate(('FG_L510_Audio', 'Aeon_LVAsp', 'FG_L510_Hdr', 'Aeon_LVRes')):   # resolution last
            if k in l:
                return i
        return 9
    keep.sort(key=key)
    status = ('<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye_off.png</texture><visible>$EXP[FG_L510_Dot]</visible></control>\n'
              '<control type="image"><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">common/aeon_eye.png</texture><visible>$EXP[FG_L510_Tick]</visible></control>\n'
              '<control type="image"><width>30</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>$EXP[FG_L510_Ring]</visible></control>\n'
              '<control type="label"><width min="10" max="400">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>[UPPERCASE]$VAR[FG_L510_Status][/UPPERCASE]</label><visible>!$EXP[FG_L510_Ring]</visible></control>\n'
              '<control type="label"><width min="10" max="400">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>fg_mark</textcolor><selectedcolor>fg_mark</selectedcolor><label>[UPPERCASE]$VAR[FG_L510_Status][/UPPERCASE]</label><visible>$EXP[FG_L510_Ring]</visible></control>\n'
              '<control type="label"><width>6</width><height>34</height><label></label></control>\n')
    row2 = head + '\n' + status + '\n'.join(keep) + '\n'
    bar = bar[:g2] + row2 + bar[g2e:]
    # the studio's name (or nothing) at the right of the facts row
    SO = 'String.IsEqual(Window(Home).Property(aeon.studio.of),Container(510).ListItem.Studio)'
    studio = ('\t\t\t<!-- %s: the studio: the pack\'s logo, else its name (the helper\'s pick, as in Fused Glass) -->\n'
              '\t\t\t<control type="image"><left>1600</left><top>978</top><width>190</width><height>46</height><aspectratio align="right">keep</aspectratio>'
              '<texture background="true">resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png</texture>'
              '<visible>%s + !Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + %s</visible></control>\n'
              '\t\t\t<control type="label"><left>1300</left><top>984</top><width>490</width><height>34</height><align>right</align><aligny>center</aligny><font>lb_small_20_bold</font>'
              '<textcolor>d9ffffff</textcolor><label>[UPPERCASE]$INFO[Window(Home).Property(aeon.studio.text)][/UPPERCASE]</label>'
              '<visible>%s + !Skin.HasSetting(aeon.nostudio) + String.IsEmpty(Window(Home).Property(aeon.studio)) + !String.IsEmpty(Window(Home).Property(aeon.studio.text)) + %s</visible></control>\n'
              % (MARK, NFG, SO, NFG, SO))
    d = bar.rindex('\t\t</definition>')
    bar = bar[:d] + studio + bar[d:]
    v = v[:a] + bar + v[b:]
    io.open(V2, 'w', encoding='utf-8', newline='\n').write(v)
    ET.parse(VID)
    ET.parse(V2)
    print('ok', res_shift(True), res_shift(False), title_w(True), title_w(False))


if __name__ == '__main__':
    main()
