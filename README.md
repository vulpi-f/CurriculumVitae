# Curriculum Vitae

LaTeX source for Fabio Vulpi's one-page CV.

## Build

```sh
latexmk cv.tex
```

The generated file is `cv.pdf`.

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
  `\sideheadinggap`: left-column chevron size, baseline, and heading spacing.
- `\pubiconwidth`, `\pubicongap`: publication badge width and text separation.
- Header/content anchor coordinates inside the root `tikzpicture`: use these
  only after the local size controls above are exhausted.

## Icon/package notes

Online package checks performed for icon matching:

- CTAN `fontawesome5` provides LaTeX support for the Font Awesome 5 Free set and
  supports `\faIcon{...}` names such as `phone`, `map-marker-alt`, `calendar-alt`,
  `linkedin`, `github`, `envelope`, and `link`.
- CTAN `academicons` provides academic-profile icons, including ORCID.  The
  current source keeps the existing `FIGURES/CV_orcid_icon.png` asset because it
  matches the reference colour/shape closely without requiring a new TeX package.
- The side-section arrow is now drawn as a TikZ vector chevron instead of a PNG;
  this keeps the arrow crisp and makes baseline/shape retouching local to
  `\sideheading`.

If a future editor installs extra LaTeX packages and wants a font-based ORCID
icon, test `academicons` or the ORCID icon available in newer Font Awesome
bindings against the reference PDF before replacing the current asset.
