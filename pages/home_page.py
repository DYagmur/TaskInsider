from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage(BasePage):
    URL = "https://useinsider.com/"
    COOKIE_BUTTON = (By.XPATH, "//*[@id='wt-cli-accept-all-btn']")
    COMPANY_MENU = (By.XPATH, "//a[@id='navbarDropdownMenuLink' and normalize-space(text())='Company']")
    CAREERS_MENU = (By.XPATH, "//a[@id='navbarDropdownMenuLink' and normalize-space(text())='Company']/following::a[text()='Careers'] ")

    def open_home_page(self):
        print("Opening the home page...")
        self.driver.get(self.URL)
        self.driver.maximize_window()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Insider"))
        print("Home page loaded successfully.")

    def accept_cookies(self):
        print("Accepting cookies...")
        self.click_element(*self.COOKIE_BUTTON)
        print("Cookies accepted.")

    def navigate_to_careers(self):
        print("Navigating to the 'Careers' page...")
        self.click_element(*self.COMPANY_MENU)  
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CAREERS_MENU))
        self.click_element(*self.CAREERS_MENU)
        WebDriverWait(self.driver, 10).until(EC.url_contains("/careers"))
        print("Successfully navigated to the 'Careers' page.")
