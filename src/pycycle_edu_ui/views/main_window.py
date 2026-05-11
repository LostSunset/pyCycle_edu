from __future__ import annotations

import math

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pycycle_edu_ui.models import EngineCase, estimate_reference_result
from pycycle_edu_ui.widgets import FlowDiagram, MetricCard

try:
    import pyqtgraph as pg
except Exception:  # pragma: no cover - optional at import time
    pg = None

try:
    from qfluentwidgets import PrimaryPushButton, PushButton
except Exception:  # pragma: no cover - fallback when dependency is absent
    PrimaryPushButton = QPushButton
    PushButton = QPushButton


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("pyCycle Edu Workbench")
        self.case = EngineCase()
        self.result = estimate_reference_result(self.case)

        self.stack = QStackedWidget()
        self.metric_cards: dict[str, MetricCard] = {}
        self.inputs: dict[str, QDoubleSpinBox] = {}

        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._build_sidebar())
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        self.stack.addWidget(self._build_workbench_page())
        self.stack.addWidget(self._build_results_page())
        self.stack.addWidget(self._build_report_page())
        self._refresh_results()

    def _build_sidebar(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(250)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 24, 18, 18)
        layout.setSpacing(12)

        title = QLabel("pyCycle Edu")
        title.setStyleSheet("font-size: 24px; font-weight: 800;")
        subtitle = QLabel("渦扇教學工作台")
        subtitle.setObjectName("HintText")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(18)

        buttons = [
            ("發動機設定", 0),
            ("結果圖表", 1),
            ("雙語報告", 2),
        ]
        for text, index in buttons:
            button = PushButton(text)
            button.setMinimumHeight(44)
            button.clicked.connect(lambda checked=False, page=index: self.stack.setCurrentIndex(page))
            layout.addWidget(button)

        layout.addStretch(1)
        note = QLabel("資料來源先存 Reference_sources；答案與提示詞存 Reference_answers。")
        note.setObjectName("HintText")
        note.setWordWrap(True)
        layout.addWidget(note)
        return frame

    def _build_workbench_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("單軸高旁通比渦扇：教學 UI/UX 參考實作")
        title.setObjectName("PageTitle")
        hint = QLabel("第一版先以公開可查資料與 pyCycle 範例概念建立工作流；數值計算目前是 UI 教學估算，下一階段接上 pyCycle runner。")
        hint.setObjectName("HintText")
        hint.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(hint)

        content = QHBoxLayout()
        content.setSpacing(18)
        content.addWidget(self._build_input_panel(), 0)
        content.addWidget(self._build_overview_panel(), 1)
        layout.addLayout(content, 1)
        return page

    def _build_input_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        panel.setFixedWidth(390)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        title = QLabel("發動機參數")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        family = QComboBox()
        family.addItems(["CFM56-7B 教學近似案例", "pyCycle high_bypass_turbofan 範例"])
        layout.addWidget(family)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        self.inputs = {
            "bypass_ratio": self._spin(0.5, 16.0, self.case.bypass_ratio, 0.1),
            "overall_pressure_ratio": self._spin(5.0, 60.0, self.case.overall_pressure_ratio, 0.5),
            "turbine_inlet_temperature_k": self._spin(1000.0, 2100.0, self.case.turbine_inlet_temperature_k, 10.0),
            "altitude_ft": self._spin(0.0, 45000.0, self.case.altitude_ft, 500.0),
            "mach": self._spin(0.0, 0.95, self.case.mach, 0.01),
            "mass_flow_lb_s": self._spin(100.0, 1800.0, self.case.mass_flow_lb_s, 10.0),
        }
        labels = {
            "bypass_ratio": "旁通比 BPR",
            "overall_pressure_ratio": "總壓比 OPR",
            "turbine_inlet_temperature_k": "渦輪入口溫度 K",
            "altitude_ft": "高度 ft",
            "mach": "馬赫數",
            "mass_flow_lb_s": "質量流率 lb/s",
        }
        for key, widget in self.inputs.items():
            form.addRow(labels[key], widget)
            widget.valueChanged.connect(self._handle_case_changed)
        layout.addLayout(form)

        run_button = PrimaryPushButton("更新教學估算")
        run_button.setObjectName("PrimaryButton")
        run_button.clicked.connect(self._handle_case_changed)
        layout.addWidget(run_button)

        pycycle_button = PushButton("下一階段：連接 pyCycle runner")
        pycycle_button.clicked.connect(self._show_runner_message)
        layout.addWidget(pycycle_button)

        layout.addStretch(1)
        return panel

    def _build_overview_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        title = QLabel("流程與即時摘要")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)
        layout.addWidget(FlowDiagram())

        grid = QGridLayout()
        grid.setSpacing(12)
        specs = [
            ("thrust", "淨推力", "--", "lbf"),
            ("tsfc", "TSFC", "--", "lb/lbf/hr"),
            ("fuel", "燃油流量", "--", "lb/hr"),
            ("eff", "推進效率", "--", ""),
        ]
        for index, (key, title_text, value, unit) in enumerate(specs):
            card = MetricCard(title_text, value, unit)
            self.metric_cards[key] = card
            grid.addWidget(card, index // 2, index % 2)
        layout.addLayout(grid)

        table = QTableWidget(6, 3)
        table.setHorizontalHeaderLabels(["站點", "意義", "教學輸出"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.station_table = table
        layout.addWidget(table, 1)
        return panel

    def _build_results_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("結果圖表")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._build_plot_panel("bpr"), "旁通比掃描")
        tabs.addTab(self._build_plot_panel("opr"), "壓比掃描")
        layout.addWidget(tabs, 1)
        return page

    def _build_plot_panel(self, mode: str) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)

        if pg is None:
            label = QLabel("尚未安裝 pyqtgraph；請用 uv sync 後再開啟圖表。")
            label.setObjectName("HintText")
            layout.addWidget(label)
            return panel

        plot = pg.PlotWidget()
        plot.setBackground("#FFFCF6")
        plot.showGrid(x=True, y=True, alpha=0.25)
        plot.addLegend()
        pen_thrust = pg.mkPen("#B86B32", width=3)
        pen_tsfc = pg.mkPen("#487A5E", width=3)

        if mode == "bpr":
            x_values = [3.0 + index * 0.5 for index in range(19)]
            x_label = "BPR"
            cases = [EngineCase(bypass_ratio=x, overall_pressure_ratio=self.case.overall_pressure_ratio) for x in x_values]
        else:
            x_values = [18 + index * 2 for index in range(19)]
            x_label = "OPR"
            cases = [EngineCase(bypass_ratio=self.case.bypass_ratio, overall_pressure_ratio=x) for x in x_values]

        thrust = [estimate_reference_result(case).net_thrust_lbf / 1000.0 for case in cases]
        tsfc = [estimate_reference_result(case).tsfc_lb_lbf_hr for case in cases]
        plot.plot(x_values, thrust, pen=pen_thrust, name="淨推力 klbf")
        plot.plot(x_values, tsfc, pen=pen_tsfc, name="TSFC")
        plot.setLabel("bottom", x_label)
        plot.setLabel("left", "教學估算")
        layout.addWidget(plot)
        return panel

    def _build_report_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("正體中文 / English 報告草稿")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        self.report_text = QPlainTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text, 1)

        row = QHBoxLayout()
        zh_button = PrimaryPushButton("產生正體中文摘要")
        zh_button.setObjectName("PrimaryButton")
        en_button = PushButton("Generate English Summary")
        zh_button.clicked.connect(lambda: self._write_report("zh"))
        en_button.clicked.connect(lambda: self._write_report("en"))
        row.addWidget(zh_button)
        row.addWidget(en_button)
        row.addStretch(1)
        layout.addLayout(row)
        return page

    def _spin(self, minimum: float, maximum: float, value: float, step: float) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(minimum, maximum)
        spin.setValue(value)
        spin.setSingleStep(step)
        spin.setDecimals(2 if step < 0.1 else 1)
        spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        return spin

    def _handle_case_changed(self) -> None:
        self.case = EngineCase(
            bypass_ratio=self.inputs["bypass_ratio"].value(),
            overall_pressure_ratio=self.inputs["overall_pressure_ratio"].value(),
            turbine_inlet_temperature_k=self.inputs["turbine_inlet_temperature_k"].value(),
            altitude_ft=self.inputs["altitude_ft"].value(),
            mach=self.inputs["mach"].value(),
            mass_flow_lb_s=self.inputs["mass_flow_lb_s"].value(),
        )
        self.result = estimate_reference_result(self.case)
        self._refresh_results()

    def _refresh_results(self) -> None:
        result = self.result
        self.metric_cards["thrust"].set_value(f"{result.net_thrust_lbf:,.0f}", "lbf")
        self.metric_cards["tsfc"].set_value(f"{result.tsfc_lb_lbf_hr:.3f}", "lb/lbf/hr")
        self.metric_cards["fuel"].set_value(f"{result.fuel_flow_lb_hr:,.0f}", "lb/hr")
        self.metric_cards["eff"].set_value(f"{result.propulsive_efficiency:.2%}", "")

        rows = [
            ("0", "飛行環境", f"高度 {self.case.altitude_ft:,.0f} ft, Mach {self.case.mach:.2f}"),
            ("2", "風扇出口", f"FPR {result.fan_pressure_ratio:.2f}"),
            ("3", "壓縮機出口", f"OPR {self.case.overall_pressure_ratio:.1f}"),
            ("4", "燃燒室出口", f"Tt4 {self.case.turbine_inlet_temperature_k:.0f} K"),
            ("5", "渦輪出口", f"Tt5 {result.core_exit_temp_k:.0f} K"),
            ("8", "噴嘴/性能", f"Thrust {result.net_thrust_lbf:,.0f} lbf"),
        ]
        for row_index, row in enumerate(rows):
            for column, text in enumerate(row):
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.station_table.setItem(row_index, column, item)
        self.station_table.resizeColumnsToContents()
        if hasattr(self, "report_text"):
            self._write_report("zh")

    def _write_report(self, language: str) -> None:
        if language == "en":
            text = (
                "pyCycle Edu reference report\n\n"
                f"Engine case: {self.case.engine_name}\n"
                f"Bypass ratio: {self.case.bypass_ratio:.2f}\n"
                f"Overall pressure ratio: {self.case.overall_pressure_ratio:.1f}\n"
                f"Estimated net thrust: {self.result.net_thrust_lbf:,.0f} lbf\n"
                f"Estimated TSFC: {self.result.tsfc_lb_lbf_hr:.3f} lb/lbf/hr\n\n"
                "Note: this screen currently uses a teaching placeholder model. "
                "The next milestone will connect the UI to a pyCycle example problem and compare against curated reference sources."
            )
        else:
            text = (
                "pyCycle Edu 參考報告\n\n"
                f"發動機案例：{self.case.engine_name}\n"
                f"旁通比：{self.case.bypass_ratio:.2f}\n"
                f"總壓比：{self.case.overall_pressure_ratio:.1f}\n"
                f"估算淨推力：{self.result.net_thrust_lbf:,.0f} lbf\n"
                f"估算 TSFC：{self.result.tsfc_lb_lbf_hr:.3f} lb/lbf/hr\n\n"
                "注意：目前此畫面使用教學用估算模型。下一個里程碑會接上 pyCycle 範例問題，"
                "並與 Reference_sources 中整理的公開資料比對。"
            )
        self.report_text.setPlainText(text)

    def _show_runner_message(self) -> None:
        QMessageBox.information(
            self,
            "下一階段",
            "下一階段會新增 pyCycle runner：從 UI 參數建立 pyCycle problem，執行後回填表格、圖表與雙語報告。",
        )
