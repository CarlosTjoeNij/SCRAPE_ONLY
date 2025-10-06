import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

import time
import numpy as np

import re
import requests

woonplaatsen_df = pd.read_csv("woonplaatsen.csv")  # kolommen: 'Plaats', 'Provincie'
plaats_to_provincie = dict(zip(woonplaatsen_df['Plaats'].str.lower(), woonplaatsen_df['Provincie']))

def get_chrome_driver(timeout=20):
    chrome_options = Options()
    
    # Cloud Run / headless compatibele opties
    chrome_options.add_argument("--headless=new")  # Headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(timeout)
    
    # Mask webdriver property
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
            """
        }
    )
    
    return driver

def scrape_circle8(with_description=True, max_pages=None):
    driver = get_chrome_driver()
    base_url = "https://www.circle8.nl/opdrachten"
    data = []

    try:
        page = 1
        while True:
            if max_pages and page > max_pages:
                print("Max pagina limiet bereikt, stoppen.")
                break

            url = f"{base_url}?page={page}" if page > 1 else base_url
            driver.get(url)
            wait = WebDriverWait(driver, 15)

            time.sleep(2)  # korte extra pauze voor rendering

            # Vacatures zoeken
            try:
                wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "a.c-vacancy-grid-card__wrapper")
                    )
                )
            except:
                print(f"Geen vacatures gevonden op pagina {page}.")
                break

            vacatures = driver.find_elements(By.CSS_SELECTOR, "a.c-vacancy-grid-card__wrapper")

            if not vacatures:
                break

            for vac in vacatures:
                try:
                    title = vac.find_element(By.CSS_SELECTOR, "h3.c-vacancy-grid-card__title").text.strip()
                except:
                    title = ""
                try:
                    link = vac.get_attribute("href")
                except:
                    link = ""

                # Plaats ophalen
                plaats = ""
                for usp in vac.find_elements(By.CSS_SELECTOR, "div.c-vacancy-grid-card__usp h5"):
                    text = usp.text.strip()
                    if text and not any(char.isdigit() for char in text):
                        plaats = text
                        break

                provincie = plaats_to_provincie.get(plaats.lower(), plaats)

                # Beschrijving
                description = ""
                if with_description and link:
                    driver.execute_script("window.open(arguments[0]);", link)
                    driver.switch_to.window(driver.window_handles[-1])
                    try:
                        desc_elem = wait.until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "div.c-vacancy-paragraph__body-text")
                            )
                        )
                        description = desc_elem.text.strip()
                    except:
                        description = ""
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                data.append({
                    "Titel": title,
                    "Regio": provincie,
                    "Link": link,
                    "Beschrijving": description,
                    "Bron": "Circle8"
                })

            # Pagination check
            pagination_links = driver.find_elements(By.CSS_SELECTOR, "a.c-lister-pagination__page")
            active_page = None

            for link in pagination_links:
                if "c-lister-pagination__page--active" in link.get_attribute("class"):
                    active_page = link
                    break

            # Stoppen als dit de laatste pagina is
            if not pagination_links or (active_page and active_page == pagination_links[-1]):
                break

            page += 1

        df = pd.DataFrame(data)
        return df

    finally:
        driver.quit()
