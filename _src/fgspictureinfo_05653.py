# -*- coding: utf-8 -*-
"""0.56.53 Picture info in the Fused Glass style (canvas round 2 PictureInfo2, "so good. build that"): the picture full
screen (the slideshow itself when it is behind), a gradient from the right, at the right the date taken in the accent,
the file name, the picture's place in the slideshow, the exposure as four big numbers like a camera's top display
(aperture, shutter, ISO, focal length: Kodi's own strings), then Kodi's detail list 5 as 62 px rows with the style's bar
and its scroll bar 60 in the gutter. Left / Right still step to the previous / next picture (Kodi's contract).
Not built: the filmstrip of the folder (the dialog cannot read the slideshow's pictures). Repeatable."""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

NAME = 'PicInfo'


def textures():
    src = Image.open(os.path.join(fw.SKIN, 'media', 'fg', 'fgs_vi_l.png'))
    src.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(fw.SKIN, 'media', 'fg', 'fgs_vi_r.png'))


def row(focused):
    bar = (fw.img(-40, -34, 679, 142, 'fg/sh16.png', '$VAR[FG_ShadowColM]', 'Control.HasFocus(5) + $EXP[FGS_ShadowOn]', '') .replace('<texture colordiffuse', '<texture border="56" colordiffuse') +
           fw.img(0, 0, 599, 62, 'fg/fgs_bar_dk.png', 'ffffffff', 'Control.HasFocus(5)').replace('<texture colordiffuse', '<texture border="20" colordiffuse')) if focused else ''
    return (bar + fw.img(0, 61, 599, 1, 'common/white.png', '14ffffff') +
            fw.label(24, 0, 250, 62, '$INFO[ListItem.Label]', 'st_small_20', '8cffffff') +
            fw.label(280, 0, 295, 62, '$INFO[ListItem.Label2]', 'st_small_20_semibold', 'ffffffff' if focused else 'e6ffffff', 'right'))


def strip_item(focused_unused=False):
    return ('<control type="image"><left>6</left><top>6</top><width>112</width><height>74</height><texture border="8" colordiffuse="1fffffff">fg/r8.png</texture></control>'
            '<control type="image"><left>6</left><top>6</top><width>112</width><height>74</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m112x74.png">$INFO[ListItem.Art(thumb)]</texture></control>'
            '<control type="image"><left>6</left><top>6</top><width>112</width><height>74</height><texture border="8" colordiffuse="99000000">fg/r8.png</texture>'
            '<visible>String.IsEmpty(ListItem.Property(aeon.current))</visible></control>'
            '<control type="image"><left>3</left><top>3</top><width>118</width><height>80</height><texture border="15" colordiffuse="ffffffff">fg/ring12.png</texture>'
            '<visible>!String.IsEmpty(ListItem.Property(aeon.current))</visible></control>')


STRIP = ('<control type="list" id="9301"><left>120</left><top>868</top><width>1040</width><height>90</height><orientation>horizontal</orientation>'
         '<itemlayout width="124" height="90">%s</itemlayout><focusedlayout width="124" height="90">%s</focusedlayout>'
         '<content>plugin://script.aeon.helper/?info=picstrip&amp;i=$INFO[Slideshow.SlideIndex]</content></control>')


def page():
    expo = (('21826', 'ListItem.PictureAperture'), ('21830', 'ListItem.PictureExposureTime'), ('21837', 'ListItem.PictureISO'), ('21827', 'ListItem.PictureFocalLen'))
    cells = ''
    for k, (key, info) in enumerate(expo):
        x = 1200 + k * 155
        cells += fw.label(x, 318, 155, 70, '$INFO[%s]' % info, 'st_ui_30_semibold', 'ffffffff', 'center')
        cells += fw.label(x, 388, 155, 30, '[UPPERCASE]$LOCALIZE[%s][/UPPERCASE]' % key, 'st_cap_14', '80ffffff', 'center')
        cells += fw.line(x, 310, 1, 120)
    cells += fw.line(1820, 310, 1, 120) + fw.line(1200, 310, 620) + fw.line(1200, 430, 620)
    return (
        '<include name="PicInfo_PageFGS">'
        '<control type="group"><visible>!Window.IsActive(slideshow)</visible>'
        + fw.img(0, 0, 1920, 1080, 'common/white.png', 'ff08090c') +
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>200</fadetime>'
        '<texture background="true">$INFO[ListItem.FolderPath]</texture></control></control>'
        + fw.img(0, 0, 1920, 1080, 'fg/fgs_vi_r.png') + fw.header('$LOCALIZE[1]', '$LOCALIZE[13406]') +
        fw.label(1200, 140, 620, 30, '[UPPERCASE]$INFO[ListItem.PictureDateTime][/UPPERCASE]', 'st_small_20_bold', 'fg_mark') +
        fw.label(1200, 172, 620, 60, '$VAR[PicInfo_Name]', 'st_ui_30_semibold', 'ffffffff', extra='<scroll>true</scroll>') +
        fw.label(1200, 232, 620, 34, '$INFO[Slideshow.SlideIndex,,  ·  ]$INFO[ListItem.PictureResolution]', 'st_small_20', 'a6ffffff') +
        cells +
        '<control type="group" id="9000">'
        '<control type="list" id="5"><left>1200</left><top>460</top><width>599</width><height>496</height><orientation>vertical</orientation>'
        '<onleft>Dialog.Close(all,true)</onleft><onleft>Action(left)</onleft><onleft>info</onleft>'
        '<onright condition="Control.IsVisible(60)">60</onright>'
        '<onright condition="!Control.IsVisible(60)">Dialog.Close(all,true)</onright><onright condition="!Control.IsVisible(60)">Action(right)</onright><onright condition="!Control.IsVisible(60)">info</onright>'
        '<onup>5</onup><ondown>5</ondown><pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<itemlayout width="599" height="62">%s</itemlayout><focusedlayout width="599" height="62">%s</focusedlayout></control>'
        '%s</control>' % (row(False), row(True), fw.gutter_bar('60', 1801, 460, 496, '5', '5') + fw.line(1800, 460, 1, 496) + fw.line(1820, 460, 1, 496)) +
        STRIP % (strip_item(), strip_item()) +
        fw.label(1200, 980, 620, 30, '$LOCALIZE[31234]', 'st_small_20', '73ffffff', vis='false') +
        '</include>')


def main():
    textures()
    fw.wrap('DialogPictureInfo.xml', NAME)
    import io
    w = os.path.join(fw.D, 'DialogPictureInfo.xml')
    t = io.open(w, encoding='utf-8').read()
    if 'aeon.pic.path' not in t:
        t = t.replace('<include>Anim_DialogOpenClose</include>', '<onload>SetProperty(aeon.pic.path,$ESCINFO[ListItem.FolderPath],home)</onload>\n\t'
                      '<onunload>ClearProperty(aeon.pic.path,home)</onunload>\n\t<include>Anim_DialogOpenClose</include>', 1)
        io.open(w, 'w', encoding='utf-8', newline='\n').write(t)
    from PIL import Image, ImageDraw
    m = os.path.join(fw.SKIN, 'media', 'fg', 'm112x74.png')
    if not os.path.exists(m):
        im = Image.new('RGBA', (112, 74), (255, 255, 255, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 0, 111, 73), radius=8, fill=(255, 255, 255, 255))
        im.save(m)
    fw.put(NAME, page())
    print('fgs picture info: page written')


if __name__ == '__main__':
    main()
