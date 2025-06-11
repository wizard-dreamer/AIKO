from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import Qt, QTimer
import sys
from voice_input import record_and_transcribe
from brain import generate_reply
from tts import text_to_speech
from voice_output import speak

class AikoFace(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Aiko Face")
        self.setStyleSheet("background-color: black;")
        self.showFullScreen()

        # Eye label
        self.eye_label = QLabel(self)
        self.eye_pixmap = QPixmap("assets/eyes_open.png")
        self.eye_glow_pixmap = QPixmap("assets/eyes_glow.png")
        self.eye_label.setPixmap(self.eye_pixmap)
        self.eye_label.setGeometry(600, 200, 200, 100)  # Adjust these

        # Mouth label
        self.mouth_label = QLabel(self)
        self.mouth_normal_pixmap = QPixmap("assets/mouth_normal.png")
        self.mouth_talking_pixmap = QPixmap("assets/mouth_talking.png")
        self.mouth_label.setPixmap(self.mouth_normal_pixmap)
        self.mouth_label.setGeometry(650, 400, 100, 50)  # Adjust these

        # Talking timer
        self.talking_timer = QTimer()
        self.talking_timer.timeout.connect(self.toggle_mouth)

        self.mouth_state = False

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            print("Listening...")
            self.eye_label.setPixmap(self.eye_glow_pixmap)

            user_text = record_and_transcribe()
            print(f"You said: {user_text}")

            if user_text:
                reply = generate_reply(user_text)
                print(f"Aiko: {reply}")

                # Animate talking mouth
                self.start_talking_animation()
                audio_file = text_to_speech(reply)
                speak(audio_file)
                self.stop_talking_animation()

            # Reset eyes to normal
            self.eye_label.setPixmap(self.eye_pixmap)

    def start_talking_animation(self):
        self.mouth_state = False
        self.talking_timer.start(300)  # switch mouth every 300ms

    def stop_talking_animation(self):
        self.talking_timer.stop()
        self.mouth_label.setPixmap(self.mouth_normal_pixmap)

    def toggle_mouth(self):
        if self.mouth_state:
            self.mouth_label.setPixmap(self.mouth_normal_pixmap)
        else:
            self.mouth_label.setPixmap(self.mouth_talking_pixmap)
        self.mouth_state = not self.mouth_state

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AikoFace()
    window.show()
    sys.exit(app.exec())
