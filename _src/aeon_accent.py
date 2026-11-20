# -*- coding: utf-8 -*-
"""0.55.3 Aeon accent colour: Skin settings > Appearance row 9760 (Skin.String(aeon.boxaccent): '' gold, slate, teal,
moss), variable Aeon_BoxAccent in Includes_Aeon_Glass.xml, ms_menus.py draws its boxes with it, strings 32594-32598 in
every language. It applies with the Aeon palette only; other palettes keep their own aeon_box.
Run once from the skin folder, then run _src/ms_menus.py."""
import io
import os
import re
import xml.dom.minidom as md

# 1 generator
p = '_src/ms_menus.py'
t = io.open(p, encoding='utf-8').read()
assert 'Aeon_BoxAccent' not in t
n1 = t.count("'aeon_box'")
t = t.replace("'aeon_box'", 'BOX')
t = t.replace('colordiffuse="aeon_box"', 'colordiffuse="$VAR[Aeon_BoxAccent]"')
a = "CAP_ON_BOX = 'ccffffff'"
assert a in t
t = t.replace(a, "BOX = '$VAR[Aeon_BoxAccent]'  # the palette's box colour; with the Aeon palette the chosen Aeon accent (0.55.3)\n" + a, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('generator uses', n1)

# 2 variables
p = '1080i/Includes_Aeon_Glass.xml'
t = io.open(p, encoding='utf-8').read()
n = len(re.findall(r'>aeon_box</value>', t))
t = t.replace('>aeon_box</value>', '>$VAR[Aeon_BoxAccent]</value>')
V = '''	<!-- 0.55.3 Aeon accent colour (Skin settings > Appearance, row 9760, Skin.String(aeon.boxaccent)): the colour of the
	     Aeon theme's title boxes, spines, pills and clock box. It applies with the Aeon palette (also for the menus when a
	     palette is set for the library only); every other palette keeps its own aeon_box. '' = gold. -->
	<expression name="Aeon_AccentOwn">!Skin.HasSetting(aeon.vglass) + [String.IsEqual(Skin.CurrentColourTheme,Aeon) | String.IsEqual(Skin.CurrentColourTheme,SKINDEFAULT) | String.IsEmpty(Skin.CurrentColourTheme) | String.Contains(Skin.CurrentColourTheme,library)]</expression>
	<variable name="Aeon_BoxAccent">
		<value condition="!$EXP[Aeon_AccentOwn]">aeon_box</value>
		<value condition="String.IsEqual(Skin.String(aeon.boxaccent),slate)">ff46566b</value>
		<value condition="String.IsEqual(Skin.String(aeon.boxaccent),teal)">ff2f5f66</value>
		<value condition="String.IsEqual(Skin.String(aeon.boxaccent),moss)">ff566640</value>
		<value>ff8a6d2f</value>
	</variable>
	<variable name="Aeon_BoxAccentName">
		<value condition="String.IsEqual(Skin.String(aeon.boxaccent),slate)">$ADDON[skin.aeon.fuse 32596]</value>
		<value condition="String.IsEqual(Skin.String(aeon.boxaccent),teal)">$ADDON[skin.aeon.fuse 32597]</value>
		<value condition="String.IsEqual(Skin.String(aeon.boxaccent),moss)">$ADDON[skin.aeon.fuse 32598]</value>
		<value>$ADDON[skin.aeon.fuse 32595]</value>
	</variable>
'''
a = '	<variable name="Aeon_SpinBox">'
assert t.count(a) == 1
t = t.replace(a, V + a)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('variable values', n)

# 3 settings row: a copy of the Palette row 9740 in the slot of the Fused-only row 9749 (y 821)
p = '1080i/SkinSettings.xml'
s = io.open(p, encoding='utf-8').read()
assert '9760' not in s
st = s.index('<param name="id" value="9740"/>')
gs = s.rindex('<control type="group">', 0, st)
end = '\n\t\t\t</control>\n'
ge = s.index(end, st) + len(end)
row = s[gs:ge]
r = row.replace('9740', '9760').replace('<top>331</top>', '<top>821</top>')
a = '<visible>!Skin.HasSetting(aeon.vglass)</visible>'
assert a in r
r = r.replace(a, '<visible>$EXP[Aeon_AccentOwn]</visible>')
r = r.replace('$LOCALIZE[31050]', '$ADDON[skin.aeon.fuse 32594]').replace('$VAR[Aeon_PaletteName]', '$VAR[Aeon_BoxAccentName]')
r = r.replace('<onup>9748</onup>', '<onup>9747</onup>').replace('<ondown>9741</ondown>', '<ondown>9744</ondown>')
a = '<onclick>RunScript(script.aeon.helper,palette)</onclick>'
assert a in r
r = r.replace(a, '<onclick condition="String.IsEmpty(Skin.String(aeon.boxaccent))">Skin.SetString(aeon.boxaccent,slate)</onclick>'
              '<onclick condition="String.IsEqual(Skin.String(aeon.boxaccent),slate)">Skin.SetString(aeon.boxaccent,teal)</onclick>'
              '<onclick condition="String.IsEqual(Skin.String(aeon.boxaccent),teal)">Skin.SetString(aeon.boxaccent,moss)</onclick>'
              '<onclick condition="String.IsEqual(Skin.String(aeon.boxaccent),moss)">Skin.Reset(aeon.boxaccent)</onclick>')
i = r.index('<control type="image"><left>666</left>')
j = r.rindex('</control>')
r = (r[:i] + '<control type="image"><left>826</left><top>18</top><width>34</width><height>34</height><texture colordiffuse="$VAR[Aeon_BoxAccent]">common/white.png</texture></control>\n'
     '\t\t\t\t<control type="image"><left>826</left><top>18</top><width>34</width><height>34</height><texture border="8" colordiffuse="66808080">$VAR[Aeon_MenuTexOutline]</texture></control>\n\t\t\t' + r[j:])
r = r.replace('<left>300</left><top>0</top><width>356</width>', '<left>300</left><top>0</top><width>510</width>')
r = r.replace('<!-- name of the palette in use and its five tones: highlight, boxes, page, cells, panels -->',
              '<!-- 0.55.3 Aeon accent colour: OK steps Gold, Slate, Teal, Moss; the name and its swatch -->')
s = s[:ge] + '\t\t\t' + r + s[ge:]
a = '<ondown condition="!$EXP[Aeon_FGlass]">9744</ondown>'
assert s.count(a) == 1
s = s.replace(a, '<ondown condition="!$EXP[Aeon_FGlass] + !$EXP[Aeon_AccentOwn]">9744</ondown><ondown condition="!$EXP[Aeon_FGlass] + $EXP[Aeon_AccentOwn]">9760</ondown>')
a = '<onup condition="!$EXP[Aeon_FGlass]">9747</onup>'
assert s.count(a) == 1
s = s.replace(a, '<onup condition="!$EXP[Aeon_FGlass] + !$EXP[Aeon_AccentOwn]">9747</onup><onup condition="!$EXP[Aeon_FGlass] + $EXP[Aeon_AccentOwn]">9760</onup>')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
md.parse(p)
md.parse('1080i/Includes_Aeon_Glass.xml')

# 4 strings
EN = ['Aeon accent colour', 'Gold', 'Slate', 'Teal', 'Moss']
TR = {
    'cs_cz': ['Barva akcentu Aeon', 'Zlatá', 'Břidlicová', 'Modrozelená', 'Mechová'],
    'da_dk': ['Aeon-accentfarve', 'Guld', 'Skifer', 'Blågrøn', 'Mos'],
    'de_de': ['Aeon-Akzentfarbe', 'Gold', 'Schiefer', 'Petrol', 'Moos'],
    'el_gr': ['Χρώμα έμφασης Aeon', 'Χρυσό', 'Σχιστόλιθος', 'Πετρόλ', 'Βρύο'],
    'es_es': ['Color de acento de Aeon', 'Oro', 'Pizarra', 'Verde azulado', 'Musgo'],
    'fi_fi': ['Aeonin korostusväri', 'Kulta', 'Liuske', 'Sinivihreä', 'Sammal'],
    'fr_fr': ["Couleur d'accent Aeon", 'Or', 'Ardoise', 'Bleu canard', 'Mousse'],
    'hu_hu': ['Aeon kiemelőszín', 'Arany', 'Palaszürke', 'Kékeszöld', 'Moha'],
    'it_it': ['Colore di accento Aeon', 'Oro', 'Ardesia', 'Ottanio', 'Muschio'],
    'ja_jp': ['Aeon のアクセントカラー', 'ゴールド', 'スレート', 'ティール', 'モス'],
    'ko_kr': ['Aeon 강조 색', '골드', '슬레이트', '틸', '모스'],
    'nb_no': ['Aeon-aksentfarge', 'Gull', 'Skifer', 'Blågrønn', 'Mose'],
    'nl_nl': ['Aeon-accentkleur', 'Goud', 'Leisteen', 'Groenblauw', 'Mos'],
    'pl_pl': ['Kolor akcentu Aeon', 'Złoty', 'Łupkowy', 'Morski', 'Mech'],
    'pt_br': ['Cor de destaque do Aeon', 'Ouro', 'Ardósia', 'Verde-azulado', 'Musgo'],
    'pt_pt': ['Cor de destaque do Aeon', 'Ouro', 'Ardósia', 'Verde-azulado', 'Musgo'],
    'ru_ru': ['Акцентный цвет Aeon', 'Золото', 'Сланец', 'Сине-зелёный', 'Мох'],
    'sv_se': ['Aeon-accentfärg', 'Guld', 'Skiffer', 'Blågrön', 'Mossa'],
    'tr_tr': ['Aeon vurgu rengi', 'Altın', 'Arduvaz', 'Camgöbeği', 'Yosun'],
    'uk_ua': ['Акцентний колір Aeon', 'Золото', 'Сланець', 'Синьо-зелений', 'Мох'],
    'zh_cn': ['Aeon 强调色', '金色', '石板灰', '青绿', '苔绿'],
    'zh_tw': ['Aeon 強調色', '金色', '石板灰', '藍綠', '苔綠'],
}
assert len(TR) == 22
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    q = os.path.join('language', d, 'strings.po')
    t = io.open(q, encoding='utf-8').read()
    assert '#32594"' not in t
    for k, en in enumerate(EN):
        t = t.rstrip('\n') + '\n\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (32594 + k, en, '' if lang == 'en_gb' else TR[lang][k])
    io.open(q, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
