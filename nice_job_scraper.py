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

load_dotenv(".env")
driver_path = os.getenv("CHROME_DRIVER_PATH")


CAREERS_URL = "https://www.nice.com/careers/apply?categories=27&search=student&locations=30"

class NiceScraper(BaseScraper):
    def __init__(self) -> None:    
        super().__init__(driver_path)
  

    def retrieve_positions(self):
        try:
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get(CAREERS_URL)
            self.driver.implicitly_wait(20)

            # Wait until the positions are loaded on the page
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tab-content')))

            # Check if there are any available positions
            result_count_elem = self.driver.find_element(By.ID, "results")
            positions = result_count_elem.find_elements(By.CLASS_NAME, 'result-item')

            if not positions:
                print("No positions found.")
                return []
            
            return self.create_positions_list(positions)

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

        finally:
            self.driver.quit()

    def create_positions_list(self, positions):
        list_of_positions = []
        
        for position in positions:
            # Get title
            title_elem = position.find_element(By.TAG_NAME, 'h4')
            pos_title = title_elem.text
            
            # Get location
            location_elem = position.find_element(By.TAG_NAME, 'p')
            pos_location = location_elem.text
            
            # Get link
            job_link = position.get_attribute('href')
            
            # Store position data
            position_data = Position(company="Nice", title=pos_title, location=pos_location, link=job_link)
            list_of_positions.append(position_data)

        return list_of_positions

nice_scraper = NiceScraper()
print(nice_scraper.retrieve_positions())