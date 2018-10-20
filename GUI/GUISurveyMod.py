from PyQt5.QtWidgets import QMainWindow, QFileDialog
from GUI.ui_SurveyMod import ui_SurveyMod
from SurveyMod import SurveyMod
import json


class GUISurveyMod(QMainWindow):

    log = None
    survey = None

    def __init__(self):
        super().__init__()
        self.ui = ui_SurveyMod()
        self.ui.setupUi(self)
        self.ui.runButton.clicked.connect(self.run)
        self.ui.siteConfigButton.clicked.connect(self.chooseSiteConfig)
        self.ui.helperConfigButton.clicked.connect(self.chooseHelpConfig)

    def run(self):
        siteConfig = self.ui.siteConfigLine.text()
        helperConfig = self.ui.helperConfigLine.text()
        try:
            iterations = int(self.ui.iterationsConfigLine.text())
        except ValueError:
            return
        if not siteConfig or not helperConfig or iterations <= 0:
            return
        with open(siteConfig) as site_config_file:
            site_config = json.load(site_config_file)
        with open(helperConfig) as helper_file:
            helper = json.load(helper_file)
        self.survey = SurveyMod(site_config, helper, None)
        self.survey.notificator = self.checkLog
        self.survey.run(iterations)

    def chooseSiteConfig(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Site Config ", "", "JSON Files (*.json)", options=options)
        if fileName:
            self.ui.siteConfigLine.setText(fileName)

    def chooseHelpConfig(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Helper Config ", "", "JSON Files (*.json)", options=options)
        if fileName:
            self.ui.helperConfigLine.setText(fileName)

    def checkLog(self):
        if self.log:
            self.ui.log.setPlainText(self.log.getvalue())
        if self.survey:
            self.ui.mails.setHtml(self.survey.mailTexts)
