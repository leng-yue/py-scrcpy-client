# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
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
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
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
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(935, 679)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 16, -1, -1)
        self.combobox_sort = QComboBox(self.centralwidget)
        self.combobox_sort.setObjectName(u"combobox_sort")

        self.horizontalLayout_3.addWidget(self.combobox_sort)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.input_search = QLineEdit(self.centralwidget)
        self.input_search.setObjectName(u"input_search")

        self.horizontalLayout_3.addWidget(self.input_search)

        self.button_search = QPushButton(self.centralwidget)
        self.button_search.setObjectName(u"button_search")

        self.horizontalLayout_3.addWidget(self.button_search)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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
        self.table_devices.setObjectName(u"table_devices")

        self.horizontalLayout.addWidget(self.table_devices)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkbox_devices = QCheckBox(self.centralwidget)
        self.checkbox_devices.setObjectName(u"checkbox_devices")

        self.horizontalLayout_2.addWidget(self.checkbox_devices)

        self.button_all_stop = QPushButton(self.centralwidget)
        self.button_all_stop.setObjectName(u"button_all_stop")

        self.horizontalLayout_2.addWidget(self.button_all_stop)

        self.button_all_satrt = QPushButton(self.centralwidget)
        self.button_all_satrt.setObjectName(u"button_all_satrt")

        self.horizontalLayout_2.addWidget(self.button_all_satrt)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 935, 24))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"MainWindow", None)
        )
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", u"About", None)
        )
        self.button_search.setText(
            QCoreApplication.translate("MainWindow", u"Search", None)
        )
        ___qtablewidgetitem = self.table_devices.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("MainWindow", u"Device", None)
        )
        ___qtablewidgetitem1 = self.table_devices.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("MainWindow", u"Serial Number", None)
        )
        ___qtablewidgetitem2 = self.table_devices.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("MainWindow", u"Status", None)
        )
        ___qtablewidgetitem3 = self.table_devices.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("MainWindow", u"Run Mode", None)
        )
        ___qtablewidgetitem4 = self.table_devices.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("MainWindow", u"Operate", None)
        )
        ___qtablewidgetitem5 = self.table_devices.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("MainWindow", u"Others", None)
        )
        self.checkbox_devices.setText(
            QCoreApplication.translate("MainWindow", u"CheckAll", None)
        )
        self.button_all_stop.setText(
            QCoreApplication.translate("MainWindow", u"All Stop", None)
        )
        self.button_all_satrt.setText(
            QCoreApplication.translate("MainWindow", u"All Start", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("MainWindow", u"Setting", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))

    # retranslateUi
