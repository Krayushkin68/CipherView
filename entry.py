# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'entry.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_EntryWindow(object):
    def setupUi(self, EntryWindow):
        if not EntryWindow.objectName():
            EntryWindow.setObjectName(u"EntryWindow")
        EntryWindow.resize(341, 209)
        self.centralwidget = QWidget(EntryWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.btn_exist = QPushButton(self.centralwidget)
        self.btn_exist.setObjectName(u"btn_exist")
        self.btn_exist.setGeometry(QRect(50, 150, 251, 23))
        self.btn_new = QPushButton(self.centralwidget)
        self.btn_new.setObjectName(u"btn_new")
        self.btn_new.setGeometry(QRect(50, 180, 251, 23))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 321, 111))
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.Box)
        self.label.setTextFormat(Qt.RichText)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        EntryWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EntryWindow)

        QMetaObject.connectSlotsByName(EntryWindow)
    # setupUi

    def retranslateUi(self, EntryWindow):
        EntryWindow.setWindowTitle(QCoreApplication.translate("EntryWindow", u"Shifr View", None))
        self.btn_exist.setText(QCoreApplication.translate("EntryWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u044e\u0449\u0443\u044e \u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u043d\u0443\u044e \u043f\u0430\u043f\u043a\u0443", None))
        self.btn_new.setText(QCoreApplication.translate("EntryWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043d\u043e\u0432\u0443\u044e \u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u043d\u0443\u044e \u043f\u0430\u043f\u043a\u0443", None))
        self.label.setText(QCoreApplication.translate("EntryWindow", u"\u0412\u0430\u0441 \u043f\u0440\u0438\u0432\u0435\u0442\u0441\u0442\u0432\u0443\u0435\u0442 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430 \u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043f\u0430\u043f\u043e\u043a, \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435:", None))
    # retranslateUi

