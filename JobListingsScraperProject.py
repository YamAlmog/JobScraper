import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pdb

# base on this site: http://demostore.supersqa.com/




class JobsWebScraping:
    def __init__(self) -> None:
        # Create a new instance of the WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        PATH =  "C:\Program Files (x86)\chromedriver.exe"
        service = Service(PATH)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(8)


    def filter_Jobs_by_title_and_location_Indeed(self, title:str, location:str):
        try:
            self.driver.get("https://il.indeed.com/?r=us")
            self.driver.implicitly_wait(10)

            # Wait until the job title field is present
            job_title_field_id = "text-input-what"
            job_title_search_field = self.driver.find_element(By.ID, job_title_field_id)
            
            job_title_search_field.send_keys(title)
            self.driver.implicitly_wait(10)
            
            # Wait until the location field is present
            location_field_id = "text-input-where"
            location_search_field = self.driver.find_element(By.ID, location_field_id)
            location_search_field.clear()  # Clear the field if it has a default value
            location_search_field.send_keys(location)
            self.driver.implicitly_wait(8)
            
            # Press Enter in the location search field to submit the form
            location_search_field.send_keys(Keys.RETURN)
            self.driver.implicitly_wait(8)
            
            time.sleep(5)  # Wait for results to load (increase if needed)
        
        except Exception as e:
            print(f"An error occurred: {e}")



    def filter_Jobs_by_title_and_location_GlassDoor(self, title: str, location: str):
        try:
            self.driver.get("https://www.glassdoor.com/Job/index.htm")
            self.driver.implicitly_wait(8)

            # Wait until the title field is present
            title_field_id = "searchBar-jobTitle"
            title_search_field_elem = self.driver.find_element(By.ID, title_field_id)
            title_search_field_elem.send_keys(title)
            
            time.sleep(5) 

            # Wait until the location field is present
            location_field_id = "searchBar-location"
            location_search_field_elem = self.driver.find_element(By.ID, location_field_id)
            location_search_field_elem.send_keys(location)
            
            time.sleep(5) 
            
            # Press Enter in the location search field to submit the form
            location_search_field_elem.send_keys(Keys.RETURN)
            self.driver.implicitly_wait(8)
            
            
            time.sleep(5)  # Wait for results to load (increase if needed)
        except Exception as e:
            print(f"An error occurred: {e}")
             

    def extract_all_positions(self):
        
        list_of_positions = []
        all_positions = self.driver.find_elements(By.XPATH, '//*[@id="left-column"]/div[2]')
        self.driver.implicitly_wait(8)
        print(f"Number of positions: {len(all_positions)}")
        for position in all_positions:
            print(position.text)
        
        #     price_elem = product.find_element(By.CSS_SELECTOR, 'span.amount')
        #     price = price_elem.text
        #     name_elem = product.find_element(By.CSS_SELECTOR, 'h2.woocommerce-loop-product__title')
        #     name = name_elem.text
        #     print(f"Product name: {name}")
        #     print(f"Product price: {price}")
        #     list_of_product_prices.append({'name':name, 'price':price})
        # return list_of_product_prices

def main():
    job_scraper = JobsWebScraping()
    job_scraper.filter_Jobs_by_title_and_location_GlassDoor("software engineer", "Israel")
    #job_scraper.filter_Jobs_by_title_and_location_Indeed("software engineer", "Israel")
    time.sleep(10)
    job_scraper.extract_all_positions()
    time.sleep(5)
if __name__ == "__main__":
    main()


