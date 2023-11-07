# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainBbHcoh.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
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
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(778, 566)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.combo_device = QComboBox(self.groupBox)
        self.combo_device.setObjectName("combo_device")
        self.combo_device.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.combo_device)

        self.flip = QCheckBox(self.groupBox)
        self.flip.setObjectName("flip")

        self.horizontalLayout_4.addWidget(self.flip)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(1, 100)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 3, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(200, 0))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.label_fps = QLabel(self.groupBox_2)
        self.label_fps.setObjectName("label_fps")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_fps.sizePolicy().hasHeightForWidth())
        self.label_fps.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label_fps)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.label_resolution = QLabel(self.groupBox_2)
        self.label_resolution.setObjectName("label_resolution")

        self.horizontalLayout_5.addWidget(self.label_resolution)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_6.addWidget(self.label_7)

        self.label_mouse_pos = QLabel(self.groupBox_2)
        self.label_mouse_pos.setObjectName("label_mouse_pos")

        self.horizontalLayout_6.addWidget(self.label_mouse_pos)

        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_7.addWidget(self.label_9)

        self.label_rate = QLabel(self.groupBox_2)
        self.label_rate.setObjectName("label_rate")
        self.label_rate.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_7.addWidget(self.label_rate)

        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_8.addWidget(self.label_11)

        self.label_encoder = QLabel(self.groupBox_2)
        self.label_encoder.setObjectName("label_encoder")

        self.horizontalLayout_8.addWidget(self.label_encoder)

        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.button_home = QPushButton(self.groupBox_3)
        self.button_home.setObjectName("button_home")
        self.button_home.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.button_home)

        self.button_back = QPushButton(self.groupBox_3)
        self.button_back.setObjectName("button_back")
        self.button_back.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.button_back)

        self.button_switch = QPushButton(self.groupBox_3)
        self.button_switch.setObjectName("button_switch")
        self.button_switch.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.button_switch)

        self.gridLayout.addWidget(self.groupBox_3, 1, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.button_record_click = QPushButton(self.groupBox_4)
        self.button_record_click.setObjectName("button_record_click")
        self.button_record_click.setMinimumSize(QSize(0, 40))

        self.verticalLayout_5.addWidget(self.button_record_click)

        self.button_take_region = QPushButton(self.groupBox_4)
        self.button_take_region.setObjectName("button_take_region")
        self.button_take_region.setMinimumSize(QSize(0, 40))

        self.verticalLayout_5.addWidget(self.button_take_region)

        self.button_show_log = QPushButton(self.groupBox_4)
        self.button_show_log.setObjectName("button_show_log")
        self.button_show_log.setMinimumSize(QSize(0, 40))

        self.verticalLayout_5.addWidget(self.button_show_log)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.gridLayout.addWidget(self.groupBox_4, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", "Frame", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Device", None))
        self.flip.setText(QCoreApplication.translate("MainWindow", "Flip", None))
        self.label.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:20pt;">Loading</span></p></body></html>',
                None,
            )
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("MainWindow", "Information", None)
        )
        self.label_3.setText(QCoreApplication.translate("MainWindow", "FPS", None))
        self.label_fps.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "Resolution", None)
        )
        self.label_resolution.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.label_7.setText(
            QCoreApplication.translate("MainWindow", "Mouse Position", None)
        )
        self.label_mouse_pos.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.label_9.setText(QCoreApplication.translate("MainWindow", "Rate", None))
        self.label_rate.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.label_11.setText(QCoreApplication.translate("MainWindow", "Encoder", None))
        self.label_encoder.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate("MainWindow", "Control", None)
        )
        self.button_home.setText(QCoreApplication.translate("MainWindow", "HOME", None))
        self.button_back.setText(QCoreApplication.translate("MainWindow", "BACK", None))
        self.button_switch.setText(
            QCoreApplication.translate("MainWindow", "SWITCH", None)
        )
        self.groupBox_4.setTitle(
            QCoreApplication.translate("MainWindow", "Develop", None)
        )
        self.button_record_click.setText(
            QCoreApplication.translate("MainWindow", "Record Mouse Click", None)
        )
        self.button_take_region.setText(
            QCoreApplication.translate("MainWindow", "Take Region", None)
        )
        self.button_show_log.setText(
            QCoreApplication.translate("MainWindow", "Show Log", None)
        )

    # retranslateUi
