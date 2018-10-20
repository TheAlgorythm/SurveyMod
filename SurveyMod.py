from Onion import Onion, requests
from GuerrillaMail import GuerrillaMailSession
import random
import time
import logging
from threading import Thread, Event


def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class SurveyMod:

    dataConfig = None
    helperConfig = None
    url = None
    method = None
    intervalMin = None
    intervalMax = None
    mails = []
    checkedMails = []
    mailFile = None
    mailTexts = ''

    notificator = None
    _stopCheckingMails = Event()

    log = logging.getLogger('SurveyMod')

    def __init__(self, siteConfig, helperConfig, mailFile):
        self.dataConfig = siteConfig['data']
        self.url = siteConfig['url']
        self.method = siteConfig['method'].upper()
        self.intervalMin = siteConfig['interval_min']
        self.intervalMax = siteConfig['interval_max']
        self.helperConfig = helperConfig
        self.mailFile = mailFile

    @threaded
    def run(self, iterations):
        self._stopCheckingMails.clear()
        self.checkEmails(True)
        for i in range(0, iterations):
            newHelper = self.helperConfig.copy()
            self.fillHelper(newHelper)
            newDataConfig = self.dataConfig.copy()
            self.choose(newDataConfig)
            self.replace(newDataConfig, newHelper)
            try:
                if self.method == 'POST':
                    response = Onion.post(self.url, data=newDataConfig)
                elif self.method == 'GET':
                    response = Onion.get(self.url, params=newDataConfig)
                response.raise_for_status()
                logging.info('Sended')
            except requests.RequestException as e:
                SurveyMod.log.error(('Request failed: {e.request.url} ' +
                    '{e.response.status_code} {e.response.reason}').format(e=e))
            self.notificate()
            if i != iterations - 1:
                time.sleep(random.randrange(self.intervalMin, self.intervalMax))
        self._stopCheckingMails.set()
        self.checkEmails(False)

    def fillHelper(self, helperConfig):
        helperConfig.update({'house_number': self.createHouseNumber()})
        helperConfig.update({'zip': self.createZIP()})
        self.choose(helperConfig)
        self.replace(helperConfig, helperConfig)
        helperConfig['email'] = self.createEmail(helperConfig['email'])

    def choose(self, config):
        for key, val in config.items():
            if type(val) is list:
                config[key] = random.choice(val)

    def replace(self, config, helper):
        for key, val in config.items():
            config[key] = self.replaceString(val, helper)

    def replaceString(self, val, helper):
        if '%' not in val:
            return val
        for key, helpVal in helper.items():
            val = val.replace('%' + key + '%', helpVal)
        if '%rand' in val:
            val = val.replace('%randxs%', str(random.randrange(1, 9)))
            val = val.replace('%rands%', str(random.randrange(1, 99)))
            val = val.replace('%randm%', str(random.randrange(1, 999)))
            val = val.replace('%randl%', str(random.randrange(1, 9999)))
            val = val.replace('%randxl%', str(random.randrange(1, 99999)))
        return val

    def createHouseNumber(self):
        extension = ('', 'a', 'b', 'c')
        return str(random.randrange(1, 140)) + random.choice(extension)

    def createZIP(self):
        return str(random.randrange(10001, 99999))

    def createEmail(self, lokalAdress):
        session = GuerrillaMailSession()
        session.set_email_address(lokalAdress)
        self.mails.append(session)
        return session.get_session_state()['email_address']

    @threaded
    def checkEmails(self, recursive):
        while True:
            time.sleep(60 * 20)
            for mail in self.mails:
                self.checkEmailSession(mail)
            if not recursive and not self._stopCheckingMails.isSet():
                break

    def checkEmailSession(self, session):
        mails = session.get_email_list()
        for mail in mails:
            if mail.guid in self.checkedEmail:
                continue
            self.checkedMails.append(mail.guid)
            self.printEmail(mail)

    def printEmail(self, mail):
        logging.info('Email received')
        content = '{}:{}\n{}\n\n'.format(mail.sender, mail.subject, mail.body)
        if self.mailFile:
            with open(self.mailFile, "a") as mailFile:
                mailFile.write(content)
        self.mailTexts.append(content)
        self.notificate()

    def notificate(self):
        if self.notificator:
            self.notificator()
