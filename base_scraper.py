from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC



class BaseScraper:
    def __init__(self, path) -> None:
        service = Service(path)
        self.driver = webdriver.Chrome(service=service)

    def retriev_positions(self, url, title_to_search, location) -> None:
        raise NotImplementedError("Subclass must implement abstract method")
        