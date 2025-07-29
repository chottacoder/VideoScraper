from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from tqdm import tqdm
import time
import os
import requests

def setup_driver():
    options = Options()
    options.headless = True
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

def download_file(video_url, save_path):
    print(f"\n⬇️ Downloading to: {save_path}")
    response = requests.get(video_url, stream=True)
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

def download_from_hqporner(url, save_dir="downloads"):
    print(f"\n🔄 Launching Firefox for: {url}")
    driver = setup_driver()

    try:
        driver.get(url)
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        sources = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "source"))
        )

        quality_map = {}
        for source in sources:
            title = source.get_attribute("title") or "unknown"
            src = source.get_attribute("src")
            if title and src:
                quality_map[title.lower()] = src

        if not quality_map:
            print("❌ No video sources found.")
            return

        print("\n🎥 Available Qualities:")
        for idx, quality in enumerate(quality_map.keys(), start=1):
            print(f"{idx}. {quality}")

        choice = input("\n👉 Choose quality (e.g., 360p, 720p, 1080p): ").strip().lower()
        selected_src = quality_map.get(choice)

        if not selected_src:
            print("❌ Invalid choice or quality not available.")
            return

        if selected_src.startswith("//"):
            selected_src = "https:" + selected_src

        print(f"🎯 Selected video URL:\n{selected_src}")
        slug = url.strip("/").split("/")[-1]
        filename = slug.replace("-", "_") + f"_{choice}.mp4"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        download_file(selected_src, save_path)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

def download_from_incestflix(url, save_dir="downloads"):
    print(f"\n🔄 Launching Firefox for: {url}")
    driver = setup_driver()
    driver.get(url)
    time.sleep(5)

    try:
        video = driver.find_element(By.TAG_NAME, "video")
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

        download_file(video_src, save_path)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

def download_from_superporn(url, save_dir="downloads"):
    print(f"\n🔄 Launching Firefox for: {url}")
    driver = setup_driver()
    driver.get(url)
    time.sleep(5)

    try:
        video = driver.find_element(By.ID, "superporn_player_html5_api")
        video_src = video.get_attribute("src")

        if not video_src:
            video = driver.find_element(By.TAG_NAME, "video")
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

        download_file(video_src, save_path)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

# ========== MAIN MENU ==========

if __name__ == "__main__":
    print("🎬 Video Downloader")
    try:
        url = input("🔗 Enter video URL: \n").strip()
        checkUrl = url.split("/")[2]  # Extract domain from URL

        # print(url.split("/")[2])  # Debugging line to check URL structure
        
        if checkUrl == "hqporner.com" or checkUrl == "www.hqporner.com":
            download_from_hqporner(url)
        elif checkUrl == "www.incestflix.com" or checkUrl == "incestflix.com":
            download_from_incestflix(url)
        elif checkUrl == "www.superporn.com" or checkUrl == "superporn.com":
            download_from_superporn(url)
        else:
            print("i will try to download from other sites, please wait...")
            download_from_incestflix(url)
    except ValueError:
        print("Sorry cant download from this site, please try another one. 😢")
