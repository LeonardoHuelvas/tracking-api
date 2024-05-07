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

# Función para el número de guía ingresada
def track_package(tracking_number):
    driver_path = os.getenv('CHROMEDRIVER_PATH')
    print(f"Ruta de Chromedriver: {driver_path}")
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    # Habilitar el modo headless
    options.add_argument("--headless")  # Importante para ejecución sin GUI

    # User-Agent para imitar un navegador real
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    # Configuración para evitar la detección
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    # Inicializa el navegador Chrome en modo headless
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # Navega a la página de seguimiento
        driver.get("https://www.zim.com/es/tools/track-a-shipment")
        
        # Introduce variaciones en el tiempo de espera para simular comportamiento humano
        time.sleep(random.randint(2, 5))
        
        # Espera hasta que el botón de aceptación de cookies sea clickeable y haz clic
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()

        # Movimiento humano del mouse
        action = ActionChains(driver)
        tracking_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "shipment-main-search-2"))
        )
        action.move_to_element(tracking_input).click().perform()
        time.sleep(random.uniform(0.5, 1.5))

        # Introduce el número y presiona ENTER
        tracking_input.send_keys(tracking_number)
        tracking_input.send_keys(Keys.RETURN)

        # Espera un poco antes de intentar hacer clic en seguir
        time.sleep(2)

        # Intenta hacer clic en el botón de búsqueda
        try:
            follow_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.chips-search-button"))
            )
            follow_button.click()
        except WebDriverException as e:
            print("No se pudo hacer clic en el botón de seguimiento:", e)

        # Espera hasta que los resultados sean cargados
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#trackShipment > div > div.routing-details"))
        )

        # Extrae los datos
        data_elements = driver.find_elements(By.CSS_SELECTOR, "#trackShipment > div > div.routing-details")
        details = [element.text for element in data_elements]
        return details

    except Exception as e:
        print("Error al cargar:", e)
        return []

    finally:
        # Cierra el navegador después de la sesión
        driver.quit()

# Example function call
# track_package("ZIMUMER2451448")
