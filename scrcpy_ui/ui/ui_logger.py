# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loggerEIfFsQ.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject
from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QTextBrowser


class Ui_Logger(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(433, 510)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser = QTextBrowser(self.groupBox)
        self.textBrowser.setObjectName("textBrowser")

        self.horizontalLayout.addWidget(self.textBrowser)

        self.horizontalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", "Logger", None))

    # retranslateUi
