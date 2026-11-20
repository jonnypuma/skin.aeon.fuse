# -*- coding: utf-8 -*-
"""0.56.16, outside the Aeon view chain (the user, 2026-11-16):
- "actors shall be squares in Aeon theme in all views and windows": the cast on the item information page
  (VidInfo_CastItem) as square photos in the Aeon theme (the face kept at the top), the round ones stay in Glass and
  Fused Glass (Circles 536: _src/aeon_lib_music.py);
- the item information window: a show shows its status (Continuing, Ended ...) where a film or episode shows Ends;
  Ends only for films, episodes and music videos ("no ends at on TV show or season level ... show status ... also add in
  the item show information window too");
- List (510) in Aeon / Glass: the rows start under the info pane (216), seven rows, the focused one where it was
  (FG_510Geom_old; the pane itself: _src/aeon_lib_round3.py). Runs once."""
import io
import os
import xml.etree.ElementTree as ET

VI = os.path.join('1080i', 'Includes_VideoInfo.xml')
FU = os.path.join('1080i', 'Includes_Fused.xml')
MARK = '0.56.16 misc_05616'


def patch(fn, pairs):
    t = io.open(fn, encoding='utf-8').read()
    if MARK in t:
        return False
    for old, new, n in pairs:
        assert t.count(old) == n, (fn, old[:90], t.count(old))
        t = t.replace(old, new)
    io.open(fn, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(fn)
    return True


RING = '<control type="image"><left>-6</left><top>-6</top><width>158</width><height>158</height><texture colordiffuse="$VAR[Aeon_Accent]">aeon/ring_cast.png</texture><visible>$PARAM[focused] + Control.HasFocus(50)</visible></control>'
DISC = '<control type="image"><left>0</left><top>0</top><width>146</width><height>146</height><texture colordiffuse="$VAR[AG_Raised]">aeon/disc_cast.png</texture></control>'
PHOTO = '<texture background="true" diffuse="aeon/mask_cast.png">$INFO[ListItem.Art(thumb)]</texture>\n\t\t\t\t</control>'


def main():
    d1 = patch(VI, [
        (RING, '<!-- %s: square in the Aeon theme (a frame in the accent while focused, the photo from its top) -->\n\t\t\t\t'
               '<control type="image"><left>-6</left><top>-6</top><width>158</width><height>158</height><texture colordiffuse="$VAR[Aeon_Accent]">common/white.png</texture><visible>$PARAM[focused] + Control.HasFocus(50) + !$EXP[Aeon_VGlass]</visible></control>\n\t\t\t\t'
               '<control type="image"><left>0</left><top>0</top><width>146</width><height>146</height><texture colordiffuse="$VAR[AG_Raised]">common/white.png</texture><visible>!$EXP[Aeon_VGlass]</visible></control>\n\t\t\t\t'
               % MARK + RING.replace('Control.HasFocus(50)</visible>', 'Control.HasFocus(50) + $EXP[Aeon_VGlass]</visible>'), 1),
        (DISC, DISC.replace('</control>', '<visible>$EXP[Aeon_VGlass]</visible></control>'), 1),
        (PHOTO, PHOTO.replace('\n\t\t\t\t</control>', '\n\t\t\t\t\t<visible>$EXP[Aeon_VGlass]</visible>\n\t\t\t\t</control>') +
         '\n\t\t\t\t<control type="image"><left>0</left><top>0</top><width>146</width><height>146</height><aspectratio align="center" aligny="top">scale</aspectratio><fadetime>160</fadetime>'
         '<texture background="true">$INFO[ListItem.Art(thumb)]</texture><visible>!$EXP[Aeon_VGlass]</visible></control>', 1),
        ('\t\t<value condition="ListItem.IsResumable">$ADDON[skin.aeon.fuse 32333] $INFO[ListItem.EndTimeResume]</value>\n'
         '\t\t<value condition="!String.IsEmpty(ListItem.Duration) + String.IsEmpty(ListItem.Property(aeon.missing))">$ADDON[skin.aeon.fuse 32334] $INFO[ListItem.EndTime]</value>',
         '\t\t<!-- %s: a show its status, Ends only for what plays -->\n'
         '\t\t<value condition="String.IsEqual(ListItem.DBType,tvshow) + !String.IsEmpty(ListItem.Status)">$VAR[Aeon_ShowStatus]</value>\n'
         '\t\t<value condition="ListItem.IsResumable + [String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,musicvideo)]">$ADDON[skin.aeon.fuse 32333] $INFO[ListItem.EndTimeResume]</value>\n'
         '\t\t<value condition="!String.IsEmpty(ListItem.Duration) + String.IsEmpty(ListItem.Property(aeon.missing)) + [String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,musicvideo)]">$ADDON[skin.aeon.fuse 32334] $INFO[ListItem.EndTime]</value>' % MARK, 1)])
    d2 = patch(FU, [('<include name="FG_510Geom_old"><top>0</top><height>972</height><focusposition>5</focusposition></include>',
                     '<!-- %s: Aeon / Glass List rows under the info pane (216..972, seven rows) -->\n\t<include name="FG_510Geom_old"><top>216</top><height>756</height><focusposition>3</focusposition></include>' % MARK, 1)])
    # the info page's "fits before midnight" tick reads the run time too: films / episodes / music videos only
    t = io.open(VI, encoding='utf-8').read()
    d3 = False
    if MARK + 'b' not in t:
        old = '<visible>$EXP[AG_ItemFits]</visible>'
        assert t.count(old) == 2, t.count(old)
        t = t.replace(old, '<visible>$EXP[AG_ItemFits] + [String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,musicvideo)]</visible>')
        t = t.replace('<variable name="VidInfo_EndLine">', '<!-- %sb: the fits tick only for what plays -->\n\t<variable name="VidInfo_EndLine">' % MARK, 1)
        # a show without a run time still shows its status
        old = '<usecontrolcoords>true</usecontrolcoords>\n\t\t\t\t\t\t<visible>!String.IsEmpty(ListItem.Duration)</visible>'
        assert t.count(old) == 1, t.count(old)
        t = t.replace(old, old.replace('!String.IsEmpty(ListItem.Duration)</visible>', '!String.IsEmpty(ListItem.Duration) | [String.IsEqual(ListItem.DBType,tvshow) + !String.IsEmpty(ListItem.Status)]</visible>'))
        io.open(VI, 'w', encoding='utf-8', newline='\n').write(t)
        ET.parse(VI)
        d3 = True
    print('ok', d1, d2, d3)


if __name__ == '__main__':
    main()
