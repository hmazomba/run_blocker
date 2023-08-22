from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)

class TenderScraper:
    def __init__(self):
        self.base_url = "https://easytenders.co.za/tenders"
        self.logger = logging.getLogger(__name__)

    def fetch_tender_details(self, search_term, num_searches):
        result = []
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            tenders = soup.find_all("div", class_="tender")

            for tender in tenders:
                department = tender.find("div", class_="text-info").text.strip()
                description = tender.find("div", class_="pt-1").text.strip()

                if search_term.lower() in description.lower():
                    result.append({
                        "department": department,
                        "description": description
                    })

                    if len(result) == num_searches:
                        break

        except requests.exceptions.RequestException as e:
            self.logger.error("Error fetching tenders: %s", e)
        
        return result

tender_scraper = TenderScraper()

@app.route('/tenders', methods=['GET'])
def get_tenders():
    search_term = request.args.get('search_term')
    num_searches = int(request.args.get('num_searches'))
    
    tenders = tender_scraper.fetch_tender_details(search_term, num_searches)
    return {"tenders": tenders}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run()
