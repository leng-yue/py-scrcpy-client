# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'region_save_dialogACuejq.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class Ui_RegionSaveDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(502, 298)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QSize(200, 0))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_resolution = QLabel(self.groupBox_2)
        self.label_resolution.setObjectName("label_resolution")

        self.horizontalLayout_2.addWidget(self.label_resolution)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.label_point1 = QLabel(self.groupBox_2)
        self.label_point1.setObjectName("label_point1")

        self.horizontalLayout_3.addWidget(self.label_point1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.label_6)

        self.label_point2 = QLabel(self.groupBox_2)
        self.label_point2.setObjectName("label_point2")

        self.horizontalLayout_4.addWidget(self.label_point2)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_5.addWidget(self.label_8)

        self.label_region_size = QLabel(self.groupBox_2)
        self.label_region_size.setObjectName("label_region_size")

        self.horizontalLayout_5.addWidget(self.label_region_size)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.image_display = QLabel(self.groupBox)
        self.image_display.setObjectName("image_display")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.image_display.sizePolicy().hasHeightForWidth()
        )
        self.image_display.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.image_display)

        self.horizontalLayout_6.addWidget(self.groupBox)

        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 3)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")

        self.verticalLayout_2.addWidget(self.label_10)

        self.line_edit_region_name = QLineEdit(self.groupBox_3)
        self.line_edit_region_name.setObjectName("line_edit_region_name")

        self.verticalLayout_2.addWidget(self.line_edit_region_name)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(
            155, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            155, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.groupBox_2.setTitle(
            QCoreApplication.translate("Dialog", "Infomation", None)
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "Dialog", "\u6e90\u56fe\u7247\u5206\u8fa8\u7387", None
            )
        )
        self.label_resolution.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "Dialog", "\u533a\u57df\u5de6\u4e0a\u89d2\u5750\u6807", None
            )
        )
        self.label_point1.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "Dialog", "\u533a\u57df\u53f3\u4e0b\u89d2\u5750\u6807", None
            )
        )
        self.label_point2.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.label_8.setText(
            QCoreApplication.translate("Dialog", "\u533a\u57df\u5927\u5c0f", None)
        )
        self.label_region_size.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", "Image", None))
        self.image_display.setText(QCoreApplication.translate("Dialog", "PIXMAP", None))
        self.groupBox_3.setTitle(
            QCoreApplication.translate("Dialog", "Region-Entry-Name", None)
        )
        self.label_10.setText(
            QCoreApplication.translate(
                "Dialog", "\u952e\u5165\u533a\u57df\u6807\u8bc6:", None
            )
        )

    # retranslateUi
