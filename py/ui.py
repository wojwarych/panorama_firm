import sys

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore


class MainWindow(QtWidgets.QMainWindow):


	def __init__(self):
		

		super().__init__()
		self.initUI()


	def initUI(self):

		self.title = QtWidgets.QLabel('Title')

		
		self.title_edit = QtWidgets.QLineEdit()
		QtWidgets.QToolTip.setFont(QtGui.QFont('Calibri', 12))

		self.create_buttons()

		self.set_geometry()

		self.show()


	def set_geometry(self):

		self.grid_elements()

		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.resize(400, 300)
		self.setWindowTitle('Company Finder 0.1')
		self.move(qr.topLeft())


	def create_buttons(self):

		self._start_window = None
		self.start_btn = QtWidgets.QPushButton('Start', self)
		self.start_btn.setToolTip('Kliknij, żeby uruchomić program')
		self.start_btn.clicked.connect(self.show_start_page)
		self.start_btn.resize(100, 100)

		self.exit_btn = QtWidgets.QPushButton('Exit', self)
		self.exit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		self.exit_btn.setToolTip('Kliknij, żeby zamknąć program')
		self.exit_btn.resize(100, 100)


	def grid_elements(self):

		widget = QtWidgets.QWidget(self)
		self.setCentralWidget(widget)
		
		layout = QtWidgets.QGridLayout()
		layout.setRowStretch(0, 2)
		layout.setRowMinimumHeight(0, 300)
		layout.setRowStretch(1, 1)
		layout.setColumnStretch(0, 1)
		layout.setColumnStretch(1, 1)
		layout.setColumnStretch(2, 1)
		layout.setSpacing(10)

		layout.addWidget(self.title, 1, 0, 1, 3)
		layout.setAlignment(self.title, QtCore.Qt.AlignTop)

		layout.addWidget(self.start_btn, 2, 1)
		layout.addWidget(self.exit_btn, 2, 2)
		
		widget.setLayout(layout)


	def show_start_page(self):

		self._start_window = StartPage()
		self._start_window.show()


class StartPage(QtWidgets.QMainWindow):


	def __init__(self):
		

		super().__init__()
		self.initUI()


	def initUI(self):

		self.title = QtWidgets.QLabel('Title')

		
		self.title_edit = QtWidgets.QLineEdit()
		QtWidgets.QToolTip.setFont(QtGui.QFont('Calibri', 12))

		self.create_buttons()

		self.set_geometry()

		self.show()


	def set_geometry(self):

		self.grid_elements()

		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.resize(400, 300)
		self.setWindowTitle('Company Finder 0.1')
		self.move(qr.topLeft())


	def create_buttons(self):


		self.start_btn = QtWidgets.QPushButton('Start', self)
		self.start_btn.setToolTip('Kliknij, żeby uruchomić program')
		self.start_btn.resize(100, 100)

		self.exit_btn = QtWidgets.QPushButton('Exit', self)
		self.exit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		self.exit_btn.setToolTip('Kliknij, żeby zamknąć program')
		self.exit_btn.resize(100, 100)


	def grid_elements(self):

		widget = QtWidgets.QWidget(self)
		self.setCentralWidget(widget)
		
		layout = QtWidgets.QGridLayout()
		layout.setRowStretch(0, 2)
		layout.setRowMinimumHeight(0, 300)
		layout.setRowStretch(1, 1)
		layout.setColumnStretch(0, 1)
		layout.setColumnStretch(1, 1)
		layout.setColumnStretch(2, 1)
		layout.setSpacing(10)

		layout.addWidget(self.title, 1, 0, 1, 3)
		layout.setAlignment(self.title, QtCore.Qt.AlignTop)

		layout.addWidget(self.start_btn, 2, 1)
		layout.addWidget(self.exit_btn, 2, 2)
		
		widget.setLayout(layout)



if __name__ == "__main__":


	app = 	QtWidgets.QApplication(sys.argv)
	w = MainWindow()
	sys.exit(app.exec_())