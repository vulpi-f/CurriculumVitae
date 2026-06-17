# Curriculum Vitae

LaTeX source for Fabio Vulpi's one-page CV.

## Build

```sh
latexmk -pdf -interaction=nonstopmode cv.tex
python3 scripts/check_visual_metrics.py cv.log
```

The generated file is `cv.pdf`.  The second command validates the visual-layout
metrics emitted in the LaTeX log.

## Visual metrics

`cv.tex` emits `CVVISUAL|...` lines while it builds.  These values are intended
to fail fast when text edits accidentally break the planned visual alignment:

- `publication_height_delta_pt`: teal publication badge height versus measured
  publication text height after visual trims.
- `publication_icon_center_delta_pt`: publication icon centre versus badge
  centre.
- `publication_icon_art_size_delta_pt`: link artwork size versus
  `\publinkiconsize`.
- `page_margin_*` and `column_gutter_*`: horizontal geometry derived from the
  header photo margin, including equal outer margins and equal gutters around
  the sidebar frame rule.
- `main_auto_gap_count_pt`, `main_auto_gap_pt`,
  `main_auto_divider_gap_pt`, `main_auto_section_gap_pt`, and
  `main_auto_gap_balance_delta_pt`:
  right-column content is measured with zero gaps, the remaining height is
  divided across ordinary, divider-rule, and section-title transitions, and
  the result must fill the frame exactly while staying non-negative.
- `sidebar_auto_gap_count_pt`, `sidebar_auto_gap_pt`, and
  `sidebar_auto_gap_balance_delta_pt`: left-column content is measured with
  zero object gaps, then the remaining sidebar height is distributed equally
  across the designated sidebar transitions.
- `mainsection_rule_center_delta_pt`: horizontal rules beside titles such as
  `AWARDS` versus the measured title-box centre.
- `divider_gap_delta_pt`: symmetry check for the vertical gaps around
  right-column dividers.

Run `python3 scripts/check_visual_metrics.py cv.log` after each PDF build to
apply the current tolerances.

## Structure

- `cv.tex`: main LaTeX source.
- `FIGURES/CV_picture_canva.png`: header photo extracted from the Canva reference PDF.
- `FIGURES/CV_picture.JPG`: original profile photo.

## Visual calibration notes for future edits

This repository is tuned as a one-page, absolute-positioned reproduction of the
reference CV.  The commit history shows that the largest visual changes came
from replacing the header crop (`138a969`) and then introducing dedicated icon
assets/spacing controls (`74f088f`), so future retouching should be incremental:

1. Rebuild `cv.pdf`.
2. Compare against the reference PDF at full-page scale first, then at 200%.
3. Change the named constants near the top of `cv.tex` before moving individual
   coordinates.

Current high-impact controls in `cv.tex`:

- `\cvphotomarginvalue`: single source for the outer page margin. It is the
  left margin of the header photo and drives the left sidebar x position, the
  right edge of the main column, the main-column header anchors, and the derived
  gutters around the sidebar frame rule.
- `\cvsidecolumnwidthvalue`, `\cvmaincolumnwidthvalue`,
  `\cvcolumnrulewidthvalue`: column widths and frame-rule thickness. The rule
  x coordinate and both gutters are derived from these plus `\cvphotomarginvalue`.
- `\cvmaincontent` and `\cvpreparemainlayout`: right-column content and its
  automatic vertical rhythm. The layout measures the natural content height,
  counts ordinary title/location/description transitions through `\cvmaingap`,
  counts divider-rule transitions through `\cvmaindividergap`, counts
  section-title transitions through `\cvmainsectiongap`, and fills
  `\cvmaincontentheight` with separate computed gaps. Tune
  `\cvmainbodygapshare`, `\cvmaindividergapshare`, and
  `\cvmainsectiongapshare`; the three shares are intended to sum to `1`, and
  equal shares produce equal individual gap sizes.
- `\sideheadingfontsize`, `\sidearrowheight`, `\sidearrowboxwidth`,
  `\sidearrowxshift`, `\sidearrowtrimleft`, `\sidearrowtrimbottom`,
  `\sidearrowtrimright`, `\sidearrowtrimtop`, `\sideheadingtextoffset`,
  `\sideheadinggap`, `\pubheadinggap`: left-column heading size, chevron
  height, fixed marker box, artwork crop, horizontal correction, and heading
  spacing. `\sideheadingtextoffset` keeps the larger chevron from crowding the
  title text while `\pubheadinggap` keeps the publication title on its row grid.
- `\cvsidebarframecutleftvalue`, `\cvsidebarframecutrightvalue`,
  `\cvsidebarframecutrisevalue`, and `\cvsidebarframecutdropvalue`: triangular
  sidebar-frame cutout that aligns the top border with the extended upper rear
  edge of the first chevron.
- `\sectiontitlegap`: gap between the main-column section titles and the
  horizontal rules.  `\mainsection` measures the title and computes both rule
  widths from `\linewidth`, so the rule pair is anchored to the right-column
  text block.
- `\cvsidecontent`, `\cvpreparesidelayout`, and `\cvsideobjectgap`:
  left-column content and measured automatic vertical rhythm. The layout first
  measures the sidebar with zero object gaps, counts designated transitions,
  and then computes `\cvsideobjectgap` so the content fills the sidebar frame.
- `\cvskillgroupvspace`, `\cvlangbarvspace`, `\cvsidebeforepublicationsgap`:
  left-column vertical rhythm controls for the digital-skills groups, language
  bars, and the gap before the publications heading; object-level gaps share
  the computed sidebar rhythm.
- `\cvsoftskilltriangleheightvalue`, `\cvsoftskilltrianglerule`: soft-skill
  triangle height and stroke thickness.
- `\pubiconwidth`, `\pubiconboxwidth`, `\pubicongap`, `\publinkiconsize`,
  `\pubicontrimleft`, `\pubicontrimbottom`, `\pubicontrimright`,
  `\pubicontrimtop`, `\pubboxvisualtoptrim`, `\pubboxvisualbottomtrim`,
  `\pubtextwidth`, `\publineheight`, `\pubentrygap`: publication badge,
  link-artwork size, transparent-canvas crop, visual text trims, text width,
  line-height, and inter-entry spacing controls.
- `\orcidboxwidth`, `\orcidartsize`, `\orcidtrimleft`,
  `\orcidtrimbottom`, `\orcidtrimright`, `\orcidtrimtop`: ORCID marker box,
  fixed artwork size, crop, and heading-centred vertical placement for the
  publications heading.
- Header/content anchor coordinates inside the root `tikzpicture`: use these
  only after the local size controls above are exhausted.

Publication line breaks are encoded with `\pubbreak`, not raw `\\`.  The
reference PDF requires controlled line cuts that cannot be reproduced by one
single natural text width for every publication title; using the semantic macro
keeps those breaks searchable and easy to retune.  The ORCID asset marks the
`PUBLICATIONS` heading via `\pubheading`; each publication row uses the teal
link badge with `FIGURES/CV_link_icon.png`.

## Icon/package notes

Online package checks performed for icon matching:

- CTAN `fontawesome5` provides LaTeX support for the Font Awesome 5 Free set and
  supports `\faIcon{...}` names such as `phone`, `map-marker-alt`, `calendar-alt`,
  `linkedin`, `github`, `envelope`, and `link`.
- CTAN `academicons` provides academic-profile icons, including ORCID.  The
  current source keeps the existing `FIGURES/CV_orcid_icon.png` asset because it
  matches the reference colour/shape closely without requiring a new TeX package.
- The side-section arrow uses the high-resolution transparent
  `FIGURES/CV_side_arrow.png` asset.  The `\sidearrowtrim...` constants clip
  away transparent canvas before the icon is placed in its fixed marker box, so
  replacing the PNG does not change the text offset.
- The publication link icon uses the high-resolution transparent
  `FIGURES/CV_link_icon.png` inside a dynamic TikZ badge.  The
  `\pubicontrim...` constants clip the icon canvas and the badge centres the
  visible artwork against each publication text box.

If a future editor installs extra LaTeX packages and wants a font-based ORCID
icon, test `academicons` or the ORCID icon available in newer Font Awesome
bindings against the reference PDF before replacing the current asset.
