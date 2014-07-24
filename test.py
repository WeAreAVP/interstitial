#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
layout in form

Tested environment:
    Mac OS X 10.6.8

"""
import sys

from PySide.QtGui import *
from PySide.QtCore import *

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()

        x, y, w, h = 500, 200, 300, 400
        self.setGeometry(x, y, w, h)


        form = QFormLayout(self)

        name_label = QLabel("Name", self)
        name_lineedit = QLineEdit(self)
        name_lineedit1 = QLineEdit(self)
        Qhj = QHBoxLayout()
        Qhj.addWidget(name_label)
        Qhj.addWidget(name_lineedit1)
        Qhj.addWidget(name_lineedit)

        form.addRow(Qhj)

        self.setLayout(form)


    def show_and_raise(self):
        self.show()
        self.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo = Demo()
    demo.show_and_raise()

    sys.exit(app.exec_())
