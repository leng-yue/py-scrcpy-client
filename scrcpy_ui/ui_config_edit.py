# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_edit.ui'
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
    QAbstractButton,
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QTextEdit,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(400, 305)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.combobox_run_mode = QComboBox(Dialog)
        self.combobox_run_mode.setObjectName("combobox_run_mode")

        self.gridLayout.addWidget(self.combobox_run_mode, 7, 3, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)

        self.lineedit_account = QLineEdit(Dialog)
        self.lineedit_account.setObjectName("lineedit_account")

        self.gridLayout.addWidget(self.lineedit_account, 4, 3, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)

        self.textedit_token = QTextEdit(Dialog)
        self.textedit_token.setObjectName("textedit_token")
        self.textedit_token.setTabChangesFocus(False)
        self.textedit_token.setHtml(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'.AppleSystemUIFont'; font-size:13pt;\"><br /></p></body></html>"
        )

        self.gridLayout.addWidget(self.textedit_token, 10, 3, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 4, 1, 1, 1)

        self.combobox_ai_level = QComboBox(Dialog)
        self.combobox_ai_level.setObjectName("combobox_ai_level")

        self.gridLayout.addWidget(self.combobox_ai_level, 2, 3, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 15, 1, 1, 4)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 10, 1, 1, 1)

        self.combobox_team = QComboBox(Dialog)
        self.combobox_team.setObjectName("combobox_team")

        self.gridLayout.addWidget(self.combobox_team, 1, 3, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 7, 1, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 8, 1, 1, 1)

        self.lineedit_nickname = QLineEdit(Dialog)
        self.lineedit_nickname.setObjectName("lineedit_nickname")

        self.gridLayout.addWidget(self.lineedit_nickname, 8, 3, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.combobox_run_mode.setCurrentText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", "AI Level: ", None))
        self.lineedit_account.setText("")
        self.lineedit_account.setPlaceholderText(
            QCoreApplication.translate("Dialog", "id1,id2,id3", None)
        )
        self.label_5.setText(QCoreApplication.translate("Dialog", "Team: ", None))
        self.textedit_token.setPlaceholderText(
            QCoreApplication.translate("Dialog", "token cookie", None)
        )
        self.label.setText(QCoreApplication.translate("Dialog", "Account: ", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "Token: ", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "Run Mode: ", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", "Nick Name: ", None))

    # retranslateUi
