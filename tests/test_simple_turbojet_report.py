from __future__ import annotations

from pycycle_edu_ui.runner.simple_turbojet_runner import (
    SimpleTurbojetInputs,
    SimpleTurbojetPoint,
    parse_summary_rows,
)
from pycycle_edu_ui.simple_turbojet_report import build_bilingual_report_text


SAMPLE_VIEWER = """
----------------------------------------------------------------------------
                              POINT: DESIGN
----------------------------------------------------------------------------
                       PERFORMANCE CHARACTERISTICS
    Mach      Alt       W      Fn      Fg    Fram     OPR     TSFC
 0.00000      0.0 168.453 11800.0 11812.0    12.0  13.500  0.91234
"""


def test_parse_summary_rows_preserves_design_values() -> None:
    points = parse_summary_rows(SAMPLE_VIEWER)

    assert points == [
        SimpleTurbojetPoint(
            point="DESIGN",
            mach=0.0,
            altitude_ft=0.0,
            mass_flow_lbm_s=168.453,
            net_thrust_lbf=11800.0,
            gross_thrust_lbf=11812.0,
            ram_drag_lbf=12.0,
            overall_pressure_ratio=13.5,
            tsfc=0.91234,
        )
    ]


def test_bilingual_report_uses_english_first_traditional_chinese_second() -> None:
    point = SimpleTurbojetPoint(
        point="DESIGN",
        mach=0.0,
        altitude_ft=0.0,
        mass_flow_lbm_s=168.453,
        net_thrust_lbf=11800.0,
        gross_thrust_lbf=11812.0,
        ram_drag_lbf=12.0,
        overall_pressure_ratio=13.5,
        tsfc=0.91234,
    )

    report = build_bilingual_report_text(
        inputs=SimpleTurbojetInputs(),
        points=[point],
        artifacts=["DESIGN.comp.pdf", "DESIGN.turb.pdf"],
        elapsed_seconds=1.25,
    )

    assert "# Simple Turbojet Report / 簡單渦輪噴射報告" in report
    assert "## Inputs / 輸入條件" in report
    assert "Net thrust Fn / 淨推力 Fn" in report
    assert "DESIGN.comp.pdf" in report
