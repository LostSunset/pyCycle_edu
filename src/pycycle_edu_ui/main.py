from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from pycycle_edu_ui.theme import apply_app_theme
from pycycle_edu_ui.views.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("pyCycle Edu Workbench")
    app.setOrganizationName("pyCycle Edu")
    apply_app_theme(app)

    window = MainWindow()
    window.resize(1320, 820)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
