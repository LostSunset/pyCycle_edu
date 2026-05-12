from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from pycycle_edu_ui.paths import PROJECT_ROOT, UPSTREAM_PYCYCLE


SIMPLE_TURBOJET_DIR = PROJECT_ROOT / "tutorials" / "simple_turbojet"
SIMPLE_TURBOJET_SCRIPT = Path(__file__).resolve().parent / "scripts" / "run_simple_turbojet_once.py"
SIMPLE_TURBOJET_OUT_DIR = SIMPLE_TURBOJET_DIR / "simple_turbojet_out"

SUMMARY_RE = re.compile(
    r"^\s*(?P<mach>-?\d+\.\d+)\s+"
    r"(?P<alt>-?\d+\.\d+)\s+"
    r"(?P<w>-?\d+\.\d+)\s+"
    r"(?P<fn>-?\d+\.\d+)\s+"
    r"(?P<fg>-?\d+\.\d+)\s+"
    r"(?P<fram>-?\d+\.\d+)\s+"
    r"(?P<opr>-?\d+\.\d+)\s+"
    r"(?P<tsfc>-?\d+\.\d+)\s*$"
)


@dataclass(slots=True)
class SimpleTurbojetInputs:
    altitude_ft: float = 0.0
    mach: float = 0.000001
    fn_target_lbf: float = 11800.0
    t4_target_deg_r: float = 2370.0
    compressor_pr: float = 13.5
    compressor_efficiency: float = 0.83
    turbine_efficiency: float = 0.86


@dataclass(slots=True)
class SimpleTurbojetPoint:
    point: str
    mach: float
    altitude_ft: float
    mass_flow_lbm_s: float
    net_thrust_lbf: float
    gross_thrust_lbf: float
    ram_drag_lbf: float
    overall_pressure_ratio: float
    tsfc: float


@dataclass(slots=True)
class SimpleTurbojetRunResult:
    ok: bool
    output_dir: Path
    raw_output: Path
    bilingual_text_report: Path
    bilingual_pdf_report: Path
    artifacts: list[Path]
    points: list[SimpleTurbojetPoint]
    inputs: SimpleTurbojetInputs
    elapsed_seconds: float
    stdout: str
    stderr: str
    error: str | None = None


def parse_summary_rows(text: str) -> list[SimpleTurbojetPoint]:
    points: list[SimpleTurbojetPoint] = []
    current_point = ""
    waiting_for_summary = False

    for line in text.splitlines():
        if "POINT:" in line:
            current_point = line.split("POINT:", 1)[1].strip()
            waiting_for_summary = False
            continue
        if "Mach" in line and "TSFC" in line:
            waiting_for_summary = True
            continue
        if not waiting_for_summary:
            continue
        match = SUMMARY_RE.match(line)
        if match is None:
            continue
        values = {key: float(value) for key, value in match.groupdict().items()}
        points.append(
            SimpleTurbojetPoint(
                point=current_point,
                mach=values["mach"],
                altitude_ft=values["alt"],
                mass_flow_lbm_s=values["w"],
                net_thrust_lbf=values["fn"],
                gross_thrust_lbf=values["fg"],
                ram_drag_lbf=values["fram"],
                overall_pressure_ratio=values["opr"],
                tsfc=values["tsfc"],
            )
        )
        waiting_for_summary = False
    return points


def run_simple_turbojet(inputs: SimpleTurbojetInputs | None = None, timeout_seconds: int = 240) -> SimpleTurbojetRunResult:
    from pycycle_edu_ui.simple_turbojet_report import (
        build_bilingual_report_text,
        save_bilingual_report_pdf,
        save_bilingual_map_pdfs,
    )

    inputs = inputs or SimpleTurbojetInputs()
    SIMPLE_TURBOJET_OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_output = SIMPLE_TURBOJET_OUT_DIR / "simple_turbojet_raw_output.txt"
    bilingual_text_report = SIMPLE_TURBOJET_OUT_DIR / "simple_turbojet_bilingual_report.txt"
    bilingual_pdf_report = SIMPLE_TURBOJET_OUT_DIR / "simple_turbojet_bilingual_report.pdf"

    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    env.setdefault("OPENMDAO_REPORTS", str(SIMPLE_TURBOJET_OUT_DIR))
    env["PYTHONPATH"] = (
        str(UPSTREAM_PYCYCLE)
        + os.pathsep
        + str(SIMPLE_TURBOJET_DIR)
        + os.pathsep
        + env.get("PYTHONPATH", "")
    )
    env.update(
        {
            "PYCYCLE_SIMPLE_TURBOJET_ALTITUDE_FT": str(inputs.altitude_ft),
            "PYCYCLE_SIMPLE_TURBOJET_MACH": str(inputs.mach),
            "PYCYCLE_SIMPLE_TURBOJET_FN_TARGET_LBF": str(inputs.fn_target_lbf),
            "PYCYCLE_SIMPLE_TURBOJET_T4_TARGET_DEG_R": str(inputs.t4_target_deg_r),
            "PYCYCLE_SIMPLE_TURBOJET_COMPRESSOR_PR": str(inputs.compressor_pr),
            "PYCYCLE_SIMPLE_TURBOJET_COMPRESSOR_EFF": str(inputs.compressor_efficiency),
            "PYCYCLE_SIMPLE_TURBOJET_TURBINE_EFF": str(inputs.turbine_efficiency),
        }
    )

    started = time.time()
    try:
        completed = subprocess.run(
            [sys.executable, str(SIMPLE_TURBOJET_SCRIPT)],
            cwd=SIMPLE_TURBOJET_OUT_DIR,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        raw_output.write_text(stdout + "\n" + stderr, encoding="utf-8", errors="replace")
        return SimpleTurbojetRunResult(
            ok=False,
            output_dir=SIMPLE_TURBOJET_OUT_DIR,
            raw_output=raw_output,
            bilingual_text_report=bilingual_text_report,
            bilingual_pdf_report=bilingual_pdf_report,
            artifacts=[],
            points=[],
            inputs=inputs,
            elapsed_seconds=time.time() - started,
            stdout=stdout,
            stderr=stderr,
            error=f"simple_turbojet timed out after {timeout_seconds} seconds.",
        )

    stdout = completed.stdout
    stderr = completed.stderr
    raw_output.write_text(stdout + ("\n" + stderr if stderr else ""), encoding="utf-8", errors="replace")
    points = parse_summary_rows(stdout)
    save_bilingual_map_pdfs(SIMPLE_TURBOJET_OUT_DIR, points)
    save_bilingual_map_pdfs(SIMPLE_TURBOJET_DIR, points)
    artifacts = sorted(SIMPLE_TURBOJET_OUT_DIR.glob("*.pdf"))
    report_text = build_bilingual_report_text(inputs, points, [path.name for path in artifacts], time.time() - started)
    bilingual_text_report.write_text(report_text, encoding="utf-8")
    save_bilingual_report_pdf(bilingual_pdf_report, report_text)
    artifacts = sorted(SIMPLE_TURBOJET_OUT_DIR.glob("*.pdf"))

    ok = completed.returncode == 0 and bool(points)
    return SimpleTurbojetRunResult(
        ok=ok,
        output_dir=SIMPLE_TURBOJET_OUT_DIR,
        raw_output=raw_output,
        bilingual_text_report=bilingual_text_report,
        bilingual_pdf_report=bilingual_pdf_report,
        artifacts=artifacts,
        points=points,
        inputs=inputs,
        elapsed_seconds=time.time() - started,
        stdout=stdout,
        stderr=stderr,
        error=None if ok else f"simple_turbojet exited with code {completed.returncode}; parsed {len(points)} points.",
    )
