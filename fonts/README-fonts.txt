Fonts in this folder (all SIL Open Font License 1.1, see the OFL-*.txt files)

Figtree, Barlow: the upstream static files, unchanged.

Cut from the upstream variable fonts (Google Fonts repository) with fontTools varLib.instancer, at weights 400 / 500 / 600 / 700,
because Kodi cannot pick a weight inside a variable font:
  Montserrat-*.ttf   from Montserrat[wght].ttf
  Manrope-*.ttf      from Manrope[wght].ttf
  AeonPSans-*.ttf    from IBMPlexSans[wdth,wght].ttf (width 100)      licence: OFL-IBMPlexSans.txt
  AeonSSans-*.ttf    from SourceSans3[wght].ttf                       licence: OFL-SourceSans3.txt
  AeonSSerif-*.ttf   from SourceSerif4[opsz,wght].ttf (default size)  licence: OFL-SourceSerif4.txt
"Plex" and "Source" are Reserved Font Names: a modified font may not carry them, so those three cuts have another
family name inside the file and another file name.

Heading faces for the font combinations (0.37.0), one weight each:
  Fraunces-Bold.ttf           cut from Fraunces[SOFT,WONK,opsz,wght].ttf at wght 700, opsz 48, SOFT 0, WONK 1   licence: OFL-Fraunces.txt
  Oswald-SemiBold.ttf         cut from Oswald[wght].ttf at wght 600                                          licence: OFL-Oswald.txt
  BebasNeue-Regular.ttf       upstream static file, unchanged                                                 licence: OFL-BebasNeue.txt
  BarlowCondensed-Bold.ttf    upstream static file, unchanged                                                 licence: OFL-BarlowCondensed.txt
Fraunces and Oswald have no Reserved Font Name, so the cuts keep their names.

Font combinations added in 0.38.0 (all SIL OFL 1.1, upstream files, unchanged):
  FunnelDisplay-ExtraBold.ttf                      Funnel (Dicotype)              OFL-Funnel.txt
  CalSans-SemiBold.ttf                             Cal Sans (Cal.com)             OFL-CalSans.txt
  HubotSans-*.ttf, HubotSansCondensed-ExtraBold.ttf, HubotSansExpanded-Bold.ttf   Hubot Sans (GitHub)   OFL-HubotSans.txt
  Saira-*.ttf, SairaCondensed-Bold.ttf             Saira (Omnibus-Type)           OFL-Saira.txt
  ClarityCity-*.ttf                                Clarity City (VMware)          OFL-ClarityCity.txt
  PretendardStd-*.ttf                              Pretendard Std                 OFL-Pretendard.txt
  Gnomon-Simple.ttf (variable; Kodi draws its default instance)   Gnomon (Indestructible Type)   OFL-Gnomon.txt
  LTSuperior-*.otf, LTSuperiorSerif-Bold.otf       LT Superior (LyonsType)        OFL-LTSuperior.txt, OFL-LTSuperiorSerif.txt
  LTVeritas-*.ttf, LTVeritas-BoldCondensed.ttf     LT Veritas (LyonsType)         OFL-LTVeritas.txt
  CooperHewitt-*.otf                               Cooper Hewitt                  OFL-CooperHewitt.txt
  Ronzino-*.otf                                    Ronzino (Collletttivo)         OFL-Ronzino.txt
  TASAExplorer-ExtraBold.ttf                       TASA (Taiwan Space Agency)     OFL-TASA.txt
LT Veritas and Ronzino have no SemiBold: the helper uses Medium there. Several of these carry Reserved Font Names;
the files are unmodified, so they keep their names.
The *.zip files in this folder are the user's own downloads; they are not part of the skin (the deploy skips them).

0.39.3: Figtree-*.ttf have two glyphs added by _src/fg_figtree_symbols.py: U+2726 BLACK FOUR POINTED STAR and U+25CF
BLACK CIRCLE (drawn as plain shapes), used in TV channel names. Figtree has no Reserved Font Name, so the name stays.

