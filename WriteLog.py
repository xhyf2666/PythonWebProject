import logging


class WriteLog():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fileHandler = logging.FileHandler("log.log")
        self.fileHandler.setLevel(logging.ERROR)
        self.fileHandler.setFormatter(self.formatter)

    def ErrorLog(self, error):
        self.logger.addHandler(self.fileHandler)
        self.logger.error(error)

    def WarningLog(self, warning):
        self.logger.addHandler(self.fileHandler)
        self.logger.warning(warning)
