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

# Microsoft careers params
CAREERS_URL = "https://jobs.careers.microsoft.com/global/en/search?q=software%20engineer&lc=Israel&exp=Students%20and%20graduates&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true"


class MicrosoftScraper(BaseScraper):
    def __init__(self) -> None:    
        super().__init__(driver_path)


    def retrieve_positions(self):
        try:
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get(CAREERS_URL)
            self.driver.implicitly_wait(10)
            # Wait until the positions are loaded on the page
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ms-List-cell')))

            # Find all position elements
            positions = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ms-List-cell')))
            
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
            title_elem = position.find_element(By.CLASS_NAME, 'MZGzlrn8gfgSs8TZHhv2')
            pos_title = title_elem.text
            
            # Get location
            location_elem = position.find_element(By.XPATH, ".//i[@data-icon-name='POI']/following-sibling::span")
            pos_location = location_elem.text
            
            # Get posted date
            date_elem = position.find_element(By.XPATH, ".//i[@data-icon-name='Clock']/following-sibling::span")
            pos_date = date_elem.text
            
            # Get job description
            description_elem = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-537')))
            pos_description = description_elem.text
            
            # Store position data
            position_data = Position(company="Microsoft", title=pos_title, location=pos_location, posted_date=pos_date, description=pos_description)
            list_of_positions.append(position_data)

        return list_of_positions

msft_scraper = MicrosoftScraper()
print(msft_scraper.retrieve_positions())