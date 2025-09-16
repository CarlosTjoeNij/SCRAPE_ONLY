# scraper_core.py
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st  # Voor secrets

from platformen.striive import scrape_striive
from platformen.flextender import scrape_flextender
from platformen.yacht import scrape_yacht

# --- COMBINED SCRAPE ---
def scrape_all_jobs():
    start_time = time.time()
    print("➡️ Start scrape: Striive")
    df_striive = scrape_striive()

    print("➡️ Start scrape: Flextender")
    df_flex = scrape_flextender()

    #print("➡️ Start scrape: Yacht")
    #df_yacht = scrape_yacht()

    df_combined = pd.concat([df_striive, df_flex], ignore_index=True)
    duration = time.time() - start_time
    print(f"✅ Scraping voltooid in {duration/60:.1f} minuten")
    return df_combined
