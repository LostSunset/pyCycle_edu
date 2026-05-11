from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication


BACKGROUND = "#F6F1E8"
SURFACE = "#FFF9EF"
SURFACE_ALT = "#EFE5D6"
INK = "#2E2A24"
MUTED = "#6F665B"
ACCENT = "#B86B32"
ACCENT_DARK = "#7C4724"
BORDER = "#D7C8B8"
SUCCESS = "#487A5E"
WARNING = "#B1812C"
FONT_FAMILY = "Microsoft JhengHei UI"


def _load_cjk_font() -> str:
    candidates = [
        Path("C:/Windows/Fonts/msjh.ttc"),
        Path("C:/Windows/Fonts/NotoSansTC-Regular.otf"),
        Path("C:/Windows/Fonts/NotoSansCJKtc-Regular.otf"),
        Path("C:/Windows/Fonts/NotoSansHK-VF.ttf"),
        Path("C:/Windows/Fonts/mingliu.ttc"),
    ]
    for font_path in candidates:
        if not font_path.exists():
            continue
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            return families[0]
    return FONT_FAMILY


def apply_app_theme(app: QApplication) -> None:
    global FONT_FAMILY
    font_family = _load_cjk_font()
    FONT_FAMILY = font_family
    font = QFont(font_family)
    font.setPointSize(12)
    app.setFont(font)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(BACKGROUND))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(INK))
    palette.setColor(QPalette.ColorRole.Base, QColor(SURFACE))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(SURFACE_ALT))
    palette.setColor(QPalette.ColorRole.Text, QColor(INK))
    palette.setColor(QPalette.ColorRole.Button, QColor(SURFACE))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(INK))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)

    try:
        from qfluentwidgets import Theme, setTheme, setThemeColor

        setTheme(Theme.LIGHT)
        setThemeColor(ACCENT)
    except Exception:
        pass

    app.setStyleSheet(
        f"""
        QWidget {{
            background: {BACKGROUND};
            color: {INK};
            font-family: "{font_family}";
            font-size: 17px;
        }}
        QMainWindow, QDialog {{
            background: {BACKGROUND};
        }}
        QTabWidget#Ribbon::pane {{
            border: 0;
            border-bottom: 1px solid {BORDER};
            background: {SURFACE_ALT};
        }}
        QTabWidget#Ribbon QTabBar::tab {{
            background: {SURFACE_ALT};
            border: 0;
            border-right: 1px solid {BORDER};
            padding: 8px 18px;
            min-width: 112px;
            min-height: 28px;
            font-weight: 700;
        }}
        QTabWidget#Ribbon QTabBar::tab:selected {{
            background: {SURFACE};
            color: {ACCENT_DARK};
        }}
        QFrame#RibbonGroup {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 6px;
        }}
        QLabel#RibbonGroupTitle {{
            color: {MUTED};
            font-size: 13px;
        }}
        QLabel#PageTitle {{
            font-size: 30px;
            font-weight: 700;
            color: {INK};
        }}
        QLabel#SectionTitle {{
            font-size: 21px;
            font-weight: 700;
            color: {INK};
        }}
        QLabel#HintText {{
            color: {MUTED};
            font-size: 15px;
        }}
        QFrame#Panel, QFrame#MetricCard, QGroupBox {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 8px;
        }}
        QFrame#Sidebar {{
            background: {SURFACE_ALT};
            border-right: 1px solid {BORDER};
        }}
        QStatusBar {{
            background: {SURFACE_ALT};
            border-top: 1px solid {BORDER};
            color: {MUTED};
            font-size: 14px;
        }}
        QPushButton {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 7px;
            min-height: 40px;
            padding: 7px 14px;
        }}
        QPushButton:hover {{
            border-color: {ACCENT};
            color: {ACCENT_DARK};
        }}
        QPushButton#PrimaryButton {{
            background: {ACCENT};
            border-color: {ACCENT};
            color: white;
            font-weight: 700;
        }}
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit, QPlainTextEdit {{
            background: #FFFCF6;
            border: 1px solid {BORDER};
            border-radius: 6px;
            min-height: 36px;
            padding: 5px 8px;
        }}
        QTabWidget::pane {{
            border: 1px solid {BORDER};
            border-radius: 8px;
            background: {SURFACE};
        }}
        QTabBar::tab {{
            background: {SURFACE_ALT};
            border: 1px solid {BORDER};
            padding: 9px 16px;
            min-width: 120px;
        }}
        QTabBar::tab:selected {{
            background: {SURFACE};
            color: {ACCENT_DARK};
            font-weight: 700;
        }}
        QTableWidget {{
            background: #FFFCF6;
            gridline-color: {BORDER};
            selection-background-color: #EDD0B4;
        }}
        QHeaderView::section {{
            background: {SURFACE_ALT};
            border: 1px solid {BORDER};
            font-weight: 700;
            padding: 8px;
        }}
        """
    )
