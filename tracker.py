import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

def track_package(tracking_number):
    """
    Realiza el seguimiento de un paquete utilizando Selenium.

    Parámetros:
    tracking_number (str): Número de seguimiento del paquete.

    Retorna:
    list: Detalles del seguimiento del paquete.
    """
    # Obtener la ruta del archivo chromedriver
    driver_path = os.path.join(os.getcwd(), 'driver', 'chromedriver.exe')

    # Verificar si el archivo chromedriver existe
    if not os.path.exists(driver_path):
        raise FileNotFoundError("El archivo chromedriver no existe en la ruta especificada.")

    # Configurar el servicio y las opciones del navegador Chrome
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en modo sin cabeza
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Deshabilitar las características de blink controladas por automatización
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # Excluir los interruptores de habilitar la automatización
    options.add_experimental_option('useAutomationExtension', False)  # No usar la extensión de automatización

    # Inicializar el navegador Chrome
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # Ocultar la detección de Selenium

    try:
        # Acceder al sitio web de seguimiento de paquetes
        driver.get("https://www.zim.com/es/tools/track-a-shipment")
        time.sleep(random.randint(2, 5))  # Esperar un tiempo aleatorio para simular comportamiento humano

        # Aceptar las cookies si es necesario
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

        # Realizar acciones de mouse para ingresar el número de seguimiento
        action = ActionChains(driver)
        tracking_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "shipment-main-search-2")))
        action.move_to_element(tracking_input).click().perform()
        time.sleep(random.uniform(0.5, 1.5))  # Esperar un tiempo aleatorio
        tracking_input.send_keys(tracking_number)  # Ingresar el número de seguimiento
        tracking_input.send_keys(Keys.RETURN)  # Presionar Enter

        # Esperar a que se carguen los resultados del seguimiento
        time.sleep(2)  # Esperar un tiempo fijo
        follow_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.chips-search-button")))
        follow_button.click()  # Hacer clic en el botón de seguimiento
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#trackShipment > div > div.routing-details")))  # Esperar a que se carguen los detalles de seguimiento

        # Extraer los detalles del seguimiento
        data_elements = driver.find_elements(By.CSS_SELECTOR, "#trackShipment > div > div.routing-details")
        details = [element.text for element in data_elements]

        return details  # Retornar los detalles del seguimiento
    except Exception as e:
        print("Error al cargar:", e)  # Imprimir cualquier error que ocurra durante el proceso
        return []  # Retornar una lista vacía en caso de error
    finally:
        driver.quit()  # Cerrar el navegador después de realizar el seguimiento del paquete
