# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frame_viewerIXWQEi.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtWidgets import (
    QGraphicsView,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class Ui_FrameViewer(object):
    def __init__(self, view_type=None):
        self.graphics_view_type = view_type or QGraphicsView

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(866, 575)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(180, 0))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_4.addWidget(self.label_7)

        self.label_picture_resolution = QLabel(self.groupBox_2)
        self.label_picture_resolution.setObjectName("label_picture_resolution")

        self.horizontalLayout_4.addWidget(self.label_picture_resolution)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.label)

        self.label_picture_zoom = QLabel(self.groupBox_2)
        self.label_picture_zoom.setObjectName("label_picture_zoom")

        self.horizontalLayout.addWidget(self.label_picture_zoom)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_6 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_region_point1 = QLabel(self.groupBox_2)
        self.label_region_point1.setObjectName("label_region_point1")

        self.horizontalLayout_2.addWidget(self.label_region_point1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_3.addWidget(self.label_5)

        self.label_region_point2 = QLabel(self.groupBox_2)
        self.label_region_point2.setObjectName("label_region_point2")

        self.horizontalLayout_3.addWidget(self.label_region_point2)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_4 = QSpacerItem(
            20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_5.addWidget(self.label_9)

        self.label_region_size = QLabel(self.groupBox_2)
        self.label_region_size.setObjectName("label_region_size")

        self.horizontalLayout_5.addWidget(self.label_region_size)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.graphicsView = self.graphics_view_type(self.groupBox_3)
        self.graphicsView.setObjectName("graphicsView")

        self.horizontalLayout_6.addWidget(self.graphicsView)

        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 2, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_take_region = QPushButton(self.groupBox)
        self.button_take_region.setObjectName("button_take_region")
        self.button_take_region.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.button_take_region)

        self.button_save_region = QPushButton(self.groupBox)
        self.button_save_region.setObjectName("button_save_region")
        self.button_save_region.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.button_save_region)

        self.button_cancel_region = QPushButton(self.groupBox)
        self.button_cancel_region.setObjectName("button_cancel_region")
        self.button_cancel_region.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.button_cancel_region)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", "Info", None))
        self.label_7.setText(
            QCoreApplication.translate("Form", "\u56fe\u7247-\u5206\u8fa8\u7387", None)
        )
        self.label_picture_resolution.setText(
            QCoreApplication.translate("Form", "TextLabel", None)
        )
        self.label.setText(
            QCoreApplication.translate("Form", "\u56fe\u7247-\u7f29\u653e", None)
        )
        self.label_picture_zoom.setText(
            QCoreApplication.translate("Form", "TextLabel", None)
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "Form", "\u9009\u533a-\u5de6\u4e0a\u89d2\u70b9", None
            )
        )
        self.label_region_point1.setText(
            QCoreApplication.translate("Form", "TextLabel", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("Form", "\u9009\u533a-\u53f3\u4e0b\u70b9", None)
        )
        self.label_region_point2.setText(
            QCoreApplication.translate("Form", "TextLabel", None)
        )
        self.label_9.setText(
            QCoreApplication.translate("Form", "\u9009\u533a-\u5927\u5c0f", None)
        )
        self.label_region_size.setText(
            QCoreApplication.translate("Form", "TextLabel", None)
        )
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", "Picture", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", "control", None))
        self.button_take_region.setText(
            QCoreApplication.translate(
                "Form", "\u5f00\u59cb\u9009\u62e9\u9009\u533a", None
            )
        )
        self.button_save_region.setText(
            QCoreApplication.translate("Form", "\u4fdd\u5b58\u9009\u533a", None)
        )
        self.button_cancel_region.setText(
            QCoreApplication.translate("Form", "\u53d6\u6d88\u9009\u533a", None)
        )

    # retranslateUi
