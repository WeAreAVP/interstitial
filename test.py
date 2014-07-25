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
class New(QWidget):
    def __init__(self, parent=None):
        super(New, self).__init__(parent)

    def createFirstExclusiveGroup(self):




        self.vbox.addStretch(1)

        self.groupBox.setLayout(self.vbox)

        print(self.radio3)

        return self.groupBox



        pass
class loader(QWidget):
    def __init__(self, parent=None):
          super(loader, self).__init__(parent)

    def loadwidget(self, layout):

        layout
class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.groupBox = QGroupBox("Exclusive Radio Buttons")
        self.vbox = QVBoxLayout()

        grid = QGridLayout()

        self.radio1 = QPushButton("&Radio button 1", 0, 1)
        self.radio2 = QPushButton("R&adio button 2", 0, )
        self.radio3 = QPushButton("Ra&dio button 3", 0, 1)

        self.vbox.addWidget(self.radio1)
        self.vbox.addWidget(self.radio2)
        self.vbox.addWidget(self.radio3)
        self.radio1.clicked.connect(self.removeDAWDirectory)

        self.groupBox.setLayout(self.vbox)

        self.setLayout(grid)

        self.setWindowTitle("Group Box")
        grid.addWidget(self.groupBox)

    def removeDAWDirectory(self):
        self.vbox.removeWidget(self.radio1)
        self.radio1.deleteLater()
        self.radio1.destroy()
        del self.radio1

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())


#from PySide.QtCore import *
#from PySide.QtGui import *
#import sys
#from functools import partial
##!/usr/bin/env python
#
#import sys
#
#
##class HelloApplication(QApplication):
##
##    def __init__(self, args):
##        """ In the constructor we're doing everything to get our application
##            started, which is basically constructing a basic QApplication by
##            its __init__ method, then adding our widgets and finally starting
##            the exec_loop."""
##        QApplication.__init__(self, args)
##        self.addWidgets()
##        self.exec_()
##
##    def addWidgets(self):
##        """ In this method, we're adding widgets and connecting signals from
##            these widgets to methods of our class, the so-called "slots"
##        """
##        groupBox = QGroupBox("E&xclusive Radio Buttons")
##        groupBox.setCheckable(True)
##        groupBox.setChecked(False)
##
##        radio1 = QRadioButton("Rad&io button 1")
##        radio2 = QRadioButton("Radi&o button 2")
##        radio3 = QRadioButton("Radio &button 3")
##        radio1.setChecked(True)
##        checkBox = QCheckBox("Ind&ependent checkbox")
##        checkBox.setChecked(True)
##
##        self.hellobutton = QPushButton("Say 'Hello world!'",None)
##        self.connect(self.hellobutton, SIGNAL("clicked()"), self.slotSayHello)
##        self.hellobutton.show()
##
##    def slotSayHello(self):
##        """ This is an example slot, a method that gets called when a signal is
##            emitted """
##        print "Hello, World!"
##
### Only actually do something if this script is run standalone, so we can test our
### application, but we're also able to import this program without actually running
### any code.
##if __name__ == "__main__":
##    app = HelloApplication(sys.argv)
#
#class New(QWidget):
#    def __init__(self, parent=None):
#        super(New, self).__init__(parent)
#        self.loader = loader()
#
#    def createFirstExclusiveGroup(self):
#        self.groupBox = QGroupBox("Exclusive Radio Buttons")
#
#        self.vbox = QVBoxLayout()
#
#        self.vbox = self.loader.loadwidget(self.vbox)
#
#        self.vbox.addStretch(1)
#
#        self.groupBox.setLayout(self.vbox)
#
#        return self.groupBox
#
#
#        pass
#
#class loader(QWidget):
#    def __init__(self, parent=None):
#          super(loader, self).__init__(parent)
#
#    def loadwidget(self, layout):
#        self.radio1 =  QPushButton("Ra&dio button 1")
#        self.radio2 =  QPushButton("Ra&dio button 2")
#        self.radio3 = QPushButton("Ra&dio button 3")
#
#        layout.addWidget(self.radio1)
#        layout.addWidget(self.radio2)
#        layout.addWidget(self.radio3)
#        print(self.radio1.clicked.connect(partial(self.removeDAWDirectory, layout)))
#        return layout
#
#    def removeDAWDirectory(self, layout):
#        print('1234')
#        layout.removeWidget(self.radio3)
#
#class Window(QWidget):
#    def __init__(self, parent=None):
#        super(Window, self).__init__(parent)
#
#        grid = QGridLayout()
#        self.nwwe = New()
#
#        grid.addWidget(self.nwwe.createFirstExclusiveGroup())
#        #grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
#        #grid.addWidget(self.createPushButtonGroup(), 1, 1)
#        self.setLayout(grid)
#
#        self.setWindowTitle("Group Box")
#
#if __name__ == '__main__':
#
#    import sys
#
#    app = QApplication(sys.argv)
#    clock = Window()
#    clock.show()
#    sys.exit(app.exec_())
xec_())
