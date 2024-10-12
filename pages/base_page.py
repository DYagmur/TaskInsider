from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def accept_cookies(self):
        """Accept cookies if the cookie banner is present."""
        try:
            
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/span/div/div[2]/a[1]')) 
            )
            cookie_button.click()
            print("Cookies accepted.")  
        except Exception as e:
            print(f"Could not accept cookies: {str(e)}")

    
            

    def wait_for_element(self, by, locator, timeout=10):
        """Waits for an element to be visible."""
        try:
            print(f"Waiting for element: {locator}")
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, locator)))
        except TimeoutException:
            print(f"Timeout: Element not found: {locator}")
            raise

    def wait_for_elements(self, by, locator, timeout=10):
        """Waits for multiple elements to be present."""
        try:
            print(f"Waiting for elements: {locator}")
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((by, locator)))
        except TimeoutException:
            print(f"Timeout: Elements not found: {locator}")
            raise

    def click_element(self, by, locator, timeout=10):
        """Clicks on an element when it's clickable."""
        try:
            element = self.wait_for_element(by, locator, timeout)
            print(f"Clicking element: {locator}")
            element.click()
        except TimeoutException:
            print(f"Failed to click element: {locator}")
            raise
