from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import time

class QAJobsPage(BasePage):
    QA_URL = "https://useinsider.com/careers/quality-assurance/"
    QA_JOBS_BUTTON = (By.XPATH, '//a[normalize-space(text())="See all QA jobs"]')
    LOCATION_FILTER = (By.XPATH, "//span[@id='select2-filter-by-location-container']")
    CITY_SELECTION = (By.XPATH, "//li[@id='select2-filter-by-location-result-2vur-Istanbul, Turkey']")
    JOBS_LIST = (By.XPATH, '//*[@id="jobs-list"]/div/div')
    VIEW_ROLE_BUTTONS = (By.XPATH, "//a[normalize-space(text())='View Role']")
    CHECK_RESULT_COUNTER = (By.XPATH, '//*[@id="resultCounter"]')
    APPLY_FOR_JOB = (By.XPATH, "//a[text()='Apply for this job']")
    APPLICATION_FORM = (By.XPATH, "//form[@id='application-form']")


    def go_to_qa_jobs(self):
        print("Navigating directly to QA Jobs page...")
        self.driver.get(self.QA_URL)
        self.accept_cookies()
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.QA_JOBS_BUTTON))
            print("QA Jobs page loaded successfully.")
        except TimeoutException:
            print("QA Jobs page did not load within the expected time.")
            raise

    def click_see_all_qa_jobs(self):
        try:
            self.wait_for_element(*self.QA_JOBS_BUTTON, timeout=10)
            self.click_element(*self.QA_JOBS_BUTTON)
            print("'See all QA jobs' button clicked, jobs page opened.")
        except Exception as e:
            print(f"Failed to click 'See all QA jobs' button: {str(e)}")
            raise

    def click_location_filter(self):
        """Click the location filter and select a city using JavaScript."""
        try:
            print("Waiting for the page to load...")
            time.sleep(3)  
            self.driver.execute_script("window.scrollBy(0, 500);")
            print("Page scrolled down by 500 pixels.")
            time.sleep(10)  
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.CHECK_RESULT_COUNTER))
            print("CHECK_RESULT_COUNTER is visible.")
            time.sleep(20) 

            option1 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOCATION_FILTER)
            )
            option1.click()
            time.sleep(10) 

            option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//ul[@id='select2-filter-by-location-results']/li[text()='Istanbul, Turkey']"))
            )
            option.click()
            time.sleep(5) 
            print()
        except TimeoutException:
            print("CHECK_RESULT_COUNTER, LOCATION_FILTER, or CITY_SELECTION is not visible: timed out.")
            raise
        except Exception as e:
            print(f"An error occurred while selecting the city: {str(e)}")
            raise
        
    def verify_jobs_display(self):
        print("Verifying QA jobs are displayed...")
        job_elements = self.driver.find_elements(*self.JOBS_LIST)
        WebDriverWait(self.driver, 10).until(lambda d: len(job_elements) > 0)

        for job in job_elements:
            position = job.find_element(By.XPATH, ".//p[contains(@class, 'position-title')]").text
            department = job.find_element(By.XPATH, ".//span[contains(@class, 'position-department')]").text
            location = job.find_element(By.XPATH, ".//div[contains(@class, 'position-location')]").text

            assert "Quality Assurance" in position, f"Position '{position}' does not contain 'Quality Assurance'"
            assert "Quality Assurance" in department, f"Department '{department}' does not contain 'Quality Assurance'"
            assert "Istanbul, Turkey" in location, f"Location '{location}' does not contain 'Istanbul, Turkey'"



    def verify_view_role_redirect_and_apply(self):
       
        original_window = self.driver.current_window_handle
        view_role_buttons = self.driver.find_elements(*self.VIEW_ROLE_BUTTONS)

        for button in view_role_buttons:
            button.click()
            print("View role button is clicked")

            
            WebDriverWait(self.driver, 10).until(EC.new_window_is_opened)
            
            
            all_windows = self.driver.window_handles

            
            for window in all_windows:
                if window != original_window:
                    self.driver.switch_to.window(window)
                    print("Yeni sekmeye geçiş yapıldı.")
                    break

            try:
                
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.APPLY_FOR_JOB)
                )
                self.driver.find_element(*self.APPLY_FOR_JOB).click()
                print("Apply for this job button clicked.")
                time.sleep(8)
                
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.APPLICATION_FORM)
                )
                time.sleep(4)
                print("Application form is visiable")
            except TimeoutException:
                print("Apply for this job button bulunamadı veya zaman aşımına uğradı.")
                raise
            except Exception as e:
                print(f"Bir hata oluştu: {str(e)}")
                raise
            time.sleep(10)  
                
           
