# -*- coding: utf-8 -*-
"""0.56.9 Add-on category icons: Kodi names an icon for every add-on category and menu entry of the add-on browser
(DefaultAddonVideo.png, DefaultAddonContextItem.png, DefaultAddonsRepo.png ...) and a skin supplies them; the skin had
none, so the category rows showed a blank square and the side panel one generic tile. The user (2026-11-16): "use some
icons for the addon categories, we have that (video add-ons, context menus etc)".

Each icon is a dark tile (an add-on icon's shape, so the masks round it as they round real add-on icons, and it shows
on the white focus bar too) with the matching white glyph of Font Awesome Free. 0.56.10: the glyphs are drawn from the
font at 512 px, so they stay sharp in the add-on browser's 200 px panel (0.56.9 upscaled 128 px PNGs; the user: "that is
one mangled icon. please make a good one or find a free one online"). Font Awesome Free 6 (https://fontawesome.com):
icons CC BY 4.0, font SIL OFL 1.1; only the rendered PNGs ship (media/DefaultAddon-icons.txt says so).
Also the masks of the add-on browser's Fused Glass panel. Run from the skin folder; safe to run again."""
import os

from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir,
                    'skin.arctic.fuse.3.ce-mod', 'fonts', 'fa-solid-900.ttf')
OUT = 'media'
ICONS = {
    'DefaultAddon.png': 0xf12e, 'DefaultAddonNone.png': 0xf12e,                        # puzzle-piece
    'DefaultAddonAlbumInfo.png': 0xf51f, 'DefaultAddonArtistInfo.png': 0xf130,         # compact-disc, microphone
    'DefaultAddonAudioDecoder.png': 0xf1c7, 'DefaultAddonAudioEncoder.png': 0xf1c7,    # file-audio
    'DefaultAddonContextItem.png': 0xf142, 'DefaultAddonFont.png': 0xf031,             # ellipsis-vertical, font
    'DefaultAddonGame.png': 0xf11b, 'DefaultAddonHelper.png': 0xf7d9,                  # gamepad, screwdriver-wrench
    'DefaultAddonImageDecoder.png': 0xf1c5, 'DefaultAddonImages.png': 0xf302,          # file-image, images
    'DefaultAddonInfoLibrary.png': 0xf1c0, 'DefaultAddonInfoProvider.png': 0xf05a,     # database, circle-info
    'DefaultAddonInputstream.png': 0xf144, 'DefaultAddonLanguage.png': 0xf1ab,         # circle-play, language
    'DefaultAddonLibrary.png': 0xf121, 'DefaultAddonLookAndFeel.png': 0xf53f,          # code, palette
    'DefaultAddonLyrics.png': 0xf3c9, 'DefaultAddonMovieInfo.png': 0xf008,             # microphone-lines, film
    'DefaultAddonMusic.png': 0xf001, 'DefaultAddonMusicVideoInfo.png': 0xf03d,         # music, video
    'DefaultAddonPVRClient.png': 0xf26c, 'DefaultAddonPeripheral.png': 0xf1e6,         # tv, plug
    'DefaultAddonPicture.png': 0xf03e, 'DefaultAddonProgram.png': 0xf1b3,              # image, cubes
    'DefaultAddonRepository.png': 0xf187, 'DefaultAddonScreensaver.png': 0xf186,       # box-archive, moon
    'DefaultAddonService.png': 0xf085, 'DefaultAddonSkin.png': 0xf1fc,                 # gears, paintbrush
    'DefaultAddonSubtitles.png': 0xf20a, 'DefaultAddonTvInfo.png': 0xf26c,             # closed-captioning, tv
    'DefaultAddonUISounds.png': 0xf025, 'DefaultAddonVfs.png': 0xf1c0,                 # headphones, database
    'DefaultAddonVideo.png': 0xf03d, 'DefaultAddonVisualization.png': 0xf83e,          # video, wave-square
    'DefaultAddonWeather.png': 0xf6c4, 'DefaultAddonWebSkin.png': 0xf0ac,              # cloud-sun, globe
    'DefaultAddonsInstalled.png': 0xf49e, 'DefaultAddonsRecentlyUpdated.png': 0xf1da,  # box-open, clock-rotate-left
    'DefaultAddonsRepo.png': 0xf0ed, 'DefaultAddonsSearch.png': 0xf002,                # cloud-arrow-down, magnifying-glass
    'DefaultAddonsUpdates.png': 0xf021, 'DefaultAddonsZip.png': 0xf1c6,                # arrows-rotate, file-zipper
}
SIZE = 512


def tile(code, dst, font):
    """a square dark tile (top a little lighter) with the white glyph, half the tile, in the middle"""
    base = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 255))
    d = ImageDraw.Draw(base)
    for y in range(SIZE):                          # #2c313c at the top to #171a21 at the bottom
        f = y / (SIZE - 1.0)
        c = tuple(int(a + (b - a) * f) for a, b in zip((44, 49, 60), (23, 26, 33)))
        d.line([(0, y), (SIZE, y)], fill=c + (255,))
    m = font.getmask(chr(code), mode='L')
    g = Image.frombytes('L', m.size, bytes(m))
    g = g.crop(g.getbbox())
    side = int(SIZE * 0.5)
    k = side / float(max(g.size))
    g = g.resize((max(1, round(g.size[0] * k)), max(1, round(g.size[1] * k))), Image.LANCZOS)
    white = Image.new('RGBA', g.size, (255, 255, 255, 255))
    white.putalpha(g.point(lambda v: int(v * 0.94)))
    base.alpha_composite(white, ((SIZE - g.size[0]) // 2, (SIZE - g.size[1]) // 2))
    base.convert('RGB').save(dst, optimize=True)


def mask(w, h, r):
    p = os.path.join('media', 'fg', 'm%dx%d.png' % (w, h))
    ss = 4
    a = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(a).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255)
    im = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    im.putalpha(a.resize((w, h), Image.LANCZOS))
    im.save(p, optimize=True)


if __name__ == '__main__':
    font = ImageFont.truetype(os.path.normpath(FONT), 400)
    for name, code in sorted(ICONS.items()):
        tile(code, os.path.join(OUT, name), font)
    for w, h, r in ((500, 281, 28), (120, 120, 22), (156, 88, 12), (488, 274, 12), (152, 86, 10)):
        mask(w, h, r)
    with open(os.path.join(OUT, 'DefaultAddon-icons.txt'), 'w') as handle:
        handle.write('media/DefaultAddon*.png: glyphs of Font Awesome Free 6 (https://fontawesome.com), icons licensed CC BY 4.0,\n'
                     'font SIL OFL 1.1; drawn on tiles by _src/addon_icons.py.\n')
    print('%d add-on icons, 5 masks' % len(ICONS))
