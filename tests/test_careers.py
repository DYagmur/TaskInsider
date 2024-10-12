import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_jobs_page import QAJobsPage
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.base_page import BasePage

class TestCareers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up the test environment...")
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Disable the sandbox
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")

         
        # Initialize the WebDriver with options
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.maximize_window()
        cls.base_page = BasePage(cls.driver)
        print("Test environment set up successfully.")
        
    @classmethod
    def tearDownClass(cls):
        print("Tearing down the test environment...")
        cls.driver.quit()
        print("Test environment torn down successfully.")

    def test_a_home_page(self):
        print("Starting test: test_home_page")
        home_page = HomePage(self.driver)
        home_page.open_home_page()
        home_page.accept_cookies()
        print("test_home_page completed.")

    def test_careers_page_sections(self):
        print("Starting test: test_careers_page_sections")

        try:
            home_page = HomePage(self.driver)
            home_page.navigate_to_careers()
            print("Navigated to Careers page.")
        except Exception as e:
            print(f"Error navigating to Careers page: {str(e)}")
    
        try:
            careers_page = CareersPage(self.driver)
            careers_page.verify_sections_visible()
            print("test_careers_page_sections completed successfully.")
        except Exception as e:
            print(f"Test failed: {str(e)}")
                
        
            
        qa_jobs_page = QAJobsPage(self.driver)
        qa_jobs_page.go_to_qa_jobs()  # Navigate directly to QA Jobs page
        qa_jobs_page.click_see_all_qa_jobs()
        qa_jobs_page.click_location_filter()
        qa_jobs_page.verify_jobs_display()
        qa_jobs_page.verify_view_role_redirect_and_apply()
    

                

if __name__ == "__main__":
    unittest.main()
