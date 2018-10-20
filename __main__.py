from SurveyMod import SurveyMod
import json
import sys
import logging
from PyQt5.QtWidgets import QApplication
from GUI.GUISurveyMod import GUISurveyMod
from io import StringIO


class App:

    @staticmethod
    def run(arg):
        logging.basicConfig(level=logging.INFO, format='SurveyMod: %(levelname)s: %(message)s')
        logging.getLogger('SurveyMod')
        with open(arg[0]) as site_config_file:
            site_config = json.load(site_config_file)
        with open(arg[1]) as helper_file:
            helper = json.load(helper_file)
        survey = SurveyMod(site_config, helper, arg[2])
        survey.run(int(arg[3]))

    @staticmethod
    def runGUI(arg):
        app = QApplication(arg)

        log_stream = StringIO()

        logging.basicConfig(level=logging.INFO, stream=log_stream, format='SurveyMod: %(levelname)s: %(message)s')
        logging.getLogger('SurveyMod')

        mainWidget = GUISurveyMod()

        mainWidget.log = log_stream

        mainWidget.show()

        sys.exit(app.exec_())


if __name__ == '__main__' and sys.argv != None:
    if len(sys.argv) == 5:
        App.run(sys.argv[1:])
    else:
        App.runGUI(sys.argv)
