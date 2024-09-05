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


class ManageScrapersMessages:

    def scan_all_job_platforms(self, list_of_scrapers: list) -> List[Position]:
        all_positions = []
        for scraper in list_of_scrapers:
            positions_list = scraper.retrieve_positions()
            all_positions += positions_list

        return all_positions



    def build_message(self, position: Position) -> str:
        message = {
                    'Company': position.company,
                    'Job title': position.title,
                    'Location': position.location,
                    'Link for the job': position.link,
                    'Job description': position.description,
                    'Posted date': position.posted_date
                }
        return message


    def combine_all_job_messages(self):
        list_of_scrapers = [nice_scraper, check_point_scraper, msft_scraper, google_scraper]
        all_positions = self.scan_all_job_platforms(list_of_scrapers)
        result = []
        for position in all_positions:
            message = self.build_message(position)
            result.append(message)
        
        return result


        
    
def main():
    massage_manager = ManageScrapersMessages()
    messages = massage_manager.combine_all_job_messages()
    for msg in messages:
        print(msg)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()