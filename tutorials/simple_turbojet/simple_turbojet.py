"""Simple Turbojet tutorial — pyCycle model + PySide6 GUI.

Running this file directly launches a PySide6 GUI. All artefacts (summary
text, charts) are written to the directory that contains this script.

The model classes (`Turbojet`, `MPTurbojet`) and helper functions
(`viewer`, `comprehensive_performance_summary`, `map_plots`,
`plot_ts_diagram`, `plot_pressure_enthalpy_diagram`) are kept intact so
that other entry points (e.g. ``src/pycycle_edu_ui/runner``) can still
import them.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

# Pick a Qt backend for the GUI mode, but never override an explicit
# MPLBACKEND (the headless runner sets it to "Agg").
if not os.environ.get("MPLBACKEND"):
    try:
        matplotlib.use("QtAgg")
    except Exception:  # pragma: no cover - matplotlib backend selection
        pass

import matplotlib.pyplot as plt

# 設定中文字體
matplotlib.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "Arial Unicode MS",
    "DejaVu Sans",
]
matplotlib.rcParams["axes.unicode_minus"] = False

import openmdao.api as om
import pycycle.api as pyc


# ---------------------------------------------------------------------------
# pyCycle model
# ---------------------------------------------------------------------------


class Turbojet(pyc.Cycle):
    def setup(self):
        USE_TABULAR = True

        if USE_TABULAR:
            self.options["thermo_method"] = "TABULAR"
            self.options["thermo_data"] = pyc.AIR_JETA_TAB_SPEC
            FUEL_TYPE = "FAR"
        else:
            self.options["thermo_method"] = "CEA"
            self.options["thermo_data"] = pyc.species_data.janaf
            FUEL_TYPE = "Jet-A(g)"

        design = self.options["design"]

        # Add engine elements
        self.add_subsystem("fc", pyc.FlightConditions())
        self.add_subsystem("inlet", pyc.Inlet())
        self.add_subsystem(
            "comp",
            pyc.Compressor(map_data=pyc.AXI5, map_extrap=True),
            promotes_inputs=["Nmech"],
        )
        self.add_subsystem("burner", pyc.Combustor(fuel_type=FUEL_TYPE))
        self.add_subsystem(
            "turb",
            pyc.Turbine(map_data=pyc.LPT2269),
            promotes_inputs=["Nmech"],
        )
        self.add_subsystem("nozz", pyc.Nozzle(nozzType="CD", lossCoef="Cv"))
        self.add_subsystem("shaft", pyc.Shaft(num_ports=2), promotes_inputs=["Nmech"])
        self.add_subsystem("perf", pyc.Performance(num_nozzles=1, num_burners=1))

        # Connect flow stations
        self.pyc_connect_flow("fc.Fl_O", "inlet.Fl_I", connect_w=False)
        self.pyc_connect_flow("inlet.Fl_O", "comp.Fl_I")
        self.pyc_connect_flow("comp.Fl_O", "burner.Fl_I")
        self.pyc_connect_flow("burner.Fl_O", "turb.Fl_I")
        self.pyc_connect_flow("turb.Fl_O", "nozz.Fl_I")

        # Make other non-flow connections
        self.connect("comp.trq", "shaft.trq_0")
        self.connect("turb.trq", "shaft.trq_1")
        self.connect("fc.Fl_O:stat:P", "nozz.Ps_exhaust")
        self.connect("inlet.Fl_O:tot:P", "perf.Pt2")
        self.connect("comp.Fl_O:tot:P", "perf.Pt3")
        self.connect("burner.Wfuel", "perf.Wfuel_0")
        self.connect("inlet.F_ram", "perf.ram_drag")
        self.connect("nozz.Fg", "perf.Fg_0")

        # Add balances for design and off-design
        balance = self.add_subsystem("balance", om.BalanceComp())
        if design:
            balance.add_balance("W", units="lbm/s", eq_units="lbf", rhs_name="Fn_target")
            self.connect("balance.W", "inlet.Fl_I:stat:W")
            self.connect("perf.Fn", "balance.lhs:W")

            balance.add_balance("FAR", eq_units="degR", lower=1e-4, val=0.017, rhs_name="T4_target")
            self.connect("balance.FAR", "burner.Fl_I:FAR")
            self.connect("burner.Fl_O:tot:T", "balance.lhs:FAR")

            balance.add_balance("turb_PR", val=1.5, lower=1.001, upper=8, eq_units="hp", rhs_val=0.0)
            self.connect("balance.turb_PR", "turb.PR")
            self.connect("shaft.pwr_net", "balance.lhs:turb_PR")
        else:
            balance.add_balance("FAR", eq_units="lbf", lower=1e-4, val=0.3, rhs_name="Fn_target")
            self.connect("balance.FAR", "burner.Fl_I:FAR")
            self.connect("perf.Fn", "balance.lhs:FAR")

            balance.add_balance("Nmech", val=1.5, units="rpm", lower=500.0, eq_units="hp", rhs_val=0.0)
            self.connect("balance.Nmech", "Nmech")
            self.connect("shaft.pwr_net", "balance.lhs:Nmech")

            balance.add_balance("W", val=168.0, units="lbm/s", eq_units="inch**2")
            self.connect("balance.W", "inlet.Fl_I:stat:W")
            self.connect("nozz.Throat:stat:area", "balance.lhs:W")

        newton = self.nonlinear_solver = om.NewtonSolver()
        newton.options["atol"] = 1e-6
        newton.options["rtol"] = 1e-6
        newton.options["iprint"] = 2
        newton.options["maxiter"] = 15
        newton.options["solve_subsystems"] = True
        newton.options["max_sub_solves"] = 100
        newton.options["reraise_child_analysiserror"] = False

        self.linear_solver = om.DirectSolver()

        super().setup()


def viewer(prob, pt, file=sys.stdout):
    """Print a report of all the relevant cycle properties."""

    summary_data = (
        prob[pt + ".fc.Fl_O:stat:MN"],
        prob[pt + ".fc.alt"],
        prob[pt + ".inlet.Fl_O:stat:W"],
        prob[pt + ".perf.Fn"],
        prob[pt + ".perf.Fg"],
        prob[pt + ".inlet.F_ram"],
        prob[pt + ".perf.OPR"],
        prob[pt + ".perf.TSFC"],
    )

    print(file=file, flush=True)
    print(file=file, flush=True)
    print(file=file, flush=True)
    print("----------------------------------------------------------------------------", file=file, flush=True)
    print("                              POINT:", pt, file=file, flush=True)
    print("----------------------------------------------------------------------------", file=file, flush=True)
    print("                       PERFORMANCE CHARACTERISTICS", file=file, flush=True)
    print("    Mach      Alt       W      Fn      Fg    Fram     OPR     TSFC  ", file=file, flush=True)
    print(" %7.5f  %7.1f %7.3f %7.1f %7.1f %7.1f %7.3f  %7.5f" % summary_data, file=file, flush=True)

    fs_names = ["fc.Fl_O", "inlet.Fl_O", "comp.Fl_O", "burner.Fl_O", "turb.Fl_O", "nozz.Fl_O"]
    fs_full_names = [f"{pt}.{fs}" for fs in fs_names]
    pyc.print_flow_station(prob, fs_full_names, file=file)

    comp_full_names = [f"{pt}.comp"]
    pyc.print_compressor(prob, comp_full_names, file=file)

    pyc.print_burner(prob, [f"{pt}.burner"])

    turb_full_names = [f"{pt}.turb"]
    pyc.print_turbine(prob, turb_full_names, file=file)

    noz_full_names = [f"{pt}.nozz"]
    pyc.print_nozzle(prob, noz_full_names, file=file)

    shaft_full_names = [f"{pt}.shaft"]
    pyc.print_shaft(prob, shaft_full_names, file=file)


def map_plots(prob, pt):
    pyc.plot_compressor_maps(prob, [f"{pt}.comp"])
    pyc.plot_turbine_maps(prob, [f"{pt}.turb"])


def plot_ts_diagram(prob, pt):
    """建立溫度-熵圖（独立視窗）。"""

    stations = ["fc.Fl_O", "inlet.Fl_O", "comp.Fl_O", "burner.Fl_O", "turb.Fl_O", "nozz.Fl_O"]
    temperatures = [prob[f"{pt}.{s}:tot:T"][0] for s in stations]
    entropies = [prob[f"{pt}.{s}:tot:S"][0] for s in stations]

    plt.figure(figsize=(12, 8))
    plt.plot(entropies, temperatures, "bo-", linewidth=3, markersize=10, label="Cycle Path")

    labels = ["0-Ambient", "1-Inlet", "2-Compressor", "3-Combustor", "4-Turbine", "5-Nozzle"]
    colors = ["red", "blue", "green", "orange", "purple", "brown"]
    for s, t, label, color in zip(entropies, temperatures, labels, colors):
        plt.annotate(
            label,
            (s, t),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=12,
            fontweight="bold",
            color=color,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
        )

    plt.xlabel("Entropy S (Btu/lbm/degR)", fontsize=14)
    plt.ylabel("Temperature T (degR)", fontsize=14)
    plt.title(f"Temperature-Entropy Diagram - {pt}", fontsize=16, fontweight="bold")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()


def plot_pressure_enthalpy_diagram(prob, pt):
    """建立壓力-焓圖（独立視窗）。"""

    stations = ["fc.Fl_O", "inlet.Fl_O", "comp.Fl_O", "burner.Fl_O", "turb.Fl_O", "nozz.Fl_O"]
    pressures = [prob[f"{pt}.{s}:tot:P"][0] for s in stations]
    enthalpies = [prob[f"{pt}.{s}:tot:h"][0] for s in stations]

    plt.figure(figsize=(12, 8))
    plt.semilogy(enthalpies, pressures, "ro-", linewidth=3, markersize=10, label="Cycle Path")

    labels = ["0-Ambient", "1-Inlet", "2-Compressor", "3-Combustor", "4-Turbine", "5-Nozzle"]
    colors = ["red", "blue", "green", "orange", "purple", "brown"]
    for h, p, label, color in zip(enthalpies, pressures, labels, colors):
        plt.annotate(
            label,
            (h, p),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=12,
            fontweight="bold",
            color=color,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
        )

    plt.xlabel("Enthalpy h (Btu/lbm)", fontsize=14)
    plt.ylabel("Pressure P (psia)", fontsize=14)
    plt.title(f"Pressure-Enthalpy Diagram - {pt}", fontsize=16, fontweight="bold")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()


def comprehensive_performance_summary(prob, pt):
    """詳細的性能摘要（列印到 stdout）。"""

    print(f"\n{'=' * 80}")
    print(f"Comprehensive Performance Analysis - {pt}")
    print(f"{'=' * 80}")

    fn = prob[f"{pt}.perf.Fn"][0]
    tsfc = prob[f"{pt}.perf.TSFC"][0]
    opr = prob[f"{pt}.perf.OPR"][0]
    wfuel = prob[f"{pt}.burner.Wfuel"][0]
    w_air = prob[f"{pt}.inlet.Fl_O:stat:W"][0]

    print(f"Thrust (Fn):              {fn:.1f} lbf")
    print(f"TSFC:                     {tsfc:.5f} lbm/hr/lbf")
    print(f"Overall Pressure Ratio:   {opr:.2f}")
    print(f"Fuel Flow Rate:           {wfuel:.3f} lbm/s")
    print(f"Air Flow Rate:            {w_air:.1f} lbm/s")
    print(f"Fuel-to-Air Ratio:        {wfuel / w_air:.4f}")

    print("\nTemperature Distribution:")
    stations = ["fc.Fl_O", "inlet.Fl_O", "comp.Fl_O", "burner.Fl_O", "turb.Fl_O", "nozz.Fl_O"]
    labels = ["Ambient", "Inlet", "Comp Exit", "Burner Exit", "Turb Exit", "Nozz Exit"]
    for station, label in zip(stations, labels):
        T = prob[f"{pt}.{station}:tot:T"][0]
        P = prob[f"{pt}.{station}:tot:P"][0]
        print(f"{label:12}: {T:.1f} degR ({(T - 459.67) * 5 / 9:.1f} degC), {P:.1f} psia")

    comp_eff = prob[f"{pt}.comp.eff"][0]
    turb_eff = prob[f"{pt}.turb.eff"][0]
    print("\nComponent Efficiency:")
    print(f"Compressor Efficiency:    {comp_eff:.3f}")
    print(f"Turbine Efficiency:       {turb_eff:.3f}")

    print("\nFlow Parameters:")
    for station, label in zip(stations, labels):
        MN = prob[f"{pt}.{station}:stat:MN"][0]
        V = prob[f"{pt}.{station}:stat:V"][0]
        print(f"{label:12}: Mach {MN:.3f}, Velocity {V:.1f} ft/s")


class MPTurbojet(pyc.MPCycle):
    def setup(self):
        self.pyc_add_pnt("DESIGN", Turbojet())

        self.set_input_defaults("DESIGN.Nmech", 8070.0, units="rpm")
        self.set_input_defaults("DESIGN.inlet.MN", 0.60)
        self.set_input_defaults("DESIGN.comp.MN", 0.020)
        self.set_input_defaults("DESIGN.burner.MN", 0.020)
        self.set_input_defaults("DESIGN.turb.MN", 0.4)

        self.pyc_add_cycle_param("burner.dPqP", 0.03)
        self.pyc_add_cycle_param("nozz.Cv", 0.99)

        # define the off-design conditions we want to run
        self.od_pts = ["OD0", "OD1"]
        self.od_MNs = [0.000001, 0.2]
        self.od_alts = [0.0, 5000]
        self.od_Fns = [11000.0, 8000.0]

        for i, pt in enumerate(self.od_pts):
            self.pyc_add_pnt(pt, Turbojet(design=False))
            self.set_input_defaults(pt + ".fc.MN", val=self.od_MNs[i])
            self.set_input_defaults(pt + ".fc.alt", self.od_alts[i], units="ft")
            self.set_input_defaults(pt + ".balance.Fn_target", self.od_Fns[i], units="lbf")

        self.pyc_use_default_des_od_conns()
        self.pyc_connect_des_od("nozz.Throat:stat:area", "balance.rhs:W")

        super().setup()


# ---------------------------------------------------------------------------
# Output directory — everything is written next to this script
# ---------------------------------------------------------------------------

OUT_DIR = Path(__file__).resolve().parent / "output"
STATIONS = ["fc.Fl_O", "inlet.Fl_O", "comp.Fl_O", "burner.Fl_O", "turb.Fl_O", "nozz.Fl_O"]
STATION_LABELS = ["0-Ambient", "1-Inlet", "2-Compressor", "3-Combustor", "4-Turbine", "5-Nozzle"]
# Per-station label offsets in display points. Tuned so neighbouring
# stations that cluster (0/1, 2/3, 4/5) fan their labels apart.
STATION_LABEL_OFFSETS = [
    (-55, -30),  # 0-Ambient — down-left
    (35, -30),   # 1-Inlet — down-right
    (-65, 30),   # 2-Compressor — up-left
    (25, 30),    # 3-Combustor — up-right
    (-55, -30),  # 4-Turbine — down-left
    (25, 25),    # 5-Nozzle — up-right
]


# ---------------------------------------------------------------------------
# Headless solve helper (shared by CLI / GUI worker)
# ---------------------------------------------------------------------------


def solve_problem(params: dict) -> tuple[om.Problem, "MPTurbojet"]:
    """Build the MPTurbojet problem, apply user inputs, and run the model."""

    # chdir into OUT_DIR so OpenMDAO's auto-generated work directory
    # (work_dir/<prob_name>_out/reports/) lands inside output/. We flatten
    # the HTML reports up to OUT_DIR after the run finishes.
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    os.chdir(OUT_DIR)
    os.environ.pop("OPENMDAO_REPORTS", None)

    prob = om.Problem()
    mp = prob.model = MPTurbojet()
    prob.setup(check=False)

    prob.set_val("DESIGN.fc.alt", params["altitude_ft"], units="ft")
    prob.set_val("DESIGN.fc.MN", params["mach"])
    prob.set_val("DESIGN.balance.Fn_target", params["fn_target_lbf"], units="lbf")
    prob.set_val("DESIGN.balance.T4_target", params["t4_target_deg_r"], units="degR")
    prob.set_val("DESIGN.comp.PR", params["compressor_pr"])
    prob.set_val("DESIGN.comp.eff", params["compressor_efficiency"])
    prob.set_val("DESIGN.turb.eff", params["turbine_efficiency"])

    prob["DESIGN.balance.FAR"] = 0.0175506829934
    prob["DESIGN.balance.W"] = 168.453135137
    prob["DESIGN.balance.turb_PR"] = 4.46138725662
    prob["DESIGN.fc.balance.Pt"] = 14.6955113159
    prob["DESIGN.fc.balance.Tt"] = 518.665288153

    for pt in mp.od_pts:
        prob[pt + ".balance.W"] = 166.073
        prob[pt + ".balance.FAR"] = 0.01680
        prob[pt + ".balance.Nmech"] = 8197.38
        prob[pt + ".fc.balance.Pt"] = 15.703
        prob[pt + ".fc.balance.Tt"] = 558.31
        prob[pt + ".turb.PR"] = 4.6690

    prob.set_solver_print(level=-1)
    prob.set_solver_print(level=2, depth=1)
    prob.run_model()
    _flatten_openmdao_reports(prob)
    return prob, mp


def _flatten_openmdao_reports(prob: om.Problem) -> list[Path]:
    """Move OpenMDAO's nested HTML reports up into OUT_DIR.

    OpenMDAO 3.40 writes reports to ``<work_dir>/<prob_name>_out/reports/``
    and offers no public hook to redirect them. We let OpenMDAO write them
    in-place, then move every HTML file up to ``OUT_DIR`` and clean the
    intermediate ``*_out`` work folder.
    """

    moved: list[Path] = []
    try:
        reports_dir = Path(prob.get_reports_dir())
    except Exception:
        return moved
    if not reports_dir.exists():
        return moved

    for src in reports_dir.glob("**/*.html"):
        dst = OUT_DIR / src.name
        try:
            if dst.exists():
                dst.unlink()
            src.replace(dst)
            moved.append(dst)
        except OSError:
            continue

    # Walk back up to the top-level "<prob_name>_out" and remove the empty tree.
    work_root = reports_dir
    while work_root.parent != work_root and work_root != OUT_DIR:
        parent = work_root.parent
        if work_root.name.endswith("_out") and parent == OUT_DIR:
            import shutil

            shutil.rmtree(work_root, ignore_errors=True)
            break
        work_root = parent
    return moved


# ---------------------------------------------------------------------------
# Plotting helpers that draw onto a passed-in Figure
# ---------------------------------------------------------------------------


def _annotate_stations(ax, xs, ys, *, log_y: bool = False) -> None:
    """Place station labels with leader lines so close-packed points don't overlap."""

    bbox = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#444", alpha=0.9)
    arrow = dict(arrowstyle="-", color="#666", lw=0.8, shrinkA=0, shrinkB=4)
    for x, y, label, offset in zip(xs, ys, STATION_LABELS, STATION_LABEL_OFFSETS):
        ax.annotate(
            label,
            xy=(x, y),
            xytext=offset,
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            ha="left" if offset[0] >= 0 else "right",
            va="bottom" if offset[1] >= 0 else "top",
            bbox=bbox,
            arrowprops=arrow,
        )

    # Add a little headroom so labels at the edges don't get clipped.
    x_lo, x_hi = min(xs), max(xs)
    x_pad = (x_hi - x_lo) * 0.15 if x_hi > x_lo else 1.0
    ax.set_xlim(x_lo - x_pad, x_hi + x_pad)
    if not log_y:
        y_lo, y_hi = min(ys), max(ys)
        y_pad = (y_hi - y_lo) * 0.12 if y_hi > y_lo else 1.0
        ax.set_ylim(y_lo - y_pad, y_hi + y_pad)


def draw_ts_diagram(fig, prob, pt: str) -> None:
    fig.clear()
    ax = fig.add_subplot(111)
    Ts = [prob[f"{pt}.{s}:tot:T"][0] for s in STATIONS]
    Ss = [prob[f"{pt}.{s}:tot:S"][0] for s in STATIONS]
    ax.plot(Ss, Ts, "bo-", linewidth=3, markersize=10, label="Cycle Path")
    _annotate_stations(ax, Ss, Ts)
    ax.set_xlabel("Entropy S (Btu/lbm/degR)")
    ax.set_ylabel("Temperature T (degR)")
    ax.set_title(f"Temperature-Entropy Diagram - {pt}")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()


def draw_ph_diagram(fig, prob, pt: str) -> None:
    fig.clear()
    ax = fig.add_subplot(111)
    Ps = [prob[f"{pt}.{s}:tot:P"][0] for s in STATIONS]
    Hs = [prob[f"{pt}.{s}:tot:h"][0] for s in STATIONS]
    ax.semilogy(Hs, Ps, "ro-", linewidth=3, markersize=10, label="Cycle Path")
    _annotate_stations(ax, Hs, Ps, log_y=True)
    # Manual log-y padding (multiplicative) so labels at the top/bottom fit.
    p_lo, p_hi = min(Ps), max(Ps)
    ax.set_ylim(p_lo / 1.6, p_hi * 1.6)
    ax.set_xlabel("Enthalpy h (Btu/lbm)")
    ax.set_ylabel("Pressure P (psia)")
    ax.set_title(f"Pressure-Enthalpy Diagram - {pt}")
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(loc="lower right")
    fig.tight_layout()


def draw_comparison(fig, prob, points: list[str]) -> None:
    fig.clear()
    axes = fig.subplots(2, 2)
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]
    styles = ["-", "--", ":", "-.", "-"]

    ax_ts = axes[0, 0]
    for i, pt in enumerate(points):
        Ts = [prob[f"{pt}.{s}:tot:T"][0] for s in STATIONS]
        Ss = [prob[f"{pt}.{s}:tot:S"][0] for s in STATIONS]
        ax_ts.plot(Ss, Ts, "o-", color=colors[i % len(colors)], linestyle=styles[i % len(styles)], linewidth=2, label=pt)
    ax_ts.set_xlabel("Entropy S (Btu/lbm/degR)")
    ax_ts.set_ylabel("Temperature T (degR)")
    ax_ts.set_title("T-S Diagram Comparison")
    ax_ts.grid(True, alpha=0.3)
    ax_ts.legend()

    bar_colors = [colors[i % len(colors)] for i in range(len(points))]
    thrusts = [prob[f"{pt}.perf.Fn"][0] for pt in points]
    tsfcs = [prob[f"{pt}.perf.TSFC"][0] for pt in points]
    oprs = [prob[f"{pt}.perf.OPR"][0] for pt in points]

    axes[0, 1].bar(points, thrusts, color=bar_colors, alpha=0.75)
    axes[0, 1].set_ylabel("Thrust (lbf)")
    axes[0, 1].set_title("Thrust Comparison")
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].bar(points, tsfcs, color=bar_colors, alpha=0.75)
    axes[1, 0].set_ylabel("TSFC (lbm/hr/lbf)")
    axes[1, 0].set_title("TSFC Comparison")
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].bar(points, oprs, color=bar_colors, alpha=0.75)
    axes[1, 1].set_ylabel("Overall Pressure Ratio")
    axes[1, 1].set_title("OPR Comparison")
    axes[1, 1].grid(True, alpha=0.3)

    fig.tight_layout()


def capture_summary_text(prob, points: list[str]) -> str:
    """Run viewer + comprehensive summary into a single string."""

    import contextlib
    import io

    buf = io.StringIO()
    for pt in points:
        viewer(prob, pt, file=buf)
    with contextlib.redirect_stdout(buf):
        for pt in points:
            comprehensive_performance_summary(prob, pt)
    return buf.getvalue()


def save_component_maps(prob, pt: str, out_dir: Path) -> list[Path]:
    """Call upstream map plotters and save each figure as PNG + PDF."""

    saved: list[Path] = []

    def _capture(plot_call, prefix: str) -> None:
        before = set(plt.get_fignums())
        plot_call()
        new_nums = sorted(set(plt.get_fignums()) - before)
        for idx, num in enumerate(new_nums):
            fig = plt.figure(num)
            png_path = out_dir / f"{prefix}_{pt}_{idx}.png"
            pdf_path = out_dir / f"{prefix}_{pt}_{idx}.pdf"
            fig.savefig(png_path, dpi=120, bbox_inches="tight")
            fig.savefig(pdf_path, bbox_inches="tight")
            saved.append(png_path)
            saved.append(pdf_path)

    _capture(lambda: pyc.plot_compressor_maps(prob, [f"{pt}.comp"]), "simple_turbojet_compressor_map")
    _capture(lambda: pyc.plot_turbine_maps(prob, [f"{pt}.turb"]), "simple_turbojet_turbine_map")

    for num in list(plt.get_fignums()):
        plt.close(num)
    return saved


def save_summary_pdf(path: Path, title: str, body_text: str) -> None:
    """Render a plain-text summary as a simple PDF via reportlab."""

    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Preformatted

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()
    mono_style = ParagraphStyle(
        "mono",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
    )
    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),
        Preformatted(body_text, mono_style),
    ]
    doc.build(story)


# ---------------------------------------------------------------------------
# PySide6 GUI
# ---------------------------------------------------------------------------


def _import_qt():
    """Import PySide6 lazily so the module is still usable headlessly."""

    try:
        from PySide6 import QtCore, QtGui, QtWidgets  # noqa: F401
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
        from matplotlib.figure import Figure
    except ImportError as exc:  # pragma: no cover - depends on env
        raise SystemExit(
            "PySide6 is required to launch the GUI.\n"
            "Install it with:  uv pip install PySide6\n"
            f"Underlying error: {exc}"
        )
    return QtCore, QtGui, QtWidgets, FigureCanvasQTAgg, NavigationToolbar2QT, Figure


def launch_gui() -> int:
    QtCore, QtGui, QtWidgets, FigureCanvas, NavigationToolbar, Figure = _import_qt()

    class CycleWorker(QtCore.QObject):
        finished = QtCore.Signal(object)
        failed = QtCore.Signal(str)
        log = QtCore.Signal(str)

        def __init__(self, params: dict):
            super().__init__()
            self.params = params

        @QtCore.Slot()
        def run(self) -> None:
            import contextlib
            import io
            import time

            try:
                self.log.emit("Setting up MPTurbojet…")
                solver_buf = io.StringIO()
                started = time.time()
                with contextlib.redirect_stdout(solver_buf):
                    prob, mp = solve_problem(self.params)
                elapsed = time.time() - started
                self.log.emit(f"Solver finished in {elapsed:.2f} s.")
                points = ["DESIGN"] + list(mp.od_pts)
                summary = capture_summary_text(prob, points)
                self.finished.emit(
                    {
                        "prob": prob,
                        "mp": mp,
                        "points": points,
                        "summary": summary,
                        "solver_log": solver_buf.getvalue(),
                        "elapsed": elapsed,
                        "params": self.params,
                    }
                )
            except Exception as exc:
                import traceback

                self.failed.emit(f"{exc}\n\n{traceback.format_exc()}")

    class PlotTab(QtWidgets.QWidget):
        def __init__(self, parent: QtWidgets.QWidget | None = None):
            super().__init__(parent)
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            self.toolbar = NavigationToolbar(self.canvas, self)
            layout = QtWidgets.QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.toolbar)
            layout.addWidget(self.canvas)

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Simple Turbojet — pyCycle GUI")
            self.resize(1280, 820)

            self._thread: QtCore.QThread | None = None
            self._worker: CycleWorker | None = None
            self._last_result: dict | None = None

            self._build_ui()
            self.statusBar().showMessage(f"輸出資料夾 / Output: {OUT_DIR}")

        # ----- UI construction --------------------------------------------------
        def _build_ui(self) -> None:
            central = QtWidgets.QWidget()
            self.setCentralWidget(central)
            root = QtWidgets.QHBoxLayout(central)

            # Left pane: input form + log
            left = QtWidgets.QWidget()
            left.setMaximumWidth(360)
            left_layout = QtWidgets.QVBoxLayout(left)

            form_box = QtWidgets.QGroupBox("Design Point Inputs / 設計點輸入")
            form = QtWidgets.QFormLayout(form_box)

            self.altitude = self._spin(0.0, -1000.0, 80000.0, 100.0, 1, suffix=" ft")
            self.mach = self._spin(0.000001, 0.0, 3.0, 0.05, 6)
            self.fn_target = self._spin(11800.0, 0.0, 1.0e6, 100.0, 1, suffix=" lbf")
            self.t4_target = self._spin(2370.0, 500.0, 4000.0, 10.0, 1, suffix=" degR")
            self.comp_pr = self._spin(13.5, 1.0, 60.0, 0.5, 3)
            self.comp_eff = self._spin(0.83, 0.30, 1.0, 0.01, 3)
            self.turb_eff = self._spin(0.86, 0.30, 1.0, 0.01, 3)

            form.addRow("Altitude / 高度", self.altitude)
            form.addRow("Mach / 馬赫數", self.mach)
            form.addRow("Target Fn / 目標淨推力", self.fn_target)
            form.addRow("T4 target / 渦輪入口溫度", self.t4_target)
            form.addRow("Compressor PR / 壓縮機壓比", self.comp_pr)
            form.addRow("Compressor η / 壓縮機效率", self.comp_eff)
            form.addRow("Turbine η / 渦輪效率", self.turb_eff)

            left_layout.addWidget(form_box)

            btn_row = QtWidgets.QHBoxLayout()
            self.run_btn = QtWidgets.QPushButton("▶ Run / 執行")
            self.run_btn.setDefault(True)
            self.reset_btn = QtWidgets.QPushButton("Reset / 重設")
            self.open_dir_btn = QtWidgets.QPushButton("Open output folder")
            btn_row.addWidget(self.run_btn)
            btn_row.addWidget(self.reset_btn)
            left_layout.addLayout(btn_row)
            left_layout.addWidget(self.open_dir_btn)

            self.progress = QtWidgets.QProgressBar()
            self.progress.setRange(0, 0)
            self.progress.setVisible(False)
            left_layout.addWidget(self.progress)

            log_box = QtWidgets.QGroupBox("Log")
            log_layout = QtWidgets.QVBoxLayout(log_box)
            self.log_view = QtWidgets.QPlainTextEdit()
            self.log_view.setReadOnly(True)
            font = QtGui.QFont("Consolas")
            font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
            self.log_view.setFont(font)
            log_layout.addWidget(self.log_view)
            left_layout.addWidget(log_box, 1)

            root.addWidget(left)

            # Right pane: tabs
            self.tabs = QtWidgets.QTabWidget()

            self.summary_view = QtWidgets.QPlainTextEdit()
            self.summary_view.setReadOnly(True)
            self.summary_view.setFont(font)
            self.tabs.addTab(self.summary_view, "Summary / 摘要")

            self.tab_ts = PlotTab()
            self.tab_ph = PlotTab()
            self.tab_compare = PlotTab()
            self.tabs.addTab(self.tab_ts, "T-S Diagram")
            self.tabs.addTab(self.tab_ph, "P-h Diagram")
            self.tabs.addTab(self.tab_compare, "Comparison")

            self.maps_scroll = QtWidgets.QScrollArea()
            self.maps_scroll.setWidgetResizable(True)
            self.maps_container = QtWidgets.QWidget()
            self.maps_layout = QtWidgets.QVBoxLayout(self.maps_container)
            self.maps_scroll.setWidget(self.maps_container)
            self.tabs.addTab(self.maps_scroll, "Component Maps")

            root.addWidget(self.tabs, 1)

            # Signals
            self.run_btn.clicked.connect(self._on_run)
            self.reset_btn.clicked.connect(self._on_reset)
            self.open_dir_btn.clicked.connect(self._on_open_dir)

        @staticmethod
        def _spin(value: float, lo: float, hi: float, step: float, decimals: int, suffix: str = "") -> "QtWidgets.QDoubleSpinBox":
            box = QtWidgets.QDoubleSpinBox()
            box.setRange(lo, hi)
            box.setSingleStep(step)
            box.setDecimals(decimals)
            box.setValue(value)
            if suffix:
                box.setSuffix(suffix)
            box.setMinimumWidth(160)
            return box

        # ----- Slots -----------------------------------------------------------
        def _log(self, msg: str) -> None:
            self.log_view.appendPlainText(msg)

        def _collect_params(self) -> dict:
            return {
                "altitude_ft": self.altitude.value(),
                "mach": self.mach.value(),
                "fn_target_lbf": self.fn_target.value(),
                "t4_target_deg_r": self.t4_target.value(),
                "compressor_pr": self.comp_pr.value(),
                "compressor_efficiency": self.comp_eff.value(),
                "turbine_efficiency": self.turb_eff.value(),
            }

        def _on_run(self) -> None:
            if self._thread is not None:
                return
            params = self._collect_params()
            self.log_view.clear()
            self._log(f"Run started @ {OUT_DIR}")
            self._log(f"Params: {params}")
            self.run_btn.setEnabled(False)
            self.progress.setVisible(True)

            self._thread = QtCore.QThread(self)
            self._worker = CycleWorker(params)
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._worker.log.connect(self._log)
            self._worker.finished.connect(self._on_finished)
            self._worker.failed.connect(self._on_failed)
            self._worker.finished.connect(self._thread.quit)
            self._worker.failed.connect(self._thread.quit)
            self._thread.finished.connect(self._cleanup_thread)
            self._thread.start()

        def _cleanup_thread(self) -> None:
            if self._worker is not None:
                self._worker.deleteLater()
            if self._thread is not None:
                self._thread.deleteLater()
            self._worker = None
            self._thread = None
            self.run_btn.setEnabled(True)
            self.progress.setVisible(False)

        def _on_failed(self, msg: str) -> None:
            self._log("Run failed:")
            self._log(msg)
            QtWidgets.QMessageBox.critical(self, "Run failed", msg)

        def _on_finished(self, result: dict) -> None:
            self._last_result = result
            prob = result["prob"]
            points = result["points"]
            summary = result["summary"]
            solver_log = result["solver_log"]
            elapsed = result["elapsed"]

            self.summary_view.setPlainText(summary)
            self._log(f"Solver elapsed: {elapsed:.2f} s")
            self._log(f"Points solved: {', '.join(points)}")

            # Redraw embedded plots
            draw_ts_diagram(self.tab_ts.figure, prob, "DESIGN")
            self.tab_ts.canvas.draw_idle()
            draw_ph_diagram(self.tab_ph.figure, prob, "DESIGN")
            self.tab_ph.canvas.draw_idle()
            draw_comparison(self.tab_compare.figure, prob, points)
            self.tab_compare.canvas.draw_idle()

            # Save artefacts to OUT_DIR
            saved: list[Path] = []

            summary_path = OUT_DIR / "simple_turbojet_summary.txt"
            summary_path.write_text(
                "=== Inputs ===\n"
                + "\n".join(f"{k}: {v}" for k, v in result["params"].items())
                + f"\n\nElapsed: {elapsed:.2f} s\n\n"
                + "=== Solver Log ===\n"
                + solver_log
                + "\n\n=== Performance Summary ===\n"
                + summary,
                encoding="utf-8",
            )
            saved.append(summary_path)

            def _save_fig(fig, stem: str) -> None:
                png = OUT_DIR / f"{stem}.png"
                pdf = OUT_DIR / f"{stem}.pdf"
                fig.savefig(png, dpi=140, bbox_inches="tight")
                fig.savefig(pdf, bbox_inches="tight")
                saved.append(png)
                saved.append(pdf)

            _save_fig(self.tab_ts.figure, "simple_turbojet_ts_diagram")
            _save_fig(self.tab_ph.figure, "simple_turbojet_ph_diagram")
            _save_fig(self.tab_compare.figure, "simple_turbojet_comparison")

            summary_pdf = OUT_DIR / "simple_turbojet_summary.pdf"
            try:
                save_summary_pdf(summary_pdf, "Simple Turbojet — Run Summary", summary_path.read_text(encoding="utf-8"))
                saved.append(summary_pdf)
            except Exception as exc:  # pragma: no cover - reportlab edge cases
                self._log(f"Summary PDF skipped: {exc}")

            # Component maps — generated separately via pyc helpers
            try:
                saved.extend(save_component_maps(prob, "DESIGN", OUT_DIR))
            except Exception as exc:  # pragma: no cover - upstream plotter quirks
                self._log(f"Component-map plotting skipped: {exc}")

            self._refresh_maps_tab(saved)

            self._log("Artefacts written:")
            for path in saved:
                self._log(f"  - {path.name}")
            self.statusBar().showMessage(f"Done. {len(saved)} files written to {OUT_DIR}")

        def _refresh_maps_tab(self, saved: list[Path]) -> None:
            while self.maps_layout.count():
                item = self.maps_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            map_files = [p for p in saved if "_map_" in p.name and p.suffix == ".png"]
            if not map_files:
                lbl = QtWidgets.QLabel("(No component-map images were generated.)")
                lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.maps_layout.addWidget(lbl)
                return

            for path in map_files:
                title = QtWidgets.QLabel(path.name)
                title.setStyleSheet("font-weight: bold; padding: 6px;")
                self.maps_layout.addWidget(title)

                img_label = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(str(path))
                if not pixmap.isNull():
                    img_label.setPixmap(
                        pixmap.scaledToWidth(
                            min(900, pixmap.width()),
                            QtCore.Qt.TransformationMode.SmoothTransformation,
                        )
                    )
                img_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.maps_layout.addWidget(img_label)

            self.maps_layout.addStretch(1)

        def _on_reset(self) -> None:
            self.altitude.setValue(0.0)
            self.mach.setValue(0.000001)
            self.fn_target.setValue(11800.0)
            self.t4_target.setValue(2370.0)
            self.comp_pr.setValue(13.5)
            self.comp_eff.setValue(0.83)
            self.turb_eff.setValue(0.86)

        def _on_open_dir(self) -> None:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(OUT_DIR)))

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(launch_gui())
