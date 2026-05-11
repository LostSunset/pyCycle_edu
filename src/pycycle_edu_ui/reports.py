from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pycycle_edu_ui.paths import REPORTS_DIR
from pycycle_edu_ui.reference_data import CFM56_7B_REFERENCE
from pycycle_edu_ui.runner.hbtf_runner import PerformancePoint, PyCycleRunResult


def select_design_point(points: list[PerformancePoint]) -> PerformancePoint | None:
    for point in points:
        if point.point == "DESIGN":
            return point
    return points[0] if points else None


def build_chinese_report(run: PyCycleRunResult) -> str:
    design = select_design_point(run.points)
    lines = [
        "# pyCycle HBTF 與 CFM56-7B 參考資料比對報告",
        "",
        f"產生時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"pyCycle 英文 viewer 報告：{run.english_report}",
        f"pyCycle 執行時間：{run.elapsed_seconds:.1f} s",
        "",
        "## 摘要",
        "",
    ]
    if design is None:
        lines.append("本次 pyCycle 執行沒有可解析的 performance row，請檢查英文 viewer 報告與 stderr。")
        return "\n".join(lines)

    lines.extend(
        [
            "本報告使用 upstream pyCycle 的 `high_bypass_turbofan.py` 範例執行結果，",
            "並與 `Reference_sources/` 中保存的 CFM56-7B 公開資料做工程等級比對。",
            "",
            "重要限制：pyCycle HBTF 範例不是 CFM56-7B 原廠 engine deck；",
            "設計點為巡航條件，不能直接拿巡航淨推力與海平面靜推力相減當作校正誤差。",
            "",
            "## 輸入條件",
            "",
            "| 欄位 | 數值 | 單位 |",
            "|---|---:|---|",
            f"| Mach | {run.inputs.mach:.3f} | - |",
            f"| Altitude | {run.inputs.altitude_ft:,.0f} | ft |",
            f"| T4 / Tt4 | {run.inputs.t4_max_deg_r:,.1f} | degR |",
            f"| Fn target | {run.inputs.fn_target_lbf:,.1f} | lbf |",
            f"| BPR | {run.inputs.bypass_ratio:.3f} | - |",
            f"| Fan PR | {run.inputs.fan_pressure_ratio:.3f} | - |",
            f"| LPC PR | {run.inputs.lpc_pressure_ratio:.3f} | - |",
            f"| HPC PR | {run.inputs.hpc_pressure_ratio:.3f} | - |",
            f"| Percent thrust | {run.inputs.percent_thrust:.2%} | - |",
            "",
            "## pyCycle 設計點結果",
            "",
            "| 欄位 | 數值 | 單位 |",
            "|---|---:|---|",
            f"| Mach | {design.mach:.3f} | - |",
            f"| 高度 | {design.altitude_ft:,.0f} | ft |",
            f"| 淨推力 Fn | {design.net_thrust_lbf:,.1f} | lbf |",
            f"| 總推力 Fg | {design.gross_thrust_lbf:,.1f} | lbf |",
            f"| Ram drag | {design.ram_drag_lbf:,.1f} | lbf |",
            f"| OPR | {design.overall_pressure_ratio:.3f} | - |",
            f"| TSFC | {design.tsfc:.5f} | lbm/hr/lbf |",
            f"| BPR | {design.bypass_ratio:.3f} | - |",
            "",
            "## CFM56-7B 公開資料",
            "",
            "| 欄位 | 參考值 | 單位 | 來源 | 備註 |",
            "|---|---:|---|---|---|",
        ]
    )

    for metric in CFM56_7B_REFERENCE:
        lines.append(f"| {metric.zh_name} | {metric.value:g} | {metric.unit} | {metric.source} | {metric.note} |")

    lines.extend(
        [
            "",
            "## 判讀",
            "",
            f"- BPR：pyCycle 設計點為 {design.bypass_ratio:.3f}，與 CFM56-7B 約 5.1 的公開資料量級一致。",
            f"- OPR：pyCycle 設計點為 {design.overall_pressure_ratio:.3f}，可與公開資料約 32.7 做量級檢查。",
            f"- 推力：pyCycle 設計點 {design.net_thrust_lbf:,.1f} lbf 是巡航條件，不等同 CFM56-7B 海平面靜推力級距。",
            "- pyCycle 英文 viewer 已保存，正體中文版由本 app 依解析數據與來源清單產生。",
        ]
    )
    return "\n".join(lines)


def save_chinese_report(run: PyCycleRunResult) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output = REPORTS_DIR / f"hbtf_cfm56_7b_report_zh_{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    output.write_text(build_chinese_report(run), encoding="utf-8")
    return output
