from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models import Position
from base_scraper import BaseScraper
from dotenv import load_dotenv
import os
import time
import random

load_dotenv(".env")
driver_path = os.getenv("CHROME_DRIVER_PATH")


CAREERS_URL = "https://www.linkedin.com/jobs/search/?currentJobId=4010499766&distance=25&f_E=1%2C2&f_T=9%2C25194%2C25201%2C8950&f_TPR=r86400&f_WT=1%2C3&geoId=101620260&keywords=junior%20software%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD&spellCorrectionEnabled=true"

class LinkedInScraper(BaseScraper):
    def __init__(self) -> None:    
        # Set Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
        
        # Pass the options to the BaseScraper
        super().__init__(driver_path, options=options)
  

    def retrieve_positions(self, url):
        try:
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get(url)
            self.driver.implicitly_wait(20)


            # Find all position elements
            positions = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "base-search-card")))
            
            return self.create_positions_list(positions)

        except Exception as e:
            print(f"An error occurred: {e}")
        
        input("Press Enter to close the browser...")
        self.driver.quit()

    def create_positions_list(self, positions):
        list_of_positions = []
        
        for position in positions:
            time.sleep(random.uniform(0.5, 2))
            # Get title
            pos_title = position.find_element(By.CLASS_NAME, "base-search-card__title").text
            
            # Get location
            pos_location = position.find_element(By.CLASS_NAME, "job-search-card__location").text
            
            # Get link
            job_link = position.get_attribute('href')
            
            # Get the job posting time
            posted_time = position.find_element(By.TAG_NAME, "time").text


            # Print or store the title, location, date, and description
            print(f"Title: {pos_title}, Location: {pos_location}")
            
            # Store position data
            position_data = Position(title=pos_title, location=pos_location, link=job_link, posted_date=posted_time)
            list_of_positions.append(position_data)

        return list_of_positions

linkedin_scraper = LinkedInScraper()
print(linkedin_scraper.retrieve_positions(CAREERS_URL))