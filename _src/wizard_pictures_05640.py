# -*- coding: utf-8 -*-
"""0.56.40 the setup wizard's pictures (media/aeon/wizard, 960 x 540 like the old ones):
- theme_<theme>.jpg: Home in each theme (box shots of 0.56.37, skin.glass/mockups/menus-system-style/box05637);
- shots/<name>.jpg: the box screenshots of every option (scratchpad session05640b.py; the 1920 x 1080 PNGs are kept in
  skin.glass/mockups/setup-wizard/shots05640);
- shots/font_<key>.jpg: each font combination over Lawrence of Arabia's fanart, the heading face for the title and the
  text face under it (the skin's own font files); no words that would need translating;
- shots/addon_<id>.jpg: the add-on's icon and name over the same fanart, blurred.
Run from the skin folder after the screenshots are in. Repeatable."""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN = os.path.join(HERE, '..')
ADDONS = os.path.join(SKIN, '..')
MOCK = os.path.join(ADDONS, 'skin.glass', 'mockups')
OUT = os.path.join(SKIN, 'media', 'aeon', 'wizard')
SHOTS = os.path.join(OUT, 'shots')
RAW = os.path.join(MOCK, 'setup-wizard', 'shots05640')
FANART = os.path.join(HERE, 'wizard_art', 'lawrence_fanart.jpg')
FONTS = os.path.join(SKIN, 'fonts')
W, H = 960, 540

# key: (heading file, text file) as fonts.PRESETS pairs them ('' text = Figtree, the font set's)
PAIRS = {'figtree': ('Figtree-Bold.ttf', 'Figtree-Regular.ttf'), 'fraunces': ('Fraunces-Bold.ttf', 'Figtree-Regular.ttf'),
         'bebas': ('BebasNeue-Regular.ttf', 'Figtree-Regular.ttf'), 'oswald': ('Oswald-SemiBold.ttf', 'AeonSSans-Regular.ttf'),
         'barlowc': ('BarlowCondensed-Bold.ttf', 'Barlow-Regular.ttf'), 'funnel': ('FunnelDisplay-ExtraBold.ttf', 'Figtree-Regular.ttf'),
         'calsans': ('CalSans-SemiBold.ttf', 'Figtree-Regular.ttf'), 'hubotc': ('HubotSansCondensed-ExtraBold.ttf', 'HubotSans-Regular.ttf'),
         'hubote': ('HubotSansExpanded-Bold.ttf', 'Figtree-Regular.ttf'), 'sairac': ('SairaCondensed-Bold.ttf', 'Saira-Regular.ttf'),
         'clarity': ('ClarityCity-Bold.ttf', 'PretendardStd-Regular.ttf'), 'gnomon': ('Gnomon-Simple.ttf', 'ClarityCity-Regular.ttf')}
ADDON_IDS = ('plugin.video.themoviedb.helper', 'script.embuary.helper', 'script.cu.lrclyrics', 'script.artistslideshow',
             'script.karmamole.helper', 'resource.images.studios.white', 'resource.images.recordlabels.white',
             'resource.images.languageflags.colour', 'screensaver.aeon.fuse', 'service.skippy', 'service.trickplay')
NAMES = {'plugin.video.themoviedb.helper': 'TMDb Helper', 'script.embuary.helper': 'Embuary Helper',
         'script.cu.lrclyrics': 'CU LRC Lyrics', 'script.artistslideshow': 'Artist Slideshow',
         'script.karmamole.helper': 'KarmaMole Skin Helper', 'resource.images.studios.white': 'Studio Icons - White',
         'resource.images.recordlabels.white': 'Recordlabel Icons - White',
         'resource.images.languageflags.colour': 'Language Flags Colour', 'screensaver.aeon.fuse': 'Aeon Fuse Screensaver',
         'service.skippy': 'Skippy - Video Segment Skipper', 'service.trickplay': 'Trickplay Preview'}


def save(im, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.convert('RGB').save(path, quality=86, optimize=True)


def fanart(blur=0, dim=0.55):
    im = Image.open(FANART).convert('RGB').resize((W, H), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    veil = Image.new('RGB', (W, H), (8, 9, 12))
    im = Image.blend(im, veil, dim)
    # a darker left side for the text, as the skin's views do
    grad = Image.linear_gradient('L').rotate(90).resize((W, H))
    left = Image.new('RGB', (W, H), (6, 7, 10))
    return Image.composite(im, left, grad.point(lambda v: min(255, 60 + v)))


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def fonts():
    for key, (head, text) in PAIRS.items():
        im = fanart()
        d = ImageDraw.Draw(im)
        d.text((60, 300), 'Lawrence of Arabia', font=font(head, 66), fill=(255, 255, 255))
        d.text((62, 392), '1962   ·   3:48   ·   8.3', font=font(text, 28), fill=(230, 230, 230))
        d.text((62, 440), 'Aa Bb Cc Dd Ee   0123456789', font=font(text, 24), fill=(190, 190, 190))
        save(im, os.path.join(SHOTS, 'font_%s.jpg' % key))


def addons():
    for aid in ADDON_IDS:
        im = fanart(blur=18, dim=0.62)
        icon = None
        for rel in ('icon.png', os.path.join('resources', 'icon.png'), os.path.join('resources', 'media', 'icon.png')):
            p = os.path.join(ADDONS, aid, rel)
            if os.path.isfile(p):
                icon = Image.open(p).convert('RGBA').resize((200, 200), Image.LANCZOS)
                break
        if icon:
            im.paste(icon, ((W - 200) // 2, 118), icon)
        d = ImageDraw.Draw(im)
        f = font('Figtree-Bold.ttf', 40)
        name = NAMES[aid]
        w = d.textlength(name, font=f)
        d.text(((W - w) / 2, 352), name, font=f, fill=(255, 255, 255))
        save(im, os.path.join(SHOTS, 'addon_%s.jpg' % aid))


def themes():
    """the List library view of each theme on Lawrence of Arabia with the Fanart background (the user, 2026-11-18: Home
    looks the same in all three; show the List view)"""
    for path, k in ((os.path.join(MOCK, 'fanart-glass-combos', 'box05626', 'dimmedfan_darkglass.png'), 'fused'),
                    (os.path.join(RAW, 'aeon_libbg_fanart.png'), 'aeon'), (os.path.join(RAW, 'glass_libbg_fanart.png'), 'glass')):
        save(Image.open(path).resize((W, H), Image.LANCZOS), os.path.join(OUT, 'theme_%s.jpg' % k))


def shots():
    if not os.path.isdir(RAW):
        print('no screenshots in', RAW)
        return 0
    n = 0
    for f in sorted(os.listdir(RAW)):
        if f.endswith('.png'):
            save(Image.open(os.path.join(RAW, f)).resize((W, H), Image.LANCZOS), os.path.join(SHOTS, f[:-4] + '.jpg'))
            n += 1
    return n


def main():
    themes()
    fonts()
    addons()
    print('shots', shots())
    if '--check' in sys.argv:
        import json
        need = json.load(open(os.path.join(HERE, 'wizard_pictures.json')))
        missing = [p for p, _k, _t, _th in need if not os.path.isfile(os.path.join(SKIN, 'media', p))]
        print('missing', len(missing), missing)


if __name__ == '__main__':
    main()
