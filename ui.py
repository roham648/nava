import sys
from pathlib import Path
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
from PyQt6.QtCore import QThread, pyqtSignal
from stt import speech_to_text
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel
)

class SpeechThread(QThread):
    result = pyqtSignal(str)
    def run(self):
        text = speech_to_text()
        self.result.emit(text)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice To Text")
        self.resize(500, 400)
        layout = QVBoxLayout()
        self.button = QPushButton(
            "🎤 شروع ضبط"
        )
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.status = QLabel(
            "آماده"
        )
        layout.addWidget(self.status)
        layout.addWidget(self.button)
        layout.addWidget(self.text_box)
        self.setLayout(layout)
        self.button.clicked.connect(
            self.start_recording
        )
        self.thread = None


    def start_recording(self):
        self.button.setEnabled(False)
        self.button.setText(
            "🎤 در حال گوش دادن..."
        )
        self.status.setText(
            "صحبت کنید..."
        )
        self.thread = SpeechThread()
        self.thread.result.connect(
            self.show_result
        )
        self.thread.start()

    def show_result(self, text):
        self.text_box.setText(text)
        self.status.setText(
            "متن دریافت شد"
        )
        self.button.setEnabled(True)
        self.button.setText(
            "🎤 شروع ضبط"
        )

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
