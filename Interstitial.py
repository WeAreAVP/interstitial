# Interstitial Error Detector
# Version 0.1, 2013-07-30

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from time import sleep
import interstitialcore
import keyhandler
from os import path

# printer
# allows for writing to a QWindow
class printer():
	def __init__(self, t):
		self.t = t 
	
	def write(self, m):
		self.t.moveCursor(QTextCursor.End)
		self.t.insertPlainText(m)

class MainWin(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('Interstitial Error Detector')
		self.fd1 = QPushButton("...", self)
		self.fd1.clicked.connect(self.getDir1)
		self.line1 = QLineEdit()
		self.fd2 = QPushButton("...", self)
		self.fd2.clicked.connect(self.getDir2)
		self.line2 = QLineEdit()
		self.fd3 = QPushButton("...", self)
		self.fd3.clicked.connect(self.getDir3)
		self.line3 = QLineEdit()
		self.line3.setText(path.expanduser('~/'))
		self.go = QPushButton("Run!", self)
		self.go.clicked.connect(self.newWin)
		layout = QGridLayout(self)
		layout.addWidget(QLabel("DAW Directory"), 0, 0)
		layout.addWidget(QLabel("Reference Directory"), 1, 0)
		layout.addWidget(QLabel("Manifest Destination"), 2, 0)
		layout.addWidget(self.line1, 0, 1)
		layout.addWidget(self.line2, 1, 1)
		layout.addWidget(self.line3, 2, 1)
		layout.addWidget(self.fd1, 0, 2)
		layout.addWidget(self.fd2, 1, 2)
		layout.addWidget(self.fd3, 2, 2)
		layout.addWidget(self.go, 4, 1)
		self.setLayout(layout)

	def getDir1(self):
		f = QFileDialog.getExistingDirectory(directory=path.expanduser('~'))
		self.line1.setText(f)

	def getDir2(self):
		f = QFileDialog.getExistingDirectory(directory=path.expanduser('~'))
		self.line2.setText(f)

	def getDir3(self):
		f = QFileDialog.getExistingDirectory(directory=path.expanduser('~'))
		self.line3.setText(f)

	def newWin(self):
		d = QDialog(self)
		d.setWindowTitle('Interstitial Error Detector')
		lay = QVBoxLayout(d)
		xit = QPushButton("Exit", self)
		xit.setEnabled(False)
		xit.clicked.connect(self.close)
		te = QTextEdit(self)
		te.setReadOnly(True)
		lay.addWidget(te)
		lay.addWidget(xit)
		d.setLayout(lay)
		sys.stdout = printer(te)
		d.resize(1000, 300)
		d.show()
		interstitialcore.execute(str(self.line1.text()), str(self.line2.text()), str(self.line3.text()), QCoreApplication.instance())
		xit.setEnabled(True)

def main():
	app = QApplication(sys.argv)
	w = MainWin()
	w.show()
	w.raise_()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()