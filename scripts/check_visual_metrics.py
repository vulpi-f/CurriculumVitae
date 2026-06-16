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
    "main_content_bottom_delta_pt": 0.10,
    "publication_height_delta_pt": 0.25,
    "publication_icon_center_delta_pt": 0.10,
    "mainsection_rule_center_delta_pt": 0.15,
    "divider_gap_delta_pt": 0.05,
}

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

    for idx, value in enumerate(require(metrics, "publication_height_delta_pt"), start=1):
        checks.append((f"publication {idx}: badge height equals text box height", abs(value), LIMITS["publication_height_delta_pt"]))
    for idx, value in enumerate(require(metrics, "publication_icon_center_delta_pt"), start=1):
        checks.append((f"publication {idx}: icon center equals badge center", abs(value), LIMITS["publication_icon_center_delta_pt"]))
    for idx, value in enumerate(require(metrics, "mainsection_rule_center_delta_pt"), start=1):
        checks.append((f"main section {idx}: rule centered on title box", abs(value), LIMITS["mainsection_rule_center_delta_pt"]))

    divider_values = require(metrics, "divider_gap_delta_pt")
    checks.append(("divider gaps: before/after divider rule are equal", max(abs(v) for v in divider_values), LIMITS["divider_gap_delta_pt"]))

    failed = False
    for label, observed, limit in checks:
        status = "OK" if observed <= limit else "FAIL"
        print(f"{status}: {label}: {observed:.3f}pt <= {limit:.3f}pt")
        failed = failed or observed > limit

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
