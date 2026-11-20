"""0.39.10 Player overlays during a trailer started from an information page: the trailer is only a file
("tvshow-trailer.mkv") or a YouTube address, so the Video OSD said "Now playing in MOVIES" with the file name as the
title. The helper (trailer.play) now leaves the show / film in Window(Home) aeon.tr.kind / title / logo / poster and
the playing file in aeon.tr.now; while that very file plays (Aeon_OSD_Trailer) the shared OSD variables use them:
kind (TV shows / Movies), clearlogo or the name, the poster on the card, and "<name> | Trailer" as the card's line.
Video OSD, seek bar and information screen all read these variables. Run in 1080i."""
import io

p = 'Includes_Aeon_OSD.xml'
s = io.open(p, encoding='utf-8').read()
TR = '$EXP[Aeon_OSD_Trailer]'


def once(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


once('''	<variable name="Aeon_OSD_Logo">
		<value condition="!String.IsEmpty(Player.Art(tvshow.clearlogo))">$INFO[Player.Art(tvshow.clearlogo)]</value>
		<value>$INFO[Player.Art(clearlogo)]</value>
	</variable>
	<expression name="Aeon_OSD_HasLogo">[!Skin.HasSetting(aeon.nologos) + [!String.IsEmpty(Player.Art(tvshow.clearlogo)) | !String.IsEmpty(Player.Art(clearlogo))]]</expression>
	<variable name="Aeon_OSD_Kind">
		<value condition="!String.IsEmpty(VideoPlayer.TVShowTitle)">$LOCALIZE[31353]</value>
		<value>$LOCALIZE[31354]</value>
	</variable>
	<variable name="Aeon_OSD_Title">
		<value condition="!String.IsEmpty(VideoPlayer.TVShowTitle)">[UPPERCASE]$INFO[VideoPlayer.TVShowTitle][/UPPERCASE]</value>
		<value>[UPPERCASE]$INFO[VideoPlayer.Title][/UPPERCASE]</value>
	</variable>
	<variable name="Aeon_OSD_Sub">
''', '''	<!-- 0.39.10: a trailer started from an information page (helper trailer.play): while that very file plays, the
	     overlays show the show / film it belongs to (Window(Home) aeon.tr.*), not "Movies" and the file name -->
	<expression name="Aeon_OSD_Trailer">[!String.IsEmpty(Window(Home).Property(aeon.tr.now)) + String.IsEqual(Player.FilenameAndPath,Window(Home).Property(aeon.tr.now))]</expression>
	<variable name="Aeon_OSD_Logo">
		<value condition="%(tr)s">$INFO[Window(Home).Property(aeon.tr.logo)]</value>
		<value condition="!String.IsEmpty(Player.Art(tvshow.clearlogo))">$INFO[Player.Art(tvshow.clearlogo)]</value>
		<value>$INFO[Player.Art(clearlogo)]</value>
	</variable>
	<expression name="Aeon_OSD_HasLogo">[!Skin.HasSetting(aeon.nologos) + [[%(tr)s + !String.IsEmpty(Window(Home).Property(aeon.tr.logo))] | [!%(tr)s + [!String.IsEmpty(Player.Art(tvshow.clearlogo)) | !String.IsEmpty(Player.Art(clearlogo))]]]]</expression>
	<variable name="Aeon_OSD_Kind">
		<value condition="%(tr)s + String.IsEqual(Window(Home).Property(aeon.tr.kind),tvshow)">$LOCALIZE[31353]</value>
		<value condition="%(tr)s">$LOCALIZE[31354]</value>
		<value condition="!String.IsEmpty(VideoPlayer.TVShowTitle)">$LOCALIZE[31353]</value>
		<value>$LOCALIZE[31354]</value>
	</variable>
	<variable name="Aeon_OSD_Title">
		<value condition="%(tr)s">[UPPERCASE]$INFO[Window(Home).Property(aeon.tr.title)][/UPPERCASE]</value>
		<value condition="!String.IsEmpty(VideoPlayer.TVShowTitle)">[UPPERCASE]$INFO[VideoPlayer.TVShowTitle][/UPPERCASE]</value>
		<value>[UPPERCASE]$INFO[VideoPlayer.Title][/UPPERCASE]</value>
	</variable>
	<variable name="Aeon_OSD_Sub">
		<value condition="%(tr)s">[UPPERCASE]$INFO[Window(Home).Property(aeon.tr.title)]  |  $LOCALIZE[20410]  [/UPPERCASE]</value>
''' % {'tr': TR})
once('''	<variable name="Aeon_OSD_Poster">
''', '''	<variable name="Aeon_OSD_Poster">
		<value condition="%(tr)s + !String.IsEmpty(Window(Home).Property(aeon.tr.poster))">$INFO[Window(Home).Property(aeon.tr.poster)]</value>
''' % {'tr': TR})
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
