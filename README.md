# VideoScraper

💡 How It Works:

    Launches a headless Firefox browser
    Opens the target SuperPorn video page
    Waits for the <video id="superporn_player_html5_api"> element
    Extracts the video stream URL (src)
    Downloads the video using requests
    Displays a beautiful progress bar during the download
    Saves the file as downloads/video-title.mp4
