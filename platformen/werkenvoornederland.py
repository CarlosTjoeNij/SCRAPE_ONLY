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
    def fetch_vacature_description(link, title):
        """Haalt de beschrijving van de detailpagina (snel via requests)."""
        try:
            resp = requests.get(link, timeout=(5, 10))
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
        except Exception as e:
            print(f"⚠️ Beschrijving mislukt ({title}): {e}")
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

    wait = WebDriverWait(driver, 6)
    data = []
    seen_links = set()

    for idx, vac in enumerate(vacatures):
        try:
            title_el = vac.find_element(By.CSS_SELECTOR, "h2.vacancy__title a")
            title = title_el.text.strip()
            link = title_el.get_attribute("href")
            if not link.startswith("http"):
                link = "https://www.werkenvoornederland.nl" + link
            if link in seen_links:
                continue
            seen_links.add(link)

            # Plaats
            try:
                plaats = vac.find_element(By.CSS_SELECTOR, "li.job-short-info__item-icon span.job-short-info__value-icon").text.strip()
            except NoSuchElementException:
                plaats = ""

            # Opdrachtgever
            try:
                opdrachtgever = vac.find_element(By.CSS_SELECTOR, "p.vacancy__employer").text.strip()
            except NoSuchElementException:
                opdrachtgever = ""

            # Beschrijving via requests
            beschrijving = fetch_vacature_description(link, title) if with_description else ""

            # --- Email via Selenium ---
            email = ""
            try:
                # Open vacaturepagina
                driver.execute_script("window.open(arguments[0]);", link)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)

                # Wachten tot e-mail zichtbaar (max 5 sec)
                email_el = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "span.job-contact-person__email a[href^='mailto:']")
                    )
                )
                email = email_el.text.strip()

            except TimeoutException:
                email = ""
            except Exception as e:
                print(f"⚠️ Geen email gevonden bij {title}: {e}")
            finally:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            data.append({
                "Titel": title,
                "Plaats": plaats,
                "Regio": plaats,  # later mappen
                "Opdrachtgever": opdrachtgever,
                "Email": email,
                "Link": link,
                "Beschrijving": beschrijving,
                "Bron": "Werken voor Nederland"
            })

        except Exception as e:
            print(f"⚠️ Fout bij vacature {idx+1}: {e}")
            continue

    driver.quit()
    df = pd.DataFrame(data)

    # Mapping Plaats → Provincie
    woonplaatsen_df = pd.read_csv("woonplaatsen.csv")
    plaats_to_provincie = dict(zip(
        woonplaatsen_df['Plaats'].str.lower().str.strip(),
        woonplaatsen_df['Provincie'].str.strip()
    ))

    df["Regio"] = df["Plaats"].str.lower().map(plaats_to_provincie).fillna(df["Plaats"])
    return df
