#!/usr/bin/env python3
"""Validate CV visual-layout metrics emitted by cv.tex.

Run after a LaTeX build, for example:
  latexmk -pdf -g -interaction=nonstopmode cv.tex
  python3 scripts/check_visual_metrics.py cv.log
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LIMITS = {
    "sidebar_content_bottom_delta_pt": 0.10,
    "sidebar_auto_gap_balance_delta_pt": 0.10,
    "main_content_bottom_delta_pt": 0.10,
    "main_auto_gap_balance_delta_pt": 0.10,
    "sidebar_top_inset_delta_pt": 0.05,
    "page_margin_left_delta_pt": 0.05,
    "page_margin_right_delta_pt": 0.05,
    "page_margin_symmetry_delta_pt": 0.05,
    "column_gutter_left_delta_pt": 0.05,
    "column_gutter_right_delta_pt": 0.05,
    "sideheading_arrow_height_delta_pt": 0.05,
    "publication_height_delta_pt": 0.25,
    "publication_icon_center_delta_pt": 0.10,
    "publication_icon_art_size_delta_pt": 0.05,
    "publication_top_delta_pt": 0.10,
    "publication_bottom_delta_pt": 0.10,
    "mainsection_rule_center_delta_pt": 0.15,
    "divider_gap_delta_pt": 0.05,
}

MAIN_GAP_NEGATIVE_TOLERANCE_PT = 0.05

METRIC_RE = re.compile(r"CVVISUAL\|(?P<name>[^|]+)\|\s*(?P<value>[-+0-9.]+)\s*pt")


def read_metrics(log_path: Path) -> dict[str, list[float]]:
    metrics: dict[str, list[float]] = {}
    for line in log_path.read_text(errors="replace").splitlines():
        match = METRIC_RE.search(line)
        if match:
            metrics.setdefault(match.group("name"), []).append(float(match.group("value")))
    return metrics


def require(metrics: dict[str, list[float]], name: str) -> list[float]:
    values = metrics.get(name, [])
    if not values:
        raise SystemExit(f"missing metric: {name}")
    return values


def main() -> int:
    log_path = Path(sys.argv[1] if len(sys.argv) > 1 else "cv.log")
    if not log_path.exists():
        raise SystemExit(f"log file not found: {log_path}")

    metrics = read_metrics(log_path)
    checks: list[tuple[str, float, float]] = []

    checks.append((
        "sidebar frame: fixed top plus height reaches target bottom",
        abs(require(metrics, "sidebar_content_bottom_delta_pt")[0]),
        LIMITS["sidebar_content_bottom_delta_pt"],
    ))
    checks.append((
        "main frame: fixed top plus height reaches target bottom",
        abs(require(metrics, "main_content_bottom_delta_pt")[0]),
        LIMITS["main_content_bottom_delta_pt"],
    ))
    main_gap_count = require(metrics, "main_auto_gap_count_pt")[0]
    main_gap = require(metrics, "main_auto_gap_pt")[0]
    main_body_gap_count = metrics.get("main_auto_body_gap_count_pt", [main_gap_count])[0]
    main_divider_gap_count = metrics.get("main_auto_divider_gap_count_pt", [0.0])[0]
    main_divider_gap = metrics.get("main_auto_divider_gap_pt", [main_gap])[0]
    main_section_gap_count = metrics.get("main_auto_section_gap_count_pt", [0.0])[0]
    main_section_gap = metrics.get("main_auto_section_gap_pt", [main_gap])[0]
    checks.append((
        "main column: measured elements plus computed weighted gaps fill the frame",
        abs(require(metrics, "main_auto_gap_balance_delta_pt")[0]),
        LIMITS["main_auto_gap_balance_delta_pt"],
    ))
    checks.append((
        r"sidebar top inset: actual gap matches \cvsideframetopinsetvalue",
        abs(require(metrics, "sidebar_top_inset_delta_pt")[0]),
        LIMITS["sidebar_top_inset_delta_pt"],
    ))
    checks.append((
        "outer margin: left column starts at the photo-derived page margin",
        abs(require(metrics, "page_margin_left_delta_pt")[0]),
        LIMITS["page_margin_left_delta_pt"],
    ))
    checks.append((
        "outer margin: right column ends at the photo-derived page margin",
        abs(require(metrics, "page_margin_right_delta_pt")[0]),
        LIMITS["page_margin_right_delta_pt"],
    ))
    checks.append((
        "outer margins: left and right are symmetric",
        abs(require(metrics, "page_margin_symmetry_delta_pt")[0]),
        LIMITS["page_margin_symmetry_delta_pt"],
    ))
    checks.append((
        "column gutter: left-column text to frame rule matches derived gutter",
        abs(require(metrics, "column_gutter_left_delta_pt")[0]),
        LIMITS["column_gutter_left_delta_pt"],
    ))
    checks.append((
        "column gutter: right-column text to frame rule matches derived gutter",
        abs(require(metrics, "column_gutter_right_delta_pt")[0]),
        LIMITS["column_gutter_right_delta_pt"],
    ))

    sidebar_top_inset = require(metrics, "sidebar_top_inset_pt")[0]
    sidebar_gap_count = require(metrics, "sidebar_auto_gap_count_pt")[0]
    sidebar_gap = require(metrics, "sidebar_auto_gap_pt")[0]
    sidebar_ordinary_gap_count = metrics.get(
        "sidebar_auto_ordinary_gap_count_pt", [sidebar_gap_count]
    )[0]
    sidebar_publication_gap_count = metrics.get(
        "sidebar_auto_publication_gap_count_pt", [0.0]
    )[0]
    sidebar_publication_gap = metrics.get(
        "sidebar_auto_publication_gap_pt", [sidebar_gap]
    )[0]
    checks.append((
        "sidebar column: measured elements plus computed gaps fill the frame",
        abs(require(metrics, "sidebar_auto_gap_balance_delta_pt")[0]),
        LIMITS["sidebar_auto_gap_balance_delta_pt"],
    ))
    print(
        "INFO: sidebar top gap from frame line: "
        f"{sidebar_top_inset:.3f}pt; adjust \\cvsideframetopinsetvalue to move ABOUT ME"
    )
    print(
        "INFO: sidebar column ordinary gap: "
        f"{sidebar_gap:.3f}pt across {int(round(sidebar_ordinary_gap_count))} transitions"
    )
    print(
        "INFO: sidebar column publication gap: "
        f"{sidebar_publication_gap:.3f}pt across "
        f"{int(round(sidebar_publication_gap_count))} transitions"
    )
    print(
        "INFO: main column body gap: "
        f"{main_gap:.3f}pt across {int(round(main_body_gap_count))} ordinary transitions"
    )
    print(
        "INFO: main column divider gap: "
        f"{main_divider_gap:.3f}pt across {int(round(main_divider_gap_count))} divider transitions"
    )
    print(
        "INFO: main column section gap: "
        f"{main_section_gap:.3f}pt across {int(round(main_section_gap_count))} title transitions"
    )

    for idx, value in enumerate(require(metrics, "publication_height_delta_pt"), start=1):
        checks.append((f"publication {idx}: badge height equals trimmed visual text box", abs(value), LIMITS["publication_height_delta_pt"]))
    for idx, value in enumerate(require(metrics, "publication_icon_center_delta_pt"), start=1):
        checks.append((f"publication {idx}: icon center equals badge center", abs(value), LIMITS["publication_icon_center_delta_pt"]))
    for idx, value in enumerate(require(metrics, "publication_icon_art_size_delta_pt"), start=1):
        checks.append((f"publication {idx}: icon artwork follows link-icon size parameter", abs(value), LIMITS["publication_icon_art_size_delta_pt"]))
    for idx, value in enumerate(require(metrics, "publication_top_delta_pt"), start=1):
        checks.append((f"publication {idx}: badge top equals trimmed visual text top", abs(value), LIMITS["publication_top_delta_pt"]))
    for idx, value in enumerate(require(metrics, "publication_bottom_delta_pt"), start=1):
        checks.append((f"publication {idx}: badge bottom equals trimmed visual text bottom", abs(value), LIMITS["publication_bottom_delta_pt"]))
    for idx, value in enumerate(require(metrics, "mainsection_rule_center_delta_pt"), start=1):
        checks.append((f"main section {idx}: rule centered on title box", abs(value), LIMITS["mainsection_rule_center_delta_pt"]))
    for idx, value in enumerate(require(metrics, "sideheading_arrow_height_delta_pt"), start=1):
        checks.append((
            f"sidebar heading {idx}: arrow vertical box equals configured arrow height",
            abs(value),
            LIMITS["sideheading_arrow_height_delta_pt"],
        ))

    divider_values = require(metrics, "divider_gap_delta_pt")
    checks.append(("divider gaps: before/after divider rule are equal", max(abs(v) for v in divider_values), LIMITS["divider_gap_delta_pt"]))

    failed = False
    for label, value in (
        ("sidebar column: object gap remains non-negative", sidebar_gap),
        (
            "sidebar column: publication gap remains non-negative",
            sidebar_publication_gap,
        ),
        ("main column: ordinary gap remains non-negative", main_gap),
        ("main column: divider gap remains non-negative", main_divider_gap),
        ("main column: section gap remains non-negative", main_section_gap),
    ):
        if value >= -MAIN_GAP_NEGATIVE_TOLERANCE_PT:
            print(f"OK: {label}: {value:.3f}pt >= {-MAIN_GAP_NEGATIVE_TOLERANCE_PT:.3f}pt")
        else:
            print(f"FAIL: {label}: {value:.3f}pt >= {-MAIN_GAP_NEGATIVE_TOLERANCE_PT:.3f}pt")
            failed = True

    for label, observed, limit in checks:
        status = "OK" if observed <= limit else "FAIL"
        print(f"{status}: {label}: {observed:.3f}pt <= {limit:.3f}pt")
        failed = failed or observed > limit

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
