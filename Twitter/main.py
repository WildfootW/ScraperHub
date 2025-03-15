#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyleft (ɔ) 2025 wildfootw <wildfootw@wildfoo.tw>
#
# Distributed under terms of the MIT license.

import os
import time
import requests
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse

# Twitter username to scrape
USERNAME = "kumattoforest"
OUTPUT_DIR = "kumattoforest_images"
DELAY_BETWEEN_REQUESTS = 3  # Seconds between each image download
TIMEOUT_MS = 120000  # 120 seconds timeout for loading the page
SCROLL_PAUSE_TIME = 5  # Wait time after each scroll to let tweets load

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_image(url):
    """Download an image and save it locally."""
    original_url = url.replace("&name=small", "&name=orig")  # Get original resolution
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(original_url, headers=headers, stream=True)

    if response.status_code == 200:
        filename = os.path.join(OUTPUT_DIR, os.path.basename(urlparse(original_url).path))
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {original_url}")

def scrape_twitter_images():
    """Use Playwright to scroll through the Twitter timeline and extract images."""
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Make browser visible
        page = browser.new_page()

        print("Opening Twitter...")
        page.goto(f"https://twitter.com/{USERNAME}", timeout=TIMEOUT_MS)  # 120s timeout

        image_urls = set()
        last_height = 0

        while True:  # Infinite scrolling
            # Extract image URLs
            images = page.query_selector_all("img")
            for img in images:
                src = img.get_attribute("src")
                if src and "pbs.twimg.com" in src:
                    image_urls.add(src)

            # Scroll down & wait for new tweets to load
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(SCROLL_PAUSE_TIME)  # **Wait longer to let tweets load**

            # Check if new content appeared
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                print("Waiting for new tweets to load...")
                time.sleep(10)  # **Give extra time before checking again**
                new_height = page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    print("No new tweets loaded, stopping.")
                    break
            last_height = new_height

        browser.close()

    # Download all collected images
    for img_url in image_urls:
        download_image(img_url)
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Respect rate limits

if __name__ == "__main__":
    scrape_twitter_images()

