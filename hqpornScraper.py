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

def download_video_from_hqporner(url, save_dir="downloads"):
    print(f"\n🔄 Launching Firefox for: {url}")

    options = Options()
    options.headless = True
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(url)

        # Wait for iframe and switch to it
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        # Wait for <video> or <source> inside iframe
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

        print(f"\n⬇️ Downloading to: {save_path}")
        response = requests.get(selected_src, stream=True)
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
    url = input("🔗 Enter HqPorner video URL: ").strip()
    download_video_from_hqporner(url)
