from __future__ import annotations

import contextlib
import os
import sys
import time

import matplotlib

matplotlib.use("Agg")

import openmdao.api as om

from simple_turbojet import MPTurbojet, comprehensive_performance_summary, viewer


def env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return float(raw)


def main() -> int:
    altitude_ft = env_float("PYCYCLE_SIMPLE_TURBOJET_ALTITUDE_FT", 0.0)
    mach = env_float("PYCYCLE_SIMPLE_TURBOJET_MACH", 0.000001)
    fn_target = env_float("PYCYCLE_SIMPLE_TURBOJET_FN_TARGET_LBF", 11800.0)
    t4_target = env_float("PYCYCLE_SIMPLE_TURBOJET_T4_TARGET_DEG_R", 2370.0)
    compressor_pr = env_float("PYCYCLE_SIMPLE_TURBOJET_COMPRESSOR_PR", 13.5)
    compressor_eff = env_float("PYCYCLE_SIMPLE_TURBOJET_COMPRESSOR_EFF", 0.83)
    turbine_eff = env_float("PYCYCLE_SIMPLE_TURBOJET_TURBINE_EFF", 0.86)

    prob = om.Problem()
    mp_turbojet = prob.model = MPTurbojet()
    prob.setup(check=False)

    prob.set_val("DESIGN.fc.alt", altitude_ft, units="ft")
    prob.set_val("DESIGN.fc.MN", mach)
    prob.set_val("DESIGN.balance.Fn_target", fn_target, units="lbf")
    prob.set_val("DESIGN.balance.T4_target", t4_target, units="degR")
    prob.set_val("DESIGN.comp.PR", compressor_pr)
    prob.set_val("DESIGN.comp.eff", compressor_eff)
    prob.set_val("DESIGN.turb.eff", turbine_eff)

    prob["DESIGN.balance.FAR"] = 0.0175506829934
    prob["DESIGN.balance.W"] = 168.453135137
    prob["DESIGN.balance.turb_PR"] = 4.46138725662
    prob["DESIGN.fc.balance.Pt"] = 14.6955113159
    prob["DESIGN.fc.balance.Tt"] = 518.665288153

    for pt in mp_turbojet.od_pts:
        prob[pt + ".balance.W"] = 166.073
        prob[pt + ".balance.FAR"] = 0.01680
        prob[pt + ".balance.Nmech"] = 8197.38
        prob[pt + ".fc.balance.Pt"] = 15.703
        prob[pt + ".fc.balance.Tt"] = 558.31
        prob[pt + ".turb.PR"] = 4.6690

    prob.set_solver_print(level=-1)
    prob.set_solver_print(level=2, depth=1)
    started = time.time()
    prob.run_model()

    for pt in ["DESIGN"] + mp_turbojet.od_pts:
        viewer(prob, pt)
        comprehensive_performance_summary(prob, pt)

    print()
    print(f"time {time.time() - started:.2f}")
    return 0


if __name__ == "__main__":
    with contextlib.redirect_stderr(sys.stderr):
        raise SystemExit(main())
