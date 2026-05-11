from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReferenceMetric:
    key: str
    zh_name: str
    english_name: str
    value: float
    unit: str
    tolerance: float | None
    note: str
    source: str


CFM56_7B_REFERENCE = [
    ReferenceMetric(
        key="sea_level_static_thrust_lbf_min",
        zh_name="海平面靜推力下限",
        english_name="Sea-level static thrust lower bound",
        value=19500.0,
        unit="lbf",
        tolerance=None,
        note="CFM56-7B 系列依型號不同約為 19,500 到 27,300 lbf。pyCycle 範例設計點是巡航條件，不可直接等同靜推力。",
        source="Reference_sources/aircraft-commerce-cfm56-7b-specs.pdf",
    ),
    ReferenceMetric(
        key="sea_level_static_thrust_lbf_max",
        zh_name="海平面靜推力上限",
        english_name="Sea-level static thrust upper bound",
        value=27300.0,
        unit="lbf",
        tolerance=None,
        note="作為等級檢查，不作為單一設計點誤差。",
        source="Reference_sources/aircraft-commerce-cfm56-7b-specs.pdf",
    ),
    ReferenceMetric(
        key="bypass_ratio",
        zh_name="旁通比",
        english_name="Bypass ratio",
        value=5.1,
        unit="-",
        tolerance=0.35,
        note="pyCycle high_bypass_turbofan 範例設計 BPR 約 5.105，可直接做等級比對。",
        source="Reference_sources/source_manifest.md",
    ),
    ReferenceMetric(
        key="overall_pressure_ratio",
        zh_name="總壓比",
        english_name="Overall pressure ratio",
        value=32.7,
        unit="-",
        tolerance=4.0,
        note="公開資料常列 CFM56-7B OPR 約 32.7；pyCycle 範例 OPR 受範例設計假設影響。",
        source="Reference_sources/aircraft-commerce-cfm56-7b-specs.pdf",
    ),
    ReferenceMetric(
        key="fan_diameter_in",
        zh_name="風扇直徑",
        english_name="Fan diameter",
        value=61.0,
        unit="in",
        tolerance=None,
        note="目前 pyCycle 範例不直接輸出風扇直徑，保留在 app 中作來源對照。",
        source="Reference_sources/aircraft-commerce-cfm56-7b-specs.pdf",
    ),
]


def reference_by_key() -> dict[str, ReferenceMetric]:
    return {metric.key: metric for metric in CFM56_7B_REFERENCE}
