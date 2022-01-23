# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog_open(object):
    def setupUi(self, Dialog_open):
        if not Dialog_open.objectName():
            Dialog_open.setObjectName(u"Dialog_open")
        Dialog_open.resize(317, 155)
        self.centralwidget = QWidget(Dialog_open)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 181, 16))
        self.Edit_path = QLineEdit(self.centralwidget)
        self.Edit_path.setObjectName(u"Edit_path")
        self.Edit_path.setGeometry(QRect(10, 40, 241, 20))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 70, 91, 16))
        self.btn_obzor = QPushButton(self.centralwidget)
        self.btn_obzor.setObjectName(u"btn_obzor")
        self.btn_obzor.setGeometry(QRect(259, 38, 51, 21))
        self.Edit_passwd = QLineEdit(self.centralwidget)
        self.Edit_passwd.setObjectName(u"Edit_passwd")
        self.Edit_passwd.setGeometry(QRect(10, 90, 241, 20))
        self.Edit_passwd.setEchoMode(QLineEdit.Password)
        self.btn_ok = QPushButton(self.centralwidget)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setGeometry(QRect(100, 120, 75, 23))
        self.btn_cancel = QPushButton(self.centralwidget)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(180, 120, 75, 23))
        Dialog_open.setCentralWidget(self.centralwidget)

        self.retranslateUi(Dialog_open)

        QMetaObject.connectSlotsByName(Dialog_open)
    # setupUi

    def retranslateUi(self, Dialog_open):
        Dialog_open.setWindowTitle(QCoreApplication.translate("Dialog_open", u"\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043f\u0430\u043f\u043a\u0438", None))
        self.label.setText(QCoreApplication.translate("Dialog_open", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0430\u043f\u043a\u0443 \u0434\u043b\u044f \u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u0438\u044f:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_open", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043f\u0430\u0440\u043e\u043b\u044c:", None))
        self.btn_obzor.setText(QCoreApplication.translate("Dialog_open", u"\u041e\u0431\u0437\u043e\u0440..", None))
        self.btn_ok.setText(QCoreApplication.translate("Dialog_open", u"\u041e\u043a", None))
        self.btn_cancel.setText(QCoreApplication.translate("Dialog_open", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

