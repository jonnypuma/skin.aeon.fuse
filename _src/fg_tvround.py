"""0.39.4 Live TV, Fused Glass:
- The white focus of the area tabs and of the options row (AG_SubNavButton: group, sort, order...) was the Fused button
  focus texture (fxb_pill.png: about 18 px corners), next to frosted pills with fully round ends (r22.png at 44 px).
  Both now use the same round pill: r22.png white (focus style Frost: a light frost, Outline: the white ring e22.png,
  Flat keeps its flat bar). AG_SubNavButton is also used by the add-on browser and playlist windows: same pills there.
- Live TV always draws in Figtree: the few labels of the TV windows and TV dialogs that used the font preset's section
  names (lb_ / pl_) use the plain names, which come from Kodi's font set (Figtree; Roboto CJK in the CJK set). Figtree
  has the channel symbols (_src/fg_figtree_symbols.py); most preset text families do not.
Run in 1080i."""
import io
import re

# ---- the tab focus pill on the card (Misc_PVRFrame)
p = 'Includes_Misc.xml'
s = io.open(p, encoding='utf-8').read()
pad = re.compile(r'\t\t\t\t<control type="image"><left>(\d+)</left><top>6</top><width>204</width><height>54</height><texture border="20,18,20,24">\$VAR\[Misc_PVRTabFocusTex\]</texture><visible>\$EXP\[Aeon_FGlass\] \+ Control.HasFocus\((\d+)\) \+ !String.IsEqual\(Skin.String\(aeon.fgfocus\),flat\)</visible><include>FG_LandVisible</include></control>\n')
found = pad.findall(s)
assert len(found) == 6, found


def pills(m):
    x, cid = int(m.group(1)) + 4, m.group(2)
    return ('\t\t\t\t<control type="image"><left>%d</left><top>8</top><width>196</width><height>44</height><texture border="22" colordiffuse="$VAR[FG_PillFocusCol]">fg/r22.png</texture><visible>$EXP[Aeon_FGlass] + Control.HasFocus(%s) + !String.IsEqual(Skin.String(aeon.fgfocus),flat) + !String.IsEqual(Skin.String(aeon.fgfocus),outline)</visible><include>FG_LandVisible</include></control>\n'
            '\t\t\t\t<control type="image"><left>%d</left><top>8</top><width>196</width><height>44</height><texture border="22" colordiffuse="ffffffff">fg/e22.png</texture><visible>$EXP[Aeon_FGlass] + Control.HasFocus(%s) + String.IsEqual(Skin.String(aeon.fgfocus),outline)</visible><include>FG_LandVisible</include></control>\n'
            % (x, cid, x, cid))


s = pad.sub(pills, s)
s = s.replace('in Fused Glass the focus pill is drawn here too, its body exactly on the tab. -->',
              'in Fused Glass the focus pill is drawn here too: the round r22 pill of the frosted ones, exactly on the tab. -->', 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)

# ---- variables / includes
p = 'Includes_Fused.xml'
t = io.open(p, encoding='utf-8').read()
a = t.index('\t<variable name="Misc_PVRTabFocusTex">')
b = t.index('</variable>', a) + len('</variable>')
t = t[:a] + '''	<!-- 0.39.4 round focus pill (TV area tabs, options rows): white; a light frost in the Frost focus style -->
	<variable name="FG_PillFocusCol">
		<value condition="String.IsEqual(Skin.String(aeon.fgfocus),frost)">4dffffff</value>
		<value>ffffffff</value>
	</variable>
	<include name="FG_SubNavFocus">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_SubNavFocus_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_TexRowFocus</include>
	</include>
	<include name="FG_SubNavFocus_fg">
		<include>FG_LandFocus</include>
		<include condition="String.IsEqual(Skin.String(aeon.fgfocus),flat)">FG_BtnFocusTex_flat</include>
		<include condition="String.IsEqual(Skin.String(aeon.fgfocus),frost)">FG_PillFocus_frost</include>
		<include condition="String.IsEqual(Skin.String(aeon.fgfocus),outline)">FG_PillFocus_outline</include>
		<include condition="!String.IsEqual(Skin.String(aeon.fgfocus),flat) + !String.IsEqual(Skin.String(aeon.fgfocus),frost) + !String.IsEqual(Skin.String(aeon.fgfocus),outline)">FG_PillFocus_white</include>
	</include>
	<include name="FG_PillFocus_white"><texturefocus border="22" colordiffuse="ffffffff">fg/r22.png</texturefocus></include>
	<include name="FG_PillFocus_frost"><texturefocus border="22" colordiffuse="4dffffff">fg/r22.png</texturefocus></include>
	<include name="FG_PillFocus_outline"><texturefocus border="22" colordiffuse="ffffffff">fg/e22.png</texturefocus></include>''' + t[b:]
io.open(p, 'w', encoding='utf-8', newline='').write(t)

# ---- the options row buttons
p = 'Includes_Common.xml'
c = io.open(p, encoding='utf-8').read()
a = c.index('<include name="AG_SubNavButton">')
b = c.index('</definition>', a)
blk = c[a:b]
assert blk.count('<include>Aeon_TexRowFocus</include>') == 1
c = c[:a] + blk.replace('<include>Aeon_TexRowFocus</include>', '<include>FG_SubNavFocus</include>') + c[b:]
io.open(p, 'w', encoding='utf-8', newline='').write(c)

# ---- Figtree in the TV windows and dialogs
files = ('MyPVRChannels.xml', 'MyPVRGuide.xml', 'MyPVRRecordings.xml', 'MyPVRTimers.xml', 'MyPVRSearch.xml',
         'DialogPVRChannelGuide.xml', 'DialogPVRChannelsOSD.xml', 'DialogPVRInfo.xml', 'DialogPVRRadioRDSInfo.xml',
         'DialogPVRGuideControls.xml', 'DialogPVRGuideSearch.xml', 'DialogPVRChannelManager.xml', 'DialogPVRGroupManager.xml')
fx = io.open('Font.xml', encoding='utf-8').read()
for f in files:
    x = io.open(f, encoding='utf-8').read()
    names = re.findall(r'<font>(?:lb|hm|hd|st|pl)_([a-z0-9_]+)</font>', x)
    for n in set(names):
        assert '<name>%s</name>' % n in fx, n
    y = re.sub(r'<font>(?:lb|hm|hd|st|pl)_([a-z0-9_]+)</font>', r'<font>\1</font>', x)
    if y != x:
        io.open(f, 'w', encoding='utf-8', newline='').write(y)
        print('figtree', f, len(names))
print('ok')
