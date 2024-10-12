from selenium.webdriver.common.by import By
from .base_page import BasePage
import time  

class CareersPage(BasePage):
    LOCATIONS_SECTION = (By.XPATH, "//p[text()='New York']")
    TEAMS_SECTION = (By.XPATH, "//*[@id='career-find-our-calling']/div/div/a")
    LIFE_AT_SECTION = (By.XPATH, "//h2[text()='Life at Insider']")

    def scroll_to_element(self, element):
        """Helper function to scroll to an element"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(4) 

    def verify_sections_visible(self):
        print("Verifying 'Teams', 'Locations', and 'Life at Insider' sections...")

    # Verify Teams Section
        try:
            teams_element = self.wait_for_element(*self.TEAMS_SECTION)
            self.scroll_to_element(teams_element)
            assert teams_element.is_displayed(), "Teams section is not visible"
            print("Teams section is visible.")
        except Exception as e:
            print(f"Error verifying Teams section: {str(e)}")

    # Verify Locations Section
        try:
            locations_element = self.wait_for_element(*self.LOCATIONS_SECTION)
            self.scroll_to_element(locations_element)
            assert locations_element.is_displayed(), "Locations section is not visible"
            print("Locations section is visible.")
        except Exception as e:
            print(f"Error verifying Locations section: {str(e)}")

    # Verify Life at Insider Section
        try:
            life_at_element = self.wait_for_element(*self.LIFE_AT_SECTION)
            self.scroll_to_element(life_at_element)
            assert life_at_element.is_displayed(), "Life at Insider section is not visible"
            print("Life at Insider section is visible.")
        except Exception as e:
            print(f"Error verifying Life at Insider section: {str(e)}")

