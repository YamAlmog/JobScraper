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


CAREERS_URL ="https://careers.checkpoint.com/?q=&module=cpcareers&a=search&fa%5B%5D=country_ss%3AIsrael&fa%5B%5D=department_s%3AProducts%2520-%2520QA&fa%5B%5D=department_s%3AProducts%2520-%2520R%26D&fa%5B%5D=seniority_s%3AStudents%2FPart-time&fa%5B%5D=seniority_s%3AEntry%2520Level&sort="


class CheckPointScraper(BaseScraper):
    def __init__(self) -> None:    
        super().__init__(driver_path)
  

    def retrieve_positions(self):
        try:
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get(CAREERS_URL)
            self.driver.implicitly_wait(20)

             # Check if there are no positions available
            res_size_element = self.driver.find_element(By.ID, "resSize")
            res_size = res_size_element.text.strip()

            if res_size == "0":
                print("No positions found.")
                return []

            # Wait until the positions are loaded on the page
            #WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'resultsWrapper')))

            # Find all position elements
            positions = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "position")))
            
            return self.create_positions_list(positions)

        except Exception as e:
            print(f"An error occurred: {e}")
        
        input("Press Enter to close the browser...")
        self.driver.quit()

    def create_positions_list(self, positions):
        list_of_positions = []
        
        for position in positions:
            # Get title
            title_elem = position.find_element(By.TAG_NAME, "a")
            pos_title = title_elem.text
            
            # Get location
            location_elem = position.find_element(By.CSS_SELECTOR, ".posInfo p")
            pos_location = location_elem.text
             
            # Get link
            job_link = position.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            # Print or store the title, location, date, and description
            print(f"Title: {pos_title}, Location: {pos_location}")
            
            # Store position data
            position_data = Position(company="Check Point", title=pos_title, location=pos_location, link=job_link)
            list_of_positions.append(position_data)

        return list_of_positions

check_point_scraper = CheckPointScraper()
print(check_point_scraper.retrieve_positions())