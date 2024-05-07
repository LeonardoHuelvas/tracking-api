import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

# Carga las variables de entorno del archivo .env
from dotenv import load_dotenv
load_dotenv()

def track_package(tracking_number):
    driver_path = os.getenv('CHROMEDRIVER_PATH')
    print(f"Ruta de Chromedriver: {driver_path}")
    
    # Inicializa el Service con la ruta del chromedriver
    service = Service(executable_path=driver_path)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Modo sin interfaz gráfica
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    # Inicializa el navegador Chrome con el Service y las opciones configuradas
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get("https://www.zim.com/es/tools/track-a-shipment")
        time.sleep(random.randint(2, 5))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
        action = ActionChains(driver)
        tracking_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "shipment-main-search-2"))
        )
        action.move_to_element(tracking_input).click().perform()
        time.sleep(random.uniform(0.5, 1.5))
        tracking_input.send_keys(tracking_number)
        tracking_input.send_keys(Keys.RETURN)
        time.sleep(2)
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.chips-search-button"))
        )
        follow_button.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#trackShipment > div > div.routing-details"))
        )
        data_elements = driver.find_elements(By.CSS_SELECTOR, "#trackShipment > div > div.routing-details")
        details = [element.text for element in data_elements]
        return details
    except Exception as e:
        print("Error al cargar:", e)
        return []
    finally:
        driver.quit()

# Example function call
# track_package("ZIMUMER2451448")
