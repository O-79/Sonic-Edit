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
        self.UI()
    
    def UI(self):
        self.setWindowTitle('Sonic Edit')
        self.setFixedSize(600, 400)  # Increased size to accommodate equalizer

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

        self.equalizer_widget = QWidget()
        LAY_MAIN.addWidget(self.equalizer_widget)
        self.UI_EQUALIZER()

        self.setStyleSheet(Styles.MISC_0)

    def UI_EQUALIZER(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        
        y_axis_layout = QVBoxLayout()
        y_axis_labels = ['18', '15', '12', '9', '6', '3', '0']
        for label in y_axis_labels:
            y_label = QLabel(f"{label} dB")
            y_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            y_label.setFixedWidth(48)
            y_axis_layout.addWidget(y_label)
        y_axis_layout.setSpacing(0)
        main_layout.addLayout(y_axis_layout)
        
        sliders_layout = QHBoxLayout()
        self.sliders = []
        freq_ranges = ['32', '64', '125', '250', '500', '1K', '2K', '4K', '8K', '16K']
        
        for freq in freq_ranges:
            slider_layout = QVBoxLayout()
            slider = QSlider(Qt.Orientation.Vertical)
            slider.setRange(0, 18)
            slider.setValue(0)
            slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
            slider.setTickInterval(3)
            
            label = QLabel(freq)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            slider_layout.addWidget(slider)
            slider_layout.addWidget(label)
            sliders_layout.addLayout(slider_layout)
            self.sliders.append(slider)
        
        main_layout.addLayout(sliders_layout)
        self.equalizer_widget.setLayout(main_layout)
    
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
        freq_ranges = [(1, 32), (32, 64), (64, 125), (125, 250), (250, 500),
                       (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000)]
        
        for i, (low, high) in enumerate(freq_ranges):
            db_increase = self.sliders[i].value()
            AUD_1 = Edit.EQUALIZER(AUD_1, self.SPL_RTE, db_increase, low, high)
        
        AUD_1 = np.int16(AUD_1 / np.max(np.abs(AUD_1)) * 32767)
        
        AUD_1_PATH = f"{os.path.splitext(self.AUD_PATH)[0]}_equalized.wav"
        sf.write(AUD_1_PATH, AUD_1, self.SPL_RTE, format='wav')
        print(f"[LOG] EXPORT -> Exported file to: {AUD_1_PATH}")

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    VIEW = SonicEdit()
    VIEW.show()
    sys.exit(APP.exec())