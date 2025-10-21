import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException, InvalidSessionIdException

def get_chrome_driver(timeout=15):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(timeout)
    return driver

def scrape_werkenvoornederland(with_description=True, max_scrolls=30):
    def fetch_vacature_description_safe(link, title, max_retries=3):
        for attempt in range(max_retries):
            try:
                resp = requests.get(link, timeout=(5, 10))  # <— snellere timeout
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                sections = soup.select("div.width-100")
    
                text_parts = []
                for sec in sections:
                    heading = sec.select_one("h2")
                    content = sec.select_one("div.s-article-content")
                    if heading and content and heading.text.strip() in [
                        "Dit ga je doen",
                        "Dit vragen wij",
                        "Hier kom je te werken",
                    ]:
                        text_parts.append(f"### {heading.text.strip()}\n{content.text.strip()}")
    
                return "\n\n".join(text_parts)
    
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Beschrijving poging {attempt+1}/{max_retries} mislukt ({title}): {e}")
                time.sleep(2 ** attempt)
    
        print(f"❌ Beschrijving mislukt voor {title}.")
        return ""

    def start_driver():
        driver = get_chrome_driver()
        driver.set_page_load_timeout(30)
        driver.get(
            "https://www.werkenvoornederland.nl/vacatures?"
            "type=vacature&werkdenkniveau=CWD.04%2CCWD.08&"
            "vakgebied=CVG.02%2CCVG.32%2CCVG.08"
        )
        time.sleep(3)
        return driver

    def scroll_page(driver):
        last_count = 0
        for _ in range(max_scrolls):
            vacatures = driver.find_elements(By.CSS_SELECTOR, "div.vacancy-list__item section.vacancy")
            if len(vacatures) == last_count:
                break
            last_count = len(vacatures)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        return driver.find_elements(By.CSS_SELECTOR, "div.vacancy-list__item section.vacancy")

    driver = start_driver()
    vacatures = scroll_page(driver)

    data = []
    seen_links = set()
    idx = 0

    while idx < len(vacatures):
        try:
            vac = vacatures[idx]
            title_el = vac.find_element(By.CSS_SELECTOR, "h2.vacancy__title a")
            title = title_el.text.strip()
            link = title_el.get_attribute("href")

            if not link or link in seen_links:
                idx += 1
                continue
            seen_links.add(link)

            try:
                regio = vac.find_element(
                    By.CSS_SELECTOR,
                    "li.job-short-info__item-icon span.job-short-info__value-icon"
                ).text.strip()
            except NoSuchElementException:
                regio = ""

            desc = ""
            if with_description:
                desc = fetch_vacature_description_safe(link, title)

            data.append({
                "Titel": title,
                "Regio": regio,  # <-- Locatie komt hier in "Regio"
                "Link": link,
                "Beschrijving": desc,
                "Bron": "Werken voor Nederland"
            })

            #print(f"[{idx+1}/{len(vacatures)}] ✅ {title}")
            idx += 1

        except (TimeoutError, WebDriverException, InvalidSessionIdException) as e:
            print(f"⚠️ Selenium-timeout of sessieprobleem ({type(e).__name__}) — herstarten en hervatten bij index {idx}...")
            try:
                driver.quit()
            except:
                pass
            time.sleep(5)
            driver = start_driver()
            vacatures = scroll_page(driver)
            continue

    driver.quit()
    df = pd.DataFrame(data)

    
    woonplaatsen_df = pd.read_csv("woonplaatsen.csv")  #
    plaats_to_provincie = dict(zip(
        woonplaatsen_df['Plaats'].str.lower().str.strip(),
        woonplaatsen_df['Provincie'].str.strip()
    ))
    df['Regio'] = df['Regio'].str.lower().map(plaats_to_provincie).fillna(df['Regio'])
    
    print(f"\n📄 Totaal {len(df)} vacatures succesvol opgehaald.")
    return df
