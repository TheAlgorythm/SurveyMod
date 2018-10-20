from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class ui_SurveyMod:

    def setupUi(self, window):
        window.setObjectName('SurveyMod')
        window.setWindowTitle('SurveyMod')
        window.resize(400, 600)
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.formlayout = QtWidgets.QFormLayout()
        self.formlayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formlayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hlayout1 = QtWidgets.QHBoxLayout()
        self.hlayout2 = QtWidgets.QHBoxLayout()

        self.siteConfigLine = QtWidgets.QLineEdit()
        self.siteConfigLine.setReadOnly(True)
        self.siteConfigButton = QtWidgets.QPushButton('Choose')
        self.hlayout1.addWidget(self.siteConfigLine)
        self.hlayout1.addWidget(self.siteConfigButton)

        self.helperConfigLine = QtWidgets.QLineEdit()
        self.helperConfigLine.setReadOnly(True)
        self.helperConfigButton = QtWidgets.QPushButton('Choose')
        self.hlayout2.addWidget(self.helperConfigLine)
        self.hlayout2.addWidget(self.helperConfigButton)

        self.iterationsConfigLine = QtWidgets.QLineEdit()

        self.formlayout.addRow('Site Config', self.hlayout1)
        self.formlayout.addRow('Helper Config', self.hlayout2)
        self.formlayout.addRow('Iterations', self.iterationsConfigLine)

        self.log = QtWidgets.QPlainTextEdit()
        self.log.setReadOnly(True)
        self.mails = QtWidgets.QPlainTextEdit()
        self.runButton = QtWidgets.QPushButton('Run')

        self.layout.addLayout(self.formlayout)
        self.layout.addWidget(self.log)
        self.layout.addWidget(self.mails)
        self.layout.addWidget(self.runButton)
        window.setCentralWidget(self.widget)
