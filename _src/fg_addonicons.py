"""0.39.13 Fused Glass: add-on icons with round corners.
- Add-ons window (and every window using the generic detail panel AG_GenericDetail): the big icon was drawn with
  'keep' inside 500 x 420 and no mask, square corners. In the add-on browser (add-on icons are square) it is now a
  420 x 420 tile through fg/m420x420.png, radius 28 (the radius of the skin's big cards and covers); elsewhere the
  panel keeps its old look (it shows posters and thumbs of any shape there).
- Generic list rows (AG_LibListRow: add-ons, programs, files ...): the 48 px icon is cut by fg/m48x48.png, radius 12
  (small tiles inside rows), instead of masks/square_round8.png (radius 8 at 48 px hardly shows on a TV).
Run from the skin folder."""
import io
import os

from PIL import Image, ImageDraw

SS = 4


def mask(w, h, r, name):
    im = Image.new('L', (w * SS, h * SS), 0)
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius=r * SS, fill=255)
    im = im.resize((w, h), Image.LANCZOS)
    out = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    out.putalpha(im)
    out.save(os.path.join('media', 'fg', name), optimize=True)


mask(420, 420, 28, 'm420x420.png')
mask(48, 48, 12, 'm48x48.png')

p = os.path.join('1080i', 'Includes_Views.xml')
s = io.open(p, encoding='utf-8').read()


def once(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


once('''				<aspectratio scalediffuse="false">scale</aspectratio>
				<texture background="true" diffuse="masks/square_round8.png">$VAR[AG_RowIcon]</texture>
			</control>''', '''				<aspectratio scalediffuse="false">scale</aspectratio>
				<texture background="true" diffuse="masks/square_round8.png">$VAR[AG_RowIcon]</texture>
				<visible>!$EXP[Aeon_FGlass]</visible>
			</control>
			<!-- 0.39.13 Fused Glass: radius 12, like the small tiles inside rows -->
			<control type="image">
				<left>22</left>
				<top>14</top>
				<width>48</width>
				<height>48</height>
				<aspectratio scalediffuse="false">scale</aspectratio>
				<texture background="true" diffuse="fg/m48x48.png">$VAR[AG_RowIcon]</texture>
				<visible>$EXP[Aeon_FGlass]</visible>
			</control>''')
once('''				<aspectratio align="left" aligny="top">keep</aspectratio>
				<fadetime>160</fadetime>
				<texture background="true" colordiffuse="$VAR[AG_ArtDim]">$VAR[AG_RowIconLarge]</texture>
			</control>''', '''				<aspectratio align="left" aligny="top">keep</aspectratio>
				<fadetime>160</fadetime>
				<texture background="true" colordiffuse="$VAR[AG_ArtDim]">$VAR[AG_RowIconLarge]</texture>
				<visible>![$EXP[Aeon_FGlass] + Window.IsActive(addonbrowser)]</visible>
			</control>
			<!-- 0.39.13 Fused Glass, add-on browser: the (square) add-on icon as a 420 px tile, radius 28 -->
			<control type="image">
				<left>0</left>
				<top>0</top>
				<width>420</width>
				<height>420</height>
				<aspectratio scalediffuse="false">scale</aspectratio>
				<fadetime>160</fadetime>
				<texture background="true" diffuse="fg/m420x420.png" colordiffuse="$VAR[AG_ArtDim]">$VAR[AG_RowIconLarge]</texture>
				<visible>$EXP[Aeon_FGlass] + Window.IsActive(addonbrowser)</visible>
			</control>''')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
