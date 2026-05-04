import markdown
import sys
import requests
import psutil
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer, QSize
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLineEdit, QTextBrowser, QLabel)
from PyQt6.QtGui import QMovie

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:e4b"
DISTRACTIONS = ["spotify.exe","discord.exe","steam.exe"]

class OllamaWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, user_input):
        super().__init__()
        self.formatted_prompt = f"System: You are a whale assistant. Use bullet points. \nUser: {user_input}"

    def run(self):
        try:
            # Using 127.0.0.1 is perfect for local Windows Ollama
            url = "http://127.0.0.1:11434/api/generate"

            # The payload dictionary should be constructed here
            payload = {
                "model": "gemma4:e4b",
                "prompt": self.formatted_prompt,
                "stream": False
            }

            r = requests.post(url, json=payload, timeout=30)

            # Use .json() only if the request was successful
            if r.status_code == 200:
                answer = r.json().get("response", "The whale is diving...")
                self.finished.emit(answer)
            else:
                self.finished.emit(f"Error: Server returned status {r.status_code}")

        except Exception as e:
            self.finished.emit(f"Error: {e}")


class WhaleAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.nudge_timer = QTimer()
        self.nudge_timer.timeout.connect(self.proactive_nudge)
        self.nudge_timer.start(10000)

    def init_ui(self):
        # 1. Whale Window: Frameless & Transparent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.layout = QVBoxLayout()
        self.whale_label = QLabel(self)
        self.movie = QMovie("whale.gif")  # Ensure whale.gif is in the same folder
        self.movie.setScaledSize(QSize(120, 100))
        self.whale_label.setMovie(self.movie)
        self.movie.start()

        self.layout.addWidget(self.whale_label)
        self.setLayout(self.layout)

        # Position: Bottom right
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - 150, screen.height() - 150)

        # 2. Chat Box Window (The "Readability" Upgrade)
        self.chat_box = QWidget()
        self.chat_box.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.chat_box.setWindowTitle("Whale Assistant")
        self.chat_box.setStyleSheet("background-color: #1e1e1e; color: white;")

        chat_layout = QVBoxLayout()

        # History using QTextBrowser for Markdown/HTML support
        self.history = QTextBrowser()
        self.history.setReadOnly(True)
        self.history.setOpenExternalLinks(True)
        self.history.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #444;
            }
        """)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type and press Enter...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: #333; 
                color: white; 
                border-radius: 5px; 
                padding: 8px;
                border: 1px solid #555;
            }
        """)
        self.input_field.returnPressed.connect(self.handle_query)

        chat_layout.addWidget(self.history)
        chat_layout.addWidget(self.input_field)
        self.chat_box.setLayout(chat_layout)
        self.chat_box.resize(350, 450)

    def mousePressEvent(self, event):
        # Handle Dragging Logic
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

        # Handle Chat Box Toggle (keep your existing logic)
        if self.chat_box.isVisible():
            self.chat_box.hide()
        else:
            # Position chat box relative to where the whale is dropped
            self.chat_box.move(self.x() - 360, self.y() - 300)
            self.chat_box.show()

    def mouseMoveEvent(self, event):
        # This allows you to drag the whale around the screen
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def handle_query(self):
        query = self.input_field.text()
        if not query: return

        self.history.append(f"<b style='color: #a8dadc;'>You:</b> {query}")
        self.input_field.clear()
        self.history.append("<i style='color: #888;'>Whale is thinking...</i>")

        self.worker = OllamaWorker(query)
        self.worker.finished.connect(self.display_answer)
        self.worker.start()

    def display_answer(self, answer):
        # Convert Markdown to HTML for the browser
        html_answer = markdown.markdown(answer, extensions=['fenced_code', 'codehilite'])

        styled_message = f"""
            <div style='margin-top: 10px;'>
                <b style='color: #4da6ff;'>Whale:</b><br>
                {html_answer}
            </div>
            <hr style='border: 0; border-top: 1px solid #444; margin: 10px 0;'>
        """
        self.history.append(styled_message)

        # Force scroll to bottom
        self.history.verticalScrollBar().setValue(
            self.history.verticalScrollBar().maximum()
        )

    def proactive_nudge(self):
        try:
            running_apps = [p.info['name'].lower() for p in psutil.process_iter(['name'])]

            for app in DISTRACTIONS:
                if app.lower() in running_apps:
                    self.history.append(
                        "<b style='color: #ff4b4b;'>Whale:</b> Surface for air! You're on a distraction.")
                    if not self.chat_box.isVisible():
                        self.chat_box.show()
                    break
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    whale = WhaleAssistant()
    whale.show()
    sys.exit(app.exec())