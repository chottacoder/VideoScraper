from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from tqdm import tqdm
import time
import os
import requests

def download_video_from_superporn_firefox(url, save_dir="downloads"):
    print(f"\n🔄 Launching Firefox for: {url}")

    options = Options()
    options.headless = True
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(url)
    time.sleep(5)

    try:
        video = driver.find_element(By.ID, "superporn_player_html5_api")
        video_src = video.get_attribute("src")

        if not video_src:
            source = video.find_element(By.TAG_NAME, "source")
            video_src = source.get_attribute("src")

        if not video_src:
            print("❌ Video source not found.")
            return

        print(f"🎯 Found video URL:\n{video_src}")

        slug = url.strip("/").split("/")[-1]
        filename = slug.replace("-", "_") + ".mp4"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        print(f"\n⬇️ Downloading to: {save_path}")
        response = requests.get(video_src, stream=True)
        total = int(response.headers.get('content-length', 0))

        with open(save_path, "wb") as f, tqdm(
            desc="📥 Progress",
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print("✅ Download complete!")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

# Run it
if __name__ == "__main__":
    url = input("🔗 Enter SuperPorn video URL: ").strip()
    download_video_from_superporn_firefox(url)
