import sys

from PySide6.QtWidgets import QApplication

from .window_main import MainWindow

app = QApplication([])


def main():
    # dialog = LoginDialog()
    # if dialog.exec() == QDialog.Accepted:
    #     m = MainWindow(dialog.account_info)
    #     m.show()

    # s = ScreenWindow()
    # s.show()
    m = MainWindow()
    m.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
