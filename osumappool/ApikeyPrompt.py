from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool, QObject, QRunnable, QTimer, pyqtSignal, pyqtSlot
from .layout import ApikeyPromptUI
import urllib.request

class WorkerSignals(QObject):
    result = pyqtSignal(bool)

class Worker(QRunnable):
    def __init__(self, key):
        super(Worker, self).__init__()
        self.key = key
        self.signals = WorkerSignals()
    
    @pyqtSlot()
    def run(self):
        url = f"https://osu.ppy.sh/api/get_beatmaps?k={self.key}&b=2156070"
        try:
            response = urllib.request.urlopen(url)
        except:
            self.signals.result.emit(False)
        else:
            self.signals.result.emit(True)

class ApikeyPrompt(QtWidgets.QMainWindow, ApikeyPromptUI.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.check_api_key)
        self.threadpool = QThreadPool()

    def check_api_key(self):
        self.pushButton.setEnabled(False)
        self.key = self.lineEdit.text()
        self.label_3.setText("Checking the api key...")
        
        worker = Worker(self.key)
        worker.signals.result.connect(self.key_check_finished)

        self.threadpool.start(worker)

    def key_check_finished(self, result):
        if result:
            self.key_check_success()
        else:
            self.key_check_failed()

    def key_check_failed(self):
        self.pushButton.setEnabled(True)
        self.label_3.setText("Api key check failed, please enter valid api key or check your internet connection.")

    def key_check_success(self):
        self.label_3.setText("Api key check success. Saving...")

        with open("mykey.apikey", "w") as outfile:
            outfile.write(self.key)
        
        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.finish)
        self.timer.start()

    def finish(self):
        self.close()
        self.timer.stop()
        print("Quit")

def prompt_apikey():
    app = QtWidgets.QApplication([])
    window = ApikeyPrompt()
    window.show()
    app.exec_()