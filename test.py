from PySide.QtCore import *
from PySide.QtGui import *
import sys
#!/usr/bin/env python

import sys


#class HelloApplication(QApplication):
#
#    def __init__(self, args):
#        """ In the constructor we're doing everything to get our application
#            started, which is basically constructing a basic QApplication by
#            its __init__ method, then adding our widgets and finally starting
#            the exec_loop."""
#        QApplication.__init__(self, args)
#        self.addWidgets()
#        self.exec_()
#
#    def addWidgets(self):
#        """ In this method, we're adding widgets and connecting signals from
#            these widgets to methods of our class, the so-called "slots"
#        """
#        groupBox = QGroupBox("E&xclusive Radio Buttons")
#        groupBox.setCheckable(True)
#        groupBox.setChecked(False)
#
#        radio1 = QRadioButton("Rad&io button 1")
#        radio2 = QRadioButton("Radi&o button 2")
#        radio3 = QRadioButton("Radio &button 3")
#        radio1.setChecked(True)
#        checkBox = QCheckBox("Ind&ependent checkbox")
#        checkBox.setChecked(True)
#
#        self.hellobutton = QPushButton("Say 'Hello world!'",None)
#        self.connect(self.hellobutton, SIGNAL("clicked()"), self.slotSayHello)
#        self.hellobutton.show()
#
#    def slotSayHello(self):
#        """ This is an example slot, a method that gets called when a signal is
#            emitted """
#        print "Hello, World!"
#
## Only actually do something if this script is run standalone, so we can test our
## application, but we're also able to import this program without actually running
## any code.
#if __name__ == "__main__":
#    app = HelloApplication(sys.argv)


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        #grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
        #grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
        #grid.addWidget(self.createPushButtonGroup(), 1, 1)
        self.setLayout(grid)

        self.setWindowTitle("Group Box")
        self.resize(480, 320)

    def createFirstExclusiveGroup(self):
        groupBox = QGroupBox("Exclusive Radio Buttons")

        radio1 = QRadioButton("&Radio button 1")
        radio2 = QRadioButton("R&adio button 2")
        radio3 = QRadioButton("Ra&dio button 3")

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    #def createSecondExclusiveGroup(self):
    #    groupBox = QGroupBox("E&xclusive Radio Buttons")
    #    groupBox.setCheckable(True)
    #    groupBox.setChecked(False)
    #
    #    radio1 = QRadioButton("Rad&io button 1")
    #    radio2 = QRadioButton("Radi&o button 2")
    #    radio3 = QRadioButton("Radio &button 3")
    #    radio1.setChecked(True)
    #    checkBox = QCheckBox("Ind&ependent checkbox")
    #    checkBox.setChecked(True)
    #
    #    vbox = QVBoxLayout()
    #    vbox.addWidget(radio1)
    #    vbox.addWidget(radio2)
    #    vbox.addWidget(radio3)
    #    vbox.addWidget(checkBox)
    #    vbox.addStretch(1)
    #    groupBox.setLayout(vbox)
    #
    #    return groupBox



    #def createPushButtonGroup(self):
    #    groupBox = QGroupBox("&Push Buttons")
    #    groupBox.setCheckable(True)
    #    groupBox.setChecked(True)
    #
    #    pushButton = QPushButton("&Normal Button")
    #    toggleButton = QPushButton("&Toggle Button")
    #    toggleButton.setCheckable(True)
    #    toggleButton.setChecked(True)
    #    flatButton = QPushButton("&Flat Button")
    #    flatButton.setFlat(True)
    #
    #    popupButton = QPushButton("Pop&up Button")
    #    menu = QMenu(self)
    #    menu.addAction("&First Item")
    #    menu.addAction("&Second Item")
    #    menu.addAction("&Third Item")
    #    menu.addAction("F&ourth Item")
    #    popupButton.setMenu(menu)
    #
    #    newAction = menu.addAction("Submenu")
    #    subMenu = QMenu("Popup Submenu", self)
    #    subMenu.addAction("Item 1")
    #    subMenu.addAction("Item 2")
    #    subMenu.addAction("Item 3")
    #    newAction.setMenu(subMenu)
    #
    #    vbox = QVBoxLayout()
    #    vbox.addWidget(pushButton)
    #    vbox.addWidget(toggleButton)
    #    vbox.addWidget(flatButton)
    #    vbox.addWidget(popupButton)
    #    vbox.addStretch(1)
    #    groupBox.setLayout(vbox)
    #
    #    return groupBox


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())