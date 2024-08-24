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

# Google careers params
CAREERS_URL = 'https://www.google.com/about/careers/applications/'
TITLE_FIELD_ID = 'i6'
LOCATION_FIELD_ID = 'c4'
POSITIONS_XPATH = '/html/body/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/ul'
CLICK_SEARCH_BUTTON = '//*[@id="hero-section"]/div[1]/div[1]/div[1]/form/div[1]/div[3]/button'


class GoogleScraper(BaseScraper):
    def __init__(self) -> None:    
        super().__init__(driver_path)

    def retriev_positions(self, url, title_to_search, location):
        try:
            self.driver.get(url)
            
            # Wait until the title field is present
            title_search_field_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, TITLE_FIELD_ID))
            )
            title_search_field_elem.send_keys(title_to_search)
            
            # Wait until the location field is present
            location_search_field_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, LOCATION_FIELD_ID))
            )
            location_search_field_elem.send_keys(location)

            time.sleep(1)
            
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="c10"]/span[3]'))
            ).click()

            # Click the search button
            click_search_field_elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, CLICK_SEARCH_BUTTON))
            )


            click_search_field_elem.click()

            time.sleep(1)

            # Retrieve all positions
            list_of_positions = []
            # all_positions = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_all_elements_located((By.XPATH, POSITIONS_XPATH))
            # )
            all_positions_element = self.driver.find_element(By.XPATH, POSITIONS_XPATH)
            positions = all_positions_element.find_elements(By.XPATH, './*')

            for position in positions:

                # print(f"-------------------------------\n {position.text} \n-------------------------------")
                print('Location: ' + position.find_element(By.CLASS_NAME, 'r0wTof ').text)
                continue
                
                title_elem = position.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/ul/li[3]/div/div/div[1]/div/div[1]/div')
                pos_title = title_elem.text
                print(f"position title: {pos_title}")
                
                location_elem = position.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/ul/li[3]/div/div/div[1]/div/div[3]/p/span')
                pos_location = location_elem.text
                print(f"position location: {pos_location}")
                
                position = Position(title=pos_title, location=pos_location)
                list_of_positions.append(position)
            return list_of_positions

        except Exception as e:
            print(f"An error occurred: {e}")



google_scraper = GoogleScraper()
google_scraper.retriev_positions(CAREERS_URL, 'software engineer', 'Israel')