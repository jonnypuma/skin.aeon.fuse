# -*- coding: utf-8 -*-
"""0.56.40 Setup wizard (dialog 1173) rebuilt (the user, 2026-11-17: "just build the wizard as you have suggested").

The wizard is drawn like Skin settings in whatever theme and style run now: the same window chrome, a column of steps
where Skin settings has its categories, and pages of rows copied from Skin settings (same ids, so the same preview cards,
help texts, pickers, toggles and dimming). What it changes:
- Skin theme first (Fused Glass, Aeon, Aeon Glass) with a picture of each theme's Home; the pages that follow show the
  rows of the CHOSEN theme (window property aeon.wiz.theme), not of the running one. Theme, Skin style (aeon.menutheme /
  aeon.fgmenu), palette and fonts wait for Finish (properties aeon.wiz.*): they need the skin loaded again, and a reload
  leaves skin settings misread, so Finish applies them and restarts Kodi (Linux). All other rows change at once.
- Start: Use the defaults (the chosen theme's look, then Finish at once), Customise, Keep my current settings (a re-run).
- Look (Skin style, Menu background, Panel shadow, Focus highlight, Navigation animation, Toast pill / Palette, Aeon
  accent colour / Font combination), Libraries (Aeon, Aeon Glass: corner boxes, side strip, settings strip, library
  options), Home (position, focused name only, underline, Now playing, vignette, vignette shape), Backgrounds (fanart
  backdrop, strength, library background, fanart look), Home menu items (switches; Live TV only with a PVR add-on),
  Add-ons (install the optional ones), All set (Finish, a summary, the credits).
- Step counter in the title band, Next row at the end of every page, Left = the steps, Back = the step, then the step
  before; Back on the first step closes the wizard (and counts it as done).
The helper (script.aeon.helper 0.3.107) opens it (wizard,open), picks palettes (wizard,palette), fonts (fonts,wizard),
applies defaults (wizard,defaults[,finish]) and finishes (wizard). Expert settings stay out of the wizard.
PARKED (the user, 2026-11-17: "don't discard what you have just spent an hour on. keep it for now. then bring back the
old wizard"): by default it writes into _src/wizard_settings_look/ and takes its help block out of Dlg_SkinHelp, so the
skin keeps the classic wizard (_src/wizard_05640.py). `python _src/wizard_settingslook_05640.py --install` puts this one
in 1080i instead (it copies the final rows, previews and help texts, so run it last). Box shots:
skin.glass/mockups/setup-wizard/box05640."""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from appearance_order_05633 import children, row_id, own_visible, set_visible, head_end, ctl_end  # noqa: E402

D = os.path.join(HERE, '..', '1080i')
DATA = json.load(io.open(os.path.join(HERE, 'wizard_data.json'), encoding='utf-8'))


INSTALL = '--install' in sys.argv
OUT_DIR = D if INSTALL else os.path.join(HERE, 'wizard_settings_look')


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    """the wizard's own files go to OUT_DIR; Includes_Settings.xml (the help block) stays in 1080i"""
    folder = D if name == 'Includes_Settings.xml' else OUT_DIR
    io.open(os.path.join(folder, name), 'w', encoding='utf-8', newline='\n').write(text)


def A(n):
    return '$ADDON[skin.aeon.fuse %d]' % n


def L(n):
    return '$LOCALIZE[%d]' % n


def P(name):
    return 'Window(Home).Property(aeon.wiz.%s)' % name


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


SS = rd('SkinSettings.xml')
FG, GL, AE = '$EXP[Wiz_FG]', '$EXP[Wiz_GL]', '$EXP[Wiz_AE]'
NOTFG = '!$EXP[Wiz_FG]'
DONE = 'Skin.HasSetting(aeon.wizard.done)'

# ------------------------------------------------------------------------------------------------- new strings (32694+)
S_FG_HELP = 32694          # Fused Glass: what it is
S_DEFAULTS, S_DEFAULTS_HELP = 32695, 32696
S_CUSTOM, S_CUSTOM_HELP = 32697, 32698
S_KEEP, S_KEEP_HELP = 32699, 32700
S_GLASS_HELP = 32701       # Aeon Glass: what it is
S_ADDONS = {               # what each optional add-on adds
    'plugin.video.themoviedb.helper': 32702,
    'script.embuary.helper': 32703,
    'script.cu.lrclyrics': 32704,
    'script.artistslideshow': 32705,
    'script.karmamole.helper': 32706,
    'service.skippy': 32707,
    'service.trickplay': 32708,
    'resource.images.studios.white': 32709,
    'resource.images.recordlabels.white': 32710,
    'resource.images.languageflags.colour': 32711,
    'screensaver.aeon.fuse': 32712,
}

# --------------------------------------------------------------------------------------------------------- the pages
# key, step button id, name, icon, page grouplist id, scroll bar id, visible (None = always)
PAGES = [
    ('theme', 9600, A(32249), 'aeon/icons/sun.png', 9870, 9880, None),
    ('start', 9551, A(32035), 'aeon/icons/play.png', 9871, 9881, None),
    ('look', 9566, L(31726), 'aeon/icons/sparkle.png', 9872, 9882, None),
    ('library', 9567, A(32244), 'aeon/icons/film.png', 9873, 9883, NOTFG),
    ('home', 9552, L(31019), 'aeon/icons/home.png', 9874, 9884, None),
    ('backdrop', 9568, L(31729), 'aeon/icons/image.png', 9875, 9885, None),
    ('items', 9569, A(32251), 'aeon/icons/lines.png', 9876, 9886, None),
    ('addons', 9601, L(24001), 'aeon/icons/layers.png', 9877, 9887, None),
    ('done', 9553, A(32257), 'aeon/icons/check.png', 9878, 9888, None),
]
KEYS = [p[0] for p in PAGES]
STEP = dict((p[0], p[1]) for p in PAGES)

# rows copied from Skin settings: page -> [(row id, visible in the wizard or None)]
COPIED = {
    'look': [(9748, None),
             (9798, FG + ' + String.IsEqual(%s,system)' % P('fgmenu')),
             (9529, FG), (9749, FG), (9759, FG), (9528, FG),
             (9740, AE),
             (9760, '$EXP[Wiz_AccentOwn]'),
             (9542, None)],
    'library': [(9747, None), (9524, None), (9525, None), (9547, '$EXP[Wiz_MS]')],
    'home': [(9746, None), (9546, None), (9766, NOTFG), (9743, NOTFG), (9733, None), (9765, None)],
    'backdrop': [(9741, None), (9742, None), (9745, None), (9767, 'String.IsEqual(Skin.String(aeon.vbg),fanart)')],
}
# the wizard's own rows
NEXT_ID = dict((k, 9420 + i) for i, k in enumerate(KEYS))          # Next row of each page
ADDONS = [  # id, name, shown when
    ('plugin.video.themoviedb.helper', 'TMDb Helper', None),
    ('script.embuary.helper', 'Embuary Helper', None),
    ('script.cu.lrclyrics', 'CU LRC Lyrics', None),
    ('script.artistslideshow', 'Artist Slideshow', None),
    ('script.karmamole.helper', 'KarmaMole Skin Helper', None),
    ('resource.images.studios.white', 'Studio Icons - White', None),
    ('resource.images.recordlabels.white', 'Recordlabel Icons - White', None),
    ('resource.images.languageflags.colour', 'Language Flags Colour', None),
    ('screensaver.aeon.fuse', 'Aeon Fuse Screensaver', 'System.HasAddon(repository.skippyrepo) | System.HasAddon(screensaver.aeon.fuse)'),
    ('service.skippy', 'Skippy - Video Segment Skipper', 'System.HasAddon(repository.skippyrepo) | System.HasAddon(service.skippy)'),
    ('service.trickplay', 'Trickplay Preview', 'System.HasAddon(repository.skippyrepo) | System.HasAddon(service.trickplay)'),
]

# theme atoms of the running skin -> the theme / style chosen in the wizard (rows' values and previews only; the
# window's own chrome stays in the running theme)
REWRITE = [
    ('Skin.HasSetting(aeon.fglass)', FG),
    ('Skin.HasSetting(aeon.vglass)', '$EXP[Wiz_Glassy]'),
    ('$EXP[Aeon_FGlass]', FG),
    ('$EXP[Aeon_VGlass]', '$EXP[Wiz_Glassy]'),
    ('$EXP[Aeon_MS_mosaic]', '$EXP[Wiz_MS_mosaic]'),
    ('$EXP[Aeon_MS_ledger]', '$EXP[Wiz_MS_ledger]'),
    ('$EXP[Aeon_MS_bridge]', '$EXP[Wiz_MS_bridge]'),
    ('$EXP[Aeon_MS_tabslab]', '$EXP[Wiz_MS_tabslab]'),
    ('$EXP[Aeon_MS]', '$EXP[Wiz_MS]'),
    ('$EXP[Aeon_Fused]', '$EXP[Wiz_Fused]'),
    ('$EXP[Aeon_AccentOwn]', '$EXP[Wiz_AccentOwn]'),
    ('Skin.String(aeon.menutheme)', P('menutheme')),
    ('Skin.String(aeon.fgmenu)', P('fgmenu')),
]


def rewrite(x, previews=False):
    for a, b in REWRITE:
        x = x.replace(a, b)
    if previews:
        x = x.replace('$EXP[FGS]', '$EXP[Wiz_FGS]')
    return x


# ------------------------------------------------------------------------------------------------- rows from Skin settings
def grab_rows():
    rows = {}
    for gid in ('9770', '9772'):
        g = SS.index('<control type="grouplist" id="%s">' % gid)
        kids, _gend = children(SS, g)
        for s, e in kids:
            b = SS[s:e]
            r = row_id(b)
            if r:
                rows[r] = b.strip('\n')
    return rows


ROWS = grab_rows()
TEMPLATE = ROWS[9546]


def focus_group(rid):
    s = TEMPLATE.index('<control type="group"><left>41</left>')
    e = ctl_end(TEMPLATE, s)
    return TEMPLATE[s:e].replace('Control.HasFocus(9546)', 'Control.HasFocus(%d)' % rid)


def fixed_row(rid):
    """a row of a page with fixed places (Backgrounds) as a grouplist row: its focus bar from the template, its own
    group without its place"""
    i = SS.index('<param name="id" value="%d"/>' % rid)
    s = SS.rfind('<control type="group">', 0, SS.rfind('<include content="Dlg_SkinRowChrome"', 0, i))
    e = ctl_end(SS, s)
    body = SS[s + len('<control type="group">'):e - len('</control>')]
    body = re.sub(r'^\s*<top>\d+</top>', '', body, count=1)
    return ('\t<control type="group"><!-- row %d -->\n\t\t<width>1100</width><height>70</height>\n%s\n'
            '<control type="group"><left>160</left><top>0</top>%s</control>\n\t</control>' % (rid, focus_group(rid), body))


def source_row(rid):
    return ROWS[rid] if rid in ROWS else fixed_row(rid)


def protect(b):
    """the row's focus bar and its name chrome stay in the running theme: keep them out of the rewrite"""
    keep = []
    s = b.index('<control type="group"><left>41</left>')
    e = ctl_end(b, s)
    keep.append(b[s:e])
    b = b[:s] + '@@KEEP0@@' + b[e:]
    m = re.search(r'<include content="Dlg_SkinRowChrome">.*?</include>', b, re.S)
    keep.append(m.group(0))
    b = b[:m.start()] + '@@KEEP1@@' + b[m.end():]
    return b, keep


def unprotect(b, keep):
    for n, k in enumerate(keep):
        b = b.replace('@@KEEP%d@@' % n, k)
    return b


def button_span(b, rid):
    s = b.index('<control type="button" id="%d">' % rid)
    return s, ctl_end(b, s)


def set_clicks(b, rid, clicks):
    s, e = button_span(b, rid)
    btn = b[s:e]
    btn = re.sub(r'\s*<onclick(?: condition="[^"]*")?>[^<]*</onclick>', '', btn)
    btn = btn[:-len('</control>')] + ''.join('\n\t\t\t\t\t' + c for c in clicks) + '\n\t\t\t\t</control>'
    return b[:s] + btn + b[e:]


def replace_value_area(b, rid, value):
    """everything after the row's button inside its content group -> value"""
    s, e = button_span(b, rid)
    # the content group ends with the row's last '</control>' before the row's own closing tag
    end = b.rstrip().rfind('</control>')                     # the row group
    end = b.rfind('</control>', 0, end)                      # the content group
    return b[:e] + '\n' + value + '\n\t\t\t' + b[end:]


def value_label(rid, label, left=300, width=560, col='$VAR[FGS_Dim99]'):
    return ('<control type="label"><left>%d</left><top>0</top><width>%d</width><height>70</height><align>right</align><aligny>center</aligny>'
            '<font>st_ui_22_bold</font><textcolor>%s</textcolor><label>%s</label><visible>!Control.HasFocus(%d)</visible></control>'
            '<control type="label"><left>%d</left><top>0</top><width>%d</width><height>70</height><align>right</align><aligny>center</aligny>'
            '<font>st_ui_22_bold</font><textcolor>$VAR[FGS_Aeon_OnBarInk]</textcolor><label>%s</label><visible>Control.HasFocus(%d)</visible></control>'
            % (left, width, col, label, rid, left, width, label, rid))


STYLE_CLICKS = [
    # Fused Glass: Dark -> Clear -> Frost -> Fused Glass -> Dark (skinstyle.ORDER)
    '<onclick condition="%s + String.IsEmpty(%s)">SetProperty(aeon.wiz.fgmenu,glass,home)</onclick>' % (FG, P('fgmenu')),
    '<onclick condition="%s + String.IsEqual(%s,glass)">SetProperty(aeon.wiz.fgmenu,frost,home)</onclick>' % (FG, P('fgmenu')),
    '<onclick condition="%s + String.IsEqual(%s,frost)">SetProperty(aeon.wiz.fgmenu,system,home)</onclick>' % (FG, P('fgmenu')),
    '<onclick condition="%s + String.IsEqual(%s,system)">ClearProperty(aeon.wiz.fgmenu,home)</onclick>' % (FG, P('fgmenu')),
    # Aeon: Mosaic -> Ledger -> Bridge ('') -> Tab slab -> Fuse -> Mosaic (the helper's menutheme order)
    '<onclick condition="%s + String.IsEqual(%s,mosaic)">SetProperty(aeon.wiz.menutheme,ledger,home)</onclick>' % (AE, P('menutheme')),
    '<onclick condition="%s + String.IsEqual(%s,ledger)">ClearProperty(aeon.wiz.menutheme,home)</onclick>' % (AE, P('menutheme')),
    '<onclick condition="%s + [String.IsEmpty(%s) | String.IsEqual(%s,bridge)]">SetProperty(aeon.wiz.menutheme,tabslab,home)</onclick>' % (AE, P('menutheme'), P('menutheme')),
    '<onclick condition="%s + String.IsEqual(%s,tabslab)">SetProperty(aeon.wiz.menutheme,fused,home)</onclick>' % (AE, P('menutheme')),
    '<onclick condition="%s + String.IsEqual(%s,fused)">SetProperty(aeon.wiz.menutheme,mosaic,home)</onclick>' % (AE, P('menutheme')),
    # Aeon Glass: its own menus <-> Fuse
    '<onclick condition="%s + String.IsEqual(%s,fused)">ClearProperty(aeon.wiz.menutheme,home)</onclick>' % (GL, P('menutheme')),
    '<onclick condition="%s + !String.IsEqual(%s,fused)">SetProperty(aeon.wiz.menutheme,fused,home)</onclick>' % (GL, P('menutheme')),
]


def wizard_row(rid, vis):
    b = source_row(rid)
    # the row's own visibility: the wizard's
    if vis:
        b = set_visible(b, vis)
    elif own_visible(b) is not None:
        he = head_end(b)
        b = re.sub(r'\s*<visible>[^<]*</visible>', '', b[:he], count=1) + b[he:]
    b, keep = protect(b)
    b = re.sub(r'<on(?:up|down)(?: condition="[^"]*")?>[^<]*</on(?:up|down)>', '', b)
    b = re.sub(r'<onback>\d+</onback>', '@@BACK@@', b)
    b = re.sub(r'<onleft>SetFocus\(\d+\)</onleft>', '@@LEFT@@', b)
    b = rewrite(b)
    b = unprotect(b, keep)
    if rid == 9748:
        b = set_clicks(b, rid, STYLE_CLICKS)
    elif rid == 9740:
        b = set_clicks(b, rid, ['<onclick>RunScript(script.aeon.helper,wizard,palette)</onclick>'])
        b = replace_value_area(b, rid, value_label(rid, '$VAR[Wiz_PaletteName]', 300, 510, 'ffffffff') +
                               '<control type="image"><left>826</left><top>18</top><width>34</width><height>34</height><texture colordiffuse="$VAR[Wiz_PalSwatch]">common/white.png</texture></control>'
                               '<control type="image"><left>826</left><top>18</top><width>34</width><height>34</height><texture border="8" colordiffuse="66808080">$VAR[Aeon_MenuTexOutline]</texture></control>')
    elif rid == 9542:
        b = set_clicks(b, rid, ['<onclick>RunScript(script.aeon.helper,fonts,wizard)</onclick>'])
        b = replace_value_area(b, rid, value_label(rid, '$INFO[%s]' % P('font'), 240, 620))
    return b


# ------------------------------------------------------------------------------------------------- the wizard's own rows
def chrome(rid, label, icon, namew=560):
    return ('<include content="Dlg_SkinRowChrome"><param name="namefgs" value="%d"/>\n\t\t\t\t\t<param name="id" value="%d"/>'
            '<param name="namew" value="%d"/><param name="label" value="%s"/><param name="hint" value=""/><param name="labelTop" value="0"/>'
            '<param name="labelH" value="70"/><param name="icon" value="%s"/><param name="labelx" value="46"/>\n\t\t\t\t</include>'
            % (namew + 101, rid, namew, label, icon))


def own_row(rid, label, icon, clicks, value='', vis=None, namew=560):
    return ('\t<control type="group"><!-- row %d -->\n\t\t<width>1100</width><height>70</height>\n%s%s\n'
            '<control type="group"><left>160</left><top>0</top>\n\t\t\t\t%s\n'
            '\t\t\t\t<control type="button" id="%d">\n\t\t\t\t\t<include>Dlg_SkinRowButton</include>\n\t\t\t\t\t@@BACK@@\n\t\t\t\t\t@@LEFT@@\n%s\n\t\t\t\t</control>\n%s\n\t\t\t</control>\n\t</control>'
            % (rid, '\t\t<visible>%s</visible>\n' % vis if vis else '', focus_group(rid), chrome(rid, label, icon, namew), rid,
               ''.join('\t\t\t\t\t%s\n' % c for c in clicks), value))


def toggle_value(rid, cond):
    s = TEMPLATE.index('<control type="button" id="9546">')
    s = ctl_end(TEMPLATE, s)
    end = TEMPLATE.rstrip().rfind('</control>')
    end = TEMPLATE.rfind('</control>', 0, end)
    v = TEMPLATE[s:end]
    return v.replace('Skin.HasSetting(aeon.hm.icons)', cond).replace('9546', str(rid))


def check_value(rid, cond):
    return ('<control type="image"><left>828</left><top>19</top><width>32</width><height>32</height><texture colordiffuse="$VAR[FGS_ToggleOn]">aeon/icons/check.png</texture>'
            '<visible>[%s] + !Control.HasFocus(%d)</visible></control>'
            '<control type="image"><left>828</left><top>19</top><width>32</width><height>32</height><texture colordiffuse="$VAR[FGS_Aeon_OnBarIcon]">aeon/icons/check.png</texture>'
            '<visible>[%s] + Control.HasFocus(%d)</visible></control>' % (cond, rid, cond, rid))


def go(page, first):
    """onclick actions: open a page and focus its first row (the pages allow hidden focus)"""
    return ['<onclick>SetProperty(aeon.wiz.page,%s,home)</onclick>' % page, '<onclick>SetFocus(%d)</onclick>' % first]


THEMES = [('fused', 9401, A(32402), A(S_FG_HELP)), ('aeon', 9402, L(31678), A(32049)), ('glass', 9403, L(31679), A(S_GLASS_HELP))]
THEME_ICON = {'fused': 'aeon/icons/blur.png', 'aeon': 'aeon/icons/grid.png', 'glass': 'aeon/icons/drop.png'}
# Home menu items: "on" = the item is on the menu and not hidden (the condition of Aeon_WizMenu_<key>, kept from the old
# wizard in Includes_Aeon_Wizard.xml; a condition cannot hold a $VAR)
OLD_INC = io.open(os.path.join(OUT_DIR, 'Includes_Aeon_Wizard.xml'), encoding='utf-8').read()
MENU_VARS = re.findall(r'\t<variable name="Aeon_WizMenu_\w+">.*?</variable>', OLD_INC, re.S)
MENU_ON = dict((re.search(r'name="Aeon_WizMenu_(\w+)"', v).group(1),
                re.search(r'<value condition="([^"]*)">on</value>', v).group(1).replace('&amp;', '&')) for v in MENU_VARS)


def first_row(page):
    return {'theme': 9401, 'start': 9411, 'look': 9748, 'library': 9747, 'home': 9746, 'backdrop': 9741,
            'items': 9431, 'addons': 9451, 'done': 9409}[page]


def next_page(page):
    """the page after this one for the chosen theme: (condition, page) pairs"""
    i = KEYS.index(page)
    nxt = KEYS[i + 1]
    if nxt == 'library':
        return [(NOTFG, 'library'), (FG, 'home')]
    return [(None, nxt)]


def next_clicks(page):
    out = []
    for cond, nxt in next_page(page):
        c = ' condition="%s"' % cond if cond else ''
        out.append('<onclick%s>SetProperty(aeon.wiz.page,%s,home)</onclick>' % (c, nxt))
        out.append('<onclick%s>SetFocus(%d)</onclick>' % (c, first_row(nxt)))
    return out


def own_rows(page):
    """[(id, visible, xml)]"""
    out = []
    if page == 'theme':
        for key, rid, name, _help in THEMES:
            clicks = ['<onclick>SetProperty(aeon.wiz.theme,%s,home)</onclick>' % key] + go('start', 9411)
            out.append((rid, None, own_row(rid, name, THEME_ICON[key], clicks,
                                           check_value(rid, 'String.IsEqual(%s,%s)' % (P('theme'), key)))))
        out.append((9404, None, own_row(9404, A(32038), 'aeon/icons/back.png',
                                        ['<onclick>Skin.SetBool(aeon.wizard.done)</onclick>', '<onclick>Dialog.Close(1173)</onclick>'])))
    elif page == 'start':
        out.append((9411, None, own_row(9411, A(S_DEFAULTS), 'aeon/icons/star.png',
                                        ['<onclick>RunScript(script.aeon.helper,wizard,defaults,finish)</onclick>'])))
        out.append((9412, None, own_row(9412, A(S_CUSTOM), 'aeon/icons/settings.png',
                                        ['<onclick condition="!%s">RunScript(script.aeon.helper,wizard,defaults)</onclick>' % DONE] + go('look', 9748))))
        out.append((9413, DONE, own_row(9413, A(S_KEEP), 'aeon/icons/check.png', go('done', 9409), vis=DONE)))
    elif page == 'items':
        for n, item in enumerate(DATA['menu']):
            m = re.match(r'\$VAR\[Aeon_Name_(\w+)\]$', item['label'])
            if not m:
                continue                                # the old wizard's Next item
            key = m.group(1)
            rid = 9431 + n
            vis = 'System.HasPVRAddon' if key == 'livetv' else None
            out.append((rid, vis, own_row(rid, item['label'], 'aeon/icons/lines.png',
                                          ['<onclick>RunScript(script.aeon.helper,wizard,menu,%s)</onclick>' % key],
                                          toggle_value(rid, '$EXP[Wiz_MenuOn_%s]' % key), vis=vis)))
    elif page == 'addons':
        for n, (aid, name, vis) in enumerate(ADDONS):
            rid = 9451 + n
            have = 'System.HasAddon(%s)' % aid
            value = (value_label(rid, L(35257), 300, 560, '$VAR[FGS_OnText]').replace('<visible>', '<visible>%s + ' % have) +
                     value_label(rid, L(24038), 300, 560).replace('<visible>', '<visible>!%s + ' % have))
            out.append((rid, vis, own_row(rid, name, 'aeon/icons/layers.png',
                                          ['<onclick condition="!%s">InstallAddon(%s)</onclick>' % (have, aid)], value, vis=vis)))
    elif page == 'done':
        out.append((9409, None, own_row(9409, A(32142), 'aeon/icons/check.png',
                                        ['<onclick>RunScript(script.aeon.helper,wizard)</onclick>'],
                                        value_label(9409, '$VAR[Wiz_FinishHint]', 240, 620))))
    if page not in ('theme', 'start', 'done'):
        nid = NEXT_ID[page]
        out.append((nid, None, own_row(nid, L(209), 'aeon/icons/chevron_right.png', next_clicks(page),
                                       value_label(nid, '$VAR[Wiz_NextName_%s]' % page, 240, 620))))
    return out


# ------------------------------------------------------------------------------------------------- previews
def preview_inner(rid):
    """the Skin settings preview of a row (Control.HasFocus group), rewritten for the chosen theme"""
    tag = '<!-- preview:%d -->' % rid
    if tag not in SS:
        return None
    s = SS.index('<control type="group">', SS.index(tag))
    e = ctl_end(SS, s)
    inner = SS[s:e]
    inner = inner[inner.index('</visible>') + len('</visible>'):-len('</control>')]
    return rewrite(inner, previews=True)


def cap(text):
    return ('<control type="label"><left>16</left><top>54</top><width>248</width><height>30</height><align>left</align><aligny>center</aligny>'
            '<font>st_cap_20</font><textcolor>66ffffff</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>' % text)


def picture(tex):
    return ('<control type="image"><left>16</left><top>96</top><width>248</width><height>140</height><aspectratio>scale</aspectratio>'
            '<texture background="true">%s</texture></control>'
            '<control type="image"><left>16</left><top>96</top><width>248</width><height>140</height><texture border="14" colordiffuse="33ffffff">fg/e28.png</texture></control>' % tex)


def textbox(text, top=248, height=520):
    return ('<control type="textbox"><left>16</left><top>%d</top><width>248</width><height>%d</height><font>st_small_20</font>'
            '<textcolor>a0ffffff</textcolor><label>%s</label></control>' % (top, height, text))


def facts(rows, top=96):
    """the summary: small capitals and the value under them"""
    out = []
    y = top
    for label, value, vis in rows:
        v = '<visible>%s</visible>' % vis if vis else ''
        out.append('<control type="group"><top>%d</top>%s'
                   '<control type="label"><left>16</left><top>0</top><width>248</width><height>24</height><font>st_cap_14</font><textcolor>66ffffff</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>'
                   '<control type="label"><left>16</left><top>22</top><width>248</width><height>32</height><font>st_ui_22_bold</font><textcolor>eeffffff</textcolor><label>%s</label></control></control>'
                   % (y, v, label, value))
        y += 62
    return ''.join(out), y


CREDITS = ('djh_  ·  jurialmunkey  ·  jamal2362  ·  KarmaMole  ·  %s' % A(32146))


def own_previews(page):
    out = []
    if page == 'theme':
        for key, rid, name, help_ in THEMES:
            out.append((rid, cap(name) + picture('aeon/wizard/theme_%s.jpg' % key) + textbox(help_)))
    elif page == 'done':
        f, y = facts([(A(32249), '$VAR[Wiz_ThemeName]', None),
                      (A(32250), '$VAR[Wiz_StyleName]', None),
                      (L(31050), '$VAR[Wiz_PaletteName]', AE),
                      (A(32423), '$INFO[%s]' % P('font'), '!String.IsEmpty(%s)' % P('font'))])
        out.append((9409, cap(A(32257)) + f + textbox(A(32145) + ': ' + CREDITS, y + 10, 300)))
    elif page == 'addons':
        for n, (aid, name, _vis) in enumerate(ADDONS):
            rid = 9451 + n
            out.append((rid, cap(name) +
                        '<control type="image"><left>76</left><top>96</top><width>128</width><height>128</height><aspectratio>keep</aspectratio>'
                        '<texture background="true">$INFO[System.AddonIcon(%s)]</texture><visible>System.HasAddon(%s)</visible></control>' % (aid, aid) +
                        textbox(A(S_ADDONS[aid]))))
    return out


def preview_card(page, rows):
    """skin_previews.container for the wizard's page"""
    if not rows:
        return ''
    cond = ' | '.join('Control.HasFocus(%d)' % r for r, _x in rows)
    o = ['<!-- PREVIEW CARD wizard %s -->' % page,
         '<control type="group"><left>920</left><top>199</top><width>280</width><height>470</height><visible>%s</visible>' % cond,
         '<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/>'
         '<effect type="slide" start="0,16" end="0,0" time="200" tween="cubic" easing="out"/></animation>',
         '<control type="group"><width>280</width><height>470</height><visible>!$EXP[Aeon_FGlass] + !$EXP[Aeon_MS]</visible><include content="Aeon_Glass"><param name="fgs" value="true"/></include></control>',
         '<control type="group"><left>12</left><top>-91</top><width>272</width><height>866</height><visible>$EXP[Aeon_FGlass]</visible><include content="Aeon_Glass"><param name="fgs" value="true"/></include></control>',
         '<control type="group"><animation effect="slide" start="0,0" end="8,-80" time="0" condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">Conditional</animation>'
         '<animation effect="slide" start="0,0" end="0,86" time="0" condition="$EXP[Aeon_MS_bridge]">Conditional</animation>',
         '<control type="label"><left>16</left><top>14</top><width>248</width><height>30</height><font>st_cap_20</font>'
         '<textcolor>$VAR[Aeon_Accent]</textcolor><label>$LOCALIZE[31681]</label></control>']
    for rid, inner in rows:
        o.append('<!-- preview:%d -->' % rid)
        o.append('<control type="group"><visible>Control.HasFocus(%d)</visible>%s</control>' % (rid, inner))
    o.append('</control></control>')
    o.append('<!-- /PREVIEW CARD wizard %s -->' % page)
    return '\n'.join(o)


# ------------------------------------------------------------------------------------------------- page assembly
def chain(tag, items):
    out = ''
    for rid, vis in items:
        out += '<%s condition="%s">%d</%s>' % (tag, vis, rid, tag) if vis else '<%s>%d</%s>' % (tag, rid, tag)
        if not vis:
            break
    return out


def page_rows(page):
    """[(id, visible, xml)] in page order"""
    out = [(rid, vis, wizard_row(rid, vis)) for rid, vis in COPIED.get(page, [])]
    return out + own_rows(page)


GL_OPEN = SS[SS.index('<control type="grouplist" id="9770">'):]
GL_OPEN = GL_OPEN[:GL_OPEN.index('<control type="group">')]
SB = SS[SS.index('<control type="scrollbar" id="9771">'):ctl_end(SS, SS.index('<control type="scrollbar" id="9771">'))]


def page_xml(page):
    _key, sid, _name, _icon, gid, sbid, _vis = PAGES[KEYS.index(page)]
    rows = page_rows(page)
    seq = [(rid, vis) for rid, vis, _x in rows]
    body = []
    for n, (rid, vis, x) in enumerate(rows):
        ups = list(reversed(seq[:n])) + list(reversed(seq[n + 1:]))
        downs = seq[n + 1:] + seq[:n]
        s, e = button_span(x, rid)
        btn = x[s:e].replace('<control type="button" id="%d">' % rid,
                             '<control type="button" id="%d">\n\t\t\t\t\t%s%s' % (rid, chain('onup', ups), chain('ondown', downs)), 1)
        x = x[:s] + btn + x[e:]
        x = x.replace('@@BACK@@', '<onback>%d</onback>' % sid).replace('@@LEFT@@', '<onleft>SetFocus(%d)</onleft>' % sid)
        body.append(x)
    previews = []
    for rid, _vis, _x in rows:
        inner = preview_inner(rid)
        if inner:
            previews.append((rid, inner))
    have = set(r for r, _x in previews)
    previews += [(r, x) for r, x in own_previews(page) if r not in have]
    gl = (GL_OPEN.replace('id="9770"', 'id="%d"' % gid).replace('<pagecontrol>9771</pagecontrol>', '<pagecontrol>%d</pagecontrol>' % sbid)
          .replace('<onleft>9600</onleft>', '<onleft>%d</onleft>' % sid))
    sb = SB.replace('id="9771"', 'id="%d"' % sbid).replace('<onleft>9770</onleft>', '<onleft>%d</onleft>' % gid)
    return ('\t\t<control type="group"><!-- wizard page %s -->\n\t\t\t<left>600</left>\n'
            '\t\t\t<animation effect="slide" start="0,0" end="20,0" time="0" condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">Conditional</animation>\n'
            '\t\t\t<visible allowhiddenfocus="true">String.IsEqual(Window(Home).Property(aeon.wiz.page),%s)</visible>\n'
            '%s\n\t\t\t<include>Aeon_PageIn</include>\n%s%s\n</control>\n%s\n\t\t</control>\n'
            % (page, page, preview_card(page, previews), gl, '\n'.join(body), sb))


# ------------------------------------------------------------------------------------------------- the window
def window_chrome():
    s = SS.index('<controls>') + len('<controls>')
    e = SS.index('<control type="group">\n\t\t\t<left>page_margin</left>')
    x = SS[s:e]
    x = x.replace('Window(Home).Property(aeon.skincat)', P('page'))
    x = x.replace('<include content="Aeon_MenuHeader"><param name="lead" value="Aeon Fuse"/><param name="label" value="$LOCALIZE[5]"/></include>',
                  '<include content="Aeon_MenuHeader"><param name="lead" value="Aeon Fuse"/><param name="label" value="%s"/></include>' % A(32361))
    assert A(32361) in x
    x = x.replace('[UPPERCASE]$LOCALIZE[31847][/UPPERCASE]', '[UPPERCASE]%s[/UPPERCASE]' % A(32243))
    m = re.search(r'<control type="label"><left>600</left>[^\n]*\$VAR\[Aeon_SkinCatName\][^\n]*</control>', x)
    title = m.group(0)
    new = title.replace('$VAR[Aeon_SkinCatName]', '$VAR[Wiz_PageName]')
    # the step counter at the band's right end, same place and slides as the title
    count = (title.replace('[UPPERCASE]$VAR[Aeon_SkinCatName][/UPPERCASE]', '$VAR[Wiz_StepNo] / $VAR[Wiz_StepCount]')
             .replace('<aligny>center</aligny>', '<aligny>center</aligny><align>right</align>', 1)
             .replace('<width>880</width>', '<width>876</width>', 1)
             .replace('<font>st_ui_30_semibold</font>', '<font>st_ui_24</font>', 1)
             .replace('<textcolor>$VAR[AG_Ink]</textcolor>', '<textcolor>80ffffff</textcolor>', 1)
             # the counter ends 24 px inside the divider at 1500 in every style (the title moves left in the style)
             .replace('<animation effect="slide" start="0,0" end="-95,0" time="0" condition="$EXP[FGS]">Conditional</animation>', ''))
    assert count != title and '-95,0' not in count
    x = x.replace(title, new + '\n\t\t' + count)
    return x


def step_column():
    s = SS.index('<control type="group">\n\t\t\t<left>page_margin</left>')
    e = ctl_end(SS, s)
    g = SS[s:e]
    first = g.index('<control type="group">', len('<control type="group">'))
    head = g[:first]
    f0 = g[first:ctl_end(g, first)]
    assert 'Control.HasFocus(9600)' in f0 and '<top>199</top>' in f0
    out_s = g.index('<!-- category outline')
    outline = g[out_s:g.rindex('</control>')]
    o = [head]
    lifted = False
    for i, (key, sid, name, icon, _gid, _sb, vis) in enumerate(PAGES):
        lift = '$EXP[Wiz_FG]' if lifted else 'false'
        fg = f0.replace('Control.HasFocus(9600)', 'Control.HasFocus(%d)' % sid).replace('<top>199</top>', '<top>%d</top>' % (199 + 70 * i), 1)
        if lifted:
            fg = fg.replace('</visible>', '</visible>\n\t\t\t\t<animation effect="slide" start="0,0" end="0,-70" time="0" condition="$EXP[Wiz_FG]">Conditional</animation>', 1)
        o.append(fg)
        prev = PAGES[i - 1][1] if i else None
        nxt = PAGES[i + 1][1] if i + 1 < len(PAGES) else PAGES[0][1]
        params = [('id', sid), ('top', 199 + 70 * i), ('label', name), ('key', key), ('icon', icon),
                  ('onright', first_row(key)), ('onclick', 'SetFocus(%d)' % first_row(key)),
                  ('onup', prev or PAGES[-1][1]), ('ondown', nxt),
                  ('onback', prev if prev else 'Skin.SetBool(aeon.wizard.done)'),
                  ('visible', vis or 'true'), ('lift', lift)]
        o.append('\t\t\t<include content="Wiz_Category">\n\t\t\t\t%s\n\t\t\t</include>' %
                 ''.join('<param name="%s" value="%s"/>' % (k, esc(str(v)) if k in ('visible', 'lift') else v) for k, v in params))
        if vis:
            lifted = True
    o.append(outline)
    o.append('\t\t</control>')
    return '\n'.join(o)


def help_box():
    m = re.search(r'\t\t<control type="textbox">\s*<left>600</left><top>972</top>.*?</control>', SS, re.S)
    return m.group(0).replace('Window(Home).Property(aeon.skincat)', P('page'))


def window():
    head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!-- GENERATED by _src/wizard_05640.py from SkinSettings.xml - edit the generator, not this file.\n'
            '     Setup wizard: Skin settings rows in pages (Window(Home).Property(aeon.wiz.page)), steps in the category column. -->\n'
            '<window type="dialog" id="1173">\n'
            '\t<defaultcontrol always="true">9401</defaultcontrol>\n'
            '\t<onload condition="String.IsEmpty(Window(Home).Property(aeon.wiz.page))">SetProperty(aeon.wiz.page,theme,home)</onload>\n'
            '\t<onload condition="String.IsEmpty(Window(Home).Property(aeon.wiz.theme))">SetProperty(aeon.wiz.theme,fused,home)</onload>\n'
            '\t<onunload>ClearProperty(aeon.wiz.page,home)</onunload>\n'
            '\t<include>Anim_WindowOpenClose</include>\n\t<controls>\n')
    body = window_chrome() + step_column() + '\n' + ''.join(page_xml(k) for k in KEYS) + help_box() + '\n'
    return head + body + '\t</controls>\n</window>\n'


# ------------------------------------------------------------------------------------------------- includes
def category_include():
    t = rd('Includes_Settings.xml')
    s = t.index('\t<include name="Dlg_SkinCategory">')
    e = t.index('\t</include>\n', t.index('</definition>', s)) + len('\t</include>\n')
    x = t[s:e].replace('name="Dlg_SkinCategory"', 'name="Wiz_Category"')
    x = x.replace('Window(Home).Property(aeon.skincat)', P('page')).replace('SetProperty(aeon.skincat,', 'SetProperty(aeon.wiz.page,')
    x = x.replace('<onback>ActivateWindow(home)</onback>\n\t\t\t\t\t<onback>ActivateWindow(1151)</onback>', '<onback>$PARAM[onback]</onback>')
    assert '<onback>$PARAM[onback]</onback>' in x, 'category onback'
    x = x.replace('<param name="onclick">noop</param>', '<param name="onclick">noop</param>\n\t\t<param name="visible">true</param>\n\t\t<param name="lift">false</param>')
    x = x.replace('<top>$PARAM[top]</top>', '<top>$PARAM[top]</top>\n\t\t\t\t<visible>$PARAM[visible]</visible>\n'
                  '\t\t\t\t<animation effect="slide" start="0,0" end="0,-70" time="0" condition="$PARAM[lift]">Conditional</animation>', 1)
    return x


def var(name, values, default=None):
    o = ['\t<variable name="%s">' % name]
    for cond, val in values:
        o.append('\t\t<value condition="%s">%s</value>' % (esc(cond), val))
    if default is not None:
        o.append('\t\t<value>%s</value>' % default)
    o.append('\t</variable>')
    return '\n'.join(o)


def includes():
    keep = MENU_VARS
    assert len(keep) == 14, len(keep)
    mt = P('menutheme')
    exprs = [
        ('Wiz_FG', 'String.IsEqual(%s,fused)' % P('theme')),
        ('Wiz_GL', 'String.IsEqual(%s,glass)' % P('theme')),
        ('Wiz_AE', '!$EXP[Wiz_FG] + !$EXP[Wiz_GL]'),
        ('Wiz_Glassy', '$EXP[Wiz_FG] | $EXP[Wiz_GL]'),
        ('Wiz_Fused', 'String.IsEqual(%s,fused) + !$EXP[Wiz_FG]' % mt),
        ('Wiz_MS', '$EXP[Wiz_AE] + !String.IsEqual(%s,fused)' % mt),
        ('Wiz_MS_mosaic', '$EXP[Wiz_MS] + String.IsEqual(%s,mosaic)' % mt),
        ('Wiz_MS_ledger', '$EXP[Wiz_MS] + String.IsEqual(%s,ledger)' % mt),
        ('Wiz_MS_tabslab', '$EXP[Wiz_MS] + String.IsEqual(%s,tabslab)' % mt),
        ('Wiz_MS_bridge', '$EXP[Wiz_MS] + !String.IsEqual(%s,mosaic) + !String.IsEqual(%s,ledger) + !String.IsEqual(%s,tabslab)' % (mt, mt, mt)),
        ('Wiz_FGS', '$EXP[Wiz_FG] + String.IsEqual(%s,system)' % P('fgmenu')),
        ('Wiz_PalDefault', 'String.IsEmpty(%s) | String.IsEqual(%s,SKINDEFAULT) | String.IsEqual(%s,Aeon)' % (P('palette'), P('palette'), P('palette'))),
        ('Wiz_AccentOwn', '$EXP[Wiz_AE] + $EXP[Wiz_PalDefault]'),
        # Finish needs the skin loaded again: another theme, Skin style, palette or fonts
        ('Wiz_ThemeChanged', '[$EXP[Wiz_FG] + !Skin.HasSetting(aeon.fglass)] | [$EXP[Wiz_GL] + ![Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)]] | [$EXP[Wiz_AE] + Skin.HasSetting(aeon.vglass)]'),
        ('Wiz_StyleChanged', '[$EXP[Wiz_FG] + [' + ' | '.join(
            '[%s + !%s]' % (a, b) for a, b in (
                ('String.IsEmpty(%s)' % P('fgmenu'), 'String.IsEmpty(Skin.String(aeon.fgmenu))'),
                ('String.IsEqual(%s,glass)' % P('fgmenu'), 'String.IsEqual(Skin.String(aeon.fgmenu),glass)'),
                ('String.IsEqual(%s,frost)' % P('fgmenu'), 'String.IsEqual(Skin.String(aeon.fgmenu),frost)'),
                ('String.IsEqual(%s,system)' % P('fgmenu'), 'String.IsEqual(Skin.String(aeon.fgmenu),system)'))) + ']]' +
         ' | [!$EXP[Wiz_FG] + [[String.IsEqual(%s,fused) + !String.IsEqual(Skin.String(aeon.menutheme),fused)] | [!String.IsEqual(%s,fused) + String.IsEqual(Skin.String(aeon.menutheme),fused)]]]' % (mt, mt)),
        ('Wiz_Restart', '$EXP[Wiz_ThemeChanged] | $EXP[Wiz_StyleChanged] | !String.IsEmpty(%s) | !String.IsEmpty(%s)' % (P('palchanged'), P('fontchanged'))),
    ]
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<!-- Setup wizard (dialog 1173): GENERATED by _src/wizard_05640.py - edit the generator, not this file. -->',
         '<includes>']
    for name, x in exprs:
        o.append('\t<expression name="%s">%s</expression>' % (name, esc(x)))
    for key, cond in sorted(MENU_ON.items()):
        o.append('	<expression name="Wiz_MenuOn_%s">%s</expression>' % (key, esc(cond)))
    o.append(category_include())
    # page names, step numbers
    o.append(var('Wiz_PageName', [('String.IsEqual(%s,%s)' % (P('page'), k), n) for k, _s, n, _i, _g, _b, _v in PAGES]))
    nums = []
    for k in KEYS:
        i = KEYS.index(k)
        if i > KEYS.index('library'):
            nums.append(('String.IsEqual(%s,%s) + %s' % (P('page'), k, FG), '$NUMBER[%d]' % i))
        nums.append(('String.IsEqual(%s,%s)' % (P('page'), k), '$NUMBER[%d]' % (i + 1)))
    o.append(var('Wiz_StepNo', nums))
    o.append(var('Wiz_StepCount', [(FG, '$NUMBER[%d]' % (len(KEYS) - 1))], '$NUMBER[%d]' % len(KEYS)))
    for k in KEYS[:-1]:
        o.append(var('Wiz_NextName_%s' % k, [(c or 'true', PAGES[KEYS.index(n)][2]) for c, n in next_page(k)]))
    # names of the choices
    o.append(var('Wiz_ThemeName', [(FG, A(32402)), (GL, L(31679))], L(31678)))
    fgm, mt_ = P('fgmenu'), P('menutheme')
    o.append(var('Wiz_StyleName', [
        (FG + ' + String.IsEqual(%s,glass)' % fgm, A(32549)), (FG + ' + String.IsEqual(%s,frost)' % fgm, A(32547)),
        (FG + ' + String.IsEqual(%s,system)' % fgm, A(32402)), (FG, A(32573)),
        ('String.IsEqual(%s,fused)' % mt_, 'Fuse'),
        (GL, L(31679)),
        ('String.IsEqual(%s,mosaic)' % mt_, A(32452)), ('String.IsEqual(%s,ledger)' % mt_, A(32453)),
        ('String.IsEqual(%s,tabslab)' % mt_, A(32455))], A(32454)))
    o.append(var('Wiz_PaletteName', [('$EXP[Wiz_PalDefault]', 'Aeon')], '$INFO[%s]' % P('palette')))
    o.append(var('Wiz_PalSwatch', [('String.IsEqual(%s,%s)' % (P('palette'), p['val']), p['swatch']) for p in DATA['palettes']
                                   if p['val'] != 'SKINDEFAULT'], 'ffe9e9e9'))
    plat = 'System.Platform.Linux + !System.Platform.Android'
    o.append(var('Wiz_FinishHint', [('$EXP[Wiz_Restart] + ' + plat, A(32276)), ('$EXP[Wiz_Restart]', A(32277))], A(32278)))
    o.append(var('Wiz_FinishMore', [('$EXP[Wiz_Restart] + ' + plat, A(32279)), ('$EXP[Wiz_Restart]', A(32280))], A(32281)))
    o.extend(keep)
    o.append('</includes>')
    return '\n'.join(o) + '\n'


HELP_BEGIN, HELP_END = '\t\t<!-- WIZARD HELP (_src/wizard_05640.py) -->', '\t\t<!-- /WIZARD HELP -->'


def help_values():
    """Dlg_SkinHelp: the wizard's rows first (the window is 1173); copied rows whose help depends on the theme follow
    the chosen theme there"""
    t = rd('Includes_Settings.xml')
    s = t.index('<variable name="Dlg_SkinHelp">')
    e = t.index('</variable>', s)
    block = t[s:e]
    block = re.sub(r'\n?' + re.escape(HELP_BEGIN) + r'.*?' + re.escape(HELP_END), '', block, flags=re.S)
    w = 'Window.IsActive(1173) + '
    vals = []
    for key, rid, _name, help_ in THEMES:
        vals.append((w + 'Control.HasFocus(%d)' % rid, help_))
    vals.append((w + 'Control.HasFocus(9404)', A(32040)))
    vals += [(w + 'Control.HasFocus(9411)', A(S_DEFAULTS_HELP)), (w + 'Control.HasFocus(9412)', A(S_CUSTOM_HELP)),
             (w + 'Control.HasFocus(9413)', A(S_KEEP_HELP))]
    vals += [(w + 'Control.HasFocus(9748) + ' + FG, A(32574)), (w + 'Control.HasFocus(9748) + ' + AE, A(32456)),
             (w + 'Control.HasFocus(9748)', A(32457))]
    vals.append((w + 'Control.HasFocus(9743)', L(31580)))
    for n, (aid, _name, _vis) in enumerate(ADDONS):
        vals.append((w + 'Control.HasFocus(%d)' % (9451 + n), A(S_ADDONS[aid])))
    vals.append((w + 'Control.HasFocus(9409)', '$VAR[Wiz_FinishMore]'))
    for k in KEYS[:-1]:
        if k in ('theme', 'start'):
            continue
        vals.append((w + 'Control.HasFocus(%d)' % NEXT_ID[k], L(209) + ': $VAR[Wiz_NextName_%s]' % k))
    vals.append((w + '[%s]' % ' | '.join('Control.HasFocus(%d)' % (9431 + n) for n in range(len(DATA['menu']))), A(32263)))
    lines = ['\t\t<value condition="%s">%s</value>' % (esc(c), v) for c, v in vals]
    if not INSTALL:                                  # parked: the classic wizard has no use for these
        wr('Includes_Settings.xml', t[:s] + block + t[e:])
        return
    first = block.index('\n', block.index('<variable name="Dlg_SkinHelp">')) + 1
    block = block[:first] + HELP_BEGIN + '\n' + '\n'.join(lines) + '\n' + HELP_END + '\n' + block[first:]
    t = t[:s] + block + t[e:]
    wr('Includes_Settings.xml', t)


def main():
    wr('Includes_Aeon_Wizard.xml', includes())
    wr('Custom_1173_SetupWizard.xml', window())
    help_values()
    x = io.open(os.path.join(OUT_DIR, 'Custom_1173_SetupWizard.xml'), encoding='utf-8').read()
    ids = re.findall(r'<control type="(?:button|grouplist|scrollbar)" id="(\d+)">', x)
    dup = sorted(set(i for i in ids if ids.count(i) > 1))
    assert not dup, ('duplicate ids', dup)
    print('wizard: %d bytes, %d buttons' % (len(x), len(ids)))


if __name__ == '__main__':
    main()
