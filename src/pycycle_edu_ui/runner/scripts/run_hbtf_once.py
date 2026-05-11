from __future__ import annotations

import sys
import time
from pathlib import Path

import openmdao.api as om

from high_bypass_turbofan import MPhbtf, viewer


def main() -> int:
    output = Path("hbtf_view.out")
    prob = om.Problem()
    prob.model = MPhbtf()
    prob.setup()

    prob.set_val("DESIGN.fan.PR", 1.685)
    prob.set_val("DESIGN.fan.eff", 0.8948)
    prob.set_val("DESIGN.lpc.PR", 1.935)
    prob.set_val("DESIGN.lpc.eff", 0.9243)
    prob.set_val("DESIGN.hpc.PR", 9.369)
    prob.set_val("DESIGN.hpc.eff", 0.8707)
    prob.set_val("DESIGN.hpt.eff", 0.8888)
    prob.set_val("DESIGN.lpt.eff", 0.8996)
    prob.set_val("DESIGN.fc.alt", 35000.0, units="ft")
    prob.set_val("DESIGN.fc.MN", 0.8)
    prob.set_val("DESIGN.T4_MAX", 2857, units="degR")
    prob.set_val("DESIGN.Fn_DES", 5900.0, units="lbf")
    prob.set_val("OD_full_pwr.T4_MAX", 2857, units="degR")
    prob.set_val("OD_part_pwr.PC", 0.8)

    prob["DESIGN.balance.FAR"] = 0.025
    prob["DESIGN.balance.W"] = 100.0
    prob["DESIGN.balance.lpt_PR"] = 4.0
    prob["DESIGN.balance.hpt_PR"] = 3.0
    prob["DESIGN.fc.balance.Pt"] = 5.2
    prob["DESIGN.fc.balance.Tt"] = 440.0

    for pt in ["OD_full_pwr", "OD_part_pwr"]:
        prob[pt + ".balance.FAR"] = 0.02467
        prob[pt + ".balance.W"] = 300
        prob[pt + ".balance.BPR"] = 5.105
        prob[pt + ".balance.lp_Nmech"] = 5000
        prob[pt + ".balance.hp_Nmech"] = 15000
        prob[pt + ".hpt.PR"] = 3.0
        prob[pt + ".lpt.PR"] = 4.0
        prob[pt + ".fan.map.RlineMap"] = 2.0
        prob[pt + ".lpc.map.RlineMap"] = 2.0
        prob[pt + ".hpc.map.RlineMap"] = 2.0
        prob[pt + ".fc.MN"] = 0.8
        prob[pt + ".fc.alt"] = 35000.0

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
