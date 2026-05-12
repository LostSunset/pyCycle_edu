from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from pycycle_edu_ui.runner.simple_turbojet_runner import SimpleTurbojetInputs, SimpleTurbojetPoint


def build_bilingual_report_text(
    inputs: SimpleTurbojetInputs,
    points: list[SimpleTurbojetPoint],
    artifacts: list[str],
    elapsed_seconds: float,
) -> str:
    lines = [
        "# Simple Turbojet Report / 簡單渦輪噴射報告",
        "",
        f"Generated at / 產生時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Elapsed time / 執行時間: {elapsed_seconds:.2f} s",
        "",
        "## Inputs / 輸入條件",
        "",
        "| Field / 欄位 | Value / 數值 | Unit / 單位 |",
        "|---|---:|---|",
        f"| Mach / 馬赫數 | {inputs.mach:.6f} | - |",
        f"| Altitude / 高度 | {inputs.altitude_ft:,.1f} | ft |",
        f"| Target net thrust Fn / 目標淨推力 Fn | {inputs.fn_target_lbf:,.1f} | lbf |",
        f"| T4 target / T4 目標 | {inputs.t4_target_deg_r:,.1f} | degR |",
        f"| Compressor pressure ratio / 壓縮機壓比 | {inputs.compressor_pr:.3f} | - |",
        f"| Compressor efficiency / 壓縮機效率 | {inputs.compressor_efficiency:.3f} | - |",
        f"| Turbine efficiency / 渦輪效率 | {inputs.turbine_efficiency:.3f} | - |",
        "",
        "## Performance Summary / 性能摘要",
        "",
        "| Point / 工作點 | Mach / 馬赫數 | Altitude / 高度 ft | W / 質量流率 lbm/s | Net thrust Fn / 淨推力 Fn lbf | Gross thrust Fg / 總推力 Fg lbf | OPR / 總壓比 | TSFC / 比油耗 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    if points:
        for point in points:
            lines.append(
                f"| {point.point} | {point.mach:.5f} | {point.altitude_ft:,.1f} | "
                f"{point.mass_flow_lbm_s:,.3f} | {point.net_thrust_lbf:,.1f} | "
                f"{point.gross_thrust_lbf:,.1f} | {point.overall_pressure_ratio:.3f} | {point.tsfc:.5f} |"
            )
    else:
        lines.append("| No parsed points / 沒有解析到工作點 | - | - | - | - | - | - | - |")

    lines.extend(
        [
            "",
            "## Artifacts / 輸出檔案",
            "",
        ]
    )
    if artifacts:
        lines.extend(f"- {artifact}" for artifact in artifacts)
    else:
        lines.append("- No PDF artifacts generated / 尚未產生 PDF 輸出")

    lines.extend(
        [
            "",
            "## Notes / 備註",
            "",
            "- This GUI uses the repository simple turbojet case, not a calibrated production engine deck. / 本 GUI 使用 repository simple turbojet 案例，不是已校正的量產發動機 deck。",
            "- English is shown first, followed by Traditional Chinese. / 顯示順序為英文在前，正體中文在後。",
        ]
    )
    return "\n".join(lines)


def save_bilingual_report_pdf(output: Path, report_text: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    font_name = _register_cjk_font()
    styles = getSampleStyleSheet()
    for style_name in ["Title", "Heading1", "Heading2", "BodyText"]:
        styles[style_name].fontName = font_name

    story = []
    for line in report_text.splitlines():
        if not line.strip():
            story.append(Spacer(1, 8))
            continue
        if line.startswith("# "):
            story.append(Paragraph(line[2:], styles["Title"]))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], styles["Heading2"]))
        elif line.startswith("|"):
            story.append(Paragraph(_escape(line), styles["BodyText"]))
        elif line.startswith("- "):
            story.append(Paragraph(_escape(line), styles["BodyText"]))
        else:
            story.append(Paragraph(_escape(line), styles["BodyText"]))
    SimpleDocTemplate(str(output), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36).build(story)


def save_bilingual_map_pdfs(output_dir: Path, points: list[SimpleTurbojetPoint]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    font_name = _matplotlib_cjk_font()
    if font_name:
        plt.rcParams["font.sans-serif"] = [font_name, "Microsoft JhengHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    labels = [point.point for point in points] or ["DESIGN"]
    opr = [point.overall_pressure_ratio for point in points] or [0.0]
    tsfc = [point.tsfc for point in points] or [0.0]
    thrust = [point.net_thrust_lbf for point in points] or [0.0]

    _save_metric_pdf(
        output_dir / "DESIGN.comp.pdf",
        "Compressor Map Summary / 壓縮機圖摘要",
        "Point / 工作點",
        "Overall Pressure Ratio / 總壓比",
        labels,
        opr,
        "#3B6EA8",
    )
    _save_metric_pdf(
        output_dir / "DESIGN.turb.pdf",
        "Turbine Map Summary / 渦輪圖摘要",
        "Net thrust Fn / 淨推力 Fn",
        "TSFC / 比油耗",
        [f"{value:,.0f}" for value in thrust],
        tsfc,
        "#A85F3B",
    )


def _save_metric_pdf(
    output: Path,
    title: str,
    xlabel: str,
    ylabel: str,
    labels: list[str],
    values: list[float],
    color: str,
) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.plot(range(len(labels)), values, marker="o", linewidth=2.5, color=color)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.28)
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def _register_cjk_font() -> str:
    candidates = [
        Path("C:/Windows/Fonts/msjh.ttc"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/mingliu.ttc"),
    ]
    for path in candidates:
        if path.exists():
            pdfmetrics.registerFont(TTFont("PyCycleGuiCJK", str(path)))
            return "PyCycleGuiCJK"
    return "Helvetica"


def _matplotlib_cjk_font() -> str:
    candidates = ["Microsoft JhengHei", "Microsoft YaHei", "SimHei"]
    return candidates[0]


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
