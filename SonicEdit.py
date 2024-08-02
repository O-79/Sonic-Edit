import sys
import os
import numpy as np
import librosa
import soundfile as sf
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from scipy.signal import butter, lfilter
from Edit import Edit
from Styles import Styles

class SonicEdit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(' ')
        self.setFixedSize(176, 47)

        WGT_MAIN = QWidget()
        self.setCentralWidget(WGT_MAIN)
        LAY_MAIN = QVBoxLayout(WGT_MAIN)

        self.TBR = QToolBar()
        self.addToolBar(self.TBR)
        self.TBR.setMovable(False)
        self.TBR.setFloatable(False)

        self.BUT_OPN = QAction('Open', self)
        self.BUT_OPN.triggered.connect(self.AUD_FND)
        self.TBR.addAction(self.BUT_OPN)

        self.BUT_EXP = QAction('Equalize', self)
        self.BUT_EXP.triggered.connect(self.AUD_EXP)
        self.BUT_EXP.setEnabled(False)
        self.TBR.addAction(self.BUT_EXP)

        self.setStyleSheet(Styles.MISC_0)
    
    def AUD_FND(self):
        AUD_TYP = "Audio Files (*.mp3 *.wav *.ogg *.flv *.flac *.mp4 *.wma *.aac *.m4a)"
        self.AUD_PATH, _ = QFileDialog.getOpenFileName(self, "Select an Audio File", "", AUD_TYP)
        
        if self.AUD_PATH:
            print(f"[LOG] SETUP -> Selected file path: {self.AUD_PATH}")
            self.BUT_EXP.setEnabled(True)
            self.AUD, self.SPL_RTE = librosa.load(self.AUD_PATH, sr=None, mono=True)
            self.SPL = self.AUD

    def AUD_EXP(self):
        AUD_1 = self.SPL
        AUD_1 = Edit.EQUALIZER(AUD_1, self.SPL_RTE, 32, 1, 192)
        AUD_1_PATH = f"{os.path.splitext(self.AUD_PATH)[0]}_1.wav"
        sf.write(AUD_1_PATH, AUD_1, self.SPL_RTE, format='wav')
        print(f"[LOG] EXPORT -> Exported file to: {AUD_1_PATH}")

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    VIEW = SonicEdit()
    VIEW.show()
    sys.exit(APP.exec())