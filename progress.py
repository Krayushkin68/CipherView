# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ProgressCipher(object):
    def setupUi(self, ProgressCipher):
        if not ProgressCipher.objectName():
            ProgressCipher.setObjectName(u"ProgressCipher")
        ProgressCipher.resize(389, 64)
        self.centralwidget = QWidget(ProgressCipher)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 4, 6, 5)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStyleStrategy(QFont.PreferDefault)
        self.label.setFont(font)
        self.label.setCursor(QCursor(Qt.ArrowCursor))
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        font1 = QFont()
        font1.setPointSize(9)
        self.progressBar.setFont(font1)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.progressBar)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        ProgressCipher.setCentralWidget(self.centralwidget)

        self.retranslateUi(ProgressCipher)

        QMetaObject.connectSlotsByName(ProgressCipher)
    # setupUi

    def retranslateUi(self, ProgressCipher):
        ProgressCipher.setWindowTitle(QCoreApplication.translate("ProgressCipher", u"\u0428\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.label.setText(QCoreApplication.translate("ProgressCipher", u"\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0441\u044f \u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u0438\u0435...", None))
    # retranslateUi

