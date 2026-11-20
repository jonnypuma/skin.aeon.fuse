"""0.39.8 Guide: a fast way through many channels. Left / Right move through time in the grid, so the scroll bar (60)
could not be reached. EPG tools (always one Back away) gets "Scroll through channels" (string 32440, all languages)
after "Choose channel group": it closes the card and focuses the scroll bar, where Up / Down page through the
channels; Left / Right / Back return to the grid. AG_Scrollbar takes an optional onback (default noop: Back does what
it did). Run from the skin folder."""
import io
import os
import re

TR = {'en_gb': '', 'cs_cz': 'Procházet kanály', 'da_dk': 'Rul gennem kanaler', 'de_de': 'Durch Sender blättern',
      'el_gr': 'Κύλιση στα κανάλια', 'es_es': 'Desplazarse por los canales', 'fi_fi': 'Selaa kanavia',
      'fr_fr': 'Faire défiler les chaînes', 'hu_hu': 'Csatornák görgetése', 'it_it': 'Scorri i canali',
      'ja_jp': 'チャンネルをスクロール', 'ko_kr': '채널 스크롤', 'nb_no': 'Bla gjennom kanaler',
      'nl_nl': 'Door zenders scrollen', 'pl_pl': 'Przewijaj kanały', 'pt_br': 'Rolar pelos canais',
      'pt_pt': 'Percorrer os canais', 'ru_ru': 'Прокрутка каналов', 'sv_se': 'Bläddra bland kanaler',
      'tr_tr': 'Kanallar arasında kaydır', 'uk_ua': 'Прокрутка каналів', 'zh_cn': '滚动浏览频道', 'zh_tw': '捲動瀏覽頻道'}
for d in sorted(os.listdir('language')):
    lang = d.replace('resource.language.', '')
    p = os.path.join('language', d, 'strings.po')
    t = io.open(p, encoding='utf-8').read()
    if 'msgctxt "#32440"' in t:
        continue
    t = t.rstrip('\n') + '\n\nmsgctxt "#32440"\nmsgid "Scroll through channels"\nmsgstr "%s"\n' % TR[lang]
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('strings: %d languages' % len(os.listdir('language')))

X = '1080i'


def rw(name, pairs):
    p = os.path.join(X, name)
    s = io.open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (name, old[:70])
        s = s.replace(old, new)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


rw('Includes_Dialogs.xml', [
    ('''	<include name="AG_Scrollbar">
		<param name="onleft">noop</param>
		<param name="onright">noop</param>''', '''	<include name="AG_Scrollbar">
		<param name="onleft">noop</param>
		<param name="onright">noop</param>
		<param name="onback">noop</param>'''),
    ('''				<onright>$PARAM[onright]</onright>
				<orientation>vertical</orientation>''', '''				<onright>$PARAM[onright]</onright>
				<onback>$PARAM[onback]</onback>
				<orientation>vertical</orientation>''')])

p = os.path.join(X, 'MyPVRGuide.xml')
s = io.open(p, encoding='utf-8').read()
n = s.count('''			<param name="onleft" value="50"/>
			<param name="onright" value="50"/>''')
assert n == 2, n
s = s.replace('''			<param name="onleft" value="50"/>
			<param name="onright" value="50"/>''', '''			<param name="onleft" value="50"/>
			<param name="onright" value="50"/>
			<param name="onback" value="50"/>''')
io.open(p, 'w', encoding='utf-8', newline='').write(s)

p = os.path.join(X, 'DialogPVRGuideControls.xml')
s = io.open(p, encoding='utf-8').read()
a = s.index('<control type="button" id="9703">')
b = s.index('</control>', a) + len('</control>')
blk = s[a:b]
assert blk.count('<ondown>9704</ondown>') == 1
s = s[:a] + blk.replace('<ondown>9704</ondown>', '<ondown>9711</ondown>') + s[b:]
ind = s[s.rindex('\n', 0, a) + 1:a]
row = ('''<control type="button" id="9711">
%(i)s	<!-- 0.39.8: the scroll bar, for a fast way through many channels (Up / Down page; Left / Right / Back: the grid) -->
%(i)s	<include>FG_EpgToolRow</include>
%(i)s	<label>$ADDON[skin.aeon.fuse 32440]</label>
%(i)s	<font>ui_24_semibold</font>
%(i)s	<textcolor>99ffffff</textcolor>
%(i)s	<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>
%(i)s	<aligny>center</aligny>
%(i)s	<include>Aeon_TexRowFocus</include>
%(i)s	<onclick>Dialog.Close(pvrguidecontrols,true)</onclick>
%(i)s	<onclick>SetFocus(60)</onclick>
%(i)s	<onup>9703</onup>
%(i)s	<ondown>9704</ondown>
%(i)s	<onleft>noop</onleft>
%(i)s	<onright>noop</onright>
%(i)s</control>
%(i)s''') % {'i': ind}
b = s.index('</control>', s.index('<control type="button" id="9703">')) + len('</control>')
nl = s.index('\n', b) + 1
s = s[:nl] + ind + row.rstrip('\t') + s[nl:] if False else s[:nl] + ind + row[:-len(ind)] + s[nl:]
a4 = s.index('<control type="button" id="9704">')
b4 = s.index('</control>', a4)
blk4 = s[a4:b4]
assert blk4.count('<onup>9703</onup>') == 1
s = s[:a4] + blk4.replace('<onup>9703</onup>', '<onup>9711</onup>') + s[b4:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
