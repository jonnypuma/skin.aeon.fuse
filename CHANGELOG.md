# Aeon Fuse changelog

## 0.56.55
- The start-up splash stays until Home is really loaded: each section's row and its spotlight must have their items and
  have stopped loading (it ended at once after a skin switch, when the helper's "row in" flags were already set, and
  never waited for the spotlights); at least 8 s, cap 40 s -> 90 s (_src/splashmin_05655.py).
  The skin reload the helper does once after an update (your fonts into the fresh Font.xml) no longer ends it either:
  the splash stays over the reload and waits again (helper 0.3.125).

## 0.56.54
- TinyPPI is a CoreELEC tool: addon.xml no longer imports it (Kodi for Windows listed it among the skin's
  dependencies); in the setup wizard and Skin settings > System > Recommended add-ons it now says "CoreELEC only" off
  CoreELEC and is not installed or counted there (helper 0.3.124; _src/tinyppi_05654.py after wizard_05640.py).
  String 32820.

## 0.56.53
- Live TV in the Fused Glass style (canvas round 8; _src/fgslivetv_05653.py, helper 0.3.123): the guide has eight day
  chips over the grid (the day in view gold, a dot where a timer is set, OK jumps the grid to that day) and the
  programme's line gets its day in words; Recordings become cards like the library (art, NEW, how far you got, channel
  logo); Search shows the search as a big field and each result with its day, time and channel logo; Timer rules show
  each rule as a card with what it catches as a sentence, and New rule / Edit / Activate-Deactivate / Delete as cells.
  TV Timers and Timer rules draw on the normal Live TV background (the old list, its card and the sort row slide out
  of view; no dark page); reminders gold, series violet, recordings red; "No timers set"; even hour steps.
  Strings 32817-32819.
- TV Timers as the week in lanes of time (canvas round 7, idea B; _src/fgstimers_05653.py, helper 0.3.122): in the
  Fused Glass style the timers page shows how many timers the next five days hold, when the next one starts and how
  much is set to record, then a lane per day (today first) with each timer placed and sized by its time (red =
  recording, gold = series, outline = reminder, faded when disabled) and a gold line for now; New timer, Edit,
  Activate / Deactivate, Delete and Hide disabled as cells at the foot. Kodi's list stays the focus (Up / Down walk
  the timers, the block of the focused one is white). Timer rules and the radio pages keep today's page. Strings
  32812-32816. Today's list (also Recordings, Search) no longer runs into its scroll bar, which shows only with more
  than one page.
- Sort and show only now also for TV shows, albums and artists (user: "the same style"): the sorts Kodi accepts for each
  list (shows: Title, Year, Date added, Rating, My rating, Last played, Episodes; albums: Album, Artist, Artist / Year,
  Year, Rating, My rating, Date added, Last played, Play count; artists: Artist, Date added) and their filters (shows:
  unwatched, in progress, watched, continuing, ended, genre, decade, MPAA rating; albums: never played, played, genre,
  decade; artists: genre). Strings 32810-32811.
- Box check of the round-3 windows: the timer column of Timer settings was drawn under the page's background (now over
  it); the file browser shows its counts with the folder and file icons, the choice gold-tinted with OK, New folder,
  Cancel in the board's order; the text viewer sets the text at a narrower reading measure and shows a clock icon
  (the box font has no "≈"); the colour picker's contrast numbers work (the helper looked for "colorpicker", Kodi 22
  calls it dialogcolorpicker; helper 0.3.121).
- Sort and show only (canvas round 6, Films in the Fused Glass style; _src/sortshow_05653.py, dialog 1179, helper 0.3.121):
  the side strip's Sort row opens a two-column panel instead of Kodi's Select sort method - the nine sorts Kodi accepts
  for films (Title, Year, Date added, Duration, Rating, My rating, MPAA rating, Play count, Last played; OK again flips
  the order; Original title, Sort title and Random are ignored by Kodi for films) and Show only (unwatched, in progress,
  watched, 4K, HDR, several versions, genre, decade, MPAA rating, clear all) with counts, the live total in the column
  head and the filters in force at the foot. Other screens keep Kodi's own list. Strings 32803-32809.
- The player information's File and season page in the Fused Glass style (canvas round 6; _src/fgsfileseason_05653.py,
  run after fg_fullinfo.py): on the fanart with the faded gradient; the file as a spec sheet (picture chips, the sound
  streams as rows with flags, the subtitles as round flags, file, size, length, screen, decoder) and the season at the
  right (films: the poster). Other themes keep today's page (FG_FullInfoPage2_Classic).
- Keyboard (Fused Glass style) brought to its board: a solid dark page, keys focused with a thin white ring and a gold
  underline, the matches count at the end of the input line; library matches fixed (helper 0.3.121).
- Round 5 of the Fused Glass style windows (canvas boards without a note; _src/fgsround5_05653.py): the login screen
  (profiles as round pictures, the focused one large with a white ring, Power / Exit / Restart as cells), the keyboard
  (keys as cells on the frame line to line, a big input line, the library titles matching what you type and the recent
  searches above the keys - OK types one in; helper 0.3.120; new string 32802 "In your library"), the slider (the OSD
  panel's offset card alone at the top: ruler, value in the accent, gold marker), and the notification, volume, busy and
  background progress as pills in the style's glass (volume a tall pill at the right edge, busy a ring in the centre,
  background progress still beside the clock, with a gold bar inside). Other themes and styles keep today's windows.
- Files (box check): the skin draws its own row icons (network share, folder, add-ons, a gold + on Add ...) where Kodi's
  default source icons are missing; the peek reloads with each folder (aeon.peek.stamp) and hides when there is nothing
  to show; its counts as a folder and a file icon with their numbers (also in the file browser and media source).
- Files in the Fused Glass style (canvas round 4, idea A): Videos > Files, Music > Files, folders inside a source and
  untyped add-on folders (the plain list 50) get the page spec: the path as crumbs in the title band, a 70 px row per
  item with Kodi's icon, the kind as a tag (NFS / SMB / ADD-ONS ...) and its details, "Add videos... / Add music..." in
  the accent, the bar in the gutter, and at the right a peek inside the folder in focus (helper 0.3.119). Music keeps
  Albums / Artists / Songs / Genres as cells in the band. Pictures > Files already uses the Photos view
  (_src/fgsfiles_05653.py).
- List rows (user, on the box with the updated versions): in the Fused Glass List the year and the genres follow the
  title on line 1, dimmed; line 2 holds the version alone as an outline chip sized to its text (UNRATED DIRECTOR'S CUT
  no longer cut off), a film without a version gets its title centred; version names written with underscores read as
  words (DIRECTORS_CUT -> Director's Cut, Aeon_VerPretty); films that are not HDR show SDR in the HDR slot (List and the
  wide Low list), so the chip column has no hole (_src/rowsver_05653.py).
- Round 3 of the Fused Glass style windows (canvas, "they all look good"; _src/fgsround3_05653.py, helper 0.3.118):
  play queue (the record player at the left, the queue as a rail of dots with the playing one in the accent), file
  browser (the path as crumbs, a peek inside the folder in focus), text viewer (a reader: reading time, a wide column,
  the bar as a rail in the accent), media source (all sources at the left, the three steps in the band, the paths with
  the room, a peek inside the path), the PVR timer dialog (what will happen, in the left column) and the OSD subtitle
  tab (the film's subtitles as cards with round flags, your language first, OK picks one). New strings 32800-32801.
- OSD audio / subtitle panel: the offset now as the mockup draws it (user: "doesn't look as nice as your mockup"): its own
  card at the top of the panel, the name, the value big in the accent, a tall ruler -0.5 .. +0.5 s with long / medium /
  short ticks, the white centre line, a wide accent marker; Kodi's rows start under it (the video tab keeps the full
  height).
- Box check of the Fused Glass style windows (2026-11-20): Video / Music information, Picture info (with its strip),
  versions, PVR channel / group manager, game controllers, font picker, profile settings all draw as built. Fixed from
  the shots: "War HorseWar Horse" (title or label, not both), the focused track beside the tracks, the doubled count,
  cut-off cells (Artist information, Set as default, the group manager's buttons), ISO under the third exposure
  number, the stray dot before the resolution, the versions page's background and logo from the version item and the
  version's file name on its card, the PVR managers' header, the profile icon when a profile has no picture.
- Fused Glass style windows, what Kodi does not hand the skin, now from the helper (0.3.117, user: "these could be shown
  with the helper?"): Picture info shows a strip of the folder's pictures with the one on screen lit; the colour
  picker shows the colour in focus on white and on the dark ground with its contrast (a tick at 4.5:1); the OSD audio /
  subtitle panel shows the offset on a -0.5 .. +0.5 s ruler with its value; Music information draws the album as one
  bar, a segment per track, the first in the accent; Video information marks the intermission on the watched bar from
  Skippy's chapters sidecar (read only) with "Intermission at" (new string 32799 in all languages).
- Fused Glass style, round 2 of Kodi's standard windows (canvas: "so good. build that"); every other theme and style
  keeps today's window (<Name>_PageClassic in the new Includes_FGSWin.xml, shared plumbing _src/fgswin_05653.py):
  - Picture info: the picture full screen, a gradient from the right, date taken, file name, the exposure as four big
    numbers (aperture, shutter, ISO, focal length), Kodi's detail rows with the bar in the gutter (fgspictureinfo).
  - Manage versions / extras: the film's fanart and clear logo, the versions as cards side by side (art, name, the
    default marked in the accent, chips, runtime / size / audio / subtitles), Kodi's buttons as one row (fgsversions).
  - Colour picker: Kodi's colours as rounded swatches on the frame and a live preview of the colour in focus where an
    accent lands (row marker, progress, chip, dot, Home mark) (fgscolour).
  - PVR channel manager: channel rows with logos, inactive dimmed, the channel's switches and the tools as rows, the
    logo in the title band; group manager: the groups as rows, the channels in / not in the group as logo tiles, members
    marked in the accent (fgspvr).
  - Game controllers: Kodi's own controller picture large in the middle, controllers and buttons as rows (fgsgamectl).
  - Font picker: every row a specimen card drawn in its own fonts (the preview families pv0-pv44) (fgsfonts).
  - Settings dialogs: the page spec with the style's setting rows; profile settings with the avatar column (Kodi's
    Profile picture row picks a picture); the OSD side panel with the tabs in the title band (fgssettingsdlg).
- Music information, Fused Glass style (canvas round 2): the artist fanart under the faded gradient, the cover with a
  record sliding out behind it, the facts and the record label's logo under it, the artist and a big title, the
  description (OK: the full text), one action row line to line; Down: the cover and the focused track stay at the left
  while the tracks scroll (number, title, length; the length bars were dropped, user: "meaningless"); further down More by the artist (album pages,
  new) or Top tracks (artist pages) and Similar artists as round photos (album pages too now; helper 0.3.116). Other
  themes and styles keep today's page (MusInfo_PageClassic) (_src/fgsmusicinfo_05653.py). New string 32798 in all
  languages. Video information: the studio / network logo under the facts (user note).
- Video information, Fused Glass style (canvas round 2): the fanart full screen under a faded gradient, poster at
  the top left with the facts under it, the clear logo (else the title), tagline, rating / genre / end time, the media
  chips, the plot (OK: the full plot), the watched bar and one action row line to line (Resume, Play, From start,
  Browse, Trailer, Versions, Extras, More; More swaps in Kodi's other buttons in the same place). Down slides to the
  cast as round photos with names and roles, the crew and the file as cells; further down Recommended, Similar and
  Reviews as rounded posters with a white ring. Every other theme and style keeps today's page unchanged
  (VidInfo_PageClassic) (_src/fgsvideoinfo_05653.py).
- List rows, option A: every row shows its own film. The media chips sit in fixed slots ending at the same right
  edge (resolution, HDR, audio, aspect, rating; a slot stays empty when a film has no value for it) and line 2 stops
  before them, the same width on every row (List, Low list, Compact list, the episode lists). The version (Kodi's
  version name, the sidecar edition only when Kodi says Standard Edition) is an outline chip opening line 2, in the
  Fused Glass List and the Aeon List row; the dimmed version after the title is gone. Before, the chips and the
  version came from grouplists, which read the focused film on every row (_src/rowchipsA_05653.py).
- Skin settings > System: **Recommended add-ons** (row 9507, under Import). OK opens the list of the optional add-ons
  that give the skin more to show (TMDb Helper, KarmaMole Skin Helper, Studio / Record label icons, Language flags,
  Weather icons, Embuary, CU LRC Lyrics, Artist Slideshow, Aeon Fuse Screensaver, Skippy, Trickplay, TinyPPI, the
  Copacetic and Roboto CJKSC fonts) with what each adds and whether it is installed; the row shows "n / 15". OK on a
  missing one installs it with Kodi's own Install dialog; when it lives in a repository that is not installed (Skippy
  Repo, jamal2362) that repository is installed first from its zip, after a yes (helper 0.3.114 addonrec).
- Skin settings > Libraries: **Update and clean on another Kodi** (row 9502) with Address (9503), User name (9504),
  Password (9505) and Test connection (9506), shown only while the switch is on. With it on, the skin's library update
  and clean (Home system menu, the library panel, the power menu items, the context menu) are sent to that Kodi's
  JSON-RPC (VideoLibrary.Scan / Clean, AudioLibrary.Scan / Clean) instead of running here, with that Kodi showing its own progress bar; an update there is followed
  until it ends ("Library update finished", the lists here refresh). Every UpdateLibrary / CleanLibrary of the skin now
  goes through RunScript(script.aeon.helper,lib,update|clean,video|music) (38 places, _src/libremote_05653.py; also
  fg_home_system.py). The password is the helper's own hidden setting, not a skin string, so Export skin settings
  leaves it out. Kodi's own update entries (Settings > Media > Library, the file list's Scan to library) still run here.
- Setup wizard: **Recommended add-ons** is now step 2, right after the welcome page (it was the step before All set).
  All 15 add-ons are listed; OK ticks one (installed ones say Installed), the picture shows what it adds to the skin
  (media/aeon/wizard/shots/addfeat_<id>.jpg from box shots, _src/wizard_addonshots_05653.py) and the text says what it
  does. Next installs the ticked ones in the background while the wizard goes on (helper addonrec,batch: the
  repository first when needed, Kodi's own install question answered Yes) and says how many went in.
- Fused Glass player information page (Up in the player): the language flags of the audio and of the subtitles
  shown, under the Audio line (only the Aeon page had them). _src/flags_05653.py; re-run it after fg_fullinfo.py.
- Rounded language flags in the player: the Audio / Subtitles OSD settings panel shows its language's flag at the end
  of its heading, and the controls' audio button shows the playing audio's flag in its circle while focused (same
  script; re-run it after fg_osdrow.py too).
- Audio / Subtitles / Video OSD settings panels: Up from the first row reaches the tab row again in every menu style
  (it went round to the last row: with only conditional Up actions, none of which holds while Kodi builds the rows,
  Kodi links the first row to the last; a fallback Up that holds only then fixes it; ms_menus.py patched too).
- Media info chips from sidecars (video source, video codec, version, container, bitrate, size, subtitles, chapters,
  commentary, 3D) now show in every chip row: library views of all three themes, widget screens and Home spotlights /
  strips (they were on the information page only). _src/sidechips_05653.py adds them after each run of chip buttons, in
  that row's look, for that row's item; re-run it after placegate_05652.py. Helper 0.3.114 reads the sidecar of the
  Home spotlight's item when the focused item is no video.
  They sit on a second line (user): container and bitrate stay on the first line beside the resolution, the others
  go to a line of their own under the chips in the Fused Glass panels, to the ratings line next to the chips in the
  spotlights / widgets / cards (with a twin line for when ratings are off), a fourth line in the Aeon views, under the
  chips in the big Home spotlight (its plot moves down) and above the chips in the List view card (its plot shorter).
  _src/chipline2_05653.py; run it after sidechips_05653.py. Video codec joins container and bitrate on the first
  line. The five Fused Glass strip views (Poster wall, Landscape wall, Showcase, Square wall, Cards) give their lower
  chip lines the strip's full width (1656 px) instead of the 560 px column, where they ran off.
- The Aeon / Aeon Glass library views write the media info as text: the sidecar values are added to that line
  ("TRUEHD 7.1  •  1.78:1  •  DV P7 MEL  •  4K  •  HEVC  •  MKV ..."), $VAR[Aeon_TxSide], _src/sidetext_05653.py.
- That text follows Media info chips part by part like the chips (user): the aspect ratio has its own switch (it went
  with Resolution), the channels follow Audio channels, the Dolby Vision profile follows DV profile (plain DV when off).
  The right info pane's line in the episode views ("4K  •  HEVC  •  HDR10  •  TRUEHD  7.1 CH") gets the channel switch,
  the sidecar values and the bullet separator of the other views (it was " | "). _src/textgate_05653.py, after
  sidetext_05653.py.
- Fused Glass wall views (Poster wall, Landscape wall, Showcase, Square wall, Cards), the info strip (user): the clear
  logo sits at the strip's top right and the studio logo in its lower right corner; the plot ends before the clear logo,
  the chip lines before the studio logo, and the left column's kicker / meta lines no longer make room for the logo.
  The Aeon / Aeon Glass wall views (Aeon_V_Info) the same way: the clear logo at the panel's top right where the
  studio logo was, the studio logo beneath it, the title / ratings / media line / plot ending before them.
  _src/walls_05653.py, after chipline2_05653.py.
- Fused Glass list rows in focus: the progress ring's track was black at 20 % on the white focus bar, so only the
  coloured arc showed; now 40 % (11 rings, fg_lib.py).
- Aeon / Aeon Glass library views: the in-progress ring drew only its arc (a film 8 % in showed an orange sliver, no
  circle); every arc now has its track under it, in the arc's colour at 35 % (21 rings, _src/ringtrack_05653.py).
- List rows (user, style B): films with a real version name get a small outline tag with it right after the title in
  the List view (all themes; not the Compact list, whose title column leaves no room for it); the title is a
  self-sizing disabled button there (Kodi sizes buttons, not labels, to their text inside a list row).
  _src/tagrows_05653.py. Aeon / Aeon Glass info panels: the version in front of the watched / progress status
  (_src/versionstat_05653.py).
- Time left in the library rows, cards and panels like the run time beside it: "[B]3[/B]·29 left" (was "209 min
  left"); helper 0.3.114 aeon.left.<k>.hmb; the generators write .hmb.
- Episode combined: the plot moves up under the status line (three lines high now); under it the media chips up to the
  HDR, then a line with video codec, container, bitrate and the other sidecar chips; the subtitles and chapters chips
  sit after "S3 E1 · Season premiere" under the episode picture; the status line holds the version and the status
  only (the sidecar chips were cut there). _src/epcomb_05653.py (round2 for the second arrangement).
- Player information page and chips: Dolby Vision with its profile ("DV P8.1") for the file playing, and the sidecar's
  source format and bitrate on the Video line (helper 0.3.114 PlayerSidecar: aeon.pf.dvp, aeon.pf.mi.*). In flags_05653.py.
- List row version tag: also the sidecar edition of the film in focus (Lawrence of Arabia: Anniversary Edition).
- A film's version / edition goes with its title, not with the media info (user): Kodi's version name (the library's
  own versions; not the default "Standard Edition"), else the sidecar's edition for the film in focus (Version switch).
  Fused Glass: every info panel's status line starts with it, in front of the ring ("Director's Cut  ◯ 209 min left",
  22 lines in 19 views), and the List / Compact list rows have it after the title. Aeon / Aeon Glass: the heading lines no longer say "Standard
  Edition" for every film. The edition chip leaves the library chip rows and media text lines (the information page
  keeps it). _src/edition_05653.py, after the sidecar scripts.
- Setup wizard "Use the defaults": Aeon and Aeon Glass start with the Color backdrop behind the library views and the
  corner boxes on Colors (helper wizard.DEFAULTS, the user's choice); Fused Glass unchanged.
- Skin settings: a dimmed row in focus drew its name in fixed dark ink, which vanished on the dark Fused Glass style
  focus bar; it now dims the style's own focus ink.
  Strings 32762-32794 in all 23 languages.

- Fused Glass season views (Banner list, Showcase, Square wall, Compact list, Season list combined 1 / 2 / 3, Low list,
  Flix and the other library views): a season's panel shows the show's next airing in the accent colour ("S3 E7 airs Wednesday 25
  November", helper 0.3.115 aeon.sn.next) and then the season's plot, else the show's plot (Container.ShowPlot)
  (_src/seasonplot_05653.py).
- Fused Glass list rows (List, Low list, the episode lists, Compact list): the media chips are right-aligned and all end
  at one edge per row, leaving the duration column room for "3·29 left" whether the item is in progress or not; a chip
  that does not apply leaves no gap (_src/rowchips_05653.py). Compact list titles are as wide in every row.
- Aeon / Aeon Glass List view: subtitles, chapters and commentary from the sidecar moved from the bottom media line to
  a line under the plot in the top panel (_src/extras_05653.py).
- Fused Glass List view: the chevron that says Left opens a film's versions (or a set's films) moved off the poster's
  edge, where it was a dark circle on a dark poster, into the gap between the poster and the list (_src/chevron_05653.py).
- Fused Glass info panels: the media chip lines show only for films, episodes and music videos; empty, they still took
  room and pushed a season's plot out of the Banner list panel (_src/mediagate_05653.py).
- "Season finale" is no longer put on the last episode of a season in the library while a later episode of that
  season is still to air (helper 0.3.115).
- Fused Glass Banner list, a season in focus: the airing line and plot fill the empty right half of the panel (11
  lines) instead of two lines under the year (_src/bannerplot_05653.py).
- Skin settings > Home menu: Delete for custom items (last button of the editor, 9687): asks, clears the item's name,
  path, icon, spotlight, backdrop, widgets and submenu, and moves the items below it up, so the numbers stay 1, 2, 3...
  Presets show it dimmed with "Custom items only" (strings 32795-32796, 23 languages).
- Skin settings > Home menu / Context menu in Fused Glass style: the editor buttons draw the style's grey bar when
  focused (they drew the white bar under white text: unreadable); the list scrollbar sits in the gap at the list card's
  edge instead of in the Selected item column (rows 995 wide) (_src/homeedit_05653.py).
- Aeon / Aeon Glass list rows: the duration's dot sits halfway between the hour and the minutes (the minutes were
  right-aligned in their box and stood 11 px off the dot; the hour 5).
- List rows with a version tag (Aeon List, Fused Glass List): only the focused row draws the outline tag; the other rows
  carry the version inline, dimmed. Before, a row in a grouplist read the focused film, so every row with versions
  showed the focused film's title and version (_src/tagfix_05653.py).
- Home > Music spotlight: the artist clearlogo is at most 100 high and sits under the category header (a tall logo such
  as ADELE covered "RECENTLY PLAYED").
- Now playing (Windows): the waveform box follows any Aeon Fuse Waveform Visualizer add-on (the visualizer is now four
  add-ons, visualization.aeonwave.<platform>, named "Aeon Fuse Waveform Visualizer (<platform>)"), not one exact name.
- Recommended add-ons: Aeon Fuse Waveform Visualizer, the build for this device (string 32797, 23 languages; pictures
  media/aeon/wizard/shots/addon_visualization.aeonwave.<platform>.jpg).
- Skin settings > Libraries > Library fanart blur: the middle step reads 0 (it read "Programs": Kodi takes a label of
  digits for a string id); the hour of a duration under an hour in the Aeon rows too ($NUMBER[0]).
- Skin settings > Information: the rows Resolution and codec, HDR tag and Audio codec and channels are gone; they set
  the same switches as three ticks of Media info chips, which now is the one place for every chip (settings, defaults
  and looks unchanged) (_src/chiprows_05653.py).
- Add-on settings, add-on browser, add-on information: the add-on's fanart is drawn on its own ground, so the general
  backdrop no longer shows through it; in the Fuse menu themes their deep background is no longer drawn over it.
  Add-on browser: inside a repository, an item without fanart (a folder) shows the repository's fanart before the
  backdrop (helper aeon.ab.repofanart).
- Fused Glass: the Home menu's submenu and widget editors (Edit submenu, Edit widgets) rebuilt in the Fused Glass design:
  backdrop, header, clock pill; the list in a frame (style: rules and focus bar meet the vertical lines) or a glass card,
  with a title band, a rule above the first row and numbered rows; the row being edited stays marked while the options
  have focus; the options panel says "Selected item:" and that row (it showed the Home item). Choose type (it changed
  the Home item's type) and Add list... (the same as + Add item) are gone; Widget screen options is the widgets panel's
  first option; all options fit the panel (_src/fgeditors_05653.py).
- Fused Glass style: Edit widgets / Edit submenu on the Skin settings grid: rows 70 high (were 84), + Add item one row,
  the options in the column 1501-1820 sharing the list's right line (it stood 20 px apart), 70 high from 191 with a
  line at the top of each, scrolling with their own scroll bar when they do not fit (_src/fgeditors_05653.py).
- Fused Glass style: Edit spotlight, the Planner spotlight, Live TV and Widget screen options in the Skin settings
  design (they had the plain classic page): backdrop, header and clock, the frame with its title band, rows 70 high
  flush with the frame's lines, each with its line, the style's focus bar; other looks unchanged (_src/fgspot_05653.py).
- Fused Glass style: the focus shadow under every focus bar (it was off in the style; FGS_ShadowOn), buttons too
  (_src/btnshadow_05653.py: 83 option buttons).
- Fused Glass style: the scroll bar gutter: a 20 px column between two lines on the right of each list, the scroll bar
  square inside it (Skin settings rows | right column from 1521; editors: list | options | ; the option dialogs);
  the editors' list has a scroll bar now (_src/gutter_05653.py, fgeditors, fgspot).
- Fused Glass library views that scroll sideways: Flix (528), 529 and the 518 strip have a level scroll bar under the
  row on a faint track (Flix's belonged to no list, the others stood upright); the wrap lists' still bars (523, 531) are gone
  (_src/libbars_05653.py); Down from the row reaches its bar (when the row scrolls), Up returns, Down goes on where
  the row's Down went; while the bar has the focus its whole track lights up in the accent (with thousands of items
  the thumb is a few px) (_src/libbarsnav_05653.py).
- Add-on browser / Favourites in Fused Glass style: rows 70 high (were 100) as the strip above; the strip's buttons are
  cells with a line at their right edge and no gap; Up from the strip goes to the last add-on, Down from the last
  to the first (_src/addonbrowser_05653.py).
- Fused Glass style, one page spec for Kodi's standard windows (the Skin settings window: frame 120-1820 x 108-960,
  title band, 70 rows, one line between columns, the scroll bar gutter, the style's bar with the dark fill):
  Kodi settings and Add-on settings have pages of their own (FGS_SettingsPage / FGS_AddonSettingsPage, were the Aeon
  page bent by slides; _src/fgspage_05653.py); System information's sections are grid rows with the style's bar, the
  open one dimmed, the meters inside the frame (_src/sysinfo_05653.py); the Event log rebuilt in the style
  (_src/fgseventlog_05653.py); Select gets the gutter and a left line (_src/selgutter_05653.py).
- Fused Glass style: the File manager and the music playlist editor rebuilt on the page spec - two panes of 70 rows
  with their own gutters, the path / heading and count in the title band, the playlist editor's Open / Save / Clear
  as a strip of cells (_src/fgsfilemanager_05653.py, fgsplaylisted_05653.py).
- Fused Glass style: the play queue (Shuffle / Repeat / Save / Clear as a strip, the list with its gutter, the focused
  item's art in the right column) and the file browser (the dialog's ground and header, the path in the band, the
  list with its gutter, OK / Cancel / New folder / Mirror in the right column) on the page spec
  (_src/fgsplaylist_05653.py, fgsfilebrowser_05653.py).
- Fused Glass style: the text viewer (the text in the frame, the square bar in the gutter, Right reaches it) and the
  Add / Edit media source dialog (paths + gutter, Browse / Add / Remove in the right column, the name row, OK / Cancel
  as a strip) on the page spec (_src/fgstextviewer_05653.py, fgsmediasource_05653.py).
- A-Z strips (every video and music view): each letter goes to the top of the view before Kodi's phone-key jumps, which
  count from the item in focus - B went to C and A to # depending on where you were; a view whose first item already
  starts with the letter stays there (_src/azfix_05653.py).
- Fused Glass library: an item without fanart (e.g. a leftover whose file is gone) stands on the neutral ground - the
  library ground no longer carries the random settings backdrop that showed through (_src/libneutral_05653.py).
- Fused Glass: the flash over the film library is gone - the Aeon Glass library layer (tab bar, "Films . n of total"
  card, the hour timeline view 506) faded in and out while the window opened; in Fused Glass it is no longer loaded
  (_src/libflash_05653.py; review 2026-11-18's open "Flix flash").
- Fused Glass style dialogs: the context menu, Manage... and every dialog row get the focus bar's dark fill
  (FGS_DlgRow: fgs_bar_dk); Select (and the yes/no Kodi shows when no similar film exists) names the film when it
  adds a version (the version manager keeps its title),
  its Browse files / Browse library are the frame's last row (were below it), the focused row's path scrolls
  (_src/fgsdlgfix_05653.py).
- Start-up splash: it stays one second after the last step is in, so every step shows its tick (TV shows and Music
  landed in the same moment the splash ended and never showed theirs; timers aeonsplashend / aeonsplashfin). Its cap
  is 40 s after Home opens (was 30: a big Movies library took longer and TV shows / Music never got their turn).
- Fused Glass style: every window that draws its scroll bar through AG_Scrollbar gets the gutter (AG_ScrollbarFGS: two
  lines 20 apart, the square bar between; _src/agsbgutter_05653.py).
- Fused Glass style: the focus bar's dark fill everywhere - rows that cannot carry the shadow image (Kodi's settings,
  categories, sub-nav cells) use fg/fgs_bar_dk.png; Select and Add-on rows get the shadow.
- Fused Glass style 'Pop' focus animation: its second zoom ran from 101.2 to 100, which Kodi multiplies with the
  first, so every bar with it stayed 1.2 % too wide (past the frame lines); now 100 to 98.814.
- Skin settings in Fused Glass style: the focused row's extra top rule is gone (top and bottom lines alike); Right
  from a row reaches its page's scroll bar on every page (not while it picks a value); the bar starts on the band's
  rule (_src/rowbar_05653.py).
- Every scroll bar turns the accent colour while it has the focus (Fused Glass yellow, Aeon Glass its time-of-day
  accent, the other themes their accent; Aeon_SBFocus / _L, _src/sbfocus_05653.py): 52 bars, the Fused Glass
  library views had it already.
- Skin settings > Home menu / Context menu in Fused Glass style: rows and option buttons are 70 high, the Categories'
  height, on the Categories' grid: the rows from 191, the option buttons from 191 too (all eleven, Delete with its
  reason, fit to the frame's bottom; Selected item moves up into the title band); every row and option button has
  the settings rows' line at its top; the options' scroll bar sits on the right line. The Context menu page's rows
  get the lines and the style's dimmed marker for the row being edited (it had the Fuse outline).
- Skin settings > Home menu / Context menu in Fused Glass style: the option bars run from the column line to the frame
  (1501-1820, were 1536-1792) with the text 24 px in, and the Home menu rows and their marker run to the line (1019
  wide, as every other settings page; the scroll bar sits on the line).
- Skin settings > Home menu: Right from a row stops on the scroll bar first (it turns the accent colour; Up/Down scroll,
  Left goes back to the row, Right on to the options; the row stays marked meanwhile); without a scroll bar Right goes
  straight to the options.
- Skin settings > Home menu in Fused Glass style: the row being edited is marked with the style's dimmed bar, like the
  selected category (it had the Fuse outline).
## 0.56.52
- Skin settings > Information: **Ratings shown in** (row 9500, under Ratings shown as) and **Media info shown in** (row
  9501, under Media info chips). OK opens a tick list of the places: Library views, Information pages, Widget &
  Spotlight screens, Home spotlights, Player info, and Live TV (ratings) / the screensaver (chips). All on by default;
  the row shows "n / 6" (helper 0.3.113 placepick). _src/places_05652.py writes the rows and $EXP[Aeon_Rate_<place>] /
  $EXP[Aeon_Chip_<place>]; _src/placegate_05652.py puts the switch on 975 rating / chip controls in all three themes
  (separators that only show with them go too). Re-run placegate after the generators that write those views
  (fg_lib*.py, fg_epcomb.py, wx_screensaver.py, fg_ss.py). Strings 32751-32761 in all 23 languages.
- Kodi's select list with pictures (actor search from the information page, ...): the picture falls back to landscape
  -> episode still -> the show's landscape -> fanart with the clear logo on it -> poster -> icon (a TV show without a
  thumb drew nothing). Aeon's icon grid shows the poster first (_src/selart_05652.py).
- Widget & Spotlight screens: a dot for every item (up to 30), ten per page; the dots page with the focus. Before,
  the dots stopped at the autoscroll count and moving past it left no focus dot (_src/spotdots_05652.py).

## 0.56.51
- Skin settings > Theme & style > Theme: picking Aeon or Fused Glass set Aeon Glass (since 0.56.45 every pill of the row
  ran the Aeon Glass switch: the generator took the theme from the word "glass" in each pill's condition). Each pill
  sets its own theme again (_src/themefix_05651.py; pickmode_05645.theme_key).
- After a setting that reloads the skin the focus goes back to that row also when Kodi reloads twice (a theme switch
  does, 4 s apart): the window clears its note 8 s after opening instead of at once, and the rows cancel a pending
  clear when they set one.

## 0.56.50
- The start-up splash shows the skin's version (v0.56.50) in the bottom right corner, on the hint's line, on the first
  frame and on Home's splash (_src/splashver_05650.py).

## 0.56.49
The user's notes of 2026-11-18 (evening). Helper 0.3.112.
- Start-up splash from the first frame: Kodi draws nothing until the start-up window's onload has run, and that onload
  loaded Home (7 s on the box) before anything showed, so the screen stayed black and the splash came last. Startup.xml
  now draws the splash itself (the same face, Aeon_SplashFront) and asks for Home a second later; the screen keeps the
  splash while Home loads and Home's splash (with the drifting fanart) carries on from it (_src/startup_05649.py).
- Color needs KarmaMole: without script.karmamole.helper the Color option is not offered for the Screensaver, Library,
  Spotlight and Widget screen backgrounds or the Corner boxes (Skin settings rows, View settings, Spotlight options,
  section editor, setup wizard). The other options share the row; a Color already chosen shows as the look it falls back
  to (Fanart, or Neutral for library backgrounds and corner boxes); the preview cards drop their Color line, and
  Libraries > Box colors from artwork (the helper colours boxes only with KarmaMole) is hidden (_src/karma_05649.py).
- Fused Glass style, Skin settings: the preview sits in the grid's third column; each preview card drew its own Fused
  Glass panel over that column (a second panel and shadow under the preview). Its text is 24 px in, as in the other
  columns (_src/fgs_preview_05649.py).
- Skippy's segments as chapters: when the file has no chapters of its own, the player's bars (Aeon, Aeon Glass, Fused
  Glass seek bar, player card, poster bar, pause card) show gaps at every segment Skippy found (start and end), and the
  chapter line reads Chapter n / m. The helper reads Skippy's segment list (skippy.parse_cache_snapshot.v1) and publishes
  aeon.sk.ranges / part / count (_src/osdchap_05649.py, helper resources/lib/skchapters.py).

## 0.56.48
The user's three notes of 2026-11-18 (_src/sets_05648.py, repeatable; the generators carry the same changes).
- Fused Glass, List view, movie sets: the set's film posters sit under the clearlogo (they lay on it); with no logo
  (or logos off) they stay at the top. A set shows no studio logo there. A chevron on the big poster's right edge
  says Left opens the film selection (also a film's versions).
- Banner list is no longer offered for movie sets (picker card and the view itself, every theme); a set node that was
  on it opens in List. Movies, TV shows and seasons keep it.
- View settings, Fused Glass: Panel blur also shows with the Clear style (it hid there since 0.56.45). Clear's Default
  is Off; Light / Medium / Strong blur the panels of that view. Dark and Frost as before.

## 0.56.47
- Ready for Kodi 23's smooth movement: Kodi 22 draws every skin picture on whole pixels, so slow pans and growing bars
  move in 1 px steps. Kodi 23 can draw between pixels. The moving fanart (screensaver zoom and slide, music Now playing
  drift, Home spotlight and widget screens, start-up splash) now carries subpixel="true" mipmap="true", and every
  progress bar's fill and end cap carries subpixel="true" (_src/subpixel_05647.py, repeatable). No change on Kodi 22,
  which skips both attributes.

## 0.56.46
- Music player controls, the album track list: a white circle under the focused arrow; the album shown keeps its title
  over the list, the album an arrow would open shows between the arrows; the panel is wider (to 1840).
- Fused Glass style, the Add-ons list: the focused row has a line above and below only (no box), the lines stay still
  and stop before the scrollbar (the focus animation pushed them over it).
- Movement between pixels: Kodi 22 places every skin picture on whole pixels; Kodi 23 adds <texture subpixel="true">
  (not used yet: Kodi 22 ignores it).

## 0.56.45
The user's notes of 2026-11-18 after 0.56.44.
- Skin settings: rows with three or more options open with OK; Left / Right move the pick (a ring round the pills, the
  help line says how), OK sets it, Up / Down / Back keep the option in use. Two-option rows and switches keep one press.
  Rows that reload the skin (Skin style, Focus highlight, palette, fonts) bring the focus back to themselves afterwards
  (it used to fall back to the category list).
- Fused Glass, Clear style: Panel blur hides (the Clear style draws no blurred copy).
- Start-up splash: the TV shows and Music steps wait for their own rows (they were also done once the helper's preload
  ended, and the preload skipped a row the skin had armed itself, so the splash could leave after Movies).
- View settings (library views): Backdrop strength is gone (it is for the menus); the library fanart's opacity is
  Library fanart opacity alone. Every option that follows Skin settings says "Default (its value)". Library fanart tint
  works with the Dimmed fanart look and with fanart that has no colours of its own. Library fanart blur has Off, -2 .. +2
  (0, the old Light, is the default, here and in Skin settings; old values move to the new steps). New: Panel shadow,
  opacity, blur (Fused Glass) and tint per view.
- Home menu: Start on - the Home menu item that has the focus when Kodi starts, once the splash has gone.
- System menu: the line under the focused item lists what is inside (Settings: Player, Media, ...; CoreELEC: System,
  Updates, Network, ...).
- Fused Glass style: System info in the settings grid.
- Music player controls: the album track list on the right, with arrows through the artist's albums; OK on a track
  plays that album from there.

## 0.56.44
Review round 2, part 2 (2026-11-18) and the Kodi 22 freeze found for good.
- Freeze: leaving music Now playing froze the box (the third freeze that day). gdb showed it exactly: Kodi 22 reads a
  list's `<content target>` in its loader thread while holding the list's lock (CDirectoryProvider::StartDirectoryJob,
  after a playback start / stop or a library update refreshed every Home list), and any info label there waits for the
  GUI lock the screen holds while it waits for that list. The custom Home rows had the only such target (a variable
  choosing videos / music / programs). Each row now has four contents with plain targets (videos, music, programs,
  pictures; Kodi's multi provider sends clicks to the content that gave the item), and the old choice picks which
  content gets the row's path. 20 play / stop rounds on Home and from Now playing ran clean on the box.
- Skin settings > Theme & style: the Expert settings switch and Reset expert settings are gone; the rows they showed are
  always there (Panel opacity / blur / tint, Library fanart opacity / blur / tint).
- Aeon Glass gets the panel and focus options of Fused Glass: Panel shadow, Panel opacity and Panel tint (its cards'
  two frosted fills and their shadow), its own Panel blur (Off / Light / Medium / Strong: the picture behind menus and
  dialogs blurred by the helper, Off = as before) and Focus highlight (Glass = the accent bar as before, Pill, Frosted,
  Outline, Tight; menus, dialogs and Home lists, with dark text on the white ones; not with the Fuse style, which draws
  its own focus cards; library rows keep the glass bar with its pointer tips). Setup wizard: Panel shadow and Focus
  highlight steps for Aeon Glass.
- Fused Glass: Focus highlight hides with the Fused Glass style (it draws its own focus); in the Dark, Clear and Frost
  styles the row icons, names, headings and page title move 101 px to the left like the Fused Glass style's, so long
  names no longer run into their options.

## 0.56.43
Review round 2 (2026-11-18) and a Kodi 22 freeze.
- Freeze: OK on Pictures (slideshow of the newest folder) froze Kodi twice. Kodi runs SlideShow() inside its message
  handler holding the GUI lock for the whole show while still processing Home underneath; a Home list that was loading
  and changed its path re-read it in the loader thread, waited for the GUI lock, and the screen waited for that list.
  The slideshow now starts from the Pictures window (helper 0.3.109); the Home spotlight's set strip (list 9441) reads its
  path from Skin.String(aeon.rt.setrow), written by the helper, not from the spotlight lists.
- Context menu: the skin's own top row (View, sort, filter...) has the same focus picture as Kodi's rows (it showed a
  square bar with hard corners in the card's rounded top in Aeon Glass and the Fused Glass non-system styles).
- Splash: every step in a row that ticks off (Library, Movies, TV shows, Music, Live TV guide, Weather; the current one
  with a small yellow spinner); it waits for Home's Movies / TV shows / Music rows (the helper preloads them one after
  another) and the TV channels, at most 30 s; weather is not waited for.
- Flix (Aeon / Aeon Glass): the studio / network logo's right edge on the plot's (920).
- Music player controls: the button row centred on the screen.
- Confirm dialog: CoreELEC's icon when CoreELEC asks (its update question) - classic card top right, Fused Glass style
  grid left cell (System.AddonIcon). Not in the Aeon menu-style variants yet.
- Toasts in Fused Glass: the icon is the round 40 px cut again (0.56.42's square icon undone; the capsule's end is round).

## 0.56.42
The user's Skin settings review of 2026-11-18, second part.
- Skin settings in new categories (_src/regroup_05642.py; names in all 23 languages): Theme & style, Home, Home menu,
  Libraries, Information (ratings under their own heading), Widget & Spotlight screens, Player, Music player,
  Screensaver & backdrops, System, Context menu. Every page is a scrolling list (70 px rows, hidden rows take no room,
  Up / Down written from the order and the rows' visibility); previews and help moved with their rows. Long category
  names wrap to two lines. _src/settings_rows.py: helpers to add rows to these lists.
- System > Export skin settings / Import skin settings (helper settingsio.py): every skin setting with Kodi's theme,
  colours and font to aeon-fuse-settings-<date>-<time>.json in a folder you pick; Import asks with the file's date, sets
  only what differs, writes the fonts again when a font choice changed and restarts Kodi (Linux; elsewhere the skin
  reloads). New icons export.png / import.png (_src/icons_05642.py).
- Home > Home gradient Off | Soft | Strong (aeon.homegrad; Soft = the look so far): the fade from the bottom of the screen
  up to the Home menu in every theme, Strong a second, taller fade; Off hides it and Fused Glass's bottom scrim. Preview
  card. Setup wizard step (pictures from Fused Glass Home).
- Home > Now playing on Home in Fused Glass: Beside the clock | Left corner (aeon.fgnpleft; its own switch, Aeon's Slot /
  Corner / Line / Bar stays apart); Left corner puts the capsule in the lower left corner, clear of the rows. Wizard step.
- Player > Segment skip button placement (Tab | Glass) in Aeon Glass too: its player controls get Fused Glass's skip
  button (they had none); its own help line (_src/skip_05642.py).
- The library strip's Music player opens a Now playing panel over the library (Custom_1177, Aeon 2 ideas board): the
  artist's backdrop, logo, song, artist, track and album, year and label, cover, previous / play-pause / next / the artist
  in the music library / full Now playing, progress and times, the next song; Back closes it; it closes itself when the
  music stops (Custom_1178). New icon artist.png.
- Big libraries: the focused title's poster, fanart, thumb, landscape and clearlogo show at once (helper focusart.py
  fetches them from the library while Kodi's list still loads its art from the top); 168 art variables fall back to it
  only while the item's own picture is empty and the copy belongs to that item (_src/focusart_05642.py).
- View settings: Library fanart opacity, blur and tint per library view (aeon.vo.<content>.<view>.fop / fblur / ftint;
  Default follows Skin settings), shown while the view has fanart (_src/viewfan_05642.py).
- (Undone in 0.56.43) Toasts in Fused Glass showed the caller's whole icon (48 px, rounded corners).
- One start-up splash for every theme (_src/splash_05642.py), after Arctic Fuse 3's: a random film's fanart drifting
  under a dark veil, AEON FUSE with FUSE in the yellow, the yellow spinner, "Getting Home ready · <step>" and four step
  marks, "OK or Back skips".
- Strings 32722-32746 (all 23 languages, _src/strings_05642.py, _src/strings_05642b.py).

## 0.56.41
The user's Skin settings review of 2026-11-18, first part (_src/review_05641.py, _src/strings_05641*.py).
- Setup wizard: the Skin theme step shows each theme's List library view (Lawrence of Arabia with the Fanart
  background) instead of Home, which looks alike in all three; the texts tell the themes apart: Aeon = solid panels in
  a palette you pick, Aeon Glass = Aeon with glass menus, no palettes, Fused Glass = its own library views and glass
  cards. The Palette step has no pictures any more: one Aeon List view mock-up takes the focused palette's colours
  (page, panel, rows, highlight bar, corner boxes) as you move through the list; OK takes it and moves on.
- Renamed (all 23 languages): Toasts expand from clock pill, Fanart Menu Backdrop, Menu Backdrop Strength, Library
  background, Library fanart look, Library fanart opacity / blur / tint, Combine multi-episode files into a single row
  in library (its name gets the room up to its On / Off), Subtitle offset strip, Show clock on OSD, Show weather on OSD,
  Words style placement, Show language flags on OSD, Show poster on OSD controls, Segment skip button placement, Show
  weather on screensaver, Show clock on screensaver.
- Plotline: Plot | Tagline | Both. Every library view follows it now: before, the Fused Glass views (and some Aeon
  ones) drew the tagline on its own line whatever the setting said. Fused Glass: Plot = the plot only, Tagline = the
  tagline only (the plot when there is none), Both = the tagline over the plot. Aeon: the tagline line only with Both.
- Spinning disc art: Off | Videos | Music | Both (aeon.osd.discart; the old switch becomes Both once).
- Font picker preview: the heading face also sets a film title over the sample text, so combinations that share the
  text face (Figtree, Fraunces + Figtree, Bebas Neue + Figtree) no longer look alike.
- Stacked row on Home: its preview shows what it is: under the plot, the small posters of the set or show focused in
  the row under the Home menu (it looked like submenus).
- Found while shooting the wizard's pictures: in a big library Kodi loads the list's art in the background from the
  top, so a title in the middle of 6127 films gets its poster and fanart some 30-40 s after the view opens (the Fused
  Glass List view showed an empty poster card until then). Not changed yet.

## 0.56.40
- Setup wizard (dialog 1173) in its original look, one setting per step, in the flow agreed on 2026-11-17
  (_src/wizard_05640.py; the user: "bring back the old wizard and update it based on what we agreed" and "One setting
  per step"). The look is the old wizard's: the dark ground, the step label, title and text top left, the option
  cards, the big preview with the focused option's name and text, the credits on the first step, the progress dots
  and the key hint (taken from the 0.56.39 files, kept in _src/wizard_classic_0539/).
- Steps: Welcome > Skin theme (Fused Glass, Aeon, Aeon Glass) > Start (Use the defaults, Customise, Keep my current
  settings on a re-run) > Fused Glass: Skin style, Menu background (Fused Glass style), Panel shadow, Focus highlight,
  Navigation animation, Toast expand from clock pill / Aeon: Skin style, Palette, Aeon accent colour (Aeon palette) /
  Aeon Glass: Skin style > Corner boxes, Library side strip, Settings strip, Library options (Aeon menu styles) >
  Home menu position, only the focused item's name, Home menu underline and Now playing (Aeon, Aeon Glass), Home
  vignette, Vignette shape > Fanart backdrop, Backdrop strength (with the backdrop), Library background, Fanart look
  (Fanart background) > Font combination > Home menu items > Add-ons (Install) > All set (Finish). Steps of the other
  themes are skipped: OK and Back jump over them and their dots hide. On entering a step the card in use has the focus.
- Previews: real box screenshots of every option in each theme (media/aeon/wizard/shots, 960 x 540; the 1920 x 1080
  shots in skin.glass/mockups/setup-wizard/shots05640, scratchpad session05640b.py); the font combinations and the
  add-ons are drawn over Lawrence of Arabia's fanart (_src/wizard_pictures_05640.py); the themes use Home shots.
- Theme, Skin style, palette, fonts and the focus highlight wait for Finish (they need the skin loaded again, and a
  reload leaves settings misread): Finish applies them and restarts Kodi on Linux (CoreELEC); elsewhere the skin
  reloads. Every other step changes its setting at once. Use the defaults sets the chosen theme's look (helper
  wizard.DEFAULTS: a placeholder until the user's per-theme defaults) and finishes; Customise on a first run starts
  from those defaults.
- The Skin-settings-look wizard built first (steps column, Skin settings rows and preview cards) is kept, not loaded:
  _src/wizard_settings_look/ and _src/wizard_settingslook_05640.py (--install puts it in 1080i); its box shots are in
  skin.glass/mockups/setup-wizard/box05640.
- Strings 32694-32719 (all 23 languages). Needs helper 0.3.107.

## 0.56.39
- Panel shadow is how high a panel floats (_src/shadow_lift_05639.py; the user: "increasing the size of the shadow
  underneath a panel so it seems it is raised higher, nothing to do with outline"). Before, the strengths mostly
  changed how dark the shadow was and Heavy added a lit rim; the preview drew its shadow under its picture and its
  swatches on the near-black column, so it showed nothing but Heavy's outline.
- Every panel shadow (110) now picks its picture from the strength: the shadow pictures are hollow rings (clear where
  the glass is) or soft solid shapes, and each gets Mild / Strong / Heavy versions (fg/<name>_<strength>.png): the
  panel's shape dropped and blurred, the hole kept exactly on the panel: Mild tight, Strong wider and lower, Heavy
  widest and lowest. Darkness x0.8 / x1.4 / x1.75 of Medium. No rim (FG_Edge / FG_EdgeM). Measured on the box under
  the preview card: brightness 129 (Mild), 121 (Medium), 78 (Strong), 50 (Heavy).
- The dialogs' baked shadows are drawn again the same way. The preview: the picture, the shadow in use, the card on
  top (40 px round it like the library's cards); its swatches are small cards on a picture with their own shadow.
  Help 32669 in all 23 languages. fg_material.py / expert_05628.py write the same from now on.

## 0.56.38
- The add-on information page in the Fused Glass style (_src/fgs_addoninfo_05638.py): the header names the add-on's
  type and the add-on; one grid with the icon (rounded) and its facts (version, type, installed, updated, status) in
  the icon column; right of the divider the summary, creator, a lifecycle notice, the description (or What's new) and
  then the actions as rows (Open, Configure, Auto-update as the gold switch, Dependencies, Enable / Disable,
  Versions, Update, Install / Uninstall, What's new): Kodi shows the ones it enables; the white bar on focus; Back
  closes. The page outside the style moved unchanged into AddonInfo_Classic (Includes_Dialogs.xml).

## 0.56.37
- The Add-ons window in the Fused Glass style (_src/fgs_addons_05637.py): no side card any more (the dark rounded
  panel on the left); one centred grid like the System screen: the toolbar (sort, Hide foreign / incompatible, Check
  for updates, Settings) is the grid's first row, 70 high, its buttons fill the cell (text centred, capitals, the white
  bar on focus; they sat low in a pill row before); then rows of 100 with the icon in the icon column (rounded), the
  name in capitals with the add-on's summary under it, the version at the end, the focused row outlined, the counter
  above the grid; "Repositories checked" on the hint line. Favourites and the other media windows use the same grid
  with wide pictures. AG_SubNavButton gains param fgs (only these windows ask for the style's look).
- "Home menu: only the focused item's name" works in every theme (_src/home_names_05637.py): the icon row Fused Glass
  used serves Aeon and Aeon Glass too, the focused icon's mark as in each theme's Home row (Aeon: a square line, Aeon
  Glass: the pill, with Home menu underline on); the row sits under ALL THEMES after Home menu position; its help
  loses "Fused Glass only." in all 23 languages.

## 0.56.36
- Short format names everywhere (_src/strings_05636.py, all 23 languages): the spotlights, two library views and the
  information page used long names (DOLBY DIGITAL PLUS ATMOS, DOLBY ATMOS, DOLBY DIGITAL PLUS / +, DOLBY DIGITAL,
  DTS-HD MASTER AUDIO, DTS-HD HIGH RES); they now read DD+ Atmos, DD+, DD, DTS-HD MA, DTS-HD HRA like the rest of the
  skin (TrueHD Atmos, TrueHD and DTS:X were short already). Each string is used only for its codec.

## 0.56.35
- Raw format names everywhere (_src/codec_aliases_05635.py): the library also holds the spellings its NFO files use
  (eac3 atmos, truehd atmos, truehd/atmos, dts-hd ma, dts_x, ac-3, dca, x264, avc, x265, h265, vc-1, hdr ...), and the
  skin only knew Kodi's names, so an episode showed "EAC3 ATMOS" instead of DD+ Atmos and "hdr" titles showed SDR.
  Every audio codec, video codec and HDR test in the skin (580: spotlights, views, info page, OSD, flags) now also
  takes those spellings; the label stays the one of Kodi's name. Kodi conditions cannot hold spaces, slashes or '+',
  so the aliases test the start and end of the name (eac3 ... atmos, dts-hd ... ma, dts ... x). Run it after any
  generator that writes codec tests.

## 0.56.34
- The Fused Glass style's context menu stands in the middle of the screen when it has no poster to show: Kodi often
  gives the menu no art (the box's List view loads none), and the rows then sat beside an empty icon column, off to the
  right. With a poster the grid keeps the icon column (fgs_dialogs_05632).

## 0.56.33
The Fused Glass style, round 3 (the user's notes of 2026-11-17, evening; _src/fgs_round3_05633.py,
_src/appearance_order_05633.py, fgs_dialogs_05632 updated):
- No smeared lines: a row's rule / divider picture was 8 px and Kodi stretched its transparent middle with linear
  filtering, so the line bled into a fade across the whole row (the "frosted gradient" in the context menu and Yes /
  No rows, faintly under every Kodi settings rule). fg/fgs_rowdiv.png is 16 px with a transparent margin (border
  2,0,0,2); fgs_rule_top / fgs_rule are drawn with a 2-px border.
- Everything but the focused row is dim, like the System screen: unfocused labels, values, icons 40 % (a switch's On 60 %); frame outlines and
  dividers 10 % (were 19 %); rules 7 %; group titles 55 %; the open category dims while the focus is in the list;
  unfocused pills 70 %, toggles gold at 70 %. The focused row has a full outline (fg/fgs_bar.png: top, bottom and
  right edge at 27 % with the white bar on the left), so its piece of the frame lights up with it.
- Select lists: the focused first row's top line (the list clipped it) and the row's right edge.
- The navigation animation plays in the style: Kodi's rows and categories, the dialogs' rows and the select lists
  animate on focus (FGS_RowAnim, Focus), Skin settings rows animate their name with the bar; Glow (it zoomed a shadow
  the style does not draw) brightens the row in (FGS_LandGlow).
- The System screen: the focused option's icon grows from 40 to 56 with a small pop.
- Home > System > Shortcuts: Files (Kodi's video sources) after File manager.
- The grid list's icon (favourites, add-on browser, media windows): 96 x 54 with rounded corners (fg/m96x54.png).
- Skin settings > Appearance: Library background above Fanart look; Fanart look (and its expert rows) only with a
  Fanart library background; the expert rows sit under what they change (Panel opacity / blur / tint under Skin
  style, Fanart opacity / blur / tint under Fanart look) instead of at the bottom of the page; every row's Up / Down is
  rebuilt from the page order (appearance_order_05633.py).

## 0.56.32
The Fused Glass style: menus and dialogs in the System grid (_src/fgs_dialogs_05632.py, canvas boards Ctx, Select,
SelectOverlay, Pick, YesNo, Fav; the user's notes there):
- Full screen, no card: the header top left (light word, bold word), the clock, one grid 360-1560 with the icon column,
  the divider at 810 and capitals at 846; rows of 70 under a faint rule; the focus a white bar on the divider with
  brighter rules; Back closes (no Cancel row); a key hint bottom left (32692 / 32693).
- Context menu: the item's name + OPTIONS; Kodi clones one button for every row (no icons per row), so the item's
  poster (or thumb) stands in the icon column. The skin's own View, sort, filter row stays first.
- Select: list 3 puts the number (01, 02 ...) in the icon column, list 6 the picture with label2 under the label;
  multi-select ticks in gold; the count (3 / 12) above the grid's right end; Kodi's OK / extra buttons under the grid
  when it shows them. The skin's palette and icon pickers and the track panel over video keep their look.
- Yes / No: the question in the grid's first cell, then the Yes / No / custom rows; the progress line under the text.
- Favourites (and the other Misc_MediaWindow lists): the add-on browser's grid list (FGS_View50); every kind of
  favourite shows its own icon (poster, channel logo, add-on icon) at its own shape in the icon column.
- Background: the item's fanart (else the settings backdrop) under the settings screens' dim, or (new row Skin
  settings > Appearance > Menu background, 9798, only in the style) the screen the menu opened on, dimmed
  (Skin.String(aeon.fgsdlgbg) '' / screen). Strings 32689-32691; its preview card (skin_previews p_dlgbg).
- fg/fgs_rowdiv.png: a dialog row's divider and rule in one texture (Kodi's cloned buttons cannot carry images).
- fgs_grid_05631 toggles() is repeatable (skin_previews writes its preview switches with the plain accent).

## 0.56.31 (helper 0.3.106)
The Fused Glass style: capitals in the settings lists, as in the mockup (_src/fgs_caps_05631.py):
- Kodi draws a label as written; capitals need an [UPPERCASE] tag or a font with style uppercase. Kodi's own rows get
  their text from Kodi, so only a font reaches them. The helper now writes uppercase twins uc_st_ui_24,
  uc_st_ui_24_semibold, uc_st_ui_24_bold and uc_st_small_20_semibold (the settings face + style uppercase) in its
  section block of Font.xml, in all 7 font sets; they follow the settings font choice. (A first try wrote them into
  that block by hand: the helper rebuilt the block at start and Kodi fell back to its default font.)
- Under the style the twins are used by: Kodi settings and add-on settings (categories, rows with their values, group
  titles, the level button, the add-on OK buttons) and Skin settings (categories, row names, the 66-px sub-section
  rows). New include Param_F (a font from a param, chosen at load like Param_W / Param_H).
- Skin settings categories in the style use 22-px capitals (uc_st_ui_22_*), the label 4 px left and 290 wide:
  MOTION, MEMORY, RESET is 303 px in 24-px bold capitals, 287 in 22 (room 284). _src/fgs_capsfit.py measures every
  Skin settings name and category against its room.
The grid, round 3 (_src/fgs_grid_05631.py, after fgs_caps_05631):
- Unfocused rules are fainter: 7 % white (the mockup's value, was 15 %), Kodi rows, categories, the add-on browser.
- A rule under every section title: Kodi's rows draw their rule at the top (fg/fgs_rule_top.png), so the first row under
  a group title draws its line; Kodi's group separator is a full-width faint line (it was 1058 wide and doubled the
  row rule). Skin settings rows get the same faint top rule (they had none) and the headings a rule above them.
- Skin settings: icons, names, hints and headings move 101 px left (icon at 503, 22 px from the column line like the
  category icons; the page title at 505, 24 px in like CATEGORIES); every name keeps its right end and gets 101 px more
  room (param namefgs on each Dlg_SkinRowChrome call). All 126 names fit in capitals.
- CATEGORIES and the page title sit in the middle of the title band (108-191): 8 px lower.
- The Skin settings scroll bars (9771, 9773, 9775) sit on the column line at 1500; they were at 1520, in the preview.
- Toggles are gold when on: fg_mark, the skin's one accent (the mark under the Home icon); Kodi rows (FGS_RadioTex)
  and Skin settings (FGS_ToggleOn / FGS_ToggleOnF).
- Renamed (all 23 languages): Landing animation -> Navigation animation (32415), Toasts from the clock pill -> Toast
  expand from clock pill (32474).

## 0.56.30
The Fused Glass style, round 2 (the user's notes of 2026-11-17; _src/fgs_round2_05630.py):
- Every settings row has its rule again: the unfocused rows' rule was drawn with a 24 % line tinted to 12 %, so only
  the focused row showed lines; now fg/fgs_rule.png (a full line at 15 %) under each row and category, the focused row
  with its brighter rules above and below.
- Rows are 70 high everywhere in the style: Skin settings, the Kodi settings pages, add-on settings, their categories,
  the section titles and the level button (flush with the bottom of the frame).
- The settings rows reach the right outline (Kodi settings 481-1814, add-on settings 481-1546); the scroll bar sits on
  the outline and, in every theme, shows only when the list is longer than its frame.
- The Kodi settings and add-on settings frame is ten rows (700) under the style: the list scrolled to a cut-off row
  in a 684 frame of 70-px rows; the frame lines, the list and the scroll bar grow by 16, the level button meets the new
  bottom. Player > Videos checked: it scrolls, the bar follows.
- Spin values get a pill split in two around the arrows (fg/fgs_spin_down.png / fgs_spin_up.png); on / off settings get
  the skin's own toggle (the Skin settings switch, accent track and dark knob when on, fg/fgs_toggle_on.png /
  fgs_toggle_off.png) instead of the check box.
- Add-on browser: the list in the System grid (frame, a rule under every row, the icon column and its divider, names
  in capitals, the version at the end, the bar on the divider), no card, the scroll bar on the outline (FGS_View50).

## 0.56.29
- The Fused Glass style, phase 1: Skin style in the Fused Glass theme is Dark | Clear | Frost | Fused Glass
  (Skin.String(aeon.fgmenu) = system; OK runs script.aeon.helper 0.3.105 skinstyle, which also sets the library glass,
  Dark for Fused Glass, and offers to start Kodi again going to or from Fused Glass). In Skin settings, the Kodi settings
  pages and add-on settings it draws the System screen's language (the canvas "Menus in the System style"): no cards,
  thin rules under the rows, the focus a white bar on the left edge with brighter rules above and below
  (media/fg/fgs_bar.png) instead of the white pill, the text in focus white, no glow under the focus. Expression FGS,
  the FGS_* twins of the ink variables, Aeon_Glass param fgs, FG_SettingRow / FG_SettingTemplates params fgs / pre
  (_src/fgs_05629.py). The open category in Skin settings carries the bar too, dimmed. Help 32574 names the fourth
  style and is shorter (two lines) in all 23 languages; the preview card lists it.
- The Fused Glass style's settings screens are one connected grid, as on the boards (the user: "the new menu sections
  are not connected, it's missing the vertical line between settings groups and you have huge gaps"): in Skin settings
  the Fused Glass offsets are off under the style, so the columns touch, and the frame and the dividers at 480 / 1500
  show; the Kodi settings pages and add-on settings use the classic page (one frame, the divider at 480) with the
  style's templates (params fgs / pre on Aeon_SettingCategoryTemplate / Aeon_SettingTemplates / Aeon_SettingRow, the
  level button's round param), the open category's grey overlay off (_src/fgs_flush_05629.py; run after fgs_05629.py
  and again after skin_previews.py).
- Still to come: rows 100 high and labels in capitals as on the boards, the help line's dotted i, the dialogs full
  screen in the System grid (context menu, select lists with numbers or pictures,
  yes / no, favourites), labels in capitals, and the style in the Aeon and Aeon Glass themes; then Fused Glass becomes
  the default style.

## 0.56.28
- Panel shadow (Skin settings > Appearance, Fused Glass, row 9529 where Library view theme was): Mild | Medium | Strong
  | Heavy (Skin.String(aeon.fgshadow), Medium the old shadow). Every panel shadow follows it, menus and library alike
  (FG_PanelSh_xx: half, as before, 1.6 times, e6), Heavy adds the lit rim (FG_Edge / FG_EdgeM) like the old Raised, and
  the dialog panel pictures have a copy per strength (dialogs/panel_fg*_sh*.png, AG_PanelTex). The menus no longer
  freeze their shadows to fixed values (fg_material.py to_menu).
- Expert settings (Appearance, all themes, at the end): a switch (Skin.HasSetting(aeon.expert)) that shows
  Panel opacity, Panel blur and Panel tint (Fused Glass), Fanart opacity, Fanart blur and Fanart tint, and Reset
  expert settings. Opacity and tint: five steps (-2 .. +2) around the style's own value (the fills' twins <name>X,
  FGX_* expressions, _src/fg_expert.py); Panel blur Off / Light / Default / Strong and Fanart blur Off / Light / Medium /
  Strong come from script.aeon.helper 0.3.104 (blur radius, aeon.fanblur); Fanart opacity steps the library fanart
  alpha (Aeon_VFanAlpha / Aeon_VFanAlphaG twins); Fanart tint Off / Light / Default / Strong is the Frosted look's colour
  wash (7 / 14 / 28 %). Preview cards for Panel shadow and the expert rows; help texts and 21 strings (32668-32688) in
  all 23 languages (_src/expert_05628.py, _src/expert_strings_05628.py).

## 0.56.27
- Skin style (the user's decision of 2026-11-17): the row Menu theme is named Skin style in all three themes (string
  32250, all 23 languages). Aeon and Aeon Glass: only the name changes. Fused Glass: Dark | Clear | Frost (Glass is
  named Clear, 32549); OK on the row also sets the library's glass (aeon.fgmat: none / clear / frost), so library
  views, Home panels, the Home bar, the player, Planner and the screensaver follow the style. The Library view theme
  row (9529) is hidden and Raised is gone with it; script.aeon.helper 0.3.103 puts aeon.fgmat in step at start. Help
  32574 says what the style covers; the preview card names Clear (_src/skinstyle_05627.py, _src/skin_previews.py).
  The Fused Glass style (the System-style menus) joins later as the fourth value; the setup wizard waits.
- System information in Aeon: the section column is a card of its own, so its outline closes the box on the left; the
  scroll bar shows only with the privacy policy, and only when the text is longer than the box (AG_Scrollbar params
  visible / showonepage).

## 0.56.26
- Media info chips (needs script.aeon.helper 0.3.102): the picker (Skin settings > Details > Media info chips) gets
  Video source (the sidecar's <video_source>, "UHD Bluray"), Video codec (<video_codec>, "HEVC") and Version (<edition>,
  "Theatrical Cut"), off by default; Source is named Source format (sidecar) and shows <source_format> ("UHD Remux"),
  else the source read from the release name. On the information page they sit in that order: video source, source
  format, video codec, version, then container ... The row counts 17 chips (_src/chips_05626.py, strings 32653 and
  32665-32667 in all 23 languages). The information page's chip row is 1290 px wide (was 1100), so the default chips
  and these fit in one row; with many more sidecar chips on, the last ones are cut at the edge.
- File manager in Aeon Glass: no hairline across the tops of the two cards.
- Checked on the box: Lawrence of Arabia's information page in Aeon and Fused Glass, the picker (17 rows), the File
  manager in Aeon Glass.

## 0.56.25
- Aeon Glass, Kodi settings pages (Interface, Media, Services, System, Player ...) and add-on settings: the
  highlight of the first category and the Settings level button (Basic / Standard / Advanced / Expert) now follow the
  card's rounded corners instead of sticking out square at the top-left and bottom-left. Kodi gives every category
  the same focus texture, so the first category's bar (focused, and faded while its settings have the focus) is drawn
  as a picture with the card's own corner (media/aeon/cat_tl380*.png, AG_CatGlassCorners, Aeon_TexCatFocus); the
  level button has its own textures with the bottom-left corner (media/aeon/lvl_bl380*.png, AG_SettingLevelButton
  round). The level button no longer reaches 1 px below the card. The open category is found by
  Container(3).CurrentItem, so add-on settings (which open with the focus in the list) are covered too.
- Aeon Glass, Skin settings: one rounded card for categories and settings, like the Kodi settings pages, instead of
  two cards inside a square hairline frame; the square outline around the categories is gone there too. The last
  category (Context menu) sits in the card's bottom-left corner: its highlight and open-category fill are masked to
  that corner (media/aeon/mask_bl360x70.png).
- Aeon Glass, File manager: the two-way arrow between the two cards (no bar; the Aeon bar stays Aeon only).
- Skin settings: the category Behaviour is now OSD settings (string 31728, all 23 languages).
- _src/aeonglass_corners_05625.py writes all of it (idempotent). Checked on the box in Aeon Glass (Skin settings, Interface,
  Media, Services, System, add-on settings, File manager; first category, open category, level button, last
  category) and in Aeon with Mosaic (unchanged apart from the OSD settings name).

## 0.56.24
- List view (510): an episode row shows its certificate in the left column, like a film row (Kodi keeps no
  certificate per episode; an episode's is its show's). Before, that column held the episode code ("6x01") while the
  title line also started with the number ("01. LA X (1)"), so the number showed twice. The number now stays in the
  title line only; a joined row reads "01-02. LA X" (_src/list_cert_05624.py).
- The Library view theme (Appearance, aeon.fgmat) changes library view panels only, no longer the menus: settings,
  dialogs, side menus, the keyboard, the context menu, information pages, toasts and the clock capsule on those
  screens take their fill, edge and shadows from the Menu theme alone (the values they had with the default library theme). The library copy of the shared
  card and the A-Z bubble keep following it, as do Home panels and the Home bar. _src/fg_material.py writes it
  (FG_MenuFill / FG_KbFill / AG_PanelTex without the material, FG_MenuPanel one dark strip, fixed twins FG_EdgeM,
  FG_FrostM, FG_PanelM, FG_ShadowColM for MENU_FILES, FG_LibCardFill, FG_ClockCapsule frost / edge params). The
  Menu theme preview card shows one tint per menu theme (_src/skin_previews.py). Help texts 32551 and 32574 reworded in all
  23 languages.

## 0.56.23
- Episodes in one file as one row (Skin settings > Details, row 9781, off by default; the approved board "1-2 LA X"):
  a season whose episodes share a video file (a double episode, three cartoons in one file) is listed by the helper
  with those episodes as one row: the numbers as a range (1-2, 36-38), the title once (part markers dropped), the plot
  once when the parts say the same, and the file's own running time (not the parts added up: Kodi gives every part
  the whole file's length). The row plays, resumes and counts as watched like the library's episode. Every view's
  episode number and episode code show the range ("S6 E1-2", "Season 6 | Episodes 1-2"); 29 range variables
  (_src/epjoin_05623.py, _src/epjoin_05623b.py, strings 32663-32664, a preview card). Fused Glass: the panels'
  "S6 E1 · Season premiere" kickers show the range, and a joined season's header reads "TV shows › Lost" over
  "Season 6" (_src/epjoin_05623c.py). Checked on the box in Aeon, Aeon Glass and Fused Glass (Lost season 6,
  Looney Tunes Cartoons season 1).

## 0.56.22
The user's notes of 2026-11-17:
- Pictures on the Home menu has a camera icon (media/aeon/icons/camera.png, the item's own icon; _src/camera_05622.py).
- Screensaver (with screensaver.aeon.fuse 1.3.0 and helper 0.3.99): rounds. Each round is N items (Items per round,
  10) drawn at random from the switched-on sources and mixed; one dot per item, the one on show ringed; then N new
  ones. The slide reads each item's own kind (_src/ss_round_05622.py).
- Start-up splash: a thin spinning ring in each look's accent instead of the progress strip (still with Reduce motion);
  a dialog that opens while the splash is up (CoreELEC's update question) waits below the screen with its buttons
  and focus (nothing is answered) and a toast on the splash names it; it slides in when the splash ends. Kodi's
  "Keep changes?" after a skin change is never held back (_src/splash_05622.py, string 32644). A held dialog opens on
  an invisible guard button: OK or Back there ends the splash only and focuses No, so "OK or Back skips" can never
  answer the hidden question; when the splash ends by itself No gets the focus too (_src/splash_05622b.py).
- Episode code: S1 E1, S1 | E1 and S1 • E1 besides 1x01 and S01E01 (row 9709 is five pills; _src/epcode_05622.py).
- Skin settings > Details > Media info chips (row 9780): a picker for the chips of the information page, Home's hero,
  the library panels and the Fused Glass panels (resolution, aspect ratio, HDR / Dolby Vision, Dolby Vision profile,
  audio format, audio channels, source) and new sidecar chips on the information page, off by default (container,
  bit rate, file size, subtitles, chapters, commentary, 3D). The Resolution / HDR / Audio rows keep working with it;
  the small chips inside list rows follow only those three (_src/chips_05622.py, strings 32645-32662).
- Skin settings previews: Ratings shows a high, a middle and a low score (green, amber, red with Colour on); Episode
  code shows all five; the four pictures behind the cards are bundled (media/previews, from Skin Backgrounds - Clear
  Design, CC BY-SA 3.0 US) and the skin no longer imports that add-on.

## 0.56.21
Pictures, from the approved canvas (board PicturesHome / PicturesWindow), in every theme (_src/pictures_05621.py):
- Home > Pictures: the newest photo of your picture sources behind Home; "Newest folder" with its name, the folder above
  it, how many photos and videos, the dates of its files, its four newest photos and "+N"; under the menu "Folders,
  newest first" (list 9311, helper ?info=picfolders), the last card opens the Pictures window. OK on Pictures plays the
  newest folder as a slideshow (the Pictures window when there is no picture); Down goes to the folders, OK on a card
  opens that folder. No picture source: "No pictures yet" and how to add one.
- Pictures window: a new view, Photos (519, the first view): the list on the left (date taken or file date and size),
  the photo panel on the right (the picture, its name, date / resolution / size, camera and exposure, the photos
  around it), a band with the folder, its number of items and the sort. The sub-nav (sort, slideshow, randomise) sits
  above the list and has a View button (Photos / cards / list).
- Strings 32629-32643 in every language.

## 0.56.20
The user's notes of 2026-11-17 and the Fuse menu theme survey (board VYbR9x9VrGpYHHQTowqYi4):
- Fuse menu theme, Aeon: the square parts inside its rounded cards are rounded - dialog buttons, outlined rows and
  chips, pills, the primary / outline buttons, the information page's flags and poster, the settings level button.
  Every skin-load switch that gave Aeon Glass a rounded texture and Aeon a square one has a third branch for Aeon +
  Fuse: Aeon Glass's shape with Aeon's colours (_src/fuse_survey_05620.py).
- Context menu: Aeon + Fuse focuses a 12 px rounded bar, concentric with its card; Aeon Glass + Fuse insets its rows like
  Fused Glass; in Aeon Glass the focused row's text is dark on the white bar (it was white on white).
- Aeon Glass: the media chips on the information page are rounded.
- File manager (Fuse): the strip between the panes is a pill. Browse for folder / Choose art's picker: 9 whole rows,
  no row cut in half. Select dialogs: the card follows the number of rows and stays centred. Kodi's Settings hub:
  Aeon Glass with the Fuse menu theme takes the Fuse hub. Interface / settings categories and add-on settings: one
  card (no line between the categories and the settings), the settings list to the card's edge (no empty strip).
- Aeon Glass legibility: the event log and system info have one dense card under the menu and the content; the file
  manager panes, favourites, profiles and the review viewer use a denser glass (AG_CardDense).
- Colour picker: rounded swatches with Fuse and in Aeon Glass (_src/fuse_survey2_05620.py).
- List view (510): the view's name ("LIST: TITLE") sits at the top of the info pane, over the title line; the focused
  row's pointer tip is a triangle in the bar's own colour (Aeon Glass showed a white diamond on its accent bar); the
  same for the episode / season rows' tips (_src/aeon_lib_round6.py, chain step 15; the chain script is now
  _src/rebuild_aeon_chain.py and re-applies the Aeon Glass rename).
- Home > Favourites, Aeon / Aeon Glass: an episode favourite shows the episode's thumb and a progress line on its card,
  and the spotlight shows the episode, the time left, a progress bar and the next episode, as in Fused Glass
  (_src/aeon_fav_ep_05620.py).
- Home spotlight: OK on a show (TV shows) or album (Music) opens it in the library (the lists had no target).
- Home spotlight window (Up from a spotlight's buttons): OK works again. Its first action closed the window and the
  next ones read ListItem after that, from Home; the item is now kept in Home properties before the window closes
  (Kodi checks every condition when OK is pressed, but fills an action's $INFO only when that action runs). OK on an
  episode (the TV spotlight lists recent episodes) opens its show in the library; films still play.
- List view (510): the poster pane shows the film's own poster file (poster.jpg or <file>-poster.jpg in its folder, the
  file Kodi has cached) as soon as the film has the focus. Kodi 22's art loader fills a list from the top, about 9 ms a
  film on this library, so a film half-way down 6,000 waited about 30 s for its poster (_src/aeon_lib_round8.py).
- Keyboard and number pad, Aeon Glass and the Fuse menu theme: the focused key is a rounded box (Done was a big square).
- Skin settings > Details: a new row, Media info from sidecars (off; script.aeon.helper 0.3.97 reads Curator Media
  Manager's <name>.cmm_mediainfo.xml first, else tinyMediaManager's <name>-mediainfo.xml); the page is a list that
  scrolls, like Appearance and Look (_src/settings_details_05620.py). The information page then shows the source as
  a chip (the chip row is wider) and three lines in the Ending at card: source / edition / size / bitrate; the main
  audio track, the audio and commentary counts; subtitles (SDH) and chapters (_src/mediainfo_skin*_05620.py).
- Premieres and finales: the Planner tags a next episode SERIES PREMIERE, SEASON PREMIERE, MID-SEASON FINALE, SEASON
  FINALE or SERIES FINALE (instead of EPISODE) and adds it to the spotlight line; the next-episode line under an episode
  / season list ends with it (_src/aeon_lib_round7.py, chain step 16; the helper asks TMDb Helper for the episode type).
- Fused Glass player: the audio / subtitle flags come from Language Flags Rounded (resource.images.languageflags.rounded,
  optional) when it is installed, else from the colour pack, else the code as text.
- Screensaver: the pager's dots stand for the sections it cycles through (films, shows, albums, in cinemas, airing today,
  airing tomorrow), the one on show ringed; it hides when there is only one. A list with a single item (one episode
  airing today) left a lone ring (screensaver.aeon.fuse 1.2.2).
- Skin settings > Spotlight & widgets > In cinemas now: films from (new, Everywhere by default): the United States, or
  the United States and one more country. TMDb Helper's US list holds every film with a US release (many Indian
  ones); with a country picked only films made in the US or there stay (Aeon Fuse Helper).
- Home > Power in Aeon and Aeon Glass: the Fused Glass Power page in Aeon dress, on the Power item's own fanart. Up,
  OK or Down on Power go to its round actions (Shutdown timer, Sleep, Restart Kodi, Reboot, Reboot to Android,
  Shut down with OK twice, Log off, Screensaver); the timer is Aeon's option picker (pills in Aeon Glass, the
  clock on a glass card). The old Power list (9338) is no longer opened.
- Start-up splash, all themes: AEON FUSE over Home while it loads, with Library, Weather, Home rows and Live TV
  guide ticking off; it ends when they are done or after 20 s, OK or Back at once. It is part of Home, so Home's
  rows keep loading behind it. Not after a skin reload.
- Planner, Week view in Aeon and Aeon Glass: each day column shows a spinner and Loading while its list loads, as
  in Fused Glass.
- The Kodi System screen looks as in Fused Glass in every theme: on the fanart backdrop (Skin settings > Fanart
  backdrop still turns it off), and its rows land with Fused Glass's landing animation (pop by default; Reduce
  motion stops it). The Settings hub and the other screens built from the same rows move the same way.
- Skin settings previews: real fanart behind every card (Skin Backgrounds - Clear Design, now an optional dependency, when it is installed, else the
  library fanart of the settings backdrop); Library view theme, Menu theme (Fused Glass), Home vignette and Backdrop
  strength show the real panel at its real size, and every option row (also Library, Screensaver and Widget screens
  background, Corner boxes, Home bar, Focus highlight) a line per option: a swatch over the same picture, its name and
  its number (tint, or how much of the picture shows, for the theme, strength and material in use; a soft dot where
  the picture behind is blurred).
- Skin settings > Appearance > Menu theme, Aeon Glass: the preview shows its card with the accent bar (Aeon Glass) or
  the inset pill (Fuse); it was an empty card. The denser glass is a little denser (65 %).
- Information page: the media chips are no longer cut off after about 700 px (UHD REMUX showed half): the hero's
  text column list was 700 wide and clipped the wider chip row inside it.
- List view: the local poster shown while Kodi still loads the art is <file>-poster.jpg first, then poster.jpg, the
  order Kodi uses; a folder with both showed the other poster first and swapped when the art came.
- Planner, Week view: a card's second line names the premiere or finale in place of the episode's title
  (3x01   Season premiere); before, only the list rows showed it.

## 0.56.19
Found by the Fuse menu theme survey (2026-11-16):
- Skin settings, all three themes: 0.56.18's wider option pills overlapped their neighbours by up to 27 px (the gaps
  between segments were measured against the moved ones), so in Watched indicators "Watched" still ran into the Both
  pill and the Menu theme options looked unevenly spaced. The pills are laid out again without overlaps; a picker now
  grows to the left as far as the English setting name allows (16 px before the track), and a longer translated name
  ends in "..." there and scrolls while its row has focus (Dlg_SkinRowChrome namew, _src/picker_names_05618.py).
  Every English option has at least 16 px a side (Unwatched 16), except the seven Landing animation options (10).

## 0.56.18
The user's notes of 2026-11-16 (evening):
- Version / set panes (List, Banner list, Compact list), Aeon and Aeon Glass: changing version changes the band's media
  info, run time, rating and Ends, the title line and the plot. In a library window ListItem.* is always the main
  list's item, also while a pane has the focus; the panes now read copies of those labels per pane
  (Container(<pane>).ListItem.*). The up / down pointers are smaller (pill 36 x 24, chevron 18; the List pane 44 x 28 in
  the Compact list's style: light pill, dark chevron); the Compact list pane's parts no longer overlap (title, version,
  play ring, counter, pointers) and Down moves through the versions (_src/aeon_lib_round5.py, chain step 14).
- The Glass theme is called Aeon Glass: the theme picker, the help lines that name it (all languages), headings, View
  settings and the setup wizard. Kodi's theme value stays "Glass" so the setting people have keeps working
  (_src/rename_aeonglass_05618.py).
- Skin settings, all three themes: an option picker's first and last pill reach the ends of its track, so the selected
  end option covers the grey strip completely (_src/pickers_flush_05618.py); every option is at least as wide as its
  longest label (Latin-script languages) plus 16 px a side where the setting's name leaves room (Watched indicators:
  "Unwatched" no longer touches "Watched") (_src/pickers_fit_05618.py).
  Every picker ends on the same line (860), the five with their own right edge moved to it.
- Information page, Aeon Glass: rounded cards like the focus ring around them (also the full-screen review); the hero
  picture fades in from the left into the glass (Fused Glass's mask, no fade strip with a hard edge, the soft shade
  over its foot); the focus glow no longer fills the focused card (the "frosted"
  plot card: aeon/ring_glow_out_<r>, _src/ring_glow_out.py); Recommended / Similar posters and the review cards are
  rounded in Aeon Glass and with the Fuse menu theme (_src/aeonglass_info_05618.py).

## 0.56.17
The user's fourth round of notes (canvas HJTtCDChVWkaZZAyt76wJA, board Built05616):
- Compact list (524), Aeon and Glass: the poster is as tall as the landscape art (186 x 280 beside 498 x 280, the two
  across the 700 px column); the version / set pane in the poster's place is scaled with it. The studio / network logo
  sits at the bottom left of the column, under the plot, and is larger (400 x 90); the title, credits and plot move up.
- Poster wall strip (and the other walls with the same strip): the studio logo is larger (380 x 92, was 300 x 72).
- Music Compact list (513): album and artist rows lose the ring / note icon, and their names start where it was
  (96 px more room for long names); songs keep the track number; the header row over the list follows.
(_src/aeon_lib_round4.py, step 13 of the Aeon view chain.)

## 0.56.16
The user's third round of notes (canvas HJTtCDChVWkaZZAyt76wJA) and "actors shall be squares in Aeon theme in all views
and windows":
- Aeon theme: people are square: Circles (536) for everyone (actors, directors, music video artists) and the cast on the
  item information page (a frame in the accent while focused, the photo from its top); Glass and Fused Glass keep the
  round portraits (_src/aeon_lib_music.py, _src/misc_05616.py).
- List (510), Aeon and Glass: the title line and plot have their own pane (0..216) and the list pane starts under it,
  so the rows no longer run under the text (seven rows, the focused one where it was; the plot three lines). An
  episode's line names its genres too. While the version or set pane has the focus, the line and the plot are that
  version's / film's (with the version's name) (_src/aeon_lib_round3.py).
- Banner / Compact list band: the genres after the year. Ends only for films, episodes and music videos; a show writes
  its status there (Continuing, Ended ...), and so does the item information window instead of "Ends at" (its
  "fits before midnight" tick also only for what plays; a show without a run time still shows its status).
- The version / set panes' bands (List, Banner list, Compact list) as text with bullets too.
- Music Compact list (513): the track count and its note centred on the row like the run time.
- Skin settings, Aeon menu styles: Bridge's palette tile is as tall as the title band twice (its squares meet the band's
  edge; the side column starts under it); the category rules are the settings rows' neutral rule (no slate blue); the
  light frame marks the box the highlight bar is in (categories or settings) (_src/ms_menus.py,
  _src/settings_outline_05616.py).
- Helper 0.3.96: Kodi froze on the box after a version was added to a film (a lock-order deadlock between the film
  list being rebuilt and the helper reading a list label); the helper now reads list labels on Kodi's main thread.

## 0.56.15
The user's second round of notes on the Aeon library views (canvas HJTtCDChVWkaZZAyt76wJA) and their requests:
- Aeon / Glass info areas as text (the user: "let's not use square badges, only text labels with bullet point
  separators. also add hh:mm left if in progress after the Ends at time"): the List band, the Banner / Compact list
  band, the wall strip (Poster, Landscape, Square wall, Cards, Showcase), the Low list / Flix chips and the Episode list
  panel write "1996  •  RATED R  •  105 MINS  •  ENDS 17:10  •  0:07 LEFT" and "DTS 5.1  •  1.78:1  •  FULL HD"; the
  status says IN PROGRESS where the time left is in the facts (helper 0.3.95, string 32606) (_src/aeon_lib_round2.py).
- List (510): the line over the rows is the title, year and genres with the watched status beside it; the rows lose the
  audio / aspect / HDR badges (the band has them), Aeon's resolution pill stays on the far right; no year in the band.
- Episode list and Flix: NEXT EPISODE in the yellow highlight colour.
- Compact list (524): the list 1000 wide, the poster / picture / text column 700 (longer titles fit); the network logo
  under the picture on the right (Banner list too, under its picture); the progress line on the picture; a ring on the
  poster with the share of watched episodes (a show or season; an episode list's own share from the helper).
- Music: the List view is called Compact list for artists, albums and songs (picker and heading; its picker line "Rows
  with A-Z keys"); Fanart wall no longer offered for albums (Fused Glass never had it, so it fell back to the list).
- View names: the Aeon / Glass heading of a video view uses the picker's name per content (Show posters, Season posters,
  Episode wall, Season poster wall combined) (_src/views_05615.py).
- Music side strip: Artists, Albums, Songs and Genres at the top, as the top menu; the one on screen says Current
  (_src/libpanel_music_05615.py).
- Skin settings (_src/settings_05615.py, _src/aeon_lib_round2b.py):
  - Appearance (Aeon / Glass): Home menu underline Off | On, the accent line under the focused Home menu item as in Fused
    Glass (off by default).
  - Appearance (all themes): Fanart look Dimmed | Frosted for the library backdrop; the theme's own until chosen (Aeon
    dimmed, Glass and Fused Glass frosted).
  - Ratings: Ratings shown as Icons | Text; every rating row in every theme shows the provider's name instead of its icon
    in Text mode. The preview lists the providers one under the other (it cut off after two), with icon or name and the
    number in the rating colour (the name too as text).

## 0.56.14
- Home menu, Power: OK opens the Power menu, as Up does (the user: "Pressing OK shall show the bigger menu - same as
  when pushing up. The smaller menu ... is thereby no longer needed"). Kodi's small shutdown menu stays reachable through
  the Power menu's own "Power menu" entry. (Kodi runs every action of a static menu item's OK and reads list items
  there as empty, so the item carries the Up key's focus moves with conditions on the theme and the entry count.)
- Aeon theme library views, first part of the list row and info panel rules (canvas HJTtCDChVWkaZZAyt76wJA, the user's
  notes on it), Aeon and Glass themes (Fused Glass unchanged):
  - List (510) rows: Aeon's resolution pill, then audio (short names), aspect ratio and HDR (with the Dolby Vision
    profile) as Aeon pills, right-aligned before the watched mark; the mark in its own column right before the run time;
    while in progress the progress ring and the time left in the accent colour. Over the rows: the kicker and the plot.
    The band: the facts line gains the year and Ends; the status line (mark, Unwatched / time left / Watched) starts the
    chips row; one audio chip; HDR with the profile and no SDR chip; the studio's logo or name at the right
    (_src/aeon_lib510.py).
  - Episode list (511) and Season list combined 3 episodes: line 2 of each row "EPISODE 4 · date" and the chips; the mark
    and run time / time left in fixed columns. The panel: the picture fills its column (Episode list), name,
    "SEASON 3 | EPISODE 1 | date | minutes | ENDS", ratings and certificate, the status line, chips without the codec,
    the plot. The network logo under the poster and the next episode under it (helper 0.3.94) (_src/aeon_lib511.py).
- Aeon theme library views, the rest ("and then build the other ones"), Aeon and Glass themes:
  - Compact list (524): the mark right before the run time in one column (films and episodes), the rating after it;
    the ring and the time left while in progress; TV shows and seasons keep their mark behind their count columns. The
    Banner / Compact list band as the List's: year and Ends, the status line first, one audio chip, no SDR, the
    resolution last, the studio's logo or name left of the clearlogo (_src/aeon_lib_lists.py).
  - Banner list (522): the status on each banner's top right, in a dark square: the eye, or the yellow ring while in
    progress (_src/aeon_lib522.py).
  - Low list (527): rows as the List's (chips with the resolution pill on the far right, the mark in the List's column,
    ring and time left); the panel: the episode picture beside the clearlogo, the network logo at the bottom right,
    episodes' facts "SEASON 3 | EPISODE 1 | date | minutes | ENDS", films' "year | minutes | ENDS | genres", the status
    beside the certificate (no run-time chip, it is in the facts). Flix shares the info chips: status after the
    certificate, one audio chip, no SDR, the resolution last (_src/aeon_lib_lists2.py).
  - Poster wall, Landscape wall, Square wall, Cards, Showcase: the info strip as the Poster wall board: kicker
    (FILM · genres, TV SHOW · genres, SEASON · show, MOVIE SET) with the studio's logo or name on the right, the title,
    ratings · year · certificate · run time · ENDS · status, the chips (resolution last), the plot (_src/aeon_lib_walls.py).
  - Album list (532) and Song list (533): the focus bar meets the cover column; album rows "artist · year · genre" (no
    more album name twice), the release type (EP / SINGLE / LIVE), the track count with a note and the length; the
    column under the cover: the artist's clearlogo (the name when there is none), the kicker in gold, the facts
    (year · tracks · length), the review or biography in the Unicode twin font, so phonetic letters no longer show as
    boxes. Album wall, Cover showcase, Artist wall: the same kicker, facts and text, the artist's clearlogo on the right.
    List (513): the artist's clearlogo over the facts (artists, albums and songs). Circles (536): music video artists
    as squares in the Aeon theme (_src/aeon_lib_music.py). Helper 0.3.94: the focused album's track count for those
    walls too.
  - Planner (537): the rows meet the clock box and the A-Z strip (Fused Glass keeps its spacing); Flix (528): the next
    episode (S3 E5 · WED 18 NOV) and the network logo under the plot (_src/aeon_lib_other.py).
- Fused Glass music views: the heading names the view by what it shows (the Album wall showing artists is the Artist
  wall), as Aeon and Glass already did.
- Fixed: Look > Settings strip > Permanent never showed the strip in Aeon / Glass (expression Aeon_StripPerm had one
  closing bracket too many; Kodi logged "Error parsing boolean expression" and read it as false).

## 0.56.13
- TV guide: the channel number you type (Kodi jumps to it after a moment) shows while you type it, so you no longer
  type blind: "CHANNEL 25" in an accent-colour pill over the channel group pill in Fused Glass (it moves with the guide over the
  playing channel), in the accent colour in the corner above the channel column in Aeon and Glass
  (PVR.ChannelNumberInput; _src/fg_livetv.py writes the Fused Glass part).

## 0.56.12
The user, on the add-on shots and the Glass menu mockups (canvas RfMMKDTnbQCAG46Y3hpn9j):
- Add-on browser: every screenshot an add-on names (up to 20) is in the shots panel, which scrolls ("i can only see 6
  out of the 10 screenshots for our skin addon").
- Menu theme in Fused Glass: Dark | Glass | Frost ("A. Darker will be the new Glass theme, and you will add B. Frost
  as a third option"). Glass draws its cards halfway from the old Glass to the Dark fill (b222262e with the Frost and
  Raised materials, 93171a20 Clear, c8171a20 Dark material). Frost (new, aeon.fgmenu = frost) has Glass's see-through
  menus on a light cool tint over a blurred picture. Kodi cannot blur the screen, so the blur is the backdrop's: the
  settings windows show the blurred copy of their backdrop (helper 0.3.93), and a library window lays the blurred copy
  of its backdrop over itself while a menu dialog is open (context menu, select, yes / no, keyboard, number pad, file
  browser, add-on settings, view picker...). Information pages and windows without a blurred backdrop get the tint
  alone. Dialog panels baked per material: dialogs/panel_fgf*.png (_src/fg_frostmenus.py, _src/fg_material.py).
- Skin settings: Look > Material is now Appearance > Library view theme, right under Menu theme ("it should really
  be next to Menu theme"). Appearance and Look are lists that scroll, with a scroll bar when the rows do not fit
  ("Create scrollbar if needed"). Appearance: Skin theme, then the theme in use as a heading over its own rows (Fused
  Glass: Menu theme, Library view theme, Focus highlight, Landing animation, Home menu names, Toasts from the clock
  pill; Aeon / Glass: Menu theme, Palette, Aeon accent colour, Corner boxes, Library side strip, Settings strip,
  Library options, Now playing on Home), then All themes over the shared rows (Fanart backdrop, Backdrop strength,
  Library background, Home menu position). Look keeps the rows every theme has. Now playing on Home is hidden in
  Fused Glass instead of greyed out (it does nothing there). _src/settings_sections.py; the previews follow their rows.

## 0.56.11
The user's notes on the box shots of 0.56.10:
- Every list row: the chips right-aligned, ending just before the run time ("move all chips towards duration and right
  align them, to give space for genres", "this is a general comment"): List, Low list, Episode list and the season
  lists' episodes, Episode combined (under the run time); a row in progress (wider "16 min left") has them further
  left. The grey line (year · genres, Episode N · first aired) reaches up to them. Variants keep them flush right
  whether or not the item has HDR or a known certificate.
- Studio logos: the first of the item's studios that has a logo in the studio pack (the helper reads the pack's
  index); when none has one, the studio's name stands there as text ("just put a text label then"). In the List,
  Compact list / Flix / sets, Season wall, Season list combined 3, Episode combined panels and the walls' band.
- Showcase and the walls' band: the clearlogo stands at the right of the name column, beside the kicker, ratings and
  facts; the facts, status line and chips move up ("Put clearlogo here instead to give more space for the mediainfo").
- Music: an album without a review shows its artist's bio, a song list its album's review or the artist's bio
  ("Album or artist bio"; the helper: aeon.m.bio).
- Add-on browser: the side card is the same card as the list beside it (Menu theme), without the bottom fade over
  the list in Fused Glass ("why is this panel different from other panels?"); the screenshots are a panel: Left from
  the list moves into it, OK shows the picture full screen ("need to be able to navigate to screenshots and view them").
  The column of the side card is 4 px wider each side, so the white focus frame round a screenshot is not clipped on
  its left (the user's photo).

## 0.56.10
The user's notes on the box shots of 0.56.9:
- Row chips keep their text 6 px inside the outline ("some labels inside chips clip the outline"); audio chips are
  112 wide in every row (TrueHD Atmos, DTS-HD MA 5.1 fit).
- Compact list: the chips sit right before the run time (further left for an item in progress, whose "16 min left" is
  wider), so the titles get the room ("why the huge space between chips and duration??").
- The walls' info band (Showcase, Wall, Episode wall ...): the name column is 560 wide (was 380), the plot narrower
  ("way too cramped, make plot narrower"); the facts line no longer cuts at "Ends".
- Studio / network logo in Episode combined (under the season's facts) and Season list combined 3 (under the
  episode's panel, whose plot is longer now: "there is more space for plot and a studio icon"). A film whose studio
  has no logo in the studio pack (2 Days in the Valley: Redemption Productions) shows none.
- Music: track counts in the rows are the number and the song icon, in Fused Glass (List, Album list) and in the
  Aeon / Glass music views ("use the song icon instead of tracks label in general for all views").
- Add-on category icons drawn from Font Awesome Free at 512 px (sharp at panel size; the repository icon was "one
  mangled icon"); media/DefaultAddon-icons.txt names the licence.
- Fused Glass add-on browser: the side panel is a glass card ("has to be on a card background"): the fanart (or a
  plate with the icon) at the top, the icon in its corner, name, status, the add-on's description (new), then the
  screenshots right under it ("bring them up closer to the icon, add addon description").
- Hide foreign / Hide incompatible are the same pill as Check for updates, with a dot in front that is gold while
  the filter is on ("they should look the same as that check for updates button").
- Add-on settings show a blurred copy of the add-on's fanart, so the panels read as on top of it (Skippy's fanart
  has a light card in the middle that seemed to sit over the category panel).

## 0.56.9
- Fused Glass info panels follow one rule (the Info panel rule board; the user's notes: "DV type chip too, e.g. P7
  FEL or P5 or P8.1", "Aspect ratio!", "Missing watched status dots and circle progress in general"). In every
  panel (List, Compact list, Flix, Low list, the walls, Showcase, Episode list, the season lists, Episode combined):
  - kicker: films and shows their genres, seasons the show, sets "Movie set" (was "Sets"), episodes "S3 E1" and
    "Season premiere" / "Series premiere" on the first episode (the header names the show);
  - facts in one order: rating sources · year (episodes: first aired) · certificate · run time (1h 13m) · Ends;
    seasons "2026 · 4 Episodes"; the watched counts left the facts line;
  - a status line, new: the watched mark (dot, progress ring, tick, as the rows) and its words: "15 min left" for
    an item in progress, Watched, Unwatched, "0 of 20 episodes watched", "0 of 4 films watched";
  - the chips of the row in the row's order and names: resolution (1080, 4K), audio (DD+ 5.1, TrueHD Atmos),
    aspect ratio (now in every panel), HDR; no SDR chip; Dolby Vision with its profile, "DV P7 FEL", "DV P8.1",
    "DV P5", from the film's .nfo or the media manager's mediainfo file (the helper's aeon.dvp, which only the Aeon
    views used); the row in focus shows the profile in its DV chip too; no genre chips;
  - Episode combined: "1h 13m" instead of "74 min"; the still keeps its bar, its words moved to the status line.
- Music: album facts are year · tracks · length · genres; the release type only when it is not an album.
- Add-on browser, add-on information and add-on settings show the add-on's fanart behind them (over the backdrop,
  dimmed the same way); the settings dialog finds it through the helper (aeon.as.fanart).
- Fused Glass add-on browser: an add-on with fanart shows it as a 16:9 card with the add-on's icon in its corner,
  then name, status, plot and up to six screenshots; without fanart the icon tile, a shorter plot and three
  screenshots. Screenshots come from the helper (aeon.ab.*): the add-on's addon.xml, or Kodi's add-on database
  for the repository being browsed.
- Add-on categories and the browser's menu entries have icons: Kodi's 44 DefaultAddon*.png names as dark tiles
  with the af3 glyph (video add-ons, context menus, services, look and feel, weather ...), _src/addon_icons.py.
- Back in the add-on browser goes up one folder, as before; it leaves the window only from the folder it was
  opened at (the jump to Home came from a test that opened the browser directly at "all add-ons").

## 0.56.8
- Fused Glass library lists follow one row rule (the List row rule board; the user's notes: the aspect ratio chip
  "in general is missing", keep the bold, bigger run time, the tick white "is better" than green). In List, Low
  list, Episode list, the Season lists' episodes, Compact list and Episode combined:
  - line 1 the title (an episode's own title), line 2 the grey line (episodes: "Episode N · first aired") and the
    chips after it: resolution, audio, aspect ratio, certificate, HDR (DV / HDR10+ / HDR10 / HLG), for films and
    music videos as well as episodes; a row gets as many as fit, the aspect ratio in every row (numbered and Compact
    rows: resolution, audio, aspect);
  - at the right the run time, bold as before; an item in progress shows its time left there ("16 min left") on
    every row, not only the focused one; shows, seasons and sets watched / total;
  - the audio chip says "DD 5.1" for Dolby Digital, like "DD+ 5.1" (the long name did not fit narrow rows);
  - the mark (ring, tick, dot) last, at the far right; the tick is white, and the ring track / tick stay light on
    the Frosted and Outline focus bars.
  - the progress bar on the numbered rows' title line, the caps kicker of Episode combined and the Compact list's
    year column are gone (the still keeps its bar; the side panel has the year).
- Watched ticks show again: Kodi has no ListItem.IsPlayed (it always read false), so every tick that tested it, in
  the Fused Glass marks and five Aeon includes (27 places), never appeared; they test the play count now.
- Fused Glass Add-on browser and the generic list windows (View_50_List / _L): the scroll bar sits beside the card,
  12 px out, not in the focus bar's 12 px gap, where the bar covered its left edge (the user's box photo).
- Music: the Album list shows each album's track count at the right (as the List view does), not the year again;
  the List view's counts read "11 tracks" like the other rows' right column; the Song list has no play count.
- Helper 0.3.89: timeleft.py keeps the time left of every film / episode / music video in progress
  (Window(Home) aeon.left.<k>.type / id / text, 40 slots, refreshed after playback stops and when the library
  changes); the track counts for the Album list rows (aeon.tc532.<row>).

## 0.56.7
- Names in every script: music names and Live TV names (the user: Japanese artist names showed as rectangles; then
  "changing fonts for artists and live tv, we really need to ensure that it is also done for all the font sets").
  Kodi has no fallback font for a missing character, and the skin's families have no Japanese, Chinese or Korean
  (Figtree no Cyrillic either); Kodi's own arial.ttf (DejaVu Sans + CJK) has them. Every skin font that a name label
  uses has a twin un_<font> in every font set (Kodi's arial.ttf at that set's size, bold where the font is bold or
  semibold; 19 twins), and those labels use the twin: artist / album / track names, header, card caption and row
  subline in the Fused Glass music views (not the A-Z letters); channel names and programme titles everywhere, and
  item names in the Live TV windows, dialogs and their Fused Glass parts. Other text keeps the skin's font.
  _src/fg_cjk_names.py (the box keeps its own Font.xml: run it on a copy and put that back).
- Fused Glass TV channels: the sort / filter row is drawn over the channels card (its glass dimmed the row, strongly
  with Material Dark): Misc_PVRSubNav, drawn after FG_PVRChannels.
- Fused Glass: the left settings strip has a frosted base under the rail's tint in every material (the views' ground
  and the blurred backdrop), so the list behind it no longer reads through.
- Fused Glass music List view: the Aeon theme's cover timer (aeonmusiccov) moved the album cycler a second time per
  turn; it runs in Aeon / Glass only now (the cycler moves one album every 5 s).

## 0.56.6
- Skin settings > Backgrounds > Home vignette: Off | Light | Medium | Strong | Heavy. Strong is new, between Medium
  and the old Strong, which is now Heavy (the user: Strong "is a bit too strong, i want something in the middle";
  "the strong we have now shall be called Heavy and be the strongest one"). Skin.String(aeon.vignette): e = Strong
  (vignette cc, Home rows' scrim b0), d = Heavy (as before), so a stored Strong keeps its look under the name Heavy.
  The five choices share the same pill (the row's name needs the room on its left). String 32603 Heavy, all
  languages. _src/vignette_heavy.py.
- Fused Glass: Skin settings rows the Aeon and Glass themes only use are hidden: Look > Library side strip (Dark /
  White) and Appearance > Corner boxes; the rows under them move up and Up / Down go round them.
  _src/fg_aeon_only_rows.py.
- Fused Glass: the side strips on both sides are one material (the user: "does the settings side strip have the same
  material as the clock/A-Z strip ... they should be the same"): the library settings strip / View settings / Skin
  settings rail (FG_MenuPanel) and the clock / A-Z rail of the views (FG_Strip) are a step denser than the cards:
  b32a2e38 Frost / Raised, 9914161c Clear, cc14161c Dark; the blurred backdrop is under both in Frost / Raised / Dark
  (the left strip got its own layer). _src/fg_material.py, _src/fg_panel_blur.py.
- Fused Glass toasts from the clock pill: one contiguous pill in every material (the user: under Glass "it shows the
  left rounded edge of the clock dock so the illusion breaks"). The pill was a stretched band with whole round caps
  over its ends, over the window's own clock capsule: with see-through glass the overlaps and the capsule's round end
  showed through. Now half caps, band and rim never overlap (fg/pill64*.png), the pill takes the capsule's material,
  starts and ends as exactly the capsule, and the window's capsule hides while it shows. _src/fg_toast_pill.py.
- Information screen: moving between the rows (Cast, Recommended, Similar, Reviews) glides (340 ms, easing in and out)
  instead of snapping (200 ms, fast start). Fused Glass: the More row's buttons (More by this director, My rating,
  Versions ...) look like Play / Trailer / More: 56 px line pills, the focused one white with the gold ring round it
  (in its own picture, fg/btn56f.png, as the row sizes its buttons to their words) and zoomed to 105 %.
  _src/fg_morebuttons.py. Recommended / Similar titles that are not in the library stay dimmed except the one in
  focus. (The information cards follow Menu theme; the user keeps that: Glass gives glass cards.)
- Fused Glass music views: the album cover cycler moves on every 5 s from a skin timer (Timers.xml aeoncycler).
  Kodi's autoscroll counts its time only while the list is redrawn, so in the List view it stepped twice 0.6 s apart
  and then waited, nearly skipping every other album; and the Aeon theme's cover timer (aeonmusiccov) moved the same
  list again in Fused Glass (now Aeon / Glass only).
- Fused Glass A-Z rail, every view: the white focus circle (36 px) was cut by the edge of the letter list (26 px rows)
  on # and Z; it is drawn outside the list now, one per letter slot. # jumped to the List view's list (510) in every
  view; now to the view's own list. _src/fg_rail_fix.py (fg_lib.rail writes the same).

## 0.56.5
- Fused Glass: glass is glass in every library view, in the chosen Material (the user: views looked like "dark
  overlay" panels while Episode combined looked like glass; "the episode combined looks like i expect glass to look
  like for all views", "if a user applies another material then the panels shall use those instead").
  - The panel drop shadows (fg/sh16-32, FG_PanelSh_xx) were blurred rectangles solid in the middle, drawn under the
    see-through cards: every card sat on a sheet of up to 55 % black whatever the material. They are now an outline
    round the card only (fg/sho<r>.png: the same soft fall-off with the card's shape cut out, 40 px round it, no
    drop offset), for every card that had one: library views, Home, player panels, the keyboard, the shared menu /
    dialog card. Shadows under opaque things (posters, the video window, the skip pill) stay. _src/fg_glass_shadows.py.
  - The blurred backdrop under the cards (Material Frost, Raised, Dark) was drawn through four hand-made masks (List,
    Episode list, Season list combined 3, the A-Z rail), so every other view showed the backdrop sharp through its
    frosted cards. Every card of every library view now has its own blur layer under it, masked to its shape
    (fg/bmp_*.png), in its own group, so it shows, hides and slides with its card ($EXP[FG_PanelBlur]: fanart
    backdrop, Material not Clear). _src/fg_panel_blur.py. Clear still shows the backdrop sharp.
  - The side strips (library options strip, View settings, the Skin settings rail) are dark in every material and
    menu theme (the user: "glass shall be glass, except for the side strips, they can be dark"; with Glass + Clear the
    strip was a 30 % tint): FG_MenuPanel fa2a2e38 with Frost / Raised, else fa14161c (98 %: the list
    behind does not read through). _src/fg_material.py.
  - Flix keeps its cinematic scrims (it has no cards).
  - Order after the view generators: fg_lib*.py / fg_epcomb.py, then fg_material.py, fg_glass_shadows.py,
    fg_panel_blur.py.

## 0.56.4
- Home: the strips under Movies, TV shows and Music load once and keep their titles, load ahead after Kodi starts,
  and show that they are loading (the user: Down on a Home item did nothing while things loaded; "a loading toast and
  spinner in the submenu while things load like we do for the planner", and load "progressively on startup as long as
  no video is playing"). Each strip took its path from the shared submenu list 9391 and only while its item had the
  focus, so every visit loaded it again from nothing (box: films 1.3 s, TV shows 3.6-4.7 s, music 1.7-2.0 s). Now:
  - each strip has a hidden submenu list of its own (93911 / 93912 / 93913) that gives it its path whichever item
    has the focus (Aeon_StripPath_*); 9391 still draws the submenu.
  - a section loads once it is armed (Window(Home) aeon.pl.movies / tv / music): the skin timer aeonhomearm arms the
    focused one at once, and the helper arms all three one after another after Kodi starts, one at a time, while Home
    is open and no video plays (helper 0.3.88, service HomePreload).
  - while the focused item's strip loads, the Planner's capsule (spinner, Loading...; the Fused Glass panel, a dark
    box in the other themes) sits where the submenu opens, under the menu on the left (Aeon_H_StripLoading).
  - Down lands in a strip at once when it is in. One that is still loading, or refreshing after a library change
    (a strip is out of sight while it refreshes), keeps the focus on the menu with the capsule showing, and Down
    lands as soon as it is in, waiting up to 45 s (it gave up after 5 s, and could land in a strip still out of
    sight). Right after Kodi starts, while a dozen add-on services start one after another, a list can take 25 s
    and more on the box: the capsule shows meanwhile.
  - a strip is in sight only while it has the focus itself (it was: while any strip had the focus, when the other two
    were empty anyway).
  _src/home_preload.py.

## 0.56.3
- Fused Glass: Skin settings > Appearance > Focus highlight is Pill, Frosted, Outline or Tight; Flat is gone (the user:
  fill the gap to the card's round corners, "if you are unable then we remove flat as an option for Fused Glass but
  keep the others"). A flat bar ends 12 px from the card's top or bottom, inside its round corner, and pokes out of it;
  the library lists could fill that gap (0.56.2), but Kodi's settings and add-on settings keep their rows in a
  scrolling grouplist and do not tell the skin where the focused row is. A Flat chosen before is the pill now (Home
  resets it; FG_FocusFlat is false). The library views' flat bars are gone too (fg_lib_focus.FLAT_SLOTS).
  _src/fg_noflat.py.
- Fused Glass, information screen: the focused button (Resume, From start, Play, Trailer, More) has the gold accent,
  a gold ring round the white pill like the ring round a focused poster in the library walls (it was grey).
  AG_PillHalo takes the ring colour as a param; every other button keeps the grey ring. _src/fg_infogold.py.

## 0.56.2
- Fused Glass library views follow Skin settings > Appearance > Focus highlight, like the menus (they always drew their
  own rounded bar): Pill (default), Flat, Frosted, Outline, Tight. Flat is a square white bar to the card's edges (12 px
  wider on both sides) and over the gap under the row; on the first row it runs up to the card's top and on the last
  row (where that row ends at the card's bottom: Episode list, Season list episodes, Low list, the music lists,
  Episode combined) down to its bottom, with the card's round corners (fg/rtop28.png, fg/rbot28.png); with Frosted
  and Outline, whose bar is see-through, the row's
  text stays light. All library lists: List, Episode list, Season list combined 1 / 2 / 3 and their episodes, Compact
  list, Low list, the music lists, Episode combined. _src/fg_lib_focus.py, called by _src/fg_lib.py (and its
  style_bar() by _src/fg_epcomb.py). One picture per style, switched by visibility: Kodi keeps a $VAR picture in a
  list row as it was when the rows were made.
- Fused Glass, List view (and Episode list, the open seasons view): no clear glass panel above and round the card any
  more. The blurred backdrop under the frosted panels (Material Frost and Dark) went through masks of the views from
  before the redesign (the old List panel 727,24 1093 x 1032); the masks now have the new cards' shapes, the open
  seasons view has its own (fg/bm512.png), and the A-Z rail mask fits the rail (1836, 64 wide, r32).
  _src/fg_blur_masks.py (fg_textures.py has the same shapes).
- Skin settings > Look > Material: the fourth choice is called Dark (it said Today); its help line says so in every
  language. The setting's value is unchanged. _src/fg_material_dark.py.

## 0.56.1
- The permanent settings strip is for Aeon and Glass only: in Fused Glass the strip is too wide to stay over the
  views. Fused Glass ignores "Permanent" (Skin settings or per view) and keeps the strip as an overlay that slides in
  with Left or the Menu key (Aeon_StripPerm is off there). Skin settings > Look > Settings strip (row 9525) is hidden
  in Fused Glass, the rows under it move up a row and Up / Down go round it; the per-view "Settings strip" item in View
  settings is hidden in Fused Glass too. Aeon and Glass keep both. _src/fg_nostrip_perm.py.

## 0.56.0
- Skin settings, preview cards (the user: "fix the existing cards but also make more previews for options which
  genuinely can have them"). One generator now draws them all: _src/skin_previews.py (the older drawings are kept in
  _src/skin_previews_legacy.json). 74 rows have a preview (was 44).
  - The card: Glass and Aeon with Menu theme Fuse beside the settings, 280 x 470 (was 280 x 300); the Aeon menu styles
    use their own side column (no second box); Fused Glass a full-height third card 1552..1824 x 108..974 like the Home
    menu page's side card, the content 12 px in from its sides.
  - The explanation text has room: 196 px in st_small_20 (it was 46 px in st_cap_14 and cut long texts off, e.g. Look >
    Settings strip).
  - Fixed: Appearance > Skin theme showed the old accent sample ("Library lists") from before the row took its id.
  - New previews, most of them following the current choice: Look > Watched indicators, Trailer button, Logos instead
    of titles, Library side strip, Progress line on posters, Home menu: only the focused item's name, Toasts from the
    clock pill, Material (the real card fill); Playback > Words lyrics size, Seek bar while paused, Language flags,
    Cinema mode, Clearlogo in Now playing; Appearance > Skin theme, Menu theme (the real menu fill / the Aeon style's
    boxes), Library background, Home menu position, Corner boxes, Focus highlight (the real highlight picture);
    Details > Hide spoilers, Episode code, Cast photos; Behaviour > the Skippy rows (skip button, segment line, Aeon
    skip button style, up next, skip button on the player card); Backgrounds > Home vignette (the real vignette and
    strength), Weather / Clock box on the screensaver, Screensaver background, Band under the Home menu, Home bar;
    Spotlight & widgets > Stacked row, Widget screens background; Time > Weather row and rain; Home menu > Menu names
    in capitals.
- Skin settings > Backgrounds > Vignette shape (new row 9765 under Home vignette, Skin.HasSetting(aeon.vignette.side)):
  Round (default, the vignette so far) | Side, the look of the font mockups: dark from the left (solid for the first
  30 %, 80 % at 58 %, 25 % at the right edge; media/common/aeon_vignette_side.png) under the Home text. Home vignette
  (Off / Light / Medium / Strong) sets how strong either shape is; Strong gives the mockups' look exactly. Strings
  32599-32602 (Side, Vignette shape, Round, help line) in all 22 languages. _src/vignette_side.py. (A fifth choice in
  the Home vignette row did not fit: long translations of the row's name, e.g. Ukrainian 318 px, ran into it.)
  - Side is also drawn inside the Home spotlight layout (Aeon_H_Spot2Item), after its scrims and before its logo and
    plot: the spotlight wraplists (9421 ... 9424) paint their picture full-screen over the Home darkening layers, so a
    vignette down there never showed on a spotlight in any theme. Round stays where it was, so the default look does not
    change.

## 0.55.3
- Aeon theme: new option Skin settings > Appearance > Aeon accent colour (row 9760, Skin.String(aeon.boxaccent)):
  Gold (default, a matte ochre ff8a6d2f that ties in with Fused Glass's gold), Slate, Teal, Moss. OK steps through
  them. It colours the title boxes, spines, On pills and the clock box, replacing the brown. It applies with the
  Aeon palette only (also for the menus when a palette is set for the library only); every other palette keeps its
  own box colour, and the row hides then. Strings 32594-32598 in all 22 languages.
- How: variable Aeon_BoxAccent (Includes_Aeon_Glass.xml); _src/ms_menus.py draws every box with it (BOX);
  _src/aeon_accent.py made the change once.

## 0.55.2 (helper 0.3.87)
- Live TV, EPG tools panel: new row "Reload EPG" (string 32593, all 22 languages), between Search and Return to
  guide. Kodi has no command to fetch the guide again, so the helper (swap.py epgreload) switches the enabled PVR
  add-ons off and on; live TV stops for a few seconds and the channel that was playing is opened again.
- Fused Glass: the panel's rows are 72 px high (were 78) so all twelve fit without cutting the last one.

## 0.55.1
- Fused Glass, Live TV: the programme progress bar on the focused (white) channel row stays gold too.
- Fused Glass, TV channels: Right from the Guide button (after Play and Record) opens the EPG tools side panel.

## 0.55.0
- Aeon theme, all four menu styles (Mosaic, Ledger, Bridge, Tab slab): the on-screen keyboard and the number pad
  (PINs, times, dates, the IP address) are built like the other menus, after the boards on the Aeon menus page
  (skin.glass/mockups/aeon-menus). Every key is a flush square cell (x_raised on an x_panel ground, 1 px apart), the
  focused key is the white bar with dark ink, OK and Done have the palette colour, and a keyboard mode that is on
  (Symbols, Caps, Shift) fills its cell with the palette colour.
  - Mosaic: the title box and the field form the top band; the keys and the buttons meet under them.
  - Ledger: a palette spine runs down the field row and every key row; the focused row's spine cell turns white and
    points at the row.
  - Bridge: stairs. Title, the field one row lower and across, the keys under the title, the buttons one more row down;
    the row under the title names the keyboard layout.
  - Tab slab: the dialog's name is a tab that flows into the slab holding the heading, the field and the keys; on the
    keyboard Symbols, Caps and Shift are tabs beside it (so the space bar is wider), and a mode that is on takes the
    slab's colour. The buttons hang beside the tabs and the slab.
  - Kodi does not say which part of an IP address is being typed, so the boards' "Part 4 of 4" note is left out;
    Kodi's own highlight shows that part in white and the rest dimmed.
  - Navigation is worked out from the cells' places and wraps at the edges. Keys a keyboard layout leaves out (short
    rows, the empty fourth row of Italian symbols) are skipped, so the focus never lands on a hidden key.
  - Glass, Fused Glass and Aeon with Menu theme Fuse keep today's keyboard and pad: their controls moved unchanged
    into Kb_Classic / Num_Classic (new 1080i/Includes_Keyboard.xml), and the windows pick a look the way DialogConfirm
    does. Generator: _src/ms_menus.py (keys_mosaic ... keys_tabslab, MS_Kb_* / MS_Num_*); _src/fg_keyboard.py and
    fg_glassmenus.py now read Includes_Keyboard.xml.

## 0.54.7
- Live TV, EPG tools panel: Back and "Return to guide" closed the panel and then also left the guide (to Channels or
  Home). The panel was opened straight from the grid's <onback>; being modal it ran inside that Back action, and Kodi
  finished the Back when it closed. Back now goes to a 1 px button (6058) that hands the focus back to the grid and
  opens the panel from an alarm.
- Live TV tab bar (Channels, Groups, Guide, Recordings, Timers, Timer rules, Search), all themes: Left / Right only
  move along the tabs and the screen stays as it is until OK opens the area. Groups no longer disappears while moving
  along the bar (it left with the window change). OK opens the area with the focus kept on its tab; areas are opened,
  not replaced, so Back from Search or Recordings returns to the Live TV view you came from, not to Home.
- Fused Glass, Live TV: the programme progress bars (channel rows, the info pane, the guide's foot) are gold
  (fg_mark) pills; the bar on the white focused row stays dark for contrast.
- Edited in place (Includes_Fused.xml FG_PVRTabs, Includes_Misc.xml tab params, MyPVRGuide.xml): _src/fg_livetv.py
  no longer reproduces the live block, so it was not re-run.

## 0.54.6
- Aeon theme, Mosaic menu style, Kodi settings and add-on settings: the icon box no longer sits over the first two
  category rows, where it could cover a long category name. It stands in the title row, at the right end of the
  title box (same height), and the title scrolls in the room left of it. Generator: _src/ms_menus.py
  (settings_mosaic); only MS_SetCat_mosaic and MS_AddonSet_mosaic changed.

## 0.54.5 (helper 0.3.86)
- Audio settings during playback: the slider rows (Volume, Volume amplification, Downmix: Center Mix Level) no longer
  draw their name over the value ("Downmix: Center Mix Level" ran through "0.0 dB" in Fused Glass and touched it in
  Glass). Kodi places the value one text offset left of the slider, so that offset counts three times in a slider row.
  - Fused Glass: both playback side panels (OSD settings and the track select) put their text 40 px in from the row
    ends instead of 80. Tabs, heading, rule, rows, buttons and hint now start at 1232 (Dlg_PanelCol_fg,
    Dlg_PanelShift_fg); the track rows, check marks and separators moved with them, and the second label now ends at
    1848 like the settings values. Slider 140 wide (was 220), 1708..1848.
  - Glass: slider 90 wide (was 130); the rest of the panel is unchanged.
  - Both looks cap the slider row's name with textwidth (330 / 281), so a longer translation is cut with "..." before
    the widest value ("-60.0 dB") instead of running into it. FG_SettingTemplates / AG_SettingTemplates take
    sliderwidth and slidertail params; other settings pages keep their defaults.
- Fused Glass slider rows (also Kodi settings and add-on settings): the slider no longer disappears on the white focus
  bar. Kodi keeps the unfocused knob until OK is pressed and never changes the track on focus, and both were light.
  The track is now an opaque grey (ff404145), and the knob is the old one inside a 2 px dark rim (fg/slider_nib.png).
  On the dark card it looks as before; on the white bar the track and rimmed knob show, and the active knob turns dark.
- Highlight gaps measured again on the box: 12 / 12 in both side panels.

## 0.54.4 (helper 0.3.86)
- Fused Glass, the playback side panels: Audio / Subtitle / Video settings and the track select (a list chosen over
  playing video) now have the list highlight 12 px from both card edges, measured on the box (they were about 94 / 66
  and 96 / 72). Both panels are the same floating r28 card, 1184..1896 (r32 before for the settings panel; the track
  select's card ran off the screen's right edge), 12 px clear of the top and bottom and 24 px on the right, where the
  scroll bar now sits instead of inside the card.
  - Settings panel: the option rows run 1192..1888 (Dlg_OsdListGeo_fg) with the text 80 px in, so labels stay at 1272
    under the heading; FG_SettingRow / FG_SettingTemplates take a textoffsetx param (default 24, as before).
  - Track select: its lists run the card's width with the highlight 12 px in (Dlg_TrackListLayout_fg); the row content
    (Dlg_TrackRowContent_fg) keeps every label and the separators where they were.
  - The other looks keep both panels as they were (load-time conditions on aeon.fglass).

## 0.54.3 (helper 0.3.86)
- Fused Glass: every list highlight sits 12 px from both edges of the card around it. The cards have corner radius
  28 and the highlight 16, so 12 px nests the two corners on one centre. Measured on the box with a screenshot tool
  (skin.glass/mockups/home-menu-add/scripts/gaps.py, 12/12 everywhere listed here):
  - Skin settings > Home menu: the list's scroll bar sits in the gutter between the cards, not in the highlight's gap
    (it made the right gap 5 px). Categories, rows and side panel were 12 / 12 already.
  - Context menu (it was 4 px): rows 6 px in and 12 px narrower. EPG tools card (it was 26): rows 8 px in, 544 wide.
  - Select / multi-select / select with details / long lists, the video versions dialog, the file browser and the font
    picker: the row highlight is 12 px inside a row that starts at the card edge (shared Dlg_RowFocus / Dlg_RowFocusGrey,
    fg_l / fg_r, default 12); the select dialog's buttons and the video versions / file browser buttons moved to 12 px
    from the card's right edge, the file browser's list to the card edge.
  - Kodi settings and add-on settings: the option list 4 px further left and as wide as its card less 16 (it was 16 /
    40), the scroll bar beside the card; add-on settings' OK / Cancel / Defaults 12 px inside their card (were 16).
  - Event log, Profiles and the file manager: their cards fitted 12 px around the lists (were 20 / 30, 20 / 160 and
    28 / 23 with the scroll bar inside); the file manager's scroll bars now sit beside the cards.
  - Add-on browser and the list view rows (AG_LibListRow): 12 px in (were 4), in the highlight's r16 shape instead of
    a radius-20 card. Library options and View settings rails: 12 px (were 8), radius 16 instead of 24.
- Fused Glass: a list's selected row while the focus is elsewhere is rounded: Skin settings > Home menu and Context
  menu rows and System information use the frosted inset pill of the open category (fg/selrow16.png) instead of a
  square; dialog rows draw it 12 px in like the highlight, and the 3 px square edge of Dlg_RowFocus no longer shows.
- Aeon theme, all four menu styles: the side panels of Skin settings > Home menu and Context menu start 24 px inside
  their box (Mosaic, Ledger, Tab slab: "Selected item:" sat on the box's top edge). The Home menu panel shows ten
  buttons and scrolls to the eleventh of a custom item, with a scroll bar (9643, Dlg_HmPanelH_ms).
- The OSD settings panel and the track-select side panel followed in 0.54.4.

## 0.54.2 (helper 0.3.86)
- Aeon theme, Bridge menu style: the side panel of Skin settings > Home menu and > Context menu ("Selected item:", the
  item's name, since 0.54.0 also "Add item") was drawn on Bridge's corner squares, which fill the top of that column
  (x 1500-1640, y 108-248). In Bridge the whole panel now starts 91 px lower, its first line 24 px inside the deep column under the
  squares; that column runs on into the help band, so all eleven buttons of a custom item still fit. The other styles
  and themes are unchanged.

## 0.54.1 (helper 0.3.86)
- Fused Glass, Season list combined 3: a hint that Right opens the season's episodes (the user's pick, board 5126 of
  the library canvas). The episodes peek in as a slim glass strip beside the seasons card: the number of episodes,
  the word Episodes turned on its side and a tick per episode (bright = watched, up to twelve). A white disc with a
  dark chevron rides on the strip at the season in focus while the seasons have focus. The poster (340 x 510) and the
  facts move over to make room (_src/fg_lib_lists2.py v512).

## 0.54.0 (helper 0.3.86)
- Skin settings > Home menu has Add item: a row under the last item (+ Add item, with the positions in use, 13 / 24)
  that opens the type picker, headed Add item (the items not on the menu yet and Custom item; no Empty position), and
  puts the choice in the first free position after the last item, or in a gap when the end is full. The new row takes
  the focus, so Rename, Choose icon and the rest are one Right away. While the row has the focus the panel on the
  right says what it does. The help line under the rows names it (31671, all languages).
- 24 Home menu positions (was 13) and 10 custom items (was 3): the 14 items of the skin and all ten custom items fit
  on the menu at once. Custom items 4-10 work like 1-3: own path, label, icon, Spotlight (lists 9415-9420, 9424, page
  dots, timer, the Spotlight editor's path button 9854-9860), widgets and submenu (skinvariables nodes guid-aeon0015 to
  0021, in shortcuts/skinvariables-shortcut-aeonmenu2.json; the helper adds them to a saved copy), and the Custom item
  settings button in the editor panel (9680-9686). "All ten custom items are in use" (31912, all languages).
- The editor's rows are a list that scrolls (grouplist 9641, thin bar 9642): rows after the last item hide, so the
  list is as long as the menu plus Add item. Rows 14-24 are 9627-9629 and 9631-9638, Add item 9639; the row groups
  have no id (a group with its button's id took the focus from Kodi and dropped Up / Down). The Home menu category's Right goes to the list.
- Home had four System fallback items (one per position 10-13), so System could show twice when it sat at 10-12;
  one item now, shown when no position holds System.
- The type cycle of the Home lists window (Aeon_EditNext*) runs through all ten custom items before Empty.
- Built by _src/menu24.py (clones every per-position piece from 13 to 14-24 and every per-custom-item piece from 3
  to 4-10; runs once) and _src/menu24_strings.py (32591 Add item, 32592 the panel text, 31671, 31912). The Glass
  theme's custom item pills on the library top bar stay for items 1-3.

## 0.53.2 (helper 0.3.85)
- The skin's skip pill follows Skippy > Progress bar counts down (service.skippy progress_bar_countdown): the ring
  and the bar empty instead of fill, in every look (Fused Glass ring, Aeon bar, Glass bar), smooth or per cent.
  Skippy.Segment.Progress / .Frame stay "played", so the countdown pictures are the same ones numbered the other way
  round (media/fg/pringr, pringfr, aeon/skipbarr, skipbarfr; _src/skip_smooth.py). Before, the pill always filled.
- The Up next card's bar does the same with Skippy > Next episode countdown (next_episode_popup_countdown): it is now
  drawn as pictures (media/fg/unbar, unbarf and their reversed copies) so it can run either way, and it declares
  Skippy.SkinNextEpisodeProgress.Frames 421 so Skippy drives it one pixel at a time (_src/fg_upnext.py).
- Fused Glass: the keyboard (search box) is a rounded frosted card with the Fused Glass edge and soft shadow, 48 px
  clear of the screen's sides and bottom, and the text sits in a rounded input well, instead of the square
  full-width slab. It keeps $VAR[FG_KbFill], so Menu theme and Look > Material still colour it. Aeon and Glass keep
  the slab (_src/fg_keyboard.py). The keys' focus is rounded to match (radius 14, keyboard and number pad, Fused
  Glass only).
- The number pad (PIN, time and the IP address input from the keyboard): its input field was a rounded 1 px outline
  in every theme. Fused Glass draws the keyboard's rounded input well, the Aeon menus a flush deep box (square, like
  the rest of Aeon); Glass and Fuse keep the outline.

## 0.53.1 (helper 0.3.85)
- Skippy's progress hook takes the skin's windows by their real ids: Kodi registers a skin's custom window as
  10000 + its XML id, and xbmcgui.Window(1167) does not exist (tested on the box), so the skin declares 11167 (skip
  pill) and 11174 (Up next card) as Skippy.SkinSkipProgress.Window / Skippy.SkinNextEpisodeProgress.Window.

## 0.53.0 (helper 0.3.85)
- Skin settings > Appearance > Menu theme works in Fused Glass: Dark (the look so far, default) | Glass. Glass draws
  the settings menus, dialogs, the context menu, the keyboard, information pages, the library options strip and View
  settings on frosted glass in the material chosen under Look > Material (Today, Frost, Raised, Clear) instead of the
  dark fills; the dim behind dialogs is lighter and the settings backdrop shows more of its picture. It switches at
  once, no restart. Fused Glass keeps its own setting (Skin.String(aeon.fgmenu)), so the Aeon menu style and the
  Glass theme's Glass | Fuse choice are untouched; the row no longer offers Fuse there (it did nothing in Fused Glass).
  Shared card Aeon_Glass / _L (was fg_frost2) -> FG_MenuFill, dialog panel -> dialogs/panel_fgg*.png, strip / rail ->
  FG_MenuPanel, keyboard -> FG_KbFill, all written by _src/fg_material.py; the rest by _src/fg_glassmenus.py.
- Skin settings > Backgrounds > Home bar (Fused Glass, Off by default): Bar (one frosted capsule as wide as the Home
  menu row), Keys (a glass circle under each icon, a capsule round the focused item) or Shelf (a band across the
  screen), from the mockup canvas https://claude.ai/artifact/Me64YpHgSLfR9w7xkLCRvH. It follows Look > Material and
  works in both Home menu modes (icons, titles) and both positions. Bar and Keys grow with the focused name
  (shadow / fill / edge grouplists laid out like the icons row). Textures media/fg/hb_*.png.
- Look > Material: the help says what the material changes (library views, Home panels, the Home bar, and menus and
  dialogs with Menu theme Glass). New strings 32573-32579 (Dark, Menu theme help, Home bar, Bar, Keys, Shelf, Home bar
  help) and the reworded 32551 in all languages (_src/fg_glassmenu_strings.py).

## 0.52.6 (helper 0.3.85)
- Smooth skip progress through Skippy's progress hook (needs service.skippy 7.15.0): the skin declares its skip pill
  (window 1167) with a driven progress control (31) and 421 pictures, so while Skippy drives it the Fused Glass ring
  and the bars over the seek bar step by Skippy.Segment.Frame every video frame (media/fg/pringf, media/aeon/skipbarf:
  the 420 px bar moves a pixel at a time) and the Glass pill's bar is the driven control. With an older Skippy
  everything shows the whole-per-cent pictures as before. _src/skip_smooth.py.
- View picker: a long name wraps onto a second line (a textbox: labels in list rows never wrap).

## 0.52.5 (helper 0.3.85)
- Fused Glass Up next card: Skippy's next episode prompt in the skin's look, through Skippy's skin hook
  (Skippy.SkinNextEpisode): a frosted card at the bottom right with the next episode's picture and the countdown
  under it (Skippy drives that bar every video frame), the heading ("Play next episode?" / "Still watching?"), show,
  season and episode, title, and Play now / Close (Continue / Stop). OK on a button or Back answers Skippy
  (RunScript(service.skippy,next_episode_play|close)). Windows 1174 (the card), 1175 / 1176 (opener and closer, as the
  skip pill's 1171 / 1172), written by _src/fg_upnext.py. It comes with Skin settings > Skippy: the skin's skip
  button, in Fused Glass only; the skip pill gives way while the card is up. The setting's help says so (all languages).
- The season views' A-Z rail: Combined (529) has a scroll bar now (its rows had no page control); in Combined and the
  Season list combined views the bar shows even when everything fits, and while a season's episodes (or a show's
  seasons, a set's films in Combined) have the focus the rail shows their scroll bar and their number of items.
- Season list combined is now "Season list combined 3"; Combined of seasons is "Season poster wall combined" in the
  picker and in the header's view pill (the pill also names Season posters, Show posters and Episode wall as the
  picker does).
- View picker cards are bigger (320 x 360): long names wrap onto two lines, the mock-ups are centred.

## 0.52.4 (helper 0.3.85)
- Skin settings > Motion, memory, reset: the rate row is called "Progress bar updates per second" (was "Updates per
  second"; the user's wording). Its pills are narrower (Screen 136 px, numbers 52 px, from x 506) so the longer label
  clears them in every language; long translations name the bar briefly ("barra", "Balken", "Sáv"), Greek abbreviates
  the second. _src/smoothprog_rate_pills.py, _src/smoothprog_rate_strings.py.

## 0.52.3 (helper 0.3.85)
- Smooth song progress is on by default (the user's call: it costs little). The switch now stores the opposite,
  Skin.HasSetting(aeon.smoothprogress.off); OK toggles it.
- New row under it, Updates per second (9763): Screen | 10 | 25 | 30 | 60 (Skin.String(aeon.smoothprogress.rate),
  Screen by default). Screen updates as often as Kodi draws the GUI (System.FPS); the others are fixed rates. The
  helper no longer paces by pixels. Label, "Screen" and help in all languages (32570-32572); the Greek label says
  "update rate", the long form ran under the pills. _src/smoothprog_rate.py, _src/smoothprog_rate_strings.py.
- Motion, memory, reset: Save lyrics next to the song moves one row down (821).

## 0.52.2 (helper 0.3.84)
- Skin settings: "Save lyrics next to the song" moved from Playback to Motion, memory, reset, under "Smooth song
  progress" (the user's choice). Playback has room for 11 rows and had 12: the row was drawn over "Clearlogo in Now
  playing" at the bottom of the page.
- The row has a new id (9762). Its old id 9567 was also the Ratings category's, so Left / Back on a Ratings row could
  land on the hidden row, and the row showed the Ratings description as its help: it has its own help line now
  (32560). _src/lyricsave_move.py.

## 0.52.1 (helper 0.3.84)
- Smooth song progress (Skin settings > Motion, memory, reset, off by default; Skin.HasSetting(aeon.smoothprogress)):
  in the Fused Glass Now playing card the song's progress behind the waveform glides a pixel at a time instead of
  jumping 8 px at every 1 %. Kodi's progress control reads Player.Progress as a whole percent; a twin of the card's
  fill without <info> (progress 4801, Includes_Aeon_Music.xml) takes over while the helper drives it
  (Window(Home).Property(aeon.smoothprog), expression Aeon_SmoothProgress) and the helper sets its percent as a
  fraction from the player's time, about twice per pixel of travel (11 a second for a 4:35 song, at most 60).
  Measured on the box: the helper's thread uses 0.3 s of CPU a minute (about 0.5 % of one core), Kodi's render
  thread no measurable change; setting it every frame (53 a second) would cost 1.6 %. Pause holds the fill still;
  seeks and the next song show within 0.1 s; the music OSD's 84 % zoom carries it along.
- The row (9579) is the last of Motion, memory, reset: the Playback page has no free row. OK switches it, Left goes
  back to the categories. Label and help in all languages (32568, 32569); _src/smoothprog_row.py,
  _src/smoothprog_strings.py.

## 0.52.0 (helper 0.3.83)
- Two new season views in Fused Glass, after the canvas boards 5120 / 5121 / 5122 (_src/fg_lib_seasons.py; the
  Season list combined view stays as it was):
  - Season list combined 1 (517): one layout for both pages. The seasons card, the focused season's episodes beside
    it (always there), and at the right the season (the show's fanart with the season's ring, the show's logo over
    the season's name, facts, genres, plot, network logo) or, while the episodes have the focus, the episode.
  - Season list combined 2 (518): the seasons card and one wide glass card with the season poster and its ring, the
    facts and plot, the network logo and the season's episodes as a strip of stills (Right goes into it; the facts
    then follow the episode).
  - Both are in the view picker (seasons, Fused Glass) with their own mock-up cards; names and descriptions in all
    languages.
- Showcase of seasons: the pill under the big poster shows the season in focus ("Season 3 · 0 of 4 episodes
  watched" with its ring), not the show's totals (the user's call: a season view shows the season's numbers). The
  helper's aeon.sp.* show lookup is gone (helper 0.3.83).
- Episode rows show the aspect ratio and the certificate next to the resolution and audio chips in every episode
  list: List, Episode list, Season list combined and combined 1, Compact list, Low list and Episode combined (fixed
  chips: Kodi takes no grouplists or buttons inside list rows). Numbered episode rows have two lines for it.
- Screensaver: the album cover's shadow is one pre-blurred soft texture (fg/shc.png, _src/fg_cover_shadow.py) instead
  of six stacked black copies of the cover, which showed as steps.

## 0.51.0 (helper 0.3.82)
- Skin settings change with OK / Enter only. Left on a row goes back to the category list and never steps the value
  back; Right does nothing. 122 rows, 1746 arrow actions dropped by _src/ok_only.py (run it after any generator that
  writes settings rows; ms_settings_row.py and fg_artguard_rows.py write OK-only rows themselves now).
- Fused Glass Neutral backdrop: the palette's surface colour with a soft light upper left and the accent's lower
  right, under a lighter vignette. It was the deep ground (ff0e0e0e with the default palette) under a 90% vignette,
  which read as black. Aeon keeps its flat dark Neutral.
- View settings > Backdrop says what Default stands for: "Default (Neutral)", "Default (Fanart)" or "Default
  (Colors)" (the section's Backdrop, else the global one).
- Backdrop = Colors follows the episode thumbs in a view's second list (the episodes of Combined, the Season list
  combined, Episode combined); it stayed on the season poster's colour (helper 0.3.82).
- Flix: the gold ring and the lift of a season poster are no longer clipped at the top (the row starts 28 px higher,
  the tiles stay where they were).
- The Season list view is called "Season list combined" (all languages).

## 0.50.1 (helper 0.3.81)
- Fused Glass Showcase of seasons, the last approved library board:
  - The season's poster with its ring leads the info band; the name column and the plot move right for it (films,
    shows and sets keep their band). _src/fg_lib_walls.py info_band(lead=True).
  - Under the big poster, a glass pill shows the show's own progress: a ring and "The show · 16 of 52 episodes
    watched". The helper reads the show's episode counts (aeon.sp.*); the pill shows only while that show's seasons
    are listed. It grows with its text: left and right pill halves (media/fg/pill_*.png) in centred grouplists.
- The plot boxes of every wall's info band hold whole lines only, so no half line shows at the bottom.

## 0.50.0
- Fused Glass, the last parts of the approved library mockups:
  - Episode wall: the Landscape wall of a season's episodes shows the season poster with the season's ring and the
    show's clearlogo at the left and the stills three a row beside them (item layouts that switch on the content,
    so the films and shows keep their four landscapes a row; _src/fg_lib_walls.py).
  - Low list of seasons: the card of rows is narrower and the season's poster with its ring and the facts (the show,
    the season's name, year, watched episodes, plot) get the room; shows and episodes keep their layout.
  - Seasons show the show's clearlogo over the season's name in the facts of Flix and the Banner and Compact lists
    (not in the Season list or the Low list, which already show the show's logo).
- Not in this release: the Showcase of seasons with the season poster leading the info band and the show's progress
  under the big poster (the band is shared by all walls; for later). There is no mockup for the view picker, so it
  keeps its look.

## 0.49.0 (helper 0.3.80)
- Fused Glass: the music library views are redrawn after the approved mockups: Fanart list (513), Wall (530), Showcase
  (531), Rows / Album list (532), Song list (533) and Fanart wall (534), written by _src/fg_lib_music.py. As the user
  decided on the mockups, Fused Glass offers the Wall for artists and albums only (not songs) and the Fanart wall for
  artists only (not albums); the Aeon and Glass views are unchanged.
- The music menu (Artists, Albums, Songs, Genres) sits as glass pills at the top right before the view capsule; the
  pill of what the list shows is lit, and the capsule opens the view picker (it is the menu's View button, 9805). Up
  from the first row goes to the lit pill.
- One music info band under the walls and the showcase: an artist's clearlogo (an album: the artist's clearlogo over
  the album's name), the facts, the bio or review as wide as it fits, then for artists the album count with its icon
  and their album covers, moving on every 5 s; for albums the record label logo.
- Fanart list: the list in a card with the library line and position, five rows (albums with their track count),
  under them the bio, or the artist's clearlogo with the review, the album count and the moving covers or the artist's
  photo; the big picture in a card at the right with the clearlogo or the album's facts. Rows / Album list: rows with
  the picture, a second line and the album count (artists) or year (albums); at the right the picture, the name and
  facts, the record label logo, the bio or review and, for artists, the album count with the moving covers and the
  album's name and year. Song list: the album's cover, the artist's clearlogo, the album's name, facts and label logo,
  the review under them; the tracks in a card with number, title, plays and length.
- The artist's album covers really move on now (the Aeon cycler list never scrolled, so it always showed the first
  album). A row without a picture shows a quiet square in its place.

## 0.48.0
- Fused Glass: the other video library views are redrawn after the approved mockups, like the List view and the walls
  in 0.47.0: Banner list (522), Compact list (524), Low list (527), Flix (528), Combined (529), Episode list (511),
  Season list (512) and Circles (536). In Fused Glass each loads its own include (FG_V<id>_View, written by
  _src/fg_lib_lists.py and _src/fg_lib_lists2.py); the Aeon and Glass views are unchanged.
- The facts of the item in focus are one block in every view: kicker, clearlogo or name, the rating sources with the
  facts, "16 of 52 episodes watched", media chips, tagline and plot; what an item lacks takes no room. Beside them the
  art row: the poster with its watched mark and the landscape art; an episode: its still with the progress bar and
  the season poster with the season's ring (from the list's watched / unwatched counts).
- Banner list: rounded banners down the left (the landscape art when there is no banner), the item in a glass card at
  the right; a set: its poster, the facts beside it and its films under them. Compact list: short rows in a card
  (name, resolution, year, run time or watched / total, mark), the item at the right; with text titles the clearlogo
  sits at the bottom right. Both keep Right into a film's versions or a set's films: one at a time on the poster's
  place, or the strip of films (View settings: versions as a grid / sets one at a time).
- Low list: the show's clearlogo up top, the art and facts from the top of the low card of rows at the bottom right,
  the network logo at the bottom. Episode list: the season poster with the season's ring and the network logo,
  numbered rows (a progress bar for an episode in progress), the still and facts of the episode in focus. Season
  list: the seasons with their rings in a narrow card, the season poster, the show's logo, the season's facts, genre
  and network; Right still opens the season's episodes in place of the poster and facts.
- Flix: the fanart of the item in focus fills the screen under a shade; clearlogo and facts at the top left; at the top
  right the studio / network logo, a set's films or an episode's season poster with the season's ring; four big
  landscapes along the bottom (seasons: their posters). The trailer window stays.
- Combined: the posters in a row at the top; under them a card with a show's seasons or a set's films (with watched /
  total or run time) beside the facts; seasons: the season's episodes across the card (5291 for seasons and films,
  5292 for episodes). Circles: round photos seven a row with the name and role under each, the gold ring in focus.
- The rail shows a five-digit item count in a smaller font. Audio chips in the walls' info band use short names for
  every codec (FG_L<id>_AudioS; the shared short-name variable left some codecs empty).

## 0.47.1
- Aeon theme, Bridge menu style (the user's notes on the dialog-audit canvas, skin.glass/mockups/dialog-audit):
  - Yes / No, OK and progress: the button row was 20 px too far left. The first button's top-right corner now meets
    the message box's bottom-right corner, and a lone OK / Cancel ends flush with the box. The row has room for
    Kodi's third (custom) button, which the old 520 px row cut off.
  - Select and multi-select: OK + Cancel (2 x 240) were wider than the info column (460) and reached 20 px into
    the list box. The Bridge buttons are now half the info column wide, flush with the list box.
  - Context menu: the info box was one row shorter than the menu, so the plot was cut. It is at least 8 rows tall
    now (six facts and the two-row plot) and reaches below a shorter menu; the menu centres on that height.
  - Generator: _src/ms_menus.py (centring() and ctx_frame() take the height to centre on, sel_footer() a button
    width); only MS_Ctx_bridge, MS_Confirm_bridge, MS_Select_bridge and MS_TrackSel_bridge changed.
- Aeon theme, Event log: the events card is as wide as the list, so the white focus bar is flush with both sides
  of the dark card. Glass, Fused Glass and the Fuse menu theme keep the rounded card with inset rows.

## 0.47.0 (helper 0.3.79)
- Fused Glass: the library views are redrawn after the approved mockups (canvas "Fused Glass library views",
  skin.glass/mockups/fused-library-views). This release: the List view (510) for films, sets, TV shows, seasons and
  episodes, and the Poster wall (520), Landscape wall (521), Square wall (525), Cards (526) and Showcase (523). In
  Fused Glass each loads its own include (FG_V<id>_View in Includes_Fused.xml, written by _src/fg_lib.py and
  _src/fg_lib_walls.py); the Aeon and Glass views are unchanged.
- The parts every redrawn view shares: the header (kicker and title at the top left, the view and sort order in a
  quiet capsule at the top right) and a glass rail at the right edge (the clock, the A-Z jump list, the item count).
  One rule for watched marks on every media type: a gold dot = not watched, a progress ring = part watched (a film
  or episode: how far it is played; a show or season: its episodes; a set: its films), a tick = all watched.
- List view: the poster as tall as the list (an episode: its season poster) with its mark; six rows (a white row
  with dark ink in focus), episodes with their still and progress bar, media chips, the mark, the run time or
  watched / total. Under the rows the item in focus: the rating sources (IMDb, TMDb, Rotten Tomatoes; a star with
  the library rating when none is known), year, certificate, run time, ends at, "16 of 52 episodes watched", the
  tagline in italics, the plot, media chips with full names, the clearlogo and the studio / network logo; a set
  shows its films, moving on every 5 s when it has more than four. Left from the list: a film's versions, or a
  set's films two by two.
- Walls: the tiles run edge to edge from x 96 to 1800, rounded, with the gold ring and a small lift on the tile in
  focus, the watched mark in the corner and the name under it; Cards show the fanart with the clearlogo over it;
  Showcase is a cover flow with the poster in focus big in the middle. One info band under them: the name column
  (kicker, clearlogo or title, the facts, the rating sources, media chips or "16 of 52 episodes watched"), the
  tagline and plot as wide as they fit, a set's films, the studio / network logo at the far right.
- View settings, per view and media type, override the global settings: Watched status (Default / On / Off; in
  Fused Glass it shows in every video view and stands for the dots and ticks), Progress rings (new, string 32563
  in every language) and Logos instead of titles. Default follows Watched indicators, rings on and Logos instead
  of titles. The helper publishes aeon.vo.rings and aeon.vo.logos (VIEW_OPTIONS).
- Fonts: title_50 (the title face at 50) and tag_22 (the body font in italics) are plain fonts in every font set;
  the helper makes their section copies (lb_title_50, lb_tag_22 ...) like the others.
- Not done yet: the Episode wall of the mockup (the season poster left of the stills). A panel keeps one item size,
  so episodes get the Landscape wall's four stills a row. The other views follow in the next releases.

## 0.46.5 (helper 0.3.78)
- File manager, Aeon look: the two cards reach up to the clock box (their top edge sits on its bottom edge, y 108;
  it was 168) and the lists show 11 rows instead of 10. The hairline under the header no longer runs across the top
  of the cards (AG_TopBar has a new param rule). The gap between the cards is a black bar with a white two-way arrow
  in its middle (FM_Divider, arrow from the bundled Arctic Fuse 3 icons). Glass and Fused Glass unchanged.

## 0.46.4 (helper 0.3.78)
- File manager: each card's scroll bar can be reached. Right walks the source list > its scroll bar > the
  destination list > its scroll bar, and Left walks back the same way (Right from the source list used to jump
  straight to the destination list). A scroll bar is a stop only when its list has more than one page, as in the
  file browser; with a short list Left / Right go straight to the other list. Up / Down on a scroll bar page its
  list, Back on a scroll bar returns to its list. The path of the card in focus stays highlighted while its
  scroll bar has the focus. Same in every look (FM_Side in Includes_Misc.xml, FileManager.xml).
- File manager: a scroll bar gives the focus back to its list two seconds after the last key press (timer aeonfmsb,
  like the library views' scroll bars). Kodi hangs when the File manager refreshes while a scroll bar has the focus
  (tested on the box with Container.Refresh; its Refresh() only expects a list in focus, and a refresh comes when a
  copy / move / delete finishes), so the focus must not stay there. Estuary has the same weak spot.
- Fused Glass: the row a list keeps while it does not have the focus has the shape of the focus highlight
  (rounded; square for "flat", small corners for "tight") instead of the square bar with a 3 px edge. Every
  AG_ListLayout / Dlg_IndexListLayout list: File manager, file browser, video versions, game menu, font picker,
  power menu. Other looks unchanged (Dlg_ParentRowTex in Includes_Dialogs.xml).

## 0.46.3 (helper 0.3.78)
- Planner: says Loading while it fills its lists, instead of "Nothing planned". In the Day view the Fused Glass
  capsule of the busy dialog (spinner, "Loading...", string 31952 in every language) sits where "Nothing planned"
  goes; in the Week view each day card that is still loading shows a small spinner and "Loading...". "Nothing
  planned" / "Nothing out" only show once the list has loaded and the day really is empty. The window sets
  aeon.planner.busy when it opens and the helper clears it once the lists have their items (also after View, Week
  starts, Shows you watch, Earlier days, Show and Update now); a list that loads is Container(id).IsUpdating. Kodi
  keeps showing a list's old items until the new ones are in (last week's titles under next week's days), so a list
  that reloads fades out and its Loading shows instead. Right after Kodi starts, before the helper has chosen a view,
  the capsule shows too (the screen was blank), and the View pill names the saved view (it said Day). Other looks: the
  same spinner and word on a dark box (Day view).
- Planner with Earlier days on: Left from today no longer gets stuck. The helper counted the episodes the kept list
  still had for the days before today, but those days' lists show only the library's episodes, so Left could land on
  a day whose list was empty (Saturday on the box: one kept episode, none in the library). The focus was then lost,
  every key went to the View pill and Down could not reach the lists again. Now the days before today count only the
  library's episodes (what their lists show), so the Week view steps over a day without them as over any empty day.
- Planner, focus: a list that is about to load other items hands the focus to a holding button first (9501 in the
  Day view, now always there, 1 x 1; new 9518 in the Week view), and the helper puts it on the new list once that has
  loaded and has items, or leaves it on the holding button when the day is empty (Left / Right / Up work there).
  Down from the option pills goes straight to the day list only when it has items and is not loading; otherwise the
  helper places the focus. The focus is no longer pulled back down when you moved up to the pills meanwhile.
- Planner, Earlier days: the week's aired episodes are read once and kept for ten minutes (the query took about a
  second per move on the box, 67,000 episodes); the day lists use the same copy.
- Written by _src/fg_planner.py (Fused Glass header and Week view) and _src/pl_loading_0463.py (Day view, the classic
  header and Week view); _src/fg_material.py run again.

## 0.46.2 (helper 0.3.77)
- Live TV, Channels / Groups over the picture: the channel card starts at the same left edge as the Now playing
  pill and the player controls card (it sat 32 px further left).

## 0.46.1 (helper 0.3.77)
- Live TV, guide over the picture: the sheet sits higher and the player controls card shows under it, as it was when
  Guide was pressed; Back returns to the controls with Guide in focus (the full-screen window reopens them).
- Live TV, Channels / Groups: the channel list is shorter (7 rows) and opens over the controls card; Back returns to it.
- Live TV information (Info): a compact card instead of the film layout with its empty poster slot: the channel's
  logo and number, channel and genre, the programme with LIVE, two lines of plot, Next, and a bar across the card with
  the start, the time left and "Ends" with the scheduled end.
- Live TV controls: Play / pause shows when Kodi can pause the channel (Player.PauseEnabled: a PVR add-on with
  time-shift on), and while it is paused or plays from the time-shift buffer.
- Home > Power: the card that opens on Up is drawn over the page's clock and timer pills (the page comes first now);
  the Shut down row's ring is solid red instead of a faint glow.
- Home, a set's films in a spotlight: a round yellow focus ring and rounded dimming on Fused Glass (was a square white
  frame and square shading over the rounded posters).

## 0.46.0 (helper 0.3.77)
Fused Glass Live TV, from the mockups LiveTVChannels, LiveTVGuide and LiveTVGuideOverlay (_src/fg_livetv.py; Fused
Glass only, the other themes keep the tab card, list and guide they had: Misc_PVRTabsClassic).
- The Live TV areas in one glass pill at the top left (TV / Radio, Channels, Groups, Guide, Recordings, Timers, Timer
  rules, Search); the open area has a yellow mark. New Groups button right after Channels (Channels and Guide): it
  shows the group in use and opens Kodi's group list. Left / Right still go straight from area to area.
- Channels: a list card (number, logo tile, channel, what is on, time and progress; a red dot on the channel that
  plays) with sort and filter in its head, and a spotlight card for the channel in focus (logo, now, progress, end
  time and length, plot, next, Play / Record / Guide).
- Guide: the programme in focus at the top (logo, channel, NOW, title, time, plot), the playing picture in a tile on
  the right, the grid in a card with the group pill; programme cells with a yellow focus ring, the playing channel
  marked with a red dot.
- Guide over the playing channel: the Live TV player controls' Guide button now opens the guide as a sheet over the
  picture, which keeps playing above it; OK on a programme on now switches to that channel (Kodi's guide select
  action), Back goes back to the picture. (Before, the button opened pvrosdguide, which this skin has no window for;
  Kodi also refuses to open a window while the player controls are open, so the button closes them first.)
- Live TV player controls: Stop on Live TV too, no play / pause there (it could not pause); they open on Channel +;
  a new Groups button opens the channel list with its group pill in focus.
- The channel list over live TV (Channels button) in the Fused Glass look: a glass card with a group pill (Left /
  Right switch the channel group) and the rows of Live TV > Channels (FG_ChOSD; ChOSD_Classic for the other themes).
- Live TV > Channels: Right from the list goes to its scroll bar, then on to Play / Record / Guide.
- Audio names on the player: AAC, HE-AAC, MP3, MP2, Opus, Vorbis, FLAC, ALAC, WMA, AC-4 (was the codec id, AAC_LC).
- Home > Power: the focus ring is the solid accent yellow (red for Shut down), not a faint glow that read brown; the
  card Up opens is always dark, whatever the material, as the spotlight text runs under it.
- Home strips (Fused Glass): an episode in focus (Recent episodes, Recently played ...) shows its thumb under the
  show's logo with a yellow line for how far it was watched, as on Favourites (_src/fg_stripep.py).
- Planner: the day list's scroll bar is a slim rounded one (FG_ScrollPill), yellow while in focus.
- The view picker shows a mock-up for Episode combined (_src/fg_pick538.py).
- Now playing: the artist's fanart no longer gives way to a plain background for a while when the next one is not yet
  downloaded: the main fanart lies under the changing one and the others are loaded ahead (_src/fg_npfanart.py).

## 0.45.2 (helper 0.3.77)
- Home: the Sets item can show the movie sets you watched last. Skin settings > Spotlight & widgets > "Home
  spotlight: recently watched sets" (row 9757 under Home spotlight: transition, Skin.HasSetting(aeon.sp.recentsets),
  off by default): a Home spotlight whose path is the movie sets (videodb://movies/sets/ or a
  library://video/movies/sets node, a custom item's own sets path too) lists the sets whose films were played last,
  newest first, and leaves out sets nobody played (helper plugin ?info=recentsets&limit=N, sorted by lastplayed
  descending). Off: as before (all sets, in the order of the item's spotlight settings, random by default). The
  spotlight editor still shows the item's own path and sort; only the spotlight lists 9421 / 9411-9413 read the new
  wrappers Aeon_SP2List_* / ListSort_* / ListOrder_* (Includes_Aeon_Sub.xml, _src/fg_recentsets.py).
- Home lists (Edit lists) and other pickers offer "Recently watched sets" (skinvariables-shortcut-config.json; the
  picker's names come from that file and stay English, like the others there).
- Strings 32561-32562 in all 22 languages (_src/fg_strings_0452a.py).

## 0.45.1 (helper 0.3.76, screensaver 1.2.0)
Fused Glass refinements: fixes and wishes from the review of parts 1-5.
- Video player: the small seek bar (paused) and the information panel show chapters as gaps, like the player
  controls (Aeon_SeekLine uses FG_SeekBar on Fused Glass; the information panel's bar gets a ranges control with the
  new 6 px gap fg/chgap6.png). The disc art no longer turns back the other way when paused (reversible="false").
- Live TV player controls: every button moves Left / Right itself, past the hidden ones (_src/fg_osdrow.py), so focus
  no longer sticks on Stop; the controls open on Play. Channel down / up beside the transport buttons, a red Record
  button, Guide (pvrosdguide) and Channels (pvrosdchannels) on the right.
- Home: Skin settings > Menu names > "Menu names in capitals" (row 9566, aeon.hm.caps, Fused Glass).
- Shadows rebuilt as one smooth Gaussian fade with a light dither (_src/fg_shadows.py: fg/sh16, sh24, sh28, sh32), so
  no bands show on a laptop screen; FG_ShadowCol 6b000000 (Frost / Raised b3000000).
- Posters with rounded corners on Fused Glass everywhere they were square (set spotlight and versions on Home, set and
  versions panes; _src/fg_roundposters.py, 14 places, masks fg/m88x132 ... m727x1080).
- The yellow accent where the mockups have it: the focus ring of Favourites tiles, the Search row and the Planner, the
  glow of every Power button (red for Shut down), the yellow label of the new screensaver slides.
- System: the IP address on the This box card.
- Favourites: a heart for the Home item; smaller tiles (150 high) that no longer reach the screen edge; a TV channel
  shows its logo whole (on the tile and in the spotlight, with Now / Next); an episode saved as a favourite shows its
  thumb under the show's logo with Continue / Resume / All episodes.
- Search on Home: smaller posters (120 x 180) and YouTube pictures (256 x 144), the row moved in so the labels stay on
  screen, yellow focus ring.
- Planner: the yellow ring no longer clipped at the sides of a day; the day view's headline (the day) and caption
  (PLANNER · date) no longer run into the buttons; OK on a title opens Kodi's information page with what the Planner
  knows of it (plot, release date, cast, rating), also for films in the cinemas that are not in the library; Background Colors follows the title in focus; on Home the first day is marked only once Down is
  pressed; moving between days of the same week no longer slides the whole week; cards show the episode's thumb
  darkened (else the season poster, else the show's); View settings strip > Earlier days (aeon.planner.past, row 9459)
  shows what aired on this week's days before today (library episodes).
- Library views: with View settings open, the strip's now playing keeps the cover, artist and song (FG_StripNP).
- Material: the dialogs and the context menu follow it too (dialogs/panel_fg_frost, _raised, _clear.png, made by
  _src/fg_material.py; Clear lets the picture show through the menu).
- Screensaver (screensaver.aeon.fuse 1.2.0): three new slides, each with its own switch: a film in the cinemas now,
  what the Planner has airing today, and tomorrow; a small label says which (IN CINEMAS NOW, AIRING TODAY · network),
  the credits line shows "S3 E5 · title", the pager shows as many dots as there are items (_src/fg_ss_lists.py).
- Skin settings > Player > "Save lyrics next to the song" (row 9567, aeon.lyrics.save): switches CU LRC Lyrics' own
  "save to the song's folder" settings (.lrc and .txt); the music folder must be writable.
- Strings 32552-32560 in every language (_src/fg_strings_0451a.py, _src/fg_strings_0451b.py).

## 0.45.0 (helper 0.3.75)
Fused Glass refinements, part 5: the material (mockup Materials; _src/fg_material.py, run it again after any generator
that writes colordiffuse="fg_frost" / "fg_edge").
- Skin settings > Look > Material (new row 9529, Fused Glass): Frost, Raised, Clear, Today (the look so far, default).
  Frost: a lighter frost the picture's colours glow through, strong artwork shadows. Raised: the same frost with a lit
  rim and deep panel shadows. Clear: tint 30 %, no blurred copy of the backdrop under the panels. Today: tint 72 %.
- Every frosted panel, edge and panel shadow now follows $VAR[FG_Frost] / $VAR[FG_Edge] / $VAR[FG_PanelSh_xx] (160 / 172 /
  32 places); FG_ShadowCol (artwork and focus shadow) is stronger with Frost and Raised.
- Strings 32547-32551 in every language (_src/fg_strings_0450a.py).

## 0.44.0 (helper 0.3.75)
Fused Glass refinements, part 4: the library view Episode combined (538, mockup EpisodeCombined; _src/fg_epcomb.py).
Offered in the view picker for episode lists in Fused Glass (other themes fall back to another view).
- Header: TV SHOWS › the show and a big Season 3. Season pills from the helper (episodes per season, a tick when
  watched, a dot on the season on screen; OK switches season in place) and a sort pill (Episodes 1 → 4 / 4 → 1).
- Left: the season poster, the number of episodes, "1 in progress · 3 unwatched" and the next airing.
- Middle: the episodes in a frosted card: thumb with a yellow progress line, EPISODE 1 · 74 MIN, title, resolution and
  audio pills (DD+ Atmos ...), minutes left on the row in focus, a dot on unwatched episodes, a tick on watched ones;
  the row in focus white with dark ink.
- Right: the episode in focus: thumb with "35:44 of 1:13:33 · 38 min left" and a yellow bar, S3 E1 · SEASON
  PREMIERE, title, minutes · rating · date · Ends, pills (4K, SDR / HDR, DD+ 5.1, 2.40:1) and the plot.
- Strings 32541-32546 in every language (_src/fg_strings_0440a.py); masks fg/m178x100, m580x326, m300x440.

## 0.43.0 (helper 0.3.74)
Fused Glass refinements, part 3: the Planner (mockups PlannerWeek and PlannerStrip). Fused Glass only; the other themes
keep their header, options and Week view (moved unchanged into Includes_Planner.xml: Planner_TopClassic,
Planner_WeekClassic). Built by _src/fg_planner.py.
- Header: PLANNER · the week, a big headline (Next 7 days when the week starts today, This week, Next week, else the
  dates), the clock pill at the top right, and pills: Shows you watch (yellow dot when on), View, Show, View settings.
- Week: seven glass day cards; the selected day lighter; Today with its short date, other days their day number; titles
  as small cards (SHOW · S2 E3 and the episode title, films with their poster); the title in focus has a yellow ring
  and says You're on S3 E1 when you are behind on that show; Nothing out on an empty day; past days faded.
- View settings opens a strip at the left: View, Show, Shows you watch, Background, Week starts, Update the list,
  Update now, Home spotlight, with the week's count at the top ("21 episodes, 26 films this week") and a help box.
  Back or Right closes it.
- Shows you watch (Skin setting aeon.planner.watching, off by default): only episodes of shows with a watched episode.
- Week starts can be Today: the week is then always the next seven days.
- Background (Skin.String(aeon.planner.bg)): Colors (default: KarmaMole's colour picture when it has one, else the
  helper's blurred copy of the title's fanart), Neutral, Fanart. The library views' right strip is not drawn in the
  Fused Planner.
- Strings 32524-32540 in every language (_src/fg_strings_0430a.py).

## 0.42.0 (helper 0.3.73)
Fused Glass refinements, part 2: Home (mockups: skin.glass/mockups/fused-glass-refinements, boards Main, Power,
Favourites, FavouritesOK, Search, SearchResults). Fused Glass only; Aeon and Glass keep their pages (now
Aeon_H_PowerPage_Classic, Aeon_H_Favourites_Classic, Aeon_H_FavBg_Classic, Aeon_H_SearchRecent_Classic and
Search_WindowClassic; the old System panels are hidden in Fused Glass). Each page is chosen when the skin loads.
### System
- Three cards over the System picture (_src/fg_home_system.py, FG_H_SystemPage): This box (Kodi 22, the build, OS and
  device, the OS release line, skin, screen, how long Kodi and the box have run), Health (a memory ring, the processor
  bar and average, memory in use, CPU / GPU temperature tiles and a status pill: All good / Running warm / Memory almost
  full) and Library (films, shows and episodes with watched counts, songs, albums, artists, with thousands separators).
- Under the menu three tabs (9345): Shortcuts (Settings, Skin settings, Add-ons, File manager, Events, System
  information, Profiles when there is more than one), Recently used add-ons (program add-ons, last used first) and
  Library jobs (update / clean the video and music libraries) over a row of tiles (9343 / 9344 / 9346). Down from the
  System item reaches the row, Up from the row the tabs.
### Power
- A big clock with the date, how long Kodi and the box have run and what plays; the shutdown timer as pills (Off, 30,
  60, 90, 120 min, When this ends) in the spotlight; under the menu round actions: Shutdown timer, Sleep, Restart Kodi,
  Reboot, Reboot to Android (CoreELEC), Shut down (OK twice; the first OK only arms it for 6 s), Log off (exits Kodi),
  Screensaver (_src/fg_home_power.py, FG_H_PowerPage).
### Favourites
- A spotlight of the chosen favourite over its fanart: FAVOURITES · kind · network, clearlogo (or title); for a show
  Continue S3 E1 · title, the minutes left with a progress bar in the accent colour, the next airing and how many more
  are waiting in the season; for films and albums the plot.
- Filter pills All · n / Video / Music / Channels / Add-ons (9361) and a row of tiles in three shapes: wide for shows,
  poster for films and sets, square for albums, channels (with what is on now), add-ons and folders; an Add to
  favourites tile at the end opens Kodi's Favourites window. Kodi lists draw one size, so the row is a grouplist of
  slots (9370) fed from the off-screen list 9309 (_src/fg_home_fav.py; textures _src/fg_fav_tex.py).
- OK on a show, film, album or artist moves to the spotlight's buttons (Resume S3 E1 / Play, Play from beginning,
  All episodes or Shuffle, an info button); Back returns to the tile. Other favourites open at once. No progress bar on
  the tiles.
### Search
- Home > Search: a search field and the recent searches (with Clear) over the picture; under the menu tabs Last search:
  rings · n / Online: TMDb / YouTube over a row of results (a row only reads its path while its tab is chosen).
- The Search window (FG_SearchWindow): the query in a field at the top (OK opens Kodi's keyboard for any text), a
  keyboard of its own on the left (a-z, 0-9, Space, Delete, Clear) and the results beside it as you type: TV shows as
  wide cards (the card in focus says You're on S3 E1 and when the next episode airs), films as posters, then Also
  search: Music, People (films and shows with someone whose name holds the text), TMDb, YouTube.
### Other
- New textures: fg/mring (memory ring, _src/fg_mring.py), masks m300x168 / m112x168 / m168x168 / m126x190 / m148x222,
  fg/dash168, fg/btninfo_n / _f, fg/pw_android (_src/fg_power_icons.py); Font.xml: base display_160 in every fontset.
- Strings 32489-32523 in every language (_src/fg_strings_0420a-d.py).

## 0.41.0 (helper 0.3.72)
Fused Glass refinements, part 1: the player (mockups: skin.glass/mockups/fused-glass-refinements). Fused Glass only;
the Aeon and Glass players are unchanged (their parts are now Aeon_OSD_Classic, OSD_Bookmarks_Classic, FullInfo_Classic).
### Player card (Video OSD)
- New card (1080i/Includes_FusedPlayer.xml, FG_OSD2, chosen when the skin loads): 96..1824 x 752..1042, radius 32.
  Top left a Now playing pill as tall as the clock pill (NOW PLAYING | title); the clock pill shows ENDS and the end time
  (Live TV: the programme's end). The "ends at" ring is gone.
- The controls start at the same place on every card (388). Without disc art the poster is centred in front of them;
  with disc art (Seek bar / OSD > Spinning disc art) the poster slides 40 px left as the card opens and the disc slides
  out from behind it, inside the card, and spins while playing (stops on pause).
- Card text: Season 3 · Episode 1 (film: year and genre; Live TV: channel), the title, at the right Skippy's Up next or
  the media chips (4K, DV, DTS:X 7.1 ...).
- Seek bar: 12 px with a gap at every chapter end (the chapter ranges drawn in the card's colour, fg/chgap.png, colour
  fg_gapcol), a round marker, a soft ring while the bar has focus. Under it the time, the chapter (Chapter 2 / 3) and
  Skippy's line (NEXT CREDITS AT ...), the total or time left.
- Buttons: round, dark grey when not focused, white 76 px with dark ink and the label under it when focused; transport
  on the left (previous, rewind, play/pause, forward, next, stop), panels on the right (subtitles, audio, video,
  chapters, info, stats or tinyPPI, whose icon is drawn larger).
- Live TV: the channel logo and number on a frosted tile, a red LIVE pill after the programme (not while time-shifted),
  Next · time and the next programme at the right, the programme's start and end under the bar and how long is left.
- Trickplay (service.trickplay): with the card open the preview sits over the card's seek point, 352 x 198 with round
  corners, a white ring and the seek time on a white pill (DialogSeekBar group 94102).
- Skin settings > Playback > Clearlogo in Now playing (new row 9550, off by default; aeon.osd.nplogo): the show's or
  film's clearlogo in the pill instead of the title, the helper's trimmed copy (aeon.osd.logo).
### Chapters and bookmarks (Fused Glass)
- The card's look: heading with the count, the buttons as pills at the right, one row of chapter / bookmark pictures
  (Kodi lists both together), a "Now playing" tag on the chapter playing, the seek bar with its chapter gaps under it.
### Information screen (Fused Glass)
- Overview: poster with progress and times, kicker, title, a meta line (aired, minutes, rating, genre, studio; films:
  year, rating, director, genre), the ratings, the plot, the cast as chips; at the right the media chips (4K, DV, HEVC,
  DD+ Atmos 5.1, 2.40:1), the audio languages and Up next.
- Down: a second page, File and season: video, audio, subtitles (all languages, counted), file name, size, playing on;
  for an episode the season's episodes (the one playing marked). Up returns to the overview, Back closes.
- Skin settings > Details > Cast photos in the information screen (new row 9761, off by default; aeon.osd.castphotos):
  the cast as round photos with name and character under each, as on the item information view, in one row that
  shifts left as you move along it (Down from the screen reaches it, Down again the second page).
### Media names
- `dts-x` (how this library stores DTS:X) shows as DTS:X in every chip; the player's Dolby Vision chip says DV.
- Strings 32476-32488 in every language.

## 0.40.5 (helper 0.3.71)
### Menu styles: text inside its box
- Skin settings: each style draws the help line inside its own help box, 24 px in from both ends and centred on the
  box's height. It ran past the box's right end, in Bridge far past it (that box ended at the settings column); Bridge's
  help box now runs the whole width. The window's own textbox stays for the other looks.
- Mosaic: the palette tile (four squares) moved from over the first two category rows (Appearance, Look) to beside the
  clock box, on the caption band.
- Add-on settings: the add-on's name in the title box no longer scrolls (a screenshot caught a cut middle part); a
  long name ends in "…", the full name is in the window's header line.
- Checked on the box in Mosaic, Ledger, Bridge and Tab slab: Skin settings, Kodi's settings pages, add-on settings.
### Band under the Home menu
- Skin settings > Backgrounds > Band under the Home menu (new row, Aeon and Glass, off by default; aeon.homeband): a band
  from the menu down to the bottom, darker towards the bottom, with a thin line on top. It used to lie under the
  spotlight pictures, so a spotlight covered it as soon as its picture loaded (it only flashed at start-up); it is drawn
  over them now, under their text and the menu, at the menu's height (middle: line at 653, low: 763). Off: no band.
### Toasts from the clock pill (Fused Glass)
- Skin settings > Look > Toasts from the clock pill (new row, off by default; aeon.toastpill): a notification widens the
  clock pill to the left and shows in it (skin.glass/mockups/clock-pill, look A). The round left end slides out while
  a flat band stretches from the clock, then the text fades in; closing, the text goes first, the pill shrinks back and
  fades to the frosted clock pill. Reduce motion: it only fades. Library views and full-screen video keep the capsule.
- Strings 32472-32475 in every language.

## 0.40.4 (helper 0.3.71)
### A palette for the menus, the library views or both
- Choosing a palette other than Aeon (Skin settings > Appearance > Palette, or View settings > Palette) now asks where it
  applies: Menus and library views (default, as before), Menus only (the library views keep the Aeon colours) or
  Library views only (the menus keep the Aeon colours). The palette row shows the choice ("Nord · Menus only"), its
  swatches show the palette's colours either way. RunScript(script.aeon.helper,palscope) asks only the second question.
- How: the library windows (MyVideoNav, MyMusicNav, MyPics) draw with colour names of their own, lib_<name>; includes and
  variables they share with other windows got a library copy (<name>_L). Every palette file also defines its lib_ names,
  and each palette has two more files: "<palette> (menus).xml" (without them) and "<palette> (library).xml" (only them).
  Made by _src/pal_scope.py; new library code must use the lib_ names. Strings 32466-32469, 32471.
### Corner boxes with the Neutral backdrop
- With Corner boxes on Colors (the default), the library's corner boxes (clock, count, media type ...) take the
  palette's own box colour, a darker shade of it, when the backdrop is Neutral and a palette other than Aeon colours the
  library. The Aeon palette keeps the boxes in the artwork's colours.
  The settings strip, View settings and the Library panel over such a view take the same box colour.
- View settings has a Corner boxes entry for the view on screen: Default (the skin setting) | Colors | Neutral | Fanart |
  Backdrop (per view, like Backdrop). The Corner boxes row in Skin settings has a help text now (32470).
### Toast icons
- Kodi's info / warning / error toasts showed an empty icon slot: the skin had no DefaultIconInfo.png,
  DefaultIconWarning.png or DefaultIconError.png. Added as rounded tiles with a white glyph (_src/ms_toast_icons.py).
### Screensaver: album covers as they are
- The album cover is drawn as it is, without the square edge line and the square card shadow, which showed around
  covers that are not quite square. A soft dropped shadow made of the cover itself follows its real shape.
## 0.40.3 (helper 0.3.70)
### Flix: season posters
- Flix (view 528) on a show's season list draws each season as a poster (the season's own poster, else the show's
  poster, else its icon) instead of a landscape tile, so seasons without landscape art no longer all repeat the show's
  landscape. Episodes, shows and films keep the landscape tiles.
### Strip or Box from View settings
- View settings has a Library options entry (Aeon theme with its own menus) in the side strip and in the box: Strip |
  Box, the same setting as Skin settings > Look > Library options. View settings opens again in the chosen look.
### Aeon theme: the skin's own skip button
- With Skin settings > Behaviour > Skippy: skin's skip button on, the Aeon theme draws its own button (no longer the
  rounded Fused Glass one): a palette tile with the skip glyph and a label cell (SKIP INTRO, time left, a line for how
  much of the segment has played). Skin settings > Behaviour > Skippy: skip button style (new row 9738, Aeon theme):
  - Box pair (default): bottom right at the screen edge; above the pause / seek panel when that shows, above the player
    controls in the player controls.
  - Clock dock: tile and label cell in one row at the top right that ends in the clock box.
  In the player controls the boxes show dark until Up from the seek bar focuses them. New strings 32462-32465 in every
  language. Glass and Fused Glass keep their buttons.
- The segment line is a bar image per whole per cent (media/aeon/skipbar): a progress control cannot read
  Skippy.Segment.Progress (a window property) and stayed empty.

## 0.40.2 (helper 0.3.70)
### The side strip stays the library's settings
- 0.40.1 replaced the library's side strip (Left at a view's edge, the Menu key) with the menu style's big box in the
  Aeon theme. The strip is the default again in every theme. Skin settings > Look > Library options (new row 9547,
  Aeon theme with its own menus): Strip | Box; Box opens the Library panel and View settings as the big box
  (Skin.HasSetting(aeon.libpanel.box)). New strings 32458-32461 in every language.
### Aeon theme menu styles: the Settings hub
- The Kodi Settings hub (window settings) follows the Menu theme in the Aeon theme: Mosaic / Ledger / Bridge / Tab
  slab, the same 13 entries (Aeon_SettingsItems), the focused entry's glyph as the joining tile, its help text and
  "This box" (Kodi, skin, address, screen, uptime) on the row grid. Its Aeon look before became Hub_Classic
  (Includes_Aeon_Menu.xml) for the Fuse menu theme; Glass is unchanged. The System menu stays as it is.
- The menu styles' player info (audio settings, track list) names the audio the way the library's media flags do
  ("DOLBY DIGITAL PLUS · 5.1" instead of "eac3 · 6ch"): MS_PlayerAudio + OSD_AudioChannels.

## 0.40.1 (helper 0.3.70)
### Aeon theme menu styles: the Library panel, View settings and the track panel
- The Library panel (View, View settings, Sort, Order, Unwatched only, Sets, Search, Update / Clean library, Library
  settings; Left at a view's edge or the Menu key) is a menu in the four styles: each row with its icon, name and
  current value (Ledger: the icon in the palette spine, the value in its own column). Beside it the focused library
  item's poster, fanart and facts; the Clean library question explains itself in the side box (Ledger: in the bottom
  row); with music playing the bottom row is the now-playing button. From the System menu (Update / Clean library) it
  shows no library item.
- View settings (1166) in the four styles, at the left with a light dim so the view underneath shows each change.
- The track list over the playing video (audio / subtitle streams) uses the select styles with a light dim; from the
  subtitle settings it offers Download subtitles and Subtitle settings, as before.
- The panels' items moved into includes (LibPanel_Items, LibPanel_CleanItems, ViewSet_Items) shared by the old strip
  (LibPanel_Classic, ViewSet_Classic: Glass, Fuse, Fused Glass) and the styles; the permanent strip in the library
  views is unchanged.

## 0.40.0 (helper 0.3.70)
### Aeon theme: four menu styles
- Skin settings > Appearance > Menu theme now offers, in the Aeon theme, Mosaic | Ledger | Bridge | Tab slab | Fuse
  (Bridge when nothing is set; Glass keeps Glass | Fuse). The four styles follow skin.glass/mockups/aeon-menus: square
  boxes that touch, palette colours (aeon_box, x_panel, x_raised, x_deep), 72 px rows that line up from box to box, the
  white focus bar with dark ink, and one artwork tile touching two boxes.
  - Mosaic: title box and fanart band on top, the list and an info box under them, the poster where they meet.
  - Ledger: columns that share rows (row numbers or icons in a palette spine, the labels, the values or the item's facts).
  - Bridge: title, list and info box step down and across; the poster hangs under the title; the count sits in the step.
  - Tab slab: the open tab runs into the slab under it; the art panel hangs beside both.
- The styles cover the context menu, select lists (not the palette or icon pickers, nor the track panel over the
  video), yes / no / progress dialogs, the player's Audio / Subtitles / Video settings (tabs kept) and Kodi's other
  settings dialogs, Kodi's settings pages (Player, Media, Interface, System ...), add-on settings, and the frame of the
  Aeon Fuse settings window. The System menu and the Settings window keep their look.
- The menus show the item they are about: its poster, fanart, kind, year, runtime, rating, genre, director and plot;
  over the video the playing title's art and its audio / video facts.
- A change between the four styles shows on the next menu (Kodi checks a window's include conditions when it opens);
  going to or from Fuse still restarts Kodi (or reloads the skin).
- Generated by _src/ms_menus.py into 1080i/Includes_MenuStyles.xml; the windows' earlier layouts became
  Ctx_Classic / Confirm_Classic (Includes_Dialogs.xml) and stay in use outside the Aeon theme.
- New strings 32452-32457 (style names, help lines) in every language.

## 0.39.16 (helper 0.3.69)
### All themes
- Home > Planner spotlight: the episode is spelled out, "SEASON 2 · EPISODE 2", with the episode's title after it only
  when it says something (the helper leaves it out for "Episode 2", "Folge 2", "#2", "TBA" ...), so "2X02 EPISODE 2"
  no longer repeats itself. The short 2x02 stays in the library views and the Planner window's rows
  (Aeon_PlSpot_Sub beside Aeon_Pl_Sub).
- Planner items whose calendar sends "None" (or "TBA", "N/A") as the plot show no plot, or the show's plot, instead
  of the word "None".

## 0.39.15 (helper 0.3.68)
### All themes
- Library art check: a season whose picture has the wrong shape, with nothing in its folder that fits, gets an empty
  slot instead of the show's picture (0.39.14 put the show's picture there). The skin already shows the show's
  poster / banner / landscape / fanart for an empty season slot, and a media manager fills an empty slot once real
  season art exists, while a filled one looks done to it. The 728 seasons on the box (58 on the PC) that 0.39.14 had
  given the show's picture were emptied again.
- Its summary says what changed where: first line "Only Kodi's library changed. Your files are untouched." (32451);
  "Now uses a picture from the same folder that fits" (32444), "Slot left empty: the skin shows the show's picture
  until season art is added" (32450), toast "Fixed in the library: N" (32447). All languages.
  _src/fg_artguard_showart.py, _src/fg_artguard_wording.py.
### Fused Glass
- Home > Planner week strip: today's tile has a gold ring (fg/ring24.png, 3 px outside the radius-24 tile) in every
  state. The gold line on it was hidden while the tile was white (focused, or while the menu had focus), so today lost
  its mark exactly when it was looked at.
- Toast, background progress and busy capsules dock by what is on screen: beside the clock capsule wherever one is
  drawn (TV guide, TV channels, programs, pictures, favourites ... had them slide over the clock: the old Aeon list
  of windows with a clock box did not know them), in the clock's place only where there is none (full-screen video /
  game / slideshow without the OSD, the OSD with its clock off, the music Now playing page; FG_NoClock), 92 px further
  right beside a clock without weather (FG_ClockNarrow). _src/fg_toastdock.py.

## 0.39.14 (helper 0.3.67)
- Library art check: seasons with nothing in the folder that fits took the show's picture (replaced in 0.39.15).

## 0.39.13 (helper 0.3.66)
### All themes
- Library art with the wrong shape (the helper's artguard.py): Kodi picks local art by file name only, so a folder with
  season06-poster.jpg (a real poster) and season06-poster.png (a 500 x 281 landscape picture) gave the season the .png
  on every refresh. Posters, key art, banners, landscapes and fanart are now measured; one with the wrong shape is
  replaced by a picture of the same name (another extension; for poster.* also folder.*) in the same folder that fits.
  Files are never touched.
  - After a library update (a refresh, a scan) the updated items are checked once Kodi is quiet; a toast says what was
    replaced. Skin settings > Motion, memory, reset > "Auto-fix art with the wrong shape" (on by default) switches
    it off.
  - Skin settings > Motion, memory, reset > "Check library art now": starts from Kodi's texture cache (every picture it has
    shown, with its size, in one call), checks the films and shows in the video folders that hold a picture of the
    wrong shape, fixes what it can and lists the rest (a season "banner" that is really a poster).
  - The two rows (9548 switch, 9549 action) sit under Reset; where the Linux memory rows are hidden they move up.
    Help lines 32448 / 32449. New strings 32441-32449 (all languages). _src/fg_artguard_strings.py,
    _src/fg_artguard_rows.py.
### Fused Glass
- Add-on icons with round corners: the add-on browser's big icon is a 420 px tile (radius 28, fg/m420x420.png; it was
  square-cornered), and the icons of generic list rows (add-ons, programs, files) use radius 12 (fg/m48x48.png; the
  old radius 8 hardly showed at 48 px). _src/fg_addonicons.py.

## 0.39.12 (helper 0.3.65)
### All themes
- Information page: the studio / network logo sits at the top card's right edge (48 px in, the poster's margin on the
  left), level with the buttons; it was at the art's lower left, near the middle of the card.
- File browser (Choose art > Browse..., sources, paths): Right from a list longer than one page reaches its scroll bar
  (Up / Down page through it, Left goes back); it went straight to the buttons. Select dialogs already did this.

## 0.39.11 (helper 0.3.65)
### All themes
- Information page > More > Choose art: the image picker says which art it is for, "Choose art · Poster" (Kodi
  gives the art-type list and the picker the same heading). The helper follows the type focused in the art-type list
  (Window(Home) aeon.arttype); FileBrowser.xml shows it beside Kodi's heading and clears it on close.
  AG_GenericDialog takes an optional header_visible. _src/fg_artheading.py.

## 0.39.10 (helper 0.3.64)
### All themes
- Player overlays during a trailer started from an information page (Video OSD, seek bar, information screen): the
  show or film it belongs to instead of "Now playing in MOVIES" and the file name ("TVSHOW-TRAILER"): its kind (TV
  shows / Movies), clearlogo (or its name), its poster on the card and "<name> | Trailer" as the card's line. The
  helper leaves them in Window(Home) aeon.tr.kind / title / logo / poster and the playing file in aeon.tr.now; the
  overlays use them only while that very file plays (Aeon_OSD_Trailer). _src/fg_trailer_osd.py.

## 0.39.9 (helper 0.3.63)
### All themes
- Information page > Trailer: the trailer plays full screen. The button ran PlayMedia and left the page open; a YouTube
  trailer takes seconds to resolve, the busy dialog was the top dialog when the video began, and so Kodi switched to
  full-screen video under the page instead of closing it (the trailer played behind the page, reachable only via
  Home). Now RunScript(script.aeon.helper,trailer,play,<path>) closes the page first, as Kodi's own trailer button
  does, plays, and brings full-screen video to the front once the video runs if it is not there.
### Fused Glass
- Busy indicator (DialogBusy: a plugin resolving, a slow folder): a capsule like the toast instead of the Aeon box in
  the top right corner, docked beside the clock capsule (rail clock / no clock as the toast): the spinner in a 40 px
  disc 12 px inside the round end, "Loading..." (31952) and Kodi's percentage. Drops a row below a toast and below the
  background progress. _src/fg_busy.py.
- Background progress capsule (PVR channels / guide loading at boot, scans): the percentage is centred on the
  capsule's height, 24 px in from the round end (it sat on the heading line up in the curve); heading and line stop
  12 px before it.
- Toast, background progress and busy capsules are near solid (fg_panel instead of fg_frost2): the view's item count
  behind them showed through the frost.

## 0.39.8 (helper 0.3.62)
### All themes
- Guide > EPG tools: "Scroll through channels" (new string 32440, all languages) closes the card and focuses the
  guide's scroll bar: Up / Down page through the channels, Left / Right / Back return to the grid (the scroll bar could
  not be reached, Left / Right move through time). AG_Scrollbar takes an optional onback. _src/fg_epgscroll.py.
- Player overlays: when the playing episode's season poster is a landscape picture (Cheers season06-poster.png is a
  500 x 281 JPEG), the show's poster is shown instead of a zoomed-in crop (helper: aeon.osd.noseasonposter).
- Music views, Fanart list: the artist's facts (formed / born, disbanded / died, years active, genre) show whatever the
  view's Biography option; that option hides only the biography.
### Fused Glass
- Background progress (DialogExtendedProgressBar: channels and guide loading after a boot, library scans) had no
  Fused look and showed the Glass gradient: it is the toast capsule now (spinner in the round end, heading, percent,
  item; the progress fills the capsule). _src/fg_extprog.py.
- Guide: the now pin's dot sits on its line, and the line runs down the grid right on the edge of the dimmed past
  (it was faint and sat behind that edge). Over the last channel row the line fades out. media/fg/epgnow.png is
  24 x 128 (borders 0,46,12,80): the ruler on top, a fixed 80 px bottom where the line fades while the tint stays even.
- Lyrics (CU LRC window): the shade over the cover has the cover's round corners (Lines and Words on the cover).

## 0.39.7
### All themes
- Fixed: Kodi froze (black screen, JSON-RPC dead) right after a song was stopped. gdb on the box: the GUI thread waited
  in CDirectoryProvider::IsUpdating() for a label testing Container(9881).IsUpdating (a Home row's item count) while
  that row's loader held the lock, evaluating its path, which needed the GUI lock. Every Container(<id>).IsUpdating
  test is gone: row counts show nothing while a row is empty, the Home strip paths no longer wait for the submenu
  list, empty-state labels (classic Home, Planner day) fade in after a short delay. _src/fg_deadlock.py.
- Lyrics (CU LRC Lyrics window): Left / Right scrub the song 10 s, Up / Down 60 s (with "Lyrics take focus" on, Up /
  Down still pick lines). The add-on focuses its list after every lyric line, which took the focus out of the music
  OSD (its highlight vanished, the next arrow key started again on Pause): the list is disabled while the OSD is open.
### Fused Glass
- TV / Radio guide restyled after mockup A (skin.glass/mockups/epg-guide) with the chips of B: one frosted card; its
  head section shows the selected programme (logo, title, chips: Now, start - end, length, channel; plot), the grid
  below: 7 channels, 2.5 hours, number and logo per channel, r12 cells (concentric with the r28 card), airing ones a
  shade lighter, "No information available" in a dimmer cell for channels without guide data, the white tile for
  focus. Now: a gold pin on the ruler and a light dark tint over the time already passed (the grid's progress
  indicator, fg/epgnow.png), instead of the grey veil. _src/fg_guide_a.py.
- Music now playing page: the card and the cover have the round corners of the other Fused cards (r28); the song's
  progress fills the card as one bar inside the same shape. _src/fg_npcard.py.

## 0.39.6 (helper 0.3.61)
### All themes
- TV / Radio guide > EPG tools > Channel group: the helper (`epggroup`) closes the tools card, opens Kodi's group list
  on the guide and, once the chosen group has loaded, goes to its first channel with the focus on the grid (the
  card's close animation and the group list overlapped; on the box it ended on Home). Cancel: back to the grid.
- Home heading of a custom item's spotlight: like Movies, the sort's phrase with the item's name in bold ("RANDOM
  **SETS**"); a spotlight label that is just the item's name no longer replaces it. New strings 32433-32439
  ("Random %s" ...) in all languages, each built from that language's own movie phrases.
- Curvature (new rule, `_src/fg_curvature_audit.py`): every rounded texture's corner arc fits inside its 9-slice
  border and no corner is rescaled. Fixed: pills drawn at another height than their texture (40 px bubbles from the
  44 px pill, a 36 px pill from the 40 px one, 4 px marks from the 6 px one: new aeon/pill_36.png, fg/pill4.png),
  near-pills a few px taller than 2r (the "In library" pill r15, the seek bubble r18).
### Fused Glass
- Pills are semicircles and nested shapes concentric: the TV area tabs card and the Power card's focused row are r30
  at 60 px (their 44 px pills / discs, 8 px inside, are r22: 30 - 8); the settings strip's focused row is an r24 bar
  8 px inside the r32 panel on both sides (it touched the panel's left edge); the Skin settings option columns sit
  12 px inside their r28 card, so their r16 bars are concentric (28 - 12).

## 0.39.5
### All themes
- Skin settings > Home menu: "Choose icon" was nested inside the custom-item "Set path / content" row (since 0.26.0):
  on a custom item (Sets) it was drawn on top of that row, on every other item it was missing. It is its own row
  again, between Rename and Set path. _src/fg_editcard.py.
- Skin settings > Home menu / Context menu: Back on an option row closed Skin settings (its onback ran SetFocus and
  then fell through); it returns to the row the options belong to. _src/fg_editback.py.
- Live TV (Channels, Recordings, Timers, Search): the list card is as wide as the area tabs card (102 to 1334); the
  info panel beside it is narrower (x 1380, 440 wide) and the channel icon 150 px instead of 300.
  _src/fg_tvlayout.py.
### Fused Glass
- Skin settings > Home menu: the selected item's options sit on their own card, like the context-menu editor's;
  both option columns sit inside their card (they started 16 px left of it).
- The "Fuse" menu theme no longer overrides Fused Glass: lists and buttons keep the white highlight (it gave the
  coloured Fuse bar when both were on). The Fuse option only applies to the Aeon and Glass themes.
- Live TV options row: Filter, Show hidden, Group items, the watched filter and the other radios are frosted pills
  with the round white focus, like Group / Sort / Order.

## 0.39.4
### All themes
- Live TV always draws in Figtree, whatever font combination is picked: the labels of the TV windows and TV dialogs
  that used the preset's library / player fonts use Kodi's font set (Figtree; Roboto CJK in the CJK set). Figtree has
  the channel symbols; most preset text families do not. _src/fg_tvround.py.
### Fused Glass
- Live TV: the white focus of the area tabs and of the options row (group, sort, order) is the same round pill as the
  frosted ones (r22 at 44 px: fully round ends); it was the button focus texture with ~18 px corners. Frost focus
  style: a light frost pill; Outline: a white ring; Flat stays flat. The options rows of the add-on browser and the
  playlist windows (same button) match. _src/fg_tvround.py.
- Library settings strip: music is the bottom band of the panel itself (like the foot of the List view card): a
  hairline, then a slightly lighter shade with the panel's own round bottom corners (new fg/rb32.png). Left to right:
  the cover (48 px, rounded) centred in the icon column, the moving bars, artist and song. The song's progress
  reveals a lighter band from the left with a straight edge. Focused: the band turns white with dark ink, the progress
  a darker band on it. _src/fg_stripnp2.py.

## 0.39.3
### All themes
- Fonts: the skin's Figtree files now have U+2726 (four-pointed star) and U+25CF (black circle), the two symbols the TV
  channel and programme names use (drawn as boxes before; Kodi has no font fallback). _src/fg_figtree_symbols.py.
- TV / Radio windows: the area row (Channels, Guide, Recordings, Timers, Timer rules, Search) is a row of equal tabs;
  the open area is marked; Left / Right switch straight to the next area (no OK) and the focus stays on the tabs. The
  tabs are a plain group (id 9000, still the menu control), not a grouplist: a grouplist links its children left /
  right itself, so Left / Right only moved the focus. _src/fg_pvrtabs.py, _src/fg_pvrtabs2.py.
- Home spotlight of a movie set: the row of dots follows the film strip (level with the posters, after the last one);
  it sat at its fixed place after Play / More information, which a set does not have, so it floated mid-screen.
  _src/fg_setdots.py.
### Fused Glass
- The tabs sit on a frosted card; the options row under them (group, sort, order) has glass pills. The focus pill is
  drawn by the card in the chosen focus style, its body exactly on the tab (the fxb_*.png textures have a shadow
  margin, so on the tab itself the white pill was smaller than the grey one of the open area and the label sat low).
- Home menu, "only the focused item's name": the icon row is centred on the screen.
- Home now playing capsule: the song's progress fills the capsule with a lighter frost from the left (was a thin line).
  Kodi sizes a progress fill from its background image's height, so both use the same 80 px image.
- Library settings strip (dialog 1160): music playing is the open panel's bottom section, shown as soon as the strip
  opens (was the Aeon white bar, only while its box had focus): a lighter rounded card, rounded cover, artist and title,
  the moving bars, and the song's progress filling the card. Focused: a bright edge; OK opens the visualisation.
  _src/fg_stripnp.py.

## 0.39.2
### All themes
- Home > Planner week strip: Down from the Planner item reaches the seven days (grouplist 9310), Left / Right move, OK
  opens the Planner on that day in the Day view, Up or Back return to the menu. The day in focus is the white tile
  (today's while the menu has focus; today keeps a small mark). Each day's count is split by kind: a TV icon with the
  episodes, a film icon with the films, a music icon with the albums.

## 0.39.1
### Fused Glass
- Home menu, "only the focused item's name": three icons on each side of the focused item instead of one on the left
  and the rest on the right, every gap the same (110 px between icons, and between the name and the next icon); the
  focused icon keeps its place. The wraplist only does the moving in this mode; a row after it draws the icons
  (Container(9000).ListItem(-3..3)) and the name, which rolls out of the icon on every move.

## 0.39.0
### Fused Glass
- The skin's skip button on the player cards, two styles (Skin settings > Behaviour > Skip button on the player card,
  Skin.String(aeon.skippy.cardstyle)): Tab (default), a smaller white pill sitting on the card's top edge, or Glass,
  a capsule of the card's own frost above the card's right edge. Over the small seek bar the skip dialog takes that
  shape; the Video OSD (which closes the skip dialog) draws its own skip button on its card while Skippy asks about a
  segment: Up from the seek bar reaches it, OK skips, Down goes back. Away from the player cards the button stays the
  full white capsule with the time left.
- Planner: day cells, option buttons, day-view rows and thumbnails are rounded; the week view's thumbnails are
  rounded with the walls' inner ring on focus; today is marked with the small accent mark.
### All themes
- Planner: what is in the library already (episode by show, season and number; film by title and year; album by
  title and artist) gets a white check badge on its picture, "In library" on the week view's pictures and
  "Available in library" in the day view.
- New strings 32427-32432.

## 0.38.0
### Fused Glass
- Home > Power: Up opens a frosted card above the Power item with every option of the Power sub-menu listed
  vertically, each with a line icon in a glass circle (new icons fg/pw_*.png: restart, update, log off, exit, switch
  user, screensaver); the focused row's circle turns white, with a red icon for Shut down. The card grows with the
  number of options; focus starts on the bottom row; Down, Left, Right or Back return to the menu.
- Home menu: Skin settings > Look > "Home menu: only the focused item's name" shows the other items as icons only
  (conditional item layouts of 9000); the focused item's name now rolls out of its icon each time it gets focus.
- TV guide: programme cells are rounded glass tiles with gaps (the focused one white) on a frosted card; EPG tools is
  a floating rounded card with inset pill rows instead of the black side panel.
- Player: the information screen has the Video OSD's card behind it (rounded poster, pill time bubble); the small
  seek bar uses the OSD's seek line, chapter ticks and round marker.
- Toasts: the icon sits inside the capsule's round end, cut to a circle (it stuck out of the capsule).
- List view (510): the card and the rail now run from 24 to 1056 with rounded corners at both ends and line up; the
  rail's corners are smaller so the clock and the item count fit (all 100 px rails); 8 rows, and the ratings, chips
  and view label sit inside the card on a lighter rounded foot (the dark band ran past the card and the second chip
  row was cut off).
- Low list (527): the rows sit in one frosted card like the List view (no card per row).
- Episode thumbs: a dark corner gradient behind the season / episode tag, through the thumb's rounded mask.
### All themes
- Low list: the episode thumbnail moved down beside the network logo.
- Font combinations: the 14 pairings from the font page are presets too (Funnel Display, Cal Sans, Hubot Sans
  Condensed / Expanded, Saira Condensed, Clarity City, Gnomon, LT Superior Serif, LT Veritas Condensed, Cooper Hewitt,
  Bebas Neue + Clarity City, Fraunces + Ronzino, Oswald + Pretendard, TASA Explorer); fonts in fonts/ with their
  OFL licences (README-fonts.txt). LT Victoire + Ronzino is held back: LT Victoire came without a licence.
- New strings 32425-32426.

## 0.37.0
### Fused Glass
- Landing animation (Skin settings > Appearance > Landing animation, string aeon.fganim): Pop (default: a quick swell
  and settle), Grow, Fade, Glow (the drop shadow turns into a white halo that swells), Nudge, Lift or None. It plays
  when the highlight lands on a list item, menu entry, settings row or button. Conditional animations, so no reload
  (FG_LandFocus / FG_LandVisible / FG_LandShadow* in Includes_Fused.xml). New strings 32415-32422 (all languages).
- Video OSD: "Now playing in TV shows" sits as a small line over the clearlogo (or the title, in the heading font) on
  the clock capsule's middle line, at its margin from the edge. Skippy's next episode moved from the top bar into the
  card, under the poster and the "Ends" ring. Poster, ring and disc art are centred in the card; the divider runs
  from the episode line down as far as it starts below the card's top.
### All themes
- Font combinations (Skin settings > Fonts): Figtree, Fraunces + Figtree, Bebas Neue + Figtree, Oswald + Source Sans 3
  and Barlow Condensed + Barlow, each shown in a mock-up in its own fonts before you pick it; "Fonts per section"
  keeps the old per-section choice. New heading faces in fonts/: Fraunces Bold and Oswald SemiBold (static cuts),
  Bebas Neue, Barlow Condensed Bold (all SIL OFL, see README-fonts.txt). The per-section list now offers one-weight
  faces for Headings too. New strings 32423-32424.
  In Fused Glass the picker's mock-up is a rounded card with a white pill on the focused row.
- Video OSD: the elapsed time, the duration and Skippy's segment line sit 12 px higher, so the seek marker no longer
  touches them at the start and the end.

## 0.36.0
### Fused Glass
- Focus highlight (Skin settings > Appearance > Focus highlight, string aeon.fgfocus): White pill (default), Flat
  bar, Frosted glass, Outline or Tight bar, for library lists, menus, Skin settings and Kodi's settings pages. Every
  style except the flat bar keeps its gap to the card edge and casts a soft drop shadow; the flat bar reaches the card
  edges. On Frosted and Outline the text and switches of the focused row stay white. Buttons take their focus picture
  when the skin loads, so changing the setting reloads the skin. New strings 32408-32414 (all languages).
- The skin's own skip button for Skippy (Skin settings > Behaviour): a white capsule with a soft shadow, a dark disc
  holding the skip icon inside a ring that fills as the segment plays, "Skip Intro" and the time left.
- Home: the accent mark sits centred under the menu item's icon.
- Settings pages: the help text box is exactly two lines tall (it scrolls); a third line was cut in half.
### All themes
- The old gear picture is gone from the settings windows, add-on settings and the menus over Home (Home's System page
  keeps its own).

## 0.35.0
### Fused Glass
- Settings: every settings dialog Kodi builds (sources, profiles, PVR, content, lock settings, the player's audio /
  subtitle / video panel) uses the same rows as the settings pages (72 px, white focus pill, switches); the player's
  panel is a frosted rounded card. Groups of settings are divided by a fine line (Radarr / Sonarr / Lidarr ...). The
  line above the level button (Expert) and the line above the help text now sit at the same height. The focused
  category gets its white pill (Control.HasFocus does not work for Kodi's negative category ids).
- Music Fanart list: the foot of the list card (a little lighter, under a hairline) holds what the Aeon view had: the
  album-stack icon with the album count and the album cover that changes every five seconds (albums: the artist's
  picture), beside the biography. The row of all album covers is gone. Artists show their clearlogo above the facts
  (the name when there is none).
- Skippy's skip button: a white rounded card with a soft shadow and a rounded progress bar inside it.
- Chapters dialog: the Trickplay / chapter pictures are rounded, with a soft shadow, a fine light edge and a white ring
  in focus.
- Home now playing: the position setting cannot be changed (the capsule always sits beside the clock); the row is
  dimmed and its help says so (new string 32407, all languages).
### All themes
- Home spotlights (TV shows and the shows strip) and the widget screens: chips with the number of seasons, episodes,
  watched and unwatched episodes (Kodi's own words, every language).
- Home now playing "Corner" (Aeon): top right under the clock and weather tiles, as on the screensaver (the top left
  holds the spotlight's category); one tile higher without weather. The preview in Skin settings shows it there.
- Backdrop Neutral: a soft light and a vignette instead of a flat ground. Backdrop Colours: the colour comes from the
  picture on screen again (artist photo, poster, cover), not the hidden fanart (helper 0.3.55).
- Clocks show 24-hour time (System.Time(HH:mm)).
- Dolby Vision chip: every profile from the film's .nfo or .cmm_mediainfo.xml: P5, P7 FEL / MEL, P8.1, P8.2, P8.4, P10
  (helper 0.3.55).

## 0.34.0
### Fused Glass
- Settings pages like the Settings mockup: Kodi's settings pages and the add-on settings dialog are separate frosted
  cards with a gap (categories; options; OK / Cancel / Defaults), 64 / 72 px rounded rows without rules or dark row
  boxes, the white focus pill, the open category as a frosted inset pill, on / off switches instead of ticks, the help
  text inside the options card under a hairline (with an info icon), the scroll bar inside the card. The old frame
  lines (which drew square corners over the rounded cards and touched them at the top) are gone. Skin settings: the
  categories and the options are two cards (the context-menu page has a third for its side panel), no rules between
  rows or categories, the open category an inset frosted pill.
- Information pages: the fanart fades in from the left through its own mask instead of a solid fade strip, so there
  is no hard line where the poster area meets the art; a soft shade at its foot keeps the buttons readable. Reviews,
  Recommended / Similar posters and the music info rows are rounded with a white ring in focus.
- Library: the List view's frosted panel runs off the top of the screen and keeps 12 px round the row pills (the
  numbers on the right no longer run into the pill's edge); Banner list banners, its focus and its poster / landscape
  are rounded; the progress line under art (which ran past rounded corners) is a small progress ring in the corner.
- The A-Z scroll marker is white.
- Music Fanart list: the list card runs to the foot of the screen; under a hairline it holds the biography (album:
  review), then for artists the number of albums and a row of rounded album covers; the right card keeps 24 px
  padding round the facts. Albums show their number of tracks on every row and in the facts (helper 0.3.54).
- Screensaver: posters and album covers are shown whole (nothing cut off at the sides) and the rounded mask follows
  the picture as drawn.
### All themes
- Backdrop (Skin settings > Library background, per section in the spotlight editor, per view): Neutral, Fanart and
  Colours now work in the Glass themes too, in every view and for music. Colours takes its colour and soft wash from
  the item's fanart, which stays hidden (helper 0.3.54). Glass themes keep fanart while nothing is chosen.
  The setting is now called "Library background (all)" (all 23 languages).
- Cards view: landscape art first, without a clearlogo on top (landscape carries the title); without landscape the
  fanart with the clearlogo or the title.
- Home music spotlight: the artist logo of an album sits under the category header, the album title right under it,
  the info chips close under the title.
- Home spotlight: a show whose clearlogo is named in the library but missing from disk now shows its title (the helper
  checks the logo on screen).
- Music information page: the cover is round for artists and rounded for albums again (a texture's mask cannot be a
  variable; Kodi drew it square).

## 0.33.0
### Planner (all themes)
- Planner sources: the wanted titles of Radarr, Sonarr and Lidarr join the Planner, the Home Planner spotlight and
  This week. Films you are waiting for show when they come to the cinemas ("In cinemas"), while they play there ("In
  cinemas now", listed on today), when they come out on streaming ("On streaming") and on Blu-ray ("On Blu-ray");
  Sonarr's coming episodes join those the Planner already knows (an episode is listed once; one of a show that is not
  in the library says "New show"); Lidarr's coming albums show with their artist ("New album"). Only what is monitored
  and not downloaded yet is listed. The Planner's options (Left in the Planner) have a Planner sources row that opens
  the helper's settings: each app's address and API key, how many days ahead, Read now. Needs helper 0.3.53.

## 0.32.0
### All themes
- Rounded artwork no longer shows square corners. With aspectratio scale, Kodi stretched the rounded mask over the
  whole scaled picture, so a poster or cover that is not exactly the frame's shape had its rounded corners cut off
  (Showcase's focused poster, Combined's season posters, the artist fanart wall). Every masked picture now has
  `scalediffuse="false"`: the mask fits the frame.
- Home spotlight: its category (Random shows) and, with a strip in focus, the strip's category (Recently added
  episodes) stand at the top left as on the widget screens, upper case with the last word bold (RANDOM **SHOWS**;
  the helper writes it, any language). The clearlogo, or the title when there is none, sits in one fixed box above the
  info rows (640 x 150), so logos come out the same size.
- Widget screens: the episode line (SHOW | 2x03) moved above the clearlogo box; it ran under the logo before.
- Settings backdrop: no longer one remembered fanart (the skin string aeon.lastfanart, written every two seconds and
  stuck on whatever was seen last). The helper keeps the fanart of the spotlights and strips seen on Home, plus a few
  random library titles, and each settings screen opens on a random one of them.
- Home > Favourites: the Favourites menu item has its own page now. Over a new heart picture (in the style of Power,
  Search and System) Kodi's favourites stand as a row of cards under the menu (Down from the menu), in the groups All,
  Video, Music and Add-ons (left of the row; Up / Down change the group). A favourite of a library show, film, set,
  album or artist brings that item's artwork and plot; the card in focus is the spotlight (its fanart, clearlogo,
  what it is, plot). OK opens it as Kodi's Favourites window would; OK on the menu item opens that window as before.
### Fused Glass
- Music views: the focused row of the album and song lists is dark on the white pill (it was white on white); rows
  have an inset pill and rounded covers; Cover showcase has rounded covers, a ring for focus and a frosted stand-in
  where an album has no cover; the music List view is two frosted cards; the album list's side cover and biography
  panel are rounded.
- Pagers (spotlights, Planner, widget screens): the current item is a short pill and the others small dots, as on the
  screensaver.

## 0.31.0
### Fused Glass
- Library views, the rest: Showcase, Flix, Combined (also its row of seasons / episodes), Grid, Pictures, the Episode
  list and the seasons view draw their artwork rounded (masks `fg/mWxH.png`), the focus as a ring inside the artwork
  instead of a square accent frame, and the Episode list / seasons view as two frosted cards with inset pill rows.
- Real frost: the helper (0.3.51) makes a blurred copy of the backdrop on screen; the skin lays it under the List view
  panel, the Episode list cards and the A-Z rail through masks of their shapes (`fg/bm*.png`), so those panels show
  the colours behind them softly. The panels' tint is lighter there (`fg_frostb`).
- A-Z: while a letter has focus, the letter shows large on a frosted tile beside the rail; the focused letter of the
  wall rails is a circle, as in the List view.
- Home: the categories of the focused item (Recently added, In progress, ...) stand as tabs left of the strip, the
  current one in a frosted pill (Up / Down on the strip change it, as before); the heading lines above the chips
  (Random movies, 3x01 · Marnûkh) in sentence case; now playing as a frosted capsule left of the clock capsule with
  the cover in a circle and four drawn spectrum bars (the placement setting stays for Aeon and Glass).
- Spectrum bars drawn by the skin (`FG_EqBars`, `FG_EqBarsM`): four rounded bars that rise and fall on their own
  cycles while music plays and settle low when paused; used on Home, the library rail and the screensaver.
- Player: the Video OSD is a floating frosted card (poster rounded) over a soft scrim; the top bar of the player
  overlays has no black band, the clock and weather are the clock capsule; the buttons focus as a white circle
  (text buttons a pill), the seek marker is a round knob.
- Dialogs, settings, information screens: the shared card (`Aeon_Glass`, about 60 screens) is a rounded frosted card
  with a soft shadow; the context menu has its own frosted panel (`dialogs/panel_fg.png`) and inset pill rows; the
  clock box of settings, information and other windows is the clock capsule, and toasts dock beside it.
- Screensaver: the poster floats as a rounded card, the album cover is rounded, the pager is a column of dots with
  the current slide as a pill, the clock is the clock capsule and now playing a frosted card with the spectrum bars.
- Settings windows and Skin settings: one frosted card for both columns with a hairline between them; Home: the
  System panels, the Live TV list (rows as frosted pills) and the Power row as rounded frosted shapes.
### Home (all themes)
- Power: over the picture the date, the time, Kodi's uptime and what is playing; under the menu Kodi's shutdown timer
  (Off, 30, 60, 90, 120 minutes; Down from the menu) with the time left while it runs (Kodi's own words).
- Planner: under the menu "This week", seven day cards from today with how many episodes and films come out each
  day (from the helper's Planner list).
- Search: Recent searches. The helper keeps the last eight searches made in the Search window; under the menu on
  Search a row of them (Down from the menu); OK runs one again, Clear forgets them. New text 32406 Recent searches in
  all 22 languages.

## 0.30.0
### Weather on Home (all themes)
- The Weather item of the Home menu (Skin settings > Home menu: choose Weather for a position) has its own page:
  over the weather fanart of the current condition, the location, a large icon and temperature, the condition, then
  feels like, wind, humidity, sunrise and sunset, and a panel with the next eight hours (time, icon, temperature,
  chance of rain). Under the menu "This week": seven day cards (day, icon, high, low, outlook); Down from the menu
  reaches them, OK opens Kodi's Weather window. Without a weather service a line says where to choose one.
- Data from the weather add-on's Window(Weather) properties (Hourly.N.*, Daily.N.*, Current.*, Today.*; tested with
  Open-Meteo). Icons from resource.images.weathericons.white and fanart from resource.images.weatherfanart.single
  when installed, else the skin's own icons and background. Fused Glass draws the panels and cards frosted and rounded
  with the rain chances in its accent; Aeon and Glass draw them as dark translucent boxes.
- The day icons are drawn over the cards, not in the list: a list item's picture is resolved once, before the
  forecast has arrived, and stayed on the fallback.
- New texts 32403 Next hours, 32404 This week, 32405 (no weather yet), in all 22 languages; the others are Kodi's own
  (Feels like, Wind, Humidity, Sunrise, Sunset, Today).
### Screensaver
- Weather slide: with the screensaver's weather switch on (Skin settings > Backgrounds), the fourth of the ten slides
  shows today's weather (icon, temperature, condition, today's high / low, feels like, wind, humidity, sunrise, sunset)
  and this week's seven days, over the weather fanart (`_src/wx_screensaver.py`).

### Home (all themes)
- The darkening layers of Home (vignette, the gradient over the lower part, the band, and in Fused Glass the scrims) now
  lie under the spotlights and their text. Drawn after them, they darkened the clearlogo, ratings, chips, plot and
  buttons a second time on top of the spotlight's own scrims.
### Fused Glass
- Toasts: on Home a capsule beside the clock capsule; in library views, settings and the player the same capsule docks
  at the top right beside the clock (ending at x 1808, top 24).
- List view: the poster as a rounded card (572 x 858) with a soft shadow, the list in a frosted rounded panel, the
  focused row a white pill inset in it, no column tints or runtime rule.
- Low list: every row a separate frosted card with a gap, the focused one white; rounded poster and episode still; no
  rule beside the list.

### Fused Glass: library views (part 1)
- Rails: the A-Z strip and the settings strip keep their columns but draw as floating frosted pills inset in them
  (`media/fg/rail100.png`, `rail80.png`, `rail60.png`, exactly as big as the columns, so nothing is stretched); the
  coloured boxes in them (clock, count, section) and the fanart in those boxes are gone. The focused letter is a white
  circle with dark ink.
- Settings strip opened (Left at the edge of a view, Menu; View settings): the rail grows into a near-solid frosted
  panel, every setting shows its name and value, the focused one is a white pill. No row dividers.
- Lists (List, Episode list, Season list, Compact list, Banner list, Low list, Planner, music lists): the focused row is
  a rounded white pill (27 rows), dark ink on it.
- Walls (Poster, Landscape, Square, Album, Artist walls): rounded tiles (masks at each tile size), rounded dim and
  scrim, a 3 px white ring inside the edge of the focused tile; the dark bar behind each caption is gone.
- The header clock of the walls is left out in Fused Glass (the rail has the clock). Glass: the item count no longer
  sits under that clock.

### New theme: Fused Glass (work in progress)
- A third theme beside Aeon and Glass, from the Glass redesign mockups: frosted rounded panels, white focus with dark
  ink, one warm accent for marks and progress, outlined tech chips, sentence-case menus. Skin settings > Appearance >
  Theme now has Aeon | Glass | Fused Glass (Kodi's theme "Fused Glass", `media/Fused Glass.xbt`). Glass stays as it is.
- Built on Glass: the theme sets `aeon.vglass` and `aeon.fglass`, so every screen without a Fused Glass variant yet draws
  its Glass one in the Fused Glass colours (`colors/Fused Glass.xml`: dark frost in every mood, white focus). Parts are
  restyled screen by screen; new parts live in `1080i/Includes_Fused.xml`, textures in `media/fg` (made by
  `_src/fg_textures.py`: rounded shapes, 1 px edges, focus rings, shadows, scrims, tile masks).
- First part: Home menu (sentence case, the focused item with an accent mark, the others quiet), strip tiles (rounded,
  a 3 px white focus ring, rounded dim), Play / More information as capsules, outlined chips (also in the library views
  and the information screen), soft scrims instead of the band under the hero, the clock and weather as one capsule,
  toasts as a capsule beside it, and white rounded focus rows in lists.

### Home menu
- Home strips (the rows under a Home menu item) now use the Sort by, Reverse order and Items in row chosen for each
  submenu entry in Edit submenu. They were saved but the strip loaded its path with no sort and a fixed 12 items, so
  "Sort by: Last played" did nothing. Default order: newest / highest first, titles A-Z; Reverse order flips it.
- Artwork type: new **Thumb** choice: the item's own thumb on a 16:9 tile, for episodes the episode still (not for
  films, shows, seasons and sets, whose thumb is a poster; unwatched episodes stay hidden under the spoiler setting).
  **Landscape** now shows the landscape artwork, for an episode its show's landscape. Auto is unchanged.
- The More... tile at the end of a strip takes the shape of its row under Auto (from the row's first item), so an
  episode playlist row ends in a 16:9 More tile, not a poster one.
- Recently watched (films and episodes) is now **Recently played**: watched, or stopped partway with a resume point,
  last played first. Kodi's video library has no recently played node of its own (music has), so this stays a smart
  playlist. In progress shows uses Kodi's own node, sorted by Last played in the default menu.
- Edit submenu: the Autoscroll row is gone (it is a setting of the lists under the menu; submenu strips never scroll
  by themselves). The summary under each entry shows the sort in Kodi's words ("Sort: Last played") and keeps a gap
  before "Reversed" and "Autoscroll off" (also in Edit lists).

## 0.28.4
- Skin settings > Home menu and > Context menu (Classic menu theme): the options pane on the right had its own 3 px
  divider at x 1536, 168-968, beside the page's column line at 1500 and past the page's bottom line at 960: removed,
  the column line divides the pane. The thin lines under each option of those two panes are gone too.

## 0.28.3
### Home menu
- Edit submenu and Edit lists (Skin settings > Home menu): the options of each entry (rename, choose, sort, reverse,
  limit, move, delete ...) show again, and OK on an entry opens them. Since 0.28.0 the editors told an entry from Skin
  Variables' "Add item" row by comparing the label with `$ADDON[script.skinvariables 32078]`; Kodi does not expand
  `$ADDON[...]` inside a condition and its brackets break the whole expression, so every option stayed hidden. The row
  is now told by the `blank` property Skin Variables gives it (works in every language).
### Planner
- Never during playback: see script.aeon.helper 0.3.49 (three minutes after playback and without a key press).

## 0.28.2
### Player
- Seek line: the white fill now lies exactly on the line. Kodi scales a progress bar's fill by the height of its
  background texture; the seek line had none, so its fill came out 8 px tall and below the line, which made the
  marker look misaligned (the marker itself was centred). Fill and background textures are now as tall as the line
  (`aeon/line2.png`, `line4.png`). The same fault is fixed on the Glass track and the Now playing track (18 px fills
  on 12 px tracks).
- Chapter pictures from Trickplay now show the first time the chapters open: the helper crops every chapter as soon
  as the video starts (a list item fixes its picture's path when it is first drawn, so the pictures must exist before
  the dialog opens). They are a fallback under Kodi's own chapter picture, which still wins when it loads. Bookmarks
  get theirs from the next opening.
### Views
- Compact List, films: year, length and rating spaced evenly between the resolution pill and the watched mark (the
  year ran into the hours).
- List view, sets: the set's films fill two whole rows (540 each in the 1080; with 545 only one row fitted, so moving
  to the second row scrolled and showed an empty third row).
- View settings (films and sets): Films of a set (Grid, the default, or One at a time with Up / Down) and Versions of a
  film (One at a time, the default, or Grid); skin-wide, in the List, Banner list and Compact List views. A version in
  the grid names its version.
### Planner
- Updating the Planner list no longer slows the box down: the helper asks TMDb Helper only about the shows that can
  still get episodes, one at a time (script.aeon.helper 0.3.48), not for its library-wide "airing next" list.
- The Planner list is never read during playback: it waits until playback has been over for three minutes and no key
  has been pressed for three minutes, and stops when something starts (script.aeon.helper 0.3.49).
### Home
- System has its own background in both looks, in the style of Power, Search and Live TV (a violet neon gear).
### Strings
- New: 32398 Films of a set, 32399 Versions of a film, 32400 Grid, 32401 One at a time; in all 22 languages.

## 0.28.1
### Player
- Seek line (Video OSD, scrub bar, information screen): the marker is a white square with a dark edge and a soft
  shadow, as if it hovers over the line. It follows Player.SeekBar, so it moves with every Left / Right press while
  scrubbing, before the seek happens. The marker slider is exactly as wide as the line (it was 20 px wider on the OSD
  and 40 px wider on the information screen, so the marker ran behind the fill at the start and ahead of it at the end;
  on the information screen Kodi also drew it at 125 %). Chapter marks on the line.
- Video OSD: the top bar is as tall as the clock box. It reads NOW PLAYING IN TV SHOWS: (or MOVIES:) with the show's
  or film's clearlogo beside it, the title in text without one. Skippy's next episode fits in the bar.
- Video OSD: the poster is the season's (the show's when the season has none) and as tall as the ENDS ring and the
  line beside it; poster, ring and line moved left with it.
- Video OSD: Up on the seek bar opens the information screen.
- The clock box shows in the player in the Glass look too (it was in the Aeon look only).
- Information screen: rebuilt in the Video OSD's dark look (the light rounded panel is gone). The player top bar (the
  time of day on the left, Skippy's next episode or the playlist's next item, clock box, weather box), the season /
  show poster, clearlogo or title, episode line, bedtime line, plot, chips (resolution, HDR, codec, aspect ratio,
  audio, language flags) and every rating (IMDb, TMDb, Rotten Tomatoes, Trakt; from the helper), then the seek line
  with the bedtime tick and the time bubble.
- Chapters and bookmarks: the same top bar and dark scrim; buttons with the playing time on the right, darker
  placeholders with the time. Chapter pictures from Trickplay: when the video has Trickplay sprites
  (`<video>.trickplay/`), the helper crops the picture for each chapter and bookmark and the box shows it wherever
  Kodi's own extracted frame does not arrive.
- Video / audio / subtitle settings during playback open as the side panel over the picture, as designed: the look was
  chosen with Window.IsActive(osdvideosettings) in an include condition, which Kodi evaluates before the dialog is
  active, so they always got the centred black dialog. The dim over the picture is lighter (33 %), so a video setting
  can be judged while it changes.
### Toasts
- Glass: on Home the toast is 100 tall like Home's clock box (it was 108), and it comes out from under the clock box in
  both looks. In the player the toast comes out of the clock box while the OSD, the information screen or the chapters
  are open.
### README
- The aim of the skin at the top.

## 0.28.0
- Translated into 22 languages: German, French, Spanish, Italian, Dutch, Portuguese (Portugal and Brazil), Swedish,
  Norwegian Bokmål, Danish, Finnish, Polish, Czech, Hungarian, Russian, Ukrainian, Greek, Turkish, Japanese, Korean
  and Chinese (Simplified and Traditional) (`language/resource.language.*/strings.po`). The helper, the screensaver
  and the waveform visualiser come in the same languages. Kodi shows English for any text a language lacks.
- Every text the skin shows now comes from its strings.po; no English is left in the XML apart from names, codes
  (codecs, ratings, HDR formats) and internal keys. Where Kodi has the word, the skin uses Kodi's own string, so it
  reads the way Kodi does in that language.
- The skin's ids 31000-31999 were full. Kodi only takes those ids from a skin for `$LOCALIZE` (32000 and up come
  back empty), so the new texts, 32000-32396 in the same strings.po, are read as the skin's add-on strings:
  `$ADDON[skin.aeon.fuse id]`. Conditions and view ids still use 31xxx ids only.
- The TV show status chip (Home and the library) shows Continuing, Ended, Cancelled, In production, Planned, Upcoming
  and Pilot in the chosen language instead of the scraper's English word.
- View names, sort names and other texts that conditions compared as words now go by their string ids, so the view
  picker, the remembered views and the Home menu work the same in every language.
- Texts glued from pieces were joined into whole sentences (the bedtime notes on the player and on Home, "Down for
  the cast"), so each language can put the words in its own order.
- Right-to-left languages (Arabic, Hebrew, Persian) are not included: the skin's layouts only run left to right.
- Japanese, Korean and Chinese need a font with those characters: Settings > Interface > Skin > Fonts, Roboto CJKSC
  (needs `resource.font.robotocjksc`).
- Home spotlight (Aeon): Play is wider and More information sits further right, with the page dots after it, so the
  longer words of other languages fit ("Abspielen", "Mehr Informationen"). Labels that did not fit their fixed width
  in German or Finnish (settings options, the settings categories, OSD and info chips) got shorter wording; the
  Motion, memory, reset category has a shorter name in most languages ("Bewegung, RAM, Reset").
- No label is cut off with "..." in any of the other languages either: shorter wording where a text overran its
  fixed width (mostly Greek, Russian and Ukrainian), option pills widened or rebalanced in 31 skin settings rows, wider
  OSD pills (Subtitles, Chapters, Info, Stats) and Home system-info labels, the Home "No shows in progress" note on
  two lines, and a shorter Spotlight menu-item hint ("Featured slider for this item ...", English too).
- Skin settings, reset: "every the skin setting" corrected.

## 0.27.5
- Lyrics, Words look: the ten lyric fonts now come with the skin (fonts/lyrics, unchanged, with their licence notes
  in README-lyrics-fonts.txt); Estuary MOD V2 no longer needs to be installed.
- .gitignore and .gitattributes for the skin, the helper, the screensaver and the waveform source (caches and build
  staging ignored, LF line endings, binaries marked, tests and git files left out of `git archive`).
- changelog.txt is now this CHANGELOG.md (version and section headings in Markdown). The helper and the screensaver
  have a README.md and a CHANGELOG.md of their own, the waveform source a CHANGELOG.md.
- Kodi's add-on information shows the latest changes (addon.xml news, 0.27.0 to 0.27.5), since its Changelog button
  only reads a changelog.txt.

## 0.27.4
- Episode list: the poster is a little smaller and, with the network logo, moved right of the library side strip,
  which covered both when it opened.

## 0.27.3
- Episode list: the season poster in the left column (the show's poster when the season has none).
- Episode pages: shows without a clear logo show their landscape art again (its check never matched).
- Screenshots: episode list with the poster; Now playing and the screensaver with Adele - Rolling in the Deep (single).

## 0.27.2
- Ten screenshots on the skin's add-on page (Home, list, poster wall, Flix, episode list, artists, Now playing with
  lyrics, video controls, screensaver, skin settings).
- Setup wizard, Menu theme step: the two previews say Aeon Fuse and Fuse.
- README: signde dropped from the sources (jamal2362 has the same TMDb Helper).

## 0.27.1
- Aeon Fuse artwork: an icon and a fanart for the skin, the helper, the screensaver and the waveform visualisation
  (a thin Aeon ring fused with a rounded Arctic Fuse card; each add-on its own sign). Made by artwork/make_artwork.py
  in the source tree.
- README: every add-on the skin uses, required or optional, with what it adds and where to get it; the optional ones
  are declared in addon.xml (the skin) and the helper's addon.xml.
### Helper (script.aeon.helper 0.3.45)
- Icon and fanart; TMDb Helper and KarmaMole Skin Helper declared as optional.

## 0.27.0
### Name
- Glass Aeon is now Aeon Fuse: the look of Aeon 2 with ideas from Arctic Fuse. The skin is skin.aeon.fuse (was
  skin.glass.aeon), the screensaver Aeon Fuse Screensaver (screensaver.aeon.fuse, was screensaver.glass.aeon), the
  helper Aeon Fuse Helper and the waveform Aeon Fuse Waveform Visualizer (their ids stay). Skin settings, the Home
  menu shortcuts and the chosen skin and screensaver move to the new ids.
- The menu theme Fused is now called Fuse (the choice is kept).
### Helper (script.aeon.helper 0.3.44)
- Works with the skin id skin.aeon.fuse.

## 0.26.0
### Home
- Movies, TV shows and Music: Down from the menu reaches the row under it on the first press. Those rows stay
  loaded, and while a row is still filling, Down waits for it instead of being lost.
- Movie sets show stacked posters as their menu icon (the preset, and a custom item that opens the sets).
- Choose icon (Skin settings > Home menu): a grid of the skin's icons and the 1,800 icons of Arctic Fuse 3 for every
  menu item; Default gives the item its own icon back. The icon stays with the item when it is moved.
### Music
- Now playing with the player controls: the lyrics (lines, or words on the cover) shrink with the page, so their dark
  panel stays on the cover and the lyrics stay above the controls.
- The quality line (codec, bit depth, sample rate, bit rate, channels) sits under the hairline, no longer on it, with
  the card's full width, and stays while the controls show; when a song has no tags for them, what the player decodes
  is shown.
- Waveform visualisation: on Linux / Android (CoreELEC) the wave sits in the empty band of the card between the
  RELEASED line and the hairline (it ran over the text and out of the card) and shrinks with the page under the player
  controls. Made for Aeon Fuse Waveform Visualizer (visualization.aeonwave 1.4.0, built from Kodi's Waveform 22.1.1 for Linux ARM64,
  ARM 32-bit, x86-64 and Windows x64): one even, thin line through the middle (Channels: Left, Right, Both mixed,
  Both overlaid, Both as two lines), Smoothness 0 (accurate) to 10 (calmest). Its band runs from the RELEASED line to the hairline, so loud peaks have room (they
  stopped well above the hairline). On Windows the stock Waveform keeps its own box; the skin picks by the
  visualisation that is set.
- Music library menu (Artists / Albums / Songs / Genres): the labels sit centred under their icons and the focus
  underline (they were 13 px to the right).
### Player controls
- Every music and video control button has a label under it while it is focused: one bold word (PREVIOUS, PAUSE,
  NEXT ...) or what it is set to, the setting in bold (SHUFFLE: ON, REPEAT: ALL, LYRICS: WORDS, QUEUE: 3 / 15,
  SUBTITLES: ENG, AUDIO: ENG . DD+ ATMOS 5.1, VIDEO: 4K . HEVC . DOLBY VISION, CHAPTER: 3 / 12). Some buttons had
  labels, but the row cut them off.
- Music controls: a new Album button (after Queue) opens the album of the song that plays in the music library
  (library songs only; the controls and the lyrics close first).
- The labels have room on both sides (the button rows reach the screen edges): the first button's label is no longer
  cut off on the left, long ones (an album name) show in full.
- With lyrics on, one OK opens the player controls again (it took two: the lyrics add-on moves the focus to its lines
  after every line, which the skin had switched off, so nothing had focus and the first OK only gave it back).
### Screensaver
- Music: the spectrum has its own tile under the weather tile (under the clock when weather is off, in the corner
  when both are off), with the album cover to its left and the artist and title beside it.
### Helper (script.aeon.helper 0.3.43)
- Choose icon for Home menu items; Down to the Home rows waits for them to load; a Planner read that fails waits
  longer each time before the next try (6, 12, 24, 48 hours, then 4 days).

## 0.25.0
### Planner
- The list of upcoming episodes and films is kept safely: written to a new file that then replaces the old one (the
  previous good copy stays as a backup), so a restart or a crash never loses it; a read that comes back empty (TMDb
  Helper busy, no network) no longer wipes the kept list and is tried again after six hours.
- How often the list is read again: daily, weekly, every 2 weeks (default) or monthly, and Update now - both in the
  settings strip (Left from the first option at the top), with the date of the last update.
- Settings strip: Backdrop (fanart / off) and its strength. Right strip as in the library views: clock, the day's
  scroll bar (Right from the last option at the top) and the number of titles.
- The options at the top have their focus bar again.
### Libraries
- Lengths in the h.mm style everywhere (0.58 instead of 58 or 58 MIN): List view, Low list, Compact list, the
  information panes and the Episode list.
- Compact list: episodes get room for the length (rating and watched mark further right); seasons have even columns
  for year, episodes and watched; seasons show their landscape picture, else the show's, else the fanart (also Banner).
- Wall views: the media info sits on its own row under the ratings, so neither it nor the genre is cut off.
- Showcase: the focused poster is in the middle of the view.
- Backdrop strength (View settings / settings strip) now also works with the Glass look, the Colours backdrop and Flix.
- List view: the episode badge (1x01 in its ring) is a quarter bigger.
### Home
- Middle position: the dark band under the menu reaches the bottom of the screen.
- Spotlight (films, TV): the studio / network logo sits on the row of the Play and Information buttons, on the right.
- Live TV has its own background, in the style of Power and Search.
- The More... tile at the end of a row has the row's shape (16:9 after episodes, square after albums).
### Menus
- Focus bars are back on the buttons that lost them in 0.23.0 (Home lists, submenus, Planner, add-on browser).
- Fuse menu theme, third pass, closer to the setup wizard: every row is its own rounded card with a gap to the next
  (faint, solid when focused), no rule lines, faint rounded panels instead of grey boxes, the wizard's deep background
  with its glow in every menu window, a rounded art box in the add-on browser, the header's lead word in the accent
  colour. Kodi's own settings rows get the same cards.
- Changing the Menu theme reloads the skin (CoreELEC: offers a restart, which keeps every setting readable).
- Palette picker: each palette in its own colours (row, name, swatch, focus bar, with readable text), and Right
  reaches the scroll bar for quick paging; the same for every long select list.
### Helper (script.aeon.helper 0.3.42)
- Planner list kept and merged safely, update interval and Update now; palette colours for the picker; Menu theme
  switch.

## 0.24.0
### Playback
- Seek bar: no light band over it while it has focus; the bar just thickens and shows a round knob.
- Seeking adds up: Left / Right on the seek bar use Kodi's seek steps, so quick presses add up and Kodi seeks once
  after its "delay after seek" (Settings > Player > Videos).
### Setup wizard
- Picking a palette recolours the wizard itself (focus card, ink and accent) straight away.
- Home menu position Low: the preview shows the smaller posters under the menu.
### Menus
- Fuse menu theme, second pass: every panel and card of the menus and dialogs is a rounded card without frame
  lines (the square boxes and their outlines are gone, also the outline of the settings categories); rounded pills,
  switches, knobs and outlines; rounded dialog panels with a soft shadow, on a deep background.
### Libraries
- Episode code: one format everywhere (views, Home, info panes, OSD), chosen in Skin settings > Details > Episode
  code: 1x01 (default) or S01E01.
- Wall views (Poster wall, Landscape wall, Square wall, Showcase, Cards): the info pane's divider sits on the top edge
  of its dark backing; media info chips moved up to the title line, so ratings, date, length and genre have the full
  width (the genre chip is no longer cut off).
- Wall captions under the artwork all sit on the dark gradient band (seasons, shows and movies too, as episodes did),
  with a gap under the artwork so the focused tile's progress line no longer runs into its caption.
- Compact list: the ULTRA HD / FULL HD pill of the List view instead of the small 4K / 1080 chip; year, length, rating
  and watched mark on even columns (shows: year, seasons, episodes, rating, watched), more room between rating and
  watched mark; the focused title scrolls when it is too long; seasons show their number of episodes.
- Compact list and Banner: the poster and fanart start below the header line (they cut through it) and have a soft
  shadow.
- Episode list: named Episode list in the settings strip too (was Grid); the clearlogo, season and count fit the
  height of the corner boxes, so its line meets their bottom edge; shadow behind the episode thumb; aspect ratio chip;
  4K / FULL HD / HD / SD (4K showed as 4KP); the chips are a little narrower so a long audio codec still fits.
- Season list: named Season list (was Grid); the season list starts right of the settings strip, so the strip no
  longer covers it; the season poster and the clearlogo share a top edge; poster shadows.
- Combined: a season's second row shows its episodes in order, as landscape thumbs with their code and a gradient
  title band (two full rows);
  season and movie captions on the gradient band; "1 season" / "1 episode" instead of "1 seasons".
- Cards is no longer offered for episodes (it showed the same as Landscape wall).
### Helper (script.aeon.helper 0.3.41)
- Setup wizard: starts with the skin's own colours each time it opens.

## 0.23.0
### Setup wizard
- Opens with the credits: "Huge thanks and credit go out to the following" (djh_, jurialmunkey, jamal2362, KarmaMole,
  the Kodi development team).
- 18 steps, each with a preview: library backdrop first, then the palette (only after Neutral), skin theme, menu theme,
  Home menu items (switch each preset on or off), Home menu position, spotlight backdrop and transition, corner boxes,
  watched indicators, titles or logos, media info chips, extra fanart, spoilers, motion and (Linux) memory hand-back.
### Menus
- Skin settings > Appearance > Menu theme: the skin theme's own menus, or Fuse: the wizard's look in every menu -
  rounded, inset focus cards, a faint card under every row and category, no rule lines. Library views are unchanged.
  (Aeon and Glass menus belong to their skin theme: the Glass menus' white ink would sit on the Aeon focus bar.)
- Appearance: Skin theme (was Theme) is the first row, Menu theme under it, then Palette.
### Home menu
- 13 positions instead of 10: with all the presets you use, the three custom items still fit. Favourites is one of the
  presets (Skin settings > Home menu > a position > Type, or the wizard).
### Information page
- The top card's right corner meets the clock box (the page sits 60 px higher; every card ends at the same edge).
- Studio / network logo in a fixed place on the artwork, clear of the widest row of buttons.
### Libraries
- List view: episodes show their runtime; seasons their number of episodes (E) in that column.
- Low list: the watched eye sits left of a runtime column (episodes: runtime, seasons: episodes, shows: seasons and
  episodes), and stays readable on the rows without focus (it turned dark on dark while the list had focus).
- View settings (TV shows, seasons, episodes): Hide plot and thumb (the spoiler switch of Skin settings > Details).
### Playback
- Spinning disc art is cut to a circle: disc art saved on a square background spins as a disc, not a square.
### Screensaver
- Ten slides per round, one for each pager ring (the 11th and 12th slide showed no ring).
### Helper (script.aeon.helper 0.3.40)
- Home menu: 13 positions; the wizard switches presets on and off (shown where they are, or put in the first free
  position).
### README
- Credits for jurialmunkey, jamal2362, KarmaMole and the Kodi development team.

## 0.22.0
### Setup wizard
- A setup wizard with previews: theme, palette, library background, Home menu position, Home spotlight, watched
  indicators, motion and (Linux boxes) memory hand-back, one choice a page with a mock-up of the result. It opens on
  Home the first time (Skip or Back on its first page keeps the defaults) and any time from Skin settings > Motion,
  memory, reset > Setup wizard. The other choices change at once; theme and palette wait for Finish.
### Library
- Certificates of every country share five outlines by how strict they are: all ages square (G, U, 0, TV-G),
  parental guidance circle (PG, TV-PG, 6-10), teen hexagon (PG-13, 12A, 12-14, M, TV-14), restricted triangle (R, 15-17,
  MA15+, TV-MA, 18A) and adults only double ring (NC-17, 18, R18+). Each keeps its own text, smaller where it is
  longer (three sizes in the triangle); not rated shows "NR" without an outline. Every rating in the library maps.
- The List view's info chip shows the same code ("RATED 16" for UK:16).
- List and the other library views: the extra fanart takes turns in the background (Skin settings > Backgrounds >
  Cycle extra fanart), as on Home.
- Artist wall: the artist name sits on the dark fade of the episode titles.
### Information page
- Media info in the top card, under the end time: the library's chips (resolution, aspect, HDR / Dolby Vision
  profile, audio, channels). The small copies in the "Ending at" card are gone.
- Studio / network logo at the lower left of the artwork, level with the buttons.
- TV show: the network once, above the title (not again after the episode count).
- Cast: round portraits (the circle sits where the face is in a head shot), names centred under them; the films of a
  collection keep their posters.
### Look
- Skin settings > Appearance > Corner boxes (clock, item count and the strip boxes): Colors (default, the colour of
  the artwork), Neutral (the palette's box colour), Fanart (a window onto the fanart behind it) or Backdrop (as the
  library background).
- Home spotlight: the dark fade from the left is stronger again.
- Icons: Memory hand-back a RAM chip, its minimum a pie with the free slice, Home spotlight transition shows motion,
  Home vignette a vignette, Spinning disc art a disc.
- Memory hand-back rows only on Linux (CoreELEC, LibreELEC): Windows and Android do not need them.
### Screensaver
- Studio / network logo in the lower left corner, beside the poster.
### Helper (script.aeon.helper 0.3.39)
- Setup wizard: publishes the current theme and palette before it opens; Finish applies theme and palette together.
  On Linux it then restarts Kodi (a skin reload leaves skin settings misread until the next start); on Windows the new
  look shows at once and the wizard asks for a restart (Kodi's RestartApp only quits there).
- Refresh information (context menu): the progress is the action toast out of the clock box, with the episode being
  refreshed ("Episode 3 of 24: S01E03 ..."), then "Information refreshed". It follows Kodi's own refresh job.
- Dolby Vision P7 FEL / MEL chip: when the film's .nfo has no `<hdrdetail>`, the media manager's
  `<name>.cmm_mediainfo.xml` (dovi_profile / dovi_el_type) is read.
- Studio / network logos: Kodi joins all of a title's studios ("Carnival Films / BBC Film / ..."), and no logo file
  has that name, so films with more than one studio showed none. The helper publishes the first studio for the
  information page and the screensaver.
- plugin.py ?info=trim logs what a hand-back freed.
- Memory hand-back during a 4K Dolby Vision remux (TrueHD Atmos) on the box: 26 hand-backs in a minute kept picture
  and sound in step (drift 0.14 s against 0.08 s without), no dropped frames or underruns; each took 29-106 ms.
### README
- New: what the add-ons do, the first start, credits (djh_, creator of the Aeon 2 concept) and the licence.
- LICENSE.txt names Aeon Fuse at the top (it began with Daylight's name only). It keeps Daylight's copyright notice
  and source as the work Glass is based on, and lists all eight font licence files (only two were named).

## 0.21.0
### Palettes
- 43 new palettes taken from the SABnzbd Glitter colour schemes (Abyss, Dracula, Frappe, Macchiato, Mocha, Nord,
  OneDark, Rose-Pine, Space-Gray, TrueBlack and more; the "Blackberry" / "Catppuccin" prefixes dropped, light schemes
  left out), and the 8 own palettes reworked: 51 in all. The highlight of each is kept light enough for dark text;
  the text on it is a dark tint of the palette's own colour.
- A palette now colours the highlight bar and its text, the scrollbar, the A-Z strip, the settings strip, the clock
  and item-count boxes, the certificate and length columns of the List views and the info bars.
- Palette is also in View settings (every library view). Choosing one explains that the library background takes it
  only with the Neutral backdrop and offers to switch (the view's own backdrop when chosen from View settings)
  (script.aeon.helper 0.3.33).
- A palette chosen in View settings now shows at once. Kodi shows new colours only by loading the skin again, and
  skipped that while View settings (a dialog) was open: the palette was saved but appeared only later. The helper
  closes View settings first (script.aeon.helper 0.3.37).
### Settings
- Skin settings: no "More options" sub-menu; every option sits in the list of its category. All option rows are the
  same height with an icon; every on/off option is a switch (the last On | Off pills too) at the same place on the
  right. Right switches on, Left switches off, Left again goes back to the categories.
- Switches, select-dialog ticks and their texts turn dark on the white highlight bar (they were white on white).
- Highlight bar missing (black text, no bar) in some settings pages, the Live TV menu, the add-on browser and the
  player's audio / subtitle settings: fixed (a 0.20.5 regression).
- Kodi and add-on settings: Up on the level button (Basic / Standard / Advanced / Expert) goes to the last category,
  Down to the first.
- Player audio / subtitle settings: narrower sliders so the values fit.
- Skin settings > Context menu (new category): the items Aeon Fuse adds to Kodi's context menu, each with Switch
  on / off, Move up and Move down: Refresh information, Update library, Clean library (off by default) and Take
  screenshot (on by default, last). Kodi lists them after its own items. Refresh works on films, shows, episodes
  and music videos (a show asks whether its episodes are refreshed too); Clean asks first (script.aeon.helper 0.3.37).
- Skin settings > Motion, memory, reset (was "Fonts, motion, reset") > Memory hand-back (Linux boxes such as
  CoreELEC): "When free RAM is low" (default; Minimum free RAM 512 MB - 2 GB, default 1 GB) or "After a pause" (2-30 s
  without a key press). See Helper below. Reduce motion is a switch. The three context-menu rows that were here sat
  331 px too low, over the next page's rows (they were inside the Fonts row); they moved to the Context menu category.
- Skin settings: Fonts moved to the Look category (last row), with a help line.
- Context menu: Clean library was missing when switched on (Kodi kept only one copy of each item; see Helper).
- Menus and dialog lists (select dialogs, Home menu lists, profiles, bookmarks, event log, PVR lists): the highlight
  fades out of the old row and into the new one, as in Skin settings; not while the list scrolls under the highlight.
  Kodi's settings pages, add-on settings and the context menu are made of Kodi buttons, which cannot fade their
  highlight on its own.
### Notifications
- Toasts and background progress (library updates, add-on updates) come out of the clock box at the top right. Aeon:
  a bar in the highlight colour with dark text and a turning spinner, the progress as a line along its bottom; on Home
  it matches Home's clock box. Glass: a dark fade rising from the left with white, right-aligned text. A progress bar
  moves down while a toast shows.
### Library
- Films with versions: the version (Director's Cut, Extended Edition ...) follows the title in the lists, walls,
  panes, spotlights, widgets and the information page when Settings > Media > Videos > Flatten movie versions is on,
  and for a film whose only version is not the Standard Edition.
- Dolby Vision profile 7: a "P7 FEL" / "P7 MEL" chip after the Dolby Vision chip, read from the film's .nfo
  (`<hdrdetail>7FEL</hdrdetail>`) (script.aeon.helper 0.3.33).
- List views: the arrow end of the highlight bar meets the bar's corners; the certificate outline is no longer cut.
- Progress line on posters: shows and seasons show the share of watched episodes (a part-watched episode made them
  show that episode's resume point instead). The line is also on the panes, the Low list and the Combined view.
- Combined view: the title line carries year, genres, certificate, seasons, episodes and the IMDb / TMDb ratings.
  Down, then Right past the last tile, reaches the A-Z strip.
- Episode wall: the S01E01 tag sits on a dark fade; the caption under the thumbnail is the episode title only.
- Wall info band: the length chip comes before the genres, and a long genre list is shortened instead of cutting the
  length off.
- Home: upcoming films have a much lighter dim.
- Home spotlight: its background option sat under "Widget screens" without saying it was the spotlight's, so Color
  got chosen for it by accident. With Color the skin showed the title's poster stretched over the whole screen, because
  KarmaMole was never told which list the spotlight is and never made its colour picture. Now: the category is
  "Spotlight & widgets" with the rows named "Home spotlight: background / transition" and "Widget screens: media info /
  ratings / studio" (with help texts); the helper points KarmaMole at the spotlight on screen (script.aeon.helper
  0.3.34), so Color gives KarmaMole's colour backgrounds; until that picture is there the fanart shows, scaled, never a
  stretched poster (the screensaver too).
- Widget screens (the full-screen pages, Up on a title on Home) have their own background choice: Spotlight & widgets >
  Widget screens: background, Neutral | Fanart | Color (default Fanart). Color shows KarmaMole's soft colour picture
  of the title on the page (script.aeon.helper names the page list for it); the fanart shows until it is there.
- Spotlight & widgets > Widget screens: slow zoom (on by default): the backdrop of the widget screens zooms in with
  every title; it was always on, stopped only by Reduce motion (which still stops it).
- Home: no zoom and slide any more. The spotlight's never ran (it was a Focus animation of the spotlight list, which
  never has the focus on Home); the fanart of the menu items without a spotlight drifted, now it stands still too.
- Widget screen options (on / off, autoscroll, items per list, seconds per item, and now the background too) moved
  from Edit spotlight to Edit widgets: a "Widget screen options" button at the top right.
- Home: no rule along the bottom of the menu band (on CoreELEC's 1080 menus scaled to a 4K set it was a hard line
  across the screen; in a PC window of another size Kodi smeared it away).
- List view and episode rows: the watched / unwatched eye turns dark on the highlight bar (it was white on white).
- List view: the length column is 100 wide like the certificate column, and its divider lies on the column's edge
  (the hours ran into the divider, which sat 8 px inside the tinted column). The resolution badge and the eye moved
  left to make room. Five-character ratings (TV-MA, TV-14, PG-13, NC-17 ...) use a smaller caption so they fit their
  circle or hexagon (TV-MA touched the ring).
- Music views: the heading drops the first word of the view name when the sort repeats it: "Wall: Artist", not
  "Artist wall: Artist" (also Album wall, the showcases, Artist rows, Album / Song list). The view picker keeps the
  full names.
- Episode wall: the title under the thumbnail sits on the same dark fade as the S01E01 tag, mirrored (dark at the
  left, fading out to the right).
- Screensaver: the pager dots are round (they were 8 px squares; on a PC window Kodi's scaling had blurred them
  round). Posters use the full height of the screen (they stopped 10 px short at top and bottom). Album covers stay
  square, with a soft shadow on the Fanart and Color backgrounds and a faint edge. The fanart background zooms and
  slides, starting again with every title (screensaver settings: "Zoom and slide the backgrounds", on by default; not
  with Reduce motion) (screensaver.aeon.fuse 1.0.2).
- Text boxes (plots, biographies, album descriptions, the information pages, the Home spotlight plot, the
  screensaver) show whole lines only. Kodi also draws a line whose top still fits, so the box showed the top half of
  the next line: the artist biography of the Artist wall ended in half a line at the bottom of the screen. The plot in
  the wall info band now has three whole lines (it was two and three quarters).
- Home: the Power and Search backgrounds are redrawn sharp, same picture and colours (the old ones had stair-stepped
  edges, soft glow and blotchy grain). 1920x1080 JPG: CoreELEC draws the menus at 1920x1080 even on a 4K set.
- Settings page and System menu: CoreELEC (or LibreELEC) opens the box's own settings, when that add-on is there.
- System menu: Live TV, Pictures, Favourites and the extra "Power" entry removed; Log off and Restart Kodi added, and
  Reboot to Android on CoreELEC. Each power entry says what it does underneath (they all said "Power"); Reboot has
  the two-arrow icon and the restart icon is redrawn (its arrowhead sat apart from the circle).
### Player
- Music player controls: the whole now-playing picture (card, cover, lyrics, disc) steps back together so it ends
  above the controls; the card's own times and codec line fade out meanwhile.
- Shuffle, repeat and lyrics show a line under the icon while on. The queue button opens the playlist (Kodi refused
  it while the controls were open). Lyrics steps Off -> Lines -> Words.
### Skippy (service.skippy, Skin settings > Behaviour; the rows show only when Skippy is enabled)
- Skippy: the skin's skip button (off by default). On: during a segment Skippy asks about, the player shows a
  "Skip Intro" button in the skin's look with the time left and the segment's progress; OK skips, Back hides it for
  that segment, Left / Right step through the video, Up / Down open the player controls. Skippy then opens no dialog
  of its own for those segments. Off: Skippy's own dialog, as before.
- Skippy: segment line in the player (on by default): between the times on the player controls, the segment playing
  and the time left ("Intro · 0:42 left"), or the next one ("Next Credits at 55:19"). Inside a "Main" segment (the
  sidecar's mark for the episode itself) it shows the next one.
- Skippy: up next in the player (on by default): top right of the player controls, the next episode Skippy found,
  with its picture when there is one. Skippy's own next-episode prompt is not affected.
### Helper (script.aeon.helper 0.3.38)
- Memory hand-back around videos: once as a video starts (what browsing left behind goes back before the buffers
  fill) and once when it stops. While it plays only a lasting shortage counts: free memory under the minimum for 10 s
  (a seek or a filling buffer dips for a moment), or under 384 MB at once. "After a pause" does nothing during a video.
- Font sets: a 12-point caption face (cap_12), from which the helper makes the section fonts.
- Memory on CoreELEC / Linux: Kodi kept the memory it had freed (2.4 GB on an idle Home screen of a 4 GB box, until
  it ran out while paging the libraries). The helper hands it back to the system (malloc_trim), as chosen in Skin
  settings: when free memory falls to the minimum (within 256 MB above it at the next pause in key presses, below it
  at once) or after the keys have rested for the chosen seconds. Below 384 MB free it always does it at once. A
  hand-back takes 40-260 ms. On the box: 1.9-2.4 GB down to about 1.2 GB each time; paging 2,100 shows, 6,100 films
  and 2,700 artists stayed under 2.1 GB.
- Context menu items (see Settings above): addon.xml has every item at every place; Kodi keeps only one item per
  script and arguments, so each place has its own arguments.
- Home spotlight with the Colors background: names the spotlight list on screen for KarmaMole (Groove.Helper.Container).
- Widget screens with the Color background: names the page list in focus for KarmaMole instead.
- When its files or the skin's were copied over by hand, the helper has Kodi read the new addon.xml at start-up
  (UpdateLocalAddons), so a new version and new context items are known without a restart.
- The Planner's TMDb Helper list ("Updating ListLibraryAiringNextProperties") is rebuilt at most once a fortnight,
  only after 10 idle minutes and never during playback; it pauses between pages and stops when playback starts.
- Backdrop = Colors: an episode gives the page the colour of its own thumbnail (all episodes of a show took the
  colour of the show's poster).
- The artwork colours (Colors backdrop and the palette-coloured boxes, with the KarmaMole helper) are worked out inside
  the helper's service. They used to start KarmaMole as a new script for every item the selection rested on, and Kodi
  does not give all the memory of such a script back. No colours are worked out under the screensaver any more (its
  slides counted as the selected item of the library underneath).

## 0.20.12
- Movies / TV shows / Music spotlight: the row of dots is a stop of its own. Right from "More information" moves the
  highlight to the dots (frosted disc and glow on the current one); there Left / Right change the title, Up returns to
  the buttons, Down goes to the menu. The automatic change waits meanwhile.
- The spotlight pages (Up from a spotlight) show the same disc and glow on their ring.

## 0.20.11
- Home spotlight of a movie set: the films and the row of dots are separate stops. Right past the last film moves the
  highlight to the dots; there Left / Right change the title only, Up returns to the films, Down goes to the menu.
  (0.20.10 turned the spotlight from inside the film strip, which moved both at once.)
- The dot that has the highlight sits on a frosted disc with a slow glow (custom items and Planner). The automatic
  change waits while the dots have the highlight.

## 0.20.10
- Home spotlight of a movie set: Right past the last film of the strip shows the next title of the spotlight, Left
  before the first film the previous one; the highlight stays in the strip, on the first film of the new set.

## 0.20.9
- Information page of a Planner title (not in the library): no Play or Resume button; the box on the right says
  "Coming up" with the date, the length and the network instead of "Ending at".
- Planner titles carry more from TMDb Helper: genre, certificate, studio, rating, cast and network; an episode without
  a description shows the plot of its show (script.aeon.helper 0.3.32).

## 0.20.8
- Home > Planner: Up enters the spotlight, Left / Right step through its titles (the ring in the row of dots
  follows), Down or Back return to the menu. The automatic change waits while the spotlight has the highlight.
  Up used to open the System menu here.

## 0.20.7
- Home spotlight of a movie set: with the highlight on one of its films, the spotlight shows that film's ratings,
  certificate, length, media info and plot instead of the set's plot (script.aeon.helper 0.3.31 supplies the ratings).

## 0.20.6
- Glass look: the highlight and the open ("parent") item are frosted glass with light text, in the skin settings, Kodi
  settings, add-on settings, System information, File manager and the dialog lists. Aeon keeps the white bar and the
  grey parent bar.
- Skin settings > Appearance: no Palette row in the Glass look (palettes colour the Aeon look).
- Palettes: the info bars under the library lists and the side strip take the palette's tone too (they were fixed
  near-black). The chosen palette comes back when the theme returns to Aeon (script.aeon.helper 0.3.30); Kodi drops it
  on a theme change.

## 0.20.5
- Changing the theme (Aeon / Glass) reloads the skin (script.aeon.helper 0.3.29). Parts of the skin pick their variant
  while it loads, so after a switch they kept the other look: in Glass that gave a solid white bar under white text
  on the buttons of the Home menu page.
- Glass look: the category cells of the skin settings have no grey fill.
- Home menu > Choose type > Movie sets now gives the item with a spotlight (a custom item set to the sets list); the
  plain preset has none.

## 0.20.4
- Glass look: the clock is the same tile in the top right corner on the settings pages, add-on settings, System
  information, File manager, add-on browser, Planner and the information pages (it was plain text on the
  information pages and missing on the others).
- The open category in Kodi settings and add-on settings has dark text on its grey bar in both looks, like the other
  parent bars.
- File manager: the lists end on a whole row.

## 0.20.3
- Glass look: one focus style for rows. The library lists (List, Low list, seasons, episodes, index lists), the music
  list and the Planner now use the translucent accent bar with light text that the settings pages use, instead of
  the opaque white bar with dark text. The Aeon look is unchanged (same variables, other values).
- Low list: the plot box ends on a whole line.

## 0.20.2
- Skin settings: every row is 70 high and lies on the grid of the category cells (they were 100 high on a 116 grid);
  all rows of a category fit the page, so the pages no longer scroll. The Home menu page uses the same grid; its
  selected position keeps a grey bar while the highlight is on the buttons, and "Off" is readable on the bars.
- Skin settings: own icons instead of the film placeholder (fanart backdrop, theme, library background, strips, box
  colours, lyrics, resolution and codec, studio logo, poster, spotlight, screensaver, media info).
- Palette preview: dark text and knob on the white sample bar.
- Home > Live TV: the panel lists the channels watched last; Up enters it, OK plays a channel, Right shows the channel
  group chosen under Edit spotlight, Left returns. (0.20.0 announced this but the panel had not been changed.)
- Kodi settings and add-on settings: the open category keeps a grey bar.

## 0.20.1
- Low list: behind seasons and episodes the show's fanart (a season's own "fanart" is landscape art with the title on
  it). With clean fanart the clearlogo is shown, without a clearlogo the title; when only the season landscape is
  left, the title. The logo starts on the line of the first row and has one height (140). Rows are 108 high, so the
  bar ends exactly at the item count box. Poster (197 x 296) or episode thumbnail in the free space above the logo.
- Skin settings: the "Custom rows" category is gone (nothing was set in it; lists under a menu item are made in
  Home lists, own menu items on the Home menu page). The white bar of a category lies exactly on its cell.
- Add-on settings: the same page as Kodi's settings (same frame, 76 px cells, level button as the last cell,
  description under the frame); OK / Cancel / Defaults are cells of the same height on the right.
- Low list: clearlogos lose their transparent border (script.aeon.helper 0.3.28 makes a trimmed copy), so every
  logo really starts on the line of the first row.
- List view: with the highlight in the set pane or the versions pane, the bar under the list shows the ratings
  and media info of that film.
- Information page: the "When to watch" box is "Ending at": the end time and the length, without the remarks.
- The open category keeps a grey bar with dark text while the highlight is in the list: Kodi settings, add-on
  settings, System information, and lists that share the dialog list layout (File manager and others).

## 0.20.0
- Home menu settings: Move up / Move down keep the highlight on the button. Enable / Disable only shows or hides an item:
  it keeps its name, type and every setting. New button "Choose type": a preset that is not on the menu yet, a custom
  item, or an empty position. script.aeon.helper 0.3.27.
- Power row: Reboot; on CoreELEC also Reboot to Android. Six entries fit the row.
- Live TV on Home: Up or Down from the item reaches a row of the channels watched last, Down once more the channels of a
  group; OK plays a channel. The channel, what is on now and next are shown above. Group and number of channels:
  Settings > Home menu > Edit spotlight with Live TV selected.
- Palettes also tint the library views. The settings-level button and the System boxes on Home are neutral instead of brown.
- Settings pages: group headings are as tall as the rows and the category cells; in the skin settings the Categories
  header is as tall as the title band and uses the same font, and the open category keeps a grey bar.

## 0.19.2
- Planner spotlight: pager dots with a ring on the current title. Its settings are one dialog, opened from Settings > Home
  menu > Edit spotlight (with the Planner selected) and from the Planner window: on / off, what it shows, days ahead,
  number of titles (10 by default, at most 25), seconds per title (8 by default).

## 0.19.1
- Planner spotlight on Home: with the Planner item focused, what is coming in the next days is shown one title at a time
  (fanart, logo, the day, episode or film, plot) and moves on by itself every 8 seconds. Two options in the Planner
  window: Home spotlight (7 days by default; 14, 1, 3 or off) and Spotlight shows (episodes and films, episodes, films).
  script.aeon.helper 0.3.25.

## 0.19.0
- Planner is its own window with its own two views (script.aeon.helper 0.3.24). Day: one day at a time under a strip of
  the week, Left / Right change the day. Week: seven columns, Left / Right walk the days and bring the next week in
  after the last one. Never a day before today. Upcoming films are listed with the episodes. Options above the lists:
  view, first day of the week (Monday by default), what is shown. The Planner is no longer tied to the library views.
- Themes: Aeon and Glass are in Kodi's own list (Settings > Interface > Skin > Theme); the Theme row of the skin
  settings switches the same setting.
- List view: the backdrop follows the Backdrop setting (fanart / colours) like the other views; an episode shows the
  poster of its season.
- Home: the contents of a focused set or show are a strip of small posters under the plot (no box); the heading of a
  strip is brighter.

## 0.18.0
- Trailers: the trailer file next to a film, show, season or episode is used first ("`<name>-trailer`", "tvshow-trailer",
  "season01-trailer", "trailer"); the address the library holds (usually YouTube) is only the fallback. Applies to the
  Trailer button of the information page - which now also appears for shows and seasons - and to trailer auto-play in
  the Flix view. script.aeon.helper 0.3.23.
- Planner is a Home menu item (added once to the first free position): the upcoming episodes of your shows, grouped by
  day - Today, Tomorrow, then the weekday with its date. It is no longer offered as a library view.
- The shortcut defaults of the skin are the current Home menu: "Restore shortcuts" returns to it.
- Studios, years, countries, tags and directors use the same layout as Genres instead of the old fallback page.
- List view: the focused title is dark on the white bar.

## 0.17.0
- Online lists know your library (script.aeon.helper 0.3.22): Recommended and Similar on the information page and the
  online Home sources (Trending, Popular, In cinemas, Upcoming, Top rated ...) are matched against the library. A title
  you have is your own library item with a tick - OK plays or opens it as anywhere else. A title you do not have is
  dimmed and OK does nothing; nothing is handed to TMDb Helper to play any more.
- Planner shows what is coming: "Upcoming episodes of my shows (Planner)" in the source picker (Online: TV shows) lists the
  next episodes of the shows in your library by date and opens in the Planner view. Read from TMDb Helper in the
  background twice a day.
- Stacked row on Home: a dark backing behind heading, posters and names.
- Flix view: "Play trailers automatically" in View settings (off by default). Four seconds after the selection rests, the
  trailer of the focused title plays behind the page; moving on stops it.
- Artist page: "Top tracks" and "Similar artists" buttons jump to those rows; Up from a row returns to the buttons.
- Home: aspect ratio chip beside the audio chips. Cinema mode draws trailers from more lists.
- Player: the disc art is a little narrower than the poster it rises from.

## 0.16.4
- Progress line on posters (Skin settings > Behaviour > More options, off by default; script.aeon.helper 0.3.21): a thin
  line along the bottom of a poster - how far you got in a film or episode, or the share of watched episodes of a show
  or season. In the wall, Showcase and Cards views and in the Home strips.

## 0.16.3
- Artist information page: Top tracks and Similar artists now come from Deezer's public API (no account or key; only the
  artist's name is sent, answers are kept for 30 days). Tracks and artists you have are ticked - OK plays the track or
  opens the artist; the others are shown dimmed. Without Deezer (switched off in Skin settings > Behaviour > More options,
  unreachable, or artist unknown) the rows fall back to the library: most played songs, and artists sharing the rarer
  genres. script.aeon.helper 0.3.20.

## 0.16.2
- Artist information page: two rows under the discography. Top tracks - the artist's songs, most played first; OK plays
  one. Similar artists in your library - artists that share the rarer genres of this artist's songs; OK opens that
  artist. Both come from the library, nothing is looked up online (script.aeon.helper 0.3.19).

## 0.16.1
- Information page: a Reviews row under Similar titles (TMDb reviews through TMDb Helper). OK opens the whole review
  (script.aeon.helper 0.3.18).

## 0.16.0
- Cinema mode (Skin settings > Behaviour > More options, off by default; script.aeon.helper 0.3.17): 1, 2 or 3 trailers of
  films that are in cinemas now or coming up play before a library film that is started from the beginning. Needs TMDb
  Helper (the lists) and the YouTube add-on (the trailers). Next skips a trailer, Stop ends the session. Not for
  resumed films, episodes or playlists.
- Player: Down from the buttons opens the chapter strip when the video has chapters; it lands on the thumbnails, Up
  reaches the bookmark buttons, Down or Back closes it.

## 0.15.1
- Kiosk mode (Skin settings > Behaviour > More options, off by default; script.aeon.helper 0.3.16): the library options strip
  (view, sorting, view settings, library actions) no longer opens from the views or the context menu. Settings stay
  reachable through the System menu, which is also where it is switched off again.
- Login screen in the Aeon look: page header, clock box, a centred row of profile pictures and the Power button.
  Kodi shows it only when there are extra profiles and "Show login screen on startup" is on.

## 0.15.0
- Stacked row on Home: while a set or a TV show is focused in a strip, a small second row beside the plot shows what is
  inside it (the films of the set, the seasons of the show). Display only. Off with Skin settings > Behaviour >
  More options > "Stacked row on Home" (script.aeon.helper 0.3.15).
- Home strips show the plain title of unreleased films from online lists (no red italics).
- The System menu no longer reopens by itself when Home is reached from an unrelated window.

## 0.14.3
- Home sources: the source picker (Home menu settings > submenu items and lists, Custom rows, widget pages) starts with two new groups,
  "Online: movies" (Trending, Popular, In cinemas now, Upcoming, Top rated) and "Online: TV shows" (Trending, Popular, On the air this week,
  Airing today, Top rated), plus "Everything in TMDb Helper" for Trakt lists, calendars and discover. Shown only while TMDb Helper is enabled.
- Select dialogs: the skin's outline icons turn dark on the white focus bar.

## 0.14.2
- Skin settings > Behaviour > More options (script.aeon.helper 0.3.14), a list with three new options:
  Hide spoilers of unwatched episodes (off by default) - no plot, and the show's fanart instead of the episode's still, in the library views, on Home and on the information page.
  Seek bar while paused - Always (as before), 5 seconds, or Never.
  Language flags in the player - flags of the audio and subtitle language on the player's info overlay (needs the language flags image pack; without it the language code shows as text).

## 0.14.1
- Information page: in the Aeon theme it has square artwork, flat buttons and chips, the common header (INFORMATION MOVIE ...) and the clock box; the Glass theme keeps its rounded look. Two new rows under the cast, filled by TMDb Helper: Recommended and Similar titles (Down from the cast).
- Artwork tiles and primary buttons that were still rounded in the Aeon theme (older views, dialogs) are square there now.

## 0.14.0
- New video views (pick them in the view picker):
  Flix - fanart of the focused title with its details and one row of landscape tiles (movies, sets, shows, seasons, episodes).
  Combined - a row of shows, sets or seasons, and under it what the focused one holds; Down goes into it.
  Circles - actors and directors as round portraits.
  Planner - episodes as a dated list (choose Date as the sort order in the settings strip).
- List is now also available for seasons and episodes.

## 0.13.1
- Consistency: animation speeds reduced to five steps (100, 150, 200, 300, 500 ms); Reduce motion now also switches off every open, close, show, hide and focus animation that moves or zooms something; text uses five strengths of white and one dark ink; seven near-duplicate fonts merged into their neighbours.
- View settings (Ratings, Media info, Plot) now also act in List, the walls, Showcase and Cards.
- Glass theme: the clock shows on the skin settings page. The settings panels follow the palette.

## 0.13.0
- Palette replaces Accent color (Skin settings > Appearance > Palette): nine palettes - Aeon (default), Graphite, Midnight, Ember, Forest, Wine, Sand, Ocean, Black. A palette sets the highlight colour, the clock / strip boxes and the page tones together. They are Kodi colour themes, so Settings > Interface > Skin > Colours lists them too. script.aeon.helper 0.3.13.
- One header style on every page: a light lead word and the page name in bold (KODI SETTINGS, SETTINGS INTERFACE, ADD-ON ...). Add-on settings uses it too and shows the clock box.
- Busy indicator: a thin arc going round where the clock box is, instead of the "Working" toast.
- Menu icons: the gear, info, star, power, refresh and bin icons redrawn in the thin outline of the others.
- Durations of films and episodes: hours and minutes only; music keeps the seconds.
- All Daylight names removed from the skin (files, playlists, fonts, internal names). Settings column in neutral tones instead of blue. "1 season", "1 episode". Switches in skin settings are square in the Aeon theme. Remaining English labels moved to the language file.

## 0.12.14
- Skin settings: Home menu position moved to Appearance (last row); Screensaver background moved to Backgrounds, beside the screensaver's clock and weather switches.
- Home, Low position: the logo or title of the focused strip item shows while music plays too.
- Home, Low position: the dimming behind the info of a focused strip item covers the full height again (it had moved down with the text and left a lighter band at the top).

## 0.12.13
- Home, now playing in the slot position: one line along the bottom left - the spectrum icon where the library's settings strip has it, the cover, then artist over title. The strips under the menu start under the focused menu item, so the corner stays free.
- Home strips: the heading (Recent episodes ...) and the logo or title of the focused item sit right beside the strip instead of at the far left. The spectrum icon on Home has no box behind it.
- Settings strip (library): with music playing, Down from the last setting reaches the spectrum icon; cover and artist / title slide out of it and OK opens the now-playing screen.
- Low list: the info column starts right of the settings strip; show / season poster or episode thumbnail left of the studio logo; season and episode counts and the watched state above the plot; a season without a plot shows the show's. View settings has a switch for each (Poster / thumbnail, Season and episode counts, Watched status). script.aeon.helper 0.3.12.

## 0.12.12
- Screensaver: optional clock box (Skin settings > Backgrounds > Clock box on the screensaver); with the weather box on too, the weather sits under the clock, as on Home.
- Widget pages: the same clock box with the weather box under it as on Home (they had clock numbers only).
- Accent color row: on the white focus bar the selection ring is dark and the white swatches have an outline, so they no longer vanish.
- Settings level button (Basic ... Expert): plain glass in the Glass theme instead of the brown box colour.
- "Library view style" is now called "Theme" (Aeon / Glass): it switches the whole look, not only the library.

## 0.12.11
- Home menu position Low: the spotlight logo, title, plot and studio logo move down with the rest (the plot stayed behind and ran into the ratings row); the strips reach the right edge.
- Settings menu, Glass look: the categories under each entry are the ones Kodi really has (Player: Videos · Music · Discs · Pictures · Language · Subtitles ...).
- Going Home after a settings page no longer lands on Settings by mistake: the redirect only happens when Home is reached straight from that page.

## 0.12.10
- Home menu position: Skin settings > Widget screens > Home menu position - Middle (default, as before) or Low. Low moves the band and everything on or above it 110 px down, so more of the fanart shows; the strips under the menu, their caption and the now-playing slot shrink to two thirds so they still fit. The now-playing places (slot, corner, line above the menu, bottom bar) keep working in both positions.

## 0.12.9
- System menu: an outline icon of its own for every entry (17 new icons), a two-weight header (KODI SYSTEM), and the size of the libraries under Update library.
- Settings window, Glass look: the icon column menu of the System menu instead of the card list. The focused entry shows its name and the categories it holds (Player: Videos · Music · Discs ...); the other entries stay readable, dimmed.

## 0.12.8
- Back walks one level up in the settings: a settings page (System, Interface ...) -> the Settings window -> the System menu, also when the page was opened straight from Home. Skin settings, File manager, System info and Add-ons also return to the System menu when they were opened from it.
- Settings strip, Home (all four now-playing places) and the screensaver: the music spectrum icon is now one animated picture with all four bars standing on one base line (the bars were anchored at their tops and looked scattered); still while paused.
- Slider settings: the marker sits on the track (it hung below it) and is a flat block.
- Screensaver (screensaver.aeon.fuse 1.0.1): it no longer closes the moment it starts; the preview works.

## 0.12.7
- Screensaver: optional weather box in the top right corner (Skin settings > Backgrounds > Weather box on the screensaver; off by default).
- Skin settings: the frame starts under the clock box and ends at its left edge, so the corners touch. The space above the first row is now a title band with the name of the open category, which makes the first row as tall as the others.

## 0.12.6
- Fonts per section: the big headings of a screen now follow that screen's section. Choosing a font for Home changes the Home menu labels (MOVIES, TV SHOWS, SETS ...), which 0.12.1 claimed but did not do (it moved the spotlight titles only). A family chosen for Headings still wins for all headings everywhere. script.aeon.helper 0.3.11.

## 0.12.5
- Fonts per section: Montserrat, Manrope, IBM Plex Sans, Source Sans 3 and Source Serif 4 added, each with Regular, Medium, SemiBold and Bold. They are cut from the variable fonts of the Google Fonts repository (fonts/README-fonts.txt; licences `fonts/OFL-*.txt`). script.aeon.helper 0.3.10.

## 0.12.4
- Fonts per section: Barlow added (Regular, Medium, SemiBold, Bold; SIL Open Font License, fonts/OFL-Barlow.txt). script.aeon.helper 0.3.9.

## 0.12.3
- System panel on Home and the Settings facts: uptime as 8d 15h 2m, so Total uptime no longer runs into its label (script.aeon.helper 0.3.8).
- Fonts per section: the picker only offers families with a real bold face (Default / Figtree, Roboto CJKSC, Inter (Copacetic)); a one-weight family you already chose stays listed for that section.

## 0.12.2
- Fonts per section: the family list now has a preview. A mock-up screen (heading, list rows with a focused row, chips, body text) is drawn in the family under the cursor before you choose it (script-aeon-fonts.xml, script.aeon.helper 0.3.7).

## 0.12.1
- Fonts per section: the Home menu labels (MOVIES, TV SHOWS ...) now follow the Home choice instead of Headings.
- Fonts per section: eight more families that look clearly different (script.aeon.helper 0.3.6): Daylight Serif, Daylight Display, Source Sans 3, PT Sans, Hind, Noto Sans, DejaVu Sans, Noto Mono. Each is one file, so bold text is not heavier in them.

## 0.12.0
- Fonts per section: Skin settings > Fonts, motion, reset > Fonts. Home, Library, Headings, Settings pages and Player can each use their own family (any of the skin's font sets whose files are installed), or follow the font set chosen under Settings > Interface > Skin > Fonts. The skin reloads when the list is closed. Needs script.aeon.helper 0.3.5, which writes the section fonts into Font.xml.
- Every screen now uses section font names (hm_, lb_, hd_, st_, pl_); dialogs and shared parts keep the plain names and follow the font set.

## 0.11.8
- Skin settings: the category column has its outline again (drawn over the cells); dividers are 2 px so they stay even when Kodi runs in a window that is not exactly 1920 x 1080; the open category fills its whole cell.

## 0.11.7
- Home vignette: Skin settings > Backgrounds > Home vignette - Off, Light, Medium (default) or Strong (it was Strong).
- Widget pages: clearlogo as the title (text when there is none); ratings with their icons and the media info as chips under them, with the aspect ratio chip.
- Skin settings categories: solid cells with one rule on the top edge of each, so the spacing is even and nothing shows under the last cell.

## 0.11.6
- Duration, every list view and media type: hours (large, bold) . minutes (medium) . seconds (small); no hours part under one hour. Now playing and the music OSD use the same order.
- Aspect ratio chip (1.78:1, 2.39:1 ...) beside the resolution chip in the library bars.
- Artist rows: the number of albums on every row (script.aeon.helper 0.3.4 counts the albums per artist and publishes the number for each screen row).
- Fanart list: the list reaches down to the small picture; a disc of a multi-disc album shows its disc title or number.
- Now playing: bit depth and sample rate in the codec line.
- Lyrics, Words look: new setting Words lyrics size - Full screen or On the cover.

## 0.11.5
- Lyrics, Words look: now the animated lyrics of Estuary MOD V2 (its twenty layouts and colour variables ported as Includes_Aeon_LyricsMod.xml; its fonts are used in place from the installed skin.estuary.modv2 add-on, which therefore has to stay installed).
- View headings: view name, then what the view is sorted on in bold (LANDSCAPE WALL: ORIGINAL TITLE). Added to the Music views (top row, where the Menu hint was) and the List view (bottom bar).
- Music top row: the rule sits flush with the corner boxes; the icons sit on the boxes' centre line. The strip and View settings show the picker's view names (they were read inside the dialog, where the view cannot be seen).
- Fanart list: picture, small cover and facts box meet at their corners; on albums and songs the small box shows the artist. The library backdrop steps through the extra fanart in Music.
- Songs: format, sample rate, bit rate and channels in the song rows and the Fanart list (Kodi's library holds no bit depth).
- Artist rows: the album count on the focused row now shows.
- Spectrum bars grow from one base line again. Skin settings: category icons and names centred in their cells, the frame ends with the last cell. Previews for the Playback rows and the two new Look rows.

## 0.11.4
- Settings strip: nothing is squeezed any more. Every library view keeps a fixed margin on the left where the strip opens (or sits, when permanent): lists start at 90, walls keep their columns with slightly narrower tiles, the music Fanart list moves its icons and texts. The Movies / TV List view is unchanged (the strip lies over its poster).
- Home, System item: Movies / TV shows / Episodes have their "|" on one vertical line; Music is one row with the artist, album and song icons.

## 0.11.3
- Settings strip: the view makes room while the strip is open, so it no longer lies over thumbs and lists (the Movies / TV List view keeps its full-height poster under it). Tabs row in Music: Up, and Left from the first tab, open the strip (the way to it from the showcase).
- Music views: biography (album: review) and facts in the free space - under the list and picture of the Fanart list, under the cover column of the row lists, under the title of the walls and showcase. View settings > Biography switches it off per view. The Fanart list shows the artist picture in the big box.
- Artist rows: formed / born and disbanded / died on the second line, the number of albums on the focused row. The cover sits in the corner of the top row and the A-Z strip. The strip and View settings use the view picker's names (Artist rows, Fanart list ...). No showcase for songs.
- Now playing: the disc rises out of the top of the cover and stops on pause (it used to turn backwards); elapsed and total time in the bold . light style, also on the music OSD.
- Lyrics: new setting Skin settings > Playback > Lyrics take focus (default Off: OK opens the music OSD). On: the lines take focus, OK seeks to the line, and Back only lets go of the lines - the lyrics keep running.

## 0.11.2
- Home, System item: four panels above the menu (Version, System, Hardware with CPU / memory bars, Library with watched counts; needs script.aeon.helper 0.3.2).
- System menu: the stray "&lt;" is gone. Back from Settings and from Skin settings returns to the System menu.
- System info: the menu bar and dividers reach the card; the memory / CPU box sits beside the card, a shade lighter.
- Settings boxes meet with a one pixel divider instead of a gap (skin settings categories start at the frame's top edge and the focus fills the whole cell).
- List view: the certificate outline stays visible (dark) on the white bar; the year is bold.
- Compact list: resolution tag (4K / 1080 / 720 / SD) in every row; the title's logo fills the free half of the bottom bar; the set pane shows the info and ratings of the movie in focus (also in the Banner list).
- Backdrop = Colors now does something: the page takes the colour of the poster / cover on screen, with a soft wash of the artwork on top. The music List view follows the Backdrop setting like the other views. View settings: Backdrop strength per view.
- Music OSD: icons instead of text (the name / state shows under the focused one). Now playing: disc art turns behind the cover; the fanart drifts and zooms slowly and steps through the artist's extra fanart every 16 seconds.
- Lyrics (CU LRC Lyrics): OK opens the music OSD instead of jumping the song back. New look "Words" (Skin settings > Playback > Lyrics style): the current line as big coloured words.

## 0.11.1
- Box colours: the clock / count / strip boxes now take the colour of the POSTER on screen (the palette helper's own colour follows the fanart, which gave e.g. burgundy boxes beside a yellow poster). Needs script.aeon.helper 0.3.1.
- Settings strip: can be permanent (Skin settings > Look > Settings strip, and per view in View settings). The view is squeezed 80 px to make room. Left in the List view opens the strip too.
- Skin settings: slate category boxes flush against each other, grey box for the open category, row bar and dividers span the whole cell, rule before the preview column. The 7th row and the first row use real visibility (the first row no longer stays hidden, the 7th row label is readable). New rows: Settings strip, Box colors from artwork, Clock box / Weather box on the player controls.
- Add-on settings: category column shows 8 whole rows and sits flush on the Settings level button and against the settings list; scroll bar and chevrons when there are more categories. Section headers are larger and bold (also in Kodi settings).
- System menu: the same ground as the settings pages instead of a near-black dim.
- Add-on browser: line icons for the menu entries that have no artwork.
- Video OSD: poster beside the ring is on by default (setting inverted: aeon.osd.noposter), clock box and weather box top right, icons instead of text for Subtitles / Audio / Video / Chapters / Info / Stats (the name shows under the focused one).
- Up key: Up at the top wraps in every vertical view (List had none); in Music, Up at the first item goes to the tabs only (it used to also wrap). Scroll bars give the focus back to the list two seconds after the last key press.
- Removed the unused aeon_rule.png.

## 0.11.0
- Library settings strip: a left-hand icon column in the style of the A-Z strip (View, View settings, Sort, Order, Unwatched, Sets, Search, Update / Clean library, Library settings). The focused setting grows into a bar with its name and value; the bottom box shows spectrum bars while music plays. Opened with Left at the left edge of a view and with the Menu key (which used to focus a hidden control).
- View settings: now a strip panel beside the view, so changes show at once. Fixed: Plot and Backdrop were stuck on Default (the helper lost track of the view while the dialog was open). Also available in the music views (backdrop).
- Compact list: the watched mark sits in one column for every row and stays visible (dark) on the white bar; so does the versions icon.
- Duration: one style in the list views, bold part . light part (movies hours . minutes; tracks minutes . seconds; from one hour up hours . minutes).
- Album / song lists: the duration no longer runs under the cover. The playing track is readable when focused (Kodi's "selected" text colour was white).
- One white (colour name aeon_white) for every focus bar, frame and the strip focus box.
- Clock box on the settings and add-on pages. The clock, count and strip boxes take the colour of the focused artwork when the KarmaMole helper is installed (skin bool aeon.nopalette turns it off). The toast only draws a clock box where the window has one.
- Settings: Kodi settings and add-on settings share one row height, font, inset and boxed rows; the Settings level button uses the box colour. Skin settings: the 7th row no longer runs out of the frame (the list moves up when it is focused); preview panels for Theme songs, Screensaver background, Spotlight background, Poster beside the ring and Spinning disc art.
- Aeon look: square corners for buttons, chips, segmented controls and cards (the Glass look keeps the rounded ones).
- Home: Sets / custom items show the set's movies as a row of posters (oldest first, OK plays) instead of the Play / More information buttons, and get widget pages like Movies (defaults: Random sets, Movies with versions). Power: horizontal sub-menu row (Switch user, Log off, Update video library, Update music library, Shut down). New setting Spotlight transition: Fade (default), Slide or Cut.
- Screensaver: now the separate add-on screensaver.aeon.fuse, a regular Kodi screensaver (on / off and wait time in Settings > Interface > Screensaver) that cycles through random movies, TV shows and albums. The skin no longer starts one by itself after 3 minutes.
- Disc art: also the album's disc art when music plays.
- Renamed: skin settings `daylight.*` are now `aeon.*` (carried over once by script.aeon.helper 0.3.0), media/daylight is media/aeon. "Color" everywhere. 559 more labels moved to strings.po.

## 0.10.88
- Sets spotlight: the artwork lists were drawn on top of the dots, label and buttons; moved below them.

## 0.10.87
- Sets / custom Home items: spotlight now has the pager dots, the title label and the Play (opens the set) and More information buttons like Movies. Up from the menu title goes to the buttons; Up again goes to the submenu pills.

## 0.10.86
- Home submenu pills (Sets, custom items, Power): the pills never appeared because of a conditional fade on their container; they now show (and slide in) while one of them has focus. Up from the menu title focuses them instead of also opening the System menu.

## 0.10.84
- Custom Home items: their spotlights are now the same kind of list as Movies / TV (and use the same autoscroll timer), fed by the spotlight path from the editor.

## 0.10.83
- Custom Home items (Sets, custom 1-3) now work like the built-in ones: the spotlight path is picked in the Spotlight editor and stored per item (aeon.sp2.customN.path; the "library://video/movies/sets.xml" menu path is mapped to the movie sets list), and the item's submenu entries (the node saved by the submenu editor) show as pills under the spotlight, like Power does.

## 0.10.82
- Removed the Home spotlight trailers feature again (Kodi cannot show a trailer video in the Home window without flicker). The spotlight settings, video window and autoscroll hold are gone.

## 0.10.81
- Spotlight trailers: the Home spotlight autoscroll (movies / TV) waits while a trailer is starting or playing, whatever the hold setting, and carries on when it ends. The video window sits above the spotlight artwork; the system volume bar stays hidden while the trailer is muted. Helper 0.2.5 only ever runs one copy of itself (a restart of Kodi is needed once to clear old copies).

## 0.10.80
- Home spotlight trailers (off by default): Skin settings > Home spotlight > Trailers. After the spotlight item has been in focus for 2.5 s its trailer (the library trailer, e.g. via the YouTube add-on) plays on the right above the menu and fades into the artwork. Silent unless Trailer sound is on. Never interrupts anything already playing. Needs script.aeon.helper 0.2.4.

## 0.10.79
- Settings pages: text on the focused row / category is dark on the white bar (it was white on white); rows run from the vertical divider to the scrollbar so the dividers join the lines on both sides; Settings level button fills its whole cell, beige with dark text.

## 0.10.78
- Select dialogs (option lists, audio / subtitle / version pickers): the highlight bar now runs edge to edge of the dialog instead of being inset 24px on the left.

## 0.10.77
- Fonts: new font sets in Settings > Interface > Skin > Fonts: Roboto CJKSC (resource.font.robotocjksc), Inter (Copacetic) (resource.fonts.copacetic), and McFontface Inter / Open Sans / Lato (script.mcfontface). Install the font add-on first; the default Figtree set is unchanged. McFontface fonts have one weight, so bold text is not bolder there.

## 0.10.76
- Screensaver and Home spotlight "Colors" backdrop: uses the KarmaMole helper (script.karmamole.helper) to make a real colour wash from the artwork when it is installed; falls back to the stretched poster otherwise. Needs script.aeon.helper 0.2.3.

## 0.10.75
- Video OSD: option to show the poster left of the ENDS ring, and option for the disc art to slide out of the top of the poster and spin while playing (stops when paused). Both off by default, in Skin settings > Seek bar / OSD.

## 0.10.74
- Home spotlight: background style Neutral / Fanart (default) / Colours of the poster, in Skin settings > Home spotlight > Spotlight background.

## 0.10.73
- Screensaver: animated spectrum bars next to the now-playing line (top right, like Aeon 2) and a background style - Neutral, Fanart, or Colours of the poster (fades to the next one) - in Skin settings > Appearance > Screensaver background.

## 0.10.72
- Theme songs (off by default): Skin settings > Library details > Theme songs. A theme.mp3 / .flac / .ogg / .m4a / .wav / .wma in a movie or TV show folder plays while that item is selected in the library, loops, and stops when you move on, leave the library or start something else. Never interrupts anything already playing. Needs script.aeon.helper 0.2.2.

## 0.10.71
- Now playing (corner, line and bar placements): the same solid clock-box colour as the clock on Home and in the library views.

## 0.10.70
- Add-on browser: icon frame and list card line up at the top and share a single vertical line.
- Toast notifications (Aeon): a white bar like the highlight bar slides out of the clock box at the top right, dark text, icon on the left.

## 0.10.69
- View settings: "Reset to default (global settings)" is now the first row.
- Add-on browser and file lists: the card sits flush against the add-on icon (no gap) and the white highlight bar runs edge to edge of the card.

## 0.10.68
- Library view settings: Menu / library panel > "View settings" opens a list where ratings, media info, plot and backdrop style (neutral / fanart / colours) can be set for the view you are in, separately for every media type and every view. Default follows the global settings. Needs script.aeon.helper 0.2.1.

## 0.10.67
- Settings screens: coloured boxes in the Aeon palette - slate category boxes, gold level button, dark boxes behind each setting row, white focus bar unchanged.

## 0.10.66
- Settings rows and category buttons: the row hairline texture was 4px tall, so Kodi stretched it into a dark-to-light gradient (the 3D / mirror look). It is now 128px tall so the stretch stays fully transparent with a single crisp 1px line.

## 0.10.65
- Compact / List / Banner views: movies with several versions show a layers icon next to the title.

## 0.10.64
- Compact / Banner list: the versions and set-members poster pane is parked off-screen instead of faded out while it has no focus, so its items load and Right can enter it.

## 0.10.63
- Compact list and Banner list: Right on a movie with versions (or a set) now enters the poster pane; the default Right (to the A-Z column) ran after it and took the focus back.

## 0.10.62
- List view bottom bar: two rows (ratings / certification / length, then resolution / HDR / audio), full width, nothing cut off.

## 0.10.61
- Home TV spotlight and strip info: premiere / finale chip on episodes (Series premiere, Season premiere, Season finale, Series finale), worked out by script.aeon.helper 0.2.0 from the library.

## 0.10.60
- Home: the spotlight of custom items (Movie sets ...) no longer waits for its own list to have items before it is shown (the list only loads once visible).

## 0.10.58
- Library views bottom bar: two rows, both starting at the left - ratings / certification / length on the first, resolution / HDR / audio on the second - so nothing is cut off.

## 0.10.57
- Home: custom menu items are recognised by their key (label2 custom1..3) like the other items, so their spotlight and submenu show.

## 0.10.56
- Home: the slot number of custom menu items is stored under a new property name (cmslot) because Kodi returned an unrelated value for cm; the spotlight / submenu of custom items needs it.

## 0.10.55
- Home > System: the Aeon style uses the neutral backdrop with the last fanart at the Backdrop strength you chose (like the settings screens) instead of the dark gear picture; Glass keeps the picture.

## 0.10.54
- Home > Music > Artists opens album artists only (default); the skin setting aeon.allartists switches to all artists. (A settings toggle is still to come.)

## 0.10.53
- OSD and seek bar: "ENDS" and the time are centred in the ring (moved down 12 px).

## 0.10.52
- Home strips: the "More..." tile shows a large + inside a dark poster instead of a blank poster.

## 0.10.51
- Dialogs opened from settings (add-on info, select lists ...): the blue gear background is only used in the Glass style; the Aeon style dims the screen behind like every other dialog.

## 0.10.50
- Add-ons browser (Aeon style): the add-on icon sits right next to the list with a thin frame in the same grey as the line between them; name and status below it.

## 0.10.49
- Library views bottom bar: ratings / certification / length chips get the full width (they were cut at 700 px).

## 0.10.48
- List view: certification ring, its text and the set icon are centred in their 100 px column.

## 0.10.47
- Compact list with a side pane (Sets): rating and watched mark moved left so the arrow end of the highlight no longer clips them.

## 0.10.46
- Settings categories (e.g. Media): the current category label is dark on the white bar. Add-ons list and other generic lists: no fade at the bottom, the last row has full brightness in the Aeon style.

## 0.10.45
- Widget / submenu editors: a permanent "Add item" button above the list (it was only shown while the list was empty), so more entries can always be added.

## 0.10.44
- Submenu / widget editors: adding an item for Movie sets and custom items no longer fails (they keep their entries in their own menu file, aeonmenu2).

## 0.10.43
- Edit spotlight: Items and Seconds per item open a number pad (any value), Sort by opens a list; the Library background row is hidden for custom items (it belongs to the Movies / TV shows / Music library views).

## 0.10.42
- Edit spotlight for custom items (Movie sets ...): Spotlight on/off, Label, Items, Sort by, Reverse order and Seconds now work and drive the Home spotlight of that item.

## 0.10.41
- Widget and submenu editors: Add item opens the path picker and adds the entry to the list; the buttons on the right (rename, source, sort, move, delete ...) stay greyed out until a real entry is selected; the old "Choose target" button that overlapped Rename is gone (the path of a custom item is set on the Home menu page).

## 0.10.40
- Widget and submenu editors: the highlighted row (Add item and every other row) uses dark text on the white bar.

## 0.10.39
- Edit spotlight: the Path row opens the same picker as Set path / content (for Movies / TV shows / Music it stores the spotlight path, for custom items it sets the item path); Edit widgets and Edit submenu are available for Movie sets and custom items (Home submenu uses the same node).

## 0.10.38
- Settings > Home menu: Set path / content works (one button per custom item, no hidden helper). Edit widgets / Edit submenu / Edit spotlight are greyed out for items that have no editor (only Movies, TV shows and Music have widgets, plus Power for the submenu, and custom items have a spotlight).

## 0.10.37
- Home menu: new preset "Movie sets" (opens the movie sets, rename supported). Custom items show the name you give them in the position list. New button "Set path / content" for custom items: opens the add-on / playlist / library / favourite picker.

## 0.10.36
- Settings > Home menu: Right / Select on a position now lands on Enable / Disable (the first button).

## 0.10.35
- Settings > Home menu: Show / hide is now Enable / Disable and the first button. Enable on an empty position asks which item goes there (script.aeon.helper swap.py enable). While the selected item is disabled, Move, Rename and the three Edit buttons are greyed out and skipped.

## 0.10.34
- Ratings (all views): Kodi lists only carry the default rating, so the skin now also reads every rating of the focused item (IMDb, TMDb, Rotten Tomatoes, Trakt) from script.aeon.helper 0.2.0 (Home properties `aeon.r.*`) and shows them next to the default one - episode, season, TV show, movie and Home views.

## 0.10.33
- Ratings: every rating the item has (IMDb, TMDb, Rotten Tomatoes, Trakt, ...) is shown in all views (lists, Home, spotlight, episode / season panes); the per-source skin toggles no longer hide any of them.

## 0.10.32
- Home: TV show status chip (Continuing, Ended, ...) in the spotlight and in the TV strip info, after the rating chip.

## 0.10.31
- Low list: video info (resolution, HDR) and audio info (codec, channels) chips share one row; the plot moves up.

## 0.10.30
- Aeon list (TV shows): no empty certification outline when the certification is not one the skin knows; the watched mark moved right (TV shows) and the second line gets more room.
- Low list: left panel now shows date | genre, ratings, certification / length, media info and plot under the clearlogo (or title), with the studio logo below.

## 0.10.29
- Library views: the fanart brightness follows the Backdrop strength setting (Light / Medium / Strong; Medium is the default).

## 0.10.28
- Library views (Aeon style, fanart background): the fanart is much brighter (about 63% instead of 18%, with a lighter dark layer on top).

## 0.10.27
- Settings, add-on settings and dialogs: the check mark, empty check box, spin arrows and slider knob of the focused row are now dark on the white focus bar (they were white on white).

## 0.10.26
- Video OSD and seek bar (Aeon style): times and the progress line sit above the player controls (right of the ENDS ring) instead of along the bottom edge; title block moved up to make room; trickplay preview follows that line.

## 0.10.25
- Seek bar: the trickplay overlay now carries the service.trickplay marker (control 94090, overlay rev 10), so the add-on sees the skin as set up and no longer asks to install its own snippet over the skin's seek bar.

## 0.10.24
- Select dialogs (add-on versions, current audio / subtitle track, and other lists with a ticked item): the label of the ticked row was drawn white on the white focus bar (Kodi uses the selected colour for ticked items). Selected colour now follows the row ink; the check mark is dark on the bar too.

## 0.10.23
- Add-ons browser and other generic lists: the scrollbar marker turns white when it has focus (it was black on the dark card).

## 0.10.22
- Seek bar (Aeon style): same look as the Video OSD - ENDS ring, clearlogo / title, episode line, state, times and the thin progress line; the Glass style keeps its panel. Trickplay preview sits above the title block.

## 0.10.21
- Low list view: the right-hand column now has the character list (# A-Z) for quick navigation next to the scrollbar, like the other library views.

## 0.10.20
- Trickplay: seek preview thumbnail (service.trickplay) above the Video OSD progress line and the compact seek bar, following the playhead, with timestamp chip.
- Skippy: the seek bar and the Video OSD stay hidden while a Skippy skip is in progress (Home property Skippy.Skipping).
- Add-ons browser: highlighted tab pills now use dark text on the white bar; the list has a scrollbar (also in the other generic list windows).

## 0.10.19
- Video OSD: tinyPPI support. When the optional add-on script.tinyppi is installed and enabled, a PPI icon (from Arctic Fuse 3 CE MOD) opens its dialog and takes the place of the STATS button; without it nothing changes. script.tinyppi is an optional dependency.

## 0.10.18
- Home: focusing an album / artist / song in the music strip shows its info above the menu (artist clearlogo, album or artist name, artist and year, rating, genre, label, plot).

## 0.10.17
- Home: the strip under the menu only shows while one of its items has focus, so pressing Up on a menu item (spotlight) no longer shows the strip as well.
- Home: the strip info and its shade are drawn under the strips, so the highlighted cover is shown undimmed.
- Home: the strip of the new menu item no longer loads the previous item's entries while the submenu list is still refreshing (that was the music covers under TV shows); the caption beside the strip reads from the focused strip only.
- Home: a strip that does not belong to the highlighted menu item stays out of sight, so pressing Down right after moving to another item can no longer flash the previous item's strip (e.g. music covers under TV shows).
- Home: the dark scrim behind the strip info runs the full screen height like the spotlight, so it no longer ends in a hard edge across the menu titles.
- Home: the section fanart and the spotlight art get the same slow zoom and drift as the widgets; long spotlight titles get room (three lines) so they no longer run into the year / genre line.

## 0.10.16
- Home strip info: the line under the logo describes the focused item (S02E08 · title for an episode, seasons / episodes for a show, year / genre for a film) instead of the spotlight list name; the clearlogo beside the strip no longer overlaps the category heading and sits level with the thumbnails.

## 0.10.15
- Home: focusing a TV show / episode / movie in the strip shows its info above the menu (clearlogo or title, season / episode line, media chips, rating icons, plot, studio logo); the caption beside the strip uses the show or movie clearlogo, with the title text as fallback.

## 0.10.14
- Home: the strip under the menu (recently added etc.) and its label only show once you push Down; on the menu itself nothing is shown below it, so the previous item's strip can no longer flash when you move to another menu item.

## 0.10.13
- Aeon style: labels laid over a white highlight bar (Home menu actions, widget / submenu / spotlight editors) turn dark when their row is focused.

## 0.10.12
- Skin settings > Home menu: the action column fits inside the card (Restore default order no longer overflows), has a vertical separator from the list and hairlines between the actions; the separator runs to the bottom of the card, drawn like the left one, with a line under the last action too.

## 0.10.11
- Skin settings: the option pills and labels stay visible on the white highlight bar (dark pill and text) instead of disappearing; the row icon turns dark on the bar.

## 0.10.10
- Low list now works for TV shows (year chip, title, seasons / episodes / genre, watched eye; show clearlogo and studio on the left).
- Up from the first item goes to the last and Down from the last goes to the first in the List, season and episode views.

## 0.10.9
- New view: Low list for seasons and episodes (show clearlogo and studio on the left, a low list on the right: year / S|E chip, title, episodes or writer / director, watched eye). Pick it in View.
- Watched status eye on the right of the List and Compact list rows and the episode rows (crossed eye = unwatched, eye = watched).
- TV shows: number of seasons (S) and episodes (E) in the List and Compact list.

## 0.10.8
- Library root list (Genres, Titles, Years ...): square white highlight bar edge to edge, wide list (Aeon style).
- Seasons: the show clearlogo (or title text) sits above the season name; the studio logo no longer overlaps; the season info stays in a column while the episodes are open.
- Episodes view: the show clearlogo (or title text) heads the episode list.
- Seasons and episodes views follow the library background setting (fanart / neutral / colour).

## 0.10.7
- Seasons: Aeon layout (flat list left; season poster, plot, year / episodes / unwatched / certificate chips, ratings, first aired, studio, genre and cast right). Right slides in the episodes with the episode pane. Clearlogo above the studio logo, landscape art when there is no clearlogo.
- Certification labels: smaller font and a narrower box so the text stays inside the outline.

## 0.10.6
- TV shows: no duration column; clicking a show opens its seasons (the episode pane no longer stays open from an earlier visit).
- Episodes / seasons views: the clock, scroll bar and count column on the right like the other views; seasons and episodes show the clearlogo above the studio logo, or the landscape art when there is no clearlogo.
- Episodes view (flat seasons / single season): episode list with the episode info pane always shown.

## 0.10.5
- Compact list, Album list, Song list: the selected row keeps white text when focus moves to the A-Z / scroll bar strip (dark text only while the list itself has the white bar).

## 0.10.4
- Ratings: per-source icons (IMDb, TMDb, Rotten Tomatoes, Trakt as enabled) in the episode pane, the episodes info pane and the movie / show info page; a star only when no source has data.
- Episode pane: audio codec shows DTS-HD MASTER AUDIO, DOLBY DIGITAL PLUS etc. instead of the raw codec name.

## 0.10.3
- Seasons list: the box stays put while the highlight moves. Right opens the episodes of the season (slides in) with an episode pane: thumb, season/episode, air date, runtime, media chips, rating and plot.

## 0.10.2
- Aeon style: labels and icons on the white focus bar turn dark (settings categories, rows, dialogs); the context menu and other default buttons show the white bar.

## 0.10.1
- Aeon style: the focus highlight in menus, dialogs and settings is a flat full-white bar, edge to edge in its box (the glowing glass highlight stays for the Glass style); settings list and context menu fill their box.

## 0.10.0
- Aeon style: dialogs, menus and settings now use a flat Aeon palette (greys, white focus bar with dark text) instead of the navy Glass look; the Glass style keeps the old look. Style switch: Library view style (Aeon / Glass).
- Settings, skin settings and dialog backdrops are flat grey in Aeon style (no navy art / fanart backdrop).
- Music top menu: Artists / Albums / Songs / Genres now switch the list in place (Artists no longer reloads Albums).
- Music view picker: the artist wall is called Fanart wall for artists too.

## 0.9.12
- List view: long titles stop before the resolution chip.

## 0.9.11
- List view: the count box has the film icon like the other views.
- Certification icons: R and unrated (U) get a triangle with the letter centred in it; PG is a circle; long codes (PG-13, TV-MA...) use a smaller font so they fit; letters are centred on the shape; plain "R" certificates no longer fall back to a square.

## 0.9.10
- View pickers: the List card shows its mock-up; the current view is marked with a ring like the Home pager.

## 0.9.9
- Library views: Right past the A-Z / scroll bar strip opens the options panel (Left no longer does).
- View header shows the view name in bold, e.g. POSTER WALL: TITLES.
- View pickers rebuilt as a scrolling list: Left/Right works for every card, full white outline on the focused card, current view marked.

## 0.9.8
- Movies / TV shows / sets: the clock, A-Z, scroll bar and count column is on the right, same width and style as in the music views (film icon instead of headphones); content and bottom bars made room for it.

## 0.9.7
- Movies / TV shows: view picker with a mock-up per view (Library panel > View), offering only the views that fit movies, sets, shows, seasons or episodes.

## 0.9.6
- Music view picker: only the views that fit what you are browsing (artists, albums or songs), named for it (Artist wall, Album showcase, Song list...).

## 0.9.5
- Music views: the clock / scroll bar / A-Z / count strip is on the right in every music view, same width as the Albums and Songs list.

## 0.9.4
- Music top menu: a bar under the focused button; Up from the top row of the wall views reaches the menu.

## 0.9.3
- Music views: Up from the top row of any view (wall, showcase, lists, A-Z strip) reaches the Artists / Albums / Songs / Genres menu.
- Library side strip: the option now makes the whole strip (A-Z keys, scroll bar, between the clock and count boxes) dark or white.

## 0.9.2
- Skin settings > Look: the Library scroll bar row can now be reached with Down.

## 0.9.1
- Music views: the item counter / clock no longer overlap the new View and Sort buttons.

## 0.9.0
- Resolution badge drawn from PNGs: the HD fill follows the rounded outline.
- Certification icons: a different outline per age group (circle, double ring, triangle, hexagon, rounded square).
- Music artist view re-laid out: list flush under the clock box, cover under the list beside the artist art, A-Z key list next to the scroll bar.
- Music library: Groove-style top menu (Artists / Albums / Songs / Genres, plus View and Sort buttons at the top right); Up from the first item or the # key reaches it.
- Music View: a modal with a mock-up card per view (Library panel > View, or the top-right View button).

## 0.8.1
- Home spotlights are reshuffled every time you come back to Home (random sort no longer keeps the same titles).

## 0.8.0
- List view: the media info chips and ratings sit in a bar beside the count box (the list ends above it); resolution badge in two parts (ULTRA | HD, FULL | HD, READY | HD, SD); bold hours in the runtime; the runtime column has the same tint as the certificate column.
- Library views: more room between the strip and the title pane; media chips on the ratings row, right aligned.
- Aeon library background: Neutral, Fanart or a Color that follows the artwork and fades between titles; default in Appearance, override per home menu item (Edit spotlight).
- Scroll bar colour setting (Look): dark or white.
- Music library: right strip with clock, scroll bar and count with headphones; for artists the album count and a cover that cycles through their albums every 5 s.
- Kodi screensaver set to None.

## 0.7.0
- Compact list and Banner list redesigned: narrower list (the Banner list shows seven banners), a right pane with the poster and the fanart side by side at the same height, then Title | Year | Duration, Director | Genre, tagline and the autoscrolling plot. Media info chips and ratings sit in a bar beside the count box at the bottom. The versions pane replaces the poster only; the details follow the version.

## 0.6.2
- Compact list and Banner list: the chips and ratings follow the version you are cycling through in the versions pane.

## 0.6.1
- Compact list and Banner list: poster left, title and chips beside it, a wide autoscrolling plot underneath; the versions pane fits the poster.

## 0.6.0
- Compact list and Banner list: the side column is narrower and fits the poster with the title, media chips, ratings and plot underneath; the versions / set pane uses the poster space; up / down arrows and a count show in it.
- Rows and banners of titles with versions (or sets) get an arrow-pointed highlight, like the List view.

## 0.5.7
- Banner list: titles with several versions (and sets) have the same versions pane as the Compact list.

## 0.5.6
- List view: the resolution tag has more room around its text and now shows ULTRA HD, FULL HD (1080), HD READY (720) or SD for anything lower.

## 0.5.5
- Library lists: the Banner list, Album list and Song list also end flush with the top of the count box.

## 0.5.4
- Library views: the heading sits clear of the clock box; the Compact list ends flush with the top of the count box.

## 0.5.3
- Compact list: the versions pane covers the side panel; fewer images preloaded per view.

## 0.5.2
- Compact list: titles with several versions (and sets) have a side pane like the List view; Right from the list enters it, Up / Down browse the versions, Left or Back returns.

## 0.5.1
- Library views: the info panel no longer covers the left strip.

## 0.5.0
- All library views: a left strip with the clock, A-Z quick jump, scroll bar and item count (same look as the List view strip); Left from the list reaches it, Left again opens the library panel.
- Down on the last item goes to the first, Up on the first goes to the last.
- The focused poster keeps its natural look (no gradient or dimming).
- Aeon style: neutral background by default or fanart (Appearance > Aeon library background), List-view palette.
- List view: media info chips and rating icons over the bottom of the poster.

## 0.4.0
- Library view style setting (Skin settings > Appearance > Library view style): Aeon (flat dark panels, white highlight bar with dark text, outlined chips, white tile frames) or Glass (translucent panels, soft highlight, filled chips) for every library view. Default: Aeon.

## 0.3.2
- Library views: the Compact list and Banner list side panels also show the rating icons and media info chips.

## 0.3.1
- Cards: no duplicate small title under the clearlogo.

## 0.3.0
- Library views: the info line now uses chips for resolution, HDR, audio, channels, date, genre, rating and length, and rating-source icons (IMDb, TMDb, RT, Trakt); Cards show the clearlogo (or the title) on each card.
- File browser: long file names use the full row width and scroll when focused.

## 0.2.11
- Library views: the Landscape wall, Square wall, Cards, Album wall and Artist wall used the poster for every tile (cropped); each view now uses its own artwork.

## 0.2.10
- Home strips: posters are a little smaller so the bottom edge and the focus border (also when zoomed) stay on screen.

## 0.2.9
- Home strips: posters are shown whole (no more cropped top and bottom) and the white focus border is complete on all four sides.

## 0.2.8
- Spotlight: movie and TV show clearlogos (or the title when there is none) show again; two conditions I broke had unbalanced brackets.

## 0.2.7
- Spotlight: the More information button is wide enough for its whole label.

## 0.2.6
- Music spotlight: shows the album title under the artist logo, with chips for artist, year, genre, record label and length (no movie rating sources); the album review is used as the text.

## 0.2.5
- Widget screens options: the first row is now "Widget (Up key after Spotlight)"; the rows were widened to fit.

## 0.2.4
- Home: Back from the sub-menu strips returns to the home menu item and resets the strip to its first list.

## 0.2.3
- Spotlight: the title sits above the chips and is easy to read; audio chips read TRUEHD ATMOS, DTS-HD MASTER AUDIO and so on; the rating chip reads RATED PG-13.
- Lyrics overlay: semi-transparent so the cover shows through, with the first and last lines fading out.

## 0.2.2
- Spotlight: the title (e.g. Recently added movies) sits in the upper left like on the widget screens; media info and details are chips (resolution, HDR, audio codec, channels, date, rating, runtime); rating sources show their icons (IMDb, TMDb, RT, Trakt; icons from the AF3 skin); items without fanart show a neutral background, not the poster; the More information button label no longer overlaps its icon.

## 0.2.1
- Spotlight editor (Skin settings > Home menu > Edit spotlight): on/off, label, path, items, sort by, reverse order, seconds per item. The Up-key options moved to "Widget screens options". The spotlight timers no longer use unsupported expressions.

## 0.2.0
- Home: a Netflix-style Spotlight above the menu for Movies, TV shows and Music (fanart, logo, tags, rating, plot, Play / More information, cycling with the circle and dots). Up from the menu focuses it; Up again opens the widget screens.

## 0.1.71
- Home strips: the first tile no longer loses the left edge of its white focus border. Episode tiles show season/episode number and the episode title under the thumbnail.

## 0.1.70
- Home now-playing: the equaliser bars keep a fixed base and only change height (never taller than their resting height, well below the cover).

## 0.1.69
- Home now-playing: the equaliser bars are animated while music plays (still when paused or with reduce motion).

## 0.1.68
- Home: the now-playing block has four placements (Skin settings > Appearance > Now playing on Home, with preview): Slot (lower left, default), Corner (top left), Line (above the menu), Bar (bottom). It now shows the album cover, with the eq bars in front of it, and no longer overlaps the tiles.

## 0.1.67
- Music library: scrollbar and an A-Z quick-jump strip (Right from the list) on the album/artist/song walls and lists.
- Lyrics (CU LRC Lyrics) now show as an overlay on the Now playing cover instead of the stock dialog.
- The pager rings and dots (Up pages, screensaver) are crisp, properly round images.

## 0.1.66
- Dialogs opened from settings screens (file browser, add-on install list, pickers) show the System background instead of black; focused filled buttons such as OK keep a readable dark label.

## 0.1.65
- Settings backdrop: the last fanart you looked at is now remembered between restarts (it was lost, so the backdrop and its strength showed nothing).

## 0.1.64
- Settings: the home-menu editor dialogs use the System background; the settings screens show the System background under the fanart; Backdrop strength is ordered Light / Medium / Strong and the three levels now really differ (Strong shows the most fanart).

## 0.1.63
- Search gets its own amber magnifier background on Home.

## 0.1.62
- Backgrounds: a sleek dark gradient replaces plain black everywhere; Power gets a red power-symbol background and System / the settings screens a blue gear background.

## 0.1.61
- Music widget screens: the record label logo (resource.images.recordlabels.white) is shown in the studio slot.

## 0.1.60
- Music widget screens: artist landscape art first (else fanart with the artist clearlogo under the header) and the record label under the title, with the Studio / network setting.

## 0.1.59
- Live TV: the channel list (Up from Live TV) now shows the channel logos.

## 0.1.58
- Live TV: the "Now on TV" panel on Home no longer stays hidden after moving to another menu item and back (it used two fighting animations; now a plain visible condition).

## 0.1.57
- Settings: the focus bar fades between rows instead of sliding (it could jump to the last row and back).
- Library: 7 new video views (Poster wall, Landscape wall, Square wall, Cards, Showcase, Banner list, Compact list) and 5 music views (Album wall, Cover showcase, Album list, Song list, Artist wall). The library panel View row cycles through them.

## 0.1.56
- New Widget screens settings page: media info, ratings and studio / network can be switched on for the full-screen widget pages (Up on a home item). 4K shows as "4K" not "4K P".

## 0.1.55
- Home strips: Auto artwork per item (episodes use the episode thumb in a landscape tile, artists/albums/songs use their cover or thumb in a square tile, others the poster). Square forced = square art, else cover/thumb or the poster cropped square. Landscape forced = landscape art, else fanart with the clearlogo bottom right. Episodes show S01E04.
- Spotlight: episodes show show title and S01E04 above the title.

## 0.1.54
- Settings rows: labels centred on the icon and controls; switches use a proper rounded pill texture.

## 0.1.53
- Now playing: the wave starts exactly at the card border again (the window zoom-in was shifting where Kodi started the visualisation; the window now only fades).

## 0.1.52
- Now playing: one flatter wave line that starts at the left border of the card and ends at its right border (positioned around the stock Waveform add-on's double offset).

## 0.1.51
- Now playing: the waveform is back and confined to the card width (Kodi only draws it in a full-height box).

## 0.1.50
- Versions pane: long titles wrap onto a second line instead of being cut off; the up / down markers are now glass chips with a chevron.

## 0.1.49
- Settings backdrop and glass panels now show on the Aeon settings page; backdrop a little brighter.

## 0.1.48
- Settings: new Appearance page (accent colour, fanart backdrop and strength), fanart backdrop and frosted glass panels, category and row icons, switches and segmented choices, live preview panel, sliding focus bar, pages slide in and rows appear one after another. Kodi settings pages get the backdrop and panels.
- Accent colour follows every focus bar.
- Home: vignette, tiles grow 6 percent when focused. Spotlight: slow zoom. Windows zoom and fade; dialogs drop in; paused video dims; library pages tinted by the artwork colour; empty lists show an icon.

## 0.1.47
- Submenu artwork type: Landscape replaces Banner (landscape art, else thumb).

## 0.1.46
- Settings hub, System info, Event log, Profiles and shared dialog lists restyled to Aeon (gradient focus bar, hairlines, flat boxes, uppercase header); hub says Aeon Fuse.
- Submenu rows have an Artwork type (poster / square / banner) in the Edit submenu dialog.
- OR expressions are bracketed so negating them works.

## 0.1.45
- Up pages: pages 2-6 now actually show (they stayed hidden behind page 1); the circle and dots pager is drawn above the pages.
- Home: Down / Up in a strip steps through the submenu categories (each category shows its own row).
- Widgets / submenu editors: flag labels fixed.

## 0.1.44
- Up pages: first page always focusable, path read with fallback, pager dots set on open. Home menu: Edit widgets / Edit submenu / Edit spotlight per item. Submenu categories under the home title and Power actions now come from the skinvariables list (menu aeonmenu).

## 0.1.43
- New settings pages Details, Ratings, Behaviour, Backgrounds: info tags (resolution / HDR / audio), plotline, autoscroll, studio logo, rating sources and colour, seek bar time (total / left / ends), controls on pause, Back button mode, extra fanart cycling, artist slideshow.

## 0.1.42
- Settings: removed Time & mood and Borrowed colour (old skin); descriptions now at the bottom of the screen.

## 0.1.41
- Move up / down and Restore default order now start the helper by path (Kodi would not run it by add-on id).

## 0.1.40
- Home menu settings: Move up / Move down / Show-hide / Rename / Edit lists as buttons on the right (no arrow-key moving); Restore default order. Home items can be renamed. Needs script.aeon.helper 0.1.1.

## 0.1.39
- Settings: "Main menu" category removed; Home menu has Show / hide (OK on an item) next to ordering. Hidden items say "Hidden".

## 0.1.38
- Home lists editor: option buttons were hidden by a bad condition (now shown); lists are found by id, not by position; custom menu item targets are chosen in the editor; new data file (aeonlists).

## 0.1.37
- Settings: single "Home menu" category. OK on a home item opens its lists (Up pages); Left / Right move it up / down the menu; the editor can also change what the position shows.

## 0.1.36
- Music lists: the list now ends on a whole row, so no sliver of the next title shows at the bottom.

## 0.1.35
- Up pages (spotlight) are now fed by script.skinvariables lists (menu "aeonhome"): Skin settings > Home lists opens an editor to add, delete, reorder, rename, choose a path, sort, reverse, limit, hold time and autoscroll per list.

## 0.9.21 (2026-10-30)
- Counts read right at one: 1 season, 1 episode, 1 film, 1 track, 1 item.
- Smaller download: removed images the skin never used.

## 0.9.20 (2026-10-30)
- Libraries: "Nothing here." no longer sits on the Back row of an empty folder (List and Grid views, Episodes and Rows).
- Select lists (languages, choices) no longer show a half-cut row at the bottom.
- Settings: Right on Look now enters the page when TMDb Helper is not installed (it did nothing and quietly switched Borrowed colour off).

## 0.9.19 (2026-10-29)
- The Menu button's item menu now starts with View, sort, filter… (one press up from the first item), which opens the skin's options on View.

## 0.9.18 (2026-10-28)
- More views in every section: a new Rows view for shows and seasons (one row each with the show's wide picture, year, seasons, what's left to watch and the plot). The Wall now also shows genres as name cards, and the music Grid and Spotlight now also show songs. Shows offer six views, genres three, songs three.

## 0.9.17 (2026-10-28)
- Custom main-menu items: put up to three add-ons, favourites or library folders on the main menu (Settings > Custom menu items).
- On Home they are pills of the top line between Search and the settings gear, in the same type and focus colour; the other pills move left to make room (long names are shortened when two or three show). OK opens the item; Back comes home to its pill. With none set Home is unchanged.

## 0.9.16 (2026-10-28)
- Spotlight (films and music): the strip ends on a whole poster or portrait instead of one cut at the card's edge.

## 0.9.15 (2026-10-27)
- More ways to browse (View pill or Options > View; the picker now shows up to six previews):
  - Spotlight (films, sets, shows, seasons, music videos): the focused title large, its fanart melting into the card, plot and "start now and it ends at ...", over a strip of posters that each say when they would end.
  - Wide (everything, add-ons and plug-ins too): landscape cards in four columns; episodes show their stills, add-ons their fanart, other items keep their own picture whole.
  - Time (films, episodes, music videos): each title is a bar from now to the moment it ends, four hours across; in the bedtime hours a moon line marks your bedtime and everything after it falls into shade.
  - Music Wall (albums, artists, genres, years): the whole page of covers, eight across; artists as round portraits.
  - Music Spotlight (artists, albums): the artist's fanart large with the biography or album notes, over a strip of round portraits or covers.
- Existing views and their defaults are unchanged. The Wall header no longer prints ".." for the Back item and sits on the card's inset.

## 0.9.14 (2026-10-25)
- Sleep after this: seeking, skipping, fast-forward or buffering re-time the stop, so the end of the film is no longer cut off.
- Sunday and weekend choices on Home now work in every language (they never matched before).
- Search: a query with a double quote (e.g. "Superman" or Waiting for "Superman") now finds its matches; before, the quote broke the search and nothing came up. Past the result limit a count reads "30+" instead of one more than the matches (the last item, More..., opens them all).
- Video: the buffering box also shows at 0 %, so a stall at the very start of a stream is visible.
- Code clean-up: dialog buttons no longer carry an undeclared enable parameter.

## 0.9.13 (2026-10-23)
- Weather: with no weather add-on set in Kodi, every weather piece stays hidden, and Skin settings > Time & mood says where to choose one (Settings > Services > Weather). The weather also hides while Kodi is refreshing it, in every language (no more "Busy").
- Time: the Mood row shows the mood Auto has picked next to Kodi's clock, so a wrong clock or time zone on the device is easy to spot. Daylight follows Kodi's clock in every region and in 12 h and 24 h formats.
- Bedtime shows as 12 h or 24 h by the region's clock in every language.

## 0.9.12 (2026-10-23)
- Official repository requirements: artwork moved to resources/, screenshots added.

## 0.9.11 (2026-10-22)
- Settings: choose which main menu items to show.
- Home: up to three custom rows from any add-on, playlist or favourite.
- Skin settings > Main menu: Films, Shows, Music and Search pills (on Home and in the libraries). Films also takes the hero and the film cards off For now, Shows the Next up card; the rest close up. For now and the gear always stay. Everything is shown by default.
- Custom rows: Skin settings > Custom rows: Row 1, 2 and 3. OK offers Add-on, playlist or library... (Kodi's own browser: an add-on folder, a smart playlist, a library node), A favourite... (one that opens a folder), Rename... and Clear. A row shows only while it has items; folders open in their window, files play, Back comes home. Nothing changes on Home until a row is set up. The rows are full-width card rows under Home's own rows: Down from the last row; Up returns.

## 0.9.10 (2026-10-21)
- Visualiser presets button in the music player.
- Music controls: a "Visualiser presets" pill after Queue; Left from Play/Pause reaches it in one press (the row still wraps). Opens Kodi's preset list; Back returns to the pill. Only while a visualisation with presets is running.
- Now playing over a visualisation with presets: the small card says "OK, then ← for presets".
- The OSD auto-hide waits while the preset list is open.

## 0.9.9 (2026-10-21)
- Sets row in the Library panel; fix for controls disappearing with Reduce motion on. Code clean-up for the Kodi repository checks.
- Code clean-up for the Kodi repository checks: unused code and fonts removed, on-screen text moved to the strings file, LF line endings. Search now encodes the typed text with Skin Variables (script.skinvariables, now required), so titles with & + % are found.
- Game controller windows: the controller pictures used colour names Daylight doesn't define; they now use the skin's ink colours.
- Sets: while you browse films (and the library has sets), the Options card has a "Sets" row: it opens the
  list of sets in the same window, with the same views as films (Grid, Wall, List); picking a set opens its
  films, and Back walks back set -> all sets -> films. Not a Home item.
- Reduce motion: Anim_FadeVisible, Anim_TopStrip, Anim_RowStagger and Anim_BackgroundCrossfade carried two Hidden
  animations (Kodi only resets the first when a control shows again, so with Reduce motion on, for example, the seek bar, the
  slider strip, the Home hero and the list view stayed invisible after their first hide); now one each.
- Reduce motion: a view-picker card kept its 106 % focus scale after focus left the picker list; now a
  Conditional animation on the list's focus.

## 0.9.8 (2026-10-21)
- Library panel: the library's own menu (View, Sort, Order, Unwatched only, Search, Update library, Clean
  library, Library settings) as a soft card under the header pills. Reach it with Left / Right past the
  edges of any library view, Left / Right past either end of the header pills, or the new "Options" pill
  in the top line (left of For now). Back closes it and leaves you on the item you came from.
- Clean library asks first ("No" is focused): Kodi's own CleanLibrary() would just run.
- View picker: the View pill and View in the panel open previews of the views that fit the folder (Grid,
  Wall, Episodes, List; music Grid, List), the current one marked; OK switches, Back keeps it. The previews
  are layered and take the mood colours, so they match the page at any time of day
  (_src/make_view_previews.py, no artwork).
- Home: the System menu (gear) gains Update library and Clean library (Films and shows or Music).

## 0.9.7 (2026-10-20)
- Language file: the strings.po header is valid gettext again (each header line one quoted string ending in \n).
- System menu: Live TV, Pictures, Favourites and Files (Live TV only when a PVR add-on is enabled); the card grows with the list.
- Reduce motion now also covers the slow background drift and the progress toast: no gliding, everything lands in place.

## 0.9.6 (2026-10-20)
- Author shown as KarmaMole; website link to the showcase. Solid icon (the official repository does not allow transparency).

## 0.9.5 (2026-10-20)
- Install fix: the optional TMDb Helper dependency now accepts any version from 4.0.0, so the skin installs
  next to the 5.x TMDb Helper from Kodi's official repository ("unable to match dependency" on Kodi 21.3).

# Daylight (skin.daylight) changelog

## 0.9.4 (2026-10-18)
- Library header: the Sort pill (and the sort arrow) now have fixed widths too, so nothing in the row
  moves when you pick another sort. The caption beside the page title is fitted to the room left:
  on the Shows page it shows just the count ("8 of 219"), and long titles / captions stop before the
  pills everywhere (also on the Wall view and the other list pages).
- Player controls (the small panel Kodi shows while music plays outside fullscreen) is now a rounded
  Daylight card: rounded cover, Fraunces title, rounded track with times, circle buttons in the OSD
  order (Play / Pause, Stop, Previous, Next) and Repeat / Shuffle pills for music.

## 0.9.3 (2026-10-18)
- Home hero: up to five picks instead of one. Left on Play shows the previous pick, Right past the
  last button (Trailer, or More when there's no trailer) the next one; small dots show which pick.
  Focus never lands on a hidden Trailer button.
- OSD: Play / Pause, Stop, then Previous / Next (when there are chapters or a playlist), then
  Subtitles, Audio, Video, Chapters, Info, Stats. The Back 10 s / Ahead 30 s buttons are gone
  (Left / Right seek without the OSD; Up lights the track).
- Music OSD: Play / Pause, Stop, Previous, Next, then Shuffle, Repeat, Queue; no seek buttons.
- Library header: the All / Unwatched only, In progress / All shows and View pills have fixed widths,
  so the row no longer shifts sideways when one of them changes. Same for Shuffle in the queue.
- Home suggestions are really shuffled / ranked now: Kodi ignored the order inside the smart-playlist
  links, so the hero was always the alphabetically first match and the first card ran A to Z. The hero
  is a random pick again and "More under 100 minutes" / "Top rated" are sorted by rating.
- Films with no runtime in the library are no longer offered as "fits before bedtime" / "under 100
  minutes".
- The page colour follows the hero again when you come back up from a card.
- Search: the Artists row lines up with the poster rows. System menu: a little more room under its title.

## 0.9.2 (2026-10-18)
- Home cards: Down / Up now step straight from card to card (Fits before ... -> Next up -> third
  card, and back; Up from the first card goes to the hero) from any item, no need to scroll to the
  end of a strip. Left / Right still scroll inside a card and spill over at its ends. Empty cards are
  skipped; each card keeps its position.
- The focused card shows it: its title turns accent and a small down chevron marks "Down = next card".
- Next up is now a strip of two episode tiles (thumb on top, show / episode / time below), so all
  three cards scroll the same way.
- Back always ends on Home's main menu: Home now opens on the menu (For now); Back from any Home card
  goes to the menu; the Films / Shows / Music / Search pills inside the libraries swap the page instead
  of stacking it, so one Back returns Home however many pills you used; music tabs (Albums / Artists /
  Songs / Genres) no longer add a Back step each; Collection from an info page opens in place.

## 0.9.1 (2026-10-18)
- Bedtime tick: a small mark (and moon) on the OSD / seek bar track where your bedtime falls in the film.
- Redesigned in the Daylight language (cards, Fraunces, accent-fill focus): music info, Now playing,
  music OSD, slideshow and picture info, weather, file manager, event log, profiles, system info,
  settings hub and Kodi settings pages, add-on info; PVR lists sit in a card (PVR is unused here).
- Long titles step down a size instead of clipping (info pages, Home hero, libraries, Now playing, OSD).
- Every dialog list and option row now focuses with the accent fill (no more outline frames).
- Weather words come from the condition code everywhere (the gismeteo text draws a missing glyph).
- Episode rows say "rated 7.9" (Figtree has no star glyph); keyboard Caps / Shift / Symbols widened.

## 0.9.0 (2026-10-18)
- First build, forked from the skin.majan engine and redesigned throughout.
- Four moods (Morning, Afternoon, Evening, Night) switch live with the clock; a setting can force one.
- Home "For now": greeting, countdown to bedtime, weather, a Tonight hero and three contextual cards
  (fits before bedtime / Next up / rain or just added).
- Borrowed colour: the focused film's palette tints the page light (TMDb Helper, optional).
- Video OSD: rounded panel, "ends 11:41 PM · 11 min past your bedtime", Sleep after this.

## 0.1.1 (Aeon Fuse)
- New Aeon 2 style video library view (id 510): poster pane + dark list with notch focus bar,
  Left on sets/versions opens a left poster grid/stack, Right slides the info pane in.
