# -*- coding: utf-8 -*-
"""0.56.29 the Fused Glass style, phase 1 (the user: "it shall be the default menu theme for Fused Glass" ... "Now also
build the Fused Glass style"; the design: canvas EGmWgk5AFMr3yy8fV5DG5j "Menus in the System style", the System screen's
language for every menu). Idempotent; run from the skin folder after skin_previews.py and fg_material.py, then ok_only.py.

- Skin style (row 9748, Fused Glass theme): Dark | Clear | Frost | Fused Glass (Skin.String(aeon.fgmenu) = system).
  OK runs script.aeon.helper skinstyle (helper 0.3.105): the next style, the library glass with it (Fused Glass: Dark),
  and Kodi starts again when the user agrees, going to or from Fused Glass (its button textures load with the skin).
- Expression FGS. In Skin settings, the Kodi settings pages and add-on settings (this phase), the Fused Glass style
  draws the System screen's language: no cards (Aeon_Glass param fgs), thin rules under the rows, the focus a white bar
  on the left edge with brighter rules above and below (fg/fgs_bar.png) instead of the white pill, the text in focus
  white (the FGS_* twins of the ink variables), no glow under the focus.
- Later phases: the dialogs (context menu, select lists with numbers / pictures, yes / no, favourites) full screen in
  the System grid, labels in capitals, and the style in the Aeon and Aeon Glass themes.
"""
import io
import os
import re

D = '1080i'
L = 'language'
MARK = '0.56.29 fgs_05629'
FGS = 'Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),system)'
INK = ('Aeon_OnBarInk', 'Aeon_OnBarInk2', 'Aeon_OnBarInk3', 'Aeon_OnBarIcon', 'Aeon_OnBarFill', 'Aeon_OnBarTrack', 'Aeon_OnBarLine',
       'Aeon_SegSelTxt', 'Aeon_SegUnselF')
FGS_VALUES = {'Aeon_ParentInk': 'ffffffff', 'Aeon_MenuFocusTex': 'fg/fgs_bar.png', 'FG_CatInk': 'ffffffff'}
HELP_EN = (" Fused Glass: the System screen's menus, full screen with thin rules and a white bar on the row in focus; Kodi "
           "starts again.")
HELP_T = {
    'cs_cz': " Fused Glass: nabídky jako obrazovka Systém, přes celou obrazovku s tenkými linkami a bílým pruhem u vybraného řádku; Kodi se spustí znovu.",
    'da_dk': " Fused Glass: menuerne fra System-skærmen, i fuld skærm med tynde linjer og en hvid bjælke ved rækken i fokus; Kodi starter igen.",
    'de_de': " Fused Glass: die Menüs des System-Bildschirms, bildschirmfüllend mit feinen Linien und einem weißen Balken an der fokussierten Zeile; Kodi startet neu.",
    'el_gr': " Fused Glass: τα μενού της οθόνης Σύστημα, σε πλήρη οθόνη με λεπτές γραμμές και λευκή μπάρα στη γραμμή εστίασης· το Kodi ξεκινά ξανά.",
    'es_es': " Fused Glass: los menús de la pantalla Sistema, a pantalla completa con líneas finas y una barra blanca en la fila enfocada; Kodi se reinicia.",
    'fi_fi': " Fused Glass: Järjestelmä-näytön valikot koko näytöllä ohuin viivoin ja valkoisella palkilla valitun rivin kohdalla; Kodi käynnistyy uudelleen.",
    'fr_fr': " Fused Glass : les menus de l'écran Système, en plein écran avec de fines lignes et une barre blanche sur la ligne sélectionnée ; Kodi redémarre.",
    'hu_hu': " Fused Glass: a Rendszer képernyő menüi, teljes képernyőn, vékony vonalakkal és fehér sávval a kijelölt sornál; a Kodi újraindul.",
    'it_it': " Fused Glass: i menu della schermata Sistema, a schermo intero con linee sottili e una barra bianca sulla riga attiva; Kodi si riavvia.",
    'ja_jp': " Fused Glass: システム画面のメニュー。全画面、細い線、フォーカス行に白いバー。Kodi が再起動します。",
    'ko_kr': " Fused Glass: 시스템 화면의 메뉴. 전체 화면, 가는 선, 포커스된 행의 흰색 막대. Kodi가 다시 시작됩니다.",
    'nb_no': " Fused Glass: menyene fra System-skjermen, i fullskjerm med tynne linjer og en hvit stolpe ved raden i fokus; Kodi starter på nytt.",
    'nl_nl': " Fused Glass: de menu's van het Systeemscherm, schermvullend met dunne lijnen en een witte balk bij de rij met focus; Kodi start opnieuw.",
    'pl_pl': " Fused Glass: menu ekranu System, na pełnym ekranie, z cienkimi liniami i białym paskiem przy zaznaczonym wierszu; Kodi uruchomi się ponownie.",
    'pt_br': " Fused Glass: os menus da tela Sistema, em tela cheia com linhas finas e uma barra branca na linha em foco; o Kodi reinicia.",
    'pt_pt': " Fused Glass: os menus do ecrã Sistema, em ecrã inteiro com linhas finas e uma barra branca na linha em foco; o Kodi reinicia.",
    'ru_ru': " Fused Glass: меню экрана «Система», во весь экран, с тонкими линиями и белой полосой у выбранной строки; Kodi перезапустится.",
    'sv_se': " Fused Glass: menyerna från System-skärmen, i helskärm med tunna linjer och en vit stapel vid raden i fokus; Kodi startar om.",
    'tr_tr': " Fused Glass: Sistem ekranının menüleri; tam ekran, ince çizgiler ve odaktaki satırda beyaz çubuk. Kodi yeniden başlar.",
    'uk_ua': " Fused Glass: меню екрана «Система», на весь екран, з тонкими лініями й білою смугою біля вибраного рядка; Kodi перезапуститься.",
    'zh_cn': " Fused Glass：系统屏幕的菜单，全屏、细线，焦点行有白色竖条；Kodi 将重新启动。",
    'zh_tw': " Fused Glass：系統畫面的選單，全螢幕、細線，焦點列有白色豎條；Kodi 將重新啟動。",
}


def rd(p):
    return io.open(os.path.join(D, p), encoding='utf-8').read()


def wr(p, t):
    io.open(os.path.join(D, p), 'w', encoding='utf-8', newline='\n').write(t)


def once(t, old, new, tag):
    if new in t:
        return t
    assert t.count(old) == 1, (tag, t.count(old))
    return t.replace(old, new)


def picture():
    """fg/fgs_bar.png: the System screen's focus as a 9-slice (border 20): a white bar 5 px wide on the left edge,
    rules (27 %) on the top and bottom edge, clear inside"""
    from PIL import Image
    img = Image.new('RGBA', (48, 48), (255, 255, 255, 0))
    px = img.load()
    for y in range(48):
        for x in range(48):
            if x < 5:
                px[x, y] = (255, 255, 255, 255)
            elif y in (0, 47):
                px[x, y] = (255, 255, 255, 0x44)
    img.save(os.path.join('media', 'fg', 'fgs_bar.png'), optimize=True)


def strings():
    for d in sorted(os.listdir(L)):
        code = d.replace('resource.language.', '')
        p = os.path.join(L, d, 'strings.po')
        t = io.open(p, encoding='utf-8').read()
        m = re.search(r'(msgctxt "#32574"\nmsgid ")([^\n]*)("\nmsgstr ")([^\n]*)(")', t)
        assert m, code
        en = m.group(2) if HELP_EN.strip() in m.group(2) else m.group(2) + HELP_EN.replace('"', '\\"')
        tr = m.group(4)
        if code != 'en_gb' and HELP_T[code].strip() not in tr:
            tr = tr + HELP_T[code].replace('"', '\\"')
        t = t[:m.start()] + m.group(1) + en + m.group(3) + tr + m.group(5) + t[m.end():]
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('help 32574 in 23 languages')


def variables():
    """FGS, FGS_ShadowOn and the FGS_ twins of the ink variables (their light-focus value under the Fused Glass style)"""
    f = rd('Includes_Fused.xml')
    if 'name="FGS"' in f:
        return
    glass = rd('Includes_Aeon_Glass.xml')
    out = '\t<!-- %s: the Fused Glass style (Skin style = Fused Glass) -->\n' % MARK
    out += '\t<expression name="FGS">%s</expression>\n' % FGS
    out += '\t<expression name="FGS_ShadowOn">true</expression>\n'   # 0.56.53: the focus shadow in the style too (user: "i want that everywhere")
    for name in INK:
        m = re.search(r'<variable name="%s">\s*<value condition="Skin\.HasSetting\(aeon\.fglass\) \+ \$EXP\[FG_FocusLight\]">([^<]+)</value>' % name, glass)
        assert m, name
        out += '\t<variable name="FGS_%s">\n\t\t<value condition="$EXP[FGS]">%s</value>\n\t\t<value>$VAR[%s]</value>\n\t</variable>\n' % (name, m.group(1), name)
    for name, v in FGS_VALUES.items():
        out += '\t<variable name="FGS_%s">\n\t\t<value condition="$EXP[FGS]">%s</value>\n\t\t<value>$VAR[%s]</value>\n\t</variable>\n' % (name, v, name)
    f = f.replace('</includes>', out + '</includes>')
    wr('Includes_Fused.xml', f)
    print('expressions and twins written')


def twin(text):
    for name in INK + tuple(FGS_VALUES):
        text = text.replace('$VAR[%s]' % name, '$VAR[FGS_%s]' % name)
    return text


def cards():
    """Aeon_Glass: param fgs (true in the Fused Glass style's windows) hides the card there"""
    g = rd('Includes_Aeon_Glass.xml')
    i = g.index('\t<include name="Aeon_Glass">')
    j = g.index('\t</include>', i)
    blk = g[i:j]
    if 'param name="fgs"' not in blk:
        new = blk.replace('<include name="Aeon_Glass">\n\t\t<definition>', '<include name="Aeon_Glass">\n\t\t<param name="fgs">false</param>\n\t\t<definition>', 1)
        assert new != blk
        n = new.count('<visible>$EXP[Aeon_FGlass]</visible>')
        assert n == 3, n
        new = new.replace('<visible>$EXP[Aeon_FGlass]</visible>', '<visible>$EXP[Aeon_FGlass] + ![$PARAM[fgs] + $EXP[FGS]]</visible>')
        g = g[:i] + new + g[j:]
        wr('Includes_Aeon_Glass.xml', g)
    print('cards: param fgs')


def skin_settings():
    t = rd('SkinSettings.xml')
    n0 = t.count('<include>Aeon_Glass</include>')
    t = t.replace('<include>Aeon_Glass</include>', '<include content="Aeon_Glass"><param name="fgs" value="true"/></include>')
    t = twin(t)
    t = t.replace('$EXP[FG_FocusShadowOn]', '$EXP[FGS_ShadowOn]')
    # the rules under the rows (Aeon's) under the Fused Glass style too
    rule = re.compile(r'(<control type="image">[^\n]*?<height>1</height><texture colordiffuse="[0-9a-f]{8}">common/white\.png</texture>)<visible>!\$EXP\[Aeon_Fused\] \+ !\$EXP\[Aeon_FGlass\]</visible>')
    t, n1 = rule.subn(r'\1<visible>!$EXP[Aeon_Fused] + [!$EXP[Aeon_FGlass] | $EXP[FGS]]</visible>', t)
    # the Skin style row (9748): four styles in Fused Glass, OK through the helper
    for c in ('<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),glass)">Skin.SetString(aeon.fgmenu,frost)</onclick>',
              '<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),glass)">Skin.SetString(aeon.fgmat,frost)</onclick>',
              '<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.Reset(aeon.fgmenu)</onclick>',
              '<onclick condition="Skin.HasSetting(aeon.fglass) + String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.Reset(aeon.fgmat)</onclick>',
              '<onclick condition="Skin.HasSetting(aeon.fglass) + !String.IsEqual(Skin.String(aeon.fgmenu),glass) + !String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.SetString(aeon.fgmenu,glass)</onclick>',
              '<onclick condition="Skin.HasSetting(aeon.fglass) + !String.IsEqual(Skin.String(aeon.fgmenu),glass) + !String.IsEqual(Skin.String(aeon.fgmenu),frost)">Skin.SetString(aeon.fgmat,clear)</onclick>'):
        t = re.sub(r'\n\s*' + re.escape(c), '', t)
    first = '<onclick condition="!Skin.HasSetting(aeon.fglass)">RunScript(script.aeon.helper,menutheme)</onclick>'
    t = once(t, first, first + '\n\t\t\t\t\t<onclick condition="Skin.HasSetting(aeon.fglass)">RunScript(script.aeon.helper,skinstyle)</onclick>', 'style click')
    # its Fused Glass pills: Dark | Clear | Frost | Fused Glass
    old_mark = '<!-- Fused Glass (0.56.12): Dark (default) | Glass | Frost, aeon.fgmenu (_src/fg_frostmenus.py) -->'
    if old_mark in t:
        a = t.index(old_mark)
        b = t.index('\n\t\t\t</control>', a)
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import expert_05628 as X
        opts = [('', '$ADDON[skin.aeon.fuse 32573]', 112), ('glass', '$ADDON[skin.aeon.fuse 32549]', 108),
                ('frost', '$ADDON[skin.aeon.fuse 32547]', 108), ('system', '$ADDON[skin.aeon.fuse 32402]', 172)]
        pills = X.pills(9748, 'aeon.fgmenu', opts)
        new = ('<!-- Fused Glass (0.56.12, %s): Dark (default) | Clear | Frost | Fused Glass, aeon.fgmenu -->\n'
               '\t\t\t\t<control type="group"><visible>Skin.HasSetting(aeon.fglass)</visible>\n%s\t\t\t\t</control>' % (MARK, pills))
        t = t[:a] + new + t[b:]
    wr('SkinSettings.xml', t)
    print('skin settings: cards %d, rules %d' % (n0, n1))
    s = rd('Includes_Settings.xml')
    for inc in ('Dlg_SkinCategory', 'Dlg_SkinRowChrome', 'Dlg_SkinRowButton'):
        if '<include name="%s">' % inc not in s:
            continue
        i = s.index('<include name="%s">' % inc)
        j = s.index('\n\t</include>', i)
        blk = s[i:j]
        new = twin(blk)
        new = re.sub(r'(<control type="image"><left>0</left><top>-8</top><width>360</width><height>1</height><texture colordiffuse="30ffffff">common/white\.png</texture>)<visible>!\$EXP\[Aeon_Fused\] \+ !\$EXP\[Aeon_FGlass\]</visible>',
                     r'\1<visible>!$EXP[Aeon_Fused] + [!$EXP[Aeon_FGlass] | $EXP[FGS]]</visible>', new)
        s = s[:i] + new + s[j:]
    old = ('<control type="image"><left>0</left><top>-8</top><width>360</width><height>70</height><texture border="16" colordiffuse="80ffffff">fg/selrow16.png</texture>'
           '<visible>String.IsEqual(Window(Home).Property(aeon.skincat),$PARAM[key]) + !Control.HasFocus($PARAM[id]) + $EXP[Aeon_FGlass]</visible></control>')
    if 'the Fused Glass style marks the open category' not in s:
        assert s.count(old) == 1
        s = s.replace(old, old.replace('$EXP[Aeon_FGlass]</visible>', '$EXP[Aeon_FGlass] + !$EXP[FGS]</visible>') +
                      '\n\t\t\t\t<!-- 0.56.29 fgs_05629: the Fused Glass style marks the open category with the System bar, dimmed -->\n'
                      '\t\t\t\t' + old.replace('border="16"', 'border="20"').replace('fg/selrow16.png', 'fg/fgs_bar.png')
                      .replace('$EXP[Aeon_FGlass]</visible>', '$EXP[FGS]</visible>'))
    wr('Includes_Settings.xml', s)


def settings_pages():
    f = rd('Includes_Fused.xml')
    # the row template: a param fgs (the Fused Glass style's pages) for the bar focus, the rule and white ink
    f = once(f, '''	<include name="FG_SettingRow">
		<param name="width">1236</param>
		<param name="textoffsetx">24</param>''', '''	<include name="FG_SettingRow">
		<param name="width">1236</param>
		<param name="textoffsetx">24</param>
		<param name="fgs">false</param>''', 'row param')
    i = f.index('<include name="FG_SettingRow">')
    j = f.index('\n\t</include>', i)
    blk = f[i:j]
    if 'FGS_RowTex' not in blk:
        blk = blk.replace('<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>', '<focusedcolor>$VAR[$PARAM[pre]Aeon_OnBarInk]</focusedcolor>')
        blk = blk.replace('<include>FG_BtnFocusTex</include>\n\t\t\t<texturenofocus />',
                          '<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_RowTex</include>\n'
                          '\t\t\t<include condition="![$PARAM[fgs] + $EXP[FGS]]">FG_RowTex</include>')
        blk = blk.replace('<param name="fgs">false</param>', '<param name="fgs">false</param>\n\t\t<param name="pre"></param>')
        assert 'FGS_RowTex' in blk and '$PARAM[pre]' in blk
        f = f[:i] + blk + f[j:]
        f = f.replace('\t<include name="FG_SettingRow">',
                      '\t<!-- %s: the Fused Glass style\'s settings row: the System screen\'s focus (bar + rules), a rule under the row -->\n'
                      '\t<include name="FGS_RowTex">\n\t\t<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus>\n'
                      '\t\t<texturenofocus border="0,0,0,1" colordiffuse="1fffffff">common/aeon_rule_h.png</texturenofocus>\n\t</include>\n'
                      '\t<include name="FG_RowTex">\n\t\t<include>FG_BtnFocusTex</include>\n\t\t<texturenofocus />\n\t</include>\n'
                      '\t<include name="FG_SettingRow">' % MARK, 1)
    # the templates pass fgs / pre on; their own ink variables take the prefix
    i = f.index('<include name="FG_SettingTemplates">')
    j = f.index('\n\t</include>', i)
    blk = f[i:j]
    if '<param name="fgs">' not in blk:
        blk = blk.replace('<param name="width">1236</param>', '<param name="width">1236</param>\n\t\t<param name="fgs">false</param>\n\t\t<param name="pre"></param>', 1)
        blk = blk.replace('<param name="textoffsetx" value="$PARAM[textoffsetx]"/></include>',
                          '<param name="textoffsetx" value="$PARAM[textoffsetx]"/><param name="fgs" value="$PARAM[fgs]"/><param name="pre" value="$PARAM[pre]"/></include>')
        for name in INK:
            blk = blk.replace('$VAR[%s]' % name, '$VAR[$PARAM[pre]%s]' % name)
        f = f[:i] + blk + f[j:]
    # the page: no cards, fgs on for the rows, the category bar
    i = f.index('<include name="FG_SettingsPage">')
    j = f.index('\n\t</include>', i)
    blk = f[i:j]
    if MARK not in blk:
        n = blk.count('<include>Aeon_Glass</include>')
        assert n == 3, n
        blk = blk.replace('<include>Aeon_Glass</include>', '<include content="Aeon_Glass"><param name="fgs" value="true"/></include>')
        old = '''			<include content="FG_SettingTemplates">
				<param name="width" value="$PARAM[list_w]"/>
			</include>'''
        assert blk.count(old) == 1
        blk = blk.replace(old, '''			<include content="FG_SettingTemplates"><!-- %s -->
				<param name="width" value="$PARAM[list_w]"/>
				<param name="fgs" value="true"/>
				<param name="pre" value="FGS_"/>
			</include>''' % MARK)
        f = f[:i] + blk + f[j:]
    # the category template and the open category's pill: the bar in the Fused Glass style
    i = f.index('<include name="FG_SettingCategoryTemplate">')
    j = f.index('\n\t</include>', i)
    blk = f[i:j]
    if 'FGS' not in blk:
        old = '<texturefocus border="16" colordiffuse="ffffffff">fg/selrow16.png</texturefocus>\n\t\t\t<texturenofocus />'
        assert blk.count(old) == 1
        blk = blk.replace(old, '<include condition="$EXP[FGS]">FGS_RowTex</include>\n\t\t\t<include condition="!$EXP[FGS]">FG_CatTex</include>')
        blk = blk.replace('<focusedcolor>$VAR[FG_CatInk]</focusedcolor>', '<focusedcolor>$VAR[FGS_FG_CatInk]</focusedcolor>')
        blk = blk.replace('<selectedcolor>$VAR[FG_CatInk]</selectedcolor>', '<selectedcolor>$VAR[FGS_FG_CatInk]</selectedcolor>')
        f = f[:i] + blk + f[j:]
        f = f.replace('\t<include name="FG_SettingCategoryTemplate">',
                      '\t<include name="FG_CatTex">\n\t\t<texturefocus border="16" colordiffuse="ffffffff">fg/selrow16.png</texturefocus>\n\t\t<texturenofocus />\n\t</include>\n'
                      '\t<include name="FG_SettingCategoryTemplate">', 1)
    i = f.index('<include name="FG_CatPill">')
    j = f.index('\n\t</include>', i)
    blk = f[i:j]
    if 'FGS' not in blk:
        lines = blk.split('\n')
        out = []
        for l in lines:
            if '<control type="image">' in l and '<visible>' in l:
                out.append(l.replace('</visible>', ' + !$EXP[FGS]</visible>', 1))
                if '$VAR[FG_FocusTex]' in l:
                    out.append(l.replace('$VAR[FG_FocusTex]', 'fg/fgs_bar.png').replace('border="16"', 'border="20"').replace('</visible>', ' + $EXP[FGS]</visible>', 1))
            else:
                out.append(l)
        blk = '\n'.join(out)
        f = f[:i] + blk + f[j:]
    wr('Includes_Fused.xml', f)
    print('settings pages written')


def previews():
    """skin_previews.py: the Skin style card names a fourth style"""
    p = os.path.join('_src', 'skin_previews.py')
    t = io.open(p, encoding='utf-8').read()
    a = "    for theme, name in (('glass', 32549), ('frost', 32547)):   # 0.56.27 Skin style: Glass is named Clear"
    b = "    for theme, name in (('glass', 32549), ('frost', 32547), ('system', 32402)):   # 0.56.27 Clear; 0.56.29 Fused Glass"
    if b not in t:
        assert t.count(a) == 1
        t = t.replace(a, b)
        a2 = "    fill = {'dark': ('d91a1d24', '85 %'), 'glass': ('c8171a20', '78 %'), 'frost': ('b31e2129', '70 %')}"
        assert t.count(a2) == 1
        t = t.replace(a2, "    fill = {'dark': ('d91a1d24', '85 %'), 'glass': ('c8171a20', '78 %'), 'frost': ('b31e2129', '70 %'), 'system': ('00000000', '')}")
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('previews: Fused Glass row')


if __name__ == '__main__':
    picture()
    strings()
    variables()
    cards()
    skin_settings()
    settings_pages()
    previews()
