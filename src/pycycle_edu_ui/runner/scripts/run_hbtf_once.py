from __future__ import annotations

import sys
import time
import os
from pathlib import Path

import openmdao.api as om

from high_bypass_turbofan import MPhbtf, viewer


def env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return float(raw)


def main() -> int:
    mach = env_float("PYCYCLE_INPUT_MACH", 0.8)
    altitude_ft = env_float("PYCYCLE_INPUT_ALTITUDE_FT", 35000.0)
    t4_max = env_float("PYCYCLE_INPUT_T4_MAX_DEG_R", 2857.0)
    fn_target = env_float("PYCYCLE_INPUT_FN_TARGET_LBF", 5900.0)
    bpr = env_float("PYCYCLE_INPUT_BPR", 5.105)
    fan_pr = env_float("PYCYCLE_INPUT_FAN_PR", 1.685)
    lpc_pr = env_float("PYCYCLE_INPUT_LPC_PR", 1.935)
    hpc_pr = env_float("PYCYCLE_INPUT_HPC_PR", 9.369)
    percent_thrust = env_float("PYCYCLE_INPUT_PERCENT_THRUST", 0.8)

    output = Path("hbtf_view.out")
    prob = om.Problem()
    prob.model = MPhbtf()
    prob.setup()

    prob.set_val("DESIGN.fan.PR", fan_pr)
    prob.set_val("DESIGN.fan.eff", 0.8948)
    prob.set_val("DESIGN.lpc.PR", lpc_pr)
    prob.set_val("DESIGN.lpc.eff", 0.9243)
    prob.set_val("DESIGN.hpc.PR", hpc_pr)
    prob.set_val("DESIGN.hpc.eff", 0.8707)
    prob.set_val("DESIGN.hpt.eff", 0.8888)
    prob.set_val("DESIGN.lpt.eff", 0.8996)
    prob.set_val("DESIGN.splitter.BPR", bpr)
    prob.set_val("DESIGN.fc.alt", altitude_ft, units="ft")
    prob.set_val("DESIGN.fc.MN", mach)
    prob.set_val("DESIGN.T4_MAX", t4_max, units="degR")
    prob.set_val("DESIGN.Fn_DES", fn_target, units="lbf")
    prob.set_val("OD_full_pwr.T4_MAX", t4_max, units="degR")
    prob.set_val("OD_part_pwr.PC", percent_thrust)

    prob["DESIGN.balance.FAR"] = 0.025
    prob["DESIGN.balance.W"] = 100.0
    prob["DESIGN.balance.lpt_PR"] = 4.0
    prob["DESIGN.balance.hpt_PR"] = 3.0
    prob["DESIGN.fc.balance.Pt"] = 5.2
    prob["DESIGN.fc.balance.Tt"] = 440.0

    for pt in ["OD_full_pwr", "OD_part_pwr"]:
        prob[pt + ".balance.FAR"] = 0.02467
        prob[pt + ".balance.W"] = 300
        prob[pt + ".balance.BPR"] = bpr
        prob[pt + ".balance.lp_Nmech"] = 5000
        prob[pt + ".balance.hp_Nmech"] = 15000
        prob[pt + ".hpt.PR"] = 3.0
        prob[pt + ".lpt.PR"] = 4.0
        prob[pt + ".fan.map.RlineMap"] = 2.0
        prob[pt + ".lpc.map.RlineMap"] = 2.0
        prob[pt + ".hpc.map.RlineMap"] = 2.0
        prob[pt + ".fc.MN"] = mach
        prob[pt + ".fc.alt"] = altitude_ft

    prob.set_solver_print(level=-1)
    started = time.time()
    prob.run_model()

    with output.open("w", encoding="utf-8") as stream:
        viewer(prob, "DESIGN", file=stream)
        viewer(prob, "OD_part_pwr", file=stream)

    print(f"Wrote {output.resolve()}")
    print(f"Run time {time.time() - started:.2f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
