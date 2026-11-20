"""0.38.0 Home > Power card: white line icons in the style of media/aeon/icons (96 px, 2/24 stroke, round ends),
drawn on a 24-unit grid at 16x and scaled down. Writes media/fg/pw_*.png. Run from the skin folder."""
import math
import os

from PIL import Image, ImageDraw

K = 16                     # pixels per grid unit while drawing (24 * 16 = 384)
W = 2.0 * K                # stroke
OUT = os.path.join('media', 'fg')


def canvas():
    return Image.new('L', (24 * K, 24 * K), 0)


def p(x, y):
    return (x * K, y * K)


def dot(d, x, y):
    r = W / 2
    d.ellipse((x * K - r, y * K - r, x * K + r, y * K + r), fill=255)


def line(d, *pts):
    for a, b in zip(pts, pts[1:]):
        d.line([p(*a), p(*b)], fill=255, width=int(W))
    for x, y in pts:
        dot(d, x, y)


def arc(d, cx, cy, r, start, end):
    """Clockwise from start to end in degrees (0 = east, 90 = south), round ends."""
    box = ((cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K)
    d.arc(box, start, end, fill=255, width=int(W))
    for ang in (start, end):
        a = math.radians(ang)
        dot(d, cx + r * math.cos(a), cy + r * math.sin(a))


def arrow_tip(d, x, y, ang, size=3.2):
    """Two strokes of an arrow head at (x, y) pointing along ang (degrees)."""
    for side in (150, -150):
        a = math.radians(ang + side)
        line(d, (x, y), (x + size * math.cos(a), y + size * math.sin(a)))


def head(d, x, y, ang, length=4.6, half=2.6):
    """A filled arrow head with its tip at (x, y), pointing along ang (degrees)."""
    a = math.radians(ang)
    bx, by = x - length * math.cos(a), y - length * math.sin(a)
    nx, ny = -math.sin(a), math.cos(a)
    d.polygon([p(x, y), p(bx + half * nx, by + half * ny), p(bx - half * nx, by - half * ny)], fill=255)


def save(img, name):
    out = img.resize((96, 96), Image.LANCZOS)
    rgba = Image.new('RGBA', (96, 96), (255, 255, 255, 0))
    rgba.putalpha(out)
    rgba.save(os.path.join(OUT, name))


# restart: an open circle, clockwise, the head at its end near the top
img = canvas(); d = ImageDraw.Draw(img)
arc(d, 12, 12.5, 7.5, -50, 245)
t = math.radians(245)
head(d, 12 + 7.5 * math.cos(t) + 2.6, 12.5 + 7.5 * math.sin(t) - 0.9, 335)
save(img, 'pw_restart.png')

# refresh (update library): two arcs chasing each other, filled heads
img = canvas(); d = ImageDraw.Draw(img)
arc(d, 12, 12, 7.5, 195, 315)
arc(d, 12, 12, 7.5, 15, 135)
for ang in (315, 135):
    t = math.radians(ang)
    head(d, 12 + 7.5 * math.cos(t) + 1.8 * math.cos(t + math.pi / 2), 12 + 7.5 * math.sin(t) + 1.8 * math.sin(t + math.pi / 2), ang + 90)
save(img, 'pw_refresh.png')

# log off: a door frame open to the right, an arrow leaving it
img = canvas(); d = ImageDraw.Draw(img)
line(d, (10, 4), (6, 4), (4.5, 5.5), (4.5, 18.5), (6, 20), (10, 20))
line(d, (10, 12), (20, 12))
arrow_tip(d, 20, 12, 0, 4.0)
save(img, 'pw_logout.png')

# exit: a box with an arrow out of its corner
img = canvas(); d = ImageDraw.Draw(img)
line(d, (11, 4.5), (6, 4.5), (4.5, 6), (4.5, 18), (6, 19.5), (18, 19.5), (19.5, 18), (19.5, 13))
line(d, (11, 13), (19.5, 4.5))
line(d, (13.5, 4.5), (19.5, 4.5), (19.5, 10.5))
save(img, 'pw_exit.png')

# switch user: head and shoulders
img = canvas(); d = ImageDraw.Draw(img)
r = 3.8
d.ellipse(((12 - r) * K - W / 2, (8 - r) * K - W / 2, (12 + r) * K + W / 2, (8 + r) * K + W / 2), fill=255)
d.ellipse(((12 - r) * K + W / 2, (8 - r) * K + W / 2, (12 + r) * K - W / 2, (8 + r) * K - W / 2), fill=0)
arc(d, 12, 21.5, 7, 205, 335)
save(img, 'pw_user.png')

# screensaver: a screen on a stand with a wave across it
img = canvas(); d = ImageDraw.Draw(img)
line(d, (5, 4.5), (19, 4.5), (20.5, 6), (20.5, 15), (19, 16.5), (5, 16.5), (3.5, 15), (3.5, 6), (5, 4.5))
line(d, (12, 16.5), (12, 20))
line(d, (8.5, 20.5), (15.5, 20.5))
line(d, (7, 12), (10, 9), (13, 11.5), (17, 8))
save(img, 'pw_screen.png')
print('ok')

# 0.42.0 reboot to Android (CoreELEC): the robot's head - a half dome with two antennas and two eyes, a body below
img = canvas()
d = ImageDraw.Draw(img)
arc(d, 12, 13, 7, 180, 360)
line(d, (5, 13), (19, 13))
line(d, (8.2, 7.4), (6.6, 4.8))
line(d, (15.8, 7.4), (17.4, 4.8))
r = 1.15 * K
for x in (9.4, 14.6):
    d.ellipse((x * K - r, 10.3 * K - r, x * K + r, 10.3 * K + r), fill=255)
line(d, (5, 15.5), (5, 19.5), (19, 19.5), (19, 15.5))
save(img, 'pw_android.png')
