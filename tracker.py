import os
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, TimeoutException

# Load environment variables from.env file
from dotenv import load_dotenv
load_dotenv()


def track_package(tracking_number):
    # Configure WebDriver
    driver_path = os.getenv('CHROMEDRIVER_PATH', 'default_path_if_not_set')
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    # Initialize Chrome driver in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # Navigate to tracking page
        driver.get("https://www.zim.com/es/tools/track-a-shipment")

        # Wait for cookie acceptance button to be clickable and click
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

        # Simulate human-like mouse movement
        action = ActionChains(driver)
        tracking_input = wait.until(EC.presence_of_element_located((By.ID, "shipment-main-search-2")))
        action.move_to_element(tracking_input).click().perform()
        wait.until(EC.presence_of_element_located((By.ID, "shipment-main-search-2")))

        # Enter tracking number and press ENTER
        tracking_input.send_keys(tracking_number)
        tracking_input.send_keys(Keys.RETURN)

        # Wait for search results to load
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#trackShipment > div > div.routing-details")))

        # Extract data
        data_elements = driver.find_elements_by_css_selector("#trackShipment > div > div.routing-details")
        details = [element.text for element in data_elements]
        return details

    except (WebDriverException, TimeoutException) as e:
        print("Error loading:", e)
        return []

    finally:
        # Close the browser after the session
        driver.quit()

# Example function call
# track_package("ZIMUMER2451448")