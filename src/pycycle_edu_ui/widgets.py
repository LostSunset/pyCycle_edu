from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from pycycle_edu_ui import theme


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, unit: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("MetricCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setObjectName("HintText")
        value_row = QHBoxLayout()
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 27px; font-weight: 800;")
        unit_label = QLabel(unit)
        unit_label.setObjectName("HintText")
        unit_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        value_row.addWidget(value_label)
        value_row.addWidget(unit_label)
        value_row.addStretch(1)
        layout.addWidget(title_label)
        layout.addLayout(value_row)

        self.value_label = value_label
        self.unit_label = unit_label

    def set_value(self, value: str, unit: str | None = None) -> None:
        self.value_label.setText(value)
        if unit is not None:
            self.unit_label.setText(unit)


class FlowDiagram(QWidget):
    labels = ["進氣", "風扇", "壓縮機", "燃燒室", "渦輪", "噴嘴"]

    def minimumSizeHint(self):  # type: ignore[override]
        return self.sizeHint()

    def sizeHint(self):  # type: ignore[override]
        from PySide6.QtCore import QSize

        return QSize(760, 230)

    def paintEvent(self, event):  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(22, 22, -22, -22)
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, QColor("#FFF8EC"))
        gradient.setColorAt(1, QColor("#EBDCCB"))
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(theme.BORDER), 2))
        painter.drawRoundedRect(rect, 8, 8)

        center_y = rect.center().y()
        start_x = rect.left() + 58
        end_x = rect.right() - 58
        step = (end_x - start_x) / (len(self.labels) - 1)

        painter.setPen(QPen(QColor(theme.ACCENT_DARK), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(QPointF(start_x, center_y), QPointF(end_x, center_y))
        painter.setPen(QPen(QColor(theme.MUTED), 2, Qt.PenStyle.DashLine))
        painter.drawArc(rect.adjusted(90, 42, -90, -42), 180 * 16, -180 * 16)

        font = QFont(theme.FONT_FAMILY, 12)
        font.setBold(True)
        painter.setFont(font)

        for index, label in enumerate(self.labels):
            x = start_x + index * step
            node_rect = rect.adjusted(0, 0, 0, 0)
            node_rect.setWidth(92)
            node_rect.setHeight(54)
            node_rect.moveCenter(QPointF(x, center_y).toPoint())
            painter.setBrush(QBrush(QColor("#FFFCF6")))
            painter.setPen(QPen(QColor(theme.ACCENT), 2))
            painter.drawRoundedRect(node_rect, 8, 8)
            painter.setPen(QColor(theme.INK))
            painter.drawText(node_rect, Qt.AlignmentFlag.AlignCenter, label)

        painter.setPen(QColor(theme.MUTED))
        painter.setFont(QFont(theme.FONT_FAMILY, 11))
        painter.drawText(rect.adjusted(22, 12, -22, -12), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight, "旁通流與核心流教學示意")
