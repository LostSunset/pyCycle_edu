from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
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
from pycycle_edu_ui.runner.hbtf_runner import PerformancePoint, PyCycleRunResult, run_high_bypass_turbofan
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
        self.run_result: PyCycleRunResult | None = None
        self.current_point: PerformancePoint | None = None

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
        self._refresh_empty_state()

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
        note = QLabel("實戰 app、報告與圖表輸出都保存在 Reference_answers。來源資料保存在 Reference_sources。")
        note.setObjectName("HintText")
        note.setWordWrap(True)
        layout.addWidget(note)
        return frame

    def _build_workbench_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        title = QLabel("CFM56-7B 對照用 pyCycle HBTF 實戰工作台")
        title.setObjectName("PageTitle")
        hint = QLabel("按下執行後會跑 upstream pyCycle high_bypass_turbofan.py，解析英文 viewer 報告，並與 CFM56-7B 公開資料做圖表比對。")
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

        title = QLabel("pyCycle 執行")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        info = QLabel(
            "目前實戰 app 會直接執行 upstream/pyCycle/example_cycles/high_bypass_turbofan.py。"
            "這是 pyCycle 自帶高旁通比渦扇範例；本專案只讀取它，不修改 upstream。"
        )
        info.setObjectName("HintText")
        info.setWordWrap(True)
        layout.addWidget(info)

        run_button = PrimaryPushButton("執行 pyCycle HBTF")
        run_button.setObjectName("PrimaryButton")
        run_button.clicked.connect(self._run_pycycle)
        layout.addWidget(run_button)

        zh_button = PushButton("產生正體中文報告")
        zh_button.clicked.connect(self._save_chinese_report)
        layout.addWidget(zh_button)

        self.progress = QProgressBar()
        self.progress.setRange(0, 1)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.run_status = QLabel("尚未執行。")
        self.run_status.setObjectName("HintText")
        self.run_status.setWordWrap(True)
        layout.addWidget(self.run_status)

        source_title = QLabel("比對來源")
        source_title.setObjectName("SectionTitle")
        layout.addWidget(source_title)
        for metric in CFM56_7B_REFERENCE:
            label = QLabel(f"{metric.zh_name}: {metric.value:g} {metric.unit}")
            label.setObjectName("HintText")
            label.setWordWrap(True)
            layout.addWidget(label)

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
        table.setHorizontalHeaderLabels(["項目", "pyCycle", "CFM56-7B 參考", "單位", "判讀"])
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
        self.comparison_plot_panel = self._build_comparison_plot_panel()
        tabs.addTab(self.comparison_plot_panel, "CFM56-7B 比對圖")
        tabs.addTab(self._build_points_table_panel(), "pyCycle 工作點")
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
        self.comparison_plot.setLabel("left", "正規化數值")
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
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

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

    def _spin(self, minimum: float, maximum: float, value: float, step: float) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(minimum, maximum)
        spin.setValue(value)
        spin.setSingleStep(step)
        spin.setDecimals(2 if step < 0.1 else 1)
        spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        return spin

    def _run_pycycle(self) -> None:
        self.progress.setRange(0, 0)
        self.run_status.setText("正在執行 pyCycle high_bypass_turbofan.py，請稍候...")
        QApplication.processEvents()
        result = run_high_bypass_turbofan()
        self.run_result = result
        self.current_point = select_design_point(result.points)
        self.progress.setRange(0, 1)
        self.progress.setValue(1 if result.ok else 0)
        if result.ok:
            self.run_status.setText(f"完成：解析 {len(result.points)} 個 pyCycle performance points。英文報告：{result.english_report}")
        else:
            self.run_status.setText(f"執行失敗：{result.error}\n{result.stderr[-900:]}")
        self._refresh_results()

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
            ("OPR", f"{point.overall_pressure_ratio:.3f}", f"{refs['overall_pressure_ratio'].value:.1f}", "-", "受範例假設影響，做量級檢查"),
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
        x1 = [1, 3]
        x2 = [1.6, 3.6]
        self.comparison_plot.addLegend()
        self.comparison_plot.plot(x1, pycycle_values, pen=None, symbol="o", symbolSize=16, symbolBrush="#B86B32", name="pyCycle")
        self.comparison_plot.plot(x2, ref_values, pen=None, symbol="s", symbolSize=16, symbolBrush="#487A5E", name="CFM56-7B reference")
        axis = self.comparison_plot.getAxis("bottom")
        axis.setTicks([[(1.3, labels[0]), (3.3, labels[1])]])

    def _save_chinese_report(self) -> None:
        if self.run_result is None:
            QMessageBox.warning(self, "尚未執行", "請先執行 pyCycle HBTF。")
            return
        output = save_chinese_report(self.run_result)
        self.report_text.setPlainText(build_chinese_report(self.run_result))
        QMessageBox.information(self, "已儲存", f"正體中文報告已儲存：\n{output}")

    def _show_english_report_message(self) -> None:
        if self.run_result is None:
            QMessageBox.warning(self, "尚未執行", "請先執行 pyCycle HBTF。")
            return
        QMessageBox.information(self, "pyCycle 英文 viewer", str(self.run_result.english_report))
