import sys
from PySide6.QtWidgets import QApplication
app = QApplication([])
from .window_main import MainWindow

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