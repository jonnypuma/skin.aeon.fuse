# -*- coding: utf-8 -*-
"""0.56.53 setup wizard, Recommended add-ons step: media/aeon/wizard/shots/addfeat_<add-on id>.jpg (960x540), what each
add-on adds, from real box shots (skin.glass/mockups/settings-review/box05653b.py -> box05653b/raw/<key>.png): the part
of the screen that add-on fills, cut to 16:9 and scaled. The two font packs are drawn with their own font files over
the fanart of the font pictures. Run from anywhere; a missing raw shot is skipped (said so)."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wizard_pictures_05640 as wp  # noqa: E402

SKIN = os.path.join(HERE, '..')
SHOTS = os.path.join(SKIN, 'media', 'aeon', 'wizard', 'shots')
RAW = os.path.join(SKIN, '..', 'skin.glass', 'mockups', 'settings-review', 'box05653b', 'raw')
FONTDIR = os.path.join(SKIN, '..', 'skin.glass', 'mockups', 'settings-review', 'box05653b', 'fonts')
COPA = os.path.join(SKIN, '..', 'resource.fonts.copacetic', 'resources')
W, H = 960, 540

# add-on id -> (raw shot, crop box in the 1920x1080 shot: left, top, width; height follows 16:9)
CROPS = {
    'plugin.video.themoviedb.helper': ('tmdbhelper', (0, 40, 1360)),       # the Planner
    'script.karmamole.helper': ('karmamole', (0, 0, 1920)),                # box colours from the artwork
    'resource.images.studios.white': ('studios_flags', (360, 120, 1560)),  # info page: studio logo
    'resource.images.languageflags.colour': ('flags', (980, 150, 920)),       # player info: audio / subtitle languages
    'resource.images.recordlabels.white': ('recordlabels_view', (1140, 620, 680)),  # album view: the label's logo
    'resource.images.weathericons.white': ('weathericons', (300, 160, 1600)),
    'script.embuary.helper': ('embuary', (0, 0, 1920)),                    # the shows-in-progress / Next up row
    'script.cu.lrclyrics': ('lyrics', (0, 0, 1920)),
    'script.artistslideshow': ('lyrics', (0, 0, 1280)),                    # the artist picture behind Now playing
    'screensaver.aeon.fuse': ('screensaver', (0, 0, 1920)),
    'service.skippy': ('skippy', (900, 500, 1000)),
    'service.trickplay': ('trickplay', (480, 420, 1120)),
    'script.tinyppi': ('trickplay', (1100, 620, 800)),                     # the playback info button in the controls
}


def cut(aid, key, box):
    p = os.path.join(RAW, key + '.png')
    if not os.path.isfile(p):
        print('  missing raw shot', key, 'for', aid)
        return
    im = Image.open(p).convert('RGB')
    x, y, w = box
    h = int(round(w * 9 / 16.0))
    im = im.crop((x, y, x + w, y + h)).resize((W, H), Image.LANCZOS)
    wp.save(im, os.path.join(SHOTS, 'addfeat_%s.jpg' % aid))


def drawn_fonts():
    # Copacetic: Inter in the skin's heading / text sizes
    head = os.path.join(COPA, 'Inter-NotoSansKR-Bold.ttf')
    text = os.path.join(COPA, 'Inter-NotoSansKR-Light.ttf')
    if os.path.isfile(head):
        im = wp.fanart()
        d = ImageDraw.Draw(im)
        d.text((60, 300), 'Lawrence of Arabia', font=ImageFont.truetype(head, 66), fill=(255, 255, 255))
        d.text((62, 392), '1962   ·   3:48   ·   8.3', font=ImageFont.truetype(text, 28), fill=(230, 230, 230))
        d.text((62, 440), 'Inter (Copacetic)   Aa Bb Cc 0123', font=ImageFont.truetype(text, 24), fill=(190, 190, 190))
        wp.save(im, os.path.join(SHOTS, 'addfeat_resource.fonts.copacetic.jpg'))
    else:
        print('  Copacetic fonts not beside the skin')
    # Roboto CJKSC: Chinese, Japanese and Korean titles the default fonts draw as boxes
    head = os.path.join(FONTDIR, 'RobotoCJKSC-Bold.ttf')
    text = os.path.join(FONTDIR, 'RobotoCJKSC-Light.ttf')
    if os.path.isfile(head):
        im = wp.fanart()
        d = ImageDraw.Draw(im)
        d.text((60, 250), u'アラビアのロレンス', font=ImageFont.truetype(head, 60), fill=(255, 255, 255))
        d.text((62, 340), u'阿拉伯的劳伦斯   ·   아라비아의 로렌스', font=ImageFont.truetype(text, 32), fill=(230, 230, 230))
        d.text((62, 400), u'1962   ·   3:48   ·   中文 / 日本語 / 한국어', font=ImageFont.truetype(text, 24), fill=(190, 190, 190))
        wp.save(im, os.path.join(SHOTS, 'addfeat_resource.font.robotocjksc.jpg'))
    else:
        print('  Roboto CJKSC fonts not copied (box05653b/fonts)')


def main():
    for aid, (key, box) in sorted(CROPS.items()):
        cut(aid, key, box)
    drawn_fonts()
    print('addfeat pictures in', SHOTS)


if __name__ == '__main__':
    main()
