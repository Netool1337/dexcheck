from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import traceback

# Chemin vers le navigateur Chrome
driver_path = "C:\\Users\\Hugo\\Bureau\\chromedriver-win64\\chromedriver.exe"

def scrape_address(adresse):
    attempts = 0
    max_attempts = 3  # Nombre maximal de tentatives
    success = False

    while attempts < max_attempts and not success:
        try:
            # Configuration de Selenium WebDriver
            chrome_options = Options()
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--force-color-profile=srgb")
            chrome_options.add_argument("--metrics-recording-only")
            chrome_options.add_argument("--password-store=basic")
            chrome_options.add_argument("--use-mock-keychain")
            chrome_options.add_argument("--export-tagged-pdf")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-background-mode")
            chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions")
            chrome_options.add_argument("--disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage")
            chrome_options.add_argument("--deny-permission-prompts")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--accept-lang=en-US")
            chrome_options.add_argument("--start-maximized")

            # Créer une instance de WebDriver
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Construire l'URL pour chaque adresse
            url = f"https://dexcheck.ai/app/wallet-analyzer/{adresse}"
            print(f"Ouverture de l'URL : {url}")
            driver.get(url)

            # Attendre que la page se charge complètement
            print("Attente de 20 secondes pour que la page se charge complètement...")
            time.sleep(20)  # Ajuste le délai d'attente si nécessaire

            # Récupérer le code HTML de la page
            html_content = driver.page_source

            # Utiliser BeautifulSoup pour parser le HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Afficher le HTML formaté
            #print(soup.prettify())

            # Utiliser WebDriverWait pour chaque élément
            gross_profit_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "#layout-scroll > div.absolute.inset-0.flex.flex-col > div.flex.flex-1.flex-col.gap-1.px-1\\.5.pt-2.pb-1.sm\\:gap-3.md\\:px-6.md\\:pb-2.md\\:pt-6 > div.no-scroll-bar.mt-0\\.5.w-full.overflow-x-auto.md\\:mt-1\\.5 > div > div:nth-child(1) > p"))
            )
            gross_profit = gross_profit_element.text

            realized_profit_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.grid > div:nth-child(1) > div:nth-child(3) > div:nth-child(1)"))
            )
            realized_profit = realized_profit_element.text

            unrealized_profit_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.grid > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)"))
            )
            unrealized_profit = unrealized_profit_element.text

            total_roi_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".gap-4 > div:nth-child(1) > p:nth-child(2)"))
            )
            total_roi = total_roi_element.text

            roi_realized_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".gap-4 > div:nth-child(1) > div:nth-child(3) > div:nth-child(1)"))
            )
            roi_realized = roi_realized_element.text

            roi_unrealized_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".gap-4 > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)"))
            )
            roi_unrealized = roi_unrealized_element.text

            win_rate_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-4:nth-child(3) > div:nth-child(2)"))
            )
            win_rate = win_rate_element.text

            win_realized_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-4:nth-child(3) > div:nth-child(3) > div:nth-child(1)"))
            )
            win_realized = win_realized_element.text

            win_unrealized_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-4:nth-child(3) > div:nth-child(3) > div:nth-child(2)"))
            )
            win_unrealized = win_unrealized_element.text

            # Afficher ou stocker les résultats
            print(f"Adresse: {adresse}")
            print(f"Gross Profit: {gross_profit}")
            print(f"Realized Profit: {realized_profit}")
            print(f"Unrealized Profit: {unrealized_profit}")
            print(f"Total ROI: {total_roi}")
            print(f"ROI Realized: {roi_realized}")
            print(f"ROI Unrealized: {roi_unrealized}")
            print(f"Win Rate: {win_rate}")
            print(f"Win: {win_realized}")
            print(f"Lose: {win_unrealized}")
            print("-" * 40)

            success = True  # Exit loop if successful

        except Exception as e:
            # Extraire uniquement le message d'erreur sans la stacktrace
            error_message = str(e).splitlines()[0]  # Obtenir le premier ligne du message d'erreur
            print(f"Erreur lors de la récupération des données pour l'adresse {adresse}: {error_message}")
            attempts += 1
            if attempts < max_attempts:
                print(f"Tentative {attempts} échouée. Réessai dans 5 secondes...")
                time.sleep(5)  # Attendre avant de réessayer
            else:
                print(f"Échec après {max_attempts} tentatives.")

        finally:
            driver.quit()

# Nom du fichier contenant les adresses
filename = "C:\\Users\\hugo\\Bureau\\Myfile.txt"

# Liste pour stocker les adresses extraites
adresses = []

# Ouvrir le fichier en mode lecture et extraire les adresses
with open(filename, "r") as fichier:
    for ligne in fichier:
        if "https://solscan.io/account/" in ligne:
            match = re.search(r"https://solscan.io/account/([A-Za-z0-9]+)", ligne)
            if match:
                adresses.append(match.group(1))

# Supprimer les doublons
adresses_uniques = list(set(adresses))

# Boucler sur les adresses uniques
for adresse in adresses_uniques:
    scrape_address(adresse)
