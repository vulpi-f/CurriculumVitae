# Curriculum Vitae

LaTeX source for Fabio Vulpi's one-page CV.

## Build

```sh
latexmk cv.tex
```

The generated file is `cv.pdf`.

The source also emits machine-readable visual metrics while compiling.  To
validate the alignment-sensitive parts of the layout after text edits, run:

```sh
latexmk -pdf -g -interaction=nonstopmode cv.tex
python3 scripts/check_visual_metrics.py cv.log
```

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

- `\sidearrowwidth`, `\sidearrowheight`, `\sidearrowbaseline`,
  `\sidearrowboxwidth`, `\sidearrowtrimleft`, `\sidearrowtrimbottom`,
  `\sidearrowtrimright`, `\sidearrowtrimtop`, `\sideheadinggap`: left-column
  chevron artwork size, fixed marker box, transparent-canvas crop, baseline, and
  heading spacing.
- `\sectiontitlegap`: gap between the main-column section titles and the
  horizontal rules.  `\mainsection` measures the title and computes both rule
  widths from `\linewidth`, then raises the rules so their stroke centres align
  with the measured title box centre.
- `\dividergap`: symmetric vertical spacing above and below the right-column
  entry dividers.  The divider macro suppresses the extra interline glue around
  the rule so the requested gap is the rendered gap.
- `\skillgroupvspace`, `\langbarvspace`, `\beforepublicationsgap`: left-column
  vertical rhythm controls for the digital-skills groups, language bars, and
  the gap before the publications heading.
- `\pubiconwidth`, `\pubiconboxwidth`, `\pubicongap`, `\pubiconartwidth`,
  `\pubicontrimleft`, `\pubicontrimbottom`, `\pubicontrimright`,
  `\pubicontrimtop`, `\pubtextwidth`, `\publineheight`, `\pubentrygap`:
  publication badge, transparent-canvas crop, text, line-height, and inter-entry
  spacing controls.
- `\orcidboxwidth`, `\orcidartwidth`, `\orcidtrimleft`, `\orcidtrimbottom`,
  `\orcidtrimright`, `\orcidtrimtop`, `\orcidbaseline`: ORCID marker box,
  artwork size, crop, and vertical centring for the publications heading.
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

## Visual metrics

`cv.tex` writes `CVVISUAL|...` records to `cv.log` for geometry that is easy to
break when changing copy:

- publication badge height versus measured publication text height;
- link icon centre versus badge centre;
- main-section rule centre versus section-title centre;
- divider spacing above versus below the teal rule.

`scripts/check_visual_metrics.py` parses those records and fails when a metric
exceeds its tolerance.  These checks are not a substitute for a final human
preview, but they catch the recurring alignment regressions before opening the
PDF.
