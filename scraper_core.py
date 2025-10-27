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

from platformen.striive import scrape_striive
from platformen.flextender import scrape_flextender
from platformen.yacht import scrape_yacht
from platformen.circle8 import scrape_circle8
from platformen.igom import scrape_igom
from platformen.werkenvoornederland import scrape_werkenvoornederland
from platformen.werkeninnoordoostbrabant import scrape_werkeninnoordoostbrabant
from platformen.werkeninzuidoostbrabant import scrape_werkeninzuidoostbrabant
from platformen.gemeentebanen import scrape_gemeentebanen
from platformen.greenjobs import scrape_greenjobs
from platformen.werkeninnoordhollandnoord import scrape_werkeninnoordhollandnoord

# --- COMBINED SCRAPE ---
def scrape_all_jobs():
    start_time = time.time()
    dfs = []

    # Striive
    try:
        print("➡️ Start scrape: Striive")
        df_striive = scrape_striive()
        dfs.append(df_striive)
        print(f"✅ Striive done, {len(df_striive)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping Striive: {e}")

    # Flextender
    try:
        print("➡️ Start scrape: Flextender")
        df_flex = scrape_flextender()
        dfs.append(df_flex)
        print(f"✅ Flextender done, {len(df_flex)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping Flextender: {e}")

    # Yacht
    try:
        print("➡️ Start scrape: Yacht")
        df_yacht = scrape_yacht()
        dfs.append(df_yacht)
        print(f"✅ Yacht done, {len(df_yacht)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping Yacht: {e}")

    # Circle8
    try:
        print("➡️ Start scrape: Circle8")
        df_circle8 = scrape_circle8()
        dfs.append(df_circle8)
        print(f"✅ Circle8 done, {len(df_circle8)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping Circle8: {e}")
    # IGOM
    try:
        print("➡️ Start scrape: IGOM")
        df_igom = scrape_igom()
        dfs.append(df_igom)
        print(f"✅ IGOM done, {len(df_igom)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping IGOM: {e}")

    # werkenvoornederland
    try:
        print("➡️ Start scrape: werkenvoornederland")
        df_werkenvoornederland = scrape_werkenvoornederland()
        dfs.append(df_werkenvoornederland)
        print(f"✅ werkenvoornederland done, {len(df_werkenvoornederland)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping werkenvoornederland: {e}")

    # werkeninnoordoostbrabant
    try:
        print("➡️ Start scrape: werkeninnoordoostbrabant")
        df_werkeninnoordoostbrabant = scrape_werkeninnoordoostbrabant()
        dfs.append(df_werkeninnoordoostbrabant)
        print(f"✅ werkeninnoordoostbrabant done, {len(df_werkeninnoordoostbrabant)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping werkeninnoordoostbrabant: {e}")

    # werkeninzuidoostbrabant
    try:
        print("➡️ Start scrape: werkeninzuidoostbrabant")
        df_werkeninzuidoostbrabant = scrape_werkeninzuidoostbrabant()
        dfs.append(df_werkeninzuidoostbrabant)
        print(f"✅ werkeninzuidoostbrabant done, {len(df_werkeninzuidoostbrabant)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping werkeninzuidoostbrabant: {e}")

    # gemeentebanen
    try:
        print("➡️ Start scrape: Gemeentebanen")
        df_gemeentebanen = scrape_gemeentebanen()
        dfs.append(df_gemeentebanen)
        print(f"✅ Gemeentebanen done, {len(df_gemeentebanen)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping Gemeentebanen: {e}")
        
    # greenjobs
    try:
        print("➡️ Start scrape: Greenjobs")
        df_greenjobs = scrape_greenjobs()
        dfs.append(df_greenjobs)
        print(f"✅ Greenjobs done, {len(df_greenjobs)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping Greenjobs: {e}")

    # werkeninnoordhollandnoord
    try:
        print("➡️ Start scrape: Werkeninnoordhollandnoord")
        df_werkeninnoordhollandnoord = scrape_werkeninnoordhollandnoord()
        dfs.append(df_werkeninnoordhollandnoord)
        print(f"✅ Werkeninnoordhollandnoord done, {len(df_werkeninnoordhollandnoord)} rows")
    except Exception as e:
        print(f"❌ Fout tijdens scraping Werkeninnoordhollandnoord: {e}")

    if dfs:
        df_combined = pd.concat(dfs, ignore_index=True)
    else:
        df_combined = pd.DataFrame()

    duration = time.time() - start_time
    print(f"⏱️ Scraping voltooid in {duration/60:.1f} minuten")
    return df_combined
