"""0.56.25 Aeon Glass fixes (idempotent; run from the skin folder).

1. Kodi settings pages (SetCat_Classic) and add-on settings (AddonSet_Classic) in Aeon Glass: the first category and the
   Settings level button touch the card's rounded corners (r28, card 100,180 1720x684) but their highlight was square.
   Kodi clones one focus texture for every category, so the first category's bar is drawn by AG_CatGlassCorners with the
   card's corner cut out (its own texture turns clear then: Aeon_TexCatFocus_g / Aeon_CatFocColG), the faded bar of the
   open category as well (Kodi fades it to 0x80), and the parent bar overlay takes the same shape. The level button gets
   textures with the card's bottom-left corner (AG_SettingLevelButton round=true), its last row clear (it reached 1 px
   below the card).
   The corner pictures copy the card's own corner (media/fg/r28.png) so the edges meet exactly.
2. Skin settings in Aeon Glass: one rounded card for both columns (like the Kodi settings pages) instead of two cards
   inside a square hairline frame; the frame and the square category outline are gone there.
3. File manager in Aeon Glass: the two-way arrow between the two cards (the Aeon bar stays Aeon only).
"""
import io, os, re
from PIL import Image

D = '1080i'
MEDIA = 'media'
VG = 'Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass) + !String.IsEqual(Skin.String(aeon.menutheme),fused)'


def rd(p):
    return io.open(os.path.join(D, p), encoding='utf-8').read()


def wr(p, t):
    io.open(os.path.join(D, p), 'w', encoding='utf-8', newline='\n').write(t)


def once(t, old, new, tag):
    if new in t:
        return t
    assert t.count(old) == 1, (tag, t.count(old))
    return t.replace(old, new)


# ---------------------------------------------------------------- pictures
def pictures():
    a = Image.open(os.path.join(MEDIA, 'fg', 'r28.png')).convert('RGBA').split()[3]
    tl = a.crop((0, 0, 28, 28))          # the card's top-left corner
    bl = a.crop((0, 44, 28, 72))         # the card's bottom-left corner
    W, H = 380, 76
    # first category: drawn at y 181, one row below the card top (180) -> the corner shifted up one row
    m = Image.new('L', (W, H), 255)
    m.paste(tl.crop((0, 1, 28, 28)), (0, 0))
    # level button: drawn at y 789..864; the card's corner rows are 836..863 (button rows 47..74), row 75 lies below the card
    n = Image.new('L', (W, H), 255)
    n.paste(bl, (0, 47))
    n.paste(Image.new('L', (W, 1), 0), (0, 75))
    for name, mask in (('cat_tl380', m), ('lvl_bl380', n)):
        for suf, alpha in (('', 74), ('w', 255)):    # '' = the glass row (aeon_row_glass.png is white at alpha 74)
            img = Image.new('RGBA', (W, H), (255, 255, 255, 0))
            img.putalpha(mask.point(lambda v, k=alpha: v * k // 255))
            img.save(os.path.join(MEDIA, 'aeon', name + suf + '.png'), optimize=True)
    print('pictures written')


# ---------------------------------------------------------------- settings pages
CORNERS = '''	<!-- 0.56.25 Aeon Glass (_src/aeonglass_corners_05625.py): the first category sits in the card's rounded top-left corner.
	     Kodi draws one focus texture for every cloned category, so its bar is drawn here with the corner cut out (the
	     button's own texture is clear then: Aeon_TexCatFocus_g); Kodi fades the open category's bar to 0x80 (half) and keeps it
	     focused inside the grouplist, so Container(3).CurrentItem names the open category (add-on settings open with the
	     focus in the list, where ControlGroup(3).HasFocus(-200) is false). -->
	<include name="AG_CatGlassCorners">
		<control type="group">
			<visible>%s + !Container(3).HasPrevious</visible>
			<control type="image"><left>100</left><top>181</top><width>380</width><height>76</height><texture colordiffuse="aeon_accent">aeon/cat_tl380.png</texture><visible>Control.HasFocus(-200)</visible></control>
			<control type="image"><left>100</left><top>181</top><width>380</width><height>76</height><texture colordiffuse="aeon_accent">aeon/cat_tl380.png</texture><animation effect="fade" start="50" end="50" time="0" condition="true">Conditional</animation><visible>Integer.IsEqual(Container(3).CurrentItem,1) + !Control.HasFocus(-200)</visible></control>
		</control>
	</include>
''' % VG


def settings_pages():
    t = rd('Includes_Aeon_Menu.xml')
    t = once(t, '\t<include name="SetCat_Classic">', CORNERS + '\t<include name="SetCat_Classic">', 'corners include')
    # parent bar overlay of the first category: the rounded picture in Aeon Glass
    old = ('<control type="image"><left>100</left><top>181</top><width>380</width><height>76</height><texture colordiffuse="$VAR[Aeon_CatParentCol]">common/white.png</texture>'
           '<visible>ControlGroup(3).HasFocus(-200)')
    new = ('<control type="image"><left>100</left><top>181</top><width>380</width><height>76</height><texture colordiffuse="$VAR[Aeon_CatParentCol]">$VAR[Aeon_CatParentTex1]</texture>'
           '<visible>ControlGroup(3).HasFocus(-200)')
    t = once(t, old, new, 'parent bar 1')
    t = once(t, '\t<variable name="Aeon_CatSelInk">',
             '\t<variable name="Aeon_CatParentTex1">\n\t\t<value condition="%s">aeon/cat_tl380w.png</value>\n\t\t<value>common/white.png</value>\n\t</variable>\n'
             '\t<variable name="Aeon_CatSelInk">' % VG, 'parent tex var')
    # the template: a param for the clear first bar
    old = ('''	<include name="Aeon_SettingCategoryTemplate">
		<param name="width">380</param>''')
    new = ('''	<include name="Aeon_SettingCategoryTemplate">
		<param name="width">380</param>
		<param name="roundfirst">false</param>''')
    t = once(t, old, new, 'template param')
    seg_start = t.index('<include name="Aeon_SettingCategoryTemplate">')
    seg_end = t.index('</include>', t.index('</definition>', seg_start)) + 10
    seg = t[seg_start:seg_end]
    if 'Aeon_TexCatFocus' not in seg:
        assert seg.count('<include>Aeon_TexRowFocus</include>') == 1
        seg = seg.replace('<include>Aeon_TexRowFocus</include>',
                          '<include condition="$PARAM[roundfirst]">Aeon_TexCatFocus</include>\n'
                          '\t\t\t\t<include condition="!$PARAM[roundfirst]">Aeon_TexRowFocus</include>')
        t = t[:seg_start] + seg + t[seg_end:]
    # SetCat_Classic and AddonSet_Classic: the corners, the template param, the round level button
    for name in ('SetCat_Classic', 'AddonSet_Classic'):
        s0 = t.index('<include name="%s">' % name)
        s1 = t.index('\n\t</include>', s0)
        blk = t[s0:s1]
        if 'AG_CatGlassCorners' not in blk:
            assert blk.count('<include>Aeon_CatParentBars</include>') == 1, name
            blk = blk.replace('<include>Aeon_CatParentBars</include>',
                              '<include>Aeon_CatParentBars</include>\n\t\t\t<include>AG_CatGlassCorners</include>')
            old = '''<include content="Aeon_SettingCategoryTemplate">
				<param name="width" value="380"/>
			</include>'''
            assert blk.count(old) == 1, name
            blk = blk.replace(old, '''<include content="Aeon_SettingCategoryTemplate">
				<param name="width" value="380"/>
				<param name="roundfirst" value="true"/>
			</include>''')
            old = '''<param name="height" value="76"/>'''
            assert blk.count(old) == 1, name
            blk = blk.replace(old, '''<param name="height" value="76"/>
					<param name="round" value="true"/>''')
            t = t[:s0] + blk + t[s1:]
    wr('Includes_Aeon_Menu.xml', t)

    g = rd('Includes_Aeon_Glass.xml')
    g = once(g, '\t<!-- Aeon_TexRowFocus_L: the library windows',
             '''	<!-- 0.56.25 the category template's focus (Kodi settings / add-on settings pages): as Aeon_TexRowFocus, but in Aeon
	     Glass the first category's bar is clear while AG_CatGlassCorners draws it with the card's corner -->
	<include name="Aeon_TexCatFocus">
		<include condition="String.IsEqual(Skin.String(aeon.menutheme),fused) + !Skin.HasSetting(aeon.fglass)">Aeon_TexRowFocus_u</include>
		<include condition="Skin.HasSetting(aeon.fglass)">Aeon_TexRowFocus_fg</include>
		<include condition="!String.IsEqual(Skin.String(aeon.menutheme),fused) + Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">Aeon_TexCatFocus_g</include>
		<include condition="!String.IsEqual(Skin.String(aeon.menutheme),fused) + !Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">Aeon_TexRowFocus_f</include>
	</include>
	<include name="Aeon_TexCatFocus_g"><texturefocus border="4,0,0,0" colordiffuse="$VAR[Aeon_CatFocColG]">common/aeon_row_glass.png</texturefocus></include>
	<variable name="Aeon_CatFocColG">
		<value condition="Integer.IsEqual(Container(3).CurrentItem,1) + !Container(3).HasPrevious">00ffffff</value>
		<value>aeon_accent</value>
	</variable>
	<!-- Aeon_TexRowFocus_L: the library windows''', 'cat focus include')
    wr('Includes_Aeon_Glass.xml', g)

    s = rd('Includes_Settings.xml')
    s = once(s, '''		<param name="height">56</param>
		<definition>
			<control type="button" id="20">''', '''		<param name="height">56</param>
		<param name="round">false</param>
		<definition>
			<control type="button" id="20">''', 'level param')
    old = '''				<include>Dlg_Tex_RowFocus</include>
				<texturenofocus border="12" colordiffuse="$VAR[Aeon_LevelCol]">$VAR[Aeon_FuseBox12]</texturenofocus>
				<onclick>SettingsLevelChange</onclick>'''
    new = '''				<!-- 0.56.25 round = true (380 x 76 in the Aeon Glass card): the card's bottom-left corner (AG_LevelTexRound) -->
				<include condition="$PARAM[round] + %s">AG_LevelTexRound</include>
				<include condition="![$PARAM[round] + %s]">AG_LevelTexPlain</include>
				<onclick>SettingsLevelChange</onclick>''' % (VG, VG)
    s = once(s, old, new, 'level textures')
    s = once(s, '\t<include name="AG_SettingLevelButton">', '''	<include name="AG_LevelTexPlain">
		<include>Dlg_Tex_RowFocus</include>
		<texturenofocus border="12" colordiffuse="$VAR[Aeon_LevelCol]">$VAR[Aeon_FuseBox12]</texturenofocus>
	</include>
	<include name="AG_LevelTexRound">
		<texturefocus colordiffuse="aeon_accent">aeon/lvl_bl380.png</texturefocus>
		<texturenofocus colordiffuse="$VAR[Aeon_LevelCol]">aeon/lvl_bl380w.png</texturenofocus>
	</include>
	<include name="AG_SettingLevelButton">''', 'level tex includes')
    wr('Includes_Settings.xml', s)
    print('settings pages patched')


# ---------------------------------------------------------------- Skin settings: one card, no square frame
def skin_settings():
    t = rd('SkinSettings.xml')
    two = '<visible>!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible><include>Aeon_Glass</include></control>'
    two_new = '<visible>!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS] + ![$EXP[Aeon_VGlass] + !$EXP[Aeon_Fused]]</visible><include>Aeon_Glass</include></control>'
    if two_new not in t and '0.56.25 Aeon Glass: one rounded card' not in t:     # (0.56.29: the cards take param fgs)
        for geo in ('<control type="group"><left>120</left><top>108</top><width>360</width><height>852</height>',
                    '<control type="group"><left>480</left><top>108</top><width>1340</width><height>852</height>'):
            assert t.count(geo + two) == 1, geo
            t = t.replace(geo + two, geo + two_new)       # only the two page cards (the 280 x 470 preview cards keep theirs)
        t = t.replace('<control type="group"><left>480</left><top>108</top><width>1340</width><height>852</height>' + two_new,
                      '<control type="group"><left>480</left><top>108</top><width>1340</width><height>852</height>' + two_new +
                      '\n\t\t<!-- 0.56.25 Aeon Glass: one rounded card for both columns (like the Kodi settings pages); the dividers at 480 and 1500 stay -->'
                      '\n\t\t<control type="group"><left>120</left><top>108</top><width>1700</width><height>852</height><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass] + !$EXP[Aeon_Fused]</visible><include>Aeon_Glass</include></control>')
    # the square outer frame (top, bottom, left, right): not in Aeon Glass (its card is rounded)
    vis = '<visible>[!$EXP[Aeon_Fused]] + !$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible>'
    for geo in ('<left>120</left><top>108</top><width>1700</width><height>1</height>', '<left>120</left><top>960</top><width>1700</width><height>1</height>',
                '<left>1820</left><top>108</top><width>1</width><height>852</height>', '<left>120</left><top>108</top><width>1</width><height>852</height>'):
        old = '<control type="image">%s<texture colordiffuse="30ffffff">common/white.png</texture>%s' % (geo, vis)
        new = old.replace(vis, '<visible>[!$EXP[Aeon_Fused]] + !$EXP[Aeon_FGlass] + !$EXP[Aeon_MS] + !$EXP[Aeon_VGlass]</visible>')
        if new not in t:
            assert t.count(old) == 1, geo
            t = t.replace(old, new)
    # the square category outline (Aeon menu styles): not in Aeon Glass
    vis = '<visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_FGlass] + $EXP[Aeon_SkinCatFocus]</visible>'
    n = t.count(vis)
    assert n in (0, 4), n
    t = t.replace(vis, '<visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_FGlass] + !$EXP[Aeon_VGlass] + $EXP[Aeon_SkinCatFocus]</visible>')
    wr('SkinSettings.xml', t)
    print('skin settings patched')


# ---------------------------------------------------------------- File manager arrow
def file_manager():
    t = rd('Includes_Misc.xml')
    old = '''				<texture colordiffuse="ffffffff">icons/af3/arrows-left-right.png</texture>
			</control>
		</control>
	</include>'''
    new = '''				<texture colordiffuse="ffffffff">icons/af3/arrows-left-right.png</texture>
			</control>
		</control>
		<!-- 0.56.25 Aeon Glass: the two-way arrow in the 40 px gap between the cards (120-940, 980-1800; 168-1016), no bar -->
		<control type="image"><left>930</left><top>562</top><width>60</width><height>60</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">icons/af3/arrows-left-right.png</texture><visible>Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)</visible></control>
	</include>'''
    t = once(t, old, new, 'fm arrow')
    wr('Includes_Misc.xml', t)
    print('file manager patched')


# ---------------------------------------------------------------- Skin settings: the last category in the card's corner
def skin_lastcat():
    """Context menu (9559, the last category, y 891-960) sits in the card's rounded bottom-left corner (card 120,108
    1700x852, rows 108-959): its focus bar and its open-category fill get a mask with that corner, the row below the
    card clear (image controls take a diffuse mask)."""
    a = Image.open(os.path.join(MEDIA, 'fg', 'r28.png')).convert('RGBA').split()[3]
    m = Image.new('L', (360, 70), 255)
    m.paste(a.crop((0, 44, 28, 72)), (0, 41))         # card rows 932-959 = image rows 41-68
    m.paste(Image.new('L', (360, 1), 0), (0, 69))      # row 960 lies below the card
    img = Image.new('RGBA', (360, 70), (255, 255, 255, 0))
    img.putalpha(m)
    img.save(os.path.join(MEDIA, 'aeon', 'mask_bl360x70.png'), optimize=True)
    t = rd('SkinSettings.xml')
    mark = '<!-- 0.56.25 Aeon Glass: the last category'
    vg = '$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass] + !$EXP[Aeon_Fused]'
    if mark not in t:
        i = t.index('<visible>Control.HasFocus(9559)</visible>')
        img_start = ('<control type="image"><left>0</left><top>-8</top><width>360</width><height>70</height><texture border="20" '
                     'colordiffuse="$VAR[Aeon_MenuFocusColR]">$VAR[Aeon_MenuFocusTex]</texture>')
        j = t.index(img_start, i)
        k = t.index('</control>', j)
        line = t[j:k]
        assert '<visible>' not in line
        plain = line + '<visible>![%s]</visible>' % vg
        masked = line.replace('<texture border="20" ', '<texture border="20" diffuse="aeon/mask_bl360x70.png" ', 1) + '<visible>%s</visible>' % vg
        t = t[:j] + plain + '</control>\n' + mark + " sits in the card's rounded corner -->\n" + masked + t[k:]
    old = '<param name="id" value="9559"/><param name="top" value="899"/>'
    if old + '<param name="corner" value="true"/>' not in t:
        assert t.count(old) == 1
        t = t.replace(old, old + '<param name="corner" value="true"/>')
    wr('SkinSettings.xml', t)
    s = rd('Includes_Settings.xml')
    old = '\t<include name="Dlg_SkinCategory">\n\t\t<param name="onclick">noop</param>'
    s = once(s, old, old + '\n\t\t<param name="corner">false</param>', 'corner param')
    vis = ('<visible>String.IsEqual(Window(Home).Property(aeon.skincat),$PARAM[key]) + !Control.HasFocus($PARAM[id]) + '
           '!$EXP[Aeon_Fused] + !$EXP[Aeon_FGlass]')
    old = ('\t\t\t\t<control type="image">\n\t\t\t\t\t<left>0</left><top>-8</top><width>360</width><height>70</height>\n'
           '\t\t\t\t\t<texture colordiffuse="$VAR[Aeon_ParentCol]">common/white.png</texture>\n'
           '\t\t\t\t\t' + vis + '</visible>\n\t\t\t\t</control>')
    new = ('\t\t\t\t<control type="image">\n\t\t\t\t\t<left>0</left><top>-8</top><width>360</width><height>70</height>\n'
           '\t\t\t\t\t<texture colordiffuse="$VAR[Aeon_ParentCol]">common/white.png</texture>\n'
           '\t\t\t\t\t' + vis + ' + ![$PARAM[corner] + $EXP[Aeon_VGlass]]</visible>\n\t\t\t\t</control>\n'
           '\t\t\t\t<!-- 0.56.25 corner = true (the last category) in Aeon Glass: the card\'s bottom-left corner -->\n'
           '\t\t\t\t<control type="image">\n\t\t\t\t\t<left>0</left><top>-8</top><width>360</width><height>70</height>\n'
           '\t\t\t\t\t<texture colordiffuse="$VAR[Aeon_ParentCol]" diffuse="aeon/mask_bl360x70.png">common/white.png</texture>\n'
           '\t\t\t\t\t' + vis + ' + $PARAM[corner] + $EXP[Aeon_VGlass]</visible>\n\t\t\t\t</control>')
    s = once(s, old, new, 'parent corner')
    wr('Includes_Settings.xml', s)
    print('last category patched')


if __name__ == '__main__':
    pictures()
    settings_pages()
    skin_settings()
    file_manager()
    skin_lastcat()
