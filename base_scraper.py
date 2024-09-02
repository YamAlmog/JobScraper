from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional


class BaseScraper:
    def __init__(self, path, options=None) -> None:
        service = Service(path)
        # Pass options to the WebDriver if provided
        self.driver = webdriver.Chrome(service=service, options=options)

    def retrieve_positions(self, url:str, title_to_search:Optional[str] = None, location:Optional[str] = None) -> None:
        raise NotImplementedError("Subclass must implement abstract method")
        