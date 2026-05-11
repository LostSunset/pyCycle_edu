from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EngineCase:
    engine_name: str = "CFM56-7B 教學近似案例"
    bypass_ratio: float = 5.1
    overall_pressure_ratio: float = 32.7
    turbine_inlet_temperature_k: float = 1680.0
    altitude_ft: float = 35000.0
    mach: float = 0.78
    mass_flow_lb_s: float = 780.0


@dataclass(slots=True)
class EngineResult:
    net_thrust_lbf: float
    tsfc_lb_lbf_hr: float
    fuel_flow_lb_hr: float
    fan_pressure_ratio: float
    core_exit_temp_k: float
    propulsive_efficiency: float
    thermal_efficiency: float


def estimate_reference_result(case: EngineCase) -> EngineResult:
    """Teaching placeholder until the UI is wired to an actual pyCycle problem."""
    bpr_effect = 1.0 + (case.bypass_ratio - 5.0) * 0.045
    opr_effect = 1.0 + (case.overall_pressure_ratio - 30.0) * 0.008
    tit_effect = 1.0 + (case.turbine_inlet_temperature_k - 1600.0) * 0.00035
    altitude_effect = max(0.62, 1.0 - case.altitude_ft / 110000.0)
    mach_effect = 1.0 - max(0.0, case.mach - 0.75) * 0.09

    net_thrust = (
        case.mass_flow_lb_s
        * 31.5
        * bpr_effect
        * opr_effect
        * tit_effect
        * altitude_effect
        * mach_effect
    )
    tsfc = max(0.46, 0.63 - (case.bypass_ratio - 4.5) * 0.025 - (case.overall_pressure_ratio - 28.0) * 0.002)
    fuel_flow = net_thrust * tsfc

    return EngineResult(
        net_thrust_lbf=net_thrust,
        tsfc_lb_lbf_hr=tsfc,
        fuel_flow_lb_hr=fuel_flow,
        fan_pressure_ratio=1.55 + (case.bypass_ratio - 5.0) * 0.018,
        core_exit_temp_k=780.0 + (case.turbine_inlet_temperature_k - 1600.0) * 0.16,
        propulsive_efficiency=min(0.83, 0.70 + case.bypass_ratio * 0.018),
        thermal_efficiency=min(0.52, 0.34 + case.overall_pressure_ratio * 0.004),
    )
