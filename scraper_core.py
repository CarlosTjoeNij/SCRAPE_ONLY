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

    # # werkeninzuidoostbrabant
    # try:
    #     print("➡️ Start scrape: werkeninzuidoostbrabant")
    #     df_werkeninzuidoostbrabant = scrape_werkeninzuidoostbrabant()
    #     dfs.append(df_werkeninzuidoostbrabant)
    #     print(f"✅ werkeninzuidoostbrabant done, {len(df_werkeninzuidoostbrabant)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping werkeninzuidoostbrabant: {e}")

    # # gemeentebanen
    # try:
    #     print("➡️ Start scrape: Gemeentebanen")
    #     df_gemeentebanen = scrape_gemeentebanen()
    #     dfs.append(df_gemeentebanen)
    #     print(f"✅ Gemeentebanen done, {len(df_gemeentebanen)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Gemeentebanen: {e}")
        
    # # greenjobs
    # try:
    #     print("➡️ Start scrape: Greenjobs")
    #     df_greenjobs = scrape_greenjobs()
    #     dfs.append(df_greenjobs)
    #     print(f"✅ Greenjobs done, {len(df_greenjobs)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Greenjobs: {e}")

    # # werkeninnoordhollandnoord
    # try:
    #     print("➡️ Start scrape: Werkeninnoordhollandnoord")
    #     df_werkeninnoordhollandnoord = scrape_werkeninnoordhollandnoord()
    #     dfs.append(df_werkeninnoordhollandnoord)
    #     print(f"✅ Werkeninnoordhollandnoord done, {len(df_werkeninnoordhollandnoord)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Werkeninnoordhollandnoord: {e}")

    # # werkeninfriesland
    # try:
    #     print("➡️ Start scrape: Werkeninfriesland")
    #     df_werkeninfriesland = scrape_werkeninfriesland()
    #     dfs.append(df_werkeninfriesland)
    #     print(f"✅ Werkeninfriesland done, {len(df_werkeninfriesland)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Werkeninfriesland: {e}")    

    # # werkenvoorgroningen
    # try:
    #     print("➡️ Start scrape: Werkenvoorgroningen")
    #     df_werkenvoorgroningen = scrape_werkenvoorgroningen()
    #     dfs.append(df_werkenvoorgroningen)
    #     print(f"✅ Werkenvoorgroningen done, {len(df_werkenvoorgroningen)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Werkenvoorgroningen: {e}") 

    # # vooruitindrenthe
    # try:
    #     print("➡️ Start scrape: Vooruitindrenthe")
    #     df_vooruitindrenthe = scrape_vooruitindrenthe()
    #     dfs.append(df_vooruitindrenthe)
    #     print(f"✅ Vooruitindrenthe done, {len(df_vooruitindrenthe)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Vooruitindrenthe: {e}")

    # # werkenaanhetnoorden
    # try:
    #     print("➡️ Start scrape: Werkenaanhetnoorden")
    #     df_werkenaanhetnoorden = scrape_werkenaanhetnoorden()
    #     dfs.append(df_werkenaanhetnoorden)
    #     print(f"✅ Werkenaanhetnoorden done, {len(df_werkenaanhetnoorden)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Werkenaanhetnoorden: {e}")

    # # noordnederlandwerkt
    # try:
    #     print("➡️ Start scrape: Noordnederlandwerkt")
    #     df_noordnederlandwerkt = scrape_noordnederlandwerkt()
    #     dfs.append(df_noordnederlandwerkt)
    #     print(f"✅ Noordnederlandwerkt done, {len(df_noordnederlandwerkt)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Noordnederlandwerkt: {e}")
        
    # # noorderlink
    # try:
    #     print("➡️ Start scrape: Noorderlink")
    #     df_noorderlink = scrape_noorderlink()
    #     dfs.append(df_noorderlink)
    #     print(f"✅ Noorderlink done, {len(df_noorderlink)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Noorderlink: {e}")

    # # vacaturebanknoordnederland
    # try:
    #     print("➡️ Start scrape: Vacaturebanknoordnederland")
    #     df_vacaturebanknoordnederland = scrape_vacaturebanknoordnederland()
    #     dfs.append(df_vacaturebanknoordnederland)
    #     print(f"✅ Vacaturebanknoordnederland done, {len(df_vacaturebanknoordnederland)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Vacaturebanknoordnederland: {e}")

    # # vacaturesnoordholland
    # try:
    #     print("➡️ Start scrape: Vacaturesnoordholland")
    #     df_vacaturesnoordholland = scrape_vacaturesnoordholland()
    #     dfs.append(df_vacaturesnoordholland)
    #     print(f"✅ Vacaturesnoordholland done, {len(df_vacaturesnoordholland)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Vacaturesnoordholland: {e}")

    # # werkenbijnod
    # try:
    #     print("➡️ Start scrape: Werkenbijnod")
    #     df_werkenbijnod = scrape_werkenbijnod()
    #     dfs.append(df_werkenbijnod)
    #     print(f"✅ Werkenbijnod done, {len(df_werkenbijnod)} rows")
    # except Exception as e:
    #     print(f"❌ Fout tijdens scraping Werkenbijnod: {e}")
        
    if dfs:
        df_combined = pd.concat(dfs, ignore_index=True)
    else:
        df_combined = pd.DataFrame()

    duration = time.time() - start_time
    print(f"⏱️ Scraping voltooid in {duration/60:.1f} minuten")
    return df_combined
