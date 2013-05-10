#! /usr/bin/env python

import sys
from PyQt4 import QtGui

def main():
	app = QtGui.QApplication(sys.argv)

	w = QtGui.QWidget()
	w.resize(600, 400)
	w.move(300, 300)
	w.setWindowTitle('Sample app')
	w.show()

	q = QtGui.QWidget()
	q.resize(200, 200)
	q.setWindowTitle('Chat')
	q.show()


	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
