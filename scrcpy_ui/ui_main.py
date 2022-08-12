# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(935, 679)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setEnabled(True)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 16, -1, -1)
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_info_title = QLabel(self.centralwidget)
        self.label_info_title.setObjectName("label_info_title")

        self.horizontalLayout_3.addWidget(self.label_info_title)

        self.label_info_content = QLabel(self.centralwidget)
        self.label_info_content.setObjectName("label_info_content")

        self.horizontalLayout_3.addWidget(self.label_info_content)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.input_search = QLineEdit(self.centralwidget)
        self.input_search.setObjectName("input_search")

        self.horizontalLayout_3.addWidget(self.input_search)

        self.button_search = QPushButton(self.centralwidget)
        self.button_search.setObjectName("button_search")

        self.horizontalLayout_3.addWidget(self.button_search)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table_devices = QTableWidget(self.centralwidget)
        if self.table_devices.columnCount() < 6:
            self.table_devices.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_devices.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_devices.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_devices.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_devices.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_devices.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_devices.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.table_devices.setObjectName("table_devices")

        self.horizontalLayout.addWidget(self.table_devices)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkbox_devices = QCheckBox(self.centralwidget)
        self.checkbox_devices.setObjectName("checkbox_devices")

        self.horizontalLayout_2.addWidget(self.checkbox_devices)

        self.button_all_satrt = QPushButton(self.centralwidget)
        self.button_all_satrt.setObjectName("button_all_satrt")

        self.horizontalLayout_2.addWidget(self.button_all_satrt)

        self.button_all_stop = QPushButton(self.centralwidget)
        self.button_all_stop.setObjectName("button_all_stop")

        self.horizontalLayout_2.addWidget(self.button_all_stop)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 935, 24))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.label_info_title.setText(
            QCoreApplication.translate("MainWindow", "Info: ", None)
        )
        self.label_info_content.setText("")
        self.button_search.setText(
            QCoreApplication.translate("MainWindow", "Search", None)
        )
        ___qtablewidgetitem = self.table_devices.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("MainWindow", "Device", None)
        )
        ___qtablewidgetitem1 = self.table_devices.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("MainWindow", "Serial Number", None)
        )
        ___qtablewidgetitem2 = self.table_devices.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("MainWindow", "Run Mode", None)
        )
        ___qtablewidgetitem3 = self.table_devices.horizontalHeaderItem(4)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("MainWindow", "Operate", None)
        )
        ___qtablewidgetitem4 = self.table_devices.horizontalHeaderItem(5)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("MainWindow", "Others", None)
        )
        self.checkbox_devices.setText(
            QCoreApplication.translate("MainWindow", "CheckAll", None)
        )
        self.button_all_satrt.setText(
            QCoreApplication.translate("MainWindow", "All Start", None)
        )
        self.button_all_stop.setText(
            QCoreApplication.translate("MainWindow", "All Stop", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("MainWindow", "Setting", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))

    # retranslateUi
