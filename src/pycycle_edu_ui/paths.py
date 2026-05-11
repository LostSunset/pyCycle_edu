from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_PYCYCLE = PROJECT_ROOT / "upstream" / "pyCycle"
REFERENCE_SOURCES = PROJECT_ROOT / "Reference_sources"
REFERENCE_APP = PROJECT_ROOT / "Reference_answers" / "pycycle_ui_ux_reference"
RUNS_DIR = REFERENCE_APP / "runs"
REPORTS_DIR = REFERENCE_APP / "reports"
CHARTS_DIR = REFERENCE_APP / "charts"
