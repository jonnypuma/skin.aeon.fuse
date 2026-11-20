# -*- coding: utf-8 -*-
"""0.56.40 Setup wizard (dialog 1173) in its original look, one setting per step, in the flow agreed on 2026-11-17.

The user: "bring back the old wizard and update it based on what we agreed" and "One setting per step". The look is
the old wizard's, unchanged (its window head, the option cards Aeon_WizItem, the big preview with the focused option's
name and text, the credits on the first step, the progress dots and the key hint are taken from the 0.56.39 files kept
in _src/wizard_classic_0539/). What changes is the list of steps:
  Welcome (credits) > Skin theme (Fused Glass, Aeon, Aeon Glass) > Start (Use the defaults, Customise, Keep my current
  settings on a re-run) > the chosen theme's look: Fused Glass: Skin style, Menu background (Fused Glass style), Panel
  shadow, Focus highlight, Navigation animation, Toast expand from clock pill; Aeon: Skin style, Palette, Aeon accent
  colour (Aeon palette); Aeon Glass: Skin style > Libraries (Aeon, Aeon Glass): Corner boxes, Library side strip,
  Settings strip, Library options (Aeon menu styles) > Home: menu position, only the focused item's name, underline and
  Now playing (Aeon, Aeon Glass), vignette, vignette shape > Backgrounds: fanart backdrop, its strength, library
  background, fanart look (Fanart) > Font combination > Home menu items > Add-ons > All set.
Steps that do not belong to the chosen theme are skipped (OK and Back jump over them, their dots hide). OK on a card
sets it and moves on; on entering a step the card in use has the focus. Theme, Skin style, palette, fonts and the focus
highlight wait for Finish (window properties aeon.wiz.*): the helper applies them and restarts Kodi (Linux) or reloads
the skin. Pictures: media/aeon/wizard/shots/<theme>_<step>_<value>.jpg, real box screenshots (the user's flow:
"previews should use proper fanart and library views"); fonts and add-ons are drawn (_src/wizard_pictures_05640.py).
The Skin-settings-look wizard built first is parked in _src/wizard_settings_look/ (_src/wizard_settingslook_05640.py).
Run from the skin folder. Repeatable: writes Custom_1173_SetupWizard.xml and Includes_Aeon_Wizard.xml whole."""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '1080i')
OLD = os.path.join(HERE, 'wizard_classic_0539')
DATA = json.load(io.open(os.path.join(HERE, 'wizard_data.json'), encoding='utf-8'))
SHOTS = 'aeon/wizard/shots/'


def old(name):
    return io.open(os.path.join(OLD, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def A(n):
    return '$ADDON[skin.aeon.fuse %d]' % n


def L(n):
    return '$LOCALIZE[%d]' % n


def P(name):
    return 'Window(Home).Property(aeon.wiz.%s)' % name


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


THEME_NOW = '$INFO[%s]' % P('theme')
STEP = P('step')

# ---------------------------------------------------------------------------------------------------------- new strings
S_THEME_TEXT, S_FG_SHORT, S_START_TEXT, S_SETSTRIP, S_VIGNETTE, S_ACCENT, S_ADDONS_TEXT = range(32713, 32720)
S_ADDON = dict(zip(('plugin.video.themoviedb.helper', 'script.embuary.helper', 'script.cu.lrclyrics', 'script.artistslideshow',
                    'script.karmamole.helper', 'service.skippy', 'service.trickplay', 'resource.images.studios.white',
                    'resource.images.recordlabels.white', 'resource.images.languageflags.colour', 'screensaver.aeon.fuse'),
                   range(32702, 32713)))

# ---------------------------------------------------------------------------------------------------------- conditions
# a step's "when": {var: value}; var: theme ('fused'/'aeon'/'glass' or a tuple), fgs (Fused Glass style chosen),
# ms (an Aeon menu style, not Fuse), paldef (the Aeon palette), backdrop (fanart backdrop on), vbg ('fanart')
RUNTIME = {
    'fgs': 'String.IsEqual(%s,system)' % P('fgmenu'),
    'ms': '!String.IsEqual(%s,fused)' % P('menutheme'),
    'paldef': '[String.IsEmpty(%s) | String.IsEqual(%s,SKINDEFAULT)]' % (P('palette'), P('palette')),
    'backdrop': '!Skin.HasSetting(aeon.nobackdrop)',
    'vbg': 'String.IsEqual(Skin.String(aeon.vbg),fanart)',
}


def cond_of(when, known=None):
    """True / False / a Kodi condition for a step's when, with some vars known (the card just chosen)"""
    known = known or {}
    parts = []
    for var, want in sorted(when.items()):
        if var in known:
            have = known[var]
            have = set(have) if isinstance(have, tuple) else {have}
            want_set = set(want) if isinstance(want, tuple) else {want}
            if not have & want_set:
                return False
            if have <= want_set:
                continue
            want = tuple(sorted(have & want_set))      # still open: only the values both allow
        if var == 'theme':
            ts = want if isinstance(want, tuple) else (want,)
            parts.append('[%s]' % ' | '.join('String.IsEqual(%s,%s)' % (P('theme'), t) for t in ts))
        else:
            parts.append(RUNTIME[var] if want is True else '!' + RUNTIME[var])
    return ' + '.join(parts) if parts else True


# ---------------------------------------------------------------------------------------------------------- the steps
class Step(object):
    def __init__(self, key, cap, title, text, when=None, options=None, cur=None, pictures=None, sets=None, advance=True):
        self.key, self.cap, self.title, self.text = key, cap, title, text
        self.when = when or {}
        self.options = options or []      # dicts: tok, label, label2, more, actions, known, visible, icon
        self.cur = cur                    # [(condition, token)], default token last as (None, tok)
        self.pictures = pictures          # 'theme' (per wizard theme), a fixed prefix, or None
        self.sets = sets                  # the var this step decides (for "known")
        self.advance = advance


def opt(tok, label, actions, label2='', more='', known=None, visible=None, icon=None):
    return {'tok': tok, 'label': label, 'label2': label2, 'more': more, 'actions': actions, 'known': known or {},
            'visible': visible, 'icon': icon}


def str_setting(name, values, default):
    """values: [(token, label)], token 'default' = ''; -> options' actions and the cur variable"""
    opts, cur = [], []
    for tok, label in values:
        act = ['Skin.Reset(%s)' % name] if tok == 'default' else ['Skin.SetString(%s,%s)' % (name, tok)]
        opts.append(opt(tok, label, act))
        if tok != 'default':
            cur.append(('String.IsEqual(Skin.String(%s),%s)' % (name, tok), tok))
    if default != 'default':
        cur = [c for c in cur if c[1] != default]
        cur.append(('String.IsEmpty(Skin.String(%s))' % name, default))
    cur.append((None, default))
    return opts, cur


def bool_setting(name, off_label, on_label, inverted=False):
    """a switch: tokens off / on (inverted: on = the setting reset, e.g. aeon.nobackdrop)"""
    set_on, set_off = ('Skin.Reset(%s)' % name, 'Skin.SetBool(%s)' % name) if inverted else ('Skin.SetBool(%s)' % name, 'Skin.Reset(%s)' % name)
    opts = [opt('off', off_label, [set_off]), opt('on', on_label, [set_on])]
    has = 'Skin.HasSetting(%s)' % name
    cur = [('!' + has if inverted else has, 'on'), (None, 'off')]
    return opts, cur


def prop_setting(name, values, default_tok):
    """a choice that waits for Finish: window property aeon.wiz.<name>; token 'default' = empty"""
    opts, cur = [], []
    for tok, label in values:
        act = ['ClearProperty(aeon.wiz.%s,home)' % name] if tok == 'default' else ['SetProperty(aeon.wiz.%s,%s,home)' % (name, tok)]
        opts.append(opt(tok, label, act))
        if tok != 'default':
            cur.append(('String.IsEqual(%s,%s)' % (P(name), tok), tok))
    cur.append((None, default_tok))
    return opts, cur


STEPS = []


def add(step):
    STEPS.append(step)
    return step


# 1 welcome
add(Step('welcome', A(32243), A(32246), A(32258), options=[
    opt('start', A(32035), [], A(32036), A(32037), icon='aeon/wizard/welcome.jpg'),
    opt('skip', A(32038), ['Skin.SetBool(aeon.wizard.done)', 'Dialog.Close(1173)'], A(32039), A(32040), icon='aeon/wizard/welcome.jpg')],
    cur=[(None, '')]))
# 2 recommended add-ons (0.56.53): tick the ones wanted (a skin bool each), Next installs them in the background
# (helper addonrec,batch: repository first when needed, Kodi's own install question answered Yes) and moves on.
# The list is the helper's resources/lib/recommended.py.
ADDONS = [('plugin.video.themoviedb.helper', 'TMDb Helper'), ('script.karmamole.helper', 'KarmaMole Skin Helper'),
          ('resource.images.studios.white', 'Studio Icons - White'),
          ('resource.images.recordlabels.white', 'Record Label Icons - White'),
          ('resource.images.languageflags.colour', 'Language Flags - Colour'),
          ('resource.images.weathericons.white', 'Weather Icons - White'), ('script.embuary.helper', 'Embuary Helper'),
          ('script.cu.lrclyrics', 'CU LRC Lyrics'), ('script.artistslideshow', 'Artist Slideshow'),
          ('screensaver.aeon.fuse', 'Aeon Fuse Screensaver'), ('service.skippy', 'Skippy - Video Segment Skipper'),
          ('service.trickplay', 'Trickplay Preview'), ('script.tinyppi', 'TinyPPI'),
          ('resource.fonts.copacetic', 'Copacetic Fonts (Inter)'), ('resource.font.robotocjksc', 'Roboto CJKSC')]
S_ADDON.update({'resource.images.weathericons.white': 32767, 'script.tinyppi': 32768, 'resource.fonts.copacetic': 32769,
                'resource.font.robotocjksc': 32770})
S_ADDONS_STEP, S_WILL_INSTALL = 32791, 32792
adds = []
for aid, name in ADDONS:
    x = opt('on', name, ['@tick:%s' % aid], '$VAR[Wiz_Addon_%s]' % aid.replace('.', '_'), A(S_ADDON[aid]),
            icon=SHOTS + 'addfeat_%s.jpg' % aid)
    x['cur'] = '$VAR[Wiz_AddonOn_%s]' % aid.replace('.', '_')
    adds.append(x)
adds.append(opt('next', L(209), ['RunScript(script.aeon.helper,addonrec,batch)', '@next'], '$VAR[Wiz_AddonsNext]',
                A(S_ADDONS_STEP), icon='aeon/wizard/welcome.jpg'))
add(Step('addons', L(24001), A(32762), A(S_ADDONS_STEP), {}, adds, None, advance=False))
# 2 theme
add(Step('theme', A(32243), A(32249), A(S_THEME_TEXT), sets='theme', options=[
    opt('fused', A(32402), ['SetProperty(aeon.wiz.theme,fused,home)'], A(S_FG_SHORT), A(32694), {'theme': 'fused'}, icon='aeon/wizard/theme_fused.jpg'),
    opt('aeon', L(31678), ['SetProperty(aeon.wiz.theme,aeon,home)'], A(32048), A(32049), {'theme': 'aeon'}, icon='aeon/wizard/theme_aeon.jpg'),
    opt('glass', L(31679), ['SetProperty(aeon.wiz.theme,glass,home)'], A(32050), A(32701), {'theme': 'glass'}, icon='aeon/wizard/theme_glass.jpg')],
    cur=[('String.IsEqual(%s,aeon)' % P('theme'), 'aeon'), ('String.IsEqual(%s,glass)' % P('theme'), 'glass'), (None, 'fused')]))
# 3 start
THEME_PIC = 'aeon/wizard/theme_%s.jpg' % THEME_NOW
add(Step('start', A(32243), A(32035), A(S_START_TEXT), options=[
    opt('defaults', A(32695), ['RunScript(script.aeon.helper,wizard,defaults,finish)'], '', A(32696), icon=THEME_PIC),
    opt('custom', A(32697), ['@first:RunScript(script.aeon.helper,wizard,defaults)'], '', A(32698), icon=THEME_PIC),
    opt('keep', A(32699), ['@done'], '', A(32700), visible='Skin.HasSetting(aeon.wizard.done)', icon=THEME_PIC)],
    cur=[(None, '')]))
# 4-9 Fused Glass
o, c = prop_setting('fgmenu', [('default', A(32573)), ('glass', A(32549)), ('frost', A(32547)), ('system', A(32402))], 'default')
for x in o:
    x['known'] = {'fgs': x['tok'] == 'system'}
add(Step('fgstyle', L(31726), A(32250), A(32574), {'theme': 'fused'}, o, c, 'fused_fgstyle'))
o, c = str_setting('aeon.fgsdlgbg', [('default', L(31550)), ('screen', A(32690))], 'default')
add(Step('dlgbg', L(31726), A(32689), A(32691), {'theme': 'fused', 'fgs': True}, o, c, 'fused_dlgbg'))
o, c = str_setting('aeon.fgshadow', [('mild', A(32670)), ('default', L(31071)), ('strong', L(31673)), ('heavy', A(32671))], 'default')
add(Step('shadow', L(31726), A(32668), A(32669), {'theme': 'fused'}, o, c, 'fused_shadow'))
o, c = str_setting('aeon.fgfocus', [('default', A(32409)), ('frost', A(32411)), ('outline', A(32412)), ('tight', A(32413))], 'default')
c = [x for x in c if x[0] is None or 'pill' not in x[0]]
for x in o:      # buttons take their focus picture when the skin loads: Finish restarts / reloads for it
    v = '' if x['tok'] == 'default' else x['tok']
    x['actions'].append('@reload:aeon.fgfocus:%s' % v)
add(Step('focus', L(31726), A(32408), A(32414), {'theme': 'fused'}, o, c, 'fused_focus'))
o, c = str_setting('aeon.fganim', [('default', A(32416)), ('grow', A(32417)), ('fade', A(32418)), ('glow', A(32419)),
                                   ('nudge', A(32420)), ('lift', A(32421)), ('none', L(231))], 'default')
for x in o:
    x['icon'] = SHOTS + 'fused_anim.jpg'      # motion cannot be shown in a still: one picture, the text tells
add(Step('anim', L(31726), A(32415), A(32422), {'theme': 'fused'}, o, c, None))
o, c = bool_setting('aeon.toastpill', L(31072), L(31547))
add(Step('toast', L(31726), A(32474), A(32475), {'theme': 'fused'}, o, c, 'fused_toast'))
# 10-12 Aeon
o, c = prop_setting('menutheme', [('mosaic', A(32452)), ('ledger', A(32453)), ('default', A(32454)), ('tabslab', A(32455)), ('fused', 'Fuse')], 'default')
for x in o:
    x['known'] = {'ms': x['tok'] != 'fused'}
add(Step('aeonstyle', L(31726), A(32250), A(32456), {'theme': 'aeon'}, o, c, 'aeon_aeonstyle'))
pal_opts = []
COLORS = os.path.join(HERE, '..', 'colors')
MOCK_COLS = ('aeon_white', 'aeon_onbar', 'aeon_box', 'x_ground', 'x_panel', 'x_raised', 'x_line')


def palette_colours(name):
    """a palette's colours for the live mock-up: defaults.xml, then what the palette file changes"""
    out = {}
    for f in ('defaults.xml', '' if name == 'SKINDEFAULT' else name + '.xml'):
        if not f:
            continue
        text = io.open(os.path.join(COLORS, f), encoding='utf-8').read()
        for m in re.finditer(r'<color name="([\w]+)">([0-9a-fA-F]{8})</color>', text):
            out[m.group(1)] = m.group(2).lower()
    return dict((k, out[k]) for k in MOCK_COLS)


for p in DATA['palettes']:
    name = p['val']
    # the old palette step: the wizard's own cards take the palette's colours (Aeon_WizCardF / Ink / Ink3 / Accent)
    acts = ['SetProperty(aeon.wiz.%s,%s,home)' % (k, p[v]) for k, v in (('pw', 'swatch'), ('pk', 'pk'), ('pk2', 'pk2'), ('pa', 'pa'))]
    acts.append('SetProperty(aeon.wiz.palette,%s,home)' % name)
    acts.append('@palchanged:%s' % name)
    # no picture: the preview is a mock-up drawn in the focused palette's colours (palette_mock), live while moving
    x = opt(name, p['label'], acts, '', A(32047), {'paldef': name == 'SKINDEFAULT'}, icon='-')
    x['props'] = dict((k, p[k]) for k in ('swatch', 'pk', 'pk2', 'pa'))
    x['props'].update(('c_' + k, v) for k, v in palette_colours(name).items())
    pal_opts.append(x)
add(Step('palette', L(31726), A(32248), A(32260), {'theme': 'aeon'}, pal_opts,
         [('String.IsEqual(%s,%s)' % (P('palette'), p['val']), p['val']) for p in DATA['palettes'] if p['val'] != 'SKINDEFAULT'] + [(None, 'SKINDEFAULT')]))
o, c = str_setting('aeon.boxaccent', [('default', A(32595)), ('slate', A(32596)), ('teal', A(32597)), ('moss', A(32598))], 'default')
add(Step('accent', L(31726), A(32594), A(S_ACCENT), {'theme': 'aeon', 'paldef': True}, o, c, 'aeon_accent'))
# 13 Aeon Glass
o, c = prop_setting('menutheme', [('default', L(31679)), ('fused', 'Fuse')], 'default')
c = [('String.IsEqual(%s,fused)' % P('menutheme'), 'fused'), (None, 'default')]
for x in o:      # 0.56.44: the focus step below belongs to Aeon Glass's own style, not Fuse
    x['known'] = {'ms': x['tok'] != 'fused'}
add(Step('glassstyle', L(31726), A(32250), A(32457), {'theme': 'glass'}, o, c, 'glass_glassstyle'))
# 0.56.44 Aeon Glass: Panel shadow (Fused Glass's setting) and its own Focus highlight (aeon.agfocus: Glass, the accent
# bar, or Fused Glass's pictures; menus and dialogs, not with Fuse). Pictures: Skin settings on the box per option.
o, c = str_setting('aeon.fgshadow', [('mild', A(32670)), ('default', L(31071)), ('strong', L(31673)), ('heavy', A(32671))], 'default')
add(Step('agshadow', L(31726), A(32668), A(32669), {'theme': 'glass'}, o, c, 'glass_agshadow'))
o, c = str_setting('aeon.agfocus', [('default', A(32429)), ('pill', A(32409)), ('frost', A(32411)), ('outline', A(32412)), ('tight', A(32413))], 'default')
for x in o:      # buttons take their focus picture when the skin loads: Finish restarts / reloads for it
    v = '' if x['tok'] == 'default' else x['tok']
    x['actions'].append('@reload:aeon.agfocus:%s' % v)
add(Step('agfocus', L(31726), A(32408), A(32414), {'theme': 'glass', 'ms': True}, o, c, 'glass_agfocus'))
# 14-17 Libraries
AG = ('aeon', 'glass')
o, c = str_setting('aeon.boxbg', [('default', L(31551)), ('neutral', L(31549)), ('fanart', L(31550)), ('follow', L(31543))], 'default')
add(Step('boxes', A(32244), A(32253), A(32470), {'theme': AG}, o, c, 'theme'))
o, c = bool_setting('aeon.vsbwhite', L(31665), L(31666))
add(Step('sidestrip', A(32244), L(31748), L(31577), {'theme': AG}, o, c, 'theme'))
o, c = bool_setting('aeon.strip.perm', L(31801), L(31802))
add(Step('setstrip', A(32244), L(31800), A(S_SETSTRIP), {'theme': AG}, o, c, 'theme'))
o, c = bool_setting('aeon.libpanel.box', A(32459), A(32460))
add(Step('libopts', A(32244), A(32458), A(32461), {'theme': 'aeon', 'ms': True}, o, c, 'aeon_libopts'))
# 18-23 Home
o, c = bool_setting('aeon.lowmenu', L(31857), L(31858))
add(Step('menupos', L(31019), L(31856), A(32264), {}, o, c, 'theme'))
o, c = bool_setting('aeon.hm.icons', L(31072), L(31547))
add(Step('focusname', L(31019), A(32425), A(32426), {}, o, c, 'theme'))
o, c = bool_setting('aeon.hm.underline', L(31548), L(31547))
add(Step('underline', L(31019), A(32607), A(32612), {'theme': AG}, o, c, 'theme'))
o, c = str_setting('aeon.npplace', [('default', L(31674)), ('b', L(31675)), ('c', L(31676)), ('d', L(31677))], 'default')
c = [x for x in c if x[0] is None or not x[0].endswith(',a)')]
add(Step('nowplaying', L(31019), L(31765), L(31580), {'theme': AG}, o, c, 'theme'))
# 0.56.42 Fused Glass: Now playing on Home beside the clock or in the lower left corner (aeon.fgnpleft)
o, c = bool_setting('aeon.fgnpleft', A(32742), A(32743))
add(Step('fgnowplaying', L(31019), L(31765), A(32745), {'theme': 'fused'}, o, c, 'theme'))
o, c = str_setting('aeon.vignette', [('default', L(31548)), ('b', L(31672)), ('c', L(31071)), ('e', L(31673)), ('d', A(32603))], 'default')
add(Step('vignette', L(31019), L(31821), A(S_VIGNETTE), {}, o, c, 'theme'))
o, c = bool_setting('aeon.vignette.side', A(32601), A(32599))
add(Step('vigshape', L(31019), A(32600), A(32602), {}, o, c, 'theme'))
# 0.56.42 Home gradient Off | Soft (default) | Strong, every theme (pictures from Fused Glass Home)
o, c = str_setting('aeon.homegrad', [('off', L(31548)), ('default', A(32740)), ('strong', L(31673))], 'default')
add(Step('homegrad', L(31019), A(32741), A(32744), {}, o, c, 'fused_homegrad'))
# 24-27 Backgrounds
o, c = bool_setting('aeon.nobackdrop', L(31072), L(31547), inverted=True)
for x in o:
    x['known'] = {'backdrop': x['tok'] == 'on'}
add(Step('backdrop', L(31729), L(31763), L(31576), {}, o, c, 'theme'))
o, c = str_setting('aeon.backdrop.dim', [('light', L(31672)), ('default', L(31071)), ('strong', L(31673))], 'default')
add(Step('strength', L(31729), L(31764), L(31581), {'backdrop': True}, o, c, 'theme'))
o, c = str_setting('aeon.vbg', [('default', L(31549)), ('fanart', L(31550)), ('color', L(31680))], 'default')
for x, l2, more in zip(o, (32041, 32043, 32045), (32042, 32044, 32046)):
    x['label2'], x['more'] = A(l2), A(more)
    x['known'] = {'vbg': x['tok'] == 'fanart'}
add(Step('libbg', L(31729), A(32247), L(31578), {}, o, c, 'theme', sets='vbg'))
o = [opt('dimmed', A(32609), ['Skin.SetString(aeon.fanartlook,dimmed)']), opt('frosted', A(32411), ['Skin.SetString(aeon.fanartlook,frosted)'])]
c = [('String.IsEqual(Skin.String(aeon.fanartlook),frosted) | [String.IsEmpty(Skin.String(aeon.fanartlook)) + !String.IsEqual(%s,aeon)]' % P('theme'), 'frosted'),
     (None, 'dimmed')]
add(Step('fanartlook', L(31729), A(32608), A(32613), {'vbg': True}, o, c, 'theme'))
# 28 fonts
FONTS = [('figtree', 'Figtree'), ('fraunces', 'Fraunces + Figtree'), ('bebas', 'Bebas Neue + Figtree'),
         ('oswald', 'Oswald + Source Sans 3'), ('barlowc', 'Barlow Condensed + Barlow'), ('funnel', 'Funnel Display + Figtree'),
         ('calsans', 'Cal Sans + Figtree'), ('hubotc', 'Hubot Sans Condensed + Hubot Sans'), ('hubote', 'Hubot Sans Expanded + Figtree'),
         ('sairac', 'Saira Condensed + Saira'), ('clarity', 'Clarity City + Pretendard'), ('gnomon', 'Gnomon + Clarity City')]
# compared by key: a condition cannot hold the names' spaces and '+' (the helper publishes aeon.wiz.fontkey)
o = [opt(key, name, ['RunScript(script.aeon.helper,fonts,set,%s)' % key], icon=SHOTS + 'font_%s.jpg' % key) for key, name in FONTS]
add(Step('fonts', L(31822), A(32423), A(32424), {}, o, [(None, '$INFO[%s]' % P('fontkey'))]))
# 29 Home menu items (switches; Next moves on)
items = []
for item in DATA['menu']:
    m = re.match(r'\$VAR\[Aeon_Name_(\w+)\]$', item['label'])
    if not m:
        continue
    key = m.group(1)
    items.append(opt('on', item['label'], ['RunScript(script.aeon.helper,wizard,menu,%s)' % key],
                     visible='System.HasPVRAddon' if key == 'livetv' else None,
                     icon=SHOTS + '%s_menupos_off.jpg' % THEME_NOW))
    items[-1]['cur'] = '$VAR[Aeon_WizMenu_%s]' % key
items.append(opt('next', L(209), ['@next'], icon=SHOTS + '%s_menupos_off.jpg' % THEME_NOW))
add(Step('items', L(31019), A(32251), A(32263), {}, items, None, advance=False))
# 31 all set
add(Step('done', L(20177), A(32257), A(32275), options=[
    opt('finish', A(32142), ['RunScript(script.aeon.helper,wizard)'], '$VAR[Wiz_FinishHint]', '$VAR[Wiz_FinishMore]', icon=THEME_PIC),
    opt('back', L(31245), ['@back'], A(32143), A(32144), icon=THEME_PIC)], cur=[(None, '')]))

N = dict((s.key, n) for n, s in enumerate(STEPS, 1))


def list_id(n):
    return 9100 + n


# ---------------------------------------------------------------------------------------------------------- navigation
def goto(n, cond=None):
    c = ' condition="%s"' % esc(cond) if cond else ''
    return ['<onclick%s>SetProperty(aeon.wiz.step,%d,home)</onclick>' % (c, n),
            '<onclick%s>SetFocus(%d,$VAR[Wiz_Pos_%d],absolute)</onclick>' % (c, list_id(n), n)]


def chain_after(i, known):
    """[(condition or None, step number)] to the next step that applies, from step index i"""
    out, skipped = [], []
    for j in range(i + 1, len(STEPS)):
        c = cond_of(STEPS[j].when, known)
        if c is False:
            continue
        if c is True:
            out.append((' + '.join(skipped) or None, j + 1))
            return out
        out.append((' + '.join(skipped + [c]), j + 1))
        skipped.append('![%s]' % c)
    return out


def chain_before(i):
    out, skipped = [], []
    for j in range(i - 1, -1, -1):
        c = cond_of(STEPS[j].when)
        if c is True:
            out.append((' + '.join(skipped) or None, j + 1))
            return out
        out.append((' + '.join(skipped + [c]), j + 1))
        skipped.append('![%s]' % c)
    return out


def next_clicks(i, known):
    o = []
    for cond, n in chain_after(i, known):
        o += goto(n, cond)
    return o


def onbacks(i):
    if i == 0:
        return ['<onback>Skin.SetBool(aeon.wizard.done)</onback>', '<onback>Dialog.Close(1173)</onback>']
    o = []
    for cond, n in chain_before(i):
        c = ' condition="%s"' % esc(cond) if cond else ''
        o += ['<onback%s>SetProperty(aeon.wiz.step,%d,home)</onback>' % (c, n), '<onback%s>%d</onback>' % (c, list_id(n))]
    return o


def item_clicks(i, step, x):
    o = []
    # a step shows only when its own conditions hold: they are known on its cards, and so is the card's own value
    known = dict(step.when)
    known.update(x['known'])
    for a in x['actions']:
        if a.startswith('@first:'):
            o.append('<onclick condition="!Skin.HasSetting(aeon.wizard.done)">%s</onclick>' % a[len('@first:'):])
        elif a == '@done':
            o += goto(N['done'])
        elif a == '@next':
            o += next_clicks(i, known)
        elif a == '@back':
            for cond, n in chain_before(i):
                o += goto(n, cond)
        elif a.startswith('@palchanged:'):
            name = a.split(':', 1)[1]
            o.append('<onclick condition="!String.IsEqual(%s,%s)">SetProperty(aeon.wiz.palchanged,1,home)</onclick>' % (P('pal0'), name))
            o.append('<onclick condition="String.IsEqual(%s,%s)">ClearProperty(aeon.wiz.palchanged,home)</onclick>' % (P('pal0'), name))
        elif a.startswith('@reload:'):
            _x, setting, value = a.split(':', 2)
            now = 'String.IsEmpty(Skin.String(%s))' % setting if not value else 'String.IsEqual(Skin.String(%s),%s)' % (setting, value)
            o.append('<onclick condition="!%s">SetProperty(aeon.wiz.reload,1,home)</onclick>' % now)
        elif a.startswith('@tick:'):
            aid = a.split(':', 1)[1]
            o.append('<onclick condition="!System.HasAddon(%s)">Skin.ToggleSetting(aeon.wiz.add.%s)</onclick>' % (aid, aid))
        elif a.startswith('@install:'):
            aid = a.split(':', 1)[1]
            o.append('<onclick condition="!System.HasAddon(%s)">InstallAddon(%s)</onclick>' % (aid, aid))
        else:
            o.append('<onclick>%s</onclick>' % a)
    if step.key == 'welcome' and x['tok'] == 'start':
        o += next_clicks(i, known)
    elif step.advance and step.key not in ('welcome', 'start', 'done'):
        o += next_clicks(i, known)
    elif step.key == 'start' and x['tok'] == 'custom':
        o += next_clicks(i, known)
    return o


def picture(step, x):
    if x.get('icon') == '-':
        return ''
    if x.get('icon'):
        return x['icon']
    if step.pictures == 'theme':
        return SHOTS + '%s_%s_%s.jpg' % (THEME_NOW, step.key, x['tok'])
    if step.pictures:
        return SHOTS + '%s_%s.jpg' % (step.pictures, x['tok'])
    return ''


def list_xml(i, step):
    n = i + 1
    items = []
    for x in step.options:
        vis = '\t\t\t\t\t\t<visible>%s</visible>\n' % esc(x['visible']) if x.get('visible') else ''
        cur = x.get('cur') or ('$VAR[Wiz_Cur_%d]' % n if step.cur else '')
        items.append('\t\t\t\t\t<item>\n\t\t\t\t\t\t<label>%s</label>\n\t\t\t\t\t\t<label2>%s</label2>\n\t\t\t\t\t\t<icon>%s</icon>\n'
                     '\t\t\t\t\t\t<property name="val">%s</property>\n\t\t\t\t\t\t<property name="cur">%s</property>\n'
                     '\t\t\t\t\t\t<property name="more">%s</property>\n%s%s%s\t\t\t\t\t</item>'
                     % (x['label'], x['label2'], picture(step, x), x['tok'], cur, x['more'],
                        ''.join('\t\t\t\t\t\t<property name="%s">%s</property>\n' % kv for kv in sorted((x.get('props') or {}).items())), vis,
                        ''.join('\t\t\t\t\t\t%s\n' % c for c in item_clicks(i, step, x))))
    return ('\t\t<control type="list" id="%d"><!-- step %d: %s -->\n'
            '\t\t\t<left>110</left><top>430</top><width>660</width><height>540</height>\n'
            '\t\t\t<visible allowhiddenfocus="true">String.IsEqual(%s,%d)</visible>\n'
            '\t\t\t<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/><effect type="slide" start="0,30" end="0,0" time="260" tween="cubic" easing="out"/></animation>\n'
            '\t\t\t<onleft>noop</onleft><onright>noop</onright>\n'
            '%s'
            '\t\t\t<scrolltime tween="cubic" easing="out">200</scrolltime>\n'
            '\t\t\t<itemlayout width="660" height="108"><include content="Aeon_WizItem"/></itemlayout>\n'
            '\t\t\t<focusedlayout width="660" height="108"><include content="Aeon_WizItem"><param name="focused" value="true"/></include></focusedlayout>\n'
            '\t\t\t<content>\n%s\n\t\t\t</content>\n\t\t</control>\n'
            % (list_id(n), n, step.key, STEP, n, ''.join('\t\t\t%s\n' % b for b in onbacks(i)), '\n'.join(items)))


def palette_mock():
    """the palette step's preview: one Aeon library List view drawn in the focused palette's colours (the user: "one
    mockup and user could cycle through each option and it would update the mockup in realtime"), in the preview's
    place (840, 140, 960 x 540)"""
    lid = list_id(N['palette'])

    def col(k):
        return '$INFO[Container(%d).ListItem.Property(c_%s)]' % (lid, k)

    def box(x, y, w, h, c, tex='common/white.png', extra=''):
        return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>%s'
                '<texture colordiffuse="%s">%s</texture></control>' % (x, y, w, h, extra, c, tex))

    def text(x, y, w, h, label, c, font='st_small_20', align='left'):
        return ('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>%s</align>'
                '<aligny>center</aligny><font>%s</font><textcolor>%s</textcolor><label>%s</label></control>' % (x, y, w, h, align, font, c, label))
    o = ['\t\t\t<!-- the palette step: a live mock-up in the focused palette (_src/wizard_05640.py palette_mock) -->',
         '\t\t\t<control type="group"><left>840</left><top>140</top><visible>String.IsEqual(%s,%d)</visible>' % (STEP, N['palette']),
         box(0, 0, 960, 540, col('x_ground')),
         box(0, 0, 960, 540, '33ffffff', 'aeon/wizard/mock_fanart.jpg', '<aspectratio>scale</aspectratio>'),
         box(0, 0, 960, 540, '99000000'),
         text(32, 18, 400, 36, '[UPPERCASE]$LOCALIZE[20342][/UPPERCASE]', 'ccffffff', 'st_cap_20'),
         # the clock box in the corner
         box(864, 0, 96, 92, col('aeon_box')),
         text(864, 6, 96, 40, '$INFO[System.Time(hh)]', 'ffffffff', 'st_ui_28_semibold', 'center'),
         text(864, 44, 96, 40, '$INFO[System.Time(mm)]', 'b3ffffff', 'st_ui_28_semibold', 'center'),
         # the poster in its box, the list panel beside it
         box(32, 70, 250, 380, col('aeon_box')),
         box(37, 75, 240, 370, 'ffffffff', 'aeon/wizard/mock_poster.jpg'),
         box(300, 70, 548, 380, col('x_panel'))]
    rows = ('Lawless', 'Lawman', 'Lawn Dogs', 'Lawrence of Arabia', 'The Laws of Thermodynamics', 'Layer Cake', 'The Lazarus Project')
    for i, name in enumerate(rows):
        y = 74 + i * 53
        if name == 'Lawrence of Arabia':
            o.append(box(300, y, 548, 52, col('aeon_white')))
            o.append(text(326, y, 420, 52, '[UPPERCASE]%s[/UPPERCASE]' % name, col('aeon_onbar'), 'st_ui_22_bold'))
            o.append(text(740, y, 90, 52, '3:47', col('aeon_onbar'), 'st_ui_22_bold', 'right'))
        else:
            if i % 2:
                o.append(box(300, y, 548, 52, col('x_raised')))
            o.append(text(326, y, 420, 52, '[UPPERCASE]%s[/UPPERCASE]' % name, 'e6ffffff', 'st_ui_22'))
            o.append(box(300, y + 52, 548, 1, col('x_line')))
    # the strip box and the info line under the list
    o.append(box(864, 448, 96, 92, col('aeon_box')))
    o.append(text(32, 462, 816, 34, '1962  ·  3:47  ·  8.3', 'ccffffff', 'st_small_20_semibold'))
    o.append(box(32, 500, 120, 6, col('aeon_white')))
    o.append('\t\t\t</control>\n')
    return '\n'.join(o)


# ---------------------------------------------------------------------------------------------------------- window
def window():
    w = old('Custom_1173_SetupWizard.xml')
    head = w[:w.index('\t\t<control type="list" id="9101">')]
    tail = w[w.index('\t\t\t<!-- the preview of the focused option (from step 2) -->'):]
    head = re.sub(r'<!-- Setup wizard \(dialog 1173\)\. GENERATED.*?-->',
                  '<!-- Setup wizard (dialog 1173). GENERATED by _src/wizard_05640.py - edit the generator, not this file.\n'
                  '     The original look, one setting per step (Window(Home).Property(aeon.wiz.step) = the step number, list 9100 + step).\n'
                  '     Opened by RunScript(script.aeon.helper,wizard,open). Theme, Skin style, palette, fonts and the focus\n'
                  '     highlight wait for Finish (RunScript(script.aeon.helper,wizard)); the rest changes at once. -->', head, count=1, flags=re.S)
    assert 'wizard_05640' in head
    # the progress dots: one per step, the steps of other themes hidden
    s = tail.index('\t\t\t<control type="grouplist"><left>110</left><top>1000</top>')
    e = tail.index('\t\t\t</control>\n', s) + len('\t\t\t</control>\n')
    dots = ['\t\t\t<control type="grouplist"><left>110</left><top>1000</top><width>660</width><height>14</height><orientation>horizontal</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>']
    for i, step in enumerate(STEPS):
        n = i + 1
        c = cond_of(step.when)
        vis = '' if c is True else '<visible>%s</visible>' % esc(c)
        dots.append('\t\t\t\t<control type="group"><width>24</width><height>14</height>%s'
                    '<control type="image"><left>0</left><top>1</top><width>12</width><height>12</height><texture colordiffuse="33ffffff">aeon/circle_12.png</texture><visible>!String.IsEqual(%s,%d) + !Integer.IsGreater(%s,%d)</visible></control>'
                    '<control type="image"><left>0</left><top>1</top><width>12</width><height>12</height><texture colordiffuse="99ffffff">aeon/circle_12.png</texture><visible>Integer.IsGreater(%s,%d)</visible></control>'
                    '<control type="image"><left>-1</left><top>0</top><width>14</width><height>14</height><texture colordiffuse="$VAR[Aeon_WizAccent]">aeon/circle_12.png</texture><visible>String.IsEqual(%s,%d)</visible></control></control>'
                    % (vis, STEP, n, STEP, n, STEP, n, STEP, n))
    dots.append('\t\t\t</control>\n')
    tail = tail[:s] + palette_mock() + '\n'.join(dots) + tail[e:]
    lists = ''.join(list_xml(i, st) for i, st in enumerate(STEPS))
    return head + lists + tail


# ---------------------------------------------------------------------------------------------------------- includes
def var(name, values, default=None):
    o = ['\t<variable name="%s">' % name]
    for c, v in values:
        o.append('\t\t<value condition="%s">%s</value>' % (esc(c), v))
    if default is not None:
        o.append('\t\t<value>%s</value>' % default)
    o.append('\t</variable>')
    return '\n'.join(o)


def includes():
    inc = old('Includes_Aeon_Wizard.xml')
    keep = re.findall(r'\t<variable name="Aeon_WizMenu_\w+">.*?</variable>', inc, re.S)
    assert len(keep) == 14
    look = []
    for name in ('Aeon_WizCardF', 'Aeon_WizInk', 'Aeon_WizInk3', 'Aeon_WizAccent'):
        v = re.search(r'\t<variable name="%s">.*?</variable>' % name, inc, re.S).group(0)
        # the palette step recolours the wizard's own cards (the step number and list changed)
        v = v.replace('String.IsEqual(Window(Home).Property(aeon.wiz.step),3)', 'String.IsEqual(%s,%d)' % (STEP, N['palette']))
        v = v.replace('Container(9103)', 'Container(%d)' % list_id(N['palette']))
        look.append(v)
    item = re.search(r'\t<include name="Aeon_WizItem">.*?</include>', inc, re.S).group(0)
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<!-- Setup wizard (dialog 1173): GENERATED by _src/wizard_05640.py - edit the generator, not this file. -->',
         '<includes>']
    per = lambda f: [('String.IsEqual(%s,%d)' % (STEP, n), f(n, st)) for n, st in enumerate(STEPS, 1)]   # noqa: E731
    o.append(var('Aeon_WizCap', per(lambda n, st: '[UPPERCASE]%s[/UPPERCASE]' % st.cap)))
    o.append(var('Aeon_WizTitle', per(lambda n, st: st.title)))
    o.append(var('Aeon_WizText', per(lambda n, st: st.text)))
    o.append(var('Aeon_WizPreview', per(lambda n, st: '$INFO[Container(%d).ListItem.Icon]' % list_id(n))))
    o.append(var('Aeon_WizMore', per(lambda n, st: '$INFO[Container(%d).ListItem.Property(more)]' % list_id(n))))
    o.append(var('Aeon_WizFocusName', per(lambda n, st: '$INFO[Container(%d).ListItem.Label]' % list_id(n))))
    # the value in use (the card with the check) and its place (the card that has the focus when the step opens)
    for n, st in enumerate(STEPS, 1):
        if st.cur:
            vals = [(c, t) for c, t in st.cur if c]
            o.append(var('Wiz_Cur_%d' % n, vals, [t for c, t in st.cur if c is None][0]))
        toks = [x['tok'] for x in st.options]
        pos = []
        if st.key == 'palette':
            pos = [('!String.IsEmpty(%s)' % P('palidx'), '$INFO[%s]' % P('palidx'))]
        elif st.cur and st.key not in ('fonts',):
            for c, t in st.cur:
                if c and t in toks and toks.index(t):
                    pos.append((c, '$NUMBER[%d]' % toks.index(t)))
            d = [t for c, t in st.cur if c is None][0]
            if d in toks and toks.index(d) and not any(t == d for c, t in st.cur if c):
                o.append(var('Wiz_Pos_%d' % n, pos, '$NUMBER[%d]' % toks.index(d)))
                continue
        elif st.key == 'fonts':
            pos = [('String.IsEqual(%s,%s)' % (P('fontkey'), key), '$NUMBER[%d]' % k) for k, (key, _name) in enumerate(FONTS) if k]
        o.append(var('Wiz_Pos_%d' % n, pos, '$NUMBER[0]'))
    # add-ons: installed or not
    ticked = []
    for aid, _name in ADDONS:
        k = aid.replace('.', '_')
        o.append(var('Wiz_Addon_%s' % k, [('System.HasAddon(%s)' % aid, L(35257)),
                                           ('Skin.HasSetting(aeon.wiz.add.%s)' % aid, A(S_WILL_INSTALL))], A(32765)))
        o.append(var('Wiz_AddonOn_%s' % k, [('System.HasAddon(%s) | Skin.HasSetting(aeon.wiz.add.%s)' % (aid, aid), 'on')], 'off'))
        ticked.append('[Skin.HasSetting(aeon.wiz.add.%s) + !System.HasAddon(%s)]' % (aid, aid))
    o.append(var('Wiz_AddonsNext', [(' | '.join(ticked), A(32793))], ''))
    # Finish: does the skin have to load again (theme, Skin style, palette, fonts, focus highlight)?
    mt, fm = P('menutheme'), P('fgmenu')
    theme_changed = ('[String.IsEqual({t},fused) + !Skin.HasSetting(aeon.fglass)] | [String.IsEqual({t},glass) + ![Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)]] | '
                     '[String.IsEqual({t},aeon) + Skin.HasSetting(aeon.vglass)]').format(t=P('theme'))
    fg_changed = ' | '.join('[%s + !%s]' % (a, b) for a, b in (
        ('String.IsEmpty(%s)' % fm, 'String.IsEmpty(Skin.String(aeon.fgmenu))'),
        ('String.IsEqual(%s,glass)' % fm, 'String.IsEqual(Skin.String(aeon.fgmenu),glass)'),
        ('String.IsEqual(%s,frost)' % fm, 'String.IsEqual(Skin.String(aeon.fgmenu),frost)'),
        ('String.IsEqual(%s,system)' % fm, 'String.IsEqual(Skin.String(aeon.fgmenu),system)')))
    ms_changed = ' | '.join('[%s + !%s]' % (a, b) for a, b in (
        ('[String.IsEmpty(%s) | String.IsEqual(%s,bridge)]' % (mt, mt), '[String.IsEmpty(Skin.String(aeon.menutheme)) | String.IsEqual(Skin.String(aeon.menutheme),bridge)]'),
        ('String.IsEqual(%s,mosaic)' % mt, 'String.IsEqual(Skin.String(aeon.menutheme),mosaic)'),
        ('String.IsEqual(%s,ledger)' % mt, 'String.IsEqual(Skin.String(aeon.menutheme),ledger)'),
        ('String.IsEqual(%s,tabslab)' % mt, 'String.IsEqual(Skin.String(aeon.menutheme),tabslab)'),
        ('String.IsEqual(%s,fused)' % mt, 'String.IsEqual(Skin.String(aeon.menutheme),fused)')))
    glass_changed = '[String.IsEqual(%s,fused) + !String.IsEqual(Skin.String(aeon.menutheme),fused)] | [!String.IsEqual(%s,fused) + String.IsEqual(Skin.String(aeon.menutheme),fused)]' % (mt, mt)
    restart = ('[%s] | [String.IsEqual(%s,fused) + [%s]] | [String.IsEqual(%s,aeon) + [%s]] | [String.IsEqual(%s,glass) + [%s]] | '
               '!String.IsEmpty(%s) | !String.IsEmpty(%s) | !String.IsEmpty(%s)'
               % (theme_changed, P('theme'), fg_changed, P('theme'), ms_changed, P('theme'), glass_changed,
                  P('palchanged'), P('fontchanged'), P('reload')))
    o.append('\t<expression name="Aeon_WizRestart">%s</expression>' % esc(restart))
    plat = 'System.Platform.Linux + !System.Platform.Android'
    o.append(var('Wiz_FinishHint', [('$EXP[Aeon_WizRestart] + ' + plat, A(32276)), ('$EXP[Aeon_WizRestart]', A(32277))], A(32278)))
    o.append(var('Wiz_FinishMore', [('$EXP[Aeon_WizRestart] + ' + plat, A(32279)), ('$EXP[Aeon_WizRestart]', A(32280))], A(32281)))
    o.extend(keep)
    o.extend(look)
    o.append(item)
    o.append('</includes>')
    return '\n'.join(o) + '\n'


def pictures_needed():
    """[(picture path in media, step key, token, theme or '')] for the screenshot session"""
    out = []
    for st in STEPS:
        for x in st.options:
            p = picture(st, x)
            if not p.startswith(SHOTS):
                continue
            if THEME_NOW in p:
                for t in ('fused', 'aeon', 'glass'):
                    c = cond_of(st.when, {'theme': t})
                    if c is not False:
                        out.append((p.replace(THEME_NOW, t), st.key, x['tok'], t))
            else:
                out.append((p, st.key, x['tok'], ''))
    seen, uniq = set(), []
    for row in out:
        if row[0] not in seen:
            seen.add(row[0])
            uniq.append(row)
    return uniq


def main():
    wr('Includes_Aeon_Wizard.xml', includes())
    wr('Custom_1173_SetupWizard.xml', window())
    print('steps:', ', '.join('%d %s' % (n, s.key) for n, s in enumerate(STEPS, 1)))
    need = pictures_needed()
    media = os.path.join(HERE, '..', 'media')
    missing = [p for p, _k, _t, _th in need if not os.path.isfile(os.path.join(media, p))]
    io.open(os.path.join(HERE, 'wizard_pictures.json'), 'w', encoding='utf-8').write(json.dumps(need, indent=0))
    print('pictures: %d, missing %d' % (len(need), len(missing)))


if __name__ == '__main__':
    main()
