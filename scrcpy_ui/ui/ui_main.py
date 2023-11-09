# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainYwypDX.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(778, 566)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.combo_device = QComboBox(self.groupBox)
        self.combo_device.setObjectName(u"combo_device")
        self.combo_device.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.combo_device)

        self.flip = QCheckBox(self.groupBox)
        self.flip.setObjectName(u"flip")

        self.horizontalLayout_4.addWidget(self.flip)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(1, 100)

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 3, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(200, 0))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.label_fps = QLabel(self.groupBox_2)
        self.label_fps.setObjectName(u"label_fps")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_fps.sizePolicy().hasHeightForWidth())
        self.label_fps.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label_fps)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.label_resolution = QLabel(self.groupBox_2)
        self.label_resolution.setObjectName(u"label_resolution")

        self.horizontalLayout_5.addWidget(self.label_resolution)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_6.addWidget(self.label_7)

        self.label_mouse_pos = QLabel(self.groupBox_2)
        self.label_mouse_pos.setObjectName(u"label_mouse_pos")

        self.horizontalLayout_6.addWidget(self.label_mouse_pos)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_7.addWidget(self.label_9)

        self.label_rate = QLabel(self.groupBox_2)
        self.label_rate.setObjectName(u"label_rate")
        self.label_rate.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_7.addWidget(self.label_rate)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_8.addWidget(self.label_11)

        self.label_encoder = QLabel(self.groupBox_2)
        self.label_encoder.setObjectName(u"label_encoder")

        self.horizontalLayout_8.addWidget(self.label_encoder)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.button_home = QPushButton(self.groupBox_3)
        self.button_home.setObjectName(u"button_home")
        self.button_home.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.button_home)

        self.button_back = QPushButton(self.groupBox_3)
        self.button_back.setObjectName(u"button_back")
        self.button_back.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.button_back)

        self.button_switch = QPushButton(self.groupBox_3)
        self.button_switch.setObjectName(u"button_switch")
        self.button_switch.setMinimumSize(QSize(0, 40))

        self.verticalLayout_4.addWidget(self.button_switch)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_screen_off = QPushButton(self.groupBox_3)
        self.button_screen_off.setObjectName(u"button_screen_off")
        self.button_screen_off.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.button_screen_off)

        self.button_screen_on = QPushButton(self.groupBox_3)
        self.button_screen_on.setObjectName(u"button_screen_on")
        self.button_screen_on.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.button_screen_on)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.gridLayout.addWidget(self.groupBox_3, 1, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.button_record_click = QPushButton(self.groupBox_4)
        self.button_record_click.setObjectName(u"button_record_click")
        self.button_record_click.setMinimumSize(QSize(0, 40))

        self.verticalLayout_5.addWidget(self.button_record_click)

        self.button_take_region = QPushButton(self.groupBox_4)
        self.button_take_region.setObjectName(u"button_take_region")
        self.button_take_region.setMinimumSize(QSize(0, 40))

        self.verticalLayout_5.addWidget(self.button_take_region)

        self.button_show_log = QPushButton(self.groupBox_4)
        self.button_show_log.setObjectName(u"button_show_log")
        self.button_show_log.setMinimumSize(QSize(0, 40))

        self.verticalLayout_5.addWidget(self.button_show_log)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.groupBox_4, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Frame", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Device", None))
        self.flip.setText(QCoreApplication.translate("MainWindow", u"Flip", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:20pt;\">Loading</span></p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Information", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"FPS", None))
        self.label_fps.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.label_resolution.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Mouse Position", None))
        self.label_mouse_pos.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Rate", None))
        self.label_rate.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Encoder", None))
        self.label_encoder.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Control", None))
        self.button_home.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.button_back.setText(QCoreApplication.translate("MainWindow", u"BACK", None))
        self.button_switch.setText(QCoreApplication.translate("MainWindow", u"SWITCH", None))
        self.button_screen_off.setText(QCoreApplication.translate("MainWindow", u"SCREEN OFF", None))
        self.button_screen_on.setText(QCoreApplication.translate("MainWindow", u"SCREEN ON", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Develop", None))
        self.button_record_click.setText(QCoreApplication.translate("MainWindow", u"Record Mouse Click", None))
        self.button_take_region.setText(QCoreApplication.translate("MainWindow", u"Take Region", None))
        self.button_show_log.setText(QCoreApplication.translate("MainWindow", u"Show Log", None))
    # retranslateUi

