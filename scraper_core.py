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
from concurrent.futures import ProcessPoolExecutor, as_completed

from platformen.striive import scrape_striive
from platformen.flextender import scrape_flextender
from platformen.yacht import scrape_yacht
from platformen.igom import scrape_igom
from platformen.werkenvoornederland import scrape_werkenvoornederland
from platformen.werkeninnoordoostbrabant import scrape_werkeninnoordoostbrabant
from platformen.werkeninzuidoostbrabant import scrape_werkeninzuidoostbrabant
from platformen.gemeentebanen import scrape_gemeentebanen
from platformen.greenjobs import scrape_greenjobs
from platformen.werkeninnoordhollandnoord import scrape_werkeninnoordhollandnoord
from platformen.werkeninfriesland import scrape_werkeninfriesland
from platformen.werkenvoorgroningen import scrape_werkenvoorgroningen
from platformen.vooruitindrenthe import scrape_vooruitindrenthe
from platformen.werkenaanhetnoorden import scrape_werkenaanhetnoorden
from platformen.noordnederlandwerkt import scrape_noordnederlandwerkt
from platformen.noorderlink import scrape_noorderlink
from platformen.vacaturebanknoordnederland import scrape_vacaturebanknoordnederland
from platformen.vacaturesnoordholland import scrape_vacaturesnoordholland
from platformen.werkenbijnod import scrape_werkenbijnod


# Alle scraper-functies in één lijst
SCRAPERS = [
    ("Striive", scrape_striive),
    ("Flextender", scrape_flextender),
    ("Yacht", scrape_yacht),
    ("IGOM", scrape_igom),
    ("Werkenvoornederland", scrape_werkenvoornederland),
    ("Werkeninnoordoostbrabant", scrape_werkeninnoordoostbrabant),
    ("Werkeninzuidoostbrabant", scrape_werkeninzuidoostbrabant),
    ("Gemeentebanen", scrape_gemeentebanen),
    ("Greenjobs", scrape_greenjobs),
    ("Werkeninnoordhollandnoord", scrape_werkeninnoordhollandnoord),
    ("Werkeninfriesland", scrape_werkeninfriesland),
    ("Werkenvoorgroningen", scrape_werkenvoorgroningen),
    ("Vooruitindrenthe", scrape_vooruitindrenthe),
    ("Werkenaanhetnoorden", scrape_werkenaanhetnoorden),
    ("Noordnederlandwerkt", scrape_noordnederlandwerkt),
    ("Noorderlink", scrape_noorderlink),
    ("Vacaturebanknoordnederland", scrape_vacaturebanknoordnederland),
    ("Vacaturesnoordholland", scrape_vacaturesnoordholland),
    ("Werkenbijnod", scrape_werkenbijnod),
]


def run_scraper(name, func):
    """Wrapper zodat elk proces fouten kan teruggeven."""
    print(f"➡️ Start scrape: {name}")
    try:
        df = func()
        print(f"✅ {name} klaar ({len(df)} rows)")
        return df
    except Exception as e:
        print(f"❌ Fout tijdens scraping {name}: {e}")
        return pd.DataFrame()


def scrape_all_jobs():
    start = time.time()
    dfs = []

    # Max 6–8 parallel, anders te veel Chrome-instances
    max_workers = min(8, len(SCRAPERS))

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_scraper, name, func): name
            for name, func in SCRAPERS
        }

        for future in as_completed(futures):
            df = future.result()
            dfs.append(df)

    if dfs:
        df_all = pd.concat(dfs, ignore_index=True)
    else:
        df_all = pd.DataFrame()

    duration = (time.time() - start) / 60
    print(f"⏱️ Parallel scraping voltooid in {duration:.1f} minuten")

    return df_all

if __name__ == "__main__":
    scrape_all_jobs()
