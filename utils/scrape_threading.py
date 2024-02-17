# ----------------------- Modules -------------------------------- #
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from utils.spider import *

# ----------------------- Classes -------------------------------- #
class ScrapingThread(QThread):
    scrapingIterationFinished = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.scrappedData = []
        self.paused = False
        self.stopped = False

    def run(self):
        print("Scraping thread started")
        Start(self)

    def pause(self):
        print("Scraping thread paused")
        self.paused = True

    def stop(self):
        print("Scraping thread stopped")
        self.stopped = True

    def resume(self):
        print("Scraping thread resumed")
        self.paused = False