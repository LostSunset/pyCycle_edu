from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from pycycle_edu_ui.paths import RUNS_DIR, UPSTREAM_PYCYCLE


SUMMARY_RE = re.compile(
    r"^\s*(?P<mach>-?\d+\.\d+)\s+"
    r"(?P<alt>-?\d+\.\d+)\s+"
    r"(?P<w>-?\d+\.\d+)\s+"
    r"(?P<fn>-?\d+\.\d+)\s+"
    r"(?P<fg>-?\d+\.\d+)\s+"
    r"(?P<fram>-?\d+\.\d+)\s+"
    r"(?P<opr>-?\d+\.\d+)\s+"
    r"(?P<tsfc>-?\d+\.\d+)\s+"
    r"(?P<bpr>-?\d+\.\d+)\s*$"
)


@dataclass(slots=True)
class PerformancePoint:
    point: str
    mach: float
    altitude_ft: float
    mass_flow_lbm_s: float
    net_thrust_lbf: float
    gross_thrust_lbf: float
    ram_drag_lbf: float
    overall_pressure_ratio: float
    tsfc: float
    bypass_ratio: float


@dataclass(slots=True)
class EngineInputs:
    mach: float = 0.8
    altitude_ft: float = 35000.0
    t4_max_deg_r: float = 2857.0
    fn_target_lbf: float = 5900.0
    bypass_ratio: float = 5.105
    fan_pressure_ratio: float = 1.685
    lpc_pressure_ratio: float = 1.935
    hpc_pressure_ratio: float = 9.369
    percent_thrust: float = 0.8

    def to_env(self) -> dict[str, str]:
        return {
            "PYCYCLE_INPUT_MACH": str(self.mach),
            "PYCYCLE_INPUT_ALTITUDE_FT": str(self.altitude_ft),
            "PYCYCLE_INPUT_T4_MAX_DEG_R": str(self.t4_max_deg_r),
            "PYCYCLE_INPUT_FN_TARGET_LBF": str(self.fn_target_lbf),
            "PYCYCLE_INPUT_BPR": str(self.bypass_ratio),
            "PYCYCLE_INPUT_FAN_PR": str(self.fan_pressure_ratio),
            "PYCYCLE_INPUT_LPC_PR": str(self.lpc_pressure_ratio),
            "PYCYCLE_INPUT_HPC_PR": str(self.hpc_pressure_ratio),
            "PYCYCLE_INPUT_PERCENT_THRUST": str(self.percent_thrust),
        }


@dataclass(slots=True)
class PyCycleRunResult:
    ok: bool
    run_dir: Path
    english_report: Path
    points: list[PerformancePoint]
    inputs: EngineInputs
    elapsed_seconds: float
    stdout: str
    stderr: str
    error: str | None = None


def run_high_bypass_turbofan(inputs: EngineInputs | None = None) -> PyCycleRunResult:
    inputs = inputs or EngineInputs()
    run_dir = RUNS_DIR / datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    script = Path(__file__).resolve().parent / "scripts" / "run_hbtf_once.py"
    env = os.environ.copy()
    example_cycles = UPSTREAM_PYCYCLE / "example_cycles"
    env["PYTHONPATH"] = (
        str(UPSTREAM_PYCYCLE)
        + os.pathsep
        + str(example_cycles)
        + os.pathsep
        + env.get("PYTHONPATH", "")
    )
    env.setdefault("OPENMDAO_REPORTS", "0")
    env.update(inputs.to_env())

    english_report = run_dir / "hbtf_view.out"
    started = datetime.now()
    try:
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=run_dir,
            env=env,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return PyCycleRunResult(
            ok=False,
            run_dir=run_dir,
            english_report=english_report,
            points=[],
            inputs=inputs,
            elapsed_seconds=(datetime.now() - started).total_seconds(),
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            error="pyCycle runner timed out after 180 seconds.",
        )
    if completed.returncode != 0:
        return PyCycleRunResult(
            ok=False,
            run_dir=run_dir,
            english_report=english_report,
            points=[],
            inputs=inputs,
            elapsed_seconds=(datetime.now() - started).total_seconds(),
            stdout=completed.stdout,
            stderr=completed.stderr,
            error=f"pyCycle process exited with code {completed.returncode}",
        )

    if not english_report.exists():
        return PyCycleRunResult(
            ok=False,
            run_dir=run_dir,
            english_report=english_report,
            points=[],
            inputs=inputs,
            elapsed_seconds=(datetime.now() - started).total_seconds(),
            stdout=completed.stdout,
            stderr=completed.stderr,
            error="pyCycle finished but hbtf_view.out was not generated.",
        )

    points = parse_hbtf_report(english_report.read_text(encoding="utf-8", errors="replace"))
    return PyCycleRunResult(
        ok=bool(points),
        run_dir=run_dir,
        english_report=english_report,
        points=points,
        inputs=inputs,
        elapsed_seconds=(datetime.now() - started).total_seconds(),
        stdout=completed.stdout,
        stderr=completed.stderr,
        error=None if points else "hbtf_view.out generated, but no performance rows were parsed.",
    )


def parse_hbtf_report(text: str) -> list[PerformancePoint]:
    points: list[PerformancePoint] = []
    current_point = ""
    waiting_for_summary = False

    for line in text.splitlines():
        if "POINT:" in line:
            current_point = line.split("POINT:", 1)[1].strip()
            waiting_for_summary = False
            continue
        if "Mach" in line and "TSFC" in line and "BPR" in line:
            waiting_for_summary = True
            continue
        if not waiting_for_summary:
            continue
        match = SUMMARY_RE.match(line)
        if not match:
            continue
        data = {key: float(value) for key, value in match.groupdict().items()}
        points.append(
            PerformancePoint(
                point=current_point,
                mach=data["mach"],
                altitude_ft=data["alt"],
                mass_flow_lbm_s=data["w"],
                net_thrust_lbf=data["fn"],
                gross_thrust_lbf=data["fg"],
                ram_drag_lbf=data["fram"],
                overall_pressure_ratio=data["opr"],
                tsfc=data["tsfc"],
                bypass_ratio=data["bpr"],
            )
        )
        waiting_for_summary = False
    return points
