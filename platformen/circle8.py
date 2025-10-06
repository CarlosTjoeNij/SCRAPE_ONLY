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

# Laad woonplaatsen mapping CSV
woonplaatsen_df = pd.read_csv("woonplaatsen.csv")  # kolommen: 'Plaats', 'Provincie'
plaats_to_provincie = dict(zip(woonplaatsen_df['Plaats'].str.lower(), woonplaatsen_df['Provincie']))

def get_chrome_driver(timeout=15):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless=new")  # tijdelijk uit voor debug
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    # User-agent om headless detectie te omzeilen
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(timeout)
    return driver

def scrape_circle8(with_description=True):
    driver = get_chrome_driver()
    base_url = "https://www.circle8.nl/opdrachten"
    data = []

    try:
        page = 1
        while True:
            url = f"{base_url}?page={page}" if page > 1 else base_url
            driver.get(url)
            wait = WebDriverWait(driver, 15)

            # Wacht even voor volledige render
            time.sleep(3)

            # Check of vacatures aanwezig zijn
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.c-vacancy-grid-card__wrapper")))
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
                # Plaats ophalen: eerste h5 zonder cijfers
                plaats = ""
                for usp in vac.find_elements(By.CSS_SELECTOR, "div.c-vacancy-grid-card__usp h5"):
                    text = usp.text.strip()
                    if text and not any(char.isdigit() for char in text):
                        plaats = text
                        break
                provincie = plaats_to_provincie.get(plaats.lower(), plaats)

                # Beschrijving ophalen
                description = ""
                if with_description and link:
                    driver.execute_script("window.open(arguments[0]);", link)
                    driver.switch_to.window(driver.window_handles[-1])
                    try:
                        desc_elem = wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.c-vacancy-paragraph__body-text"))
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

            # Check voor volgende pagina
            try:
                next_page_elem = driver.find_element(By.CSS_SELECTOR, f"a.c-lister-pagination__page[href='?page={page+1}']")
                page += 1
            except:
                break

        df = pd.DataFrame(data)
        return df

    finally:
        driver.quit()
