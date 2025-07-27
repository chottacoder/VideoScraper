import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QProgressBar, QLabel, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot
from urllib.parse import urlparse
from tqdm import tqdm


class VideoDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperPorn Video Downloader")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL")
        layout.addWidget(self.url_input)

        self.download_button = QPushButton("Load & Extract Video")
        layout.addWidget(self.download_button)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.status = QLabel("")
        layout.addWidget(self.status)

        self.browser = QWebEngineView()
        self.browser.setFixedHeight(100)
        layout.addWidget(self.browser)

        self.setLayout(layout)

        self.download_button.clicked.connect(self.start_loading)
        self.video_url = None

    def start_loading(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a video URL.")
            return

        self.browser.load(QUrl(url))
        self.browser.loadFinished.connect(self.extract_video_src)
        self.status.setText("🔄 Loading page...")

    @pyqtSlot(bool)
    def extract_video_src(self, ok):
        if ok:
            js = """
                (function() {
                    var video = document.getElementById("superporn_player_html5_api");
                    return video ? video.src || video.querySelector('source')?.src : null;
                })();
            """
            self.browser.page().runJavaScript(js, self.handle_video_src)
        else:
            self.status.setText("❌ Failed to load page.")

    def handle_video_src(self, video_url):
        if video_url:
            self.video_url = video_url
            self.status.setText("✅ Video found. Downloading...")
            self.download_video(video_url)
        else:
            self.status.setText("❌ Video source not found.")

    def download_video(self, url):
        os.makedirs("downloads", exist_ok=True)
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path).split("?")[0]
        save_path = os.path.join("downloads", filename)

        try:
            with requests.get(url, stream=True) as r:
                total = int(r.headers.get('content-length', 0))
                self.progress.setMaximum(total)

                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                            self.progress.setValue(self.progress.value() + len(chunk))

            self.status.setText("✅ Download complete!")
        except Exception as e:
            self.status.setText(f"❌ Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VideoDownloader()
    win.show()
    sys.exit(app.exec_())
