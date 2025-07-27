# 🎥 VideoScraper

A GUI-based Python app to extract and download videos from JavaScript-heavy sites like SuperPorn — **without using Selenium**.

---

## 💡 How It Works

1. Launches a PyQt5 GUI with an embedded browser
2. Loads the target SuperPorn video page (JavaScript-enabled)
3. Waits for the `<video id="superporn_player_html5_api">` element
4. Extracts the real video stream URL (`src`)
5. Downloads the video using `requests`
6. Displays a live progress bar during download
7. Saves the video as `downloads/video-title.mp4`

---

## 📦 Installation

Make sure Python 3.7+ is installed.

Install dependencies:

```bash
pip install PyQt5 PyQtWebEngine requests tqdm
```

---

## 🚀 Usage

1. Run the script:

```bash
python your_script.py
```

2. Paste the video URL in the input field.
3. Click "Load & Extract Video".
4. Wait for the video to load and start downloading.
5. The video will be saved in the `downloads/` folder with a clean filename.

---

## 🖥️ Features

* ✅ No Selenium required
* ✅ Supports JavaScript-heavy pages
* ✅ Embedded browser (Chromium via QtWebEngine)
* ✅ Auto video URL detection
* ✅ Live download progress bar
* ✅ Simple 300x300 GUI window

---

## 📁 Output

All downloaded videos are saved to:

```
downloads/your_video.mp4
```

---

## 🛠️ Optional Packaging

Convert to `.exe` using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile your_script.py
```

---

## ⚠️ Disclaimer

This tool is for educational and personal use only.
**Always respect website terms of service and content copyright.**

