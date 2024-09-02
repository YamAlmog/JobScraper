from models import Position
from typing import List
from microsoft_job_scraper import MicrosoftScraper
from nice_job_scraper import NiceScraper
from google_job_scraper import GoogleScraper
from check_point_scraper import CheckPointScraper

nice_scraper = NiceScraper()
check_point_scraper = CheckPointScraper()
msft_scraper = MicrosoftScraper()
google_scraper = GoogleScraper()

def main():
    def scan_all_job_platforms(list_of_scrapers: list) -> List[Position]:
        all_positions = []
        for scraper in list_of_scrapers:
            positions_list = scraper.retrieve_positions()
            all_positions += positions_list

        return all_positions


    def build_masage