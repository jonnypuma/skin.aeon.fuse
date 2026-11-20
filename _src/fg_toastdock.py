"""0.39.14 Fused Glass: where the toast, the background progress and the busy capsule dock.
They docked beside the clock capsule unless the window was on the old Aeon list of windows with a clock box
(Aeon_HasClockBox). Fused Glass draws its clock capsule in many more windows (TV guide, TV channels, programs,
pictures, favourites ...), so there the capsule slid into the clock's place and covered it. Now:
  FG_NoClock (no clock capsule on screen: full-screen video / game / slideshow without the OSD, the OSD with its clock
  switched off, the music Now playing page)  -> the capsule takes the clock's place (right edge, as before)
  FG_ClockNarrow (a clock without weather: 144 px instead of 236)          -> 92 px to the right, against that clock
  the library rail clock (FG_RailClock)                                    -> as before
Run from the skin folder."""
import io
import os

X = '1080i'
OLD = '!$EXP[Aeon_HomeAny] + !$EXP[Aeon_HasClockBox]'
NARROW = '<animation effect="slide" end="92,0" time="0" condition="$EXP[FG_ClockNarrow]">Conditional</animation>'


def rw(name, edit):
    p = os.path.join(X, name)
    s = io.open(p, encoding='utf-8').read()
    s2 = edit(s)
    assert s2 != s, name
    io.open(p, 'w', encoding='utf-8', newline='').write(s2)


def docking(s):
    n = s.count('<animation effect="slide" end="248,0" time="0" condition="%s">Conditional</animation>' % OLD)
    assert n, 'no docking slide'
    return s.replace('<animation effect="slide" end="248,0" time="0" condition="%s">Conditional</animation>' % OLD,
                     '<animation effect="slide" end="248,0" time="0" condition="$EXP[FG_NoClock]">Conditional</animation>' + NARROW)


for name in ('DialogNotification.xml', 'DialogExtendedProgressBar.xml', 'DialogBusy.xml'):
    rw(name, docking)


def fused(s):
    s = docking(s)
    old = '\t<expression name="FG_RailClock">'
    assert s.count(old) == 1
    return s.replace(old, '''	<!-- 0.39.14 no clock capsule on screen (the toast, background progress and busy capsules then take its place): full-
	     screen video / game / slideshow without the OSD (an information page over the video has its own clock), the OSD
	     with its clock switched off, the music Now playing page (its own pages have no clock) -->
	<expression name="FG_NoClock">[Window.IsActive(fullscreenvideo) + !Window.IsVisible(videoosd) + !Window.IsVisible(fullscreeninfo) + !Window.IsVisible(videobookmarks) + !Window.IsVisible(movieinformation)] | [[Window.IsVisible(videoosd) | Window.IsVisible(fullscreeninfo) | Window.IsVisible(videobookmarks)] + Skin.HasSetting(aeon.osd.noclock)] | [Window.IsVisible(visualisation) + !Window.IsVisible(musicinformation)] | Window.IsActive(slideshow) | Window.IsActive(fullscreengame)</expression>
	<!-- a clock capsule without weather is 144 px wide (236 with it): the capsules beside it move 92 px to the right -->
	<expression name="FG_ClockNarrow">!$EXP[AG_HasWeather] + !$EXP[FG_NoClock] + ![!$EXP[Aeon_HomeAny] + $EXP[FG_RailClock]]</expression>
''' + old)


rw('Includes_Fused.xml', fused)
print('ok')
