from __future__ import annotations

from PySide6.QtCore import QObject, Qt, QThread, Signal, Slot
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
    QProgressBar,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pycycle_edu_ui.reference_data import CFM56_7B_REFERENCE, reference_by_key
from pycycle_edu_ui.reports import build_chinese_report, save_chinese_report, select_design_point
from pycycle_edu_ui.runner.hbtf_runner import (
    EngineInputs,
    PerformancePoint,
    PyCycleRunResult,
    run_high_bypass_turbofan,
)
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


class PyCycleWorker(QObject):
    finished = Signal(object)

    def __init__(self, inputs: EngineInputs) -> None:
        super().__init__()
        self.inputs = inputs

    @Slot()
    def run(self) -> None:
        self.finished.emit(run_high_bypass_turbofan(self.inputs))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("pyCycle CFM56-7B 工程分析工作台")
        self.run_result: PyCycleRunResult | None = None
        self.current_point: PerformancePoint | None = None
        self.worker_thread: QThread | None = None
        self.worker: PyCycleWorker | None = None

        self.stack = QStackedWidget()
        self.metric_cards: dict[str, MetricCard] = {}
        self.inputs: dict[str, QDoubleSpinBox] = {}
        self.run_buttons: list[QPushButton] = []

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(self._build_ribbon())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(self._build_sidebar())
        body.addWidget(self.stack, 1)
        root_layout.addLayout(body, 1)
        self.setCentralWidget(root)

        self.stack.addWidget(self._build_workbench_page())
        self.stack.addWidget(self._build_results_page())
        self.stack.addWidget(self._build_report_page())
        self.stack.addWidget(self._build_sources_page())

        self.statusBar().showMessage("就緒")
        self._refresh_empty_state()

    def _build_ribbon(self) -> QWidget:
        ribbon = QTabWidget()
        ribbon.setObjectName("Ribbon")
        ribbon.setFixedHeight(136)
        ribbon.addTab(self._ribbon_model_tab(), "模型設定")
        ribbon.addTab(self._ribbon_run_tab(), "執行計算")
        ribbon.addTab(self._ribbon_results_tab(), "結果圖表")
        ribbon.addTab(self._ribbon_report_tab(), "報告輸出")
        ribbon.addTab(self._ribbon_sources_tab(), "資料來源")
        return ribbon

    def _ribbon_model_tab(self) -> QWidget:
        return self._ribbon_tab(
            [
                ("案例", [("CFM56-7B 參考模型", lambda: self.stack.setCurrentIndex(0))]),
                ("輸入", [("檢查輸入", self._show_input_validation), ("重設預設", self._reset_inputs)]),
            ]
        )

    def _ribbon_run_tab(self) -> QWidget:
        run_button = self._make_ribbon_button("執行 pyCycle", self._run_pycycle)
        self.run_buttons.append(run_button)
        return self._ribbon_tab(
            [
                ("計算", [run_button]),
                ("輸出", [("開啟結果表", lambda: self.stack.setCurrentIndex(1))]),
            ]
        )

    def _ribbon_results_tab(self) -> QWidget:
        return self._ribbon_tab(
            [
                ("檢視", [("比對圖表", lambda: self.stack.setCurrentIndex(1)), ("工作點表", lambda: self.stack.setCurrentIndex(1))]),
                ("檢查", [("更新圖表", self._refresh_results)]),
            ]
        )

    def _ribbon_report_tab(self) -> QWidget:
        return self._ribbon_tab(
            [
                ("報告", [("儲存中文報告", self._save_chinese_report), ("英文 viewer 路徑", self._show_english_report_message)]),
                ("檢視", [("報告頁", lambda: self.stack.setCurrentIndex(2))]),
            ]
        )

    def _ribbon_sources_tab(self) -> QWidget:
        return self._ribbon_tab(
            [
                ("來源", [("資料來源頁", lambda: self.stack.setCurrentIndex(3))]),
                ("限制", [("模型限制", self._show_model_limitations)]),
            ]
        )

    def _ribbon_tab(self, groups: list[tuple[str, list[tuple[str, object] | QPushButton]]]) -> QWidget:
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(10)
        for title, actions in groups:
            frame = QFrame()
            frame.setObjectName("RibbonGroup")
            group_layout = QVBoxLayout(frame)
            group_layout.setContentsMargins(10, 8, 10, 8)
            group_layout.setSpacing(6)
            row = QHBoxLayout()
            row.setSpacing(6)
            for action in actions:
                if isinstance(action, QPushButton):
                    button = action
                else:
                    text, callback = action
                    button = self._make_ribbon_button(text, callback)
                row.addWidget(button)
            label = QLabel(title)
            label.setObjectName("RibbonGroupTitle")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            group_layout.addLayout(row, 1)
            group_layout.addWidget(label)
            layout.addWidget(frame)
        layout.addStretch(1)
        return page

    def _make_ribbon_button(self, text: str, callback: object) -> QPushButton:
        button = PushButton(text)
        button.setMinimumSize(120, 44)
        button.clicked.connect(callback)  # type: ignore[arg-type]
        return button

    def _build_sidebar(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(238)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 24, 18, 18)
        layout.setSpacing(12)

        title = QLabel("pyCycle\nCFM56-7B")
        title.setStyleSheet("font-size: 21px; font-weight: 800;")
        title.setWordWrap(True)
        subtitle = QLabel("工程分析工作台")
        subtitle.setObjectName("HintText")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(18)

        buttons = [
            ("模型設定", 0),
            ("結果圖表", 1),
            ("報告輸出", 2),
            ("資料來源", 3),
        ]
        for text, index in buttons:
            button = PushButton(text)
            button.setMinimumHeight(42)
            button.clicked.connect(lambda checked=False, page=index: self.stack.setCurrentIndex(page))
            layout.addWidget(button)

        layout.addStretch(1)
        note = QLabel("計算輸出保存在 Reference_answers；公開資料保存在 Reference_sources。")
        note.setObjectName("HintText")
        note.setWordWrap(True)
        layout.addWidget(note)
        return frame

    def _build_workbench_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 22, 28, 24)
        layout.setSpacing(16)

        title = QLabel("CFM56-7B 參考模型與 pyCycle 計算")
        title.setObjectName("PageTitle")
        hint = QLabel("輸入工程條件後執行 pyCycle HBTF wrapper；計算完成後會更新結果摘要、比對圖表與報告草稿。")
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
        panel.setFixedWidth(430)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        title = QLabel("工程參數")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        case_combo = QComboBox()
        case_combo.addItems(["CFM56-7B 參考模型", "pyCycle HBTF 基準"])
        layout.addWidget(case_combo)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        self.inputs = {
            "mach": self._spin(0.0, 0.95, 0.8, 0.01, 2, "巡航馬赫數，範圍 0.00-0.95"),
            "altitude_ft": self._spin(0.0, 45000.0, 35000.0, 500.0, 0, "飛行高度，單位 ft"),
            "t4_max_deg_r": self._spin(2000.0, 3400.0, 2857.0, 10.0, 0, "燃燒室出口總溫 T4/Tt4，單位 degR"),
            "fn_target_lbf": self._spin(1000.0, 30000.0, 5900.0, 100.0, 0, "設計點目標淨推力，單位 lbf"),
            "bypass_ratio": self._spin(2.0, 10.0, 5.105, 0.005, 3, "旁通比 BPR"),
            "fan_pressure_ratio": self._spin(1.1, 2.2, 1.685, 0.001, 3, "Fan pressure ratio"),
            "lpc_pressure_ratio": self._spin(1.1, 4.0, 1.935, 0.001, 3, "Low pressure compressor PR"),
            "hpc_pressure_ratio": self._spin(4.0, 18.0, 9.369, 0.001, 3, "High pressure compressor PR"),
            "percent_thrust": self._spin(0.3, 1.0, 0.8, 0.05, 2, "Off-design percent thrust，0.30-1.00"),
        }
        labels = {
            "mach": "Mach",
            "altitude_ft": "Altitude ft",
            "t4_max_deg_r": "T4 / Tt4 degR",
            "fn_target_lbf": "Fn target lbf",
            "bypass_ratio": "BPR",
            "fan_pressure_ratio": "Fan PR",
            "lpc_pressure_ratio": "LPC PR",
            "hpc_pressure_ratio": "HPC PR",
            "percent_thrust": "Percent thrust",
        }
        for key, widget in self.inputs.items():
            form.addRow(labels[key], widget)
        layout.addLayout(form)

        run_button = PrimaryPushButton("執行 pyCycle 計算")
        run_button.setObjectName("PrimaryButton")
        run_button.clicked.connect(self._run_pycycle)
        self.run_buttons.append(run_button)
        layout.addWidget(run_button)

        self.progress = QProgressBar()
        self.progress.setRange(0, 1)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.run_status = QLabel("就緒。")
        self.run_status.setObjectName("HintText")
        self.run_status.setWordWrap(True)
        layout.addWidget(self.run_status)
        layout.addStretch(1)
        return panel

    def _build_overview_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        title = QLabel("流程、摘要與比對")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)
        layout.addWidget(FlowDiagram())

        grid = QGridLayout()
        grid.setSpacing(12)
        specs = [
            ("thrust", "pyCycle 淨推力", "--", "lbf"),
            ("tsfc", "TSFC", "--", "lb/lbf/hr"),
            ("opr", "OPR", "--", ""),
            ("bpr", "BPR", "--", ""),
        ]
        for index, (key, title_text, value, unit) in enumerate(specs):
            card = MetricCard(title_text, value, unit)
            self.metric_cards[key] = card
            grid.addWidget(card, index // 2, index % 2)
        layout.addLayout(grid)

        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(["項目", "pyCycle", "CFM56-7B", "單位", "工程判讀"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 120)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 80)
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.station_table = table
        layout.addWidget(table, 1)
        return panel

    def _build_results_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 22, 28, 24)
        layout.setSpacing(16)

        title = QLabel("結果圖表")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        tabs = QTabWidget()
        self.comparison_plot_panel = self._build_comparison_plot_panel()
        tabs.addTab(self.comparison_plot_panel, "BPR / OPR 比對")
        tabs.addTab(self._build_points_table_panel(), "DESIGN / OD 工作點")
        layout.addWidget(tabs, 1)
        return page

    def _build_comparison_plot_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)

        if pg is None:
            label = QLabel("尚未安裝 pyqtgraph；請用 uv sync 後再開啟圖表。")
            label.setObjectName("HintText")
            layout.addWidget(label)
            return panel

        self.comparison_plot = pg.PlotWidget()
        self.comparison_plot.setBackground("#FFFCF6")
        self.comparison_plot.showGrid(x=True, y=True, alpha=0.25)
        self.comparison_plot.addLegend()
        self.comparison_plot.setLabel("bottom", "比對項目")
        self.comparison_plot.setLabel("left", "數值")
        layout.addWidget(self.comparison_plot)
        return panel

    def _build_points_table_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)
        self.points_table = QTableWidget(0, 8)
        self.points_table.setHorizontalHeaderLabels(["Point", "Mach", "Alt ft", "Fn", "Fg", "OPR", "TSFC", "BPR"])
        self.points_table.verticalHeader().setVisible(False)
        self.points_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.points_table)
        return panel

    def _build_report_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 22, 28, 24)
        layout.setSpacing(16)

        title = QLabel("正體中文報告與 pyCycle 英文 viewer")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        self.report_text = QPlainTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text, 1)

        row = QHBoxLayout()
        zh_button = PrimaryPushButton("儲存正體中文報告")
        zh_button.setObjectName("PrimaryButton")
        en_button = PushButton("顯示英文 viewer 路徑")
        zh_button.clicked.connect(self._save_chinese_report)
        en_button.clicked.connect(self._show_english_report_message)
        row.addWidget(zh_button)
        row.addWidget(en_button)
        row.addStretch(1)
        layout.addLayout(row)
        return page

    def _build_sources_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 22, 28, 24)
        layout.setSpacing(16)
        title = QLabel("資料來源與模型限制")
        title.setObjectName("PageTitle")
        layout.addWidget(title)
        table = QTableWidget(len(CFM56_7B_REFERENCE), 5)
        table.setHorizontalHeaderLabels(["欄位", "參考值", "單位", "來源", "備註"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        for row, metric in enumerate(CFM56_7B_REFERENCE):
            values = [metric.zh_name, f"{metric.value:g}", metric.unit, metric.source, metric.note]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                table.setItem(row, column, item)
        table.resizeColumnsToContents()
        layout.addWidget(table, 1)
        return page

    def _spin(self, minimum: float, maximum: float, value: float, step: float, decimals: int, tooltip: str) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(minimum, maximum)
        spin.setDecimals(decimals)
        spin.setSingleStep(step)
        spin.setValue(value)
        spin.setToolTip(tooltip)
        spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        return spin

    def _collect_inputs(self) -> EngineInputs:
        return EngineInputs(
            mach=self.inputs["mach"].value(),
            altitude_ft=self.inputs["altitude_ft"].value(),
            t4_max_deg_r=self.inputs["t4_max_deg_r"].value(),
            fn_target_lbf=self.inputs["fn_target_lbf"].value(),
            bypass_ratio=self.inputs["bypass_ratio"].value(),
            fan_pressure_ratio=self.inputs["fan_pressure_ratio"].value(),
            lpc_pressure_ratio=self.inputs["lpc_pressure_ratio"].value(),
            hpc_pressure_ratio=self.inputs["hpc_pressure_ratio"].value(),
            percent_thrust=self.inputs["percent_thrust"].value(),
        )

    def _validate_inputs(self) -> bool:
        inputs = self._collect_inputs()
        total_pr = inputs.fan_pressure_ratio * inputs.lpc_pressure_ratio * inputs.hpc_pressure_ratio
        if total_pr < 10 or total_pr > 45:
            QMessageBox.warning(self, "輸入檢查", f"目前估算總壓比約 {total_pr:.1f}，請確認 Fan/LPC/HPC PR 是否合理。")
            return False
        return True

    def _show_input_validation(self) -> None:
        inputs = self._collect_inputs()
        total_pr = inputs.fan_pressure_ratio * inputs.lpc_pressure_ratio * inputs.hpc_pressure_ratio
        if self._validate_inputs():
            QMessageBox.information(self, "輸入檢查", f"輸入檢查通過。\n估算總壓比：約 {total_pr:.1f}")
            self.statusBar().showMessage(f"輸入檢查通過，估算總壓比約 {total_pr:.1f}", 6000)

    def _reset_inputs(self) -> None:
        defaults = EngineInputs()
        mapping = {
            "mach": defaults.mach,
            "altitude_ft": defaults.altitude_ft,
            "t4_max_deg_r": defaults.t4_max_deg_r,
            "fn_target_lbf": defaults.fn_target_lbf,
            "bypass_ratio": defaults.bypass_ratio,
            "fan_pressure_ratio": defaults.fan_pressure_ratio,
            "lpc_pressure_ratio": defaults.lpc_pressure_ratio,
            "hpc_pressure_ratio": defaults.hpc_pressure_ratio,
            "percent_thrust": defaults.percent_thrust,
        }
        for key, value in mapping.items():
            self.inputs[key].setValue(value)
        self.statusBar().showMessage("已重設預設工程參數", 5000)

    def _run_pycycle(self) -> None:
        if self.worker_thread is not None:
            QMessageBox.information(self, "計算進行中", "pyCycle 計算尚未完成。")
            return
        if not self._validate_inputs():
            return
        inputs = self._collect_inputs()
        self.progress.setRange(0, 0)
        self.run_status.setText("pyCycle 計算中...")
        self.statusBar().showMessage("pyCycle 計算中，UI 可繼續操作。")
        for button in self.run_buttons:
            button.setEnabled(False)

        self.worker_thread = QThread(self)
        self.worker = PyCycleWorker(inputs)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._handle_run_finished)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self._cleanup_worker)
        self.worker_thread.start()

    @Slot(object)
    def _handle_run_finished(self, result: PyCycleRunResult) -> None:
        self.run_result = result
        self.current_point = select_design_point(result.points)
        self.progress.setRange(0, 1)
        self.progress.setValue(1 if result.ok else 0)
        for button in self.run_buttons:
            button.setEnabled(True)

        if result.ok:
            self.run_status.setText(
                f"完成：{len(result.points)} 個工作點，{result.elapsed_seconds:.1f} s\n英文 viewer：{result.english_report}"
            )
            self.statusBar().showMessage(f"pyCycle 計算完成，輸出：{result.english_report}", 12000)
        else:
            self.run_status.setText(f"計算失敗：{result.error}\n{result.stderr[-900:]}")
            self.statusBar().showMessage("pyCycle 計算失敗，請檢查狀態訊息。", 12000)
        self._refresh_results()

    @Slot()
    def _cleanup_worker(self) -> None:
        self.worker_thread = None
        self.worker = None

    def _refresh_results(self) -> None:
        point = self.current_point
        if point is None:
            self._refresh_empty_state()
            return
        self.metric_cards["thrust"].set_value(f"{point.net_thrust_lbf:,.0f}", "lbf")
        self.metric_cards["tsfc"].set_value(f"{point.tsfc:.5f}", "lb/lbf/hr")
        self.metric_cards["opr"].set_value(f"{point.overall_pressure_ratio:.2f}", "")
        self.metric_cards["bpr"].set_value(f"{point.bypass_ratio:.3f}", "")

        refs = reference_by_key()
        rows = [
            ("BPR", f"{point.bypass_ratio:.3f}", f"{refs['bypass_ratio'].value:.1f}", "-", "設計點量級可直接比對"),
            ("OPR", f"{point.overall_pressure_ratio:.3f}", f"{refs['overall_pressure_ratio'].value:.1f}", "-", "受參考模型假設影響，做量級檢查"),
            ("巡航 Fn", f"{point.net_thrust_lbf:,.1f}", "19,500-27,300", "lbf", "pyCycle 為巡航點；參考值為海平面靜推力"),
            ("TSFC", f"{point.tsfc:.5f}", "公開資料依工況不同", "lb/lbf/hr", "需後續加入同工況資料才可嚴格驗證"),
            ("Fan diameter", "pyCycle 範例未輸出", "61", "in", "保留為來源對照，不畫誤差"),
        ]
        self.station_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column, text in enumerate(row):
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.station_table.setItem(row_index, column, item)
        self.station_table.resizeColumnsToContents()
        self._refresh_points_table()
        self._refresh_comparison_plot()
        if hasattr(self, "report_text") and self.run_result:
            self.report_text.setPlainText(build_chinese_report(self.run_result))

    def _refresh_empty_state(self) -> None:
        for key in ["thrust", "tsfc", "opr", "bpr"]:
            if key in self.metric_cards:
                self.metric_cards[key].set_value("--", "")
        if hasattr(self, "station_table"):
            self.station_table.setRowCount(0)

    def _refresh_points_table(self) -> None:
        if not hasattr(self, "points_table") or self.run_result is None:
            return
        points = self.run_result.points
        self.points_table.setRowCount(len(points))
        for row_index, point in enumerate(points):
            values = [
                point.point,
                f"{point.mach:.3f}",
                f"{point.altitude_ft:,.0f}",
                f"{point.net_thrust_lbf:,.1f}",
                f"{point.gross_thrust_lbf:,.1f}",
                f"{point.overall_pressure_ratio:.3f}",
                f"{point.tsfc:.5f}",
                f"{point.bypass_ratio:.3f}",
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.points_table.setItem(row_index, column, item)
        self.points_table.resizeColumnsToContents()

    def _refresh_comparison_plot(self) -> None:
        if pg is None or not hasattr(self, "comparison_plot") or self.current_point is None:
            return
        self.comparison_plot.clear()
        refs = reference_by_key()
        labels = ["BPR", "OPR"]
        pycycle_values = [self.current_point.bypass_ratio, self.current_point.overall_pressure_ratio]
        ref_values = [refs["bypass_ratio"].value, refs["overall_pressure_ratio"].value]
        self.comparison_plot.addLegend()
        self.comparison_plot.plot([1, 3], pycycle_values, pen=None, symbol="o", symbolSize=16, symbolBrush="#B86B32", name="pyCycle")
        self.comparison_plot.plot([1.6, 3.6], ref_values, pen=None, symbol="s", symbolSize=16, symbolBrush="#487A5E", name="CFM56-7B 參考")
        axis = self.comparison_plot.getAxis("bottom")
        axis.setTicks([[(1.3, labels[0]), (3.3, labels[1])]])

    def _save_chinese_report(self) -> None:
        if self.run_result is None:
            QMessageBox.warning(self, "尚未執行", "請先執行 pyCycle 計算。")
            return
        output = save_chinese_report(self.run_result)
        self.report_text.setPlainText(build_chinese_report(self.run_result))
        self.statusBar().showMessage(f"正體中文報告已儲存：{output}", 12000)
        QMessageBox.information(self, "已儲存", f"正體中文報告已儲存：\n{output}")

    def _show_english_report_message(self) -> None:
        if self.run_result is None:
            QMessageBox.warning(self, "尚未執行", "請先執行 pyCycle 計算。")
            return
        QMessageBox.information(self, "pyCycle 英文 viewer", str(self.run_result.english_report))

    def _show_model_limitations(self) -> None:
        QMessageBox.information(
            self,
            "模型限制",
            "目前使用 pyCycle HBTF 參考模型與 CFM56-7B 公開資料做工程等級比對；"
            "這不是 CFM56-7B 原廠 engine deck，也不能把巡航淨推力直接等同海平面靜推力。",
        )
