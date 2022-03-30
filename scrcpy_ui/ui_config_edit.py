# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_edit.ui'
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
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 305)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.combobox_run_mode = QComboBox(Dialog)
        self.combobox_run_mode.setObjectName(u"combobox_run_mode")

        self.gridLayout.addWidget(self.combobox_run_mode, 7, 3, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)

        self.lineedit_axie_ids = QLineEdit(Dialog)
        self.lineedit_axie_ids.setObjectName(u"lineedit_axie_ids")

        self.gridLayout.addWidget(self.lineedit_axie_ids, 4, 3, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)

        self.textedit_ronin = QTextEdit(Dialog)
        self.textedit_ronin.setObjectName(u"textedit_ronin")
        self.textedit_ronin.setTabChangesFocus(False)
        self.textedit_ronin.setHtml(
            u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
            '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>'
        )

        self.gridLayout.addWidget(self.textedit_ronin, 10, 3, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 1, 1, 1)

        self.combobox_ai_level = QComboBox(Dialog)
        self.combobox_ai_level.setObjectName(u"combobox_ai_level")

        self.gridLayout.addWidget(self.combobox_ai_level, 2, 3, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 15, 1, 1, 4)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 10, 1, 1, 1)

        self.combobox_team = QComboBox(Dialog)
        self.combobox_team.setObjectName(u"combobox_team")

        self.gridLayout.addWidget(self.combobox_team, 1, 3, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 1, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 8, 1, 1, 1)

        self.lineedit_nickname = QLineEdit(Dialog)
        self.lineedit_nickname.setObjectName(u"lineedit_nickname")

        self.gridLayout.addWidget(self.lineedit_nickname, 8, 3, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.combobox_run_mode.setCurrentText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"AI Level: ", None))
        self.lineedit_axie_ids.setText("")
        self.lineedit_axie_ids.setPlaceholderText(
            QCoreApplication.translate("Dialog", u"axie_id1, axie_id2, axie_id3", None)
        )
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Team: ", None))
        self.textedit_ronin.setPlaceholderText(
            QCoreApplication.translate(
                "Dialog",
                u"ronin:aiosdjiuqshdiu23hdih1289r89w3hr78asdsdasasdasdsadasd",
                None,
            )
        )
        self.label.setText(QCoreApplication.translate("Dialog", u"Axie IDs: ", None))
        self.label_2.setText(
            QCoreApplication.translate("Dialog", u"Ronin Addr: ", None)
        )
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Run Mode: ", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Nick Name: ", None))

    # retranslateUi
